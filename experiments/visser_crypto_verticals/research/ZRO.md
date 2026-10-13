# LayerZero (ZRO) — research note (updated 2026-10-13 with independent view)

Compiled 2026-10-11 from public sources (listed at the end). Educational notes only; not investment
advice. This note is OUTSIDE the pre-registered test: it does not change the frozen list, rules or
scoring in `../PREREGISTRATION.md`. Figures from aggregator sites were cross-checked where possible;
conflicts are flagged.

## Where it sits in the experiments
- **Visser 46-name index:** vertical *Oracle, Data & Interop Middleware* (with LINK, PYTH, GRT).
- **Danny's Crypto Portfolio v1:** not held.
- Already a big early mover: about +41% between Visser's Sept 21 report and the Sept 30 start price,
  and the best name in the 46 on the first daily check (Oct 3).

## What it is (plain English)
LayerZero is **messaging plumbing between blockchains**. An app on one chain can send a verified
message to another chain — e.g. "lock 10 tokens here, release 10 there". Apps choose who verifies
each message: one or more **DVNs** (decentralized verifier networks). More independent DVNs = safer.

It is expanding into two new products:
- **Zero** (announced Feb 2026): its own Layer-1 blockchain aimed at financial markets, using
  zero-knowledge proofs. ZRO is planned as its staking (security), gas and governance token. Announced
  "in collaboration with" Citadel Securities, DTCC, ARK Invest and ICE (The Block). No confirmed
  mainnet date found.
- **ATLAS** (announced Aug 25, 2026): a "headless exchange" back-end (matching, clearing, settlement,
  risk) that venues and brokers run under their own brand. Expected to launch "later this year".

## Token facts (CoinGecko, 2026-10-11)
| | |
|---|---|
| Max / total supply | 1,000,000,000 ZRO |
| Circulating | ~399 million (~40%) |
| Market cap / fully diluted | ~$0.83 bn / ~$2.07 bn |
| All-time high / low | Dec 2024 / Jul 31 2026 |
| 30-day / 1-year change | roughly +108% / +17% |
| CoinGecko rank | #88 |

The gap between market cap and fully diluted value is the supply still to be released.

## How value could flow to ZRO (the "token story")
1. **ATLAS fees:** after venue rebates (20–65%, more for venues staking ZRO), 25% of the remaining fee
   goes to market creators and **75% buys and burns ZRO** (The Block). Only matters once ATLAS has volume.
2. **Stargate buybacks (live now):** ~2.37m ZRO bought for ~$3.33m through August per the official
   tracker; reported ~2.54m after a 162k purchase on Oct 6 (Altcoin Buzz).
3. **Protocol fee switch (NOT active):** four referendums so far; the June 2026 vote failed to reach
   quorum. Another vote is planned for **December 2026**; if passed, message fees fund buyback-and-burn.
   (One older source says it was activated in Dec 2025 — contradicted by the Oct 2026 report.)
4. **Zero staking/gas:** future demand if Zero launches and is used.
5. **Stargate (STG) merger:** exchanges converting STG to ZRO at 1 STG = 0.08634 ZRO (Binance done;
   KuCoin Oct 9–10, 2026).

## Supply pressure (the other side)
- Monthly unlocks continue to **May 2027**, about **eight** left.
- **Next: Oct 20, 2026, ~23.6m ZRO** (~6% of circulating) — ~10.6m core contributors, ~13m strategic
  partners (DefiLlama via Altcoin Buzz). Other trackers say 23.1m or 31.25m; treat as approximate.
- Rough scale: one monthly unlock (~23m) is about ten times all buybacks to date (~2.5m).

## Risks and open questions
- **KelpDAO exploit (Apr 18, 2026):** ~$292m of rsETH released through a forged cross-chain message.
  The bridge trusted a single verifier (1-of-1 DVN) whose RPC nodes were compromised; the attacker then
  borrowed ~$190m against it on Aave, leaving large bad debt. LayerZero blamed Kelp's single-verifier
  setup and attributed the attack likely to Lazarus; it now refuses to sign for 1-of-1 apps and
  recommends 3–5 DVNs. **Kelp's parent sued LayerZero in British Columbia (Sept 2026)**, claiming
  LayerZero endorsed that setup. Outcome unknown.
