"""Intercom tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_intercom import streams


class TapIntercom(Tap):
    """Intercom tap class."""

    name = "tap-intercom"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The key to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.IntegerType,
            description="The earliest record date to sync, in unix timestamp format",
        ),
        th.Property(
            "filters",
            th.ObjectType(
                th.Property(
                    "stream",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("field", th.StringType),
                            th.Property("operator", th.StringType),
                            th.Property("value", th.StringType),
                        ),
                    ),
                ),
            ),
            description="Filters to apply to the API request (only for search endpoints)",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.IntercomStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.ConversationsStream(self),
            streams.ConversationPartsStream(self),
            streams.AdminsStream(self),
            streams.TagsStream(self),
            streams.TeamsStream(self),
            streams.ContactsStream(self),
        ]


if __name__ == "__main__":
    TapIntercom.cli()
