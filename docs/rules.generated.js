/* Generated from api/rules.py by tools/build_rules_js.py — do not edit.
   Running the check here means the message never leaves the device unless the
   person presses Share. */
window.PAKKA_RULES = [
  {
    "id": "PAY_TO_GET_JOB",
    "name": "Asks for money before a job",
    "why": "A real employer never charges you to be hired. Registration, training and security fees are the oldest job scam there is.",
    "weight": 3,
    "re": "registration fee|security (?:fee|deposit|amount)|processing fee|training fee|refundable (?:fee|deposit|amount)|joining fee|(?:have to|need to|must|kindly|please) pay (?:rs\\.?|₹)?\\s?[\\d,]+|\\bpay (?:rs\\.?|₹)\\s?[\\d,]+ (?:to|for) (?:confirm|secure|book|get|join|start|activat)"
  },
  {
    "id": "ASKS_FOR_SECRET",
    "name": "Asks for an OTP, PIN or password",
    "why": "Nobody legitimate will ever ask for your OTP, UPI PIN, CVV or password — not your bank, not a delivery agent, not HR.",
    "weight": 4,
    "re": "(?:share|send|tell|give|provide|forward|confirm|read out)\\s+(?:me\\s+|us\\s+|the\\s+|your\\s+)*\\b(?:otp|cvv|pin|password|code)\\b|\\b(?:otp|cvv|pin)\\b.{0,25}(?:with (?:our|the|me|us)|to (?:our|the|me|us|verify))|what(?:'s| is) (?:your |the )?(?:otp|cvv|pin)\\b|\\bcvv\\b.{0,20}(?:number|digits)|\\bupi pin\\b|\\batm pin\\b|share (?:your )?password|\\bnet ?banking password\\b"
  },
  {
    "id": "PAY_TO_RECEIVE",
    "name": "Asks you to pay to receive money",
    "why": "You are being asked to send money to unlock money. Refunds, prizes and lottery winnings never require a payment from you first.",
    "weight": 4,
    "re": "pay .{0,30}to (?:claim|release|receive|unlock)|(?:claim|release|receive) .{0,30}after (?:payment|paying)|processing charge .{0,20}refund|to receive your (?:prize|refund|winnings)|pay .{0,25}(?:delivery|shipping|handling|courier) charge"
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
    "re": "within \\d+ ?(?:hours?|hrs?|minutes?|mins?)|today only|last chance|(?:block|suspend|deactivat|expir|clos|disconnect|cancel|terminat)\\w*\\s+(?:with)?in\\s+\\d+\\s*(?:hours?|hrs?|days?|minutes?)|expires? (?:today|tonight|soon)|immediately|hurry|\\burgently\\b|limited (?:slots?|seats?|offer)|only \\d+ (?:slots?|seats?) left|before (?:you )?(?:lose|miss)|\\b(?:click|claim|act|apply) (?:it |this |here |the link )?now\\b"
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
    "re": "(?:won|winner).{0,30}(?:lottery|lucky draw|prize|kbc)|\\bkbc\\b|lucky (?:winner|draw)|congratulations.{0,30}\\b(?:won|winning|winner)\\b|\\b(?:won|winning|win a)\\b.{0,40}(?:iphone|mac ?book|laptop|smartphone|scooter|\\bcar\\b|\\bbike\\b|gift (?:card|voucher|hamper)|voucher|cash prize|\\bgift\\b)|\\bfree\\b.{0,20}(?:iphone|mac ?book|laptop|smartphone|\\bcar\\b|scooter|\\bbike\\b)"
  },
  {
    "id": "QR_SCAN",
    "name": "A QR code to receive money",
    "why": "Scanning a QR code can only send money out of your account. It can never bring money in. Anyone telling you to scan one to claim, collect or receive something is describing a thing that cannot happen.",
    "weight": 3,
    "re": "scan .{0,25}\\bqr\\b.{0,40}(?:claim|collect|receive your|get your|refund|prize|reward|cashback|winnings|the offer)|\\bqr code\\b.{0,30}(?:to )?(?:claim|collect|receive your|get your)|(?:claim|collect|receive) .{0,30}(?:by |through |via )?scanning"
  },
  {
    "id": "REMOTE_ACCESS",
    "name": "Wants to see or control your screen",
    "why": "No bank, no support desk and no government office will ever ask you to install a screen sharing app. Someone watching your screen sees your banking app and your PIN as you type it.",
    "weight": 4,
    "re": "\\b(?:any ?desk|team ?viewer|quick ?support|rust ?desk|ammyy|air ?droid)\\b|screen[- ]?shar(?:e|ing)|share your screen|mirror your (?:screen|phone)"
  },
  {
    "id": "APK_INSTALL",
    "name": "Wants you to install an app from outside the store",
    "why": "An app sent to you as a file has not been checked by anyone. This is how banking trojans get onto phones in India.",
    "weight": 4,
    "re": "\\bapk\\b|(?:install|download|sideload) .{0,30}(?:from|via|through) (?:this |the )?link|enable (?:unknown sources|installation from unknown)"
  },
  {
    "id": "LOOKALIKE_DOMAIN",
    "name": "A web address dressed up as a real company",
    "why": "The brand name is in the address but the domain is not theirs. Real organisations send you to their own domain, not a lookalike.",
    "weight": 3,
    "re": "https?://[^\\s]*\\b(?:sbi|hdfc|icici|axis|kotak|paytm|phonepe|amazon|flipkart|netflix|irctc|epfo|uidai|income ?tax|indiapost)[-_][a-z0-9-]+\\.|https?://[^\\s]*\\b(?:sbi|hdfc|icici|axis|paytm|phonepe|amazon|flipkart|netflix|irctc|epfo|uidai)[^\\s]*\\.(?:xyz|info|top|online|site|club|icu|buzz|link|shop|tk|ml|ga|cf)\\b|https?://[^\\s]*(?:amaz0n|g00gle|paypa1|fl1pkart|1cici|hdfc-bank)"
  },
  {
    "id": "VERIFY_DETAILS",
    "name": "Wants your details to avoid something bad",
    "why": "Being told to confirm your details to stop something bad happening is the oldest phishing shape there is. If it is real, it will still be there when you open the app yourself.",
    "weight": 2,
    "re": "(?:click|tap|open|visit) .{0,30}(?:link|here|below|url).{0,40}(?:verify|update|confirm|activate|re-?activate|avoid|prevent|suspend)|(?:verify|update|confirm) (?:your )?(?:\\w+ )?(?:account|details|kyc|card details|bank details|information).{0,30}(?:here|link|below|now|immediately|https?://)"
  },
  {
    "id": "ID_DOCUMENTS",
    "name": "Asks for your Aadhaar or PAN",
    "why": "A photo of your Aadhaar or PAN is enough to open accounts and take loans in your name. Nobody legitimate collects it over a chat message.",
    "weight": 3,
    "re": "(?:photo|copy|scan|pic|image|soft copy) .{0,25}(?:of )?(?:your )?(?:aadhaar|aadhar|pan card|passport|voter id|driving licen[cs]e)|(?:send|share|whatsapp|forward) .{0,25}\\b(?:aadhaar|aadhar|pan card)\\b|selfie .{0,30}(?:with|holding) .{0,20}(?:aadhaar|aadhar|pan|id)|(?:aadhaar|aadhar|pan card).{0,30}(?:and|\\+) .{0,15}selfie"
  },
  {
    "id": "CALLBACK_NUMBER",
    "name": "A personal mobile posing as a helpline",
    "why": "Real companies publish landlines or 1800 numbers you can look up. A ten digit mobile presented as customer care belongs to a person, not a bank.",
    "weight": 2,
    "re": "(?:customer care|help ?line|support number|official number|toll ?free)[^\\d]{0,25}\\b[6-9]\\d{9}\\b|\\b[6-9]\\d{9}\\b[^\\d]{0,25}(?:customer care|help ?line)|call (?:this|our|the above) number.{0,25}(?:to |and )?(?:cancel|stop|block|verify|reverse|claim|confirm)"
  },
  {
    "id": "COLLECT_REQUEST",
    "name": "Asks you to approve something to receive money",
    "why": "Entering your PIN or approving a request always sends money out. It can never bring money in. Anyone saying otherwise is taking, not giving.",
    "weight": 4,
    "re": "(?:accept|approve) .{0,25}request.{0,30}(?:receive|get|credit)|(?:enter|put|type) (?:your )?(?:upi )?pin.{0,30}(?:receive|get|credit|refund)|credited .{0,40}(?:click|withdraw|claim)|(?:click|tap) .{0,20}(?:here|link).{0,25}(?:to )?(?:withdraw|claim) .{0,20}(?:amount|money|cashback|reward)"
  },
  {
    "id": "STRANGER_OPENER",
    "name": "A stranger opening with money talk",
    "why": "The wrong number that turns into a friendship that turns into an investment app. It starts exactly like this, every time.",
    "weight": 2,
    "re": "(?:got|found|received|saved) your (?:number|contact) from|(?:i am|i'm|this is) \\w+,? .{0,40}(?:trade|trading|crypto|forex|investment|profit|returns)"
  },
  {
    "id": "ADVANCE_FEE",
    "name": "An inheritance or fortune from a stranger",
    "why": "Nobody picks a stranger to receive a fortune. The money does not exist, and the fees you are asked for along the way are the entire point.",
    "weight": 3,
    "re": "\\b(?:widow|late husband|late father|inheritance|next of kin|beneficiary)\\b.{0,60}(?:million|billion|fund|money|donate|\\$)|(?:transfer|donate|share) .{0,30}(?:\\$\\s?\\d|usd|million dollars|billion)|trustworthy person|\\bnext of kin\\b"
  },
  {
    "id": "BANK_DETAILS",
    "name": "Wants your account number to send you money",
    "why": "Money already owed to you goes to the account it came from. Being asked for fresh bank details is how the account gets emptied, not filled.",
    "weight": 3,
    "re": "(?:refund|amount|salary|payment|prize|claim).{0,60}(?:submit|share|send|provide|enter|fill) .{0,25}(?:bank account|account number|account details|ifsc)|(?:bank account|account number|ifsc).{0,40}(?:to )?(?:receive|claim) (?:your |the )?(?:refund|prize|amount|winnings|money)"
  },
  {
    "id": "SIM_BLOCK",
    "name": "Threatens to block your SIM or connection",
    "why": "Your operator does not disconnect you over a text with a link. The panic is the product.",
    "weight": 3,
    "re": "(?:sim(?: card)?|mobile number|connection|outgoing).{0,30}(?:will be |going to be |about to be )?(?:block|deactivat|disconnect|barred|suspend)"
  },
  {
    "id": "NEW_NUMBER",
    "name": "A new number that needs money",
    "why": "Someone claiming a new number and then asking for money is how a family member's identity gets borrowed. Call them on the number you already have.",
    "weight": 3,
    "re": "(?:this is|it'?s) (?:my |me,? )?(?:new|changed) number.{0,120}(?:send|transfer|urgent|money|pay\\b|rs\\.?\\s?\\d|\\u20b9)|\\b(?:mom|mum|mummy|dad|papa|mama)\\b.{0,60}\\bnew number\\b.{0,120}(?:send|transfer|urgent|money|pay\\b|rs\\.?\\s?\\d)|(?:lost|broke|damaged|changed) my phone.{0,80}(?:send|transfer|money|rs\\.?\\s?\\d)"
  },
  {
    "id": "STRANDED_PLEA",
    "name": "Stranded somewhere and needs money now",
    "why": "A hijacked account of someone you know, or a stranger who knows the story works. Call the person on the number you already have.",
    "weight": 2,
    "re": "(?:stuck|stranded|trapped) (?:in|at) \\w+.{0,60}(?:send|transfer|need) .{0,15}money|lost my (?:wallet|phone|passport|bag).{0,60}(?:send|transfer|need) .{0,20}money"
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
window.PAKKA_ADVICE = {
  "clause": {
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
    "ARMY_OFFICER": "it uses the posted-far-away story to avoid meeting"
  },
  "money": [
    "ADVANCE_FEE",
    "BANK_DETAILS",
    "COLLECT_REQUEST",
    "COURIER_CUSTOMS",
    "INVESTMENT_TIP",
    "LOTTERY_WIN",
    "PAY_TO_GET_JOB",
    "PAY_TO_RECEIVE",
    "PERSONAL_PAYMENT",
    "QR_SCAN",
    "TASK_COMMISSION"
  ],
  "job": [
    "NO_INTERVIEW",
    "PAY_TO_GET_JOB",
    "TASK_COMMISSION",
    "TOO_GOOD"
  ],
  "impersonation": [
    "APK_INSTALL",
    "CALLBACK_NUMBER",
    "COURIER_CUSTOMS",
    "ELECTRICITY_CUT",
    "KYC_PANIC",
    "LOAN_HARASSMENT",
    "LOOKALIKE_DOMAIN",
    "REMOTE_ACCESS",
    "SIM_BLOCK",
    "THREAT",
    "VERIFY_DETAILS"
  ],
  "property": [
    "ARMY_OFFICER",
    "SIGHT_UNSEEN"
  ]
};
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
