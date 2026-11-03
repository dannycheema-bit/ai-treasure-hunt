# Helium (HNT) — study-first note and independent view (2026-11-03)

Compiled from public sources and on-chain supply (listed at the end). Educational notes only; not investment
advice. This note is OUTSIDE the pre-registered test: it does not change the frozen list, rules or scoring in
`../PREREGISTRATION.md`. Figures marked **estimate** are my own arithmetic, not published numbers.

## Where it sits in the experiments
- **Visser 46-name index:** vertical *DePIN, Storage & Physical Networks*. He mentions it only in passing in the
  26 Oct video (10:05).
- **Danny's Crypto Portfolios v1-v3:** not held.
- **Since the 30 Sep start price:** HNT $0.466 to $0.341 (**-27%**); BTC -7%.
- **Frozen Jev usage baseline (13 Oct):** P(usage inflects) 0.23, P(value reaches holders) 0.32. No fee trend was
  available because the measured fee series was already zero.

## What it is (plain English)
People and venues run Wi-Fi hotspots. Mobile carriers pay to send phone traffic over them instead of their own
towers ("carrier offload"). Payment works through Data Credits (DC), which can only be made by burning HNT, and hotspot
owners are paid in HNT. It is the best-known wireless "DePIN" network, and it runs on Solana.

## Token facts (CoinGecko and Solana RPC, 2026-11-03)
| | |
|---|---|
| Price | $0.341 (-85% in a year; -99% from the $54.88 high of Nov 2021) |
| On-chain supply | 199.88m HNT |
| Market cap | ~$68m |
| **Effective max supply** | **~347m** (HIP 149). CoinGecko still shows 223m, and its FDV equals market cap |
| Fully diluted at ~347m (**estimate**) | ~$118m |
| 30-day average volume | ~$3.4m a day |

## 2026 changed what the token is
| Date | Event |
|---|---|
| Jan 2026 | Open-market buybacks funded by Helium Mobile revenue paused and redirected to growth. DefiLlama's measured holder revenue has been $0 since (it was ~$0.95m a month in Nov and Dec 2025). |
| Jun 2026 | Helium Mobile (the consumer business) sold to Noble Mobile, Andrew Yang's company; terms undisclosed. Nova Labs keeps the network and token operations. |
| Jun 2026 | Amir Haleem leaves the CEO role, reportedly becoming chairman, with Mario Di Dio taking over. Sources conflict on title and date. |
| Before the HIP 149 vote | Nova cuts the carrier payer rate from $0.50/GB to about $0.10/GB under HIP 143. |
| 25 Jun-3 Jul 2026 | **HIP 149 passes** (one aggregator reports 93.7% yes). CoinMarketCap's "15 Oct approved" date looks wrong: GitHub marks it approved on 6 Jul. |
| 6 Jul 2026 | Proof-of-Coverage rewards end. On the 24 Jun epoch, 114,267 of 163,607 rewarded IoT hotspots earned only PoC rewards. |
| Aug 2026 | Council recommends proceeding with the mint (unanimous), and focusing Nova on Mobile and Wi-Fi offload. IoT is to move to another operator or be shut down; Nova aims to finish that by end-2026. |
| Aug 2026 | **New mint starts** (date inferred from the supply series; supply turns up between 4 and 11 Aug). |
| 29-31 Aug 2026 | Short squeeze: $0.18 to ~$0.77 at the close. Funding hit -0.63%, volume about $89m against a normal $2-4m. The headline was Celina, Texas adding Helium to public Wi-Fi. |
| 29 Sep / 9 Oct 2026 | Wi-Fi offload wins: a hospital system (145+ TB in week one, 10,654 access points) and the first Wakefern supermarkets. |

## HIP 149 supply: the fact consensus skips
- **About 141m new HNT over 36 months**, equal to 77% of the supply at the time. It goes to a vault run by Nova Labs
  to fund operations, not to hotspot owners or holders.
