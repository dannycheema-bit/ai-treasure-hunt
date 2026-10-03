"""Capture prices for one pre-registered timestamp. See PREREGISTRATION.md.

Usage:  python capture.py start   -> prices_start.csv  (2026-09-30 20:00 UTC)
        python capture.py end     -> prices_end.csv    (2026-12-31 21:00 UTC)

Only a +/-90 minute window around the timestamp is requested, so running "start"
reveals nothing about later prices. Tokens: CoinGecko public API. Stocks: yfinance.
"""
import csv, json, sys, time, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
TARGETS = {
    "start": datetime(2026, 9, 30, 20, 0, tzinfo=timezone.utc),
    "end": datetime(2026, 12, 31, 21, 0, tzinfo=timezone.utc),
}
WINDOW = timedelta(minutes=90)


def coingecko_nearest(cg_id, target):
    lo, hi = int((target - WINDOW).timestamp()), int((target + WINDOW).timestamp())
    url = (f"https://api.coingecko.com/api/v3/coins/{cg_id}/market_chart/range"
           f"?vs_currency=usd&from={lo}&to={hi}")
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            prices = json.load(urllib.request.urlopen(req, timeout=30))["prices"]
            break
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(30 * (attempt + 1))
    else:
        return None, None
    if not prices:
        return None, None
    ms, price = min(prices, key=lambda p: abs(p[0] / 1000 - target.timestamp()))
    return price, datetime.fromtimestamp(ms / 1000, timezone.utc)


def yahoo_close(symbol, target):
    import yfinance as yf
    day = target.date()
    hist = yf.Ticker(symbol).history(start=day, end=day + timedelta(days=1), auto_adjust=False)
    if hist.empty:
        return None, None
    return float(hist["Close"].iloc[-1]), hist.index[-1].to_pydatetime()


def main(phase, stack_file="STACK.csv"):
    target = TARGETS[phase]
    out = []
    for row in csv.DictReader(open(HERE / stack_file)):
        if row["type"] == "stock":
            price, observed = yahoo_close(row["price_source_id"], target)
        else:
            price, observed = coingecko_nearest(row["price_source_id"], target)
            time.sleep(6)  # stay under the free-tier rate limit
        status = "ok" if price is not None else "MISSING"
        print(f"{row['symbol']:8} {status:8} {price} @ {observed}")
        out.append({"symbol": row["symbol"], "type": row["type"],
                    "price_usd": "" if price is None else repr(price),
                    "observed_at": "" if observed is None else observed.isoformat(),
                    "status": status})
    path = HERE / f"prices_{phase}.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    missing = sum(r["status"] == "MISSING" for r in out)
    print(f"\n{path.name}: {len(out) - missing} ok, {missing} missing "
          f"(feasibility limit: missing <= 3)")


if __name__ == "__main__":
    main(sys.argv[1])
