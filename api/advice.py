"""What to do about it, and what to say back.

A score tells you something is wrong. It does not tell you what to do at ten at
night when a stranger is pressuring you, and it is not something you can send to
the person who forwarded it. Both of those are derived from the rules that fired,
so the advice can never contradict the verdict.
"""
from __future__ import annotations

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
}

MONEY = {"PAY_TO_GET_JOB", "PAY_TO_RECEIVE", "PERSONAL_PAYMENT", "COURIER_CUSTOMS",
         "TASK_COMMISSION", "LOTTERY_WIN", "INVESTMENT_TIP", "QR_SCAN", "COLLECT_REQUEST", "ADVANCE_FEE", "BANK_DETAILS"}
JOB = {"PAY_TO_GET_JOB", "NO_INTERVIEW", "TOO_GOOD", "TASK_COMMISSION"}
IMPERSONATION = {"KYC_PANIC", "ELECTRICITY_CUT", "LOAN_HARASSMENT", "THREAT", "COURIER_CUSTOMS", "SIM_BLOCK", "LOOKALIKE_DOMAIN",
                 "VERIFY_DETAILS", "CALLBACK_NUMBER", "REMOTE_ACCESS", "APK_INSTALL"}
PROPERTY = {"SIGHT_UNSEEN", "ARMY_OFFICER"}


def build(verdict: dict) -> dict:
    fired = {f["id"] for f in verdict["findings"]}

    if not fired:
        return {
            "actions": [
                "Nothing matched, but that is not proof it is safe — it means this "
                "message does not use any of the twenty patterns Pakka knows.",
                "If it still feels wrong, verify on a number you already had, not "
                "one from the message.",
            ],
            "forward": "",
        }

    actions = ["Do not pay anything and do not share any code, however small the amount."]
    if "ASKS_FOR_SECRET" in fired:
        actions.append("Never share an OTP, PIN or CVV. No bank, delivery agent or "
                       "employer will ever ask for one.")
    if fired & MONEY:
        actions.append("Money sent to a personal UPI ID or account is very hard to get "
                       "back, which is exactly why they ask for it that way.")
    if fired & JOB:
        actions.append("Search the company name with the word careers and apply only "
                       "from its own site.")
    if fired & IMPERSONATION:
        actions.append("If you think it might be genuine, call the number printed on "
                       "your own bill, card or the official website — never the one in "
                       "the message.")
    if fired & PROPERTY:
        actions.append("See the place in person and meet the owner before any money "
                       "moves. No photo, video call or document replaces that.")
    actions.append("Report it at cybercrime.gov.in or call 1930. If money has already "
                   "gone, report within the first hour, while it can still be frozen.")
    actions.append("Block the sender, then tell whoever forwarded it to you.")

    top = [CLAUSE[f["id"]] for f in verdict["findings"][:2] if f["id"] in CLAUSE]
    reasons = " and ".join(top) if top else "it matches known scam patterns"
    forward = (f"I checked this before replying — {reasons}. That is how this kind of "
               f"scam works, so I am not paying or sharing anything. Please do not "
               f"send money either. (Checked with Pakka)")

    return {"actions": actions, "forward": forward}
