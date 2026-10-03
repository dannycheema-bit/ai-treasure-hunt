"""Score the pre-registered test ONCE, after prices_end.csv exists. See PREREGISTRATION.md."""
import csv
from pathlib import Path

HERE = Path(__file__).parent


def load(name):
    return {r["symbol"]: r for r in csv.DictReader(open(HERE / name))}


start, end = load("prices_start.csv"), load("prices_end.csv")
stack = list(csv.DictReader(open(HERE / "STACK.csv")))
assert len(stack) == 46

missing_start = [s["symbol"] for s in stack if start[s["symbol"]]["status"].startswith("ok") is False]
missing_end = [s["symbol"] for s in stack if end[s["symbol"]]["status"].startswith("ok") is False]
lines = [f"start missing: {missing_start or 'none'} | end missing: {missing_end or 'none'}"]

if len(missing_start) > 3 or len(missing_end) > 3:
    lines.append("-> INFEASIBLE (more than 3 names unpriced at one end)")
else:
    # Missing end prices must be resolved by hand per PREREGISTRATION.md (last price or -100%)
    # and written into prices_end.csv with status "ok (fallback)" before scoring.
    if missing_start or missing_end:
        raise SystemExit("Resolve missing names per PREREGISTRATION.md first.")
    rets = {s["symbol"]: float(end[s["symbol"]]["price_usd"]) / float(start[s["symbol"]]["price_usd"]) - 1
            for s in stack}
    basket = sum(rets.values()) / len(rets)
    btc = rets["BTC"]
    gap = (basket - btc) * 100
    verdict = "SUPPORTED" if gap >= 10 else "REJECTED" if gap <= 0 else "INCONCLUSIVE"
    lines += ["window 2026-09-30 20:00 UTC -> 2026-12-31 21:00 UTC, 46 names",
              f"basket {basket:+.2%} | bitcoin {btc:+.2%} | gap {gap:+.1f} pp -> {verdict}"]

print("\n".join(lines))
(HERE / "FINAL_RESULT.txt").write_text("\n".join(lines) + "\n")
