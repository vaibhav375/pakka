"""The Telegram front door.

Same idea as the WhatsApp one and rather easier to stand up: BotFather hands
you a token in a minute, with no business account, no app review and nothing to
verify. Telegram also matters on its own here, because a good share of the
scams these rules describe are run out of Telegram groups.

    POST /telegram   an update from Telegram, answered in the same chat

Telegram has no signature. Instead you hand it a secret when you register the
webhook and it sends that secret back in a header on every call, which is the
same guarantee by a simpler route.
"""
from __future__ import annotations

import hmac
import json
import os
import urllib.error
import urllib.request

API = "https://api.telegram.org"
TIMEOUT = 5

WELCOME = (
    "Forward me any message you are unsure about and I will tell you what is "
    "wrong with it and why.\n\n"
    "A PG listing, an internship offer, a bank SMS, a KYC warning, anything. I "
    "check it against 47 rules, quote the exact words that are a problem, tell "
    "you what to do next, and write a reply you can send back to whoever "
    "forwarded it to you.\n\n"
    "I am not a model guessing. The same message always gets the same answer."
)


def is_start(text: str) -> bool:
    return (text or "").strip().split("@")[0] in ("/start", "/help")


def secret_ok(headers: dict, secret: str) -> bool:
    """Telegram echoes back the secret you registered with the webhook.

    With none configured we cannot check, and refusing everything would make
    the thing impossible to set up, so it passes. Set one in production; the
    README sets it in the same command that registers the webhook.
    """
    if not secret:
        return True
    got = {k.lower(): v for k, v in (headers or {}).items()}.get(
        "x-telegram-bot-api-secret-token")
    return bool(got) and hmac.compare_digest(got, secret)


def incoming(payload: dict) -> list[dict]:
    """Pull the messages out of an update.

    Telegram sends one update per call, and most of the update types it can
    send are not messages at all, so yielding nothing is normal.
    """
    out = []
    for key in ("message", "edited_message", "channel_post"):
        m = payload.get(key)
        if not m:
            continue
        kind = "text" if "text" in m else next(
            (k for k in ("photo", "voice", "video", "document", "audio", "sticker")
             if k in m), "other")
        out.append({
            "chat_id": (m.get("chat") or {}).get("id"),
            "type": kind,
            "text": m.get("text", "") if kind == "text" else "",
        })
    return out


def send(chat_id, text: str, token: str = "") -> bool:
    """Send the reply. A failure is logged and swallowed, because Telegram
    retries an update that is not acknowledged and a retry would answer
    twice."""
    token = token or os.environ.get("TELEGRAM_TOKEN", "")
    if not token or chat_id is None:
        print("telegram: no token configured, not sending")
        return False
    body = json.dumps({"chat_id": chat_id, "text": text,
                       "disable_web_page_preview": True}).encode()
    req = urllib.request.Request(f"{API}/bot{token}/sendMessage", data=body,
                                 method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return 200 <= r.status < 300
    except urllib.error.HTTPError as e:
        print(f"telegram: api returned {e.code}: {e.read()[:300]!r}")
    except Exception as e:  # noqa: BLE001 - a send failure must not retry the scan
        print(f"telegram: send failed: {type(e).__name__}: {e}")
    return False
