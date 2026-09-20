"""One Lambda, four routes.

POST /scan        a message in, a verdict out, saved so it can be linked to
GET  /v/{id}      that saved verdict, for the person you forwarded it to
GET  /whatsapp    Meta's one-time webhook verification handshake
POST /whatsapp    a message forwarded to the WhatsApp number, answered in the
                  same thread, which is where the scam arrived in the first place

The same function object serves the local development server, so what runs on
a laptop is the code that runs in production rather than a sibling of it.
"""
from __future__ import annotations

import decimal
import json
import os
import sys
import traceback
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import store
import whatsapp
from advice import build as build_advice
from rules import evaluate

MAX_CHARS = 4000
PUBLIC_URL = os.environ.get("PAKKA_PUBLIC_URL", "").rstrip("/")

# A Lambda Function URL with CORS configured adds these itself. Sending them
# from here as well produces "Access-Control-Allow-Origin: *, *", which every
# browser rejects outright -- the API works from curl and fails in the page.
# So the code only supplies them when it is not running inside Lambda, which
# is exactly the local Build It path.
IN_LAMBDA = bool(os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
CORS = {} if IN_LAMBDA else {
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
    record = {"text": text, **verdict, "advice": build_advice(verdict)}
    scan_id = store.new_id()
    try:
        store.put(scan_id, record)
    except Exception:
        # a storage failure must not cost the user their answer
        scan_id = None
    return _reply(200, {**record, "id": scan_id})


def _verdict_for(text: str) -> tuple[dict, dict, str | None]:
    """The scan, the advice, and a link to it, shared by every front door."""
    verdict = evaluate(text)
    advice = build_advice(verdict)
    link = None
    try:
        scan_id = store.new_id()
        store.put(scan_id, {"text": text, **verdict, "advice": advice})
        link = f"{PUBLIC_URL}/v/{scan_id}" if PUBLIC_URL else None
    except Exception:
        traceback.print_exc()          # a storage failure must not cost the answer
    return verdict, advice, link


def whatsapp_webhook(event, send=whatsapp.send) -> dict:
    """Answer every message in the payload, then return 200 no matter what.

    Meta retries any webhook that does not return 200, and a retry would scan
    the message again and send a second answer, so a failure inside the loop is
    logged and swallowed rather than surfaced as an error status.
    """
    body = event.get("body") or ""
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    secret = os.environ.get("WHATSAPP_APP_SECRET", "")
    if not whatsapp.signature_ok(body, headers.get("x-hub-signature-256"), secret):
        print("whatsapp: rejected an unsigned or badly signed request")
        return {"statusCode": 403, "body": "bad signature"}

    try:
        payload = json.loads(body or "{}")
    except json.JSONDecodeError:
        return {"statusCode": 200, "body": "ignored"}

    for msg in whatsapp.incoming(payload):
        try:
            text = (msg["text"] or "").strip()[:MAX_CHARS]
            if msg["type"] != "text" or not text:
                send(msg["from"], whatsapp.reply_for(None, None, None, kind=msg["type"]),
                     msg["phone_number_id"])
                continue
            verdict, advice, link = _verdict_for(text)
            send(msg["from"], whatsapp.reply_for(verdict, advice, link),
                 msg["phone_number_id"])
        except Exception:               # one bad message must not drop the rest
            traceback.print_exc()
    return {"statusCode": 200, "body": "ok"}


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

    if path.rstrip("/").endswith("/whatsapp"):
        if method == "GET":
            status, text = whatsapp.verify(event, os.environ.get("WHATSAPP_VERIFY_TOKEN", ""))
            return {"statusCode": status, "headers": {"content-type": "text/plain"},
                    "body": text}
        if method == "POST":
            return whatsapp_webhook(event)
        return _reply(405, {"error": "Method not allowed."})

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
