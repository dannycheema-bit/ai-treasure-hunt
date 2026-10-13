"""Jev usage-inflection assessments for the 46 Visser crypto names (exploratory; does NOT change the
pre-registered basket-vs-Bitcoin test). Same question schema for every name; public evidence only
(DefiLlama fees/revenue/TVL, CoinGecko supply, Yahoo revenue for the 4 stocks); no price data.

Per name: one central request (U usage inflection, VA value accrual for tokens, T timing, EQ evidence
quality) + three scenario requests (U under adverse/base/favourable premises). Freezes the usage baseline
(baseline_2026-10-13.json) so the forecasts can be checked against DefiLlama after 31 Mar 2027.
Usage: python3 jev_usage_run.py
"""
import csv, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "ai_nexus_lagging_inflection"))
from jev_client import system_one  # noqa: E402  (official TypeSafe HTTP API, key from .env)

MODEL = "jev-latest"
AS_OF = "2026-10-13"
LOG = HERE / "jev_usage_log.jsonl"

U_TOKEN = {"type": "noul", "instructions": (
    "Over the 90 days ending 31 March 2027, will the fees users pay to this protocol or network be at least 25% "
    "higher than in the 90 days ending in `usage.fees.window_end` (`usage.fees.last90_usd`), driven by organic "
    "usage rather than token incentives, emissions, airdrop farming or a one-off event?"),
    "criteria": {"true": "Fees in the 90 days to 31 Mar 2027 are at least 25% above the baseline, organically.",
                 "false": "Growth is below 25%, fees fall, or growth is driven by incentives or one-offs."}}
U_STOCK = {"type": "noul", "instructions": (
    "Will the company's quarterly revenue for the quarter ending 31 March 2027 be at least 25% higher than its "
    "most recent reported quarter in `usage.quarterly_revenue`, driven by crypto/digital-asset activity (trading, "
    "stablecoin balances, tokenization) rather than acquisitions or one-off items?"),
    "criteria": {"true": "Revenue for the March 2027 quarter is at least 25% above the latest reported quarter.",
                 "false": "Growth is below 25%, revenue falls, or growth comes from acquisitions or one-offs."}}
VA_Q = {"type": "noul", "instructions": (
    "Over the same period, will a meaningful share of this protocol's fees reach holders of its token through "
    "protocol revenue, buybacks or burns, or fee-funded staking rewards (rather than going only to "
    "liquidity providers, validators' costs or the treasury without holder benefit)?"),
    "criteria": {"true": "A meaningful, ongoing share of fees accrues to token holders.",
                 "false": "Little or none of the fee flow accrues to token holders."}}
T_Q = {"type": "noul", "instructions": (
    "Assume usage does grow at least 25% by the 90 days ending 31 March 2027 as described. Will that growth "
    "already be clearly visible in the 90 days ending 31 December 2026?"),
    "criteria": {"true": "Early: clearly visible by end-December 2026.",
                 "false": "Later: only visible in January-March 2027."}}
EQ_Q = {"type": "score", "instructions": "How complete and reliable is the usage evidence in this state?",
        "criteria": ["Missing or nearly empty usage data",
                     "Partial data: some usage figures but short history or gaps",
                     "Good data: fee/revenue history over several windows"]}
SCENARIOS = {
    "adverse": "Assume crypto adoption by institutions and AI agents stalls through March 2027 and on-chain activity "
               "stays flat or declines.",
    "base": "Assume on-chain activity grows through March 2027 but concentrates in a few leading chains and "
            "applications, while many smaller protocols lose share.",
    "favourable": "Assume AI agents, stablecoins and tokenization drive broad growth in on-chain activity across "
                  "many protocols through March 2027.",
}


def pct(a, b):
    return None if not b else round((a / b - 1) * 100, 1)


