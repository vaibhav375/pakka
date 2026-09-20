"""Run with: python3 api/test_whatsapp.py

The webhook is a public endpoint that anyone on the internet can POST to, so
the signature check gets as much attention here as the reply formatting.
"""
import sys, pathlib, json, hmac, hashlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import whatsapp, chat
from rules import evaluate
from advice import build as build_advice

SECRET = "app-secret-123"


def envelope(text: str, wa_id: str = "919812345670") -> dict:
    """The shape Meta actually posts, trimmed to what we read."""
    return {"object": "whatsapp_business_account", "entry": [{"changes": [{"value": {
        "messaging_product": "whatsapp",
        "metadata": {"phone_number_id": "1234"},
        "messages": [{"from": wa_id, "id": "wamid.X", "type": "text",
                      "text": {"body": text}}],
    }}]}]}


def check(name, got, want):
    ok = got == want
    print(f"  {'pass' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"        got:  {got!r}\n        want: {want!r}")
    return 0 if ok else 1


def main() -> int:
    bad = 0

    # --- webhook verification handshake
    ev = {"queryStringParameters": {"hub.mode": "subscribe",
                                    "hub.verify_token": "tok",
                                    "hub.challenge": "9988"}}
    bad += check("verification returns the challenge",
                 whatsapp.verify(ev, "tok"), (200, "9988"))
    bad += check("verification rejects a wrong token",
                 whatsapp.verify(ev, "other")[0], 403)
    bad += check("verification refuses when no token is configured",
                 whatsapp.verify(ev, "")[0], 403)

    # --- signature
    body = json.dumps(envelope("hi"))
    sig = "sha256=" + hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
    bad += check("a correct signature passes",
                 whatsapp.signature_ok(body, sig, SECRET), True)
    bad += check("a tampered body fails",
                 whatsapp.signature_ok(body + " ", sig, SECRET), False)
    bad += check("a missing signature fails when a secret is set",
                 whatsapp.signature_ok(body, None, SECRET), False)
    bad += check("no secret configured means no signature check",
                 whatsapp.signature_ok(body, None, ""), True)

    # --- parsing
    msgs = whatsapp.incoming(json.loads(body))
    bad += check("one text message is read", [(m["from"], m["text"]) for m in msgs],
                 [("919812345670", "hi")])
    bad += check("a status callback yields nothing",
                 whatsapp.incoming({"entry": [{"changes": [{"value": {"statuses": [{}]}}]}]}), [])
    img = {"entry": [{"changes": [{"value": {"messages": [
        {"from": "91", "type": "image", "image": {"id": "x"}}]}}]}]}
    bad += check("a photo is read as a message with no text",
                 [(m["type"], m["text"]) for m in whatsapp.incoming(img)], [("image", "")])

    # --- the reply a person actually receives
    text = ("Dear customer your KYC has expired. Click http://sbi-verify-kyc.xyz "
            "and share OTP with our executive to reactivate within 2 hours.")
    v = evaluate(text)
    reply = chat.reply_for(v, build_advice(v), "https://pakka.example/v/abc")
    bad += check("the verdict leads", reply.splitlines()[0].startswith("Almost certainly a scam"), True)
    bad += check("it names a rule", "Asks for an OTP" in reply, True)
    bad += check("it quotes the words", '"share OTP"' in reply, True)
    bad += check("it says what to do", "1930" in reply, True)
    bad += check("it carries the link", "pakka.example/v/abc" in reply, True)
    bad += check("it fits in one WhatsApp message", len(reply) <= 4096, True)

    clean = evaluate("Your OTP is 452891. Do not share it with anyone. -SBI")
    creply = chat.reply_for(clean, build_advice(clean), None)
    bad += check("a clean message gets a calm answer",
                 creply.splitlines()[0].startswith("Nothing suspicious"), True)
    bad += check("and is not told to report anything", "1930" not in creply, True)

    empty = chat.reply_for(None, None, None, kind="image")
    bad += check("a photo gets an explanation, not silence",
                 "text" in empty.lower(), True)

    # --- end to end through the real handler, with the network stubbed out
    import handler
    sent = []
    ev = {"requestContext": {"http": {"method": "POST"}}, "rawPath": "/whatsapp",
          "headers": {}, "body": json.dumps(envelope(
              "Your KYC has expired, share OTP now within 2 hours"))}
    res = handler.whatsapp_webhook(ev, send=lambda to, text, pid="": sent.append((to, text)))
    bad += check("the webhook always answers 200", res["statusCode"], 200)
    bad += check("exactly one reply is sent", len(sent), 1)
    bad += check("it goes back to the sender", sent[0][0], "919812345670")
    bad += check("and it carries the verdict", "scam" in sent[0][1].lower(), True)

    sent.clear()
    ev["body"] = json.dumps({"entry": [{"changes": [{"value": {"statuses": [{"id": "x"}]}}]}]})
    res = handler.whatsapp_webhook(ev, send=lambda *a, **k: sent.append(a))
    bad += check("a delivery receipt sends nothing", (res["statusCode"], len(sent)), (200, 0))

    import os
    os.environ["WHATSAPP_APP_SECRET"] = SECRET
    ev["body"] = json.dumps(envelope("hi"))
    res = handler.whatsapp_webhook(ev, send=lambda *a, **k: sent.append(a))
    bad += check("an unsigned request is refused", res["statusCode"], 403)
    ev["headers"] = {"X-Hub-Signature-256": "sha256=" + hmac.new(
        SECRET.encode(), ev["body"].encode(), hashlib.sha256).hexdigest()}
    res = handler.whatsapp_webhook(ev, send=lambda *a, **k: sent.append(a))
    bad += check("a signed one is accepted", res["statusCode"], 200)
    del os.environ["WHATSAPP_APP_SECRET"]

    os.environ["WHATSAPP_VERIFY_TOKEN"] = "tok"
    ev2 = {"requestContext": {"http": {"method": "GET"}}, "rawPath": "/whatsapp",
           "queryStringParameters": {"hub.mode": "subscribe",
                                     "hub.verify_token": "tok", "hub.challenge": "42"}}
    bad += check("the handshake routes through the handler",
                 handler.lambda_handler(ev2)["body"], "42")
    del os.environ["WHATSAPP_VERIFY_TOKEN"]
    bad += check("with no token configured, verification is refused",
                 handler.lambda_handler(ev2)["statusCode"], 403)

    print(f"\n  {'all tests passed' if not bad else f'{bad} FAILED'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
