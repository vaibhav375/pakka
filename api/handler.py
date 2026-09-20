"""One Lambda, two routes.

POST /scan      a message in, a verdict out, saved so it can be linked to
GET  /v/{id}    that saved verdict, for the person you forwarded it to

The same function object serves the local development server, so what runs on
a laptop is the code that runs in production rather than a sibling of it.
"""
from __future__ import annotations

import decimal
import json
import sys
import traceback
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import store
from rules import evaluate

MAX_CHARS = 4000
CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "content-type",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
}


def _plain(value):
    """DynamoDB hands numbers back as Decimal, which json.dumps refuses. Every
    number in a scan is a count, an offset or a score, so integers are the
    honest representation."""
    if isinstance(value, decimal.Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    raise TypeError(f"cannot serialise {type(value).__name__}")


def _reply(status: int, body: dict) -> dict:
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json", **CORS},
        "body": json.dumps(body, default=_plain),
    }


def scan(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return _reply(400, {"error": "Paste a message first."})
    if len(text) > MAX_CHARS:
        return _reply(413, {"error": f"That is longer than {MAX_CHARS} characters."})

    verdict = evaluate(text)
    scan_id = store.new_id()
    record = {"text": text, **verdict}
    try:
        store.put(scan_id, record)
    except Exception:
        # a storage failure must not cost the user their answer
        scan_id = None
    return _reply(200, {**record, "id": scan_id})


def lambda_handler(event, context=None):
    """A crash here becomes a bare 502 with an empty body, which tells the
    caller nothing and tells the developer less. Catch it, log it, and answer
    in the same JSON shape as everything else."""
    try:
        return _route(event)
    except Exception as exc:  # noqa: BLE001 - last line before a 502
        traceback.print_exc()
        return _reply(500, {"error": "Something broke handling that.",
                            "detail": f"{type(exc).__name__}: {exc}"[:300]})


def _route(event):
    method = (event.get("requestContext", {}).get("http", {}).get("method")
              or event.get("httpMethod") or "GET").upper()
    path = (event.get("rawPath") or event.get("path") or "/")

    if method == "OPTIONS":
        return {"statusCode": 204, "headers": CORS, "body": ""}

    if method == "POST" and path.rstrip("/").endswith("/scan"):
        try:
            body = json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            return _reply(400, {"error": "Body must be JSON."})
        return scan(body.get("text", ""))

    if method == "GET" and "/v/" in path:
        try:
            record = store.get(path.rsplit("/v/", 1)[1].strip("/"))
        except Exception:
            return _reply(503, {"error": "Saved scans are unavailable right now."})
        if not record:
            return _reply(404, {"error": "No scan with that link."})
        return _reply(200, record)

    if method == "GET":
        return _reply(200, {"ok": True, "rules": evaluate("")["rules_checked"]})

    return _reply(405, {"error": "Method not allowed."})
