"""Contains all stream schemas."""

from singer_sdk.typing import (
    ArrayType,
    BooleanType,
    IntegerType,
    NumberType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)

# define languages for translated articles content, add here to include
languages = [
    "bg",
    "cs",
    "de",
    "en",
    "es",
    "fr",
    "hu",
    "it",
    "nb",
    "nl",
    "pl",
    "pt",
    "pt-BR",
    "sk",
    "sv",
]

# define translated content articles schema to avoid repetition
translated_content = [
    Property(
        lang,
        ObjectType(
            Property("title", StringType),
            Property("description", StringType),
            Property("author_id", IntegerType),
            Property("state", StringType),
            Property("created_at", IntegerType),
            Property("updated_at", IntegerType),
        ),
    )
    for lang in languages
]

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
            Property("updated_at", IntegerType),
            Property("rating", IntegerType),
            Property("remark", StringType),
            Property("created_at", IntegerType),
            Property(
                "contact",
                ObjectType(
                    Property("external_id", StringType),
                    Property("type", StringType),
                    Property("id", StringType),
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
                "admins",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                    ),
                ),
            ),
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
            Property(
                "assigned_team_first_response_time",
                ArrayType(
                    ObjectType(
                        Property("team_id", IntegerType),
                        Property("team_name", StringType),
                        Property("response_time", NumberType),
                    )
                ),
            ),
            Property(
                "assigned_team_first_response_time_in_office_hours",
                ArrayType(
                    ObjectType(
                        Property("team_id", IntegerType),
                        Property("team_name", StringType),
                        Property("response_time", NumberType),
                    )
                ),
            ),
            Property("handling_time", IntegerType),
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
        "conversation_parts",
        ObjectType(
            Property("type", StringType),
            Property("total_count", IntegerType),
            Property(
                "conversation_parts",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
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
                    )
                ),
            ),
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
                        Property("id", StringType),
                        Property("category", StringType),
                    )
                ),
            ),
        ),
    ),
    Property("ai_agent_participated", BooleanType),
    Property(
        "ai_agent",
        ObjectType(
            Property("source_type", StringType),
            Property("source_title", StringType),
            Property("last_answer_type", StringType),
            Property("resolution_state", StringType),
            Property("rating", IntegerType),
            Property("rating_remark", StringType),
            Property("created_at", IntegerType),
            Property("updated_at", IntegerType),
            Property(
                "content_sources",
                ObjectType(
                    Property("type", StringType),
                    Property("total_count", IntegerType),
                    Property(
                        "content_sources",
                        ArrayType(
                            ObjectType(
                                Property("content_type", StringType),
                                Property("url", StringType),
                                Property("title", StringType),
                                Property("locale", StringType),
                            )
                        ),
                    ),
                ),
            ),
        ),
    ),
    # Keeping your custom attributes as requested
    Property(
        "custom_attributes",
        ObjectType(
            Property("imported_via_standalone", BooleanType),
            Property("fin_ai_agent:_preview", BooleanType),
            Property("auto-translated", BooleanType),
            Property("fin_ai_agent:_preview_mode", BooleanType),
            Property("probleem_met_de_vermelding", StringType),
            Property("copilot_used", BooleanType),
            Property("brand", StringType),
            Property("has_attachments", BooleanType),
            Property(
                "active_draft",
                ObjectType(
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
                                        Property("has_errors", BooleanType),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            Property("cx_score_rating", IntegerType),
            Property("cx_score_explanation", StringType),
            Property("opencx_category", StringType),
            Property("opencxeventname", StringType),
            Property("opencxeventid", StringType),
            Property("opencxeventcountry", StringType),
            Property(
                "latest_bought_listings",
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
                                        Property("eventId", StringType),
                                        Property("eventTitle", StringType),
                                        Property("sellerId", StringType),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            Property(
                "selected_bought_listing",
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
                                        Property("eventId", StringType),
                                        Property("eventTitle", StringType),
                                        Property("sellerId", StringType),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            Property(
                "last_payout",
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
                                        Property("eventId", StringType),
                                        Property("eventTitle", StringType),
                                        Property("amount", StringType),  # includes currency sign
                                        Property("predictedArrivalAt", StringType),
                                        Property("state", StringType),
                                        Property("stateLabel", StringType),
                                    ),
                                ),
                                Property("type", StringType),
                            ),
                        ),
                    ),
                ),
            ),
            Property("language", StringType),
            Property("event_link", StringType),
            Property("eventcode", StringType),
            Property("organisercode", StringType),
            Property("secureswap_fr", StringType),
            Property("modify_event", StringType),
            Property("primary_ticketing_uk", StringType),
            Property("eventix_link", StringType),
            Property("primary_ticketing_fr", StringType),
            Property("modifier_l'événement", StringType),
        ),
    ),
).to_dict()

