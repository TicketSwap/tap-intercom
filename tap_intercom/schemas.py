"""Contains all stream schemas."""

from singer_sdk.typing import (
    ArrayType,
    BooleanType,
    IntegerType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)

conversations_schema = PropertiesList(
    Property("type", StringType),
    Property("id", StringType),
    Property("title", StringType),
    Property("created_at", IntegerType),
    Property("updated_at", IntegerType),
    Property("waiting_since", IntegerType),
    Property("snoozed_until", IntegerType),
    Property("open", BooleanType),
    Property("state", StringType),
    Property("read", BooleanType),
    Property("priority", StringType),
    Property("admin_assignee_id", IntegerType),
    Property("team_assignee_id", IntegerType),
    Property(
        "tags",
        ObjectType(
            Property("type", StringType),
            Property(
                "tags",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                        Property("name", StringType),
                        Property("applied_at", IntegerType),
                        Property(
                            "applied_by",
                            ObjectType(
                                Property("type", StringType),
                                Property("id", StringType),
                            ),
                        ),
                    )
                ),
            ),
        ),
    ),
    Property(
        "conversation_rating",
        ObjectType(
            Property("rating", IntegerType),
            Property("remark", StringType),
            Property("created_at", IntegerType),
            Property(
                "contact",
                ObjectType(
                    Property("type", StringType),
                    Property("id", StringType),
                    Property("external_id", StringType),
                ),
            ),
            Property(
                "teammate",
                ObjectType(
                    Property("type", StringType),
                    Property("id", StringType),
                ),
            ),
        ),
    ),
    Property(
        "source",
        ObjectType(
            Property("type", StringType),
            Property("id", StringType),
            Property("delivered_as", StringType),
            Property("subject", StringType),
            Property("body", StringType),
            Property(
                "author",
                ObjectType(
                    Property("type", StringType),
                    Property("id", StringType),
                    Property("name", StringType),
                    Property("email", StringType),
                ),
            ),
            Property(
                "attachments",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("name", StringType),
                        Property("url", StringType),
                        Property("content_type", StringType),
                        Property("filesize", IntegerType),
                        Property("width", StringType),
                        Property("height", StringType),
                    )
                ),
            ),
            Property("url", StringType),
            Property("redacted", BooleanType),
        ),
    ),
    Property(
        "contacts",
        ObjectType(
            Property("type", StringType),
            Property(
                "contacts",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                        Property("external_id", StringType),
                    )
                ),
            ),
        ),
    ),
    Property(
        "teammates",
        ObjectType(
            Property("type", StringType),
            Property(
                "teammates",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                    )
                ),
            ),
        ),
    ),
    Property(
        "first_contact_reply",
        ObjectType(
            Property("created_at", IntegerType),
            Property("type", StringType),
            Property("url", StringType),
        ),
    ),
    Property(
        "sla_applied",
        ObjectType(
            Property("type", StringType),
            Property("sla_name", StringType),
            Property("sla_status", StringType),
        ),
    ),
    Property(
        "statistics",
        ObjectType(
            Property("type", StringType),
            Property("time_to_assignment", IntegerType),
            Property("time_to_admin_reply", IntegerType),
            Property("time_to_first_close", IntegerType),
            Property("time_to_last_close", IntegerType),
            Property("median_time_to_reply", IntegerType),
            Property("first_contact_reply_at", IntegerType),
            Property("first_assignment_at", IntegerType),
            Property("first_admin_reply_at", IntegerType),
            Property("first_close_at", IntegerType),
            Property("last_assignment_at", IntegerType),
            Property("last_assignment_admin_reply_at", IntegerType),
            Property("last_contact_reply_at", IntegerType),
            Property("last_admin_reply_at", IntegerType),
            Property("last_close_at", IntegerType),
            Property("last_closed_by_id", IntegerType),
            Property("count_reopens", IntegerType),
            Property("count_assignments", IntegerType),
            Property("count_conversation_parts", IntegerType),
        ),
    ),
    Property(
        "linked_objects",
        ObjectType(
            Property("type", StringType),
            Property("total_count", IntegerType),
            Property("has_more", BooleanType),
            Property(
                "data",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                        Property("category", StringType),
                    )
                ),
            ),
        ),
    ),
    Property(
        "custom_attributes",
        ObjectType(
            Property(
                "active_draft",
                ObjectType(
                    Property("type", StringType),
                    Property(
                        "instances",
                        ArrayType(
                            ObjectType(
                                Property("id", StringType),
                                Property("external_id", StringType),
                                Property(
                                    "custom_attributes",
                                    ObjectType(
                                        Property("event_id", StringType),
                                        Property("event_title", StringType),
                                    ),
                                ),
                                Property("type", StringType),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
).to_dict()

conversation_parts_schema = PropertiesList(
    Property("type", StringType),
    Property("id", StringType),
    Property("conversation_id", StringType),
    Property("part_type", StringType),
    Property("body", StringType),
    Property("created_at", IntegerType),
    Property("updated_at", IntegerType),
    Property("notified_at", IntegerType),
    Property(
        "assigned_to",
        ObjectType(
            Property("type", StringType),
            Property("id", StringType),
        ),
    ),
    Property(
        "author",
        ObjectType(
            Property("type", StringType),
            Property("id", StringType),
            Property("name", StringType),
            Property("email", StringType),
        ),
    ),
    Property(
        "attachments",
        ArrayType(
            ObjectType(
                Property("type", StringType),
                Property("name", StringType),
                Property("url", StringType),
                Property("content_type", StringType),
                Property("filesize", IntegerType),
                Property("width", StringType),
                Property("height", StringType),
            )
        ),
    ),
    Property("external_id", StringType),
    Property("redacted", BooleanType),
).to_dict()

admins_schema =  PropertiesList(
    Property("type", StringType),
    Property("id", StringType),
    Property("name", StringType),
    Property("email", StringType),
    Property("job_title", StringType),
    Property("away_mode_enabled", BooleanType),
    Property("away_mode_reassign", BooleanType),
    Property("has_inbox_seat", BooleanType),
    Property("team_ids", ArrayType(IntegerType)),
    Property("avatar", StringType),
    Property(
        "team_priority_level",
        ObjectType(
            Property("primary_team_ids", ArrayType(IntegerType)),
            Property("secondary_team_ids", ArrayType(IntegerType)),
        ),
    ),
).to_dict()

tags_schema = PropertiesList(
    Property("type", StringType),
    Property("id", StringType),
    Property("name", StringType),
    Property("applied_at", IntegerType),
    Property("applied_by", ObjectType(Property("type", StringType), Property("id", StringType))),
).to_dict()

teams_schema = PropertiesList(
    Property("type", StringType),
    Property("id", StringType),
    Property("name", StringType),
    Property("admin_ids", ArrayType(IntegerType)),
    Property(
        "admin_priority_level",
        ObjectType(
            Property("primary_admin_ids", ArrayType(IntegerType)),
            Property("secondary_admin_ids", ArrayType(IntegerType)),
        ),
    ),
).to_dict()

contacts_schema = PropertiesList(
    Property("type", StringType),
    Property("id", StringType, description="The unique identifier for the contact"),
    Property("workspace_id", StringType, description="The ID of the workspace the contact belongs to"),
    Property(
        "external_id",
        StringType,
        description="An external identifier for the contact, set by the integrating application",
    ),
    Property("role", StringType, description="The role of the contact, either user or lead"),
    Property("email", StringType, description="The email address of the contact"),
    Property("phone", StringType, description="The phone number of the contact"),
    Property("name", StringType, description="The name of the contact"),
    Property(
        "avatar",
        ObjectType(
            Property("type", StringType, description="The type of object"),
            Property("image_url", StringType, description="URL of the contact's avatar image"),
        ),
    ),
    Property("owner_id", IntegerType, description="The ID of the teammate who owns this contact"),
    Property(
        "social_profiles",
        ObjectType(
            Property(
                "data",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("name", StringType),
                        Property("url", StringType),
                    ),
                ),
            ),
        ),
        description="A list of social profiles associated with the contact",
    ),
    Property(
        "has_hard_bounced",
        BooleanType,
        description="Indicates whether the contact's email address has hard bounced",
    ),
    Property(
        "marked_email_as_spam",
        BooleanType,
        description="Indicates whether the contact has marked emails from the workspace as spam",
    ),
    Property(
        "unsubscribed_from_emails",
        BooleanType,
        description="Indicates whether the contact has unsubscribed from emails",
    ),
    Property("created_at", IntegerType, description="The time when the contact was created, in Unix time"),
    Property("updated_at", IntegerType, description="The time when the contact was last updated, in Unix time"),
    Property("last_seen_at", IntegerType, description="The time when the contact was last seen, in Unix time"),
    Property("signed_up_at", IntegerType, description="The time when the contact signed up, in Unix time"),
    Property("last_replied_at", IntegerType, description="The time when the contact last replied, in Unix time"),
    Property(
        "last_contacted_at", IntegerType, description="The time when the contact was last contacted, in Unix time"
    ),
    Property(
        "last_email_opened_at",
        IntegerType,
        description="The time when the contact last opened an email, in Unix time",
    ),
    Property(
        "last_email_clicked_at",
        IntegerType,
        description="The time when the contact last clicked a link in an email, in Unix time",
    ),
    Property("language_override", StringType, description="The language override for the contact"),
    Property("browser", StringType, description="The browser used by the contact"),
    Property("browser_version", StringType, description="The version of the browser used by the contact"),
    Property("browser_language", StringType, description="The language of the browser used by the contact"),
    Property("os", StringType, description="The operating system used by the contact"),
    Property(
        "location",
        ObjectType(
            Property("city", StringType, description="The city of the contact's location"),
            Property("country", StringType, description="The country of the contact's location"),
            Property("region", StringType, description="The region of the contact's location"),
            Property(
                "country_code", StringType, description="The ISO 3166-1 country code of the contact's location"
            ),
        ),
        description="An object containing location meta data about a Intercom contact.",
    ),
    Property("ip", StringType, description="The IP address of the contact"),
    Property("utm_source", StringType, description="The UTM source parameter from the contact's signup URL"),
    Property("utm_medium", StringType, description="The UTM medium parameter from the contact's signup URL"),
    Property("utm_campaign", StringType, description="The UTM campaign parameter from the contact's signup URL"),
    Property("utm_term", StringType, description="The UTM term parameter from the contact's signup URL"),
    Property("utm_content", StringType, description="The UTM content parameter from the contact's signup URL"),
    Property(
        "tags",
        ObjectType(
            Property(
                "data",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                        Property("url", StringType),
                    ),
                ),
            ),
            Property("url", StringType),
            Property("total_count", IntegerType),
            Property("has_more", BooleanType),
        ),
        description="Tags associated with the contact",
    ),
    Property(
        "notes",
        ObjectType(
            Property(
                "data",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                        Property("url", StringType),
                    ),
                ),
            ),
            Property("url", StringType),
            Property("total_count", IntegerType),
            Property("has_more", BooleanType),
        ),
        description="Notes associated with the contact",
    ),
    Property(
        "companies",
        ObjectType(
            Property("url", StringType),
            Property("total_count", IntegerType),
            Property("has_more", BooleanType),
        ),
        description="Notes associated with the contact",
    ),
    Property("custom_attributes", ObjectType(), description="Custom attributes associated with the contact"),
).to_dict()
