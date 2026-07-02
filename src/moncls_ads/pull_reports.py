"""CLI: pull the core reports and write them to CSVs under ./exports/.

    python -m moncls_ads.pull_reports --customer-id 1234567890 --range LAST_90_DAYS

Requires a configured google-ads.yaml. Read-only; touches nothing in the
account. Output CSVs are gitignored.
"""

from __future__ import annotations

import argparse
import csv
import os

from .client import load_client
from . import reporting

_PULLS = {
    "campaigns": reporting.campaign_performance,
    "keywords": reporting.keyword_performance,
    "search_terms": reporting.search_terms,
}


def _write_csv(name: str, rows: list[dict], out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.csv")
    if not rows:
        open(path, "w").close()
        return path
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Pull core Google Ads reports.")
    parser.add_argument("--customer-id", required=True, help="Digits only, no dashes.")
    parser.add_argument("--range", default=reporting.DEFAULT_RANGE)
    parser.add_argument("--out", default="exports")
    args = parser.parse_args()

    customer_id = args.customer_id.replace("-", "")
    client = load_client()

    for name, fn in _PULLS.items():
        rows = fn(client, customer_id, args.range)
        path = _write_csv(name, rows, args.out)
        print(f"{name}: {len(rows)} rows -> {path}")


if __name__ == "__main__":
    main()
