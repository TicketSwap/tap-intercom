"""REST client handling, including IntercomStream base class."""

from __future__ import annotations

import typing as t

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import BaseHATEOASPaginator, JSONPathPaginator
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests

T = t.TypeVar("T")
TPageToken = t.TypeVar("TPageToken")


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
            body = {"sort": {"field": self.replication_key, "order": "ascending"}}
            start_date = self.get_starting_replication_key_value(context)
            if start_date or self.config.get("filters", {}).get(self.name):
                body["query"] = {
                    "operator": "AND",
                    "value": [
                        {"field": f["field"], "operator": f["operator"], "value": f["value"]}
                        for f in self.config.get("filters", {}).get(self.name, [])
                    ],
                }
                if start_date:
                    body["query"]["value"].append(
                        {
                            "field": self.replication_key,
                            "operator": ">",
                            "value": start_date,
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
        return JSONPathPaginator(jsonpath="$.pages.next.starting_after")


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
