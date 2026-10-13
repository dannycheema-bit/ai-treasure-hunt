"""Build PDF research cards for the top-N names by partial rubric score.

Reads local (git-ignored) outputs: first_pass.json, commentary_scores.csv,
frozen_consensus_2026-10-12.json, raw/*.json. Writes cards_top10_<date>.pdf (git-ignored).
Usage: python make_cards.py [N]
"""
import json, sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (KeepInFrame, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

HERE = Path(__file__).parent
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
INK, MUTED, ACCENT, RULE = (colors.HexColor(c) for c in ("#1a1f2b", "#5b6474", "#2456a6", "#d5dae3"))
PENDING_BG, GOOD, WARN, BAD = (colors.HexColor(c) for c in ("#f3f4f7", "#2e7d4f", "#b26a00", "#b3261e"))

ss = getSampleStyleSheet()
S = {
    "title": ParagraphStyle("t", parent=ss["Title"], fontSize=18, leading=22, textColor=INK, alignment=TA_LEFT, spaceAfter=2),
    "sub": ParagraphStyle("s", parent=ss["Normal"], fontSize=9, leading=12, textColor=MUTED),
    "h": ParagraphStyle("h", parent=ss["Heading3"], fontSize=10, leading=13, textColor=ACCENT, spaceBefore=6, spaceAfter=2),
    "b": ParagraphStyle("b", parent=ss["Normal"], fontSize=8.6, leading=11.4, textColor=INK),
    "small": ParagraphStyle("sm", parent=ss["Normal"], fontSize=7.2, leading=9.2, textColor=MUTED),
    "cell": ParagraphStyle("c", parent=ss["Normal"], fontSize=8, leading=10, textColor=INK),
}


def P(text, style="b"):
    return Paragraph(text, S[style])


def fmt_pct(x, signed=True):
    if x is None or pd.isna(x):
        return "n/a"
    return f"{x:+.0f}%" if signed else f"{x:.0f}%"


def fmt_money(x, cur):
    if x is None or pd.isna(x):
        return "n/a"
    for div, suf in ((1e12, "tn"), (1e9, "bn"), (1e6, "m")):
        if abs(x) >= div:
            return f"{cur} {x / div:,.2f}{suf}"
    return f"{cur} {x:,.0f}"


def score_color(v):
    return GOOD if v >= 75 else WARN if v >= 50 else BAD


def components_table(r):
    rows = [["Component (weight)", "Score", "Status"]]
    def add(name, w, val, status):
        rows.append([name + f" ({w}%)", "" if val is None else f"{val:.0f}", status])
    pe, pg = getattr(r, "jev_pe_score", None), getattr(r, "jev_pg_score", None)
    pe = None if pe is None or pd.isna(pe) else float(pe)
    pg = None if pg is None or pd.isna(pg) else float(pg)
    add("Jev P(E) earnings step-up", 30, pe,
        "PENDING - not assessed" if pe is None else
        f"P(E) {pe / 100:.2f}; early|E {r.P_early_given_E:.2f}; adverse/base/fav {r.P_E_adverse:.2f}/{r.P_E_base:.2f}/{r.P_E_favourable:.2f}")
    add("Operating-earnings magnitude (proxy)", 25, r.magnitude_score, "Consensus next-FY EPS growth")
    add("Technical transition", 20, r.technical_score, str(r.technical_state))
    add("Reporting-commentary progression", 15, r.commentary_score, f"Ladder stage {r.commentary_stage} of 8")
    add("Jev P(G) expectations asymmetry", 10, pg,
        "PENDING - not assessed" if pg is None else f"P(G) {pg / 100:.2f}: revenue >=5% above frozen consensus x2")
    t = Table(rows, colWidths=[70 * mm, 16 * mm, 92 * mm])
    style = [("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
             ("TEXTCOLOR", (0, 0), (-1, 0), MUTED), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
             ("LINEBELOW", (0, 1), (-1, -1), 0.3, RULE), ("ALIGN", (1, 0), (1, -1), "CENTER"),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    for i, row in enumerate(rows[1:], 1):
        if row[1] == "":
            style += [("BACKGROUND", (0, i), (-1, i), PENDING_BG), ("TEXTCOLOR", (0, i), (-1, i), MUTED)]
        else:
            style += [("TEXTCOLOR", (1, i), (1, i), score_color(float(row[1]))),
                      ("FONT", (1, i), (1, i), "Helvetica-Bold", 9)]
    t.setStyle(TableStyle(style))
    return t


def kv_table(pairs, widths=(44 * mm, 45 * mm)):
    t = Table([[P(f"<font color='#5b6474'>{escape(k)}</font>", "cell"), P(escape(v), "cell")] for k, v in pairs],
              colWidths=widths)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, RULE),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    return t


def card(r, c, frozen, raw, total):
    cur = (raw.get("info") or {}).get("financialCurrency") or r.currency or ""
    fc = frozen.get(r.ticker) or {}
    q0 = (fc.get("0q") or {}).get("avg")
    flags = r.data_quality_flags or "none"
    story = [
        P(f"{escape(r.company)} <font size=11 color='#5b6474'>&nbsp;{escape(r.ticker)}</font>", "title"),
        P(f"{escape(r.theme)} &nbsp;|&nbsp; Rank {r.partial_rank} of {total} &nbsp;|&nbsp; "
          f"<b>{r.partial_points:.1f}</b> of {100 - (r.attainable_max - r.attainable_min):.0f} available points "
          f"(no-Jev: {r.no_jev_points_of_60} of 60) &nbsp;|&nbsp; evidence quality: "
          f"{escape(str(c.evidence_quality))}", "sub"),
        Spacer(1, 5), components_table(r),
        P("Thesis link: exposed product / revenue line", "h"), P(escape(str(c.exposed_line))),
        P("Why it scores (latest checkpoint " + escape(str(c.latest_report_date)) + ")", "h"), P(escape(str(c.evidence))),
        P("Counterevidence and risks", "h"), P(escape(str(c.counterevidence))),
    ]
    left = kv_table([
        ("Next-FY EPS growth (consensus)", fmt_pct(r.next_fy_eps_growth_pct)),
        ("Next-FY EPS revision, 90 days", fmt_pct(r.eps_next_fy_rev_90d_pct)),
        ("Revisions up / down, 30 days", f"{r.up_30d if pd.notna(r.up_30d) else 'n/a'} / {r.down_30d if pd.notna(r.down_30d) else 'n/a'}"),
        ("Analysts (next FY)", f"{r.analysts:.0f}" if pd.notna(r.analysts) else "n/a"),
        ("EPS surprises, last 4", str(r.surprises_last4 or "n/a")),
        ("Data-quality flags", flags),
    ])
    right = kv_table([
        ("Chart state", str(r.technical_state)),
        ("RSI(14) / vs 50D / vs 200D", f"{r.rsi14:.0f} / {fmt_pct(r.vs50_pct)} / {fmt_pct(r.vs200_pct)}"),
        ("Return 1M / 3M", f"{fmt_pct(r.ret_1m)} / {fmt_pct(r.ret_3m)}"),
        ("From 52-week high", fmt_pct(r.from_52w_high)),
        ("Next report", str(r.next_report or "n/a")),
        ("Frozen revenue consensus, next report (12 Oct)", fmt_money(q0, cur)),
    ])
    grid = Table([[P("Expectations & results", "h"), P("Chart & timing", "h")], [left, right]],
                 colWidths=[90 * mm, 90 * mm])
    grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    story += [grid]
    promote = (f"Next report: revenue at least 5% above the frozen {fmt_money(q0, cur)} consensus <i>and</i> "
               "thesis-line guidance raised or advanced a ladder stage; next-FY EPS consensus keeps rising; "
               "price holds above a rising 50-day average.")
    invalidate = ("Revenue below the frozen consensus or thesis-line guidance cut / delayed (ladder reversal); "
                  "next-FY EPS consensus revised down over the following 30 days; close below a falling 50-day "
                  "average after the report.")
    story += [P("Measurable tests (set before the report)", "h"),
              P(f"<b><font color='#2e7d4f'>Promote:</font></b> {promote}"),
              P(f"<b><font color='#b3261e'>Invalidate:</font></b> {invalidate}")]
    srcs = [s.strip() for s in str(c.sources).split("|") if s.strip()][:4]
    story += [P("Sources", "h")] + [P(f"<link href='{escape(s)}' color='#2456a6'>{escape(s[:120])}</link>", "small") for s in srcs]
    story += [Spacer(1, 4), P("AI-assisted research from a user-defined prompt; scores are ordinal rubric points, not "
                             "expected returns; Jev outputs are subjective and uncalibrated. Not investment advice. "
                             "Local use only - contains material derived from subscriber research.", "small")]
    return KeepInFrame(180 * mm, 270 * mm, story, mode="shrink")


def cover(top, total):
    rows = [["#", "Company", "Ticker", "Theme", "Score /100", "Jev P(E)", "Chart", "Next report"]]
    for r in top.itertuples():
        rows.append([r.partial_rank, P(escape(r.company), "cell"), r.ticker, P(escape(r.theme), "cell"),
                     f"{r.partial_points:.1f}", f"{r.P_E:.2f}" if pd.notna(getattr(r, "P_E", None)) else "n/a", P(escape(str(r.technical_state)), "cell"),
                     r.next_report or "n/a"])
    t = Table(rows, colWidths=[8 * mm, 30 * mm, 16 * mm, 30 * mm, 19 * mm, 17 * mm, 36 * mm, 22 * mm], repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                           ("TEXTCOLOR", (0, 0), (-1, 0), MUTED), ("LINEBELOW", (0, 0), (-1, -1), 0.3, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return [
        P("Lagging AI themes: top-10 research cards", "title"),
        P(f"Prepared {date.today():%d %B %Y} &nbsp;|&nbsp; universe: {total} companies in four lagging AI Macro Nexus "
          "themes &nbsp;|&nbsp; pre-Q3-earnings baseline", "sub"),
        Spacer(1, 8), t, Spacer(1, 10),
        P("How to read these cards", "h"),
        P("Scores use the full default rubric: Jev P(E) 30, magnitude 25, technical 20, commentary 15, Jev P(G) 10 "
          "(Jev = TypeSafe jev-1.13.0, actual model outputs, 13 Oct 2026). Gaps of a few points are ties - read the "
          "list as a tier, not a precise order. Jev P(E) is correlated with the commentary score (it reads the same "
          "evidence), so the two are not independent votes. Jev answers are cautious on future events (most fall "
          "between 0.2 and 0.8); they are subjective and uncalibrated for earnings forecasting until validated "
          "against reported results."),
    ] + cover_notes()


def cover_notes():
    """Thesis summary and run-specific cautions live in card_notes.json (git-ignored), because they
    paraphrase subscriber research: {"sections": [{"heading": "...", "text": "..."}]}."""
    path = HERE / "card_notes.json"
    if not path.exists():
        return []
    out = []
    for s in json.loads(path.read_text()).get("sections", []):
        out += [P(escape(s["heading"]), "h"), P(escape(s["text"]))]
    return out


def disclosures():
    return [
        P("Methodology and disclosures", "title"),
        P("AI assistants (Claude Code with six AI research agents) executed a user-defined prompt, 'Visser Research + "
          "Jev, Reusable Research Prompt' v1.1 (10 Oct 2026), with the user's choice of default settings and later "
          "instructions."),
        P("Materials used", "h"),
        P("User-supplied: AI Macro Nexus 100-name list (deck), Fundamentals (25 Sep and 9 Oct 2026), Technical v3 and "
          "Exhaustion Scores (19 Sep 2026), Visser research paper (12 Oct 2026). Public: Yahoo Finance consensus, "
          "revisions, results and prices via yfinance (fetched 12 Oct 2026); company releases, filings, call "
          "summaries and press, as cited on each card."),
        P("What was checked", "h"),
        P("Every company received the same evidence packet. Agent output was validated for completeness (83 of 83, "
          "no duplicates or blanks). Four high-impact claims were independently confirmed against primary sources "
          "(Solstice-ESI deal, Modine spin-off, Lattice Q2 revenue, NVIDIA Q2 data-centre revenue). Other figures are "
          "agent-sourced; earlier reporting checkpoints often rely on secondary summaries. Where Yahoo and the "
          "user's Fundamentals file disagreed by more than 15 points on EPS growth, the more conservative figure was "
          "used and flagged."),
        P("Jev", "h"),
        P("TypeSafe Jev via the official HTTP API (requested jev-latest, returned jev-1.13.0), 13 Oct 2026. Preflight: "
          "neutral documentation example matched; sensitivity test moved P(E) from 0.07 (adverse evidence) to 0.52 "
          "(actual) to 0.68 (favourable); repeat stable. Per company: one central request (E, G, timing, commercial "
          "progression, evidence quality) and three scenario requests (adverse/base/favourable premises) - 332 "
          "requests, about 398k input tokens. State sent: public evidence only (no subscriber text, no price/chart "
          "data). Noul outputs are documented as the probability of yes; they are not calibrated for corporate "
          "earnings. No Claude judgment was substituted for Jev. A no-Jev ranking on the same 82-name cohort has "
          "rank correlation 0.92 with the default; 7 of the default top ten are also in the no-Jev top ten."),
        P("Limitations", "h"),
        P("Review was performed by AI, not human analysts. Scores are ordinal rubric points with correlated inputs, "
          "not expected returns. Any probabilities, when added, will be subjective and uncalibrated unless validated. "
          "Technical states are computed from adjusted daily closes and change quickly. Data can be revised."),
        P("Not advice", "h"),
        P("This is research, not personalised investment advice, an offer, a trade instruction or a guarantee. "
          "Local use only: it contains material derived from subscriber research whose reproduction is prohibited."),
    ]


def main():
    d = pd.read_json(HERE / "first_pass.json").sort_values("partial_rank")
    c = pd.read_csv(HERE / "commentary_scores.csv").set_index("ticker")
    frozen = json.loads((HERE / "frozen_consensus_2026-10-12.json").read_text())["data"]
    top = d.head(N)
    out = HERE / f"cards_top{N}_{date.today():%Y-%m-%d}.pdf"
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=13 * mm, bottomMargin=12 * mm,
                            title=f"Lagging AI themes - top {N} research cards", author="AI-assisted research")
    story = cover(top, len(d)) + [PageBreak()]
    for r in top.itertuples():
        raw = json.loads((HERE / "raw" / f"{r.ticker}.json").read_text())
        story += [card(r, c.loc[r.ticker], frozen, raw, len(d)), PageBreak()]
    story += disclosures()
    doc.build(story)
    print(out)


if __name__ == "__main__":
    main()
