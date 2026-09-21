"""Real scam messages collected after the first round of rules. BURNED.

Collected to test whether the rules written against tools/devset.py
generalised. They partly did: this set went from a rules score of 75% on the
first run to 85% once the categories it exposed, traffic challans and bills
that ask to be "updated", had rules of their own.

It was then spent in the same way devset.py was, so every number measured on
it now flatters the rules. tools/finalset.py is the one that is still frozen.

Sources are deliberately different from the ones devset.py used, and include
the I4C cyber-fraud advisory reported in Hindi, which is the language half of
these arrive in.

Where a publisher defanged a link, that has been restored, because the victim
received a working one. Placeholder digits a publisher wrote as XXXXXXXXXX are
left as they are. Nothing else is edited.

    python3 tools/run_holdout.py
"""

SOURCES = {
    "aajtak_i4c": "https://www.aajtak.in/technology/story/cyber-fraud-i4c-warning-sms-electricity-bill-traffic-challan-fake-link-ntc-drmt-rptc-2642402-2026-09-14",
    "kbccompany": "https://kbccompany.info/kbc-lottery-scam-alert-2026/",
    "scamcheck": "https://scamcheck.tech/scams/job-scam-india",
    "technaga": "https://technaga.com/online-scams-india-2026-guide/",
    "wikipedia": "https://en.wikipedia.org/wiki/Digital_arrest_scam",
    "scamwatchhq": "https://scamwatchhq.com/india-scams-2026-digital-arrest-upi-fraud-epidemic/",
    "unionbank": "https://www.unionbankofindia.bank.in/en/blog/digital-arrest-understanding-modus-operandi-current-trends-and-safety-tips",
    "nyayneeti": "https://nyayneeti.com/the-truth-behind-whatsapp-lottery-free-gift-scams-you-must-know/",
}

FRAUD = [
    # I4C's own advisory, reported in Hindi
    ("aajtak_i4c", "आपका बिजली बिल अपडेट नहीं है, आज रात बिजली कनेक्शन काट दिया जाएगा."),
    ("aajtak_i4c", "आपके वाहन का ट्रैफिक चालान पेंडिंग है, तुरंत भुगतान करें, वरना कानूनी कार्रवाई होगी."),
    ("aajtak_i4c", "आपका ई-चालान डाउनलोड करें"),
    ("aajtak_i4c", "अपना Electricity Bill अपडेट करें"),
    ("aajtak_i4c", "KYC तुरंत पूरा करें"),

    ("kbccompany", "Congratulations! Your mobile number has won ₹25 lakh in KBC Lottery 2026."),
    ("kbccompany", "Your WhatsApp number has been selected for a special KBC lucky draw."),
    ("kbccompany", "Contact the KBC manager immediately to receive your prize."),
    ("kbccompany", "Amitabh Bachchan KBC Lottery Winner Notification."),

    ("scamcheck", "Hello, I'm HR Manager at Amazon India. We have a Work From Home vacancy. Salary: ₹45,000/month. No experience needed. Registration fee: ₹999 only. Interested? Reply YES."),
    ("scamcheck", "Congratulations! Your profile on Naukri.com has been shortlisted for a Data Entry position at TCS. Package: ₹35,000/month. Pay ₹1,500 security deposit to confirm your slot. Contact: +91-XXXXXXXXXX"),
    ("scamcheck", "Part-time job opportunity - Earn ₹800-₹1,200 per task by completing simple product ratings on Amazon. Join our WhatsApp group to get started. No experience needed!"),

    ("technaga", "Dear Customer, your SBI/HDFC KYC has expired. Your account will be blocked in 24 hours. Click here to update: bit.ly/fake-link."),
    ("technaga", "Your electricity connection will be disconnected within a few hours unless you immediately contact a provided customer support number."),

    ("wikipedia", "There is a parcel in your name with drugs, cash and a passport. You are now under digital arrest."),
    ("scamwatchhq", "Your account will be blocked!"),
    ("scamwatchhq", "You are under digital arrest!"),
    ("scamwatchhq", "Earn ₹5000 per day!"),
    ("unionbank", "Remain on this continuous video call and transfer the money for verification and safe custody."),
    ("nyayneeti", "You have won a lottery of Rs. 25 lakhs. To claim the prize, a processing fee of Rs. 9,500 has to be paid."),
]
