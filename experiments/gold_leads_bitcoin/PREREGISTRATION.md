# Does gold lead Bitcoin? Pre-registration

Written 2026-09-19, BEFORE any price data was downloaded. Separate from the frozen V0/V1 research.

## Question
Over the last 10 years, does the direction of a gold ETF's weekly return predict the SAME direction
of Bitcoin's return the following week, more often than the baseline of always guessing Bitcoin's
more common weekly direction?

## Hunch (recorded before data)
Gold up this week -> Bitcoin up next week; gold down -> Bitcoin down. Same direction.

## Data (Yahoo Finance via yfinance; both are candidates to verify)
- Gold proxy: GLD (ETF, proxy for spot gold, not spot)
- Bitcoin: BTC-USD
- About 10 years of daily closes ending at run date.

## Weekly definition (to be checked in feasibility step, fixed before scoring)
Week = last available close on or before Friday. Weekly return = close / previous week's close - 1.
Yahoo BTC-USD daily bars close 00:00 UTC; GLD closes 4pm ET, so they differ by a few hours.
Main test (gold week t -> Bitcoin week t+1) uses Bitcoin's week t+1 window starting after gold's week t
ends, so no future information is used.

## Split (fixed by week count, not by looking at results)
- Exploration: earlier ~7 years. Untouched: most recent ~3 years (~156 weeks), scored ONCE.

## Rule
Predict sign(BTC week t+1) = sign(GLD week t).
Baseline: always predict the more common Bitcoin weekly direction, taken from the EXPLORATION period.

## Outcome (main test only, untouched period)
- SUPPORTED: rule accuracy >= baseline accuracy + 8 percentage points.
- REJECTED for practical purposes: rule accuracy <= baseline accuracy.
- INCONCLUSIVE: anything between.
- Data infeasible (large gaps / cannot define weeks): reported as infeasible, not as rejection.

## Exploratory only (cannot count as a win)
Reverse direction (BTC -> GLD), opposite-sign version, era breakdowns.

## Limits
Small sample (~156 weeks): luck alone moves accuracy ~4 points. GLD is a proxy. Dollar deliberately
excluded (possible common cause). Positive result is not evidence of profitability or causation.
Budget: a few hours, no money. No rule changes after seeing untouched results.