conversation_parts_schema = PropertiesList(
    Property("conversation_id", StringType),
    Property("type", StringType),
    Property("id", StringType),
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
            Property("from_ai_agent", BooleanType),
            Property("is_ai_answer", BooleanType),
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
    Property("conversation_part_has_body", BooleanType),
    Property("conversation_part_has_attachments", BooleanType),
    Property(
        "email_message_metadata",
        ObjectType(
            Property("subject", StringType),
            Property(
                "email_address_headers",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("email_address", StringType),
                        Property("name", StringType),
                    )
                ),
            ),
        ),
    ),
    Property(
        "metadata",
        ObjectType(
            Property(
                "quick_reply_options",
                ArrayType(
                    ObjectType(
                        Property("translations", ObjectType()),
                        Property("text", StringType),
                        Property("uuid", StringType),
                    )
                ),
            ),
            Property("quick_reply_uuid", StringType),
            Property("quick_reply_option_uuid", StringType),
        ),
    ),
    Property("state", StringType),
    Property(
        "tags",
        ArrayType(
            ObjectType(
                Property("type", StringType),
                Property("id", StringType),
                Property("name", StringType),
            )
        ),
    ),
    Property(
        "event_details",
        ObjectType(
            Property(
                "action",
                ObjectType(
                    Property("name", StringType),
                    Property("result", StringType),
                ),
            ),
            Property(
                "attribute",
                ObjectType(
                    Property("name", StringType),
                ),
            ),
            Property(
                "workflow",
                ObjectType(
                    Property("group_title", StringType),
                    Property("name", StringType),
                ),
            ),
            Property(
                "value",
                ObjectType(
                    Property("name", StringType),
                ),
            ),
            Property(
                "event",
                ObjectType(
                    Property("type", StringType),
                    Property("result", StringType),
                ),
            ),
        ),
    ),
    Property("app_package_code", StringType),
).to_dict()

admins_schema = PropertiesList(
    Property("type", StringType),
    Property("id", StringType),
    Property("name", StringType),
    Property("email", StringType),
    Property("job_title", StringType),
    Property(
        "team_priority_level",
        ObjectType(
            Property("primary_team_ids", ArrayType(IntegerType)),
            Property("secondary_team_ids", ArrayType(IntegerType)),
        ),
    ),
    Property("away_mode_enabled", BooleanType),
    Property("away_mode_reassign", BooleanType),
    Property("has_inbox_seat", BooleanType),
    Property("team_ids", ArrayType(IntegerType)),
    Property(
        "avatar",
        ObjectType(
            Property("type", StringType),
            Property("image_url", StringType),
        ),
    ),
).to_dict()

