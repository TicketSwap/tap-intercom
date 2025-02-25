"""REST client handling, including IntercomStream base class."""

from __future__ import annotations

import sys
import typing
from datetime import datetime
from pathlib import Path
from typing import Callable

T = typing.TypeVar("T")
TPageToken = typing.TypeVar("TPageToken")
_TToken = typing.TypeVar("_TToken")

import requests
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.streams import RESTStream

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class IntercomStream(RESTStream):
    """Intercom stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.intercom.io"

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.pages.next.starting_after"  # noqa: S105

    @property
    def authenticator(self):
        """Return the authenticator."""
        return BearerTokenAuthenticator.create_for_stream(self, token=self.config.get("access_token"))

    @property
    def http_headers(self) -> dict:
        """Return headers dict to be used for HTTP requests.

        If an authenticator is also specified, the authenticator's headers will be
        combined with `http_headers` when making HTTP requests.

        Returns:
            Dictionary of HTTP headers to use as a base for every request.
        """
        result = self._http_headers
        if "user_agent" in self.config:
            result["User-Agent"] = self.config.get("user_agent")
        result["Content-Type"] = "application/json"
        result["Intercom-Version"] = "2.11"
        return result

    def get_url_params(self, context, next_page_token):
        params = {}
        if self.rest_method == "GET":
            params = {"per_page": 150}
        return params

    def prepare_request_payload(
        self,
        context: dict | None,
        next_page_token: _TToken | None,
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
        if self.rest_method == "POST":
            body = {"sort": {"field": "updated_at", "order": "ascending"}}
            start_date = self.get_starting_replication_key_value(context)
            if start_date:
                if type(start_date) is str:
                    start_date = int(datetime.timestamp(datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")))
                filters = [
                    {"field": f["field"], "operator": f["operator"], "value": f["value"]}
                    for f in self.config.get("filters", {}).get(self.name, [])
                ]
                body["query"] = {
                    "operator": "AND",
                    "value": [
                        {"field": "created_at", "operator": ">", "value": start_date},
                        *filters,
                    ],
                }
            if next_page_token:
                body["pagination"] = {"per_page": 150, "starting_after": next_page_token}
            self.logger.info(body)
            return body
        return None
