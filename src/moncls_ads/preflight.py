"""First-run diagnostic: confirm credentials work and report access level.

Run this the moment all four credentials are in place. It answers three
questions before we touch anything:
  1. Do the credentials authenticate at all?
  2. Which customer accounts can this login reach?
  3. Can we actually query the target account, or is the developer token still
     stuck at Test Access (the classic DEVELOPER_TOKEN_* error)?

    python -m moncls_ads.preflight --customer-id 1234567890
"""

from __future__ import annotations

import argparse

from .client import load_client


def run(customer_id: str | None) -> int:
    try:
        client = load_client()
    except Exception as e:  # noqa: BLE001 — surface the exact config problem
        print(f"❌ Credentials not usable: {e}")
        return 1

    print("✅ Credentials loaded and authenticated.")

    # 1. Which accounts can this login reach?
    try:
        customer_service = client.get_service("CustomerService")
        accessible = customer_service.list_accessible_customers()
        ids = [rn.split("/")[-1] for rn in accessible.resource_names]
        print(f"✅ Accessible customer IDs: {ids or '(none)'}")
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  Could not list accessible customers: {e}")
        ids = []

    if not customer_id:
        print("\nNo --customer-id given; skipping the live query test.")
        return 0

    # 2. Can we actually query the target account?
    ga = client.get_service("GoogleAdsService")
    query = "SELECT customer.id, customer.descriptive_name FROM customer LIMIT 1"
    try:
        for batch in ga.search_stream(customer_id=customer_id, query=query):
            for row in batch.results:
                print(
                    f"✅ Live query OK — account {row.customer.id} "
                    f"({row.customer.descriptive_name}). Production access confirmed."
                )
        return 0
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "DEVELOPER_TOKEN" in msg or "test account" in msg.lower():
            print(
                "❌ Auth works, but the developer token is NOT approved for this "
                "account (still Test Access). Apply for Basic Access in the API "
                "Center — production calls stay blocked until Google approves.\n"
                f"   Raw: {msg.splitlines()[0]}"
            )
        else:
            print(f"❌ Live query failed: {msg.splitlines()[0]}")
        return 2


def main() -> None:
    p = argparse.ArgumentParser(description="Google Ads credential/access preflight.")
    p.add_argument("--customer-id", default=None, help="Digits only, no dashes.")
    args = p.parse_args()
    cid = args.customer_id.replace("-", "") if args.customer_id else None
    raise SystemExit(run(cid))


if __name__ == "__main__":
    main()
