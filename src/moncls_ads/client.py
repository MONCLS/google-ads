"""Builds an authenticated GoogleAdsClient.

Config resolution order:
  1. Environment variables (GOOGLE_ADS_*) — used when secrets are injected
     into the runtime as env vars (e.g. a remote environment's secret store).
  2. A google-ads.yaml file — used for local machine setups.

Either way, secrets never live in the repo. The env-var path is preferred in
shared/remote environments so credentials stay in the secret store, not on disk.
"""

from __future__ import annotations

import os

from google.ads.googleads.client import GoogleAdsClient

_DEFAULT_CONFIG = os.path.join(os.getcwd(), "google-ads.yaml")

# The env vars the official library recognizes.
_REQUIRED_ENV = (
    "GOOGLE_ADS_DEVELOPER_TOKEN",
    "GOOGLE_ADS_CLIENT_ID",
    "GOOGLE_ADS_CLIENT_SECRET",
    "GOOGLE_ADS_REFRESH_TOKEN",
)


def _env_is_configured() -> bool:
    return all(os.environ.get(k) for k in _REQUIRED_ENV)


def load_client() -> GoogleAdsClient:
    """Return an authenticated client, or raise a clear error if unconfigured."""
    if _env_is_configured():
        # login_customer_id is optional (only for Manager/MCC accounts) and is
        # read automatically from GOOGLE_ADS_LOGIN_CUSTOMER_ID if present.
        return GoogleAdsClient.load_from_env()

    path = os.environ.get("GOOGLE_ADS_CONFIGURATION_FILE_PATH", _DEFAULT_CONFIG)
    if os.path.exists(path):
        return GoogleAdsClient.load_from_storage(path)

    missing = [k for k in _REQUIRED_ENV if not os.environ.get(k)]
    raise RuntimeError(
        "Google Ads credentials not configured. Set the environment secrets "
        f"({', '.join(missing)}) or provide a google-ads.yaml. "
        "See README setup steps 2-4."
    )
