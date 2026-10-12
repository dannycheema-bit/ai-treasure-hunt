"""First-pass, equal-coverage analysis of every company in raw/ (see METHODOLOGY.md).

Computes, for all 83 names, the components that do NOT need Jev or transcript research:
  - Technical transition score (20% of the default rubric)
  - Consensus-implied earnings magnitude proxy (25% of the default rubric)
plus unscored diagnostics: expectations momentum (90-day EPS revisions), reported-results history,
and a frozen revenue consensus for the later expectations-asymmetry (G) test.
Jev P(E) 30%, Jev P(G) 10% and commentary progression 15% stay PENDING (never filled in).

Outputs (git-ignored): first_pass.xlsx, frozen_consensus_2026-10-12.json, first_pass.json
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
RAW = HERE / "raw"
WEIGHTS = {"jev_pe": 30, "magnitude": 25, "technical": 20, "commentary": 15, "jev_pg": 10}
AVAILABLE = ("magnitude", "technical", "commentary")
FROZEN = HERE / "frozen_consensus_2026-10-12.json"


def commentary_scores():
    """Phase-2 input: commentary_scores.csv (ticker, stage, commentary_score, evidence, sources).
    Missing names stay PENDING; nothing is filled in."""
    path = HERE / "commentary_scores.csv"
    if not path.exists():
        return {}
    c = pd.read_csv(path)
    return {r.ticker: r for r in c.itertuples() if pd.notna(r.commentary_score)}


def split(rec, key):
    d = rec.get(key)
    if not d:
        return None
    return pd.DataFrame(d["data"], index=d["index"], columns=d["columns"])


def rsi(close, n=14):
    delta = close.diff()
    up = delta.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    down = (-delta.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / down)


def technicals(rec):
    p = split(rec, "prices")
    if p is None or len(p) < 220:
        return None
    c = p["Close"].astype(float)
    s50, s200 = c.rolling(50).mean(), c.rolling(200).mean()
    t = {
        "last_date": str(p.index[-1])[:10],
        "rsi14": rsi(c).iloc[-1],
        "vs50_pct": (c.iloc[-1] / s50.iloc[-1] - 1) * 100,
        "vs200_pct": (c.iloc[-1] / s200.iloc[-1] - 1) * 100,
        "slope50_pct": (s50.iloc[-1] / s50.iloc[-21] - 1) * 100,          # 50D avg change over ~1 month
        "slope50_prev_pct": (s50.iloc[-21] / s50.iloc[-41] - 1) * 100,     # the month before
        "slope200_pct": (s200.iloc[-1] / s200.iloc[-21] - 1) * 100,
        "ret_1m": (c.iloc[-1] / c.iloc[-22] - 1) * 100,
        "ret_3m": (c.iloc[-1] / c.iloc[-64] - 1) * 100,
        "from_52w_high": (c.iloc[-1] / c.iloc[-252:].max() - 1) * 100,
    }
    t["state"], t["technical_score"] = classify(t)
    return t


def classify(t):
    """Rubric anchors (0-100). Rewards an EARLY improving transition, not a static strong chart."""
    above50, above200 = t["vs50_pct"] > 0, t["vs200_pct"] > 0
    turning = t["slope50_pct"] > t["slope50_prev_pct"]
    if t["vs200_pct"] > 35 or t["rsi14"] > 75:
        return "Extended", 40
    if above50 and turning and t["slope50_prev_pct"] <= 0.5 and t["vs50_pct"] <= 12 and t["rsi14"] <= 70:
        return "Early improving", 90                     # reclaiming 50D as the 50D turns up
    if above50 and above200 and t["slope50_pct"] > 0 and t["slope200_pct"] > 0:
        return "Established uptrend", 65
    if not above50 and turning and t["slope50_pct"] > t["slope50_prev_pct"] + 0.5 and t["rsi14"] >= 45:
        return "Basing (below 50D, momentum improving)", 55
    if not above50 and t["slope50_pct"] < 0 and not turning:
        return "Deteriorating", 15
    return "Neutral / mixed", 45


def growth_score(g):
    return 10 if g < 0 else 30 if g < 10 else 50 if g < 20 else 70 if g < 35 else 85 if g < 60 else 95


def magnitude(rec):
    """Consensus-implied next-FY EPS growth mapped to anchors. A PROXY for the conditional
    driver-specific step-up; theme concentration is not yet measured (needs research)."""
    e = split(rec, "earnings_estimate")
    if e is None or "0y" not in e.index or "+1y" not in e.index:
        return None, None
    cur, nxt = e.loc["0y", "avg"], e.loc["+1y", "avg"]
    if not (np.isfinite(cur) and np.isfinite(nxt)):
        return None, None
    if cur <= 0:
        g = None
        score = 75 if nxt > 0 else 20                    # loss -> profit transition vs still loss-making
    else:
        g = (nxt / cur - 1) * 100
        score = growth_score(g)
    return g, score


def magnitude_checked(rec):
    """Uniform data-quality rule: if Yahoo and the user's Fundamentals file disagree on next-FY EPS
    growth by >15pp (fiscal-year alignment, GAAP vs adjusted), keep the MORE CONSERVATIVE score."""
    g, score = magnitude(rec)
    v = rec["universe"].get("Next-Year EPS Growth")
    vg = v * 100 if isinstance(v, (int, float)) else None
    flags = []
    if g is not None and vg is not None and abs(g - vg) > 15:
        score = min(score, growth_score(vg))
        flags.append(f"growth conflict (Yahoo {g:+.0f}% vs file {vg:+.0f}%): conservative score")
    if g is not None and g > 150:
        flags.append("low-base growth (saturates)")
    e = split(rec, "earnings_estimate")
    if e is not None and "+1y" in e.index and (e.loc["+1y", "numberOfAnalysts"] or 0) < 3:
        flags.append("thin coverage (<3 analysts)")
    return g, vg, score, "; ".join(flags)


def momentum(rec):
    tr = split(rec, "eps_trend")
    rv = split(rec, "eps_revisions")
    out = {}
    if tr is not None and "+1y" in tr.index:
        now, ago = tr.loc["+1y", "current"], tr.loc["+1y", "90daysAgo"]
        if np.isfinite(now) and np.isfinite(ago) and ago:
            out["eps_next_fy_rev_90d_pct"] = (now / ago - 1) * 100 * (1 if ago > 0 else -1)
        now0, ago0 = tr.loc["0y", "current"], tr.loc["0y", "90daysAgo"]
        if np.isfinite(now0) and np.isfinite(ago0) and ago0:
            out["eps_cur_fy_rev_90d_pct"] = (now0 / ago0 - 1) * 100 * (1 if ago0 > 0 else -1)
    if rv is not None and "+1y" in rv.index:
        out["up_30d"] = rv.loc["+1y", "upLast30days"]
        out["down_30d"] = rv.loc["+1y", "downLast30days"]
    e = split(rec, "earnings_estimate")
    if e is not None and "+1y" in e.index:
        out["analysts"] = e.loc["+1y", "numberOfAnalysts"]
    return out


def reported(rec):
    ed = split(rec, "earnings_dates")
    out = {"next_report": None, "surprises_last4": None, "beats_last4": None}
    if ed is not None:
        ed.index = pd.to_datetime(ed.index, utc=True)
        fut = ed[ed["Reported EPS"].isna() & (ed.index > pd.Timestamp.now(tz="UTC"))]
        if len(fut):
            out["next_report"] = str(fut.index.min())[:10]
        past = ed.dropna(subset=["Reported EPS"]).sort_index(ascending=False).head(4)
        if len(past):
            s = past["Surprise(%)"].round(1).tolist()
            out["surprises_last4"] = ", ".join(f"{x:+.0f}%" for x in s)
            out["beats_last4"] = int((past["Surprise(%)"] > 0).sum())
    q = split(rec, "quarterly_income")
    if q is not None:
        row = "Operating Income" if "Operating Income" in q.index else ("EBIT" if "EBIT" in q.index else None)
        if row:
            v = q.loc[row].dropna().sort_index(ascending=False)
            if len(v) >= 5:
                out["opinc_yoy_latest_pct"] = (v.iloc[0] / v.iloc[4] - 1) * 100 * (1 if v.iloc[4] > 0 else -1)
            out["opinc_quarters"] = len(v)
    return out


def frozen_consensus(rec):
    r = split(rec, "revenue_estimate")
    if r is None:
        return None
    return {p: {"avg": r.loc[p, "avg"], "analysts": r.loc[p, "numberOfAnalysts"] if "numberOfAnalysts" in r else None}
            for p in r.index}


def main():
    rows, frozen = [], {}
    comm = commentary_scores()
    for path in sorted(RAW.glob("*.json")):
        rec = json.loads(path.read_text())
        u = rec["universe"]
        tech = technicals(rec) or {}
        g, vg, mscore, dq = magnitude_checked(rec)
        row = {"ticker": u["Ticker"], "company": u["Company"], "theme": u["Theme"],
               "currency": (rec.get("info") or {}).get("currency"),
               "next_fy_eps_growth_pct": g, "file_next_fy_eps_growth_pct": vg,
               "magnitude_score": mscore, "data_quality_flags": dq,
               "technical_state": tech.get("state"), "technical_score": tech.get("technical_score"),
               **{k: tech.get(k) for k in ("rsi14", "vs50_pct", "vs200_pct", "slope50_pct",
                                          "slope50_prev_pct", "slope200_pct", "ret_1m", "ret_3m",
                                          "from_52w_high", "last_date")},
               **momentum(rec), **reported(rec),
               "jev_pe": "PENDING (Jev not connected)", "jev_pg": "PENDING (Jev not connected)",
               "commentary_score": (float(comm[u["Ticker"]].commentary_score) if u["Ticker"] in comm else None),
               "commentary_stage": (comm[u["Ticker"]].stage if u["Ticker"] in comm else "PENDING (phase 2 research)")}
        avail = [c for c in AVAILABLE if row[f"{c}_score"] is not None]
        row["components_available"] = len(avail)
        pts = sum(WEIGHTS[c] * row[f"{c}_score"] / 100 for c in avail)
        missing_w = 100 - sum(WEIGHTS[c] for c in avail)
        row["partial_points"] = round(pts, 1)                    # out of the available weight
        row["attainable_min"] = round(pts, 1)
        row["attainable_max"] = round(pts + missing_w, 1)
        row["no_jev_partial_pct"] = round(100 * pts / sum(WEIGHTS[c] for c in avail), 1) if avail else None
        rows.append(row)
        frozen[u["Ticker"]] = frozen_consensus(rec)

    df = pd.DataFrame(rows)
    # Lenses (distinct perspectives, not quotas)
    lag = df["ret_3m"] < 0
    rev_up = df["eps_next_fy_rev_90d_pct"] > 3
    tech_turn = df["technical_state"].isin(["Early improving", "Basing (below 50D, momentum improving)"])
    df["lens_unpriced_inflection"] = lag & rev_up & tech_turn     # angle 2: earnings turning, chart lagging
    df["lens_revisions_up_chart_lagging"] = lag & rev_up
    df = df.sort_values(["partial_points", "eps_next_fy_rev_90d_pct"], ascending=False)
    df.insert(0, "partial_rank", range(1, len(df) + 1))

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if not FROZEN.exists():  # frozen once; never overwritten by later refreshes
        FROZEN.write_text(json.dumps(
            {"frozen_utc": stamp, "source": "Yahoo Finance revenue_estimate via yfinance", "data": frozen},
            default=float, indent=1))
    df.to_json(HERE / "first_pass.json", orient="records", indent=1, default_handler=str)
    with pd.ExcelWriter(HERE / "first_pass.xlsx") as xw:
        df.to_excel(xw, "Coverage & scores", index=False)
        df[df["lens_unpriced_inflection"]].to_excel(xw, "Lens - unpriced inflection", index=False)
        df.sort_values("eps_next_fy_rev_90d_pct", ascending=False).head(20).to_excel(
            xw, "Lens - revision momentum", index=False)
        pd.DataFrame([{"component": k, "weight": v,
                       "status": ("computed" if k in ("magnitude", "technical")
                                  else f"{len(comm)}/{len(df)} scored" if k == "commentary" else "PENDING")} for k, v in WEIGHTS.items()]
                     ).to_excel(xw, "Rubric", index=False)
    print(f"{len(df)} names | stamp {stamp}")
    print(df["technical_state"].value_counts().to_string())
    print("magnitude available:", df["magnitude_score"].notna().sum(),
          "| revisions available:", df["eps_next_fy_rev_90d_pct"].notna().sum(),
          "| unpriced-inflection lens:", int(df["lens_unpriced_inflection"].sum()))


if __name__ == "__main__":
    main()
