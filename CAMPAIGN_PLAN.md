# Moncls — New Google Ads Campaign Plan (launch-ready)

Built from historical analysis (see STRATEGY.md). Designed to buy the
**high-intent corporate / premium** customer — the opposite of the 2012
broad-match setup that drew price shoppers. Numbers here are starting points to
tune once live conversion data exists.

---

## Account structure

Two search campaigns, split by intent and geography. Keep them separate so
budget can't leak from high-value corporate/event terms into high-volume local
terms.

```
Campaign A — "Search | Daily Executive & Airport (DC Metro)"
    Geo: DC + Baltimore + Northern VA (radius targeting)      Priority: volume
    Ad group A1 — Executive Car Service
    Ad group A2 — Airport Transfers
    Ad group A3 — Chauffeured SUV / Sedan

Campaign B — "Search | Corporate & Event Ground Logistics (National)"
    Geo: National (US), bid-boost DC metro                    Priority: value
    Ad group B1 — Corporate Ground Transportation
    Ad group B2 — Event / Conference Transportation
    Ad group B3 — Delegation & Diplomatic
    Ad group B4 — Executive Roadshow / Multi-Day
```

Both campaigns share one account-level **negative keyword list** (below).

---

## Keywords (phrase & exact only — NO broad at launch)

### Campaign A — Daily / local
**A1 Executive Car Service**
- "executive car service washington dc"
- "corporate car service dc"
- "chauffeur service washington dc"
- "black car service dc"
- [executive car service dc]

**A2 Airport Transfers**
- "dulles airport car service"
- "reagan national airport car service"
- "dca car service"
- "iad car service"
- "bwi airport car service"
- "airport chauffeur washington dc"

**A3 Chauffeured SUV / Sedan**
- "chauffeured suv washington dc"
- "executive suv service dc"
- "private car service washington dc"

### Campaign B — Corporate / event / national
**B1 Corporate Ground Transportation**
- "corporate ground transportation"
- "corporate car service" (national)
- "business travel car service"
- "executive transportation services"

**B2 Event / Conference Transportation**
- "event transportation services"
- "corporate event transportation"
- "conference shuttle service"
- "event ground transportation company"

**B3 Delegation & Diplomatic**
- "delegation transportation services"
- "diplomatic car service"
- "embassy car service washington dc"
- "vip protection transportation" (review intent before enabling)

**B4 Executive Roadshow / Multi-Day**
- "executive roadshow transportation"
- "roadshow car service"
- "multi day chauffeur service"
- "multi day executive car service"

---

## Negative keywords (account-level shared list)

Price / wrong-tier: `cheap, discount, coupon, cheapest, affordable, budget,
deal, deals, rate, rates, price, cost`
Wrong product: `rental, rent, hire, car rental, uber, lyft, taxi, rideshare,
party bus, prom, homecoming, quinceanera, school bus, medical, non emergency,
ambulette, tow`
Employment: `job, jobs, salary, hiring, cdl, driver jobs, careers, employment`
Off-geo (from 2012 waste): `uk, london, aberdeen, yorkshire, surrey, cornwall,
kent, essex, cambridge, portsmouth, dorset, suffolk, gloucester, euro`
Research/DIY: `how to, start a, business plan, insurance, for sale, used`

> Note: `wedding` and `prom` are excluded to protect premium/corporate
> positioning. If you want that revenue, spin a separate campaign — don't let it
> contaminate corporate Quality Score.

---

## Ad copy (Responsive Search Ads)

**Campaign A (daily/airport) — headlines**
Executive Car Service DC · Chauffeured, On Time, Always · Dulles/DCA/BWI
Transfers · 24/7 Professional Chauffeurs · Corporate Accounts Welcome ·
Trusted Since [year] · Late-Model SUVs & Sedans · Flat-Rate Airport Pricing ·
Book in 60 Seconds
**Descriptions**
"Premium chauffeured transportation across the DC metro. Airport, executive,
and corporate travel — on time, every time." ·
"Professional chauffeurs, immaculate vehicles, flight tracking. Reserve online
or call now."

**Campaign B (corporate/event) — headlines**
Corporate Ground Logistics · Event & Conference Transportation · Trusted by
Global Institutions · Multi-Day Delegation Programs · Dedicated Account Manager
· Nationwide Chauffeur Network · Roadshow & Board-Meeting Ready · Diplomatic-Grade
Service
**Descriptions**
"End-to-end ground logistics for conferences, delegations, and multi-day
executive programs. Dedicated coordinator, vetted chauffeurs." ·
"Serving corporate and institutional clients nationwide. Request a proposal for
your next event."

> Every RSA: 12–15 headlines, 4 descriptions, pin 1 headline to the exact
> service, add sitelinks (Airport, Corporate, Events, Contact), callouts, and a
> call extension. Full asset lists to be generated at build time.

---

## Bidding & budget

- **Do NOT start on Maximize Conversions / tCPA** — there's no conversion
  history to train on. Start **Manual CPC** (or Maximize Clicks with a bid cap)
  for 2–4 weeks to gather data, then switch to **tCPA** once ~15–30 conversions
  accumulate.
- **Starting split** (adjust to your appetite): weight ~60% to Campaign B
  (higher value per booking) / ~40% to Campaign A. Set a modest daily cap per
  campaign, watch search-terms daily for the first two weeks, and mine negatives
  aggressively.
- **Location bid adjustments:** Campaign B national but +bid DC metro; Campaign
  A radius-target DC/Baltimore/NoVA only.

---

## Hard prerequisites before spending a dollar

1. **Conversion tracking live on moncls.com** — phone-call conversions (Google
   forwarding number) + booking-form submit + "request a proposal" submit.
   Without this we're flying blind and can't optimize. This is #1.
2. **Two landing pages** — one daily/airport, one corporate/event — matching ad
   intent (not the generic homepage).
3. **Basic Access** on the developer token (to launch via API rather than by
   hand in the UI).

---

## Launch sequence

1. Wire credentials into the environment → confirm read access (pull reports).
2. Confirm conversion tracking fires.
3. Build campaigns via `campaign_builder.py` in **PAUSED** state.
4. Human review of every keyword, negative, and ad in the UI.
5. Enable Campaign A first (faster feedback), then B.
6. Daily search-term mining for 2 weeks → then relax to weekly.
