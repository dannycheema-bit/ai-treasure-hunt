# Lagging-theme earnings inflection: methodology (phase 1)

AI assistants ran a user-adopted research prompt ("Visser Research + Jev, Reusable Research Prompt"
v1.1) and the user's follow-up choices. This file contains no subscriber research content. Outputs
that quote subscriber research stay local and git-ignored.

## Brief (user chose the prompt defaults on 2026-10-12)
- **Decision:** find new ideas where earnings are turning up but the chart has not caught up.
- **Universe:** every company in the four lagging themes of the user's 100-name list (83 names).
  The two strong themes and the five macro satellites are excluded by the brief, not by screening.
- **Horizon:** the next 2–4 reporting periods (to about Q2 2027 results).
- **Events:**
  - **E, earnings step-up:** a material rise in recurring consolidated operating earnings, sustained
    across two comparable periods, relative to continuation of the current business.
  - **G, expectations asymmetry:** revenue at least 5% above the consensus frozen on 2026-10-12, in
    two consecutive periods.
- **Rubric (default):**

  | Component | Weight | Phase-1 status |
  |---|---|---|
  | Jev P(E) | 30% | Pending |
  | Operating-earnings magnitude | 25% | Proxy computed |
  | Technical transition | 20% | Computed |
  | Reporting-commentary progression | 15% | Computed for all 83 (12 Oct baseline) |
  | Jev P(G) | 10% | Pending |

## Coverage funnel (phase 1)
- **Agreed universe:** 83 companies.
- **Data fetched:** 83, with no errors.
- **Technicals:** 82. ET is unavailable because Yahoo has only 9 days of price history; it stays
  unavailable rather than being scored 0.
- **Magnitude proxy:** 83.
- **90-day revisions:** 81. BIPC and VISN have only 1 analyst.
- **Commentary progression:** 83 (12 Oct baseline, before Q3 reports).
- **Jev assessments:** 0. Jev is not connected, so these are not simulated.

## Components
- **Technical transition:** computed from about 2 years of daily adjusted closes.

  | State | Score | Rule |
  |---|---|---|
  | Extended | 40 | Price more than 35% above the 200-day average, or RSI above 75 |
  | Early improving | 90 | Price above the 50-day average and within 12% of it; the 50-day slope is rising after a flat or falling month; RSI 70 or below |
  | Established uptrend | 65 | Price above both averages, and both averages rising |
  | Basing | 55 | Price below the 50-day average, but the 50-day slope is improving and RSI is at least 45 |
  | Deteriorating | 15 | Price below a falling 50-day average |
  | Neutral | 45 | Anything else |

  The score rewards a fresh turn, not a static strong chart.
- **Magnitude proxy:** consensus next-fiscal-year EPS growth (Yahoo) mapped to score anchors.

  | Growth | Below 0% | 0–10% | 10–20% | 20–35% | 35–60% | Above 60% |
  |---|---|---|---|---|---|---|
  | Score | 10 | 30 | 50 | 70 | 85 | 95 |

  Two special cases: a loss turning to profit scores 75, and a company still loss-making scores 20.
- **Data-quality rule, applied to every company:** if Yahoo and the user's Fundamentals file disagree
  by more than 15 points, the more conservative score is kept and the case is flagged. Most
  disagreements come from fiscal-year alignment or reported-versus-adjusted EPS. Growth above 150%
  and coverage under 3 analysts are also flagged.

  This is a proxy. It does not yet isolate the driver-specific step-up or the company's
  concentration in the theme.
- **Unscored diagnostics:**
  - 90-day change in next-fiscal-year EPS consensus
  - Upward and downward revision counts over 30 days
  - Last 4 EPS surprises
  - Latest year-on-year change in operating income
  - Next report date
- **Frozen consensus:** revenue estimates for the current quarter, next quarter and next two fiscal
  years, as of 2026-10-12 13:08 UTC. This is the baseline for G. It is stored locally.

- **Commentary progression (phase 2):** six AI research agents applied one identical written brief to
  every company.
  - **Inputs:** the exposed product line; the four most recent reporting checkpoints (cadence
    respected); counterevidence.
  - **Ladder:** 1 opportunity, 2 named product, 3 design win, 4 order/backlog, 5 production,
    6 delivery, 7 recognized revenue, 8 recurring profit.
  - **Score anchors:**

    | Score | Meaning |
    |---|---|
    | 90 | Stage 6–8 with acceleration |
    | 75 | Recently advanced a stage |
    | 60 | Steady at stage 4–5 |
    | 45 | Early, stage 2–3 |
    | 30 | Vague, or no exposure |
    | 15 | Reversal |

  - Each score carries an evidence-quality rating and sources.
  - Results were checked for one row per company, the exact column set and no blanks, and four claims
    were spot-checked against independent primary sources.
  - Known limitation: scores cluster at 80–90, so treat that range as one band.
  - A post-earnings re-score is scheduled against this archived baseline.

## Missing values
Pending components are never filled with 0 or 50, and the remaining weights are never silently
rescaled. Each name shows partial points out of the 45 available, plus its attainable range (adding
up to 55). Because 55% is missing for every name, the phase-1 order is a tier guide, not a ranking.

## Sources
- The user's AI Macro Nexus files: Fundamentals (2026-09-25 and 2026-10-09), Technical v3
  (2026-09-19), Exhaustion Scores (2026-09-19), the 100-name list deck, and the 2026-10-12 research
  paper.
- Yahoo Finance via yfinance 1.2.0, fetched 2026-10-12.

## Reproduce
```
python fetch.py     # writes raw/ (git-ignored)
python analyze.py   # writes first_pass.xlsx, first_pass.json, frozen_consensus_2026-10-12.json
```

Probabilities, once Jev supplies them, are subjective and uncalibrated. This is research, not
personalized investment advice.
