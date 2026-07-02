"""Machine-readable version of CAMPAIGN_PLAN.md — the data campaign_builder reads.

Keep this in sync with CAMPAIGN_PLAN.md (the human-readable rationale).
Budgets and CPCs are conservative starting points; tune once live data exists.
Update final_url to the real landing pages before launch.
"""

# Placeholder — replace with the real per-intent landing pages before launch.
_DAILY_URL = "https://moncls.com/"
_CORPORATE_URL = "https://moncls.com/"

# Geo targeting. Campaign A is local (radius around DC covering Baltimore + NoVA);
# Campaign B is national US. Google geo target constant 2840 = United States.
# Proximity radius is in miles from the DC city center.
_DC_LOCAL_GEO = {
    "type": "proximity",
    "lat": 38.9072,
    "lng": -77.0369,
    "radius_miles": 50,  # covers DC, Baltimore (~40mi), and Northern Virginia
}
_NATIONAL_GEO = {
    "type": "geo_targets",
    "geo_target_constant_ids": ["2840"],  # United States
}
# English only, on both campaigns. Language constant 1000 = English.
_LANGUAGE_IDS = ["1000"]

SHARED_NEGATIVES = [
    # price / wrong-tier
    "cheap", "discount", "coupon", "cheapest", "affordable", "budget",
    "deal", "deals", "rate", "rates", "price", "cost",
    # wrong product
    "rental", "rent", "hire", "car rental", "uber", "lyft", "taxi",
    "rideshare", "party bus", "prom", "homecoming", "school bus",
    "medical", "non emergency", "ambulette", "tow",
    # employment
    "job", "jobs", "salary", "hiring", "cdl", "driver jobs", "careers",
    # off-geo (2012 waste)
    "uk", "london", "aberdeen", "yorkshire", "surrey", "cornwall", "kent",
    "essex", "cambridge", "portsmouth", "dorset", "suffolk", "euro",
    # research / DIY
    "how to", "start a", "business plan", "for sale", "used",
]

_DAILY_HEADLINES = [
    "Executive Car Service DC", "Chauffeured, On Time, Always",
    "Dulles / DCA / BWI Transfers", "24/7 Professional Chauffeurs",
    "Corporate Accounts Welcome", "Late-Model SUVs & Sedans",
    "Flat-Rate Airport Pricing", "Book Your Ride in Minutes",
    "Premium DC Chauffeur Service", "Flight-Tracked Airport Pickups",
    "Washington DC Black Car", "Reliable Executive Transport",
]
_DAILY_DESCRIPTIONS = [
    "Premium chauffeured transportation across the DC metro. Airport, executive, and corporate travel.",
    "Professional chauffeurs, immaculate vehicles, flight tracking. Reserve online or call now.",
    "On time, every time. Serving DC, Baltimore, and Northern Virginia.",
    "Trusted chauffeured service for executives and corporate accounts.",
]

_CORPORATE_HEADLINES = [
    "Corporate Ground Logistics", "Event & Conference Transportation",
    "Trusted by Global Institutions", "Multi-Day Delegation Programs",
    "Dedicated Account Manager", "Nationwide Chauffeur Network",
    "Roadshow & Board-Meeting Ready", "Diplomatic-Grade Service",
    "Executive Event Transportation", "Vetted Professional Chauffeurs",
    "End-to-End Ground Logistics", "Request a Proposal Today",
]
_CORPORATE_DESCRIPTIONS = [
    "End-to-end ground logistics for conferences, delegations, and multi-day executive programs.",
    "Dedicated coordinator, vetted chauffeurs. Serving corporate and institutional clients nationwide.",
    "Multi-day event transportation managed start to finish. Request a proposal.",
    "Institutional-grade chauffeured service for high-stakes corporate travel.",
]

CAMPAIGN_PLAN = [
    {
        "name": "Search | Daily Executive & Airport (DC Metro)",
        "daily_budget": 40.0,
        "final_url": _DAILY_URL,
        "geo": _DC_LOCAL_GEO,
        "language_ids": _LANGUAGE_IDS,
        "rsa_headlines": _DAILY_HEADLINES,
        "rsa_descriptions": _DAILY_DESCRIPTIONS,
        "ad_groups": [
            {
                "name": "Executive Car Service",
                "cpc": 6.0,
                "keywords": [
                    "\"executive car service washington dc\"",
                    "\"corporate car service dc\"",
                    "\"chauffeur service washington dc\"",
                    "\"black car service dc\"",
                    "[executive car service dc]",
                ],
            },
            {
                "name": "Airport Transfers",
                "cpc": 5.5,
                "keywords": [
                    "\"dulles airport car service\"",
                    "\"reagan national airport car service\"",
                    "\"dca car service\"",
                    "\"iad car service\"",
                    "\"bwi airport car service\"",
                    "\"airport chauffeur washington dc\"",
                ],
            },
            {
                "name": "Chauffeured SUV / Sedan",
                "cpc": 5.5,
                "keywords": [
                    "\"chauffeured suv washington dc\"",
                    "\"executive suv service dc\"",
                    "\"private car service washington dc\"",
                ],
            },
        ],
    },
    {
        "name": "Search | Corporate & Event Ground Logistics (National)",
        "daily_budget": 60.0,
        "final_url": _CORPORATE_URL,
        "geo": _NATIONAL_GEO,
        "language_ids": _LANGUAGE_IDS,
        "rsa_headlines": _CORPORATE_HEADLINES,
        "rsa_descriptions": _CORPORATE_DESCRIPTIONS,
        "ad_groups": [
            {
                "name": "Corporate Ground Transportation",
                "cpc": 8.0,
                "keywords": [
                    "\"corporate ground transportation\"",
                    "\"corporate car service\"",
                    "\"business travel car service\"",
                    "\"executive transportation services\"",
                ],
            },
            {
                "name": "Event / Conference Transportation",
                "cpc": 8.0,
                "keywords": [
                    "\"event transportation services\"",
                    "\"corporate event transportation\"",
                    "\"conference shuttle service\"",
                    "\"event ground transportation company\"",
                ],
            },
            {
                "name": "Delegation & Diplomatic",
                "cpc": 9.0,
                "keywords": [
                    "\"delegation transportation services\"",
                    "\"diplomatic car service\"",
                    "\"embassy car service washington dc\"",
                ],
            },
            {
                "name": "Executive Roadshow / Multi-Day",
                "cpc": 9.0,
                "keywords": [
                    "\"executive roadshow transportation\"",
                    "\"roadshow car service\"",
                    "\"multi day chauffeur service\"",
                    "\"multi day executive car service\"",
                ],
            },
        ],
    },
]
