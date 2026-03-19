"""REST client handling, including IntercomStream base class."""

from __future__ import annotations

import logging
import time
import typing as t

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import BaseHATEOASPaginator, JSONPathPaginator
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests

T = t.TypeVar("T")
TPageToken = t.TypeVar("TPageToken")

LOGGER = logging.getLogger(__name__)


class IntercomStream(RESTStream):
    """Intercom stream class."""

    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.data[*]"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.intercom.io"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return the authenticator."""
        return BearerTokenAuthenticator(token=self.config["access_token"])

    @property
    def http_headers(self) -> dict:
        """Return headers dict to be used for HTTP requests.

        If an authenticator is also specified, the authenticator's headers will be
        combined with `http_headers` when making HTTP requests.

        Returns:
            Dictionary of HTTP headers to use as a base for every request.
        """
        result = self._http_headers
        user_agent = self.config.get("user_agent")
        if user_agent:
            result["User-Agent"] = user_agent
        result["Content-Type"] = "application/json"
        result["Intercom-Version"] = "2.14"
        return result

    def get_url_params(self, context: dict | None, next_page_token: object) -> dict:  # noqa: ARG002
        """Return URL params for the request.

        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token for next page of data.

        Returns:
            Dictionary of URL parameters.
        """
        params = {}
        if self.http_method == "GET":
            params = {"per_page": 150}
        return params

    def prepare_request_payload(
        self,
        context: dict | None,
        next_page_token: object,
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Developers may override this method if the API requires a custom payload along
        with the request. (This is generally not required for APIs which use the
        HTTP 'GET' method.)

        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token, page number or any request argument to request the
                next page of data.
        """
        if self.http_method == "POST":
            body = {}
            start_date = self.get_starting_replication_key_value(context)
            signpost = self.get_replication_key_signpost(context)

            if start_date or signpost or self.config.get("filters", {}).get(self.name):
                body["query"] = {
                    "operator": "AND",
                    "value": [
                        {"field": f["field"], "operator": f["operator"], "value": f["value"]}
                        for f in self.config.get("filters", {}).get(self.name, [])
                    ],
                }
                if start_date:
                    if start_date != self.config.get("start_date"):
                        start_date -= int(self.config["replication_lookback_window_seconds"])
                    body["query"]["value"].append(
                        {
                            "field": self.replication_key,
                            "operator": ">",
                            "value": start_date,
                        },
                    )
                if signpost:
                    # Freeze the extraction window for this sync to reduce cursor churn
                    # on rapidly mutating datasets.
                    body["query"]["value"].append(
                        {
                            "field": self.replication_key,
                            "operator": "<",
                            "value": signpost + 1,
                        },
                    )
            if next_page_token:
                body["pagination"] = {"per_page": 150, "starting_after": next_page_token}
            return body
        return None

    def compare_start_date(self, value: str, start_date_value: str) -> str:
        """Compare a bookmark value to a start date and return the most recent value.

        Args:
            value: The replication key value.
            start_date_value: The start date value from the config.

        Returns:
            The most recent value between the bookmark and start date.
        """
        return max(value, start_date_value)

    def get_replication_key_signpost(
        self,
        context: dict | None,  # noqa: ARG002
    ) -> int | None:
        """Overrides the signpost to be the Unix integer at sync start for incremental streams.

        This enables the SDK to finalize state as the lower of max(replication_key_value)
        seen during the run and the run start time.

        Args:
            context: Stream partition or context dictionary.

        Returns:
            Unix timestamp signpost for integer replication keys, else None.
        """
        if not self.replication_key:
            return None

        signpost = getattr(self, "_replication_key_signpost", None)
        if signpost is None:
            signpost = int(time.time())
            self._replication_key_signpost = signpost
            self.logger.info("Setting replication key signpost to current Unix timestamp at sync start.")
            self.logger.info("Signpost value: %s", signpost)
        return signpost

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: Individual record in the stream.
            context: Stream partition or context dictionary.

        Returns:
            The resulting record dict, or `None` if the record should be excluded.
        """
        if row.get("custom_attributes"):
            row["custom_attributes"] = {
                key.lower().replace(" ", "_"): value for key, value in row["custom_attributes"].items()
            }
        return row

    def get_new_paginator(self) -> JSONPathPaginator:
        """Return a new paginator instance for the stream.

        Returns:
            JSONPathPaginator: Paginator for handling paginated API responses.
        """
        return IntercomSearchPaginator(
            "$.pages.next.starting_after",
            logger=self.logger,
        )


class IntercomSearchPaginator(JSONPathPaginator):
    """JSONPath paginator with loop protection for repeated cursor tokens.

    Some Intercom search endpoints can return cursor sequences that revisit
    previously seen tokens (for example: A -> B -> A -> B) when the underlying
    dataset is changing quickly. The base paginator only detects consecutive
    repeats, so we guard against any previously seen cursor to prevent infinite
    loops.
    """

    def __init__(
        self,
        jsonpath: str,
        *args: t.Any,
        logger: logging.Logger | None = None,
        **kwargs: t.Any,
    ) -> None:
        """Create a new guarded paginator."""
        super().__init__(jsonpath, *args, **kwargs)
        self._logger = logger or LOGGER
        self._seen_tokens: set[t.Any] = set()

    def advance(self, response: requests.Response) -> None:
        """Advance the page token and stop gracefully if a token repeats."""
        self._page_count += 1

        if not self.has_more(response):
            self._finished = True
            return

        new_value = self.get_next(response)

        if new_value and new_value in self._seen_tokens:
            self._logger.warning(
                "Loop detected in pagination. Token %s was seen earlier (page %s). "
                "Stopping pagination for this stream to avoid an infinite loop.",
                new_value,
                self._page_count,
            )
            self._finished = True
            return

        if not new_value:
            self._finished = True
            return

        self._seen_tokens.add(new_value)
        self._value = new_value


class IntercomHATEOASPaginator(BaseHATEOASPaginator):
    """Paginator class for Intercom API using HATEOAS links."""

    def get_next_url(self, response: requests.Response) -> str | None:
        """Extract the next page URL from the API response.

        Args:
            response: The HTTP response object.

        Returns:
            The next page URL as a string, or None if there is no next page.
        """
        return response.json().get("pages").get("next")

    def has_more(self, response: requests.Response) -> bool:
        """Determine if there are more pages to fetch.

        Args:
            response: The HTTP response object.

        Returns:
            True if there are more pages, False otherwise.
        """
        return self.get_next_url(response) is not None
