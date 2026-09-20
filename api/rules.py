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
import unicodedata

import urls
from dataclasses import dataclass, field



_LEET = {"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t"}
def _alpha(c: str) -> bool:
    return c.isascii() and c.isalpha()


def _alnum(c: str) -> bool:
    return c.isascii() and c.isalnum()


def normalise(text: str) -> tuple[str, list[int]]:
    """Return a normalised copy of the text and a map back to the original.

    Scam messages are written to get past filters: K Y C spaced out, an O typed
    as a zero, an umlaut dropped on a vowel. Matching against a normalised copy
    keeps every rule simple, and the index map means the page can still
    highlight the words in the message the person actually pasted.

    tools/build_rules_js.py emits the same function in JavaScript and
    tools/check_parity.py fails if the two ever disagree, so any change here
    has to be made there too.
    """
    chars: list[str] = []
    idx: list[int] = []
    for i, ch in enumerate(text):
        for c in unicodedata.normalize("NFD", ch):
            if "\u0300" <= c <= "\u036f":      # a combining accent, dropped
                continue
            # anything outside the basic plane, an emoji say, becomes one
            # placeholder, so that ".{0,30}" counts it the same in JavaScript,
            # where it would otherwise be two characters
            chars.append("\ufffd" if ord(c) > 0xFFFF else c)
            idx.append(i)

    # a digit standing in for a letter, but only where a letter sits beside it,
    # so phone numbers and amounts are left alone
    for j, c in enumerate(chars):
        if c in _LEET:
            prev = chars[j - 1] if j else ""
            nxt = chars[j + 1] if j + 1 < len(chars) else ""
            if _alpha(prev) or _alpha(nxt):
                chars[j] = _LEET[c]

    # letters spaced or hyphenated apart, pulled back together
    out: list[str] = []
    oidx: list[int] = []
    n = len(chars)

    def lone(q: int) -> bool:
        """A letter standing by itself, like the K in "K Y C"."""
        return (_alpha(chars[q])
                and (q == 0 or not _alnum(chars[q - 1]))
                and (q + 1 >= n or not _alnum(chars[q + 1])))

    i = 0
    while i < n:
        if lone(i):
            run = [i]
            j = i
            sep = chars[i + 1] if i + 1 < n else ""
            # one separator throughout, so "W-O-N a prize" gives WON, not WONa
            while (j + 2 < n and chars[j + 1] == sep and sep in " .-"
                   and lone(j + 2)):
                run.append(j + 2)
                j += 2
            if len(run) >= 3:
                for k in run:
                    out.append(chars[k])
                    oidx.append(idx[k])
                i = j + 1
                continue
        out.append(chars[i])
        oidx.append(idx[i])
        i += 1
    return "".join(out), oidx


def _word(c: str) -> bool:
    return c.isalnum() or c == "_"


def _whole_words(text: str, a: int, b: int) -> tuple[int, int]:
    """Grow a span out to word edges, so a highlight never cuts "expired"
    into "expire" and a stranded "d"."""
    while a > 0 and _word(text[a - 1]) and _word(text[a]):
        a -= 1
    while b < len(text) and _word(text[b]) and _word(text[b - 1]):
        b += 1
    return a, b


