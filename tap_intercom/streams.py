"""Stream type classes for tap-intercom."""

from __future__ import annotations

import typing as t

from tap_intercom.client import IntercomStream
from tap_intercom.schemas import (
    admins_schema,
    contacts_schema,
    conversation_parts_schema,
    conversations_schema,
    tags_schema,
    teams_schema,
)


class ConversationsStream(IntercomStream):
    name = "conversations"
    path = "/conversations/search"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updated_at"
    records_jsonpath = "$.conversations[*]"
    http_method = "POST"
    schema = conversations_schema

    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"conversation_id": record["id"]}


class ConversationPartsStream(IntercomStream):
    name = "conversation_parts"
    parent_stream_type = ConversationsStream
    state_partitioning_keys = []
    path = "/conversations/{conversation_id}"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updated_at"
    records_jsonpath = "$.conversation_parts.conversation_parts[*]"
    schema = conversation_parts_schema

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        row["conversation_id"] = context["conversation_id"]
        return row


class AdminsStream(IntercomStream):
    name = "admins"
    path = "/admins"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.admins[*]"
    schema = admins_schema


class TagsStream(IntercomStream):
    name = "tags"
    path = "/tags"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.data[*]"
    schema = tags_schema


class TeamsStream(IntercomStream):
    name = "teams"
    path = "/teams"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.teams[*]"
    schema = teams_schema


class ContactsStream(IntercomStream):
    name = "contacts"
    path = "/contacts/search"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.data[*]"
    replication_key = "updated_at"
    http_method = "POST"
    schema = contacts_schema