- **Schedule:** ~196,000 HNT a day for ~360 days (about 70.6m), then a linear taper to zero over ~720 days.
- **Scale:** 9.5 times the ~20,548 HNT a day of ordinary emissions.
- **Sales:** Nova should prefer OTC sales with lockups "where practicable"; sales are reported to the Council, not publicly.
- **Limits:** a 7-seat council can only recommend a curtailment vote. It cannot block spending or set the payer rate.
- **Alignment:** Nova must present recommendations on aligning with token holders within six months of mint start
  (about **Feb 2027**). Holders have no claim on Nova's revenue today.

### What the supply series shows
Implied from CoinGecko market cap / price, checked against on-chain supply today. **All burn figures are estimates.**

| Period | Net supply change, k HNT/day | Implied burn, k HNT/day | Implied burn, $/day |
|---|---|---|---|
| May 2026 | -35.5 | ~56 | ~$48k |
| Jun 2026 | -18.3 | ~39 | ~$14k |
| Jul 2026 | -17.5 | ~38 | ~$8k |
| Sep 2026 | +210.5 | ~6 | ~$3k |
| Oct 2026 | +211.5 | ~5 | ~$2k |

- **Two independent checks agree on May:** HIP 149's ~97k GB/day (Apr) x $0.50 = ~$48k, matching Blockworks' reported
  ~$50k/day. July's ~$8k is close to 97k GB x $0.10 = ~$10k.
- **Supply went from shrinking to growing about 39% a year** (~215k/day; 199.9m today, up 10% since 4 Aug).
- **The burn since September is too small to measure** this way: net growth almost equals gross issuance. This does
  not show usage fell. HIP 149 allows fees to be routed through burn only "where commercially practicable", with possible
  periodic reconciliation, so burns may be lumpy or delayed. DefiLlama also says past burn HNT came from treasury wallets
  rather than open-market buying (single source).

## Usage: the real part
- Rewardable data grew about 4x, from ~24k GB/day (Jun 2025) to ~97k GB/day (Apr 2026), per HIP 149.
- The hospital's 145 TB in a week is about 21k GB/day, or **~21% of April's network total from one customer.** It is
  Helium's own figure, for week one, and it may not be counted the same way as rewardable data.
- Wi-Fi offload is a real product with real buyers. Hospitals replacing antenna systems and supermarket chains are not
  crypto speculators.

**The catch:** $0.10/GB is one-fifth of the old price. Usage has to grow fivefold just for the dollar burn to
stand still.

