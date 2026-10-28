"""Daily progress check for the two Q4 2026 crypto experiments. Read-only: it never
touches start prices, rules or results. Interim numbers are NOT the score; the Visser test
is scored once, after 2026-12-31 (see visser_crypto_verticals/PREREGISTRATION.md).

Usage: python check.py   -> prints a summary and appends to history.csv (git-ignored)
"""
import csv, json, urllib.request
from datetime import datetime, timezone
from pathlib import Path

EXP = Path(__file__).parent.parent
BASKETS = {
    "Visser 46-name test": EXP / "visser_crypto_verticals",
    "Danny's Crypto Portfolio v1": EXP / "dannys_crypto_portfolio_v1",
    "Danny's Crypto Portfolio v2": EXP / "dannys_crypto_portfolio_v2",
    "Danny's Crypto Portfolio v3": EXP / "dannys_crypto_portfolio_v3",
}


def rows(folder):
    names = "STACK.csv" if (folder / "STACK.csv").exists() else "PORTFOLIO.csv"
    return list(csv.DictReader(open(folder / names)))


def latest_prices(all_rows):
    tokens = sorted({r["price_source_id"] for r in all_rows if r["type"] == "token"})
    url = ("https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids="
           + ",".join(tokens))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = json.load(urllib.request.urlopen(req, timeout=30))
    prices = {k: v["usd"] for k, v in data.items() if "usd" in v}
    import yfinance as yf
    for sym in sorted({r["price_source_id"] for r in all_rows if r["type"] == "stock"}):
        hist = yf.Ticker(sym).history(period="5d", auto_adjust=False)
        if not hist.empty:
            prices[sym] = float(hist["Close"].iloc[-1])
    return prices


def main():
    now = datetime.now(timezone.utc)
    all_rows = [r for f in BASKETS.values() for r in rows(f)]
    prices = latest_prices(all_rows)
    out = [f"Crypto experiments — progress check {now:%Y-%m-%d %H:%M} UTC "
           "(interim only, not the score)"]
    log = []
    for label, folder in BASKETS.items():
        start_file = folder / "prices_start.csv"
        if not start_file.exists():
            out.append(f"\n{label}: not started yet (start prices not captured).")
            continue
        start = {r["symbol"]: float(r["price_usd"]) for r in csv.DictReader(open(start_file))
                 if r["price_usd"]}
        rets = {}
        for r in rows(folder):
            p = prices.get(r["price_source_id"])
            if p is not None and r["symbol"] in start:
                rets[r["symbol"]] = p / start[r["symbol"]] - 1
        basket = sum(rets.values()) / len(rets)
        btc = rets["BTC"]
        ranked = sorted(rets.items(), key=lambda kv: kv[1], reverse=True)
        fmt = lambda items: ", ".join(f"{s} {v:+.0%}" for s, v in items)
        out += [f"\n{label} ({len(rets)}/{len(rows(folder))} priced)",
                f"  basket {basket:+.2%} | bitcoin {btc:+.2%} | gap {(basket - btc) * 100:+.1f} pp",
                f"  best: {fmt(ranked[:3])}",
                f"  worst: {fmt(ranked[-3:])}"]
        log.append({"checked_utc": now.isoformat(timespec="minutes"), "basket": label,
                    "priced": len(rets), "basket_return": round(basket, 6),
                    "btc_return": round(btc, 6), "gap_pp": round((basket - btc) * 100, 2)})
    if log:
        hist = Path(__file__).parent / "history.csv"
        new = not hist.exists()
        with open(hist, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(log[0]))
            if new:
                w.writeheader()
            w.writerows(log)
    print("\n".join(out))


if __name__ == "__main__":
    main()
