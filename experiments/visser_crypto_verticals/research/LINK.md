# Chainlink (LINK): study first, then an independent view

Compiled 2026-10-13 from public sources (listed at the end). Educational research, not advice. This note
sits outside the pre-registered test and changes nothing in `../PREREGISTRATION.md`.

## Where it sits
- **Visser 46-name index:** *Oracle, Data & Interop Middleware*, alongside PYTH, ZRO and GRT.
- **Danny's Crypto Portfolio v1:** held (one of 16 at equal weight).
- **Jev usage run (13 Oct):**
  - P(fees +25% by Mar-2027) = 0.16, in the bottom quarter of the 46.
  - P(holders capture fees) = 0.49, mid-pack.

## 1. Understand the business (what Chainlink sells)
- **Oracles:** price feeds and data streams that DeFi protocols need to work. Chainlink is the incumbent
  standard for lending protocols such as Aave.
- **CCIP (cross-chain interoperability):** moves tokens and messages between chains. **CCIP 2.0 launched on
  28 Sep 2026 at Sibos.**
  - Banks and issuers can add their own verifiers on top of a default network of 16 node operators.
  - The separate Risk Management Network no longer acts as an independent safeguard.
  - Launch partners and supporters include AWS, ANZ, Deutsche Börse's Crypto Finance, Fidelity
    International, Infosys and SBI. No institution has yet been named as *using* the optional verifiers.
- **Institutional rails:**
  - DTCC has processed its **first production trades of tokenized US securities** with Chainlink: collateral
    pledges, securities lending, and Treasury/repo and equity delivery-versus-payment.
  - DTCC operates under a three-year no-action letter and expects collateral-management workflows on its
    AppChain in Q4 2026.
  - Swift integration lets banks reach chains through existing ISO 20022 messaging.
- **Competitive tailwind:** after the April 2026 KelpDAO hack (about $292m, a single-verifier LayerZero
  bridge), Kelp said it would move rsETH to Chainlink. Reportedly almost half of active LayerZero apps used
  one verifier. *Caution:* LayerZero now offers multi-verifier setups too.

## 2. Measure what actually happens on-chain (DefiLlama, to 12–13 Oct 2026)
| Window | Fees | Revenue (LINK to the Reserve) |
|---|---|---|
| Last 90 days | $15.1m | $14.5m |
| Prior 90 days | $14.6m (+3.6%) | $13.9m (+4.6%) |
| Same 90 days a year ago | $11.6m (+30% y/y) | $10.3m (+40% y/y) |
| Last 365 days | $62.7m | $58.8m |

The jump against the year before ($13.7m) mostly reflects the Reserve and Payment Abstraction going live in
Aug 2025, which created a measurable revenue stream. It is not a 4.6× rise in usage. **Usage is growing
roughly 30% a year but was flat quarter on quarter**, which is why Jev rated a 25% jump in six months as
unlikely.

## 3. Follow the token: supply versus demand
| Flow | Size | Basis |
|---|---|---|
| **Reserve buybacks** (from fees via Payment Abstraction) | ~374k LINK in Sep 2026 (~$4.3m); Reserve ~6.05m LINK (~$78m at $12.95) | Press reports of the on-chain reserve; no withdrawals expected "for years" |
| **Quarterly unlocks** from non-circulating addresses | ~19m LINK (Apr) and ~21m LINK (Jun), each ~$165m; mostly sent to Binance, part to the staking-rewards multisig | On-chain trackers (Onchain Lens, Yu Jin) |
| Supply still to unlock | ~233m LINK (circulating 767m of 1bn, 77%) | CoinGecko |

**The arithmetic consensus skips:** at the recent pace, unlocks of about 80m LINK a year are roughly **13×
the Reserve's buyback flow** (about 4.5m LINK a year, annualising September). Some unlocked LINK funds
staking rewards and operations rather than being sold, so this is gross supply, not net selling. Even so,
fee-funded buybacks are small next to new supply.

## 4. Valuation, roughly
- Market cap about $9.9bn; fully diluted about $13.0bn; price $12.95, down 35% over a year and about 75%
  below the May-2021 high of $52.70.
- Market cap / on-chain revenue ≈ **170×**. Off-chain enterprise fees that are converted into LINK through
  the Reserve are partly captured in that revenue figure; the rest is not disclosed.

## 5. Independent view (formed before reading price targets)
- **The business is real and gaining institutional ground.** The DTCC production trades, Swift rails and
  CCIP 2.0 are not just slideware. The security story after the KelpDAO hack works in its favour.
- **The token captures that value slowly.** Holders benefit mainly through Reserve buybacks, which are
  about $50m a year at the current pace against roughly $650m of LINK unlocked each year. Until fee flow
  grows several-fold, or the unlock schedule ends (~233m LINK left, about 3 years at the current pace),
  **adoption headlines can coexist with a weak token.** The price −35% over a year while adoption
  headlines grew is consistent with that.
- **Consensus split:**
  - Bulls read "11,000 Swift banks" or "1.7bn Infosys accounts" as demand. Those are measures of reach,
    not usage.
  - Bears read the chart and miss that institutional production usage has started.
- **The variable that decides it:** how fast the Reserve's inflow grows relative to unlock supply. Price
  and headlines will not.

## 6. Measurable tests (set now)
**Would strengthen the case:**
- Reserve inflow of at least 1m LINK a month for two consecutive months, about 3× September's pace.
- DefiLlama 90-day fees above $18.9m (+25%) by 31 Mar 2027. This is Jev's question, so it is a direct check
  on its 0.16.
- Named banks or DTCC workflows live on CCIP with disclosed volume.
- Smaller unlocks, or a larger share of each unlock going to staking rather than exchanges.

**Would weaken the case:**
- Flat fees for a further two quarters.
- Reserve growth stalls.
- Unlocks of about 20m LINK a quarter keep flowing to exchanges.
- Interoperability share lost to LayerZero or others despite CCIP 2.0.

**Next things to check:**
- the Reserve wallet monthly (on-chain);
- the next quarterly unlock (the pattern points to roughly Sep–Oct; not yet confirmed for Q3/Q4);
- DTCC Q4 AppChain go-live;
- any CCIP 2.0 verifier adopters named.

## Sources
- CoinDesk, CCIP 2.0 (2026-09-28): https://www.coindesk.com/business/2026/09/28/chainlink-updates-its-crypto-bridge-tech-months-after-a-usd292-million-hack-shook-the-industry
- PR Newswire, CCIP 2.0 launch: https://www.prnewswire.com/news-releases/chainlink-launches-ccip-2-0-to-maximize-the-utility-and-reach-of-institutional-digital-assets-across-blockchains-302891388.html
- Chainlink blog, banking and capital markets: https://blog.chain.link/chainlink-banking-capital-markets-announcements/
- Startup Fortune, CCIP 2.0 / Swift / DTCC: https://startupfortune.com/chainlink-launches-ccip-20-as-swift-and-dtcc-wire-it-into-banking/
- Cryptoticker, Reserve above 6m LINK: https://cryptoticker.io/en/chainlink-reserve-six-million-link/
- Bloomingbit, $1.13m buyback: https://en.bloomingbit.io/feed/news/117885
- ChainCatcher, quarterly unlocks: https://www.chaincatcher.com/en/article/2272499
- MEXC news, June 2026 unlock: https://www.mexc.com/news/1004402
- DefiLlama, Chainlink fees and revenue: https://defillama.com/protocol/chainlink
- CoinGecko, LINK supply and market data: https://www.coingecko.com/en/coins/chainlink
