"""Preflight required by the research prompt (section 2) before any Jev scoring.

1. Neutral test: TypeSafe's own documentation example (no research data sent).
2. Capability test: ONE company-level forward-looking event (ASML), using only public evidence
   from this project (no subscriber text), to see whether Jev returns a usable yes-probability.
Prints model version, answers and token usage; saves the full exchange to jev_preflight_log.json
(git-ignored). Never prints the API key.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

from jev_client import system_one

HERE = Path(__file__).parent

NEUTRAL_STATE = ("Our API integration started returning 500 errors on every request about 20 minutes ago, "
                 "and we can't process any customer orders until this is fixed.")
NEUTRAL_Q = {"is_urgent": {"type": "noul", "instructions": "The message conveys urgency or time-sensitivity"}}

ASML_STATE = {
    "as_of": "2026-10-12",
    "company": "ASML Holding (ASML), lithography equipment",
    "latest_report": "2026-07-15 Q2 2026: net sales about EUR 9.3bn, gross margin 54%; FY2026 outlook raised for "
                     "the second time; Q3 guide EUR 11-12bn; management says 2027 EUV capacity is close to fully "
                     "booked and AI drives logic and memory demand.",
    "consensus": "Next-fiscal-year EPS growth about +36%; next-year EPS estimate revised up about 19% over 90 days; "
                 "4 upward and 0 downward revisions in 30 days; 33 analysts.",
    "counterevidence": "Quarterly bookings no longer disclosed; China export restrictions; outlook back-end loaded.",
    "next_report": "2026-10-14",
}
E_QUESTION = {"earnings_step_up": {
    "type": "noul",
    "instructions": ("Within the next four quarterly reports after 2026-10-12, will recurring consolidated "
                     "operating income rise materially (at least 15% year over year) for two consecutive "
                     "reported quarters, driven by AI-related EUV/DUV demand rather than one-offs or acquisitions?"),
    "criteria": {"true": "The step-up happens within the horizon as defined.",
                 "false": "It does not happen within the horizon, or only through one-offs/acquisitions."},
}}


def main():
    log = {"run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "requested_model": "jev-latest"}
    r1 = system_one(NEUTRAL_STATE, NEUTRAL_Q)
    log["neutral"] = {"request": {"state": NEUTRAL_STATE, "questions": NEUTRAL_Q}, "response": r1}
    print("1) Neutral test  model:", r1.get("model"), "| is_urgent:", r1["answers"]["is_urgent"].get("noul"),
          "| usage:", r1.get("usage"))
    r2 = system_one(ASML_STATE, E_QUESTION)
    log["capability_asml"] = {"request": {"state": ASML_STATE, "questions": E_QUESTION}, "response": r2}
    a = r2["answers"]["earnings_step_up"]
    print("2) ASML P(E) test model:", r2.get("model"), "| answer fields:", sorted(a), "| noul:", a.get("noul"),
          "| usage:", r2.get("usage"))
    (HERE / "jev_preflight_log.json").write_text(json.dumps(log, indent=1))
    print("Saved jev_preflight_log.json")


if __name__ == "__main__":
    main()
