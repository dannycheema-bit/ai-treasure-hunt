"""Minimal client for TypeSafe's official HTTP API (POST /v1/systemone), stdlib only.

The API key is read from the TYPESAFE_API_KEY environment variable or, failing that, from the
repo-root .env file (git-ignored). The key is never printed, logged or written anywhere else.
Docs: https://docs.typesafe.ai/api
"""
import json, os, time, urllib.error, urllib.request
from pathlib import Path

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
REPO = Path(__file__).resolve().parents[2]


def api_key():
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key and (REPO / ".env").exists():
        for line in (REPO / ".env").read_text().splitlines():
            if line.startswith("TYPESAFE_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        raise SystemExit("TYPESAFE_API_KEY not set (environment or ~/ai-treasure-hunt/.env).")
    return key


def system_one(state, questions, model="jev-latest", retries=3):
    body = json.dumps({"state": state, "model": model, "questions": questions}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
        "Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            raise SystemExit(f"TypeSafe API error {e.code}: {detail}")
