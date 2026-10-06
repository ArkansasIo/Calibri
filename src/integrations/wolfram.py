"""Wolfram|Alpha / Wolfram Language integration boundary.

Wolfram|Alpha API access is credentialed; CALIBRI never hard-codes an App ID.
For offline mathematics, callers can still use the local math subsystem.
"""

from __future__ import annotations

import os
import urllib.parse
import urllib.request

API_URL = "https://api.wolframalpha.com/v2/query"

def configured() -> bool:
    return bool(os.environ.get("WOLFRAM_APP_ID"))

def query(question: str) -> str:
    app_id = os.environ.get("WOLFRAM_APP_ID")
    if not app_id:
        raise RuntimeError("Set WOLFRAM_APP_ID to use the Wolfram|Alpha API.")
    params = urllib.parse.urlencode({
        "appid": app_id, "input": question, "output": "json", "format": "plaintext"
    })
    with urllib.request.urlopen(f"{API_URL}?{params}", timeout=30) as response:
        return response.read().decode("utf-8")
