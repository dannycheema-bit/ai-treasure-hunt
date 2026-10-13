"""Fetch public usage evidence for the 42 tokens (DefiLlama fees/revenue/TVL, CoinGecko supply) and the
4 stocks (Yahoo revenue history/consensus). Exploratory: separate from the pre-registered test.
Writes usage_raw.json (git-ignored via experiments/*/... rules for data files)."""
import json, time, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
SLUGS = {  # DefiLlama slug candidates, first that returns data wins
    "TAO": ["bittensor"], "VIRTUAL": ["virtuals-protocol"], "VVV": ["venice"], "AKT": ["akash"],
    "AR": ["arweave"], "FIL": ["filecoin"], "GEOD": ["geodnet"], "GRASS": ["grass"], "HNT": ["helium", "helium-network"],
    "IOTX": ["iotex"], "RENDER": ["render-network", "render-network-bme"], "BTC": ["bitcoin"], "XMR": ["monero"],
    "ZEC": ["zcash"], "HYPE": ["hyperliquid"], "JUP": ["jupiter"], "RUNE": ["thorchain-dex", "thorchain"], "UNI": ["uniswap"],
    "AAVE": ["aave"], "MORPHO": ["morpho"], "PENDLE": ["pendle"], "SYRUP": ["maple", "maple-finance"],
    "GRT": ["the-graph"], "LINK": ["chainlink"], "PYTH": ["pyth-network", "pyth"], "ZRO": ["layerzero"],
    "CC": ["canton", "canton-network"], "ETH": ["ethereum"], "NEAR": ["near"], "SOL": ["solana"], "SUI": ["sui"],
    "TRX": ["tron"], "XLM": ["stellar"], "XRP": ["xrpl", "ripple"], "ENA": ["ethena"], "SKY": ["sky"],
    "ETHFI": ["ether.fi", "etherfi"], "JTO": ["jito"], "LDO": ["lido"], "CFG": ["centrifuge"],
    "HASH": ["provenance"], "ONDO": ["ondo-finance", "ondo"],
}


def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (400, 404, 500):
                return None
            time.sleep(10 * (i + 1))
        except (ValueError, urllib.error.URLError):
            return None  # non-JSON body (e.g. "not found" text) or network error
    return None


def windows(chart):
    """chart: [[unix, value], ...] daily -> sums for last 90d, prior 90d, last 30d, prior 30d."""
    if not chart:
        return None
    pts = sorted((int(t), float(v or 0)) for t, v in chart)
    last = pts[-1][0]
    def s(a, b):
        return sum(v for t, v in pts if last - b * 86400 < t <= last - a * 86400)
    return {"last_date": datetime.fromtimestamp(last, timezone.utc).date().isoformat(),
            "last30": s(0, 30), "prev30": s(30, 60), "last90": s(0, 90), "prev90": s(90, 180),
            "year_ago90": s(365, 455), "days": len(pts)}


def defillama(slugs):
    out = {"slug": None}
    for slug in slugs:
        f = get(f"https://api.llama.fi/summary/fees/{slug}?dataType=dailyFees")
        if f and f.get("totalDataChart"):
            out.update(slug=slug, name=f.get("name"), fees=windows(f["totalDataChart"]))
            r = get(f"https://api.llama.fi/summary/fees/{slug}?dataType=dailyRevenue")
            out["revenue"] = windows(r["totalDataChart"]) if r and r.get("totalDataChart") else None
            break
    for slug in ([out["slug"]] if out["slug"] else []) + slugs:
        p = get(f"https://api.llama.fi/tvl/{slug}")
        if isinstance(p, (int, float)) and p > 0:
            out["tvl_usd"] = p
            break
    return out


def main():
    import csv
    stack = list(csv.DictReader(open(HERE.parent / "STACK.csv")))
    tokens = [r for r in stack if r["type"] == "token"]
    ids = ",".join(r["price_source_id"] for r in tokens)
    cg = get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&per_page=100") or []
    cgm = {c["id"]: {k: c.get(k) for k in ("market_cap", "fully_diluted_valuation", "circulating_supply",
                                             "total_supply", "max_supply")} for c in cg}
    data = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "names": {}}
    for r in tokens:
        d = defillama(SLUGS.get(r["symbol"], []))
        d["supply"] = cgm.get(r["price_source_id"])
        data["names"][r["symbol"]] = {"name": r["name"], "vertical": r["vertical"], "type": "token", **d}
        print(f"{r['symbol']:8} slug={d['slug']!s:16} fees90={(d.get('fees') or {}).get('last90')} prev90={(d.get('fees') or {}).get('prev90')} tvl={d.get('tvl_usd')}")
        time.sleep(0.5)
    import yfinance as yf
    for r in [r for r in stack if r["type"] == "stock"]:
        t = yf.Ticker(r["price_source_id"])
        q = t.quarterly_income_stmt
        revs = q.loc["Total Revenue"].dropna().sort_index().tail(6) if "Total Revenue" in q.index else None
        est = t.revenue_estimate
        data["names"][r["symbol"]] = {"name": r["name"], "vertical": r["vertical"], "type": "stock",
            "quarterly_revenue": None if revs is None else {str(k)[:10]: float(v) for k, v in revs.items()},
            "revenue_consensus": None if est is None else {p: float(est.loc[p, "avg"]) for p in est.index}}
        print(f"{r['symbol']:8} stock revenue quarters={0 if revs is None else len(revs)}")
    (HERE / "usage_raw.json").write_text(json.dumps(data, indent=1, default=str))


if __name__ == "__main__":
    main()