## The sum that decides it (**estimates**)
| | |
|---|---|
| New HNT per day | ~216,500 (mint + emissions) |
| Worth at $0.341 | ~$74k a day |
| Burn needed to offset it, at $0.10/GB | ~**738k GB/day**, about **7.6x** April's level |
| Same in hospital-sized systems | ~31 more |
| Mint over the flat year, at today's price | ~$24m, about 35% of today's market cap |
| Market cap / inferred fee run-rate (~$3m a year from July's burn) | ~23x; ~40x fully diluted |

The break-even moves with the price: a lower HNT needs less usage, because burn is set in dollars and mint in HNT.
Price falling is what makes equilibrium easier, which is not a comfort to holders.

## Independent view (formed before reading price targets)
- **The network and the token have separated.** The usage story is improving while the token's terms have got much
  worse: buybacks gone, the consumer business sold, 77% more supply authorised, the burn price cut 80%.
- **The price is not as washed out as the chart suggests.** It is down 85% in a year, but market cap is about double the
  ~$33m of early August, despite 10% more supply and no change in measured holder revenue. The squeeze has only partly
  reversed.
- **The mint is a financing, in effect.** Holders are funding Nova's growth through dilution, about $48m at today's price
  across all 141m tokens. That can be a sensible decision for the network (93.7% reportedly voted for it). But the
  holders' return depends on terms not yet set.
- **Consensus split:**
  - Bulls cite daily users, carrier deals and "the DePIN with real customers".
  - Bears cite the 96-99% decline and the end of buybacks.
  - Neither camp usually runs the mint-versus-burn sum, and the common data sites still show the old 223m cap.
- **The variable that decides it:** paid GB per day against the ~738k break-even, and whether that revenue reaches HNT
  through burn at all. Nova sets the price, administers the mint and decides how fees are routed, so holders depend
  on one company's choices.
- **What I would say plainly:** this is an interesting network and, for now, a structurally diluted token. There's
  no evidence yet that cheapness compensates for that. The clean re-look date is about Aug 2027, when the flat mint ends,
  or sooner if the Feb 2027 alignment proposal gives holders a real claim.

## Measurable tests (set now)
**Would strengthen the case:**
- Paid data above **300k GB/day** by Aug 2027, on a public dashboard or from Nova.
- Monthly burn clearly visible in supply: net issuance below ~170k HNT/day during the flat mint.
- A Feb 2027 alignment proposal with a binding route for revenue to holders (burn or buyback), not just a statement.
- A named national carrier expanding, with volumes disclosed.
- Vault sales disclosed publicly, and mostly OTC with lockups.

**Would weaken the case:**
- Net issuance stays at ~215k/day into 2027, meaning fees are not reaching burn.
- The payer rate is cut below $0.10/GB.
- Noble Mobile moves traffic off Helium, or a carrier offload contract ends.
- The Council's curtailment route goes unused despite weak disclosure, or community seats fall vacant.
- The IoT transition ends in shutdown with material hotspot exits.

## Dates
- **Now to about Aug 2027:** flat mint (~196k HNT/day), then the taper to about Aug 2029.
- **End-2026:** IoT transition target (inside the test window).
- **About Feb 2027:** Nova's first holder-alignment recommendation.
- **Time-limited:** HIP 150's 80% deployer target (from 31 Aug 2026), reverting to 50% later.

## Unverified or open
- Vault address and sales so far: not checked on-chain.
- Actual paid GB/day since April: no public figure found.
- Hotspot and subscriber counts: only from a self-published post with affiliate links, so not used.
- AT&T as an offload partner: named only in that same post in this pass; not confirmed here.
- Price of the Helium Mobile sale, and who received the proceeds.

## Sources
- HIP 149 text: https://raw.githubusercontent.com/helium/HIP/main/0149-helium-utility-and-emissions-realignment.md
- HIP 149 discussion and status: https://github.com/helium/HIP/issues/1201
- HeliumGeek, HIP 149 details: https://heliumgeek.com/faq/what-is-hip149.html
- DefiLlama, fees and methodology: https://api.llama.fi/summary/fees/helium-network?dataType=dailyFees
- crypto.news, Noble acquisition and burn figure (2026-06-03): https://crypto.news/helium-mobile-acquisition-leaves-hnt-network-intact-as-token-tests-key-support/
- CoinMarketCap updates (hospital, Wakefern): https://coinmarketcap.com/cmc-ai/helium/latest-updates/
- Altfins, vote tally: https://altfins.com/crypto-screener/hnt-helium
- BeInCrypto, squeeze: https://beincrypto.com/helium-hnt-weekend-rally-short-squeeze/
- Blockonomi, Celina, Texas: https://blockonomi.com/helium-hnt-skyrockets-88-following-texas-citys-network-integration/
- Bitcoin Sistemi, buyback pause: https://en.bitcoinsistemi.com/surprise-altcoin-halts-token-buybacks-as-price-shows-no-improvement/amp
- crypto.news Helium tag, CEO change: https://crypto.news/tag/helium/
- CoinGecko, price, market cap, volume: https://www.coingecko.com/en/coins/helium
- Solana RPC `getTokenSupply`, HNT mint `hntyVP6YFm1Hg25TN9WGLqM12b8TQmcknKrdu1oxWux`
