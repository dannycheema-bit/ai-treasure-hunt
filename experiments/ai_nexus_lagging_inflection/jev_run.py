"""Run the actual Jev assessments (research prompt section 5) for every company, same schema for all.

Per company, 4 requests to TypeSafe Jev (model jev-latest):
  central   - E (earnings step-up), G (expectations asymmetry, if a frozen comparator exists),
              timing (early | E), commercial progression (Score), evidence quality (Score)
  adverse / base / favourable - E and G under an explicit scenario premise
State = public evidence only (agent commentary research + Yahoo consensus/results + frozen revenue
consensus). No subscriber text and no technical/price data (avoids circular "chart proves earnings").
Every exchange is cached by hash(state+questions+model) and logged to jev_log.jsonl (git-ignored).
Writes jev_scores.csv. Usage: python jev_run.py [--limit N]
"""
import csv, hashlib, json, math, sys, time
from datetime import datetime, timezone
from pathlib import Path

from jev_client import system_one

HERE = Path(__file__).parent
MODEL = "jev-latest"
AS_OF = "2026-10-12"
LOG = HERE / "jev_log.jsonl"

E_Q = {"type": "noul", "instructions": (
    f"Within the company's next four reporting periods after {AS_OF} (for half-year reporters, the next two), "
    "will recurring consolidated operating earnings improve materially relative to continuing the currently "
    "deployed business on its ordinary trend, sustained across two comparable reporting periods, because of "
    "the AI-related product line described in `exposed_line`? Material means at least 15% year-over-year growth "
    "in recurring operating income, or for a loss-making company a clear move to sustained recurring operating "
    "profit. Acquisitions, one-off items and ordinary cyclical recovery alone do not count."),
    "criteria": {"true": "The defined step-up occurs within the horizon, driven by the AI-related line.",
                 "false": "It does not occur within the horizon, or only through acquisitions, one-offs or cycle."}}
G_Q = {"type": "noul", "instructions": (
    "Will the company's reported revenue exceed the consensus frozen on 2026-10-12 "
    "(`frozen_revenue_consensus`) by at least 5% in two consecutive reporting periods within the next four "
    "periods, principally because of the AI-related product line in `exposed_line`?"),
    "criteria": {"true": "Two consecutive periods at least 5% above the frozen consensus, driven by that line.",
                 "false": "This does not happen, or beats are small, isolated or driven by other businesses."}}
T_Q = {"type": "noul", "instructions": (
    "Assume the material AI-driven operating-earnings step-up described for this company does occur within its "
    "next four reporting periods. Will it already be visible in the next two reporting periods (early) rather "
    "than only in periods three and four (later)?"),
    "criteria": {"true": "Early: visible within the next two reporting periods.",
                 "false": "Later: only visible in periods three and four."}}
CP_Q = {"type": "score", "instructions": (
    "How far has the company's AI-related product line in `exposed_line` progressed commercially, based on "
    "`latest_evidence` and `prior_checkpoints`?"),
    "criteria": ["No clear AI-related line, or only broad talk of an opportunity",
                 "Named products, design wins or qualifications, but little revenue",
                 "Orders, backlog or early production with some recognized revenue",
                 "Material recognized revenue that is growing, with recurring profit contribution"]}
EQ_Q = {"type": "score", "instructions": (
    "How strong and specific is the evidence in this state for judging the company's AI-related earnings?"),
    "criteria": ["Sparse or vague: few dated facts, mostly qualitative",
                 "Moderate: some dated figures, but gaps or secondary sources",
                 "Strong: multiple dated, quantified figures from company reports"]}

SCENARIOS = {
    "adverse": ("Assume that through 2027 efficiency gains outrun adoption: the cost of AI work falls sharply but "
                "people and businesses delegate to AI agents slowly, so growth in AI infrastructure spending slows."),
    "base": ("Assume that in 2027 AI demand grows strongly but returns diverge: owners and suppliers of the "
             "newest-generation capacity do well, while older capacity and some suppliers face pricing pressure."),
    "favourable": ("Assume that in 2027 AI demand outruns efficiency gains and the AI infrastructure earnings "
                   "cycle broadens across many suppliers, not just the leaders."),
}


def num(x):
    try:
        x = float(x)
        return None if math.isnan(x) else x
    except (TypeError, ValueError):
        return None


