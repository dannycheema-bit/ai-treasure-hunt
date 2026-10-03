"""Paper-track Danny's Crypto Portfolio v1. See README.md.

Usage:  python track.py start   -> prices_start.csv  (2026-10-05 20:00 UTC)
        python track.py end     -> prices_end.csv, then prints the return vs Bitcoin
"""
import csv, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "visser_crypto_verticals"))
import capture  # reuse the same price conventions as the Visser test

capture.TARGETS = {
    "start": datetime(2026, 10, 5, 20, 0, tzinfo=timezone.utc),
    "end": datetime(2026, 12, 31, 21, 0, tzinfo=timezone.utc),
}


def report():
    load = lambda n: {r["symbol"]: r for r in csv.DictReader(open(HERE / n))}
    start, end = load("prices_start.csv"), load("prices_end.csv")
    rets = {s: float(end[s]["price_usd"]) / float(start[s]["price_usd"]) - 1
            for s in start if start[s]["price_usd"] and end[s]["price_usd"]}
    port = sum(rets.values()) / len(rets)
    print(f"priced {len(rets)}/16 | portfolio {port:+.2%} | bitcoin {rets['BTC']:+.2%} "
          f"| gap {(port - rets['BTC']) * 100:+.1f} pp")


if __name__ == "__main__":
    phase = sys.argv[1]
    capture.HERE = HERE  # write prices_*.csv here, reading PORTFOLIO.csv
    capture.main(phase, stack_file="PORTFOLIO.csv")
    if phase == "end":
        report()