@dataclass(frozen=True)
class Rule:
    id: str
    name: str
    why: str
    weight: int
    pattern: re.Pattern

    def spans(self, text: str, norm: str | None = None,
              idx: list[int] | None = None) -> list[tuple[int, int]]:
        """Match the normalised text, report positions in the original."""
        if norm is None or idx is None:
            norm, idx = normalise(text)
        out = []
        for m in self.pattern.finditer(norm):
            a, b = m.span()
            if b > a and idx:
                out.append(_whole_words(text, idx[a], idx[min(b, len(idx)) - 1] + 1))
        return out


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
           r"(?:have to|need to|must|kindly|please) pay (?:rs\.?|₹)?\s?[\d,]+",
           r"\bpay (?:rs\.?|₹)\s?[\d,]+ (?:to|for) (?:confirm|secure|book|get|join|start|activat)"),
    ),
    Rule(
        "ASKS_FOR_SECRET", "Asks for an OTP, PIN or password",
        "Nobody legitimate will ever ask for your OTP, UPI PIN, CVV or password "
        "— not your bank, not a delivery agent, not HR.",
        4,
        _p(r"(?:share|send|tell|give|provide|forward|confirm|read out)\s+(?:me\s+|us\s+|the\s+|your\s+)*\b(?:otp|cvv|pin|password|code)\b(?!\s*(?:is\s*)?\d{4,8})",
           r"\b(?:apna|apne) otp\b", r"\botp\b .{0,15}(?:bhej|batao|bataiye|share kij)",
           r"\b(?:otp|cvv|pin)\b.{0,25}(?:with (?:our|the|me|us)|to (?:our|the|me|us|verify))",
           r"what(?:'s| is) (?:your |the )?(?:otp|cvv|pin)\b",
           r"\bcvv\b.{0,20}(?:number|digits)", r"\bupi pin\b", r"\batm pin\b",
           r"share (?:your )?password", r"\bnet ?banking password\b"),
    ),
    Rule(
        "PAY_TO_RECEIVE", "Asks you to pay to receive money",
        "You are being asked to send money to unlock money. Refunds, prizes and "
        "lottery winnings never require a payment from you first.",
        4,
        _p(r"pay .{0,30}to (?:claim|release|receive|unlock)",
           r"(?:claim|release|receive) .{0,30}after (?:payment|paying)",
           r"processing charge .{0,20}refund", r"to receive your (?:prize|refund|winnings)",
           r"pay .{0,25}(?:delivery|shipping|handling|courier) charge"),
    ),
    Rule(
        "KYC_PANIC", "KYC or account-block scare",
        "Banks do not block accounts over SMS links. This is the most common "
        "phishing script in India right now.",
        3,
        _p(r"kyc .{0,25}(?:expire|pending|suspend|incomplete|not (?:done|updated))",
           r"account .{0,30}(?:will be |has been )?(?:block|suspend|freeze|deactivat)",
           r"(?:update|complete|verify) .{0,20}kyc .{0,40}"
           r"(?:\bor\b|else|otherwise|to avoid|immediately|now|today|link|http|block|suspend|frozen)",
           r"(?:account|khata|kyc).{0,30}(?:block|band) ho jayega", r"kyc update nahi"),
    ),
    Rule(
        "URGENCY", "Manufactured urgency",
        "Pressure to act within hours exists to stop you checking. Anything "
        "genuine will still be there tomorrow.",
        1,
        _p(r"within \d+ ?(?:hours?|hrs?|minutes?|mins?)", r"today only", r"last chance",
           r"(?:block|suspend|deactivat|expir|clos|disconnect|cancel|terminat)\w*\s+"
           r"(?:with)?in\s+\d+\s*(?:hours?|hrs?|days?|minutes?)",
           r"expires? (?:today|tonight|soon)", r"immediately", r"hurry", r"\burgently\b",
           r"\bturant\b", r"\bjaldi\b", r"urgent hai",
           r"limited (?:slots?|seats?|offer)", r"only \d+ (?:slots?|seats?) left",
           r"before (?:you )?(?:lose|miss)", r"\b(?:click|claim|act|apply) (?:it |this |here |the link )?now\b"),
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
           r"\d ?(?:hours?|hrs?) (?:work )?daily.{0,25}(?:rs\.?|₹)\s?\d",
           r"ghar baithe .{0,25}kama", r"(?:rupaye|rupay) (?:daily|roz|rozana)"),
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
           r"join (?:our )?telegram", r"whats ?app (?:only|me at)",
           r"(?:whats ?app|telegram) par (?:contact|message|baat|kare)"),
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
           r"(?:i am|i'm|currently) (?:abroad|out of (?:town|country|station)|in another city|not in the city).{0,60}(?:send|transfer|pay)",
           r"book (?:it )?(?:now|today) .{0,20}without (?:a )?visit",
           r"(?:advance|token|booking).{0,40}(?:to )?(?:block|hold|reserve) the (?:room|bed|flat|house|pg)",
           r"pay .{0,25}(?:booking|advance|token).{0,30}before visit"),
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
           r"\bkbc\b", r"lucky (?:winner|draw)",
           r"congratulations.{0,30}\b(?:won|winning|winner)\b.{0,50}"
           r"(?:\brs\.?\s*\d|₹|lakh|crore|lottery|lucky draw|prize|gift|iphone|mac ?book|laptop|\bcar\b|voucher|hamper)",
           r"lottery lag gay", r"\bjeeta hai\b", r"(?:lakh|crore) rupaye jeet",
           r"\b(?:won|winning|win a)\b.{0,40}(?:iphone|mac ?book|laptop|smartphone|"
           r"scooter|\bcar\b|\bbike\b|gift (?:card|voucher|hamper)|voucher|cash prize|\bgift\b)",
           r"\bfree\b.{0,20}(?:iphone|mac ?book|laptop|smartphone|\bcar\b|scooter|\bbike\b)"),
    ),
    Rule(
        "QR_SCAN", "A QR code to receive money",
        "Scanning a QR code can only send money out of your account. It can never "
        "bring money in. Anyone telling you to scan one to claim, collect or "
        "receive something is describing a thing that cannot happen.",
        3,
        _p(r"scan .{0,25}\bqr\b.{0,40}(?:claim|collect|receive your|get your|refund|"
           r"prize|reward|cashback|winnings|the offer)",
           r"\bqr code\b.{0,30}(?:to )?(?:claim|collect|receive your|get your)",
           r"(?:claim|collect|receive) .{0,30}(?:by |through |via )?scanning"),
    ),
    Rule(
        "REMOTE_ACCESS", "Wants to see or control your screen",
        "No bank, no support desk and no government office will ever ask you to "
        "install a screen sharing app. Someone watching your screen sees your "
        "banking app and your PIN as you type it.",
        4,
        _p(r"\b(?:any ?desk|team ?viewer|quick ?support|rust ?desk|ammyy|air ?droid)\b",
           r"screen[- ]?shar(?:e|ing)", r"share your screen", r"mirror your (?:screen|phone)"),
    ),
    Rule(
        "APK_INSTALL", "Wants you to install an app from outside the store",
        "An app sent to you as a file has not been checked by anyone. This is how "
        "banking trojans get onto phones in India.",
        4,
        _p(r"\bapk\b", r"(?:install|download|sideload) .{0,30}(?:from|via|through) (?:this |the )?link",
           r"enable (?:unknown sources|installation from unknown)"),
    ),
    Rule(
        "LOOKALIKE_DOMAIN", "A web address dressed up as a real company",
        "The brand name is in the address but the domain is not theirs. Real "
        "organisations send you to their own domain, not a lookalike.",
        3,
        _p(r"https?://[^\s]*\b(?:sbi|hdfc|icici|axis|kotak|paytm|phonepe|amazon|flipkart|"
           r"netflix|irctc|epfo|uidai|income ?tax|indiapost)[-_][a-z0-9-]+\.",
           r"https?://[^\s]*\b(?:sbi|hdfc|icici|axis|paytm|phonepe|amazon|flipkart|netflix|"
           r"irctc|epfo|uidai)[^\s]*\.(?:xyz|info|top|online|site|club|icu|buzz|link|shop|tk|ml|ga|cf)\b",
           r"https?://[^\s]*\bhdfc-bank\b"),
    ),
    Rule(
        "VERIFY_DETAILS", "Wants your details to avoid something bad",
        "Being told to confirm your details to stop something bad happening is the "
        "oldest phishing shape there is. If it is real, it will still be there "
        "when you open the app yourself.",
        2,
        _p(r"(?:click|tap|open|visit) .{0,30}(?:link|here|below|url).{0,40}"
           r"(?:verify|update|confirm|activate|re-?activate|avoid|prevent|suspend)",
           r"(?:verify|update|confirm) (?:your )?(?:\w+ )?(?:account|details|kyc|card details|"
           r"bank details|information).{0,30}(?:here|link|below|now|immediately|https?://)"),
    ),
    Rule(
        "ID_DOCUMENTS", "Asks for your Aadhaar or PAN",
        "A photo of your Aadhaar or PAN is enough to open accounts and take loans "
        "in your name. Nobody legitimate collects it over a chat message.",
        3,
        _p(r"(?:photo|copy|scan|pic|image|soft copy) .{0,25}(?:of )?(?:your )?"
           r"(?:aadhaar|aadhar|pan card|passport|voter id|driving licen[cs]e)",
           r"(?:send|share|whatsapp|forward) .{0,25}\b(?:aadhaar|aadhar|pan card)\b",
           r"selfie .{0,30}(?:with|holding) .{0,20}(?:aadhaar|aadhar|pan|id)",
           r"(?:aadhaar|aadhar|pan card).{0,30}(?:and|\+) .{0,15}selfie"),
    ),
    Rule(
        "CALLBACK_NUMBER", "A personal mobile posing as a helpline",
        "Real companies publish landlines or 1800 numbers you can look up. A "
        "ten digit mobile presented as customer care belongs to a person, not a bank.",
        2,
        _p(r"(?:customer care|help ?line|support number|official number|toll ?free)"
           r"[^\d]{0,25}\b[6-9]\d{9}\b",
           r"\b[6-9]\d{9}\b[^\d]{0,25}(?:customer care|help ?line)",
           r"call (?:this|our|the above) number.{0,25}(?:to |and )?"
           r"(?:cancel|stop|block|verify|reverse|claim|confirm)"),
    ),
    Rule(
        "COLLECT_REQUEST", "Asks you to approve something to receive money",
        "Entering your PIN or approving a request always sends money out. It can "
        "never bring money in. Anyone saying otherwise is taking, not giving.",
        4,
        _p(r"(?:accept|approve) .{0,25}request.{0,30}(?:receive|get|credit)",
           r"(?:enter|put|type) (?:your )?(?:upi )?pin.{0,30}(?:receive|get|credit|refund)",
           r"credited .{0,40}(?:click|withdraw|claim)",
           r"(?:click|tap) .{0,20}(?:here|link).{0,25}(?:to )?(?:withdraw|claim) "
           r".{0,20}(?:amount|money|cashback|reward)"),
    ),
    Rule(
        "STRANGER_OPENER", "A stranger opening with money talk",
        "The wrong number that turns into a friendship that turns into an "
        "investment app. It starts exactly like this, every time.",
        2,
        _p(r"(?:got|found|received|saved) your (?:number|contact) from",
           r"(?:sorry|sry|oops),? .{0,20}wrong number",
           r"wrong number.{0,90}(?:trade|trading|crypto|forex|invest|profit|teach you)",
           r"(?:i am|i'm|this is) \w+,? .{0,40}(?:trade|trading|crypto|forex|"
           r"investment|profit|returns)"),
    ),
    Rule(
        "ADVANCE_FEE", "An inheritance or fortune from a stranger",
        "Nobody picks a stranger to receive a fortune. The money does not exist, "
        "and the fees you are asked for along the way are the entire point.",
        3,
        _p(r"\b(?:widow|late husband|late father|inheritance|next of kin|beneficiary)\b"
           r".{0,60}(?:million|billion|fund|money|donate|\$)",
           r"(?:transfer|donate|share) .{0,30}(?:\$\s?\d|usd|million dollars|billion)",
           r"trustworthy person", r"\bnext of kin\b"),
    ),
    Rule(
        "BANK_DETAILS", "Wants your account number to send you money",
        "Money already owed to you goes to the account it came from. Being asked "
        "for fresh bank details is how the account gets emptied, not filled.",
        3,
        _p(r"(?:refund|amount|salary|payment|prize|claim).{0,60}"
           r"(?:submit|share|send|provide|enter|fill) .{0,25}"
           r"(?:bank account|account number|account details|ifsc)",
           r"(?:bank account|account number|ifsc).{0,40}(?:to )?(?:receive|claim) "
           r"(?:your |the )?(?:refund|prize|amount|winnings|money)"),
    ),
    Rule(
        "SIM_BLOCK", "Threatens to block your SIM or connection",
        "Your operator does not disconnect you over a text with a link. The panic "
        "is the product.",
        3,
        _p(r"(?:sim(?: card)?|mobile number|connection|outgoing)"
           r".{0,30}(?:will be |going to be |about to be )?"
           r"(?:block|deactivat|disconnect|barred|suspend)"),
    ),
    Rule(
        "NEW_NUMBER", "A new number that needs money",
        "Someone claiming a new number and then asking for money is how a family "
        "member's identity gets borrowed. Call them on the number you already have.",
        3,
        _p(r"(?:this is|it'?s) (?:my |me,? )?(?:new|changed) number"
           r".{0,120}(?:send|transfer|urgent|money|pay\b|rs\.?\s?\d|\u20b9)",
           r"\b(?:mom|mum|mummy|dad|papa|mama)\b.{0,60}\bnew number\b"
           r".{0,120}(?:send|transfer|urgent|money|pay\b|rs\.?\s?\d)",
           r"(?:lost|broke|damaged|changed) my phone.{0,80}(?:send|transfer|money|rs\.?\s?\d)",
           r"(?:mera|mere) naya number.{0,120}(?:bhej|rupaye|rupay|paise|transfer|urgent)",
           r"purana phone (?:kho gaya|kharab)"),
    ),
    Rule(
        "STRANDED_PLEA", "Stranded somewhere and needs money now",
        "A hijacked account of someone you know, or a stranger who knows the "
        "story works. Call the person on the number you already have.",
        2,
        _p(r"(?:stuck|stranded|trapped) (?:in|at) \w+.{0,60}"
           r"(?:send|transfer|need) .{0,15}money",
           r"lost my (?:wallet|phone|passport|bag).{0,60}(?:send|transfer|need) .{0,20}money"),
    ),
    Rule(
        # Checked by api/urls.py rather than by this pattern, which never
        # matches. A rule can look for the word "sbi". It cannot tell you the
        # "a" in this address is Cyrillic.
        "LOOKALIKE_URL", "A web address that is not the characters it appears to be",
        "Letters from another alphabet, punycode, digits inside a brand name or "
        "a bare IP address. The address reads correctly to a person and goes "
        "somewhere else.",
        3,
        _p(r"(?!x)x"),
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
           r"\b(?:major|colonel|captain|subedar|havildar|brigadier) [a-z]\w+",
           r"(?:posted|deployed) (?:in|at) .{0,40}(?:cannot|can't|unable to) (?:meet|come|visit|see)",
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
    norm, idx = normalise(text)
    findings = [Finding(r, s) for r in RULES
                if r.id != "LOOKALIKE_URL" and (s := r.spans(text, norm, idx))]

    # the one check that is about the characters rather than the words
    url_hits = urls.suspicious(text)
    if url_hits:
        rule = next(r for r in RULES if r.id == "LOOKALIKE_URL")
        findings.append(Finding(rule, sorted({(a, b) for _, _, a, b in url_hits})))
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
                "why": (f.rule.why if f.rule.id != "LOOKALIKE_URL"
                        else "; ".join(dict.fromkeys(
                            r for _, r, _, _ in urls.suspicious(text)))),
                "weight": f.rule.weight,
                "spans": f.spans,
                "quotes": [text[a:b] for a, b in f.spans],
            }
            for f in sorted(findings, key=lambda f: -f.rule.weight)
        ],
        "rules_checked": len(RULES),
    }