- **Execution:** Zero and ATLAS are announced, not proven at scale. The burn story depends on them.
- **Governance:** the fee switch has repeatedly failed on turnout, not opposition.
- **Momentum:** +100% in a month, after an all-time low in July; big moves both ways are normal here.
- **Competition:** other interoperability networks (e.g. Chainlink CCIP, also in this vertical).

## Dates inside the test window (Sep 30 – Dec 31, 2026)
- Oct 20 and ~Nov 20 / ~Dec 20: monthly unlocks.
- "Later this year": ATLAS launch.
- December: fee-switch referendum.
- Ongoing: KelpDAO lawsuit.

## Questions worth answering next (Peter Lynch style)
- How much daily message volume and fee revenue does LayerZero generate today, and what would the fee
  switch have earned?
- Who are the first ATLAS venues, and what volume would cover one monthly unlock with burns?
- How many apps still run with a single DVN?

---

# Study-first update and independent view (2026-10-13)

## Measure what actually happens on-chain (DefiLlama, to 13 Oct 2026)
| Window | Messaging fees | Holder revenue (buybacks) |
|---|---|---|
| Last 90 days | $0.62m | $0.32m |
| Prior 90 days | $0.51m (+22%) | $0.48m |
| Same 90 days a year ago | $1.53m (**−59% y/y**) | n/a |
| Last 365 days | $2.13m | $3.39m |

- Value held in LayerZero contracts (TVL) is about $11.1bn. Even so, **fee usage is well below a year ago.**
  The recent quarter's +22% is a rebound from a low base.
- Fees are small partly by design: the protocol fee switch is off, so most messaging costs go to the
  verifier networks and executors, not to ZRO holders. That makes them a lower bound on activity.
- **Migrations after the Kelp hack:**
  - **Kelp** (rsETH) is moving to Chainlink CCIP.
  - **Solv** is migrating more than $700m of tokenized-bitcoin infrastructure away from LayerZero.
  - At the time of the hack, 47% of about 2,665 active LayerZero apps ran a single verifier (CoinGecko/Dune).
  - LayerZero admitted it "made a mistake", now refuses to sign single-verifier setups, and has added the
    Blockaid security integration (8 Oct).

## Follow the token: supply versus demand
| Flow | Size |
|---|---|
| Next monthly unlock, **20 Oct 2026** | ~23.6–25.7m ZRO (sources differ), about $48–53m at $2.05, ~6% of circulating supply |
| Remaining unlocks | about 8 monthly releases to **May 2027** |
| Cumulative buybacks to date (Stargate revenue) | ~2.54m ZRO, ~$5.4m |
| ATLAS burn (75% of post-rebate fees) | not yet producing measured flow |

**What consensus skips:**
- **A single monthly unlock is about 9–10× all buybacks ever made.**
- **To offset unlocks** with ATLAS burns alone, ATLAS would need about $65–70m a month of post-rebate fees,
  similar to **Hyperliquid's entire fee base** (about $76m a month on DefiLlama). That is a very high bar for
  a product that has not yet shown live volume.
- **The supply window is finite.** It ends in about May 2027, much sooner than Chainlink's roughly
  three-year tail. After that, any real burn would act on a fixed supply.

## Valuation, roughly
- Market cap about $0.82bn; fully diluted about $2.05bn; price $2.05.
- **Up about 100% in 30 days.** It was flat over a year, after an all-time low on 31 Jul 2026.
- Market cap / annual messaging fees ≈ **385×**; fully diluted value / fees ≈ 960×.
- Today the price is almost entirely **optionality on ATLAS, Zero and the fee switch**, not current cash
  flow.

## Independent view (formed before reading price targets)
- **The rally is a narrative rerating, not a usage rerating.** Fees are down 59% y/y, the fee switch is off,
  buybacks are tiny, and a migration plus a lawsuit hang over the brand. Commentary attributes the latest
  leg up to a technical breakout and speculative flows.
- **The near term is supply-heavy.** About $50m of new ZRO arrives every month until May 2027 into a
  market that has just doubled the price. The 20 Oct unlock is a live test of how much of the rally is real
  demand.
