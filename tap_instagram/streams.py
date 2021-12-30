"""Stream type classes for tap-instagram."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_instagram.client import instagramStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class UserPagesStream(instagramStream):
    """Get the facebook page associated to the account"""

    name = "facebook pages"
    path = "/me/accounts"
    primary_keys = ["id"]
    records_jsonpath = "$.data[*]"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("category", th.StringType),
        th.Property("name", th.StringType),
        th.Property("tasks", th.ArrayType(th.StringType)),
        th.Property(
            "category_list",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                )
            ),
        ),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"account_id": record["id"]}


class InstagramAccountsStream(instagramStream):
    """Get the instagram account linked to the page"""

    name = "instagram accounts"
    path = "/{account_id}?fields=instagram_business_account"
    primary_keys = ["id"]
    records_jsonpath = "$.instagram_business_account"
    replication_key = None
    parent_stream_type = UserPagesStream

    schema = th.ObjectType(th.Property("id", th.StringType)).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"instagram_id": record["id"]}


class MediaStream(instagramStream):
    """Get the media from the instagram account"""
    name = "media"
    fields = [
        "id",
        "caption",
        "media_type",
        "like_count",
        "comments_count",
        "media_url",
        "comments",
        "media_product_type",
        "insights.metric(reach,impressions)"
    ]
    path = f"/{{instagram_id}}?fields=media{{{','.join(fields)}}}"
    primary_keys = ["id"]
    records_jsonpath = "$.media.data[*]"
    replication_key = None
    parent_stream_type = InstagramAccountsStream

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("caption", th.StringType),
        th.Property("media_type", th.StringType),
        th.Property("like_count", th.IntegerType),
        th.Property("comments_count", th.IntegerType),
        th.Property("media_url", th.StringType),
        th.Property("comments",
            th.ObjectType(
                th.Property("data",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType),
                            th.Property("timestamp", th.DateTimeType),
                            th.Property("text", th.StringType)
                        )
                    )
                )
            )
        ),
        th.Property("media_product_type", th.StringType),
        th.Property("insights",
            th.ObjectType(
                th.Property("data",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("period", th.DateTimeType),
                            th.Property("values",
                                th.ArrayType(
                                    th.ObjectType(
                                        th.Property("value", th.IntegerType)
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    ).to_dict()


class StoriesStream(instagramStream):
    """Get the stories from the instagram account"""
    name = "stories"
    fields = [
        "id",
        "caption",
        "media_type",
        "media_url",
        "media_product_type",
        "insights.metric(impressions,reach,taps_forward,taps_back,exits,replies)"
    ]
    path = f"/{{instagram_id}}?fields=stories{{{','.join(fields)}}}"
    primary_keys = ["id"]
    records_jsonpath = "$.stories.data[*]"
    replication_key = None
    parent_stream_type = InstagramAccountsStream

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("caption", th.StringType),
        th.Property("media_type", th.StringType),
        th.Property("media_url", th.StringType),
        th.Property("media_product_type", th.StringType),
        th.Property("insights",
            th.ObjectType(
                th.Property("data",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("period", th.DateTimeType),
                            th.Property("values",
                                th.ArrayType(
                                    th.ObjectType(
                                        th.Property("value", th.IntegerType)
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    ).to_dict()
