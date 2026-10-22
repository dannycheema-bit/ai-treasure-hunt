# Do revenue beats still move prices? Pre-registration (Q3 2026 reporting season)

Written **2026-10-22**, before any company in the primary sample reported, and before any post-report
price or result was examined for any company in the universe. Separate from all other experiments in this
repo; it reuses only the frozen inputs listed below.

## Question
For companies in the agreed AI-infrastructure universe, does beating the **frozen 12 Oct 2026 revenue
consensus by at least 5%** lead to a better **5-trading-day market-relative price reaction** than a revenue
**miss**, in the Q3 2026 reporting season?

## Competing hypotheses (both stated before data)
- **Classic link holds** (earnings-momentum / post-earnings-drift view): beats clearly outperform misses.
- **Link weak** (Visser, *Machine-Time Economics, Human-Time Capital*, 19 Oct 2026): rising risk premia and
  less confidence in terminal values mean beats can fall as multiples compress, so the difference is small
  or absent.

## Frozen inputs (local, git-ignored; identified by hash)
- **Universe:** the 83 companies in `../ai_nexus_lagging_inflection/first_pass.json` (four lagging AI
  themes of the user's 100-name list). Sorted ticker list SHA-256
  `0ad7e7bb582d30e58f30091c2ace6323c4307dec20992c836d1415d7287dc4d1`. The tickers are not published here
  because the list derives from subscriber research.
- **Consensus:** `../ai_nexus_lagging_inflection/frozen_consensus_2026-10-12.json`, SHA-256
  `564e270f8a6e85ee0f68d8c493efa89149b0637601d3e5698cef63c984950c53`. The comparator is the `0q` revenue
  estimate, i.e. the first quarter reported after 12 Oct.

## Samples
- **PRIMARY:** universe companies whose first report after 2026-10-12 is dated **2026-10-23 to 2026-11-30
  inclusive** (actual date from Yahoo earnings dates). About 68 are expected.
- **SECONDARY (separate, cannot decide the result):** companies that reported 2026-10-13 to 2026-10-22,
  before registration (6 expected).
- Later reporters (Dec 2026 or 2027) are excluded and listed.

## Measurements
- **Revenue surprise** = reported total revenue for that quarter (Yahoo quarterly income statement) ÷
  frozen `0q` consensus − 1.
  - **Alignment check:** the reported quarter must end after 2026-06-30 and before the report date.
  - Any |surprise| > 50% is treated as a probable period or currency misalignment: excluded and listed,
    never "fixed" by hand.
- **Groups:**
  - BEAT: surprise ≥ +5%.
  - MISS: surprise < 0%.
  - IN-LINE: 0% to < 5% (reported, but not part of the main comparison).
- **Reaction window:**
  - Pre price: the last regular-session close strictly before the announcement.
  - First reaction session: the announcement date if it was made before that market's close, otherwise
    the next session.
  - Post price: the close of the 5th trading session from (and including) the first reaction session.
  - Prices are split- and dividend-adjusted (Yahoo).
- **Market-relative return** = stock return − benchmark return over the same dates:

  | Listing | Benchmark |
  |---|---|
  | US | SPY |
  | Japan (.T) | ^N225 |
  | Germany (.DE) | ^GDAXI |
  | France (.PA) | ^FCHI |
  | Netherlands (.AS) | ^AEX |
  | UK (.L) | ^FTSE |
  | Italy (.MI) | FTSEMIB.MI |
  | India (.NS) | ^NSEI |

## Statistic and decision rule (PRIMARY sample only)
- **D** = median market-relative 5-day return of BEAT − median of MISS, in percentage points.
- **Feasibility:** at least 5 names in BEAT and at least 5 in MISS; otherwise **INCONCLUSIVE (too few)**.
- **CLASSIC LINK HOLDS:** D ≥ +3.0 pp.
- **LINK WEAK (Visser supported):** D ≤ +1.0 pp.
- **INCONCLUSIVE:** +1.0 < D < +3.0 pp.

## Reported alongside (cannot change the verdict)
- Spearman correlation between surprise % and market-relative return across all PRIMARY names (BEAT,
  IN-LINE and MISS).
- The same statistics for the SECONDARY sample.
- The same split using Yahoo's EPS surprise % instead of revenue.
- Results for the phase-1 "unpriced inflection" names and the top-10 research-card names.

## Scoring
- **Once, on or after 2026-12-08**, after the last primary report (30 Nov) plus 5 sessions.
- Code: `score.py`, committed with this file before scoring.
- No changes to thresholds, windows, benchmarks or groups after this commit.

## Limits
- About 68 names with heavily correlated AI exposure in one season, so this is one draw.
- Group sizes may be small, and medians are noisy.
- Yahoo data can be revised, and period or currency alignment can fail (handled by exclusion).
- Guidance changes ("beat and raise") are not measured systematically.
- A LINK WEAK result is consistent with Visser's thesis but does not prove its mechanism (risk premium
  versus, for example, positioning or market regime).
- Research, not advice.
