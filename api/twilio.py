"""WhatsApp through Twilio's sandbox.

Meta's own Cloud API needs a business account and an app review, and the
dashboard is frequently unreachable depending on where you are. Twilio's
WhatsApp sandbox needs neither: you send a join code to their number and you
have a working WhatsApp bot in about five minutes.

It is also simpler in a way that matters here. Twilio takes the reply from the
body of the HTTP response, as TwiML, so there is no outbound API call, no
access token to keep, and no second request that can fail after the scan has
already been done.

    POST /twilio   a WhatsApp message, answered in the response itself

Nothing here needs a dependency. The name is unfortunate: this module is not
the `twilio` package from PyPI and deliberately does not use it.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import urllib.parse

MAX_BODY = 1500      # WhatsApp shows about 1600 characters before it truncates


def params(event: dict) -> dict[str, str]:
    """Twilio posts form encoded, and a Function URL may hand it over base64."""
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8", "replace")
    return {k: v[-1] for k, v in urllib.parse.parse_qs(body, keep_blank_values=True).items()}


def callback_url(event: dict) -> str:
    """The URL Twilio signed, which has to match byte for byte.

    A proxy can rewrite the host, so TWILIO_WEBHOOK_URL wins when it is set.
    """
    configured = os.environ.get("TWILIO_WEBHOOK_URL", "").strip()
    if configured:
        return configured
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    host = headers.get("host", "")
    path = event.get("rawPath") or event.get("path") or "/twilio"
    return f"https://{host}{path}"


def signature_ok(url: str, form: dict, header: str | None, token: str) -> bool:
    """Twilio signs the URL followed by every parameter in sorted key order.

    With no auth token configured we cannot check, and refusing everything
    would make the sandbox impossible to set up, so it passes. Set one in
    production; the README sets it in the same step where you copy it.
    """
    if not token:
        return True
    if not header:
        return False
    data = url + "".join(k + form[k] for k in sorted(form))
    want = base64.b64encode(
        hmac.new(token.encode(), data.encode(), hashlib.sha1).digest()).decode()
    return hmac.compare_digest(want, header)


def incoming(form: dict) -> list[dict]:
    """One message per call, or none at all for a delivery callback."""
    if "From" not in form or "Body" not in form:
        return []
    text = form.get("Body", "")
    media = (form.get("NumMedia") or "0").strip()
    kind = "media" if media not in ("", "0") and not text.strip() else "text"
    return [{"from": form["From"], "type": kind,
             "text": text if kind == "text" else ""}]


def twiml(text: str) -> str:
    """The reply, carried back in the response Twilio is already waiting on."""
    safe = (text[:MAX_BODY].replace("&", "&amp;")
                           .replace("<", "&lt;")
                           .replace(">", "&gt;"))
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            f"<Response><Message>{safe}</Message></Response>")
