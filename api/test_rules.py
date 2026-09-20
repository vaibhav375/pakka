"""Run with: python3 api/test_rules.py

Stdlib only, so anyone who clones this can run the tests without installing
anything. The last case matters most: an ordinary message has to come back
clean, or the tool cries wolf and nobody listens to it.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from rules import evaluate, RULES

CASES = [
    ("fake internship",
     "Congratulations! You have been selected without interview for Data Entry. "
     "Pay registration fee of Rs 2000 within 2 hours to confirm your seat. "
     "Contact us only on WhatsApp.",
     {"PAY_TO_GET_JOB", "NO_INTERVIEW", "URGENCY", "CHAT_ONLY"}),

    ("kyc phishing",
     "Dear customer, your KYC has expired and your account will be blocked today. "
     "Update immediately at bit.ly/kyc-fix or share OTP with our executive.",
     {"KYC_PANIC", "URGENCY", "HIDDEN_LINK", "ASKS_FOR_SECRET"}),

    ("fake pg listing",
     "2BHK near PES, fully furnished, 8000/month. I am currently abroad so please "
     "transfer the token amount to 9876543210 on google pay to block the room.",
     {"SIGHT_UNSEEN", "PERSONAL_PAYMENT"}),

    ("refund bait",
     "Your order was cancelled. Pay Rs 99 processing charge to claim your refund of Rs 4,999.",
     {"PAY_TO_RECEIVE"}),

    ("ordinary message, must stay clean",
     "Hi Vaibhav, this is Priya from the placement cell. Your Infosys interview is "
     "on Monday at 10am in Seminar Hall 2. Please carry two copies of your resume.",
     set()),
]

def main() -> int:
    failed = 0
    for name, text, expected in CASES:
        got = {f["id"] for f in evaluate(text)["findings"]}
        missing, extra = expected - got, got - expected
        ok = not missing and not extra
        failed += not ok
        print(f"  {'pass' if ok else 'FAIL'}  {name:<34} score={evaluate(text)['score']}")
        if missing: print(f"        expected but not found: {sorted(missing)}")
        if extra:   print(f"        fired unexpectedly:     {sorted(extra)}")
    # a rule that can never fire is worse than no rule
    dead = [r.id for r in RULES if not any(r.spans(t) for _, t, _ in CASES)]
    print(f"\n  {len(RULES)} rules, {len(RULES)-len(dead)} exercised by tests")
    print(f"  {'all tests passed' if not failed else str(failed) + ' FAILED'}")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
