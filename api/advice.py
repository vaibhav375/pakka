"""What to do about it, and what to say back.

A score tells you something is wrong. It does not tell you what to do at ten at
night when a stranger is pressuring you, and it is not something you can send to
the person who forwarded it. Both of those are derived from the rules that fired,
so the advice can never contradict the verdict.
"""
from __future__ import annotations

import hindi

# How each rule reads inside a sentence you would actually send someone.
CLAUSE = {
    "PAY_TO_GET_JOB": "it asks for money before a job",
    "ASKS_FOR_SECRET": "it asks for an OTP or PIN",
    "PAY_TO_RECEIVE": "it wants a payment before releasing money to you",
    "KYC_PANIC": "it uses a KYC or account-block scare",
    "URGENCY": "it pushes you to act within hours",
    "NO_INTERVIEW": "it offers a job with no interview",
    "TOO_GOOD": "the pay does not match the work",
    "PERSONAL_PAYMENT": "the money goes to a personal account",
    "FREE_EMAIL_AS_COMPANY": "a company is writing from a free Gmail address",
    "HIDDEN_LINK": "the link is shortened so you cannot see where it goes",
    "CHAT_ONLY": "it exists only on WhatsApp or Telegram",
    "THREAT": "it threatens legal or police action",
    "SIGHT_UNSEEN": "it wants rent before you have seen the place",
    "COURIER_CUSTOMS": "it wants a fee to release a parcel",
    "ELECTRICITY_CUT": "it threatens to cut your electricity",
    "LOTTERY_WIN": "it claims a prize you never entered for",
    "REMOTE_ACCESS": "it wants to see or control your screen, which no real support desk ever asks for",
    "APK_INSTALL": "it wants you to install an app sent as a file, which nobody has checked",
    "LOOKALIKE_DOMAIN": "the web address only looks like the real company",
    "VERIFY_DETAILS": "it wants your details to stop something bad happening, which is what phishing is",
    "ID_DOCUMENTS": "it asks for your Aadhaar or PAN, which is enough to take a loan in your name",
    "CALLBACK_NUMBER": "the helpline number is a personal mobile, not a company line",
    "COLLECT_REQUEST": "approving a request or entering your PIN sends money out, it cannot bring money in",
    "STRANGER_OPENER": "it is a stranger opening with money talk, which is how these always start",
    "ADVANCE_FEE": "it offers a fortune from a stranger, which does not happen",
    "BANK_DETAILS": "it wants fresh bank details in order to send you money, which is backwards",
    "SIM_BLOCK": "it threatens to block your SIM, which your operator does not do over text",
    "NEW_NUMBER": "it claims a new number and then asks for money, so call the old one first",
    "STRANDED_PLEA": "it is the stranded friend story, so call them on the number you already have",
    "QR_SCAN": "it tells you to scan a QR code to receive something, which is not a thing QR codes do",
    "LOAN_HARASSMENT": "it threatens to contact the people in your phone",
    "INVESTMENT_TIP": "it promises guaranteed returns",
    "TASK_COMMISSION": "it is a prepaid-task scheme",
    "ARMY_OFFICER": "it uses the posted-far-away story to avoid meeting",
    "PRIZE_FRAME": "it offers a reward and a link to collect it",
    "SEXTORTION": "it threatens to send private images to the people you know",
    "MULE_ACCOUNT": "it wants to move somebody else's money through your account",
    "WRONG_TRANSFER": "it says money arrived by mistake and wants it sent back",
    "TAX_REFUND": "it offers a tax refund through a link",
    "PF_CLAIM": "it offers a PF or pension payout through a link",
    "INSURANCE_LAPSE": "it says a policy is lapsing and attaches a way to pay",
    "CARD_UPGRADE": "it offers a card upgrade and wants the OTP or CVV for it",
    "UNLISTED_SHARES": "it offers pre-IPO or unlisted shares over chat",
    "GIFT_CARD_ASK": "it wants vouchers bought and the codes sent back",
    "SCREEN_CODE": "it asks for the code showing on your screen",
    "CRYPTO_DOUBLE": "it promises to multiply money in hours",
    "SUBSCRIPTION_FAIL": "it says a subscription payment failed and links somewhere to fix it",
    "VISA_JOB_ABROAD": "it wants a visa or permit fee for a job abroad",
    "GIFT_FROM_ABROAD": "it wants clearance money for a parcel from abroad",
    "LOAN_APPROVED_FEE": "it says a loan is approved and asks for a fee",
    "DORMANT_ACCOUNT": "it says the account is dormant and links somewhere to reactivate it",
    "SIM_UPGRADE": "it wants an OTP to complete a SIM upgrade",
    "GAS_SUBSIDY": "it wants gas subsidy details through a link",
    "CHARITY_PLEA": "the donation goes to a personal UPI handle",
    "BETTING_PROMO": "it promises daily income from a betting app",
    "MLM_RECRUIT": "the income depends on recruiting more people",
    "EXAM_RESULT_LINK": "it puts a result or admit card behind a sent link",
    "SCHOLARSHIP_BAIT": "it wants documents for a scholarship over chat",
    "CELEB_ENDORSE": "it attaches a famous name to an investment",
    "PROFIT_PROOF": "it offers profit screenshots as the reason to trust it",
    "WHATSAPP_CODE": "it wants the code that signs in to your chat account",
    "FAKE_INVOICE_ACCOUNT": "it says the bank account on the invoice has changed",
    "MEDICAL_PLEA": "it uses a medical emergency to rush a payment",
    "GOVT_JOB_FIXING": "it promises a government job outside the exam",
}

