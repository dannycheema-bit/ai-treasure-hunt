# Jev usage-inflection assessments: 46 crypto names (exploratory)

This is **separate from the pre-registered basket-vs-Bitcoin test** in `../PREREGISTRATION.md`, whose
rules, list and scoring are unchanged. It was run on 2026-10-13 with TypeSafe Jev, requested as
`jev-latest` and returned as `jev-1.13.0`, through the official HTTP API (`../../ai_nexus_lagging_inflection/jev_client.py`).

## Question (the same schema for every name)
- **U, usage inflection (Noul).**
  - Tokens: fees paid in the 90 days ending 2026-03-31 must be at least 25% above the 90 days ending on
    the baseline date, from organic use rather than incentives, emissions or one-offs.
  - Stocks: revenue for the March 2027 quarter must be at least 25% above the latest reported quarter.
- **VA, value accrual (Noul, tokens only):** whether a meaningful share of fees reaches token holders.
- **T, timing (Noul):** given U, whether the growth is visible by 2026-12-31. P(early) = P(U) × P(early | U).
- **EQ, evidence quality (Score 0–2).**
- **Scenario cases:** U is asked again under adverse, base and favourable premises (neutral, generic wording).

## Evidence sent (public only; no price data and no subscriber material)
- DefiLlama fees and revenue: 90- and 30-day windows, prior windows, the same window a year ago, and TVL.
- CoinGecko circulating share of fully diluted value.
- Yahoo Finance quarterly revenue and consensus for CRCL, COIN, HOOD and FIGR.
- **Coverage:** 40 of 42 tokens have DefiLlama fee data. TAO and GRASS have none, and HNT shows zero, so
  those three are sent as missing.
- RUNE uses THORChain DEX fees.

## Baseline frozen for later validation
`baseline_2026-10-13.json` (local, git-ignored), SHA-256 `313e35806fa4404e02b9d6b5b8d4004ff03685bc696997d322ad79ece183d78f`.

After 2027-03-31, compare actual DefiLlama 90-day fees (and stock revenue) with this baseline to score
each forecast.

## Results summary (2026-10-13)
- **Volume:** 184 requests, about 148k input tokens.
- **Spread:** P(U) runs from 0.11 to 0.40, with a median of 0.23. Jev rates a 25% six-month usage jump as
  unlikely for most names, so it separates names only weakly.
- **Consistency:**
  - P(U) has a rank correlation of 0.74 with recent 90-day fee momentum.
  - Scenario order (adverse ≤ base ≤ favourable) holds for every name.
- **Value accrual separates names more clearly:** from about 0.10 (BTC, ZEC, XMR) to about 0.70 (RUNE).
- **Missing-data caveat:** names with no usage data (TAO, GRASS) received mid-range P(U) of 0.26–0.29.
  These reflect an absence of evidence, not a measured outlook, so they are not comparable with the rest.

Probabilities are subjective and uncalibrated for this use. This is research, not advice.
