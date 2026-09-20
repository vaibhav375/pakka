/* Display metadata for the twenty rules. The verdict always comes from the
   server — this is only what each node is called and the phrase it hunts, so
   the constellation and the gallery can label themselves. */
window.PAKKA_RULES = [
  ["PAY_TO_GET_JOB",       "Asks for money before a job",            "registration fee"],
  ["ASKS_FOR_SECRET",      "Asks for an OTP, PIN or password",        "share the OTP"],
  ["PAY_TO_RECEIVE",       "Asks you to pay to receive money",        "pay to release your refund"],
  ["KYC_PANIC",            "KYC or account-block scare",              "KYC has expired"],
  ["URGENCY",              "Manufactured urgency",                    "within 2 hours"],
  ["NO_INTERVIEW",         "Selected without any interview",          "selected without interview"],
  ["TOO_GOOD",             "Pay that does not match the work",        "₹25,000 for 2 hours daily"],
  ["PERSONAL_PAYMENT",     "Money goes to a personal account",        "google pay to 98450…"],
  ["FREE_EMAIL_AS_COMPANY","Company mail sent from a free inbox",     "hr.hiring@gmail.com"],
  ["HIDDEN_LINK",          "Shortened or disguised link",             "bit.ly/kyc-verify"],
  ["CHAT_ONLY",            "Exists only on WhatsApp or Telegram",     "contact only on WhatsApp"],
  ["THREAT",               "Threatens legal or police action",        "FIR will be filed"],
  ["SIGHT_UNSEEN",         "Wants rent before you have seen it",      "token amount"],
  ["COURIER_CUSTOMS",      "Parcel held, pay a fee to release it",    "held at customs"],
  ["ELECTRICITY_CUT",      "Electricity disconnection threat",        "will be disconnected tonight"],
  ["LOTTERY_WIN",          "A prize you never entered for",           "you have won"],
  ["LOAN_HARASSMENT",      "Loan-app style pressure",                 "we will inform your contacts"],
  ["INVESTMENT_TIP",       "Guaranteed returns or a tips group",      "guaranteed returns"],
  ["TASK_COMMISSION",      "Prepaid task or commission work",         "prepaid task"],
  ["ARMY_OFFICER",         "Posted far away, so cannot meet",         "posted in Leh"],
].map(([id, name, hunts]) => ({ id, name, hunts }));
