"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_intercom.tap import TapIntercom

SAMPLE_CONFIG = {
    "start_date": int((datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)).timestamp()),
    "access_token": os.getenv("TAP_INTERCOM_ACCESS_TOKEN"),
}

TEST_SUITE_CONFIG = SuiteConfig(max_records_limit=10, ignore_no_records=True)


# Run standard built-in tap tests from the SDK:
TestTapIntercom = get_tap_test_class(
    tap_class=TapIntercom,
    config=SAMPLE_CONFIG,
    suite_config=TEST_SUITE_CONFIG,
)
