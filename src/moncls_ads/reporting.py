"""Read-only reporting queries against a Google Ads account (GAQL).

These are the pulls we need to understand the account before changing
anything: campaign performance, keyword performance, and the search-terms
report (what people actually typed) over a lookback window.

Nothing here writes to the account.
"""

from __future__ import annotations

from typing import Iterator

from google.ads.googleads.client import GoogleAdsClient

# Google Ads date ranges: LAST_30_DAYS, LAST_90_DAYS, LAST_7_DAYS, etc.
DEFAULT_RANGE = "LAST_30_DAYS"


def _run(client: GoogleAdsClient, customer_id: str, query: str) -> Iterator[dict]:
    """Execute a GAQL query and yield each row as a flat dict."""
    ga_service = client.get_service("GoogleAdsService")
    stream = ga_service.search_stream(customer_id=customer_id, query=query)
    for batch in stream:
        for row in batch.results:
            yield row


def campaign_performance(
    client: GoogleAdsClient, customer_id: str, date_range: str = DEFAULT_RANGE
) -> list[dict]:
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_per_conversion
        FROM campaign
        WHERE segments.date DURING {date_range}
        ORDER BY metrics.cost_micros DESC
    """
    return [
        {
            "campaign": r.campaign.name,
            "status": r.campaign.status.name,
            "channel": r.campaign.advertising_channel_type.name,
            "impressions": r.metrics.impressions,
            "clicks": r.metrics.clicks,
            "ctr": round(r.metrics.ctr, 4),
            "avg_cpc": r.metrics.average_cpc / 1_000_000,
            "cost": r.metrics.cost_micros / 1_000_000,
            "conversions": r.metrics.conversions,
            "conv_value": r.metrics.conversions_value,
            "cost_per_conv": r.metrics.cost_per_conversion / 1_000_000,
        }
        for r in _run(client, customer_id, query)
    ]


def keyword_performance(
    client: GoogleAdsClient, customer_id: str, date_range: str = DEFAULT_RANGE
) -> list[dict]:
    query = f"""
        SELECT
            campaign.name,
            ad_group.name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.cost_per_conversion
        FROM keyword_view
        WHERE segments.date DURING {date_range}
        ORDER BY metrics.cost_micros DESC
    """
    return [
        {
            "campaign": r.campaign.name,
            "ad_group": r.ad_group.name,
            "keyword": r.ad_group_criterion.keyword.text,
            "match_type": r.ad_group_criterion.keyword.match_type.name,
            "impressions": r.metrics.impressions,
            "clicks": r.metrics.clicks,
            "cost": r.metrics.cost_micros / 1_000_000,
            "conversions": r.metrics.conversions,
            "cost_per_conv": r.metrics.cost_per_conversion / 1_000_000,
        }
        for r in _run(client, customer_id, query)
    ]


def search_terms(
    client: GoogleAdsClient, customer_id: str, date_range: str = DEFAULT_RANGE
) -> list[dict]:
    """What users actually searched — the raw material for negative keywords."""
    query = f"""
        SELECT
            search_term_view.search_term,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING {date_range}
        ORDER BY metrics.cost_micros DESC
    """
    return [
        {
            "search_term": r.search_term_view.search_term,
            "campaign": r.campaign.name,
            "impressions": r.metrics.impressions,
            "clicks": r.metrics.clicks,
            "cost": r.metrics.cost_micros / 1_000_000,
            "conversions": r.metrics.conversions,
        }
        for r in _run(client, customer_id, query)
    ]
