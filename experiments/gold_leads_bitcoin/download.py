import warnings; warnings.filterwarnings("ignore")
import yfinance as yf, pandas as pd
end = pd.Timestamp.today().normalize()
start = end - pd.DateOffset(years=10)
for t in ["GLD", "BTC-USD"]:
    df = yf.download(t, start=start.date(), end=end.date(), interval="1d", auto_adjust=False, progress=False)
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df[["Close"]].dropna().to_csv(f"{t}.csv")
    c = df["Close"].dropna()
    gaps = c.index.to_series().diff().dt.days
    print(t, "rows", len(c), "first", c.index[0].date(), "last", c.index[-1].date(),
          "max gap days", int(gaps.max()), "nonpositive", int((c <= 0).sum()))