MONEY = {"PAY_TO_GET_JOB", "PAY_TO_RECEIVE", "PERSONAL_PAYMENT", "COURIER_CUSTOMS",
         "TASK_COMMISSION", "LOTTERY_WIN", "INVESTMENT_TIP", "QR_SCAN", "COLLECT_REQUEST", "ADVANCE_FEE", "BANK_DETAILS",
         "PRIZE_FRAME", "MULE_ACCOUNT", "WRONG_TRANSFER", "GIFT_CARD_ASK", "CRYPTO_DOUBLE", "UNLISTED_SHARES",
         "LOAN_APPROVED_FEE", "GIFT_FROM_ABROAD", "CHARITY_PLEA", "BETTING_PROMO", "MLM_RECRUIT", "PROFIT_PROOF",
         "CELEB_ENDORSE", "MEDICAL_PLEA", "FAKE_INVOICE_ACCOUNT"}
JOB = {"PAY_TO_GET_JOB", "NO_INTERVIEW", "TOO_GOOD", "TASK_COMMISSION",
       "VISA_JOB_ABROAD", "GOVT_JOB_FIXING", "SCHOLARSHIP_BAIT"}
IMPERSONATION = {"KYC_PANIC", "ELECTRICITY_CUT", "LOAN_HARASSMENT", "THREAT", "COURIER_CUSTOMS", "SIM_BLOCK", "LOOKALIKE_DOMAIN",
                 "VERIFY_DETAILS", "CALLBACK_NUMBER", "REMOTE_ACCESS", "APK_INSTALL",
                 "TAX_REFUND", "PF_CLAIM", "INSURANCE_LAPSE", "CARD_UPGRADE", "SUBSCRIPTION_FAIL", "DORMANT_ACCOUNT",
                 "SIM_UPGRADE", "GAS_SUBSIDY", "EXAM_RESULT_LINK", "SCREEN_CODE", "WHATSAPP_CODE", "SEXTORTION"}
PROPERTY = {"SIGHT_UNSEEN", "ARMY_OFFICER"}


def build(verdict: dict, lang: str = "en") -> dict:
    """The steps and the reply. In Hindi when the message came in Hindi:
    numbered English instructions inside a Hindi answer help nobody."""
    hi = lang == "hi"
    A = hindi.ACTIONS if hi else {}
    fired = {f["id"] for f in verdict["findings"]}

    if not fired:
        return {
            "actions": [
                A.get("nothing",
                      "Nothing matched, but that is not proof it is safe — it means "
                      "this message does not use any of the patterns Pakka knows."),
                A.get("verify",
                      "If it still feels wrong, verify on a number you already had, "
                      "not one from the message."),
            ],
            "forward": "",
        }

    actions = [A.get("no_pay",
                     "Do not pay anything and do not share any code, however small "
                     "the amount.")]
    if "ASKS_FOR_SECRET" in fired:
        actions.append(A.get("no_otp",
                       "Never share an OTP, PIN or CVV. No bank, delivery agent or "
                       "employer will ever ask for one."))
    if fired & MONEY:
        actions.append("Money sent to a personal UPI ID or account is very hard to get "
                       "back, which is exactly why they ask for it that way.")
    if fired & JOB:
        actions.append("Search the company name with the word careers and apply only "
                       "from its own site.")
    if fired & IMPERSONATION:
        actions.append(A.get("own_number",
                       "If you think it might be genuine, call the number printed on "
                       "your own bill, card or the official website — never the one "
                       "in the message."))
    if fired & PROPERTY:
        actions.append("See the place in person and meet the owner before any money "
                       "moves. No photo, video call or document replaces that.")
    actions.append(A.get("report",
                   "Report it at cybercrime.gov.in or call 1930. If money has already "
                   "gone, report within the first hour, while it can still be frozen."))
    actions.append(A.get("block",
                   "Block the sender, then tell whoever forwarded it to you."))

    clauses = hindi.CLAUSE if hi else CLAUSE
    top = [clauses.get(f["id"], CLAUSE.get(f["id"]))
           for f in verdict["findings"][:2]]
    top = [t for t in top if t]
    if hi:
        reasons = " और ".join(top) if top else "यह जानी-पहचानी धोखाधड़ी जैसा है"
        forward = hindi.UI["forward_template"].replace("{reasons}", reasons)
    else:
        reasons = " and ".join(top) if top else "it matches known scam patterns"
        forward = (f"I checked this before replying — {reasons}. That is how this kind "
                   f"of scam works, so I am not paying or sharing anything. Please do "
                   f"not send money either. (Checked with Pakka)")

    return {"actions": actions, "forward": forward}
