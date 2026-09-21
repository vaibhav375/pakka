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
    "re": "(?:share|send|tell|give|provide|forward|confirm|read out)\\s+(?:me\\s+|us\\s+|the\\s+|your\\s+)*\\b(?:otp|cvv|pin|password|code)\\b(?!\\s*(?:is\\s*)?\\d{4,8})|\\b(?:apna|apne) otp\\b|(?:अपना|अपनी)?\\s*(?:ओटीपी|ओ\\.?टी\\.?पी)|(?:पिन|पासवर्ड)\\s*(?:बताइए|बताएं|भेजिए|शेयर)|\\botp\\b .{0,15}(?:bhej|batao|bataiye|share kij)|\\b(?:otp|cvv|pin)\\b.{0,25}(?:with (?:our|the|me|us)|to (?:our|the|me|us|verify))|what(?:'s| is) (?:your |the )?(?:otp|cvv|pin)\\b|\\bcvv\\b.{0,20}(?:number|digits)|\\bupi pin\\b|\\batm pin\\b|share (?:your )?password|\\bnet ?banking password\\b"
  },
  {
    "id": "PAY_TO_RECEIVE",
    "name": "Asks you to pay to receive money",
    "why": "You are being asked to send money to unlock money. Refunds, prizes and lottery winnings never require a payment from you first.",
    "weight": 4,
    "re": "pay .{0,30}to (?:claim|release|receive|unlock)|(?:claim|release|receive) .{0,30}after (?:payment|paying)|processing charge .{0,20}refund|to receive your (?:prize|refund|winnings)|pay .{0,25}(?:delivery|shipping|handling|courier) charge|(?:फीस|शुल्क|पैसे|रकम).{0,20}(?:भेज|जमा|ट्रांसफर)"
  },
  {
    "id": "KYC_PANIC",
    "name": "KYC or account-block scare",
    "why": "Banks do not block accounts over SMS links. This is the most common phishing script in India right now.",
    "weight": 3,
    "re": "kyc .{0,25}(?:expire|pending|suspend|incomplete|not (?:done|updated))|(?:needs?|requires?) .{0,20}kyc|immediate kyc|account .{0,30}(?:will be |has been )?(?:block|suspend|freeze|deactivat)|(?:update|complete|verify) .{0,20}kyc .{0,40}(?:\\bor\\b|else|otherwise|to avoid|immediately|now|today|link|http|block|suspend|frozen)|(?:account|khata|kyc).{0,30}(?:block|band) ho jayega|kyc update nahi|केवाईसी|\\bkyc\\b.{0,25}(?:तुरंत|पूरा कर|अपडेट कर|करें)|(?:तुरंत|जल्दी).{0,20}\\bkyc\\b|(?:खाता|अकाउंट).{0,20}(?:ब्लॉक|बंद|बाधित)"
  },
  {
    "id": "URGENCY",
    "name": "Manufactured urgency",
    "why": "Pressure to act within hours exists to stop you checking. Anything genuine will still be there tomorrow.",
    "weight": 1,
    "re": "within \\d+ ?(?:hours?|hrs?|minutes?|mins?)|today only|last chance|(?:block|suspend|deactivat|expir|clos|disconnect|cancel|terminat)\\w*\\s+(?:with)?in\\s+\\d+\\s*(?:hours?|hrs?|days?|minutes?)|expires? (?:today|tonight|soon)|immediately|hurry|\\burgently\\b|\\bturant\\b|\\bjaldi\\b|urgent hai|तुरंत|जल्दी|अभी\\s*(?:ही|करें)|\\b(?:claim|collect|redeem|grab) (?:your |the |it )?(?:\\w+ ){0,3}\\bnow\\b|limited (?:slots?|seats?|offer|time|period)|only \\d+ (?:slots?|seats?) left|before (?:you )?(?:lose|miss)|\\b(?:click|claim|act|apply) (?:it |this |here |the link )?now\\b"
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
    "re": "(?:rs\\.?|₹)\\s?[1-9]\\d{3,}[^.]{0,30}(?:per day|/day|daily|per week)|earn (?:rs\\.?|₹)\\s?\\d[\\d,]*.{0,25}(?:from home|part[- ]?time|\\d ?(?:hours?|hrs?))|\\d ?(?:hours?|hrs?) (?:work )?daily.{0,25}(?:rs\\.?|₹)\\s?\\d|ghar baithe .{0,25}kama|(?:rupaye|rupay) (?:daily|roz|rozana)|घर बैठे.{0,25}कमा|(?:रोज|रोजाना|प्रतिदिन).{0,25}रुपये"
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
    "id": "BARE_LINK",
    "name": "A link with nowhere named",
    "why": "Messages you can trust say where they are sending you, by name. \"This link\" is the whole address you are given.",
    "weight": 1,
    "re": "(?:click|tap|open)(?:ing)? (?:on )?(?:this|the|below|following|attached) link|link (?:par|pe) click|(?:इस|नीचे|दिए गए)\\s*लिंक पर\\s*क्लिक"
  },
  {
    "id": "CHAT_ONLY",
    "name": "Exists only on WhatsApp or Telegram",
    "why": "No office, no website, no landline — only a chat window. There is nothing to hold accountable afterwards.",
    "weight": 1,
    "re": "(?:contact|message|ping|dm|reach) (?:me |us )?(?:only )?on (?:whats ?app|telegram)|join (?:our )?telegram|whats ?app (?:only|me at)|(?:whats ?app|telegram) par (?:contact|message|baat|kare)|(?:व्हाट्सएप|व्हाट्सऐप|टेलीग्राम).{0,20}(?:करें|कीजिए|संपर्क)"
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
    "re": "(?:token|advance|booking) (?:amount|money|fee).{0,40}(?:before|without) .{0,20}(?:visit|see)|(?:i am|i'm|currently) (?:abroad|out of (?:town|country|station)|in another city|not in the city).{0,60}(?:send|transfer|pay)|book (?:it )?(?:now|today) .{0,20}without (?:a )?visit|(?:advance|token|booking).{0,40}(?:to )?(?:block|hold|reserve) the (?:room|bed|flat|house|pg)|pay .{0,25}(?:booking|advance|token).{0,30}before visit"
  },
  {
    "id": "COURIER_CUSTOMS",
    "name": "Parcel held, pay a fee to release it",
    "why": "Couriers do not hold parcels for a fee over SMS. Customs duty is paid to the government, never to a WhatsApp number.",
    "weight": 3,
    "re": "(?:parcel|package|courier|shipment|consignment).{0,40}(?:held|on hold|stuck|seized|customs|clearance|detained)|customs (?:fee|duty|charge|clearance)|customs (?:duty|clearance|charge).{0,30}(?:pay|transfer)|(?:fedex|dhl|bluedart|india post).{0,40}(?:pay|fee|charge)"
  },
  {
    "id": "ELECTRICITY_CUT",
    "name": "Electricity disconnection threat",
    "why": "Power utilities do not warn you by SMS from a personal number, and they never ask you to call one to avoid disconnection tonight.",
    "weight": 3,
    "re": "electricity .{0,30}(?:disconnect|cut off|discontinue)|बिजली.{0,30}(?:काट|कट|बंद)|(?:power|electricity)(?: supply| connection)?.{0,30}(?:cut off|cut-off|switched off)|power .{0,20}(?:will be )?disconnect|bill .{0,20}not updated.{0,30}disconnect"
  },
  {
    "id": "LOTTERY_WIN",
    "name": "A prize you never entered for",
    "why": "You cannot win a lottery you never entered. Every version of this ends with a fee to release the winnings.",
    "weight": 4,
    "re": "(?:won|winner).{0,30}(?:lottery|lucky draw|prize|kbc)|\\bkbc\\b|lucky (?:winner|draw)|congratulations.{0,30}\\b(?:won|winning|winner)\\b.{0,50}(?:\\brs\\.?\\s*\\d|₹|lakh|crore|lottery|lucky draw|prize|gift|iphone|mac ?book|laptop|\\bcar\\b|voucher|hamper)|lottery lag gay|\\bjeeta hai\\b|(?:लॉटरी|इनाम|लकी ड्रॉ)|बधाई.{0,30}(?:जीत|इनाम|लाख|करोड़)|(?:lakh|crore) rupaye jeet|\\b(?:won|winning|win a)\\b.{0,40}(?:iphone|mac ?book|laptop|smartphone|scooter|\\bcar\\b|\\bbike\\b|gift (?:card|voucher|hamper)|voucher|cash prize|\\bgift\\b)|\\bfree\\b\\s+(?:\\w+\\s+){0,2}(?:iphone|ipad|tablet|laptop|mac ?book|smartphone|\\bphone\\b|\\btv\\b|television|smart ?watch|airpods|headphones|\\bcar\\b|scooter|\\bbike\\b|subscription|recharge|data pack|membership)"
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
    "re": "https?://[^\\s]*\\b(?:sbi|hdfc|icici|axis|kotak|pnb|canara|bob|rbi|lic|paytm|phonepe|amazon|flipkart|myntra|meesho|nykaa|bigbasket|swiggy|zomato|ola|uber|jio|airtel|\\bvi\\b|vodafone|bsnl|tata|netflix|irctc|epfo|uidai|income ?tax|indiapost)[-_][a-z0-9-]+\\.|https?://[^\\s]*\\b(?:sbi|hdfc|icici|axis|paytm|phonepe|amazon|flipkart|netflix|irctc|epfo|uidai)[^\\s]*\\.(?:xyz|info|top|online|site|club|icu|buzz|link|shop|tk|ml|ga|cf)\\b|https?://[^\\s]*\\bhdfc-bank\\b"
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
    "re": "(?:customer care|help ?line|support number|official number|toll ?free)[^\\d]{0,25}\\b[6-9]\\d{9}\\b|\\b[6-9]\\d{9}\\b[^\\d]{0,25}(?:customer care|help ?line)|call\\s+(?:\\+?91[- ]?)?[6-9]\\d{9}\\b.{0,30}(?:to |and )?(?:claim|verify|confirm|cancel|reverse|block|activate|process)|call (?:this|our|the above) number.{0,25}(?:to |and )?(?:cancel|stop|block|verify|reverse|claim|confirm)"
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
    "re": "(?:got|found|received|saved) your (?:number|contact) from|(?:sorry|sry|oops),? .{0,20}wrong number|wrong number.{0,90}(?:trade|trading|crypto|forex|invest|profit|teach you)|(?:i am|i'm|this is) \\w+,? .{0,40}(?:trade|trading|crypto|forex|investment|profit|returns)"
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
    "re": "(?:this is|it'?s) (?:my |me,? )?(?:new|changed) number.{0,120}(?:send|transfer|urgent|money|pay\\b|rs\\.?\\s?\\d|\\u20b9)|\\b(?:mom|mum|mummy|dad|papa|mama)\\b.{0,60}\\bnew number\\b.{0,120}(?:send|transfer|urgent|money|pay\\b|rs\\.?\\s?\\d)|(?:lost|broke|damaged|changed) my phone.{0,80}(?:send|transfer|money|rs\\.?\\s?\\d)|(?:mera|mere) naya number.{0,120}(?:bhej|rupaye|rupay|paise|transfer|urgent)|purana phone (?:kho gaya|kharab)|(?:मेरा|यह) नया नंबर.{0,80}(?:भेज|रुपये|पैसे|तुरंत)"
  },
  {
    "id": "STRANDED_PLEA",
    "name": "Stranded somewhere and needs money now",
    "why": "A hijacked account of someone you know, or a stranger who knows the story works. Call the person on the number you already have.",
    "weight": 2,
    "re": "(?:stuck|stranded|trapped) (?:in|at) \\w+.{0,60}(?:send|transfer|need) .{0,15}money|lost my (?:wallet|phone|passport|bag).{0,60}(?:send|transfer|need) .{0,20}money"
  },
  {
    "id": "LOOKALIKE_URL",
    "name": "A web address that is not the characters it appears to be",
    "why": "Letters from another alphabet, punycode, digits inside a brand name or a bare IP address. The address reads correctly to a person and goes somewhere else.",
    "weight": 3,
    "re": "(?!x)x"
  },
  {
    "id": "UNUSUAL_LOGIN",
    "name": "An alarm about your account, with a link attached",
    "why": "Banks do tell you about a new device. They do not put the fix behind a link in the message. The alarm is real, the link is the scam.",
    "weight": 3,
    "re": "(?:unusual|unauthori[sz]ed|suspicious|new device) (?:login|sign[- ]?in|access|activity)|(?:login|sign[- ]?in) (?:detected|attempt).{0,40}(?:new|unknown|another) device|secure your account.{0,40}https?://"
  },
  {
    "id": "GOVT_GRANT",
    "name": "A government payout you never applied for",
    "why": "No ministry selects people for money by SMS. Every real scheme has an application you made and a portal you log into yourself.",
    "weight": 3,
    "re": "(?:pmo|prime minister|ministry|govt|government|\\brbi\\b)\\b.{0,50}(?:selected|eligible|entitled|approved).{0,30}(?:grant|scheme|yojana|subsidy|fund)|(?:selected|eligible|entitled) for .{0,25}(?:₹|rs\\.?)\\s?[\\d,]+|(?:pm|pradhan mantri) .{0,20}yojana.{0,40}(?:claim|apply|register|call)|unclaimed (?:refund|amount|deposit|fund)|(?:pm|pradhan mantri|ayushman|jan dhan|ujjwala|kisan samman|digital (?:bharat|india)|skill india|\\bpmay\\b|\\bpmjay\\b)[\\w\\s]{0,30}(?:subsidy|scheme|yojana|card|grant|nidhi|extension|upgrade|approved|selected)|(?:selected|approved|eligible)[\\w\\s,]{0,30}(?:pm|pradhan mantri|ayushman|government|govt)[\\w\\s]{0,25}(?:scheme|yojana|subsidy|card|grant)"
  },
  {
    "id": "ROMANCE_BAIT",
    "name": "A stranger opening with flattery",
    "why": "A profile you never posted, seen by someone who will move you to another app and then to money. It always starts as attention.",
    "weight": 2,
    "re": "(?:saw|liked|viewed) your (?:profile|photo|picture|pic)\\b.{0,50}(?:chat|meet|reply|message|whats ?app)|(?:single|hot|lonely) (?:women|men|girls|guys|ladies).{0,50}(?:waiting|near you|meet|chat|call)|\\b(?:hi|hey|hello) (?:beautiful|handsome|sexy|dear)\\b.{0,70}(?:reply|chat|call|whats ?app|profile)"
  },
  {
    "id": "TXN_ALERT_BAIT",
    "name": "A charge you did not make, with the fix attached",
    "why": "Your bank does tell you about a transaction. It does not put the way to cancel it in the same message. The alarm is real, the link is not.",
    "weight": 4,
    "re": "(?:if (?:this|it) (?:is|was) not you|not you\\?|if not (?:you|done by you)).{0,70}(?:click|tap|\\bhttps?://|\\bwww\\.|\\b[6-9]\\d{9}\\b|this link|the link)|(?:click|tap) .{0,30}(?:to )?(?:cancel|reverse|stop) (?:the )?transaction"
  },
  {
    "id": "REWARD_EXPIRY",
    "name": "Points or cashback about to expire",
    "why": "Reward points do not need a link in a text message to redeem. The deadline exists so you move before you think.",
    "weight": 3,
    "re": "(?:reward|loyalty|credit card|bonus)\\s*points?\\b.{0,50}(?:expir|lapse|redeem|claim)|(?:cashback|reward|points?).{0,40}(?:expire|expiring|lapse)\\w*\\s*(?:today|tonight|soon|in \\d+)|redeem .{0,30}(?:before|within) .{0,20}(?:today|tonight|midnight|\\d+ ?(?:hours?|days?))"
  },
  {
    "id": "DIGITAL_ARREST",
    "name": "An arrest or investigation run over a call",
    "why": "There is no such thing as a digital arrest in Indian law. No officer investigates you by video call, and none of them will ask you to move money to prove you are innocent.",
    "weight": 4,
    "re": "digital(?:ly)? arrest|(?:stay|remain) on (?:this |the )?(?:video )?call.{0,40}(?:until|till|24)|(?:transfer|deposit|move) .{0,40}(?:funds?|money|amount).{0,40}(?:for )?verification|(?:rbi|reserve bank|supreme court|cbi|police|customs) .{0,20}(?:escrow|verification) account|(?:section \\d+|\\bipc\\b|\\bndps\\b|money laundering).{0,60}(?:jail|arrest|warrant|aadhaar|pan\\b)|(?:aadhaar|aadhar|pan card).{0,50}(?:linked to|used in|found in).{0,40}(?:parcel|drug|case|laundering|illegal)"
  },
  {
    "id": "SECRECY",
    "name": "Asks you to keep it from your family",
    "why": "Every honest institution is happy for you to ask someone. Being told not to is the tell, and it is there because the person you would ask would stop this.",
    "weight": 3,
    "re": "(?:do not|don'?t|never) (?:tell|inform|call|contact|involve|discuss (?:this|it) with)\\s*(?:your )?(?:family|anyone|anybody|wife|husband|parents|father|mother|friends|police)|keep (?:this|it) (?:strictly )?(?:confidential|secret|between us)|\\bsub[- ]?judice\\b"
  },
  {
    "id": "SERVICE_SUSPENDED",
    "name": "A service you use, suddenly suspended",
    "why": "Suspension notices that arrive with a link are the shape phishing takes. The real thing is in the app you already have.",
    "weight": 3,
    "re": "(?:your |the )?(?:upi(?: id)?|aadhaar|aadhar|pan card|netbanking|net banking|wallet|debit card|credit card|account)\\b.{0,40}(?:has been|have been|is|are|will be)\\s*(?:temporarily\\s*|permanently\\s*)?(?:suspend|deactivat|block|freez|restrict)|(?:suspicious|unusual) activity .{0,40}(?:card|account).{0,40}(?:blocked|suspended|restricted)"
  },
  {
    "id": "DELIVERY_ADDRESS",
    "name": "A delivery that failed and wants your details",
    "why": "A courier that cannot find you leaves a slip or calls. It does not ask you to retype your address into a link on a deadline.",
    "weight": 3,
    "re": "(?:could not|couldn'?t|unable to|failed to|attempted) .{0,30}deliver\\w*.{0,80}(?:update|confirm|verify|re-?schedule|correct)|(?:update|confirm|verify) .{0,25}(?:delivery )?(?:address|location).{0,50}(?:within|before|or|link|http)|(?:incomplete|incorrect|wrong) address.{0,60}(?:update|confirm|link|http)"
  },
  {
    "id": "CHALLAN",
    "name": "A traffic fine that arrives by link",
    "why": "A challan lives on the Parivahan portal and you go and look it up. It is not sent to you as a download, and it does not threaten you with a court case by SMS.",
    "weight": 3,
    "re": "(?:e-?challan|traffic challan|\\bchallan\\b).{0,60}(?:pending|download|pay|link|http|जमा|भुगतान|डाउनलोड|पेंडिंग|बकाया)|(?:vehicle|गाड़ी|वाहन).{0,40}(?:challan|चालान).{0,50}(?:pending|pay|legal|पेंडिंग|भुगतान|कानूनी)|चालान.{0,60}(?:कानूनी कार्रवाई|तुरंत भुगतान)|(?:ई-?)?चालान.{0,40}(?:डाउनलोड|भुगतान|पेंडिंग|जमा|करें)"
  },
  {
    "id": "BILL_UPDATE",
    "name": "Asks you to update a bill",
    "why": "A bill is paid, never updated. The word is there because the message needs you to open something, and there is nothing in a real bill to update.",
    "weight": 3,
    "re": "(?:update|updation of|updating) .{0,25}(?:electricity |power |gas |water |mobile |phone )?bill\\b|bill\\b.{0,20}(?:is )?not updated|(?:बिल|bill)\\s*(?:को\\s*)?(?:अपडेट|अद्यतन)|(?:अपडेट|अद्यतन).{0,20}(?:बिल|bill)"
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
    "re": "(?:army|military|cisf|crpf|bsf|navy) (?:officer|jawan|personnel)|\\b(?:major|colonel|captain|subedar|havildar|brigadier) [a-z]\\w+|(?:posted|deployed) (?:in|at) .{0,40}(?:cannot|can't|unable to) (?:meet|come|visit|see)|transfer(?:red)? .{0,25}urgent(?:ly)? .{0,25}sell"
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
window.PAKKA_HI = {
 "bands": {
  "almost_certainly": "लगभग निश्चित रूप से धोखाधड़ी",
  "likely": "शायद धोखाधड़ी है",
  "careful": "सावधान रहें",
  "one_flag": "एक बात खटकती है",
  "clear": "कुछ संदिग्ध नहीं मिला"
 },
 "rules": {
  "PAY_TO_GET_JOB": [
   "नौकरी से पहले पैसे मांगे जा रहे हैं",
   "असली कंपनी नौकरी देने के लिए पैसे नहीं लेती। रजिस्ट्रेशन, ट्रेनिंग और सिक्योरिटी फीस सबसे पुराना जॉब स्कैम है।"
  ],
  "ASKS_FOR_SECRET": [
   "ओटीपी, पिन या पासवर्ड मांगा जा रहा है",
   "कोई भी सही संस्था कभी आपका ओटीपी, यूपीआई पिन, सीवीवी या पासवर्ड नहीं मांगती। न बैंक, न डिलीवरी वाला, न एचआर।"
  ],
  "PAY_TO_RECEIVE": [
   "पैसे पाने के लिए पैसे मांगे जा रहे हैं",
   "आपका अपना पैसा पाने के लिए पहले कुछ भेजना कभी ज़रूरी नहीं होता। यही पूरा जाल है।"
  ],
  "KYC_PANIC": [
   "केवाईसी या खाता बंद होने का डर",
   "बैंक एसएमएस के लिंक से खाता बंद नहीं करते। यह इस समय भारत में सबसे आम फिशिंग तरीका है।"
  ],
  "URGENCY": [
   "बनावटी जल्दबाज़ी",
   "कुछ घंटों में काम करने का दबाव इसलिए है ताकि आप जाँच न सकें। जो असली है वह कल भी रहेगा।"
  ],
  "NO_INTERVIEW": [
   "बिना इंटरव्यू के चयन",
   "बिना इंटरव्यू वाला ऑफर ऑफर नहीं होता। असली भर्ती में बात होती है।"
  ],
  "TOO_GOOD": [
   "काम के हिसाब से बहुत ज़्यादा पैसा",
   "कुछ घंटों के काम के लिए बाज़ार से कहीं ज़्यादा कमाई चारा है। पैसा ही कांटा है, काम नहीं।"
  ],
  "PERSONAL_PAYMENT": [
   "पैसा किसी निजी खाते में जा रहा है",
   "निजी यूपीआई या खाते में भेजा पैसा वापस लाना बहुत कठिन है, और इसीलिए वहीं मांगा जाता है।"
  ],
  "FREE_EMAIL_AS_COMPANY": [
   "कंपनी का मेल मुफ़्त इनबॉक्स से",
   "असली कंपनी अपने डोमेन से लिखती है, जीमेल या याहू से नहीं।"
  ],
  "HIDDEN_LINK": [
   "छोटा किया हुआ या छिपाया गया लिंक",
   "छोटे लिंक यह छिपाते हैं कि वे असल में कहाँ ले जाते हैं। असली संस्थाएँ अपने ही पते पर भेजती हैं।"
  ],
  "BARE_LINK": [
   "ऐसा लिंक जिसमें जगह का नाम नहीं",
   "भरोसेमंद संदेश बताते हैं कि वे आपको कहाँ भेज रहे हैं, नाम लेकर। \"इस लिंक\" के अलावा आपको कोई पता नहीं दिया गया।"
  ],
  "CHAT_ONLY": [
   "सिर्फ़ व्हाट्सएप या टेलीग्राम पर मौजूद",
   "न दफ़्तर, न वेबसाइट, न लैंडलाइन, सिर्फ़ एक चैट खिड़की। जवाबदेही कहीं नहीं।"
  ],
  "THREAT": [
   "कानूनी या पुलिस कार्रवाई की धमकी",
   "असली कानूनी नोटिस एसएमएस से नहीं आता। डर ही उनका असली हथियार है।"
  ],
  "SIGHT_UNSEEN": [
   "जगह देखे बिना किराया मांगा जा रहा है",
   "कोई भी असली मकान मालिक आपके देखने से पहले पैसे नहीं मांगता।"
  ],
  "COURIER_CUSTOMS": [
   "पार्सल रोका गया, छुड़ाने के लिए फीस",
   "कस्टम्स एसएमएस के लिंक से पैसे नहीं लेता। पार्सल है ही नहीं।"
  ],
  "ELECTRICITY_CUT": [
   "बिजली काटने की धमकी",
   "बिजली विभाग रात में एसएमएस भेजकर कनेक्शन नहीं काटता। घबराहट ही उनका उत्पाद है।"
  ],
  "LOTTERY_WIN": [
   "ऐसा इनाम जिसमें आपने हिस्सा ही नहीं लिया",
   "जिस लॉटरी में आपने भाग नहीं लिया, वह जीती नहीं जा सकती। हर बार अंत में इनाम छुड़ाने की फीस आती है।"
  ],
  "QR_SCAN": [
   "पैसे पाने के लिए क्यूआर कोड",
   "क्यूआर स्कैन करने से पैसा सिर्फ़ जाता है, कभी आता नहीं। जो कहे कि स्कैन करके पैसे मिलेंगे, वह झूठ बोल रहा है।"
  ],
  "REMOTE_ACCESS": [
   "आपकी स्क्रीन देखना या चलाना चाहते हैं",
   "कोई बैंक या सपोर्ट आपसे स्क्रीन शेयर ऐप नहीं लगवाता। स्क्रीन देखने वाला आपका पिन भी देखता है।"
  ],
  "APK_INSTALL": [
   "स्टोर के बाहर से ऐप लगवाना चाहते हैं",
   "फ़ाइल के रूप में भेजा गया ऐप किसी ने जाँचा नहीं है। भारत में बैंकिंग वायरस इसी रास्ते आते हैं।"
  ],
  "LOOKALIKE_DOMAIN": [
   "असली कंपनी जैसा दिखता वेब पता",
   "नाम तो पते में है, पर डोमेन उनका नहीं। असली संस्था अपने ही डोमेन पर भेजती है।"
  ],
  "VERIFY_DETAILS": [
   "कुछ बुरा रोकने के नाम पर आपकी जानकारी",
   "\"जानकारी पक्की करो वरना नुकसान होगा\" फिशिंग का सबसे पुराना रूप है। असली होगा तो ऐप खोलने पर भी दिखेगा।"
  ],
  "ID_DOCUMENTS": [
   "आधार या पैन मांगा जा रहा है",
   "आधार या पैन की फ़ोटो से आपके नाम पर खाता खुल सकता है और लोन लिया जा सकता है।"
  ],
  "CALLBACK_NUMBER": [
   "हेल्पलाइन के नाम पर निजी मोबाइल",
   "असली कंपनियाँ 1800 या लैंडलाइन देती हैं जिन्हें आप जाँच सकें। दस अंकों का मोबाइल किसी आदमी का है, बैंक का नहीं।"
  ],
  "COLLECT_REQUEST": [
   "पैसे पाने के लिए मंज़ूरी मांगी जा रही है",
   "पिन डालने या रिक्वेस्ट स्वीकार करने से पैसा हमेशा जाता है, आता कभी नहीं।"
  ],
  "STRANGER_OPENER": [
   "अनजान व्यक्ति पैसे की बात से शुरू कर रहा है",
   "गलत नंबर जो दोस्ती बनता है और फिर निवेश ऐप बनता है। शुरुआत हर बार ऐसे ही होती है।"
  ],
  "ADVANCE_FEE": [
   "अनजान से मिली विरासत या दौलत",
   "कोई अजनबी को दौलत देने के लिए नहीं चुनता। पैसा है ही नहीं, बीच में मांगी फीस ही असली मक़सद है।"
  ],
  "BANK_DETAILS": [
   "पैसे भेजने के नाम पर खाता नंबर",
   "जो पैसा आपका है वह उसी खाते में आता है जहाँ से गया था। नया खाता नंबर मांगना उल्टा है।"
  ],
  "SIM_BLOCK": [
   "सिम या कनेक्शन बंद करने की धमकी",
   "ऑपरेटर एसएमएस भेजकर सिम बंद नहीं करता। घबराहट ही उनका उत्पाद है।"
  ],
  "NEW_NUMBER": [
   "नया नंबर जिसे पैसे चाहिए",
   "नया नंबर बताकर पैसे मांगना अपनों की पहचान चुराने का सबसे आम तरीका है। पुराने नंबर पर फ़ोन कीजिए।"
  ],
  "STRANDED_PLEA": [
   "कहीं फँसे हैं और अभी पैसे चाहिए",
   "या तो किसी अपने का खाता हैक हुआ है, या अजनबी को पता है कि यह कहानी काम करती है।"
  ],
  "LOOKALIKE_URL": [
   "वेब पता जो दिखता कुछ और है",
   "दूसरी लिपि के अक्षर, प्यूनिकोड, ब्रांड नाम में अंक या सीधा आईपी पता। पढ़ने में सही लगता है, ले कहीं और जाता है।"
  ],
  "UNUSUAL_LOGIN": [
   "खाते की चेतावनी, साथ में लिंक",
   "बैंक नए डिवाइस की जानकारी देते हैं, पर उसका समाधान संदेश के लिंक में नहीं रखते। चेतावनी सच्ची है, लिंक नहीं।"
  ],
  "GOVT_GRANT": [
   "सरकारी रकम जिसके लिए आपने आवेदन ही नहीं किया",
   "कोई मंत्रालय एसएमएस से लोगों को पैसे के लिए नहीं चुनता। हर असली योजना में आवेदन आप खुद करते हैं।"
  ],
  "ROMANCE_BAIT": [
   "अजनबी की तारीफ़ से शुरुआत",
   "जो प्रोफ़ाइल आपने डाली ही नहीं, उसे किसी ने देखा। बात दूसरे ऐप पर जाती है और फिर पैसे पर।"
  ],
  "TXN_ALERT_BAIT": [
   "जो खर्च आपने किया ही नहीं, साथ में उपाय",
   "बैंक लेनदेन की जानकारी देता है, पर उसे रोकने का रास्ता उसी संदेश में नहीं रखता। चेतावनी सच्ची है, लिंक नहीं।"
  ],
  "REWARD_EXPIRY": [
   "पॉइंट या कैशबैक ख़त्म होने वाला है",
   "रिवॉर्ड पॉइंट भुनाने के लिए संदेश में लिंक की ज़रूरत नहीं होती। समय सीमा इसलिए है कि आप सोच न सकें।"
  ],
  "DIGITAL_ARREST": [
   "फ़ोन पर चल रही गिरफ़्तारी या जाँच",
   "भारतीय कानून में डिजिटल अरेस्ट जैसा कुछ है ही नहीं। कोई अफ़सर वीडियो कॉल पर जाँच नहीं करता और बेगुनाही साबित करने को पैसे नहीं मंगवाता।"
  ],
  "SECRECY": [
   "घरवालों को न बताने के लिए कहा जा रहा है",
   "हर सही संस्था चाहती है कि आप किसी से पूछ लें। मना करना ही पहचान है, क्योंकि जिससे आप पूछते वह यह रुकवा देता।"
  ],
  "SERVICE_SUSPENDED": [
   "आपकी कोई सेवा अचानक बंद",
   "लिंक के साथ आने वाला बंद होने का नोटिस फिशिंग का रूप है। असली बात उसी ऐप में दिखती है जो आपके पास पहले से है।"
  ],
  "DELIVERY_ADDRESS": [
   "डिलीवरी नहीं हुई और जानकारी मांगी जा रही है",
   "कूरियर वाला न मिले तो पर्ची छोड़ता है या फ़ोन करता है। समय सीमा देकर लिंक में पता नहीं भरवाता।"
  ],
  "CHALLAN": [
   "चालान जो लिंक से आता है",
   "चालान परिवहन पोर्टल पर रहता है और आप खुद देखते हैं। वह डाउनलोड के रूप में नहीं भेजा जाता।"
  ],
  "BILL_UPDATE": [
   "बिल अपडेट करने को कहा जा रहा है",
   "बिल भरा जाता है, अपडेट नहीं किया जाता। यह शब्द इसलिए है कि आप कुछ खोलें।"
  ],
  "LOAN_HARASSMENT": [
   "लोन ऐप जैसा दबाव",
   "लोन के नाम पर आपके फ़ोनबुक को धमकाना गैरकानूनी वसूली है, जायज़ मांग नहीं।"
  ],
  "INVESTMENT_TIP": [
   "पक्का मुनाफ़ा या टिप्स ग्रुप",
   "पक्के रिटर्न जैसी कोई चीज़ नहीं होती। जो ऐसा कहे वह या तो झूठा है या गैरकानूनी।"
  ],
  "TASK_COMMISSION": [
   "पहले पैसे भरकर टास्क या कमीशन का काम",
   "पहले कुछ छोटे भुगतान आते हैं ताकि आप बड़ी रकम लगाएँ। वही आख़िरी होती है।"
  ],
  "ARMY_OFFICER": [
   "दूर तैनात होने का दावा, मिल नहीं सकते",
   "वर्दी और मिल न पाने का बहाना, ताकि आप देखे बिना पैसे भेज दें।"
  ]
 },
 "clause": {
  "PAY_TO_GET_JOB": "नौकरी देने के बदले पैसे मांगे जा रहे हैं",
  "ASKS_FOR_SECRET": "आपका ओटीपी, पिन या पासवर्ड मांगा जा रहा है",
  "KYC_PANIC": "केवाईसी के नाम पर खाता बंद होने का डर दिखाया जा रहा है",
  "URGENCY": "बिना सोचे तुरंत करने का दबाव है",
  "LOTTERY_WIN": "ऐसे इनाम की बात है जिसमें आपने हिस्सा ही नहीं लिया",
  "QR_SCAN": "क्यूआर स्कैन करके पैसे मिलने की बात है, जो होता ही नहीं",
  "REMOTE_ACCESS": "आपकी स्क्रीन देखने या चलाने की बात है, जो कोई सही सपोर्ट नहीं मांगता",
  "DIGITAL_ARREST": "फ़ोन पर गिरफ़्तारी की बात है, जो भारतीय कानून में है ही नहीं",
  "SECRECY": "घरवालों को न बताने के लिए कहा जा रहा है"
 },
 "actions": {
  "no_pay": "कुछ भी मत भेजिए और कोई कोड मत बताइए, रकम कितनी भी छोटी क्यों न हो।",
  "no_otp": "ओटीपी, पिन या सीवीवी कभी मत बताइए। कोई बैंक, डिलीवरी वाला या नियोक्ता यह नहीं मांगता।",
  "own_number": "अगर लगे कि असली हो सकता है, तो अपने बिल, कार्ड या आधिकारिक वेबसाइट पर लिखा नंबर मिलाइए, संदेश वाला कभी नहीं।",
  "report": "cybercrime.gov.in पर शिकायत कीजिए या 1930 मिलाइए। अगर पैसे जा चुके हैं तो पहले एक घंटे में बताइए, तब तक रोके जा सकते हैं।",
  "block": "भेजने वाले को ब्लॉक कीजिए और जिसने आपको भेजा था उसे भी बता दीजिए।",
  "nothing": "कुछ नहीं मिला, पर यह सबूत नहीं कि सुरक्षित है। इसका मतलब सिर्फ़ यह है कि इसमें वे तरीके नहीं हैं जो पक्का जानता है।",
  "verify": "फिर भी खटके तो उसी नंबर पर पूछिए जो पहले से आपके पास है, संदेश वाले पर नहीं।"
 },
 "ui": {
  "tagline": "नियम · आपके फ़ोन पर ही चलता है",
  "placeholder": "संदेश यहाँ चिपकाइए…",
  "check": "जाँचिए",
  "verdict": "नतीजा",
  "checks_fired": "जाँचें चलीं",
  "risk": "जोखिम अंक",
  "model_reading": "मॉडल का अनुमान",
  "whats_wrong": "इसमें क्या गलत है",
  "what_to_do": "अब क्या कीजिए",
  "model_says": "मॉडल क्या कहता है",
  "forward_back": "जिसने भेजा है उसे यह वापस भेज सकते हैं",
  "share": "यह नतीजा आगे भेजिए",
  "copy_link": "लिंक कॉपी कीजिए",
  "copy_message": "संदेश कॉपी कीजिए",
  "nothing_fired": "कोई भी जाँच नहीं चली",
  "nothing_fired_why": "यह गारंटी नहीं है। इसका मतलब है कि इस संदेश में वे तरीके नहीं हैं जो पक्का जानता है। फिर भी कुछ गलत लगे तो उस पर भरोसा कीजिए।",
  "of": "में से",
  "lang": "English",
  "and": "और",
  "no_reason": "यह जानी-पहचानी धोखाधड़ी जैसा है",
  "forward_template": "मैंने जवाब देने से पहले इसे जाँचा। {reasons}। इस तरह की धोखाधड़ी ऐसे ही चलती है, इसलिए मैं न पैसे भेज रहा हूँ न कुछ बता रहा हूँ। आप भी मत भेजिए। (पक्का से जाँचा)",
  "fwd_note": "उन्हीं नियमों से लिखा गया है जो चले, इसलिए यह बात बढ़ा-चढ़ाकर नहीं कह सकता",
  "model_agrees": "मॉडल भी अलग से यही कहता है,",
  "model_out_of": "में से",
  "model_unsure": "मॉडल को पक्का नहीं है,",
  "model_reacted": "इसने सबसे ज़्यादा ध्यान दिया",
  "model_low": "मॉडल इसे",
  "model_low_tail": "पर रखता है, जहाँ ज़्यादातर संदेश होते हैं। इसमें वह नहीं दिखता जिस पर यह सीखा गया है।",
  "model_flag": "कोई नियम नहीं चला, फिर भी यह धोखाधड़ी जैसा लगता है।"
 }
};

/* The same normalisation as normalise() in api/rules.py. Change one, change
   both: tools/check_parity.py fails the build if they disagree. */
const PAKKA_LEET = { '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't' };
const pakkaAlpha = (c) => !!c && /^[A-Za-z]$/.test(c);
const pakkaAlnum = (c) => !!c && /^[A-Za-z0-9]$/.test(c);

window.pakkaNormalise = function (text) {
  const chars = [], idx = [], ends = [];
  let at = 0;
  for (const ch of text) {                       /* by code point, as Python does */
    for (const c of ch.normalize('NFD')) {
      if (c >= '̀' && c <= 'ͯ') continue;   /* a combining accent */
      /* an emoji is two code units here and one character in Python, so it
         becomes one placeholder and every quantifier counts the same */
      chars.push(c.length > 1 ? '�' : c);
      idx.push(at); ends.push(at + ch.length);
    }
    at += ch.length;                              /* but index by code unit, for slice */
  }
  for (let j = 0; j < chars.length; j++) {
    if (PAKKA_LEET[chars[j]] !== undefined) {
      const prev = j ? chars[j - 1] : '', next = chars[j + 1] || '';
      if (pakkaAlpha(prev) || pakkaAlpha(next)) chars[j] = PAKKA_LEET[chars[j]];
    }
  }
  const n = chars.length;
  const lone = (q) => pakkaAlpha(chars[q])
    && (q === 0 || !pakkaAlnum(chars[q - 1]))
    && (q + 1 >= n || !pakkaAlnum(chars[q + 1]));
  let out = '', oidx = [], oend = [], i = 0;
  while (i < n) {
    if (lone(i)) {
      const run = [i];
      let j = i;
      const sep = i + 1 < n ? chars[i + 1] : '';
      while (j + 2 < n && chars[j + 1] === sep && ' .-'.indexOf(sep) !== -1 && lone(j + 2)) {
        run.push(j + 2); j += 2;
      }
      if (run.length >= 3) {
        for (const k of run) { out += chars[k]; oidx.push(idx[k]); oend.push(ends[k]); }
        i = j + 1;
        continue;
      }
    }
    out += chars[i]; oidx.push(idx[i]); oend.push(ends[i]); i += 1;
  }
  return [out, oidx, oend];
};

/* grow a span out to word edges, so a highlight never cuts "expired" into
   "expire" and a stranded "d" */
const pakkaWord = (c) => !!c && /[A-Za-z0-9_ऀ-ॣ०-ॿ]/.test(c);
function pakkaWholeWords(text, a, b) {
  while (a > 0 && pakkaWord(text[a - 1]) && pakkaWord(text[a])) a -= 1;
  while (b < text.length && pakkaWord(text[b]) && pakkaWord(text[b - 1])) b += 1;
  return [a, b];
}

window.pakkaEvaluate = function (text) {
  const [norm, idx, ends] = window.pakkaNormalise(text);
  const findings = [];
  let deferred = null;
  for (const r of window.PAKKA_RULES) {
    /* the one check that is about the characters rather than the words, so it
       is answered by web/urls.js instead of by a pattern */
    if (r.id === 'LOOKALIKE_URL') {
      /* held back and pushed after the loop, because api/rules.py appends it
         last and equal weights would otherwise tie in a different order */
      const hits = (window.pakkaUrls ? window.pakkaUrls(text) : []);
      if (hits.length) {
        const why = [...new Set(hits.map(([, reason]) => reason))].join('; ');
        const sp = [...new Set(hits.map(([, , a, b]) => a + ':' + b))]
          .map((k) => k.split(':').map(Number)).sort((x, y) => x[0] - y[0]);
        deferred = { id: r.id, name: r.name, why, weight: r.weight,
                     spans: sp, quotes: sp.map(([a, b]) => text.slice(a, b)) };
      }
      continue;
    }
    const re = new RegExp(r.re, 'gi');
    const spans = [];
    let m;
    while ((m = re.exec(norm)) !== null) {
      if (m[0] === '') { re.lastIndex++; continue; }
      const a = m.index, b = m.index + m[0].length;
      if (idx.length) spans.push(pakkaWholeWords(text, idx[a], ends[Math.min(b, ends.length) - 1]));
    }
    if (spans.length) findings.push({
      id: r.id, name: r.name, why: r.why, weight: r.weight,
      spans, quotes: spans.map(([a, b]) => text.slice(a, b)),
    });
  }
  if (deferred) findings.push(deferred);
  const score = findings.reduce((s, f) => s + f.weight, 0);
  const [, band, label] = window.PAKKA_BANDS.find(([t]) => score >= t);
  findings.sort((a, b) => b.weight - a.weight);
  return { text, score, band, label, findings, rules_checked: window.PAKKA_RULES.length };
};
