"""Stream type classes for tap-intercom."""

from __future__ import annotations

import typing as t

from singer_sdk.pagination import JSONPathPaginator
from urllib.parse import parse_qsl

from tap_intercom.client import IntercomStream, IntercomHATEOASPaginator
from tap_intercom.schemas import (
    admins_schema,
    articles_schema,
    contacts_schema,
    conversation_parts_schema,
    conversations_schema,
    tags_schema,
    teams_schema,
)


class ConversationsStream(IntercomStream):
    """Stream for Intercom conversations."""

    name = "conversations"
    path = "/conversations/search"
    replication_key = "updated_at"
    records_jsonpath = "$.conversations[*]"
    http_method = "POST"
    schema = conversations_schema

    def get_child_context(self, record: dict, context: dict | None) -> dict:  # noqa: ARG002
        """Return a context dictionary for child streams."""
        return {"conversation_id": record["id"]}


class ConversationPartsStream(IntercomStream):
    """Stream for Intercom conversation parts."""

    name = "conversation_parts"
    parent_stream_type = ConversationsStream
    state_partitioning_keys: t.ClassVar[list[str]] = []
    path = "/conversations/{conversation_id}"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updated_at"
    records_jsonpath = "$.conversation_parts.conversation_parts[*]"
    schema = conversation_parts_schema

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: Individual record in the stream.
            context: Stream partition or context dictionary.

        Returns:
            The resulting record dict, or `None` if the record should be excluded.
        """
        row["conversation_id"] = context["conversation_id"]
        return row


class AdminsStream(IntercomStream):
    """Stream for Intercom admins."""

    name = "admins"
    path = "/admins"
    records_jsonpath = "$.admins[*]"
    schema = admins_schema


class TagsStream(IntercomStream):
    """Stream for Intercom tags."""

    name = "tags"
    path = "/tags"
    schema = tags_schema


class TeamsStream(IntercomStream):
    """Stream for Intercom teams."""

    name = "teams"
    path = "/teams"
    records_jsonpath = "$.teams[*]"
    schema = teams_schema


class ContactsStream(IntercomStream):
    """Stream for Intercom contacts."""

    name = "contacts"
    path = "/contacts/search"
    replication_key = "updated_at"
    http_method = "POST"
    schema = contacts_schema

class ArticlesStream(IntercomStream):
    """Stream for Intercom articles."""

    name = "articles"
    path = "/articles/search"
    records_jsonpath = "$.data.articles[*]"
    schema = articles_schema

    # uses different pagination, overrida default
    def get_new_paginator(self):
        return IntercomHATEOASPaginator()

    def get_url_params(self, context, next_page_token):
        params = {}
        
        if next_page_token:
            params.update(parse_qsl(next_page_token.query))
            return params
        else:
            return super().get_url_params(context, next_page_token)
