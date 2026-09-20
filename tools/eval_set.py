"""A labelled set for measuring the rules, kept separate from the unit tests.

The unit tests prove a rule works. This measures how much of the real world the
whole set actually covers, including the parts it gets wrong.

Every entry is (family, text). FRAUD should be caught. LEGIT must not be. The
LEGIT half is deliberately hard: real bank alerts, real KYC reminders, real
prize wins, real recruiters, real marketing, and friends talking about money.
"""

FRAUD = [
 # --- bank and KYC phishing
 ("kyc", "Dear Customer, your SBI YONO account will be blocked today. Update your KYC at http://sbi-yono-kyc.xyz/update"),
 ("kyc", "Your PAN card is not linked with your bank account. Account will be suspended in 24 hours. Click http://bit.ly/pan-link-now"),
 ("kyc", "HDFC ALERT: Your netbanking will expire today. Re-activate your account details here immediately."),
 ("kyc", "Dear user your Paytm KYC is pending, complete verification now or wallet will be frozen. http://paytm-kyc.online"),
 ("kyc", "Your account has been temporarily suspended due to incomplete KYC. Verify your details now to restore access."),
 # --- prize and lottery
 ("prize", "Congratulations!! Your mobile number has won Rs 25,00,000 in the KBC lucky draw. Contact Mr Rana on WhatsApp."),
 ("prize", "You have won an iPhone 15 Pro in our Diwali lucky draw. Pay Rs 499 delivery charge to claim it."),
 ("prize", "Claim your free MacBook Air now before you lose the offer. Scan the QR code to claim."),
 ("prize", "Dear customer congratulations on winning a gift hamper from Flipkart. Share your address and pay handling charge."),
 ("prize", "Your number is selected in Amazon Great Indian Lucky Draw. Claim your prize by sharing bank account number."),
 # --- job scams
 ("job", "Congratulations! You are shortlisted for Amazon data entry without interview. Pay Rs 1,999 registration fee."),
 ("job", "Work from home opportunity. Earn Rs 4000 daily. No experience needed. Contact us only on WhatsApp 9812345670."),
 ("job", "Dear candidate, your resume is selected by TCS. Kindly pay Rs 2500 refundable security deposit for onboarding."),
 ("job", "hr.hiring2024@gmail.com - Offer letter attached. Pay training fee of Rs 3000 to confirm your joining."),
 ("job", "Part time job for students. Just rate hotels and earn commission. Join our telegram group to start."),
 # --- courier and customs
 ("courier", "Your parcel is held at Mumbai customs. Pay Rs 4,850 clearance duty within 6 hours or it will be returned."),
 ("courier", "India Post: your package could not be delivered due to incomplete address. Update here http://indiapost-redelivery.top"),
 ("courier", "DHL: Your shipment is on hold. A customs fee is pending. Click the link to release your consignment."),
 ("courier", "Your Amazon order could not be delivered. Update your address at http://amaz0n-delivery.info/track"),
 # --- electricity
 ("electricity", "Dear consumer your electricity will be disconnected tonight 9:30pm as your previous bill is not updated. Call 9123456780"),
 ("electricity", "BESCOM notice: power connection will be cut today due to pending bill. Contact our officer immediately on 8123456789."),
 ("electricity", "Your electricity bill is not updated in our system. To avoid disconnection call this number to confirm."),
 # --- UPI, QR and collect requests
 ("upi", "Rs 9,999 cashback has been credited to your wallet. Click here to withdraw the amount."),
 ("upi", "Your friend has sent you Rs 2,000. Accept the collect request on your UPI app to receive the money."),
 ("upi", "Scan this QR code to receive your refund of Rs 4,500 from Flipkart."),
 ("upi", "To get your refund please enter your UPI PIN in the request we have sent you."),
 ("upi", "I have sent the payment, please scan the QR I am sending to receive it in your account."),
 # --- remote access and malicious apps
 ("remote", "Sir please install AnyDesk from playstore and share the 9 digit code, I will resolve your refund."),
 ("remote", "Download our RBI verification app from this link to keep your bank account active."),
 ("remote", "Install this APK to complete your loan application. Enable installation from unknown sources."),
 ("remote", "Please allow screen sharing so I can guide you through the transaction reversal."),
 # --- loan harassment
 ("loan", "Your loan EMI is overdue. We will inform all your contacts and family about your default today."),
 ("loan", "Recovery agents have been assigned. Legal action and police complaint will be filed against you."),
 ("loan", "Pay Rs 8,400 immediately or we will share your photos with everyone in your phonebook."),
 # --- investment and pig butchering
 ("investment", "Hi, I got your number from a mutual friend. I am Linda, I trade crypto and make 30% profit monthly."),
 ("investment", "Guaranteed returns, double your money in 45 days. Join our stock tips group on WhatsApp."),
 ("investment", "Hello, sorry wrong number. But you seem nice. I do forex trading, I can teach you to earn daily."),
 ("investment", "Exclusive IPO allotment for you. Guaranteed profit. Transfer the amount to our personal account today."),
 ("investment", "Our trading signals give guaranteed income. Only limited seats left in the group."),
 # --- task and commission
 ("task", "Complete 20 simple tasks and earn commission daily. Prepaid task of Rs 5000 gives Rs 6500 return."),
 ("task", "Like and subscribe YouTube videos, earn Rs 50 per video. Contact on telegram to begin."),
 ("task", "Hotel rating job, earn Rs 3000 daily from home. Send your details on WhatsApp."),
 # --- impersonation
 ("impersonation", "I am Major Vikram Singh posted in Jammu. I cannot visit the flat, I am sending advance token amount now."),
 ("impersonation", "This is CBI. An FIR has been registered against your Aadhaar for money laundering. Call immediately."),
 ("impersonation", "Your number is involved in illegal activity. Digital arrest warrant issued. Join the video call now."),
 ("impersonation", "I am calling from TRAI. Your mobile number will be disconnected in 2 hours due to illegal use."),
 # --- new number and stranded
 ("newnumber", "Hi mom this is my new number, my old phone broke. Please send Rs 15,000 urgently, I will explain later."),
 ("newnumber", "Papa, this is my new number. I need money for fees today, please transfer Rs 20,000."),
 ("stranded", "I am stuck in Dubai and lost my wallet and passport. Please send money, I will return it."),
 ("stranded", "Bro I lost my phone and wallet at the station, can you transfer 5000 money urgently"),
 # --- identity document harvesting
 ("identity", "For loan approval send your Aadhaar card photo, PAN card and a selfie holding your Aadhaar."),
 ("identity", "Share a scan of your PAN card and voter id for the verification process."),
 ("identity", "Kindly whatsapp your aadhaar number and bank passbook photo to process the subsidy."),
 # --- advance fee
 ("advancefee", "I am Mrs Grace Williams, a widow suffering from cancer. I wish to donate my 5 million dollar fund to a trustworthy person."),
 ("advancefee", "You have been named next of kin to an unclaimed inheritance of USD 8.5 million. Reply for details."),
 ("advancefee", "Barrister John here. Your late relative left a fund. A small processing fee is needed to transfer it."),
 # --- fake customer care
 ("support", "For complaint regarding your order call our customer care 9876543210. We are the official helpline."),
 ("support", "Your credit card has an unauthorised transaction of Rs 89,000. If not done by you call this number to cancel it."),
 ("support", "Swiggy refund helpline 9988776655. Call now and share your UPI PIN for instant refund."),
 # --- SIM block
 ("sim", "Your SIM card will be blocked in 12 hours. Submit your details now to keep it active."),
 ("sim", "Your mobile connection will be deactivated due to incomplete verification. Update immediately."),
 # --- rental
 ("rental", "2BHK near Koramangala 12000/month fully furnished. I am currently abroad, transfer token amount on GPay 9988776655."),
 ("rental", "Flat available immediately. Pay booking amount before visit as many people are interested."),
 ("rental", "PG for girls, 6500 per month. Send advance on this UPI id to block the bed, I am out of station."),
 # --- adversarial: obfuscation and spacing
 ("obfuscated", "Your K Y C has expired. Share the O T P received to complete verification."),
 ("obfuscated", "Send your 0TP immediately to verify your acc0unt"),
 ("obfuscated", "C-l-i-c-k here to verify your account details now http://sbi-verify.xyz"),
 ("obfuscated", "Ur a/c will b blocked 2day. Updt ur KYC nw at bit.ly/kycfix"),
 ("obfuscated", "Congratulations 🎉 you have W-O-N a lucky draw prize of Rs 10,00,000"),
 ("obfuscated", "shäre your otp to complete the transaction"),
 # --- adversarial: Hinglish and transliteration
 ("hinglish", "Aapka KYC update nahi hua hai, account block ho jayega. Turant is link par click kare http://kyc-update.xyz"),
 ("hinglish", "Sir aapka lottery lag gaya hai, 10 lakh rupaye jeeta hai. Processing fee bhejiye."),
 ("hinglish", "Bhaiya mera naya number hai, purana phone kho gaya. Please 10000 rupaye bhej do urgent hai."),
 ("hinglish", "Aapke naam par parcel customs me ruka hai, clearance fee pay kijiye."),
 ("hinglish", "Ghar baithe kamaye 3000 rupaye daily. Whatsapp par contact kare."),
 ("hinglish", "Apna OTP share kijiye, hum bank se bol rahe hai."),
]

