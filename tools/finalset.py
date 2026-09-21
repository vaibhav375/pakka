"""A frozen test set of real scam messages, collected last of all.

SPENT, in the end. It scored 80% on its one honest run, and the two it missed
were both government scheme names used as bait, PM Kisan and Ayushman, which is
a real category and not a quirk of these two messages. So a rule was written
for it and this set stopped being frozen.

The honest trajectory across three sets, each measured once before it was
spent, is 52%, then 75%, then 80%. Every number after that is in-sample.

Sources are again different from both earlier sets. Two of these, from
Moneylife, are transcribed from what a victim actually received, typos and
broken sentences intact, which is closer to the real thing than anything a
publisher tidies up.

    python3 tools/run_holdout.py final
"""

SOURCES = {
    "razorpay": "https://razorpay.com/learn/fake-bank-text-messages-fraud/",
    "moneylife": "https://www.moneylife.in/article/fraud-alert-beware-of-electricity-bill-scam-rs1464-lakh-withdrawn-using-aadhaar-fingerprints/67517.html",
    "rtiwiki": "https://righttoinformation.wiki/fake-pm-scheme-scam-india",
    "newsx": "https://www.newsx.com/regionals/received-gas-disconnection-sms-delhi-police-arrest-4-recover-rs-600000-in-apk-fraud-how-to-avoid-gas-cylinder-scam-241286/",
    "the420": "https://the420.in/sms-banking-scams-india-mobile-fraud-report-2026/",
}

FRAUD = [
    ("razorpay", "Dear customer, your KYC has expired. Update now to avoid account suspension: http://kyc-verify.in/update"),
    ("razorpay", "INR 25,000 debited from your account. If not done by you, report here: http://bank-report.in/fraud"),
    ("razorpay", "Congratulations! You are eligible for a pre-approved loan of Rs. 5 lakhs. Apply now: http://loan-approve.in"),

    # transcribed from what victims received, typos intact
    ("moneylife", "Dear customer Your Electricity power will be disconnected. Tonight at 9.30 pm from electricity office. because your previous month bill was not update. Please immediately contact with. Our electricity officer 0000000000 Thank you."),
    ("moneylife", "Dear Consumer Your Electricity Power Will be disconnected by Tonight Last Month Bill was not updated. Immediately contact our 9163712892 -BRENTS"),

    ("rtiwiki", "You have been selected for the PM Digital Bharat Subsidy. A processing fee of Rs 5,000 is required. Approval expires tonight, slots filling fast."),
    ("rtiwiki", "PM Kisan Samman Nidhi Extension: your name is approved. Complete registration today, last day."),
    ("rtiwiki", "Ayushman Gold Card Upgrade approved for your family. Apply before tonight to keep your benefits."),

    ("newsx", "Your IGL gas connection is going to be disconnected today. Contact 9812345670 immediately for assistance."),
    ("newsx", "Install the attached APK to complete your gas connection verification and avoid disconnection."),
]
