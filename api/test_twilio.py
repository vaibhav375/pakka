"""Run with: python3 api/test_twilio.py"""
import sys, pathlib, base64, hmac, hashlib, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import twilio, chat
from rules import evaluate
from advice import build as build_advice

TOKEN = "twilio-auth-token-abc"
URL = "https://example.lambda-url.ap-south-1.on.aws/twilio"


def form(text, frm="whatsapp:+919812345670", num_media="0"):
    return {"From": frm, "To": "whatsapp:+14155238886", "Body": text,
            "MessageSid": "SM123", "NumMedia": num_media}


def encode(params):
    return urllib.parse.urlencode(params)


def sign(url, params, token=TOKEN):
    data = url + "".join(k + params[k] for k in sorted(params))
    return base64.b64encode(hmac.new(token.encode(), data.encode(), hashlib.sha1).digest()).decode()


def check(name, got, want):
    ok = got == want
    print(f"  {'pass' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"        got:  {got!r}\n        want: {want!r}")
    return 0 if ok else 1


def main() -> int:
    bad = 0
    p = form("hello")

    bad += check("a correct signature passes",
                 twilio.signature_ok(URL, p, sign(URL, p), TOKEN), True)
    bad += check("a tampered body fails",
                 twilio.signature_ok(URL, form("goodbye"), sign(URL, p), TOKEN), False)
    bad += check("a different url fails",
                 twilio.signature_ok(URL + "x", p, sign(URL, p), TOKEN), False)
    bad += check("a missing signature fails when a token is set",
                 twilio.signature_ok(URL, p, None, TOKEN), False)
    bad += check("no token configured means no check",
                 twilio.signature_ok(URL, p, None, ""), True)

    ev = {"body": encode(p), "headers": {"content-type": "application/x-www-form-urlencoded"}}
    bad += check("form encoded body is read",
                 [(m["from"], m["text"]) for m in twilio.incoming(twilio.params(ev))],
                 [("whatsapp:+919812345670", "hello")])
    b64 = {"body": base64.b64encode(encode(p).encode()).decode(), "isBase64Encoded": True}
    bad += check("a base64 body is decoded first",
                 twilio.params(b64)["Body"], "hello")
    bad += check("an image is a message with no text",
                 [(m["type"], m["text"]) for m in
                  twilio.incoming(twilio.params({"body": encode(form("", num_media="1"))}))],
                 [("media", "")])

    x = twilio.twiml('5 < 6 & "quoted"')
    bad += check("the reply is TwiML", x.startswith("<?xml"), True)
    bad += check("and escapes what XML cannot carry", "&lt;" in x and "&amp;" in x, True)

    import handler
    ev = {"requestContext": {"http": {"method": "POST"}}, "rawPath": "/twilio",
          "headers": {"host": "example.lambda-url.ap-south-1.on.aws"},
          "body": encode(form("Your KYC has expired, share OTP now"))}
    res = handler.twilio_webhook(ev)
    bad += check("the webhook answers 200", res["statusCode"], 200)
    bad += check("as xml", res["headers"]["content-type"], "text/xml; charset=utf-8")
    bad += check("with the verdict in the body", "scam" in res["body"].lower(), True)

    res = handler.twilio_webhook({"rawPath": "/twilio", "headers": {},
                                  "body": encode(form("/start"))})
    bad += check("an empty delivery callback is harmless",
                 handler.twilio_webhook({"rawPath": "/twilio", "headers": {},
                                         "body": "MessageStatus=delivered"})["statusCode"], 200)

    import os
    os.environ["TWILIO_AUTH_TOKEN"] = TOKEN
    ev2 = {"rawPath": "/twilio", "headers": {"host": "example.lambda-url.ap-south-1.on.aws"},
           "body": encode(p)}
    bad += check("an unsigned request is refused",
                 handler.twilio_webhook(ev2)["statusCode"], 403)
    ev2["headers"]["X-Twilio-Signature"] = sign(URL, p)
    bad += check("a signed one is accepted",
                 handler.twilio_webhook(ev2)["statusCode"], 200)
    del os.environ["TWILIO_AUTH_TOKEN"]

    print(f"\n  {'all tests passed' if not bad else f'{bad} FAILED'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
