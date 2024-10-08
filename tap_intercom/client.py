"""REST client handling, including IntercomStream base class."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Iterable
import typing
import base64
from urllib.parse import urlencode
from datetime import datetime
from urllib.parse import parse_qsl

T = typing.TypeVar("T")
TPageToken = typing.TypeVar("TPageToken")
_TToken = typing.TypeVar("_TToken")

import requests
from requests import Response
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BasePageNumberPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream
from singer_sdk.pagination import BaseOffsetPaginator


if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class IntercomPaginator(BaseOffsetPaginator):
    def has_more(self, response: Response) -> bool:  # noqa: ARG002
        """Override this method to check if the endpoint has any pages left.

        Args:
            response: API response object.

        Returns:
            Boolean flag used to indicate if the endpoint has more pages.
        """
        return response.json().get("pages", {}).get("next") != None

    def get_next(self, response: Response) -> TPageToken | None:
        """Get the next pagination token or index from the API response.

        Args:
            response: API response object.

        Returns:
            The next page token or index. Return `None` from this method to indicate
                the end of pagination.
        """
        return response.json().get("pages", {}).get("next", {}).get("starting_after")


class IntercomStream(RESTStream):
    """Intercom stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.intercom.io"

    records_jsonpath = "$[*]"  # Or override `parse_response`.

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

    def get_new_paginator(self) -> BaseOffsetPaginator:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return IntercomPaginator(page_size=150, start_value=None)
    
    def parse_response(self, response: Response) -> Iterable[dict]:
        self.logger.info(response.json().get("pages", {}))
        return super().parse_response(response)
    
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
                if type(start_date) == str:
                    start_date = int(datetime.timestamp(datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")))
                body["query"] = {"field": "updated_at", "operator": ">", "value": start_date}
            if next_page_token:
                body["pagination"] = {"per_page": 150, "starting_after": next_page_token}
            return body
        else:
            return None