- **The medium-term asymmetry is genuine but conditional.** If Zero and ATLAS reach real institutional
  volume **after the unlocks end**, token economics flip from dilution to burn on a fixed supply. Of the
  names studied so far, ZRO has the clearest path for that flip. Chainlink's supply tail is longer, but its
  usage is real today.
- **Consensus split:**
  - Bulls price the ATLAS/Zero endgame as if it were already happening.
  - Bears price the hack, migrations and lawsuit as permanent.
  - The data supports neither yet.
- **The variable that decides it:** measured ATLAS/Zero fee burn per month against the remaining unlock
  supply, plus whether the December fee-switch vote reaches quorum.

## Measurable tests (set now)
**Would strengthen the case:**
- The 20 Oct unlock is absorbed. Watch exchange inflows from the recipient wallets and whether the price
  holds above the pre-unlock level a week later; this is a market-reaction signal, not proof.
- ATLAS goes live with named venues and a public burn counter showing at least $5m a month of burns within
  three months of launch.
- Zero mainnet launches with named institutional participants.
- The December fee-switch vote **reaches quorum and passes.**
- Messaging fees get back above the year-ago level (90-day fees above $1.5m).
- No further major migrations.

**Would weaken the case:**
- ATLAS or Zero slip into 2027 without volume.
- The fee-switch vote fails quorum again (it would be the fifth attempt).
- Further protocol migrations to CCIP or others.
- Adverse developments in the KelpDAO lawsuit.
- The price falls back toward the pre-rally level after unlocks.

**Cross-check with Jev (13 Oct):** P(fees +25% by Mar-2027) = 0.25 and P(holders capture fees) = 0.46.
That view is moderate: more constructive on usage than Chainlink (0.16) but well short of the narrative.

## Sources
- DefiLlama, LayerZero fees and holder revenue: https://defillama.com/protocol/layerzero
- CoinDesk, LayerZero says it "made a mistake" (2026-05-09): https://www.coindesk.com/tech/2026/05/09/layerzero-says-it-made-a-mistake-in-usd292-million-kelp-exploit
- The Block, Kelp moves to Chainlink (2026-05-05): https://www.theblock.co/news/ecosystems/2026-05-05-kelp-dao-ditches-layerzero-chainlink-cross-chain-infrastructure-292-million-exploit-400131
- MEXC News, 47% of OApps on a single DVN: https://www.mexc.com/news/1051837
- CryptoTimes, ZRO +16% on 12 Oct: https://www.cryptotimes.io/2026/10/12/layerzero-zro-price-jumps-16-as-traders-assess-2-50-resistance/
- ETHNews, price vs unlock: https://ethnews.com/layerzero-price-retests-its-february-ceiling-before-unlock
- The Block — ATLAS / Zero (2026-08-25): https://www.theblock.co/news/ecosystems/2026-08-25-zro-token-layerzero-atlas-exchange-infrastructure-zero-blockchain-412736
- The Block — KelpDAO lawsuit (2026-09-25): https://theblock.co/news/regulation/2026-09-25-kelpdao-sues-layerzero-claims-it-endorsed-setup-used-in-292-million-rseth-exploit-416361
- The Block — LayerZero on Lazarus / single-point setup: https://www.theblock.co/post/398028/layerzero-kelp-dao-lazarus
- CoinDesk — Kelp blames default settings (2026-04-20): https://www.coindesk.com/tech/2026/04/20/kelp-dao-claims-layerzero-s-default-settings-are-what-actually-caused-the-usd290-million-disaster
- Blockaid — single DVN compromise: https://blockaid.io/blog/how-a-single-layerzero-dvn-compromise-drained-292m-from-kelpdao
- Altcoin Buzz — unlocks & fee-switch vote (2026-10-07): https://www.altcoinbuzz.io/layerzero-zro-unlocks-december-fee-switch-vote
- CoinStats — STG migration dates: https://coinstats.app/ai/a/latest-news-for-layerzero
- CoinGecko — token data: https://www.coingecko.com/en/coins/layerzero
- Tokenomist — unlocks/buybacks: https://tokenomist.ai/layerzero
