# Moncls Google Ads Management

In-house toolkit to analyze, report on, and manage the Moncls (Monumental
Chauffeured Limousine Service) Google Ads account via the official Google Ads
API.

## Status

- [x] Reporting + auth scaffold (this repo)
- [ ] **Basic Access** on the developer token (blocks all production calls — apply in API Center)
- [ ] OAuth client + refresh token configured (`google-ads.yaml`)
- [ ] First live report pull
- [ ] New campaign build

## Setup

**Step 1 — Developer token.** From your Google Ads API Center. Currently at
*Test Account Access*; **apply for Basic Access** to reach the production
account.

**Step 2 — OAuth client (Google Cloud Console).**
`APIs & Services > Credentials > Create Credentials > OAuth client ID >
Application type: Desktop app`. Download the `client_secret_*.json`.

**Step 3 — Refresh token.**
```bash
pip install -r requirements.txt
python scripts/generate_refresh_token.py /path/to/client_secret.json
```
Approve access as the Google account that owns the Ads account; copy the
printed `refresh_token`.

**Step 4 — Config.** `cp google-ads.yaml.example google-ads.yaml` and fill in
the developer token, client id/secret, and refresh token. This file is
gitignored — never commit it.

## Usage

Pull the core read-only reports to `./exports/`:
```bash
python -m moncls_ads.pull_reports --customer-id 1234567890 --range LAST_90_DAYS
```

## Layout

- `src/moncls_ads/client.py` — authenticated client factory
- `src/moncls_ads/reporting.py` — read-only GAQL report queries
- `src/moncls_ads/pull_reports.py` — CLI to dump reports to CSV
- `scripts/generate_refresh_token.py` — one-time OAuth helper
- `STRATEGY.md` — findings from historical data + new-campaign direction

## Security

Secrets (`google-ads.yaml`, `.env`, `client_secret*.json`) and data exports
(`exports/`, `*.csv`) are gitignored. Keep them off the repo.