def build_state(fp, cm, frozen, cur):
    fc = frozen.get(fp["ticker"]) or {}
    def rev(p):
        v = num((fc.get(p) or {}).get("avg"))
        return None if v is None else f"{cur} {v:,.0f}"
    state = {
        "as_of": AS_OF,
        "company": f"{fp['company']} ({fp['ticker']})",
        "exposed_line": cm["exposed_line"],
        "latest_report_date": cm["latest_report_date"],
        "latest_evidence": cm["evidence"],
        "counterevidence": cm["counterevidence"],
        "consensus": {
            "next_fiscal_year_eps_growth_pct": num(fp.get("next_fy_eps_growth_pct")),
            "next_fiscal_year_eps_revision_90d_pct": num(fp.get("eps_next_fy_rev_90d_pct")),
            "upward_revisions_30d": num(fp.get("up_30d")),
            "downward_revisions_30d": num(fp.get("down_30d")),
            "analysts": num(fp.get("analysts")),
        },
        "recent_results": {
            "eps_surprises_last_4_reports": fp.get("surprises_last4"),
            "latest_operating_income_yoy_pct": num(fp.get("opinc_yoy_latest_pct")),
        },
        "next_report_date": fp.get("next_report"),
        "frozen_revenue_consensus": {"next_reporting_period": rev("0q"), "following_period": rev("+1q")},
    }
    return state


def ask(state, questions, cache):
    key = hashlib.sha256(json.dumps([state, questions, MODEL], sort_keys=True).encode()).hexdigest()
    if key in cache:
        return cache[key]
    t0 = time.time()
    resp = system_one(state, questions, model=MODEL)
    rec = {"key": key, "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "requested_model": MODEL, "returned_model": resp.get("model"), "latency_s": round(time.time() - t0, 2),
           "state": state, "questions": questions, "response": resp}
    with open(LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")
    cache[key] = resp
    return resp


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    fps = json.loads((HERE / "first_pass.json").read_text())
    cms = {r["ticker"]: r for r in csv.DictReader(open(HERE / "commentary_scores.csv"))}
    frozen = json.loads((HERE / "frozen_consensus_2026-10-12.json").read_text())["data"]
    cache = {}
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            r = json.loads(line)
            cache[r["key"]] = r["response"]
    rows, usage = [], {"input_tokens": 0, "output_tokens": 0, "requests": 0}
    for i, fp in enumerate(sorted(fps, key=lambda r: r["ticker"])[:limit], 1):
        raw = json.loads((HERE / "raw" / f"{fp['ticker']}.json").read_text())
        cur = (raw.get("info") or {}).get("financialCurrency") or fp.get("currency") or ""
        state = build_state(fp, cms[fp["ticker"]], frozen, cur)
        has_g = state["frozen_revenue_consensus"]["next_reporting_period"] is not None
        qs = {"E": E_Q, "T": T_Q, "CP": CP_Q, "EQ": EQ_Q, **({"G": G_Q} if has_g else {})}
        central = ask(state, qs, cache)
        a = central["answers"]
        row = {"ticker": fp["ticker"], "returned_model": central.get("model"),
               "P_E": a["E"]["noul"], "P_G": a["G"]["noul"] if has_g else None,
               "P_early_given_E": a["T"]["noul"],
               "P_early": round(a["E"]["noul"] * a["T"]["noul"], 4),          # P(E) x P(early | E)
               "commercial_progression_0_3": a["CP"]["score"], "commercial_progression_conf": a["CP"].get("confidence"),
               "evidence_quality_0_2": a["EQ"]["score"], "evidence_quality_conf": a["EQ"].get("confidence"),
               "G_status": "assessed" if has_g else "UNAVAILABLE (no frozen comparator)"}
        for name, premise in SCENARIOS.items():
            s = dict(state, scenario_premise=premise)
            sq = {"E": E_Q, **({"G": G_Q} if has_g else {})}
            sa = ask(s, sq, cache)["answers"]
            row[f"P_E_{name}"] = sa["E"]["noul"]
            row[f"P_G_{name}"] = sa["G"]["noul"] if has_g else None
        rows.append(row)
        print(f"{i:3} {fp['ticker']:11} P(E)={row['P_E']:.2f} P(G)={row['P_G'] if row['P_G'] is None else round(row['P_G'], 2)}"
              f" early|E={row['P_early_given_E']:.2f}  E adv/base/fav={row['P_E_adverse']:.2f}/{row['P_E_base']:.2f}/{row['P_E_favourable']:.2f}")
    with open(HERE / "jev_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            r = json.loads(line)
            u = r["response"].get("usage") or {}
            usage["requests"] += 1
            usage["input_tokens"] += u.get("input_tokens", 0)
            usage["output_tokens"] += u.get("output_tokens", 0)
    print("cumulative logged usage:", usage)


if __name__ == "__main__":
    main()
