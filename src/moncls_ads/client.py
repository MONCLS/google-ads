"""Builds an authenticated GoogleAdsClient from google-ads.yaml.

Config is loaded from (in order): the GOOGLE_ADS_CONFIGURATION_FILE_PATH env
var, or ./google-ads.yaml. Secrets live only in that gitignored file.
"""

from __future__ import annotations

import os

from google.ads.googleads.client import GoogleAdsClient

_DEFAULT_CONFIG = os.path.join(os.getcwd(), "google-ads.yaml")


def load_client() -> GoogleAdsClient:
    """Return an authenticated client, or raise a clear error if unconfigured."""
    path = os.environ.get("GOOGLE_ADS_CONFIGURATION_FILE_PATH", _DEFAULT_CONFIG)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No config at {path}. Copy google-ads.yaml.example to "
            "google-ads.yaml and fill in your credentials (setup steps 2-3)."
        )
    return GoogleAdsClient.load_from_storage(path)
