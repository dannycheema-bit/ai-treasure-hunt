import sys, numpy as np, pandas as pd
UNTOUCHED_WEEKS = 156
MARGIN = 0.08
def weekly(t):
    c = pd.read_csv(f"{t}.csv", index_col=0, parse_dates=True)["Close"]
    return c.resample("W-FRI").last().dropna()   # last close on/before Friday
g, b = weekly("GLD"), weekly("BTC-USD")
df = pd.concat({"g": g, "b": b}, axis=1).dropna().pct_change().dropna()
df["g_up"] = df.g > 0; df["b_up"] = df.b > 0
df["b_next_up"] = df.b_up.shift(-1)          # Bitcoin's NEXT week; gold week t ends before it starts
d = df.dropna(subset=["b_next_up"]).copy()
d["b_next_up"] = d.b_next_up.astype(bool)
explore, held = d.iloc[:-UNTOUCHED_WEEKS], d.iloc[-UNTOUCHED_WEEKS:]
def acc(x, pred): return float((pred == x.b_next_up).mean())
common = bool(explore.b_next_up.mean() >= 0.5)   # baseline fixed from exploration only
if sys.argv[1:] == ["explore"]:
    print("weeks total", len(d), "explore", len(explore), "untouched", len(held))
    print("explore BTC up share %.3f -> baseline guesses %s" % (explore.b_next_up.mean(), "up" if common else "down"))
    print("explore baseline acc %.3f | gold-rule acc %.3f (exploratory, not the test)" %
          (acc(explore, common), acc(explore, explore.g_up)))
elif sys.argv[1:] == ["final"]:
    base, rule = acc(held, common), acc(held, held.g_up)
    verdict = "SUPPORTED" if rule >= base + MARGIN else ("REJECTED (practical)" if rule <= base else "INCONCLUSIVE")
    print("untouched", held.index[0].date(), "to", held.index[-1].date(), "weeks", len(held))
    print("baseline acc %.3f | rule acc %.3f | gap %+.3f -> %s" % (base, rule, rule - base, verdict))
if sys.argv[1:] == ["reverse"]:
    # EXPLORATORY ONLY: Bitcoin week t direction -> gold week t+1 direction, same split and baseline logic
    r = df.copy(); r["g_next_up"] = r.g_up.shift(-1); r = r.dropna(subset=["g_next_up"]); r["g_next_up"] = r.g_next_up.astype(bool)
    ex, ho = r.iloc[:-UNTOUCHED_WEEKS], r.iloc[-UNTOUCHED_WEEKS:]
    com = bool(ex.g_next_up.mean() >= 0.5)
    for name, x in [("explore", ex), ("untouched", ho)]:
        base = float((com == x.g_next_up).mean()); rule = float((x.b_up == x.g_next_up).mean())
        print("%-9s weeks %d | baseline %.3f | BTC->GLD rule %.3f | gap %+.3f" % (name, len(x), base, rule, rule - base))
