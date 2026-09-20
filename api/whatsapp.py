"""The WhatsApp front door.

A scam arrives on WhatsApp. Asking someone to copy it, open a browser, paste it
and read a page is asking them to do four things while they are being rushed,
which is the moment they are least able to. So Pakka is also a number you
forward the message to, and the answer comes back in the same thread.

Meta calls this webhook twice over:

    GET  /whatsapp   once, to verify the endpoint is yours
    POST /whatsapp   every time a message arrives

Nothing here needs a dependency. urllib sends the reply, hmac checks the
signature, and the deployment package stays four files with no install step.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import urllib.error
import urllib.request

from chat import reply_for  # noqa: F401  - re-exported, this is its front door

GRAPH = "https://graph.facebook.com/v21.0"
TIMEOUT = 5


def verify(event: dict, expected: str) -> tuple[int, str]:
    """Meta's one-time handshake: echo the challenge if the token matches."""
    if not expected:
        # An unset token must not mean "accept anything": that would let anyone
        # who finds the URL point their own WhatsApp app at it.
        print("whatsapp: WHATSAPP_VERIFY_TOKEN is not set, refusing verification")
        return 403, "verification not configured"
    q = event.get("queryStringParameters") or {}
    if q.get("hub.mode") == "subscribe" and q.get("hub.verify_token") == expected:
        return 200, str(q.get("hub.challenge", ""))
    return 403, "verification failed"


def signature_ok(body: str, header: str | None, secret: str) -> bool:
    """This endpoint is public, so anything unsigned is a stranger.

    With no app secret configured we cannot check, and refusing everything
    would make the thing impossible to set up, so it passes. Configure the
    secret in production; the README says so in the step where you get it.
    """
    if not secret:
        return True
    if not header or not header.startswith("sha256="):
        return False
    want = hmac.new(secret.encode(), (body or "").encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(want, header.split("=", 1)[1])


def incoming(payload: dict) -> list[dict]:
    """Pull the messages out of Meta's envelope.

    Delivery receipts and read receipts arrive on the same webhook and carry no
    messages at all, so most calls legitimately yield nothing.
    """
    out = []
    for entry in payload.get("entry") or []:
        for change in entry.get("changes") or []:
            value = change.get("value") or {}
            for m in value.get("messages") or []:
                kind = m.get("type", "text")
                out.append({
                    "from": m.get("from", ""),
                    "id": m.get("id", ""),
                    "type": kind,
                    "text": (m.get("text") or {}).get("body", "") if kind == "text" else "",
                    "phone_number_id": (value.get("metadata") or {}).get("phone_number_id", ""),
                })
    return out


def send(to: str, text: str, phone_number_id: str = "", token: str = "") -> bool:
    """Post the reply back. A failure here is logged and swallowed: Meta retries
    a webhook that does not return 200, and a retry would re-scan the message
    and send the answer twice."""
    token = token or os.environ.get("WHATSAPP_TOKEN", "")
    phone_number_id = phone_number_id or os.environ.get("WHATSAPP_PHONE_ID", "")
    if not token or not phone_number_id:
        print("whatsapp: no token or phone id configured, not sending")
        return False
    body = json.dumps({
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }).encode()
    req = urllib.request.Request(
        f"{GRAPH}/{phone_number_id}/messages", data=body, method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return 200 <= r.status < 300
    except urllib.error.HTTPError as e:
        print(f"whatsapp: graph returned {e.code}: {e.read()[:300]!r}")
    except Exception as e:  # noqa: BLE001 - a send failure must not retry the scan
        print(f"whatsapp: send failed: {type(e).__name__}: {e}")
    return False
