"""The rules that decide a verdict.

Deliberately plain Python, no model involved. A scam verdict has to be the
same every time and has to be explainable to the person who was nearly
scammed, so the decision lives here and the language model only gets to
phrase the summary afterwards.

Each rule knows how to find itself in a message and can say, in one sentence
a worried person can act on, why what it found is a problem.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Rule:
    id: str
    name: str
    why: str
    weight: int
    pattern: re.Pattern

    def spans(self, text: str) -> list[tuple[int, int]]:
        return [m.span() for m in self.pattern.finditer(text)]


def _p(*alts: str) -> re.Pattern:
    return re.compile("|".join(alts), re.I)


RULES: tuple[Rule, ...] = (
    Rule(
        "PAY_TO_GET_JOB", "Asks for money before a job",
        "A real employer never charges you to be hired. Registration, training "
        "and security fees are the oldest job scam there is.",
        3,
        _p(r"registration fee", r"security (?:fee|deposit|amount)", r"processing fee",
           r"training fee", r"refundable (?:fee|deposit|amount)", r"joining fee",
           r"pay(?:ment)? of (?:rs\.?|₹)\s?\d"),
    ),
    Rule(
        "ASKS_FOR_SECRET", "Asks for an OTP, PIN or password",
        "Nobody legitimate will ever ask for your OTP, UPI PIN, CVV or password "
        "— not your bank, not a delivery agent, not HR.",
        4,
        _p(r"\botp\b", r"\bcvv\b", r"\bupi pin\b", r"\batm pin\b", r"\bpin number\b",
           r"share (?:your )?password", r"\bnet ?banking password\b"),
    ),
    Rule(
        "PAY_TO_RECEIVE", "Asks you to pay to receive money",
        "You are being asked to send money to unlock money. Refunds, prizes and "
        "lottery winnings never require a payment from you first.",
        4,
        _p(r"pay .{0,30}to (?:claim|release|receive|unlock)",
           r"(?:claim|release|receive) .{0,30}after (?:payment|paying)",
           r"processing charge .{0,20}refund", r"to receive your (?:prize|refund|winnings)"),
    ),
    Rule(
        "KYC_PANIC", "KYC or account-block scare",
        "Banks do not block accounts over SMS links. This is the most common "
        "phishing script in India right now.",
        3,
        _p(r"kyc .{0,25}(?:expire|update|pending|suspend)",
           r"account .{0,20}(?:will be )?(?:block|suspend|freeze|deactivat)",
           r"(?:update|complete) .{0,15}kyc"),
    ),
    Rule(
        "URGENCY", "Manufactured urgency",
        "Pressure to act within hours exists to stop you checking. Anything "
        "genuine will still be there tomorrow.",
        1,
        _p(r"within \d+ ?(?:hours?|hrs?|minutes?|mins?)", r"today only", r"last chance",
           r"expires? (?:today|tonight|soon)", r"immediately", r"hurry",
           r"limited (?:slots?|seats?|offer)", r"only \d+ (?:slots?|seats?) left"),
    ),
    Rule(
        "NO_INTERVIEW", "Selected without any interview",
        "An offer with no interview is not an offer. Real hiring involves "
        "someone actually speaking to you.",
        2,
        _p(r"(?:selected|shortlisted) without (?:any )?interview",
           r"no interview (?:required|needed)", r"direct joining", r"instant (?:offer|joining)"),
    ),
    Rule(
        "TOO_GOOD", "Pay that does not match the work",
        "Earnings far above the going rate for a few hours a day are bait. The "
        "money is the hook, not the job.",
        2,
        _p(r"(?:rs\.?|₹)\s?[1-9]\d{3,}[^.]{0,30}(?:per day|/day|daily|per week)",
           r"earn (?:rs\.?|₹)\s?\d[\d,]*.{0,25}(?:from home|part[- ]?time|\d ?(?:hours?|hrs?))",
           r"\d ?(?:hours?|hrs?) (?:work )?daily.{0,25}(?:rs\.?|₹)\s?\d"),
    ),
    Rule(
        "PERSONAL_PAYMENT", "Money goes to a personal account",
        "Payment to a personal UPI ID or a phone number leaves you no way to "
        "recover the money and no company to complain about.",
        3,
        _p(r"\b[\w.\-]{2,}@(?:ok\w+|paytm|ybl|ibl|axl|upi|apl)\b",
           r"(?:google ?pay|phone ?pe|paytm|gpay|upi)\b.{0,25}\b(?:\+?91)?[6-9]\d{9}\b",
           r"\b(?:\+?91)?[6-9]\d{9}\b.{0,25}(?:google ?pay|phone ?pe|paytm|gpay|upi)\b",
           r"scan (?:the )?qr .{0,20}(?:pay|send)"),
    ),
    Rule(
        "FREE_EMAIL_AS_COMPANY", "Company mail sent from a free inbox",
        "A company with a careers page does not send offer letters from a "
        "personal Gmail address.",
        2,
        _p(r"\b(?:hr|careers?|recruit\w*|hiring|support|admin)[\w.\-]*@"
           r"(?:gmail|yahoo|outlook|hotmail|rediffmail)\.com\b"),
    ),
    Rule(
        "HIDDEN_LINK", "Shortened or disguised link",
        "Shortened links hide where they actually go. Legitimate organisations "
        "link to their own domain.",
        2,
        _p(r"\b(?:bit\.ly|tinyurl\.com|cutt\.ly|rb\.gy|t\.me|rebrand\.ly|is\.gd|shorturl\.at)/\S+"),
    ),
    Rule(
        "CHAT_ONLY", "Exists only on WhatsApp or Telegram",
        "No office, no website, no landline — only a chat window. There is "
        "nothing to hold accountable afterwards.",
        1,
        _p(r"(?:contact|message|ping|dm|reach) (?:me |us )?(?:only )?on (?:whats ?app|telegram)",
           r"join (?:our )?telegram", r"whats ?app (?:only|me at)"),
    ),
    Rule(
        "THREAT", "Threatens legal or police action",
        "Threats of FIRs, court cases or arrest over a message are a pressure "
        "tactic. Real legal process does not arrive by WhatsApp.",
        2,
        _p(r"\bf\.?i\.?r\.?\b", r"legal action", r"police (?:case|complaint|action)",
           r"(?:court|arrest) (?:case|warrant|notice)", r"cyber ?crime"),
    ),
    Rule(
        "SIGHT_UNSEEN", "Asks for rent before you have seen the place",
        "Paying a token or advance before visiting is how fake listings work. "
        "The photos are usually taken from a real listing elsewhere.",
        3,
        _p(r"(?:token|advance|booking) (?:amount|money|fee).{0,40}(?:before|without) .{0,20}(?:visit|see)",
           r"(?:i am|i'm|currently) (?:abroad|out of (?:town|country)|in another city).{0,60}(?:send|transfer|pay)",
           r"book (?:it )?(?:now|today) .{0,20}without (?:a )?visit"),
    ),
    Rule(
        "COURIER_CUSTOMS", "Parcel held, pay a fee to release it",
        "Couriers do not hold parcels for a fee over SMS. Customs duty is paid "
        "to the government, never to a WhatsApp number.",
        3,
        _p(r"(?:parcel|package|courier|shipment|consignment).{0,40}(?:held|stuck|seized|customs|clearance)",
           r"customs (?:duty|clearance|charge).{0,30}(?:pay|transfer)",
           r"(?:fedex|dhl|bluedart|india post).{0,40}(?:pay|fee|charge)"),
    ),
    Rule(
        "ELECTRICITY_CUT", "Electricity disconnection threat",
        "Power utilities do not warn you by SMS from a personal number, and "
        "they never ask you to call one to avoid disconnection tonight.",
        3,
        _p(r"electricity .{0,30}(?:disconnect|cut off|discontinue)",
           r"power .{0,20}(?:will be )?disconnect", r"bill .{0,20}not updated.{0,30}disconnect"),
    ),
    Rule(
        "LOTTERY_WIN", "A prize you never entered for",
        "You cannot win a lottery you never entered. Every version of this ends "
        "with a fee to release the winnings.",
        4,
        _p(r"(?:won|winner).{0,30}(?:lottery|lucky draw|prize|kbc)",
           r"\bkbc\b", r"lucky (?:winner|draw)", r"congratulations.{0,30}\bwon\b"),
    ),
    Rule(
        "LOAN_HARASSMENT", "Loan-app style pressure",
        "Threatening to contact your phonebook over a loan is illegal recovery "
        "practice, not a legitimate demand.",
        3,
        _p(r"(?:inform|contact|call).{0,25}(?:your )?(?:contacts|family|friends|relatives).{0,30}(?:loan|due|payment)",
           r"loan .{0,25}(?:overdue|default).{0,30}(?:legal|action|contacts)",
           r"defaulter.{0,30}(?:list|notice)"),
    ),
    Rule(
        "INVESTMENT_TIP", "Guaranteed returns or a tips group",
        "Guaranteed returns do not exist. Groups offering them exist to take "
        "deposits that cannot be withdrawn.",
        3,
        _p(r"guaranteed (?:returns?|profit|income)", r"(?:double|triple) your money",
           r"(?:stock|trading|crypto|forex) (?:tips?|group|signals?)",
           r"\b\d{2,3}% (?:returns?|profit)"),
    ),
    Rule(
        "TASK_COMMISSION", "Prepaid task or commission work",
        "Task scams start with small payouts that work, then ask you to deposit "
        "for a bigger task. The deposit is the point.",
        3,
        _p(r"(?:complete|do) .{0,20}tasks?.{0,30}(?:earn|commission|payout)",
           r"(?:like|subscribe|rate).{0,25}(?:videos?|hotels?|products?).{0,30}(?:earn|paid|commission)",
           r"prepaid task", r"recharge .{0,20}to (?:unlock|continue).{0,20}task"),
    ),
    Rule(
        "ARMY_OFFICER", "Claims to be posted far away and cannot meet",
        "The soldier-being-transferred story is the oldest marketplace scam in "
        "India. It exists to explain why you must pay before meeting.",
        3,
        _p(r"(?:army|military|cisf|crpf|bsf|navy) (?:officer|jawan|personnel)",
           r"(?:posted|deployed) (?:in|at) .{0,30}(?:cannot|can't) (?:meet|come)",
           r"transfer(?:red)? .{0,25}urgent(?:ly)? .{0,25}sell"),
    )
)


@dataclass
class Finding:
    rule: Rule
    spans: list[tuple[int, int]] = field(default_factory=list)


BANDS = (
    (8, "almost_certainly", "Almost certainly a scam"),
    (5, "likely", "Likely a scam"),
    (2, "careful", "Be careful"),
    (1, "one_flag", "One thing to check"),
    (0, "clear", "Nothing suspicious found"),
)


def evaluate(text: str) -> dict:
    """Score a message. Same input, same output, every time."""
    findings = [Finding(r, s) for r in RULES if (s := r.spans(text))]
    score = sum(f.rule.weight for f in findings)
    key, label = next((k, l) for threshold, k, l in BANDS if score >= threshold)
    return {
        "score": score,
        "band": key,
        "label": label,
        "findings": [
            {
                "id": f.rule.id,
                "name": f.rule.name,
                "why": f.rule.why,
                "weight": f.rule.weight,
                "spans": f.spans,
                "quotes": [text[a:b] for a, b in f.spans],
            }
            for f in sorted(findings, key=lambda f: -f.rule.weight)
        ],
        "rules_checked": len(RULES),
    }
