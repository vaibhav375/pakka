/* Generated from api/rules.py by tools/build_rules_js.py — do not edit.
   Running the check here means the message never leaves the device unless the
   person presses Share. */
window.PAKKA_RULES = [
  {
    "id": "PAY_TO_GET_JOB",
    "name": "Asks for money before a job",
    "why": "A real employer never charges you to be hired. Registration, training and security fees are the oldest job scam there is.",
    "weight": 3,
    "re": "registration fee|security (?:fee|deposit|amount)|processing fee|training fee|refundable (?:fee|deposit|amount)|joining fee|pay(?:ment)? of (?:rs\\.?|₹)\\s?\\d"
  },
  {
    "id": "ASKS_FOR_SECRET",
    "name": "Asks for an OTP, PIN or password",
    "why": "Nobody legitimate will ever ask for your OTP, UPI PIN, CVV or password — not your bank, not a delivery agent, not HR.",
    "weight": 4,
    "re": "\\botp\\b|\\bcvv\\b|\\bupi pin\\b|\\batm pin\\b|\\bpin number\\b|share (?:your )?password|\\bnet ?banking password\\b"
  },
  {
    "id": "PAY_TO_RECEIVE",
    "name": "Asks you to pay to receive money",
    "why": "You are being asked to send money to unlock money. Refunds, prizes and lottery winnings never require a payment from you first.",
    "weight": 4,
    "re": "pay .{0,30}to (?:claim|release|receive|unlock)|(?:claim|release|receive) .{0,30}after (?:payment|paying)|processing charge .{0,20}refund|to receive your (?:prize|refund|winnings)"
  },
  {
    "id": "KYC_PANIC",
    "name": "KYC or account-block scare",
    "why": "Banks do not block accounts over SMS links. This is the most common phishing script in India right now.",
    "weight": 3,
    "re": "kyc .{0,25}(?:expire|update|pending|suspend)|account .{0,20}(?:will be )?(?:block|suspend|freeze|deactivat)|(?:update|complete) .{0,15}kyc"
  },
  {
    "id": "URGENCY",
    "name": "Manufactured urgency",
    "why": "Pressure to act within hours exists to stop you checking. Anything genuine will still be there tomorrow.",
    "weight": 1,
    "re": "within \\d+ ?(?:hours?|hrs?|minutes?|mins?)|today only|last chance|expires? (?:today|tonight|soon)|immediately|hurry|limited (?:slots?|seats?|offer)|only \\d+ (?:slots?|seats?) left"
  },
  {
    "id": "NO_INTERVIEW",
    "name": "Selected without any interview",
    "why": "An offer with no interview is not an offer. Real hiring involves someone actually speaking to you.",
    "weight": 2,
    "re": "(?:selected|shortlisted) without (?:any )?interview|no interview (?:required|needed)|direct joining|instant (?:offer|joining)"
  },
  {
    "id": "TOO_GOOD",
    "name": "Pay that does not match the work",
    "why": "Earnings far above the going rate for a few hours a day are bait. The money is the hook, not the job.",
    "weight": 2,
    "re": "(?:rs\\.?|₹)\\s?[1-9]\\d{3,}[^.]{0,30}(?:per day|/day|daily|per week)|earn (?:rs\\.?|₹)\\s?\\d[\\d,]*.{0,25}(?:from home|part[- ]?time|\\d ?(?:hours?|hrs?))|\\d ?(?:hours?|hrs?) (?:work )?daily.{0,25}(?:rs\\.?|₹)\\s?\\d"
  },
  {
    "id": "PERSONAL_PAYMENT",
    "name": "Money goes to a personal account",
    "why": "Payment to a personal UPI ID or a phone number leaves you no way to recover the money and no company to complain about.",
    "weight": 3,
    "re": "\\b[\\w.\\-]{2,}@(?:ok\\w+|paytm|ybl|ibl|axl|upi|apl)\\b|(?:google ?pay|phone ?pe|paytm|gpay|upi)\\b.{0,25}\\b(?:\\+?91)?[6-9]\\d{9}\\b|\\b(?:\\+?91)?[6-9]\\d{9}\\b.{0,25}(?:google ?pay|phone ?pe|paytm|gpay|upi)\\b|scan (?:the )?qr .{0,20}(?:pay|send)"
  },
  {
    "id": "FREE_EMAIL_AS_COMPANY",
    "name": "Company mail sent from a free inbox",
    "why": "A company with a careers page does not send offer letters from a personal Gmail address.",
    "weight": 2,
    "re": "\\b(?:hr|careers?|recruit\\w*|hiring|support|admin)[\\w.\\-]*@(?:gmail|yahoo|outlook|hotmail|rediffmail)\\.com\\b"
  },
  {
    "id": "HIDDEN_LINK",
    "name": "Shortened or disguised link",
    "why": "Shortened links hide where they actually go. Legitimate organisations link to their own domain.",
    "weight": 2,
    "re": "\\b(?:bit\\.ly|tinyurl\\.com|cutt\\.ly|rb\\.gy|t\\.me|rebrand\\.ly|is\\.gd|shorturl\\.at)/\\S+"
  },
  {
    "id": "CHAT_ONLY",
    "name": "Exists only on WhatsApp or Telegram",
    "why": "No office, no website, no landline — only a chat window. There is nothing to hold accountable afterwards.",
    "weight": 1,
    "re": "(?:contact|message|ping|dm|reach) (?:me |us )?(?:only )?on (?:whats ?app|telegram)|join (?:our )?telegram|whats ?app (?:only|me at)"
  },
  {
    "id": "THREAT",
    "name": "Threatens legal or police action",
    "why": "Threats of FIRs, court cases or arrest over a message are a pressure tactic. Real legal process does not arrive by WhatsApp.",
    "weight": 2,
    "re": "\\bf\\.?i\\.?r\\.?\\b|legal action|police (?:case|complaint|action)|(?:court|arrest) (?:case|warrant|notice)|cyber ?crime"
  },
  {
    "id": "SIGHT_UNSEEN",
    "name": "Asks for rent before you have seen the place",
    "why": "Paying a token or advance before visiting is how fake listings work. The photos are usually taken from a real listing elsewhere.",
    "weight": 3,
    "re": "(?:token|advance|booking) (?:amount|money|fee).{0,40}(?:before|without) .{0,20}(?:visit|see)|(?:i am|i'm|currently) (?:abroad|out of (?:town|country)|in another city).{0,60}(?:send|transfer|pay)|book (?:it )?(?:now|today) .{0,20}without (?:a )?visit"
  },
  {
    "id": "COURIER_CUSTOMS",
    "name": "Parcel held, pay a fee to release it",
    "why": "Couriers do not hold parcels for a fee over SMS. Customs duty is paid to the government, never to a WhatsApp number.",
    "weight": 3,
    "re": "(?:parcel|package|courier|shipment|consignment).{0,40}(?:held|stuck|seized|customs|clearance)|customs (?:duty|clearance|charge).{0,30}(?:pay|transfer)|(?:fedex|dhl|bluedart|india post).{0,40}(?:pay|fee|charge)"
  },
  {
    "id": "ELECTRICITY_CUT",
    "name": "Electricity disconnection threat",
    "why": "Power utilities do not warn you by SMS from a personal number, and they never ask you to call one to avoid disconnection tonight.",
    "weight": 3,
    "re": "electricity .{0,30}(?:disconnect|cut off|discontinue)|power .{0,20}(?:will be )?disconnect|bill .{0,20}not updated.{0,30}disconnect"
  },
  {
    "id": "LOTTERY_WIN",
    "name": "A prize you never entered for",
    "why": "You cannot win a lottery you never entered. Every version of this ends with a fee to release the winnings.",
    "weight": 4,
    "re": "(?:won|winner).{0,30}(?:lottery|lucky draw|prize|kbc)|\\bkbc\\b|lucky (?:winner|draw)|congratulations.{0,30}\\bwon\\b"
  },
  {
    "id": "LOAN_HARASSMENT",
    "name": "Loan-app style pressure",
    "why": "Threatening to contact your phonebook over a loan is illegal recovery practice, not a legitimate demand.",
    "weight": 3,
    "re": "(?:inform|contact|call).{0,25}(?:your )?(?:contacts|family|friends|relatives).{0,30}(?:loan|due|payment)|loan .{0,25}(?:overdue|default).{0,30}(?:legal|action|contacts)|defaulter.{0,30}(?:list|notice)"
  },
  {
    "id": "INVESTMENT_TIP",
    "name": "Guaranteed returns or a tips group",
    "why": "Guaranteed returns do not exist. Groups offering them exist to take deposits that cannot be withdrawn.",
    "weight": 3,
    "re": "guaranteed (?:returns?|profit|income)|(?:double|triple) your money|(?:stock|trading|crypto|forex) (?:tips?|group|signals?)|\\b\\d{2,3}% (?:returns?|profit)"
  },
  {
    "id": "TASK_COMMISSION",
    "name": "Prepaid task or commission work",
    "why": "Task scams start with small payouts that work, then ask you to deposit for a bigger task. The deposit is the point.",
    "weight": 3,
    "re": "(?:complete|do) .{0,20}tasks?.{0,30}(?:earn|commission|payout)|(?:like|subscribe|rate).{0,25}(?:videos?|hotels?|products?).{0,30}(?:earn|paid|commission)|prepaid task|recharge .{0,20}to (?:unlock|continue).{0,20}task"
  },
  {
    "id": "ARMY_OFFICER",
    "name": "Claims to be posted far away and cannot meet",
    "why": "The soldier-being-transferred story is the oldest marketplace scam in India. It exists to explain why you must pay before meeting.",
    "weight": 3,
    "re": "(?:army|military|cisf|crpf|bsf|navy) (?:officer|jawan|personnel)|(?:posted|deployed) (?:in|at) .{0,30}(?:cannot|can't) (?:meet|come)|transfer(?:red)? .{0,25}urgent(?:ly)? .{0,25}sell"
  }
];
window.PAKKA_BANDS = [[8, "almost_certainly", "Almost certainly a scam"], [5, "likely", "Likely a scam"], [2, "careful", "Be careful"], [1, "one_flag", "One thing to check"], [0, "clear", "Nothing suspicious found"]];

window.pakkaEvaluate = function (text) {
  const findings = [];
  for (const r of window.PAKKA_RULES) {
    const re = new RegExp(r.re, 'gi');
    const spans = [];
    let m;
    while ((m = re.exec(text)) !== null) {
      if (m[0] === '') { re.lastIndex++; continue; }
      spans.push([m.index, m.index + m[0].length]);
    }
    if (spans.length) findings.push({
      id: r.id, name: r.name, why: r.why, weight: r.weight,
      spans, quotes: spans.map(([a, b]) => text.slice(a, b)),
    });
  }
  const score = findings.reduce((s, f) => s + f.weight, 0);
  const [, band, label] = window.PAKKA_BANDS.find(([t]) => score >= t);
  findings.sort((a, b) => b.weight - a.weight);
  return { text, score, band, label, findings, rules_checked: window.PAKKA_RULES.length };
};
