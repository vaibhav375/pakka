"""Run with: python3 api/test_llm.py

The Bedrock call is stubbed throughout, so this runs with no AWS account, no
boto3 and no network. What is being tested is the part that matters: that a
model can raise a verdict and never lower one, and that nothing it says is
shown unless it quotes the message.
"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import llm
from rules import evaluate

# Deliberately a message no rule has an opinion about: no reward framing, no
# link, no secret asked for, nothing to quote. This is the whole bucket the
# Bedrock check exists for, and the reason it cannot be a rule.
CLEAN = "Respected sir, your file is ready at our end. Please do the needful today itself."
DIRTY = "Share your OTP now or your account will be blocked today."


def said(obj) -> str:
    """What converse() hands back, trimmed to the one field that is read."""
    return json.dumps(obj) if not isinstance(obj, str) else obj


def stub(answer):
    """Stand in for the Bedrock client. Records the call so the test can check
    what was sent, and the prompt the message was put in."""
    sent = {}

    class Client:
        def converse(self, **kw):
            sent.update(kw)
            return {"output": {"message": {"content": [{"text": said(answer)}]}}}

    llm._CLIENT = Client()
    return sent


def check(name, got, want):
    ok = got == want
    print(f"  {'pass' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"        got:  {got!r}\n        want: {want!r}")
    return 0 if ok else 1


def main() -> int:
    bad = 0
    llm.MODEL_ID = "stub-model"

    # --- when it is called at all
    bad += check("a message the rules carry is not sent anywhere",
                 llm.wanted(evaluate(DIRTY)), False)
    bad += check("a message the rules found nothing in is",
                 llm.wanted(evaluate(CLEAN)), True)
    llm.MODEL_ID = None
    bad += check("with no model configured, nothing is ever sent",
                 llm.wanted(evaluate(CLEAN)), False)
    llm.MODEL_ID = "stub-model"

    # --- the call itself
    sent = stub({"concern": True, "quote": "do the needful",
                 "reason": "It presses you to act without saying what for."})
    got = llm.check(CLEAN)
    bad += check("the quoted phrase comes back with its position",
                 got["quotes"], ["do the needful"])
    bad += check("the span points at those characters",
                 CLEAN[got["spans"][0][0]:got["spans"][0][1]], "do the needful")
    bad += check("maxTokens is set explicitly, never left to the default",
                 sent["inferenceConfig"]["maxTokens"], 300)
    bad += check("the message is sent as the user turn, not inside the system prompt",
                 sent["messages"][0]["content"][0]["text"], CLEAN)

    # --- everything it says that cannot be shown
    stub({"concern": True, "quote": "a phrase that is not there", "reason": "x"})
    bad += check("a quote that is not in the message is dropped",
                 llm.check(CLEAN), None)
    stub({"concern": False, "quote": "", "reason": "looks fine to me"})
    bad += check("a clean opinion is not a finding",
                 llm.check(CLEAN), None)
    stub("I reckon this one is a scam")
    bad += check("an answer that is not JSON is dropped",
                 llm.check(CLEAN), None)
    stub({"concern": True, "quote": 42, "reason": None})
    bad += check("wrong types are dropped",
                 llm.check(CLEAN), None)

    class Broken:
        def converse(self, **kw):
            raise RuntimeError("bedrock is having a day")
    llm._CLIENT = Broken()
    bad += check("a failing call costs nothing but the call",
                 llm.check(CLEAN), None)

    # --- the band: up to careful, never past it, never down
    concern = {"reason": "r", "spans": [[0, 4]], "quotes": ["Your"]}
    clean = evaluate(CLEAN)
    raised = llm.raise_band(clean, concern)
    bad += check("a clean message can be raised to careful",
                 (clean["band"], raised["band"]), ("clear", "careful"))
    bad += check("the score stays the rules' score, so it stays reproducible",
                 raised["score"], clean["score"])
    bad += check("the reader is told which layer spoke",
                 raised["raised_by"], "llm")
    bad += check("with no concern the verdict is untouched",
                 llm.raise_band(clean, None), clean)

    dirty = evaluate(DIRTY)
    bad += check("a verdict the rules carry is never lowered",
                 llm.raise_band(dirty, concern), dirty)

    # the one failure that actually costs somebody money, asserted directly
    worst = evaluate("Pay Rs 8,400 immediately or we will share your photos with everyone.")
    bad += check("a scam the rules caught cannot be cleared by the model",
                 llm.raise_band(worst, None)["band"], worst["band"])

    print(f"\n  {'all tests passed' if not bad else f'{bad} FAILED'}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
