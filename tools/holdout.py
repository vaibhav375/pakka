"""A frozen test set of real scam messages, collected from published sources.

FROZEN. Nothing in this file may be used to write or tune a rule, widen a
pattern or train the model. It exists to answer one question honestly: how does
a rulebook written against messages I made up perform on messages I did not?

Every entry is quoted from a public page that documented it: journalism,
consumer-protection writeups and the government's own fact-check unit. Where a
publisher defanged a link so readers could not click it, writing hxxp:// or
[dot], that has been restored, because the victim received the working link and
the defanging is the publisher's, not the scammer's. Nothing else is edited.

These are published examples, which is not the same as a random sample of what
lands on a phone. They skew towards campaigns big enough to be written about.
That is a real limitation and the README says so next to the number.

    python3 tools/run_holdout.py
"""

SOURCES = {
    "trustcopilot": "https://trustcopilot.in/scam-sms-examples",
    "tradebrains": "https://tradebrains.in/money/banking-fraud-attempts-10-types-of-messages-you-should-read-twice-if-you-receive-them-in-india/",
    "scantotal": "https://scantotal.net/blog/kyc-update-scam-india/",
    "safebrowz": "https://safebrowz.com/blog/upi-paytm-phonepe-google-pay-scam-india-2026",
    "aseemjuneja": "https://aseemjuneja.in/courier-scams-in-india/",
    "fakeout": "https://www.fakeout.io/blog/whatsapp-digital-arrest-scam-2026",
    "pib_indiatv": "https://www.indiatvnews.com/news/india/india-post-text-alert-pib-fact-check-don-t-fall-for-this-viral-sms-scam-here-s-what-you-need-to-know-2025-09-14-1008149",
    "pib_india_com": "https://www.india.com/business/fake-sms-alert-govt-issues-urgent-warning-on-fake-india-post-pan-card-messages-7189984/",
}

FRAUD = [
    ("trustcopilot", "SBI ALERT: Your account will be blocked today. Verify immediately at http://bit.ly/sbi-verify to avoid suspension."),
    ("trustcopilot", "Congratulations! You have won ₹4,999 cashback. Click now to claim reward and complete UPI verification."),
    ("trustcopilot", "Dear customer, share your OTP immediately to stop account suspension. Failure to do so may block your banking access."),
    ("trustcopilot", "Your KYC is pending. Download secure banking app update here: http://short.link/update.apk"),
    ("trustcopilot", "Your parcel could not be delivered. Update your address now at http://bit.ly/delivery-fix to avoid return."),

    ("tradebrains", "Dear Customer, your Bank KYC has expired. Your account will be blocked within 24 hours. Update now: bit.ly/xxxx"),
    ("tradebrains", "Alert! Suspicious activity on your Debit Card has been detected and the card has been temporarily blocked. Reactivate immediately: www.verify-card-now.com"),
    ("tradebrains", "You have just been debited ₹24,999, if this is not you, click here right away to cancel the transaction: secure-bank-help.com"),
    ("tradebrains", "You are missing some money in your account, the amount is ₹50,000, please contact us through the link below to avoid further legal action."),
    ("tradebrains", "Congratulations! If your bank has given you some cash back, you can claim it now before midnight - claim-reward-now.com"),
    ("tradebrains", "Dear Customer, Your electricity bill is due, Your power supply will be cut off tonight if you don't pay now: bill-update.co.in"),
    ("tradebrains", "Follow the link above and enter the customs fee amount of ₹99 to complete the delivery. You can pay ₹99 for the unpaid customs fee and the parcel can be delivered, if you follow the link above."),
    ("tradebrains", "You can now get the ₹2,500 back by clicking on 'Accept' and entering the UPI PIN as it appears on the screen."),
    ("tradebrains", "Due to incomplete Aadhar verification, Your sim card will be blocked in 2 hrs. If you have an update, make sure to update now to prevent service disruption."),
    ("tradebrains", "Your credit card reward points that are worth ₹8,750 will expire today. Redeem them before it's too late by clicking: rewards-update.in"),

    ("scantotal", "Dear SBI Customer, Your KYC verification has expired. Your account will be BLOCKED in 24 hours. Update immediately: bit.ly/sbi-kyc-updt"),
    ("scantotal", "URGENT: Your UPI ID linked to Aadhaar has been suspended."),
    ("safebrowz", "Congratulations! You have won ₹4,999 cashback. Click now to claim reward and complete UPI verification."),
    ("aseemjuneja", "Your package is on hold until a payment or address verification is made. Follow the link above and enter the customs fee amount of ₹99 to complete the delivery."),

    ("fakeout", "Your Aadhaar card was linked to an intercepted drug parcel. You are under digital arrest and must stay on this video call until verification is complete."),
    ("fakeout", "Section 420, NDPS Act. 10 years jail. Your Aadhaar and PAN is misused. Don't tell your family, this matter is sub-judice."),
    ("fakeout", "Transfer all funds to RBI escrow account for verification. Will be returned in 24 hours after clearance."),
    ("fakeout", "Stay on this video call 24x7 until verification is complete. Do not disconnect or a warrant will be issued."),

    ("pib_indiatv", "Your package has arrived at the warehouse and we attempted delivery twice but were unable due to incomplete address information. Please update your delivery location within 12 hours or the package will be returned."),
    ("pib_india_com", "India Post Payment Bank KYC Login Dear user your India post payment bank account has been blocked today please updated your PAN Card immediately."),
]
