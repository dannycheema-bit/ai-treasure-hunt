# Start-price capture log

Raw prices are kept locally (git-ignored; market data is not redistributed). This log proves the local
snapshot is unchanged at scoring time.

- Target: 2026-10-28 20:00 UTC (16:00 New York)
- Captured: 2026-10-28 ~22:05 UTC via `track.py start`
- Priced: 16/16; missing: none
- Token observed_at: all 2026-10-28T20:00:00Z (CoinGecko nearest point); stocks HOOD, COIN: 2026-10-28 regular-session close (Yahoo daily bar)
- An earlier capture at ~21:50 UTC used a FIGR-based PORTFOLIO.csv; it was discarded and replaced.
- `prices_start.csv` SHA-256: `f78e6f8e43422888621eb907c3ff94f7f8e0cb6c34324c18fdc0692c408c942c`