def build_state(sym, n):
    st = {"as_of": AS_OF, "name": f"{n['name']} ({sym})", "category": n["vertical"], "type": n["type"]}
    if n["type"] == "stock":
        qr = n.get("quarterly_revenue") or {}
        st["usage"] = {"quarterly_revenue": {k: round(v) for k, v in qr.items()},
                       "revenue_consensus": {k: round(v) for k, v in (n.get("revenue_consensus") or {}).items()}}
        return st
    f, r = n.get("fees"), n.get("revenue")
    usage = {"source": "DefiLlama" if f else "no DefiLlama usage data available"}
    if f:
        usage["fees"] = {"window_end": f.get("last_date") or AS_OF,
                         "last90_usd": round(f["last90"]), "prior90_usd": round(f["prev90"]),
                         "same90_year_ago_usd": round(f["year_ago90"]),
                         "last30_usd": round(f["last30"]), "prior30_usd": round(f["prev30"]),
                         "change_90d_vs_prior90_pct": pct(f["last90"], f["prev90"]),
                         "change_30d_vs_prior30_pct": pct(f["last30"], f["prev30"]),
                         "days_of_history": f["days"]}
    if r:
        usage["protocol_revenue"] = {"last90_usd": round(r["last90"]), "prior90_usd": round(r["prev90"]),
                                     "change_90d_vs_prior90_pct": pct(r["last90"], r["prev90"])}
    if n.get("tvl_usd"):
        usage["tvl_usd"] = round(n["tvl_usd"])
    s = n.get("supply") or {}
    if s.get("market_cap") and s.get("fully_diluted_valuation"):
        usage["token_supply"] = {"circulating_share_of_fdv_pct": round(100 * s["market_cap"] / s["fully_diluted_valuation"], 1)}
    st["usage"] = usage
    return st


def ask(state, qs, cache):
    key = hashlib.sha256(json.dumps([state, qs, MODEL], sort_keys=True).encode()).hexdigest()
    if key not in cache:
        resp = system_one(state, qs, model=MODEL)
        with open(LOG, "a") as fh:
            fh.write(json.dumps({"key": key, "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                 "requested_model": MODEL, "state": state, "questions": qs, "response": resp}) + "\n")
        cache[key] = resp
    return cache[key]


def main():
    raw = json.loads((HERE / "usage_raw.json").read_text())
    base_path = HERE / "baseline_2026-10-13.json"
    if not base_path.exists():   # frozen once, for checking forecasts after 31 Mar 2027
        base = {s: {"fees_last90": (n.get("fees") or {}).get("last90"),
                    "latest_quarter_revenue": (lambda q: q[max(q)] if q else None)(n.get("quarterly_revenue") or {}),
                    "slug": n.get("slug")} for s, n in raw["names"].items()}
        base_path.write_text(json.dumps({"frozen_utc": raw["fetched_utc"], "data": base}, indent=1))
    cache = {}
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            r = json.loads(line)
            cache[r["key"]] = r["response"]
    rows = []
    stack = list(csv.DictReader(open(HERE.parent / "STACK.csv")))
    for i, row in enumerate(stack, 1):
        sym, n = row["symbol"], raw["names"][row["symbol"]]
        st = build_state(sym, n)
        token = n["type"] == "token"
        qs = {"U": U_TOKEN if token else U_STOCK, "T": T_Q, "EQ": EQ_Q, **({"VA": VA_Q} if token else {})}
        a = ask(st, qs, cache)["answers"]
        out = {"symbol": sym, "name": n["name"], "vertical": n["vertical"], "type": n["type"],
               "P_U": a["U"]["noul"], "P_early_given_U": a["T"]["noul"], "P_early": round(a["U"]["noul"] * a["T"]["noul"], 4),
               "P_value_accrual": a["VA"]["noul"] if token else None,
               "evidence_quality_0_2": a["EQ"]["score"],
               "fees_change_90d_pct": (st["usage"].get("fees") or {}).get("change_90d_vs_prior90_pct"),
               "data": st["usage"].get("source", "Yahoo revenue")}
        for name, prem in SCENARIOS.items():
            sa = ask(dict(st, scenario_premise=prem), {"U": qs["U"]}, cache)["answers"]
            out[f"P_U_{name}"] = sa["U"]["noul"]
        rows.append(out)
        print(f"{i:2} {sym:8} P(U)={out['P_U']:.2f} VA={'-' if out['P_value_accrual'] is None else round(out['P_value_accrual'], 2)}"
              f" early|U={out['P_early_given_U']:.2f} adv/base/fav={out['P_U_adverse']:.2f}/{out['P_U_base']:.2f}/{out['P_U_favourable']:.2f}"
              f" EQ={out['evidence_quality_0_2']:.2f} fees90d={out['fees_change_90d_pct']}")
    with open(HERE / "jev_usage_scores.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    use = [json.loads(l)["response"].get("usage", {}) for l in LOG.read_text().splitlines()]
    print("requests:", len(use), "| input tokens:", sum(u.get("input_tokens", 0) for u in use))


if __name__ == "__main__":
    main()
