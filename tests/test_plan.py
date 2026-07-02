"""Fast, dependency-free checks on the campaign plan and builder logic.

Run: PYTHONPATH=src python3 tests/test_plan.py
Guards against silent regressions: broad-match creeping in, geo targeting
going missing (the 2012 mistake), or the plan drifting out of shape.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from moncls_ads.plan import CAMPAIGN_PLAN, SHARED_NEGATIVES
from moncls_ads.campaign_builder import _parse_keyword


def test_no_broad_match():
    # Every keyword must resolve to PHRASE or EXACT — never broad.
    for camp in CAMPAIGN_PLAN:
        for ag in camp["ad_groups"]:
            for kw in ag["keywords"]:
                _, match = _parse_keyword(kw)
                assert match in ("PHRASE", "EXACT"), f"broad match leaked: {kw}"


def test_exact_and_phrase_parsing():
    assert _parse_keyword("[executive car service dc]") == ("executive car service dc", "EXACT")
    assert _parse_keyword('"corporate car service dc"') == ("corporate car service dc", "PHRASE")


def test_every_campaign_has_geo():
    # The whole point: no campaign may run everywhere by accident.
    for camp in CAMPAIGN_PLAN:
        geo = camp.get("geo", {})
        assert geo.get("type") in ("proximity", "geo_targets"), f"{camp['name']} missing geo"
        if geo["type"] == "proximity":
            assert geo["radius_miles"] > 0
        else:
            assert geo["geo_target_constant_ids"], "empty geo target list"


def test_plan_shape():
    assert len(CAMPAIGN_PLAN) == 2
    for camp in CAMPAIGN_PLAN:
        assert camp["daily_budget"] > 0
        assert camp["ad_groups"], "campaign has no ad groups"
        assert len(camp["rsa_headlines"]) >= 3, "RSA needs >=3 headlines"
        assert len(camp["rsa_descriptions"]) >= 2, "RSA needs >=2 descriptions"
        assert camp["language_ids"], "no language targeting"
        for ag in camp["ad_groups"]:
            assert ag["keywords"], f"{ag['name']} has no keywords"
            assert ag["cpc"] > 0


def test_negatives_cover_known_waste():
    # The exact terms that sank the 2012 account must be blocked.
    lowered = {n.lower() for n in SHARED_NEGATIVES}
    for must in ("cheap", "discount", "rental", "uber", "jobs", "london", "aberdeen"):
        assert must in lowered, f"missing critical negative: {must}"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
