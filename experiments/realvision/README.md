# Real Vision sources

An index of Real Vision videos and interviews, handled the same way as the Visser sources.

## Layout
- One folder per video: `experiments/realvision_<guest>_<YYYY-MM-DD>/` (the date is the recording or publication date).
- In each folder:
  - `SOURCE.md`: title, link, guest(s), main message, claims checked against market data, testable calls, stated
    holdings, our read, links to our experiments. Public videos only; this file can be committed.
  - `transcript.txt`: captions or a local Whisper transcript. **Git-ignored**, never published.
  - `PAPER_NOTES*.md`: notes on subscriber-only material (Real Vision Pro, Macro Insiders, Crypto Pro). **Git-ignored.**
- Subscriber videos, PDFs and decks are kept in `~/Documents/Jev-Research-Pack/4-realvision-research/`, never in the repo.

## Real Vision MCP (free tier)
- Server `realvision` at `https://mcp.realvision.com/free`, added to Claude Code for this project only (local scope; no
  login). Tools: GMI macro regime and Macro Seasons, crypto cycle dashboard, market bulletin and movers, headlines,
  US economic calendar, community attention map, and single-ticker data.
- Its answers are Real Vision's own published views (GMI = Raoul Pal's Global Macro Investor). Treat them as claims to
  check, like any other source, and record the `as_of` date each answer carries.
- `rv_submit_feedback` sends a message to Real Vision: use it only when the user asks.

## Rules (same as the Visser work)
- Public YouTube or podcast links: fetch the captions and write `SOURCE.md`. Commit only when asked.
- Walled content: use the copy the user downloads to `~/Downloads`. Notes stay local.
- Check every factual market claim against public data (yfinance, FRED) and record matches and misses.
- When a guest is already tracked elsewhere (for example Jordi Visser), link to that folder and to
  `../visser_stated_holdings/SOURCE.md` for any stated positions.

## Index
| Date | Guest(s) | Title | Folder |
|---|---|---|---|
| | | | |
