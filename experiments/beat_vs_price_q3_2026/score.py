"""Score the pre-registered beat-vs-price test ONCE (on/after 2026-12-08). See PREREGISTRATION.md.

Usage:  python score.py --dry-run   (checks data availability only; prints NO returns or surprises)
        python score.py             (scores; writes results.csv and FINAL_RESULT.txt, both git-ignored)
"""
import json, sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf

HERE = Path(__file__).parent
SRC = HERE.parent / "ai_nexus_lagging_inflection"
FROZEN = json.loads((SRC / "frozen_consensus_2026-10-12.json").read_text())["data"]
UNIVERSE = sorted(r["ticker"] for r in json.loads((SRC / "first_pass.json").read_text()))
PRIMARY = (date(2026, 10, 23), date(2026, 11, 30))
SECONDARY = (date(2026, 10, 13), date(2026, 10, 22))
BENCH = {".T": "^N225", ".DE": "^GDAXI", ".PA": "^FCHI", ".AS": "^AEX", ".L": "^FTSE", ".MI": "FTSEMIB.MI",
         ".NS": "^NSEI"}
CLOSE_HOUR = {".T": 15, ".DE": 17, ".PA": 17, ".AS": 17, ".L": 16, ".MI": 17, ".NS": 15}  # local, else 16 (US)


def bench_for(t):
    return next((b for s, b in BENCH.items() if t.endswith(s)), "SPY")


def close_hour(t):
    return next((h for s, h in CLOSE_HOUR.items() if t.endswith(s)), 16)


def report_event(tk, t):
    ed = tk.get_earnings_dates(limit=12)
    if ed is None or ed.empty:
        return None
    ed = ed[ed.index > pd.Timestamp("2026-10-12", tz=ed.index.tz)].sort_index()
    ed = ed.dropna(subset=["Reported EPS"]) if "Reported EPS" in ed else ed
    if ed.empty:
        return None
    ts = ed.index[0]
    return {"ts": ts, "eps_surprise_pct": ed.iloc[0].get("Surprise(%)")}


def revenue_surprise(tk, t, report_ts):
    q = tk.quarterly_income_stmt
    if q is None or "Total Revenue" not in q.index:
        return None, "no revenue line"
    rev = q.loc["Total Revenue"].dropna()
    rev = rev[(rev.index > pd.Timestamp("2026-06-30")) & (rev.index < report_ts.tz_localize(None))]
    est = ((FROZEN.get(t) or {}).get("0q") or {}).get("avg")
    if rev.empty or not est:
        return None, "no aligned quarter or no frozen 0q"
    s = float(rev.sort_index().iloc[-1]) / float(est) - 1
    if abs(s) > 0.5:
        return None, f"misaligned (|surprise|>50%)"
    return s, "ok"


def reaction(t, report_ts):
    first = report_ts.date() if report_ts.hour < close_hour(t) else report_ts.date() + timedelta(days=1)
    start, end = first - timedelta(days=10), first + timedelta(days=14)
    px = yf.Ticker(t).history(start=start, end=end, auto_adjust=True)["Close"]
    bx = yf.Ticker(bench_for(t)).history(start=start, end=end, auto_adjust=True)["Close"]
    px.index, bx.index = px.index.date, bx.index.date
    pre = [d for d in px.index if d < first]
    post = [d for d in px.index if d >= first]
    if not pre or len(post) < 5:
        return None
    d0, d5 = pre[-1], post[4]
    bpre = [d for d in bx.index if d <= d0]
    bpost = [d for d in bx.index if d <= d5]
    if not bpre or not bpost:
        return None
    r = px[d5] / px[d0] - 1
    b = bx[bpost[-1]] / bx[bpre[-1]] - 1
    return {"pre_date": str(d0), "post_date": str(d5), "ret": r, "bench": bench_for(t), "bench_ret": b, "abn": r - b}


def main():
    dry = "--dry-run" in sys.argv
    if not dry and date.today() < date(2026, 12, 8):
        raise SystemExit("Scoring is pre-registered for on/after 2026-12-08. Use --dry-run before then.")
    rows = []
    for t in UNIVERSE:
        tk = yf.Ticker(t)
        ev = report_event(tk, t)
        row = {"ticker": t}
        if ev is None:
            row["status"] = "no report after 12 Oct yet"
            rows.append(row)
            continue
        d = ev["ts"].date()
        row["report_date"] = str(d)
        row["sample"] = ("PRIMARY" if PRIMARY[0] <= d <= PRIMARY[1] else
                         "SECONDARY" if SECONDARY[0] <= d <= SECONDARY[1] else "EXCLUDED (outside windows)")
        if dry:
            row["status"] = "date found"
            rows.append(row)
            continue
        s, why = revenue_surprise(tk, t, ev["ts"])
        rx = reaction(t, ev["ts"])
        row.update(status=why if s is None else ("ok" if rx else "no 5-session window"), rev_surprise=s,
                   eps_surprise_pct=ev["eps_surprise_pct"], **(rx or {}))
        if s is not None:
            row["group"] = "BEAT" if s >= 0.05 else "MISS" if s < 0 else "IN-LINE"
        rows.append(row)
    df = pd.DataFrame(rows)
    if dry:
        print(df.groupby(["sample", "status"], dropna=False).size().to_string())
        return
    df.to_csv(HERE / "results.csv", index=False)
    p = df[(df["sample"] == "PRIMARY") & (df["status"] == "ok")]
    beat, miss = p[p.group == "BEAT"].abn, p[p.group == "MISS"].abn
    lines = [f"scored {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC | primary ok: {len(p)} "
             f"(BEAT {len(beat)}, IN-LINE {(p.group == 'IN-LINE').sum()}, MISS {len(miss)})"]
    if len(beat) < 5 or len(miss) < 5:
        lines.append("-> INCONCLUSIVE (too few names in BEAT or MISS)")
    else:
        D = (beat.median() - miss.median()) * 100
        verdict = "CLASSIC LINK HOLDS" if D >= 3 else "LINK WEAK (Visser supported)" if D <= 1 else "INCONCLUSIVE"
        lines.append(f"median abn 5d: BEAT {beat.median():+.2%} | MISS {miss.median():+.2%} | D {D:+.2f} pp -> {verdict}")
    lines.append("--- reported alongside (cannot change verdict) ---")
    if len(p) > 2:
        lines.append(f"Spearman(rev surprise, abn) primary: {p.rev_surprise.rank().corr(p.abn.rank()):+.2f}")
    s2 = df[(df["sample"] == "SECONDARY") & (df["status"] == "ok")]
    lines.append(f"secondary ok: {len(s2)}; median abn by group: "
                 f"{s2.groupby('group').abn.median().round(4).to_dict() if len(s2) else {}}")
    pe = p.dropna(subset=["eps_surprise_pct"])
    if len(pe) > 2:
        lines.append(f"EPS-surprise split: beat(>0) median abn {pe[pe.eps_surprise_pct > 0].abn.median():+.2%} vs "
                     f"miss(<=0) {pe[pe.eps_surprise_pct <= 0].abn.median():+.2%}")
    lines.append(f"excluded/failed: {df[df.status != 'ok'][['ticker', 'status']].values.tolist()}")
    (HERE / "FINAL_RESULT.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
