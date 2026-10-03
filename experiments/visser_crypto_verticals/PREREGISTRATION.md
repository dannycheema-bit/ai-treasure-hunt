# Does Visser's 46-name basket beat Bitcoin? Pre-registration

Written 2026-10-03, BEFORE any price after 2026-09-30 was examined. Approved via Socrates Mode brief.
Separate from the frozen V0/V1 research. Source notes: SOURCE.md.

## Question
Will an equal-weighted basket of the 46 names in the Visser-Labs 46-name Tokenized Index
(frozen at the list published as of the 2026-09-21 close), bought at the 2026-09-30 close and left
untouched, beat Bitcoin's simple price return by the 2026-12-31 close?

## Hunch (Visser's claim, not ours)
"Broadening": like semis vs Nvidia, the equal-weight basket beats the leader (07:43 in "vertical 1").

## Frozen universe
- `STACK.csv`, 46 rows (42 tokens, 4 stocks), SHA-256
  `905ec5e2fd9e2c95d7ce8d4e5f4977111254863087123a6cdb9045029f870f19`.
- Source: https://ai.22vresearch.com/wp-content/uploads/2026/09/Visser-Labs-46-Tokenized-Crypto-Index.pdf
  (title "Visser-Labs 46-name Tokenized Index - September 21, 2026 close", created 2026-09-22).
- Public copy lists names only; Visser's own Sept 21 closes and weights are kept locally, not published.
- Any membership change Visser makes later is IGNORED. Bitcoin stays in the basket (1/46).

## Timestamps (match Visser's own reset convention)
- Start: 2026-09-30 16:00 America/New_York = 20:00 UTC.
- End:   2026-12-31 16:00 America/New_York = 21:00 UTC (DST ends Nov 1).

## Prices
- Tokens: CoinGecko USD, `price_source_id` column. Use the observation nearest the timestamp,
  within ±90 minutes; record the actual observation time.
- Stocks (CRCL, COIN, HOOD, FIGR): Yahoo Finance (yfinance) regular-session close on 2026-09-30 and
  2026-12-31, unadjusted Close (no dividends are expected to matter; returns are price-only, as in Visser's index).
- Bitcoin benchmark: the same CoinGecko `bitcoin` observations used inside the basket.
- Start prices are captured early (CoinGecko free hourly history lasts ~90 days). Capturing the start
  snapshot reveals nothing about the outcome.

## Calculation
- Basket return = mean over 46 names of (end / start − 1). Buy-and-hold, equal notional at start,
  no rebalancing, no costs.
- Bitcoin return = BTC end / start − 1.
- Gap = basket return − Bitcoin return, in percentage points.

## Outcome (scored ONCE, after 2026-12-31)
- SUPPORTED: gap ≥ +10 pp.
- REJECTED: gap ≤ 0.
- INCONCLUSIVE: 0 < gap < +10 pp.
- INFEASIBLE (not a rejection): price unavailable for more than 3 of 46 names at either end.

## Missing / dead names
- Up to 3 names unavailable at the end: use the last available CoinGecko price before 21:00 UTC Dec 31;
  if it has no price at all after start (delisted/defunct), its return is −100%. Never drop a name.
- Start price unavailable for a name: counted toward the >3 infeasibility limit; if ≤3, that name is
  scored from the first observation after start within 24h, flagged in the result.

## Exploratory only (cannot count as a win)
Per-vertical returns; tokens vs the 4 stocks; our number vs Visser's own Q4 report; ex-BTC basket.

## Limits
One quarter = one draw; 45 volatile small names vs BTC can differ by >10 pp by luck. A SUPPORTED result
is weak evidence, not proof of skill or a reason to trade. The list was chosen after a +60% run, so
momentum and selection skill are confounded. No rule changes, alternative start dates, or name
removals after 2026-09-30. Budget: a few hours, no money.