tags_schema = PropertiesList(
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
    Property("id", StringType),
    Property("workspace_id", StringType),
    Property("external_id", StringType),
    Property("role", StringType),
    Property("email", StringType),
    Property("phone", StringType),
    Property("name", StringType),
    Property("avatar", StringType),
    Property("owner_id", IntegerType),
    Property(
        "social_profiles",
        ObjectType(
            Property("type", StringType),
            Property(
                "data",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("name", StringType),
                        Property("url", StringType),
                    )
                ),
            ),
        ),
    ),
    Property("has_hard_bounced", BooleanType),
    Property("marked_email_as_spam", BooleanType),
    Property("unsubscribed_from_emails", BooleanType),
    Property("created_at", IntegerType),
    Property("updated_at", IntegerType),
    Property("signed_up_at", IntegerType),
    Property("last_seen_at", IntegerType),
    Property("last_replied_at", IntegerType),
    Property("last_contacted_at", IntegerType),
    Property("last_email_opened_at", IntegerType),
    Property("last_email_clicked_at", IntegerType),
    Property("language_override", StringType),
    Property("browser", StringType),
    Property("browser_version", StringType),
    Property("browser_language", StringType),
    Property("os", StringType),
    Property(
        "location",
        ObjectType(
            Property("type", StringType),
            Property("country", StringType),
            Property("region", StringType),
            Property("city", StringType),
            Property("country_code", StringType),
            Property("continent_code", StringType),
        ),
    ),
    Property("android_app_name", StringType),
    Property("android_app_version", StringType),
    Property("android_device", StringType),
    Property("android_os_version", StringType),
    Property("android_sdk_version", StringType),
    Property("android_last_seen_at", IntegerType),
    Property("ios_app_name", StringType),
    Property("ios_app_version", StringType),
    Property("ios_device", StringType),
    Property("ios_os_version", StringType),
    Property("ios_sdk_version", StringType),
    Property("ios_last_seen_at", IntegerType),
    Property("custom_attributes", ObjectType()),
    Property(
        "tags",
        ObjectType(
            Property("type", StringType),
            Property(
                "data",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                        Property("url", StringType),
                    )
                ),
            ),
            Property("url", StringType),
            Property("total_count", IntegerType),
            Property("has_more", BooleanType),
        ),
    ),
    Property(
        "notes",
        ObjectType(
            Property("type", StringType),
            Property(
                "data",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                        Property("url", StringType),
                    )
                ),
            ),
            Property("url", StringType),
            Property("total_count", IntegerType),
            Property("has_more", BooleanType),
        ),
    ),
    Property(
        "companies",
        ObjectType(
            Property("type", StringType),
            Property(
                "data",
                ArrayType(
                    ObjectType(
                        Property("type", StringType),
                        Property("id", StringType),
                        Property("url", StringType),
                    )
                ),
            ),
            Property("url", StringType),
            Property("total_count", IntegerType),
            Property("has_more", BooleanType),
        ),
    ),
    Property(
        "custom_attributes",
        ObjectType(
            Property("preferred_language", StringType),
            Property("countrycode", StringType),
            Property("hascartitems", BooleanType),
            Property("isuserverified", BooleanType),
            Property("isabletosell", BooleanType),
            Property("anonymousid", StringType),
            Property("is_phone_verified", BooleanType),
            Property("userid", StringType),
            Property("id", StringType),
            Property("country_code", StringType),
            Property("haspayoutmethodsetup", BooleanType),
            Property("is_employee", BooleanType),
            Property("is_new_profile", BooleanType),
            Property("display_name", StringType),
            Property("verification_id", StringType),
            Property("city", StringType),
            Property("isphoneverified", BooleanType),
            Property("project", StringType),
            Property("isemailverified", BooleanType),
            Property("article_id", StringType),
            Property("job_title", StringType),
            Property("last_payout_state_description", StringType),
            Property("is_intersection_booted", BooleanType),
            Property("email", StringType),
            Property("hasgivenmarketingpushconsent", BooleanType),
            Property("hasgivenmarketingemailconsent", BooleanType),
            Property("octopods_messagebird_whatsapp_account_phone", StringType),
            Property("octopods_channel", StringType),
            Property("isreceivingemailnotifications", BooleanType),
        ),
    ),
).to_dict()

articles_schema = PropertiesList(
    Property("id", StringType),
    Property("type", StringType),
    Property("workspace_id", StringType),
    Property("default_locale", StringType),
    Property("url", StringType),
    Property("parent_id", IntegerType),
    Property("parent_type", StringType),
    Property("parent_ids", ArrayType(IntegerType)),
    Property(
        "translated_content",
        ObjectType(*translated_content),
    ),
    Property("languages", ArrayType(StringType)),
    Property(
        "tags",
        ObjectType(
            Property(
                "tags",
                ArrayType(
                    ObjectType(
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
                    ),
                ),
            ),
        ),
    ),
    Property("title", StringType),
    Property("description", StringType),
    Property("body", StringType),
    Property("author_id", IntegerType),
    Property("state", StringType),
    Property("created_at", IntegerType),
    Property("updated_at", IntegerType),
).to_dict()

articles_extended_schema = PropertiesList(
    Property("id", StringType),
    Property("parent_type", StringType),
    Property("type", StringType),
    Property("workspace_id", StringType),
    Property("default_locale", StringType),
    Property("url", StringType),
    Property("parent_id", IntegerType),
    Property("parent_ids", ArrayType(IntegerType)),
    Property(
        "translated_content",
        ObjectType(*translated_content),
    ),
    Property("languages", ArrayType(StringType)),
    Property(
        "tags",
        ObjectType(
            Property(
                "tags",
                ArrayType(
                    ObjectType(
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
                    ),
                ),
            ),
        ),
    ),
    Property("title", StringType),
    Property("description", StringType),
    Property("body", StringType),
    Property("author_id", IntegerType),
    Property("state", StringType),
    Property(
        "statistics",
        ObjectType(
            Property("views", IntegerType),
            Property("conversions", IntegerType),
            Property("reactions", IntegerType),
            Property("happy_reaction_percentage", NumberType),
            Property("neutral_reaction_percentage", NumberType),
            Property("sad_reaction_percentage", NumberType),
        ),
    ),
    Property("created_at", IntegerType),
    Property("updated_at", IntegerType),
).to_dict()
