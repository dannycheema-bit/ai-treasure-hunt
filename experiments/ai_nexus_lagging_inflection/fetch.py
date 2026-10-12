"""Fetch the evidence layer for every company in the agreed universe (equal first-pass coverage).

Universe: the four "Mixed" AI Macro Nexus themes in the user's Fundamentals file (9 Oct 2026).
Writes one JSON per ticker to raw/ (git-ignored: licensed/subscriber data stays local).
Source: Yahoo Finance via yfinance (consensus, revisions, earnings history, financials, prices).
"""
import json, sys, time
from datetime import datetime, timezone
from pathlib import Path

import openpyxl
import yfinance as yf

HERE = Path(__file__).parent
RAW = HERE / "raw"
FUND = Path.home() / "Downloads" / "AI_Macro_Nexus_Fundamentals_2026-10-09.xlsx"
THEMES = {"Optical & Interconnects", "Semicon Architecture",
          "Energy & Infrastructure", "Chemicals & Materials"}


def universe():
    rows = list(openpyxl.load_workbook(FUND, data_only=True, read_only=True)
                .active.iter_rows(values_only=True))
    header = rows[1]
    out = [dict(zip(header, r)) for r in rows[2:] if r and r[3] and r[0] in THEMES]
    return out


def frame(df):
    if df is None or getattr(df, "empty", True):
        return None
    df = df.copy()
    df.columns = [str(c) for c in df.columns]
    df.index = [str(i) for i in df.index]
    return json.loads(df.to_json(orient="split", date_format="iso"))


def fetch(row):
    t = yf.Ticker(row["Ticker"])
    rec = {"universe": {k: v for k, v in row.items()},
           "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "errors": {}}
    for name in ["eps_trend", "eps_revisions", "earnings_estimate", "revenue_estimate"]:
        try:
            rec[name] = frame(getattr(t, name))
        except Exception as e:
            rec["errors"][name] = repr(e)
    try:
        rec["earnings_dates"] = frame(t.get_earnings_dates(limit=12))
    except Exception as e:
        rec["errors"]["earnings_dates"] = repr(e)
    try:
        q = t.quarterly_income_stmt
        keep = [r for r in ("Total Revenue", "Operating Income", "EBIT") if r in q.index]
        rec["quarterly_income"] = frame(q.loc[keep]) if keep else None
    except Exception as e:
        rec["errors"]["quarterly_income"] = repr(e)
    try:
        h = t.history(period="2y", auto_adjust=True)[["Close", "Volume"]]
        rec["prices"] = frame(h)
    except Exception as e:
        rec["errors"]["prices"] = repr(e)
    try:
        info = t.info
        rec["info"] = {k: info.get(k) for k in ("longName", "currency", "financialCurrency",
                                                 "exchange", "sector", "industry", "longBusinessSummary")}
    except Exception as e:
        rec["errors"]["info"] = repr(e)
    return rec


def main():
    RAW.mkdir(exist_ok=True)
    uni = universe()
    print(f"universe: {len(uni)} companies")
    for i, row in enumerate(uni, 1):
        path = RAW / f"{row['Ticker'].replace('/', '_')}.json"
        if path.exists() and "--refresh" not in sys.argv:
            continue
        rec = fetch(row)
        path.write_text(json.dumps(rec, default=str))
        print(f"{i:3}/{len(uni)} {row['Ticker']:12} errors={list(rec['errors'])}")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
