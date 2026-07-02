# Access Setup — the steps only the account owner can do

Everything in this repo is built and tested. Go-live is blocked on three
owner-only actions (Google requires a human for each). Do these and the rest is
one command.

## 1. Apply for Basic Access (the critical path — do first)

The developer token is currently at **Test Access**, which can only call test
accounts — never the real Moncls account. Basic Access is the unlock; Google
review takes ~1–3 business days.

**Where:** Google Ads → Tools & Settings → Setup → **API Center** → **Access
level** → **Apply for Basic Access**.

**Suggested form answers:**
- Tool name: `Moncls Ads Manager`
- Own accounts or manage others'? → **My own account(s)** (in-house tool)
- Company / site: Monumental Chauffeured Limousine Service — moncls.com
- How you'll use the API:
  > In-house tool to manage our own single Google Ads account. Read-only
  > reporting (campaign, keyword, search-term performance) plus programmatic
  > campaign management — creating/updating Search campaigns, ad groups,
  > keywords, negative keywords, and responsive search ads for our chauffeured-
  > transportation business. Not resold or offered to third parties.
- API services: GoogleAdsService, CampaignService, CampaignBudgetService,
  AdGroupService, AdGroupCriterionService, CampaignCriterionService,
  AdGroupAdService.

## 2. Generate the refresh token (browser login)

```bash
pip install google-auth-oauthlib
python3 scripts/generate_refresh_token.py /path/to/client_secret_XXXX.json
```
Sign in as the account owner → **Allow** → copy the printed token.

## 3. Put the four credentials in the environment

In the Claude Code environment-variables box (`.env` format, NO quotes). Copy
`client_id`/`client_secret` straight from the JSON to avoid truncation:

```
GOOGLE_ADS_DEVELOPER_TOKEN=...
GOOGLE_ADS_CLIENT_ID=...
GOOGLE_ADS_CLIENT_SECRET=...
GOOGLE_ADS_REFRESH_TOKEN=...
GOOGLE_ADS_CUSTOMER_ID=...          # your account, digits only, no dashes
# GOOGLE_ADS_LOGIN_CUSTOMER_ID=...  # only if under a Manager/MCC account
```
Save, then start a new session.

## 4. What runs automatically after that

```bash
python -m moncls_ads.preflight        --customer-id <id>   # confirm access level
python -m moncls_ads.pull_reports     --customer-id <id> --range LAST_90_DAYS
python -m moncls_ads.campaign_builder --customer-id <id> --dry-run  # review
python -m moncls_ads.campaign_builder --customer-id <id>            # deploy PAUSED
```

## Also required before real spend (not code — account setup)

- **Conversion tracking on moncls.com**: phone-call conversions (Google
  forwarding number), booking-form submit, "request a proposal" submit. Without
  this, no campaign can be optimized. This is the #1 non-API prerequisite.
- **Two landing pages**: one daily/airport, one corporate/event.
