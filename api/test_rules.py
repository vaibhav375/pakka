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

    ("prize bait with a QR code",
     "Dear customer, congratulations on winning a new mac book air. Share your "
     "phone number and scan the given QR code to claim the offer. Click it now "
     "before you lose the offer.",
     {"LOTTERY_WIN", "QR_SCAN", "URGENCY"}),

    ("a legitimate QR, must stay clean",
     "Your order is out for delivery today. Scan the QR on the package to confirm "
     "you received it, or pay the delivery agent by scanning his QR.",
     set()),

    ("remote access tool",
     "Please install AnyDesk and share the 9 digit code so I can help you with the refund.",
     {"REMOTE_ACCESS"}),

    ("apk sideload",
     "Dear customer, download and install this APK to complete your bank verification.",
     {"APK_INSTALL"}),

    ("lookalike domain",
     "Your SBI account will be deactivated. Verify your PAN details at http://sbi-verify-kyc.xyz/login",
     {"KYC_PANIC", "LOOKALIKE_DOMAIN", "VERIFY_DETAILS"}),

    ("id document harvesting",
     "Send a photo of your Aadhaar card and PAN card for verification.",
     {"ID_DOCUMENTS"}),

    ("mobile number as official helpline",
     "For any complaint call our customer care 9876543210. We are the official helpline.",
     {"CALLBACK_NUMBER"}),

    ("money in, which is not how it works",
     "Rs 5000 has been credited to your wallet. Click here to withdraw the amount.",
     {"COLLECT_REQUEST"}),

    ("upi collect request",
     "Your friend sent you money. Accept the request on your UPI app to receive Rs 2000.",
     {"COLLECT_REQUEST"}),

    ("pig butchering opener",
     "Hi, I got your number from a mutual friend. I am Sophia, I trade crypto and make good profit daily.",
     {"STRANGER_OPENER"}),

    ("advance fee",
     "Hello dear, I am Mrs Grace, a widow with 10 million dollars to donate to a trustworthy person.",
     {"ADVANCE_FEE"}),

    ("bank details to receive a refund",
     "Your income tax refund of Rs 15,490 is approved. Submit your bank account number to receive it.",
     {"BANK_DETAILS"}),

    ("sim block scare",
     "Your SIM card will be blocked in 24 hours. Update your details now.",
     {"SIM_BLOCK", "URGENCY", "VERIFY_DETAILS"}),

    ("stranded plea",
     "I need your help, I am stuck in Dubai and lost my wallet. Please send money.",
     {"STRANDED_PLEA"}),

    ("a real OTP message, must stay clean",
     "Your OTP is 452891. Do not share it with anyone. -SBI",
     set()),

    ("a real tracking link, must stay clean",
     "Hi, your Amazon order has shipped. Track it at https://www.amazon.in/orders",
     set()),

    ("a friend sharing a number, must stay clean",
     "Call me on 9876543210 when you reach the gate, I will come down.",
     set()),

    ("asking for notes, must stay clean",
     "Can you send me a photo of your notes from today's class?",
     set()),

    ("new number asking for money",
     "Hi mom, this is my new number. My phone broke. Please send Rs 15,000 urgently.",
     {"NEW_NUMBER", "URGENCY"}),

    ("a genuine new number, must stay clean",
     "Hi, this is my new number, please save it. See you Saturday. - Rahul",
     set()),

    ("a payment receipt, must stay clean",
     "Your electricity bill payment of Rs 1,240 was successful. Receipt in the app.",
     set()),

    ("a friend needing your account number, must stay clean",
     "Can you share your bank account number? I need to transfer your share of the trip money.",
     set()),

    ("spaced out to dodge a filter",
     "Your K Y C has expired. Share the O T P received to complete verification.",
     {"KYC_PANIC", "ASKS_FOR_SECRET"}),

    ("a zero standing in for a letter",
     "Send your 0TP immediately to verify your acc0unt",
     {"ASKS_FOR_SECRET", "URGENCY"}),

    ("an accent dropped on a vowel",
     "shäre your otp to complete the transaction",
     {"ASKS_FOR_SECRET"}),

    ("hinglish kyc scare",
     "Aapka KYC update nahi hua hai, account block ho jayega. Turant is link par click kare",
     {"KYC_PANIC", "URGENCY", "BARE_LINK"}),

    ("an emoji does not shift the highlights",
     "Congratulations 🎉 you have W-O-N a lucky draw prize of Rs 10,00,000",
     {"LOTTERY_WIN"}),

    ("a cyrillic letter inside a brand name",
     "Update your account at http://\u0430mazon.in/verify now",
     {"LOOKALIKE_URL", "VERIFY_DETAILS"}),

    ("punycode",
     "Apple ID locked. Sign in at https://xn--80ak6aa92e.com/login to restore it",
     {"LOOKALIKE_URL"}),

    ("a real brand address, must stay clean",
     "Your order at https://www.amazon.in/orders is out for delivery today.",
     set()),

    ("a free gadget and a nameless link",
     "claim your free tablet now by clicking on this link",
     {"LOTTERY_WIN", "URGENCY", "BARE_LINK"}),

    ("a real message that names where it sends you, must stay clean",
     "Your order has shipped. Track it at https://www.amazon.in/orders or in the app.",
     set()),

    ("a bank alarm with the fix behind a link",
     "SBI Bank: Unusual login detected from new device. Secure your account: http://verify-bank119.com",
     {"UNUSUAL_LOGIN"}),

    ("a government payout nobody applied for",
     "PMO India: You are selected for Rs 86,200 grant under the scheme. Call 9812345670 to claim.",
     {"GOVT_GRANT", "CALLBACK_NUMBER"}),

    ("a stranger opening with flattery",
     "Hi beautiful! I saw your profile. Want to chat? Reply YES to 9409249465",
     {"ROMANCE_BAIT"}),

    ("a brand name on a domain that is not theirs",
     "Myntra: Exclusive 70% discount for you only! Shop now: http://myntra-fashion507.in",
     {"LOOKALIKE_DOMAIN"}),

    ("selected with no interview",
     "Congratulations, you are selected without interview for the data entry post.",
     {"NO_INTERVIEW"}),

    ("account details to release a refund",
     "Your refund of Rs 4,999 is approved. Share your bank account number and IFSC to receive it.",
     {"BANK_DETAILS"}),

    ("devanagari kyc scare",
     "आपका केवाईसी अपडेट नहीं हुआ है। खाता ब्लॉक हो जाएगा। तुरंत इस लिंक पर क्लिक करें",
     {"KYC_PANIC", "URGENCY", "BARE_LINK"}),

    ("an ordinary hindi message, must stay clean",
     "नमस्ते, कल मीटिंग सुबह 10 बजे है। कृपया समय पर आएं।",
     set()),

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
