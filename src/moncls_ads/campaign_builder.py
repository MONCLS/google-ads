"""Builds the new Moncls campaigns from CAMPAIGN_PLAN.md, in PAUSED state.

Everything created here starts PAUSED so a human reviews it in the UI before a
dollar is spent. Run with --dry-run first to see what would be created without
touching the account.

    python -m moncls_ads.campaign_builder --customer-id 1234567890 --dry-run
    python -m moncls_ads.campaign_builder --customer-id 1234567890   # live, paused

This is version-sensitive to the google-ads client library and must be
validated against a live/test account before use. Nothing is enabled
automatically.
"""

from __future__ import annotations

import argparse

from google.ads.googleads.client import GoogleAdsClient

from .client import load_client
from .plan import CAMPAIGN_PLAN, SHARED_NEGATIVES


def _micros(dollars: float) -> int:
    return int(round(dollars * 1_000_000))


def _add_budget(client: GoogleAdsClient, customer_id: str, name: str, daily: float) -> str:
    svc = client.get_service("CampaignBudgetService")
    op = client.get_type("CampaignBudgetOperation")
    b = op.create
    b.name = name
    b.amount_micros = _micros(daily)
    b.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    res = svc.mutate_campaign_budgets(customer_id=customer_id, operations=[op])
    return res.results[0].resource_name


def _add_campaign(
    client: GoogleAdsClient, customer_id: str, name: str, budget_rn: str
) -> str:
    svc = client.get_service("CampaignService")
    op = client.get_type("CampaignOperation")
    c = op.create
    c.name = name
    c.status = client.enums.CampaignStatusEnum.PAUSED  # always launch paused
    c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    c.campaign_budget = budget_rn
    # Start on Manual CPC — no conversion history to train a smart bidder yet.
    c.manual_cpc.enhanced_cpc_enabled = False
    c.network_settings.target_google_search = True
    c.network_settings.target_search_network = False
    c.network_settings.target_content_network = False
    res = svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    return res.results[0].resource_name


def _add_ad_group(
    client: GoogleAdsClient, customer_id: str, campaign_rn: str, name: str, cpc: float
) -> str:
    svc = client.get_service("AdGroupService")
    op = client.get_type("AdGroupOperation")
    ag = op.create
    ag.name = name
    ag.campaign = campaign_rn
    ag.status = client.enums.AdGroupStatusEnum.ENABLED
    ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ag.cpc_bid_micros = _micros(cpc)
    res = svc.mutate_ad_groups(customer_id=customer_id, operations=[op])
    return res.results[0].resource_name


def _parse_keyword(text: str):
    """'[foo]' -> EXACT, '"foo"' or plain -> PHRASE. No broad, by design."""
    text = text.strip()
    if text.startswith("[") and text.endswith("]"):
        return text[1:-1], "EXACT"
    return text.strip('"'), "PHRASE"


def _add_keywords(
    client: GoogleAdsClient, customer_id: str, ad_group_rn: str, keywords: list[str]
) -> int:
    svc = client.get_service("AdGroupCriterionService")
    ops = []
    for kw in keywords:
        text, match = _parse_keyword(kw)
        op = client.get_type("AdGroupCriterionOperation")
        c = op.create
        c.ad_group = ad_group_rn
        c.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        c.keyword.text = text
        c.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match)
        ops.append(op)
    svc.mutate_ad_group_criteria(customer_id=customer_id, operations=ops)
    return len(ops)


def _add_campaign_negatives(
    client: GoogleAdsClient, customer_id: str, campaign_rn: str, negatives: list[str]
) -> int:
    svc = client.get_service("CampaignCriterionService")
    ops = []
    for word in negatives:
        op = client.get_type("CampaignCriterionOperation")
        c = op.create
        c.campaign = campaign_rn
        c.negative = True
        c.keyword.text = word
        c.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        ops.append(op)
    svc.mutate_campaign_criteria(customer_id=customer_id, operations=ops)
    return len(ops)


def _add_rsa(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_rn: str,
    headlines: list[str],
    descriptions: list[str],
    final_url: str,
) -> None:
    svc = client.get_service("AdGroupAdService")
    op = client.get_type("AdGroupAdOperation")
    aga = op.create
    aga.ad_group = ad_group_rn
    aga.status = client.enums.AdGroupAdStatusEnum.PAUSED
    ad = aga.ad
    ad.final_urls.append(final_url)
    for h in headlines[:15]:
        asset = client.get_type("AdTextAsset")
        asset.text = h
        ad.responsive_search_ad.headlines.append(asset)
    for d in descriptions[:4]:
        asset = client.get_type("AdTextAsset")
        asset.text = d
        ad.responsive_search_ad.descriptions.append(asset)
    svc.mutate_ad_group_ads(customer_id=customer_id, operations=[op])


def build(customer_id: str, dry_run: bool = True) -> None:
    if dry_run:
        print("DRY RUN — nothing will be created.\n")
        for camp in CAMPAIGN_PLAN:
            print(f"Campaign: {camp['name']}  (${camp['daily_budget']}/day, PAUSED)")
            for ag in camp["ad_groups"]:
                print(f"  Ad group: {ag['name']}  ({len(ag['keywords'])} keywords)")
                for kw in ag["keywords"]:
                    text, match = _parse_keyword(kw)
                    print(f"      [{match:6}] {text}")
        print(f"\nShared negatives ({len(SHARED_NEGATIVES)}): {', '.join(SHARED_NEGATIVES[:8])} ...")
        return

    client = load_client()
    for camp in CAMPAIGN_PLAN:
        budget_rn = _add_budget(client, customer_id, f"{camp['name']} budget", camp["daily_budget"])
        campaign_rn = _add_campaign(client, customer_id, camp["name"], budget_rn)
        _add_campaign_negatives(client, customer_id, campaign_rn, SHARED_NEGATIVES)
        print(f"Created (PAUSED): {camp['name']}")
        for ag in camp["ad_groups"]:
            ag_rn = _add_ad_group(client, customer_id, campaign_rn, ag["name"], ag["cpc"])
            n = _add_keywords(client, customer_id, ag_rn, ag["keywords"])
            _add_rsa(
                client, customer_id, ag_rn,
                camp["rsa_headlines"], camp["rsa_descriptions"], camp["final_url"],
            )
            print(f"  + {ag['name']}: {n} keywords, 1 RSA (paused)")
    print("\nDone. Everything is PAUSED — review in the UI before enabling.")


def main() -> None:
    p = argparse.ArgumentParser(description="Build Moncls campaigns (paused).")
    p.add_argument("--customer-id", required=True, help="Digits only, no dashes.")
    p.add_argument("--dry-run", action="store_true", help="Print plan, create nothing.")
    args = p.parse_args()
    build(args.customer_id.replace("-", ""), dry_run=args.dry_run)


if __name__ == "__main__":
    main()
