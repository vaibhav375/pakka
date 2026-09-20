"""Run with: python3 api/test_telegram.py"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import telegram, chat
from rules import evaluate
from advice import build as build_advice

SECRET = "hook-secret-xyz"


def update(text, chat_id=4242):
    return {"update_id": 1, "message": {
        "message_id": 9, "from": {"id": chat_id, "first_name": "V"},
        "chat": {"id": chat_id, "type": "private"}, "text": text}}


def check(name, got, want):
    ok = got == want
    print(f"  {'pass' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"        got:  {got!r}\n        want: {want!r}")
    return 0 if ok else 1


def main() -> int:
    bad = 0

    bad += check("the right secret header passes",
                 telegram.secret_ok({"x-telegram-bot-api-secret-token": SECRET}, SECRET), True)
    bad += check("a wrong one fails",
                 telegram.secret_ok({"x-telegram-bot-api-secret-token": "no"}, SECRET), False)
    bad += check("a missing one fails",
                 telegram.secret_ok({}, SECRET), False)
    bad += check("no secret configured means no check",
                 telegram.secret_ok({}, ""), True)

    m = telegram.incoming(update("hello"))
    bad += check("a text message is read", [(x["chat_id"], x["text"]) for x in m],
                 [(4242, "hello")])
    bad += check("an edited message is read too",
                 [x["text"] for x in telegram.incoming(
                     {"edited_message": {"chat": {"id": 1}, "text": "again"}})], ["again"])
    bad += check("a photo is a message with no text",
                 [(x["type"], x["text"]) for x in telegram.incoming(
                     {"message": {"chat": {"id": 1}, "photo": [{"file_id": "a"}]}})],
                 [("photo", "")])
    bad += check("an unrelated update yields nothing",
                 telegram.incoming({"poll_answer": {}}), [])
    bad += check("/start is recognised as the first hello",
                 telegram.is_start("/start"), True)
    bad += check("and a normal message is not", telegram.is_start("hello"), False)
    bad += check("the welcome explains what to do",
                 "forward" in telegram.WELCOME.lower(), True)

    text = ("Dear customer your KYC has expired. Click http://sbi-verify-kyc.xyz "
            "and share OTP with our executive to reactivate within 2 hours.")
    v = evaluate(text)
    reply = chat.reply_for(v, build_advice(v), "https://pakka.example/v/abc")
    bad += check("the verdict leads", reply.splitlines()[0].startswith("Almost certainly"), True)
    bad += check("it fits one telegram message", len(reply) <= 4096, True)

    import handler
    sent = []
    ev = {"requestContext": {"http": {"method": "POST"}}, "rawPath": "/telegram",
          "headers": {}, "body": json.dumps(update("Your KYC has expired, share OTP now"))}
    res = handler.telegram_webhook(ev, send=lambda cid, t: sent.append((cid, t)))
    bad += check("the webhook answers 200", res["statusCode"], 200)
    bad += check("one reply goes back to that chat",
                 [(c, "scam" in t.lower()) for c, t in sent], [(4242, True)])

    sent.clear()
    res = handler.telegram_webhook(
        {"headers": {}, "body": json.dumps(update("/start"))},
        send=lambda cid, t: sent.append((cid, t)))
    bad += check("/start gets the welcome, not a verdict",
                 sent[0][1] == telegram.WELCOME, True)

    import os
    os.environ["TELEGRAM_SECRET"] = SECRET
    sent.clear()
    res = handler.telegram_webhook({"headers": {}, "body": json.dumps(update("hi"))},
                                   send=lambda cid, t: sent.append((cid, t)))
    bad += check("an unsigned request is refused", (res["statusCode"], len(sent)), (403, 0))
    res = handler.telegram_webhook(
        {"headers": {"X-Telegram-Bot-Api-Secret-Token": SECRET},
         "body": json.dumps(update("hi"))}, send=lambda cid, t: sent.append((cid, t)))
    bad += check("a signed one is accepted", res["statusCode"], 200)
    del os.environ["TELEGRAM_SECRET"]

    print(f"\n  {'all tests passed' if not bad else f'{bad} FAILED'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
