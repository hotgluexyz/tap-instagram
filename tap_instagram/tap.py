"""instagram tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_instagram.streams import (
    UserPagesStream,
    InstagramAccountsStream,
    MediaStream,
    StoriesStream
)


STREAM_TYPES = [
    UserPagesStream,
    InstagramAccountsStream,
    MediaStream,
    StoriesStream
]


class Tapinstagram(Tap):
    """instagram tap class."""
    name = "tap-instagram"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
        )
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

if __name__=="__main__":
    Tapinstagram.cli()