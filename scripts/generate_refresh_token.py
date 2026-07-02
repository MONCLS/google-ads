"""Setup step 3: mint a refresh token for the Google Ads API.

Prerequisite: you created an OAuth 2.0 Client ID of type "Desktop app" in the
Google Cloud Console and downloaded its client_secret JSON (setup step 2).

Usage:
    python scripts/generate_refresh_token.py /path/to/client_secret.json

It opens a browser (or prints a URL), you approve access with the Google
account that owns the Google Ads account, and it prints a refresh_token.
Paste that token into google-ads.yaml. The refresh token is long-lived; you
only do this once.
"""

import sys

from google_auth_oauthlib.flow import InstalledAppFlow

# Full access to the Google Ads API.
SCOPES = ["https://www.googleapis.com/auth/adwords"]


def main(client_secret_path: str) -> None:
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
    # Tries a local browser first; falls back to console copy/paste.
    try:
        creds = flow.run_local_server(port=0, prompt="consent")
    except Exception:
        creds = flow.run_console()

    print("\n=== SUCCESS ===")
    print("Add this to google-ads.yaml:\n")
    print(f'refresh_token: "{creds.refresh_token}"')
    print("\n(Keep it secret. Do not commit it.)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/generate_refresh_token.py <client_secret.json>")
    main(sys.argv[1])
