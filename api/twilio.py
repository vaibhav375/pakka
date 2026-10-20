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
import urllib.error
import urllib.parse
import urllib.request

MAX_BODY = 1500      # WhatsApp shows about 1600 characters before it truncates
MAX_PICTURE = 3_500_000
TIMEOUT = 5          # the reading still has to happen inside the same request


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
    """One message per call, or none at all for a delivery callback.

    A picture wins over a caption. Somebody forwarding a screenshot usually
    types something above it — "dekho ye aaya hai" — and those are their own
    words, not the scam. The caption is kept as a fallback for when the
    picture cannot be read at all.
    """
    if "From" not in form or "Body" not in form:
        return []
    text = form.get("Body", "")
    try:
        count = int((form.get("NumMedia") or "0").strip() or 0)
    except ValueError:
        count = 0
    has_media = count > 0
    kind = "text"
    if has_media:
        kind = ("photo" if (form.get("MediaContentType0") or "").lower()
                .startswith("image/") else "media")
    return [{"from": form["From"],
             "type": kind,
             "text": "" if has_media else text,
             "caption": text if has_media else "",
             "media_url": form.get("MediaUrl0", "") if has_media else "",
             "media_type": (form.get("MediaContentType0") or "").lower()
             if has_media else ""}]


def _is_twilio(url: str) -> bool:
    """Twilio's own host, over HTTPS, and nothing else.

    The URL arrives inside the request body. With no auth token configured the
    signature check passes everything, so an unchecked URL here would be a
    request this function makes on a stranger's behalf with credentials
    attached. "evil-twilio.com" does not end in ".twilio.com".
    """
    parts = urllib.parse.urlsplit(url)
    return (parts.scheme == "https"
            and (parts.hostname or "").lower().endswith(".twilio.com"))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Twilio answers a media request with a redirect to a signed CDN URL.
    Following it automatically would carry the Authorization header along,
    handing the account token to whoever the CDN is."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(media_url: str, media_type: str = "", sid: str = "",
          token: str = "") -> tuple[bytes, str] | None:
    """Download a picture sent to the sandbox. None on anything at all."""
    sid = sid or os.environ.get("TWILIO_ACCOUNT_SID", "")
    token = token or os.environ.get("TWILIO_AUTH_TOKEN", "")
    if not media_url or not sid or not token:
        return None
    if not _is_twilio(media_url):
        print("twilio: refused to fetch media from a host that is not Twilio's")
        return None
    auth = base64.b64encode(f"{sid}:{token}".encode()).decode()
    try:
        req = urllib.request.Request(
            media_url, headers={"Authorization": f"Basic {auth}"})
        opener = urllib.request.build_opener(_NoRedirect)
        try:
            with opener.open(req, timeout=TIMEOUT) as r:
                raw, got = r.read(MAX_PICTURE + 1), r.headers.get("content-type", "")
        except urllib.error.HTTPError as e:
            if e.code not in (301, 302, 303, 307, 308):
                raise
            # the credentials stop here: the URL Twilio points at is already
            # signed and needs none, and sending them on would leak the token
            nxt = e.headers.get("Location", "")
            if not nxt.startswith("https://"):
                return None
            with urllib.request.urlopen(nxt, timeout=TIMEOUT) as r:
                raw, got = r.read(MAX_PICTURE + 1), r.headers.get("content-type", "")
        if not raw or len(raw) > MAX_PICTURE:
            return None
        return raw, (media_type or got or "").split(";")[0].strip().lower()
    except Exception as e:  # noqa: BLE001 - a failed download is not a crash
        print(f"twilio: could not fetch the picture: {type(e).__name__}: {e}")
        return None


def twiml(text: str) -> str:
    """The reply, carried back in the response Twilio is already waiting on."""
    safe = (text[:MAX_BODY].replace("&", "&amp;")
                           .replace("<", "&lt;")
                           .replace(">", "&gt;"))
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            f"<Response><Message>{safe}</Message></Response>")