LEGIT = [
 # --- real bank messages, the hardest negatives
 ("bank", "Your OTP is 728341. Do not share it with anyone. -HDFC Bank"),
 ("bank", "OTP for your transaction of Rs 2,499 at Amazon is 449201. Valid for 10 minutes. Never share this with anyone."),
 ("bank", "HDFC Bank: Rs 2,500 debited from a/c XX1234 on 20-09-26. Not you? Call 18002026161."),
 ("bank", "Dear Customer, Rs 45,000 credited to your account XX8821 by NEFT from ACME PVT LTD."),
 ("bank", "Your SBI account statement for September is ready. View it on the YONO app."),
 ("bank", "As per RBI guidelines, please complete your periodic KYC update at your nearest branch before 31 December."),
 ("bank", "Your credit card bill of Rs 12,430 is due on 28 Sept. Pay via the app to avoid late fees."),
 ("bank", "Your fixed deposit matures on 5 October. Visit the branch or renew online."),
 # --- real deliveries
 ("delivery", "Your Amazon order has been delivered. Rate your experience in the app."),
 ("delivery", "Your Swiggy order from Meghana Foods is being prepared."),
 ("delivery", "Your parcel has been shipped and will arrive by 24 September. Track it in the app."),
 ("delivery", "Delivery agent arriving in 10 minutes. Share the OTP 4471 with him to complete delivery."),
 ("delivery", "Scan the QR on the package to confirm delivery, or pay the agent by scanning his QR code."),
 ("delivery", "Your Blue Dart shipment AWB 4471829 is out for delivery today."),
 # --- real utilities and government
 ("utility", "Reminder: electricity bill of Rs 1,240 due on 25th. Pay through the BESCOM app."),
 ("utility", "Your electricity bill payment of Rs 1,240 was successful. Receipt available in the app."),
 ("utility", "Your PF passbook has been updated for the quarter. Check on the EPFO portal."),
 ("utility", "Your income tax return for AY 2026-27 has been processed. Refund will be credited to the bank account on record."),
 ("utility", "Your gas cylinder booking is confirmed. Delivery within 2 days."),
 ("utility", "Your Aadhaar has been successfully updated. Download the e-Aadhaar from the UIDAI portal."),
 # --- real jobs and college
 ("work", "Hi Vaibhav, this is Priya from the placement cell. Your Infosys interview is Monday 10am, Seminar Hall 2."),
 ("work", "Hi, I am a recruiter at Zomato. Saw your GitHub, would you be open to a chat about a backend role this week?"),
 ("work", "Interview scheduled Friday 11am. Please carry your PAN card and two photographs for the joining formalities."),
 ("work", "Team, the standup moved to 10am tomorrow. Please update your calendar."),
 ("work", "Your internship certificate is ready. Collect it from the HOD office."),
 ("work", "Please install the company VPN from the IT portal before Monday, we are enabling it for all laptops."),
 ("work", "Registration for the hackathon closes on Friday. Submit your team details on Devfolio."),
 ("work", "Congratulations! Your team won first place in the college hackathon. Certificates will be mailed."),
 # --- real marketing, urgency words but not fraud
 ("marketing", "Flat 40% off on all shoes. Offer valid today only. Shop now at myntra.com"),
 ("marketing", "Last chance! Your Netflix plan renews tomorrow. Manage your subscription in Account settings."),
 ("marketing", "Free delivery on all orders above Rs 499 this week. Order on the app."),
 ("marketing", "Limited seats left for the weekend yoga batch. Reply to book."),
 ("marketing", "Your Zomato Gold expires in 3 days. Renew in the app to keep your benefits."),
 # --- friends and family, including money and numbers
 ("personal", "Call me on 9876543210 when you reach the gate, I will come down."),
 ("personal", "Can you send me a photo of your notes from today's class?"),
 ("personal", "Can you share your bank account number? I need to transfer your share of the trip money."),
 ("personal", "Hi, this is my new number, please save it. See you Saturday. - Rahul"),
 ("personal", "I have sent you the money on GPay, please check and confirm."),
 ("personal", "Hey I am stuck in traffic, will be 20 minutes late. Order for me."),
 ("personal", "Mummy, I reached the hostel. Will call in the evening."),
 ("personal", "Let's meet in 2 hours at the usual place."),
 ("personal", "Congratulations on your new job! Party kab hai"),
 ("personal", "Bhai mera naya number hai, save kar lena"),
 ("personal", "Rent for September received, thanks. I will send the receipt tomorrow."),
 ("personal", "Please send me your address, I want to courier the book to you."),
 ("personal", "Dad, please transfer 5000 for the hostel mess bill when you get time."),
 ("personal", "I lost my wallet yesterday, had to block all the cards. What a day."),
 # --- real services
 ("service", "Your appointment at Apollo is confirmed for 22 Sept, 4pm. Reply CANCEL to cancel."),
 ("service", "Your Uber is arriving. KA05 MJ 1234, white Swift."),
 ("service", "Your flight AI-502 is delayed by 45 minutes. New departure 18:15."),
 ("service", "The library book is due in 3 days. Please return or renew it online."),
 ("service", "Your insurance policy renews on 30 September. Premium Rs 8,400. Renew on our website."),
 ("service", "Fee payment reminder: semester fee due 30 Sept. Pay via the college ERP portal."),
]
