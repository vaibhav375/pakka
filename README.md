# Pakka

**Check before you pay.**

Paste a message you were sent — a PG listing, an internship offer, a "your KYC
has expired" SMS — and Pakka tells you which specific parts of it are a problem
and why, then gives you a link you can forward straight back to whoever sent it.

Built at **First Commit (AWS × WeMakeDevs)**, 17–20 September 2026.

---

## The problem

My mother forwards me messages to check. So do my juniors, about PG listings and
internship offers. Every time, the answer is the same shape: *this line here is
the problem, and here is why.* The person asking usually already felt something
was off — what they lacked was the confidence to say no, and the words to explain
it to whoever sent it.

Existing "is this a scam" tools answer with a percentage. A percentage is not
something you can forward to your mother. It also cannot be argued with, which
matters, because the person you are trying to protect is often mid-argument with
a stranger who sounds official.

So Pakka answers in sentences, points at the exact words, and gives you a link.

## How it decides

**Thirty-three rules, in plain Python. No model gets a vote.**

A scam verdict has to be identical every time and has to survive being explained
to the person who nearly paid. A language model can do neither reliably, so the
decision lives in [`api/rules.py`](api/rules.py), where each rule can find itself
in the message and say in one sentence why what it found is a problem.

| | Rule | Weight |
|---|---|---|
| 1 | Asks for money before a job | 3 |
| 2 | Asks for an OTP, PIN or password | 4 |
| 3 | Asks you to pay to receive money | 4 |
| 4 | KYC or account-block scare | 3 |
| 5 | Manufactured urgency | 1 |
| 6 | Selected without any interview | 2 |
| 7 | Pay that does not match the work | 2 |
| 8 | Money goes to a personal account | 3 |
| 9 | Company mail sent from a free inbox | 2 |
| 10 | Shortened or disguised link | 2 |
| 11 | Exists only on WhatsApp or Telegram | 1 |
| 12 | Threatens legal or police action | 2 |
| 13 | Asks for rent before you have seen the place | 3 |
| 14 | Parcel held, pay a fee to release it | 3 |
| 15 | Electricity disconnection threat | 3 |
| 16 | A prize you never entered for | 4 |
| 17 | A QR code to receive money | 3 |
| 18 | Wants to see or control your screen | 4 |
| 19 | Wants you to install an app from outside the store | 4 |
| 20 | A web address dressed up as a real company | 3 |
| 21 | Wants your details to avoid something bad | 2 |
| 22 | Asks for your Aadhaar or PAN | 2 |
| 23 | A personal mobile posing as a helpline | 2 |
| 24 | Asks you to approve something to receive money | 4 |
| 25 | A stranger opening with money talk | 2 |
| 26 | An inheritance or fortune from a stranger | 3 |
| 27 | Wants your account number to send you money | 3 |
| 28 | Threatens to block your SIM or connection | 3 |
| 29 | Stranded somewhere and needs money now | 2 |
| 30 | Loan-app style pressure | 3 |
| 31 | Guaranteed returns or a tips group | 3 |
| 32 | Prepaid task or commission work | 3 |
| 33 | Claims to be posted far away and cannot meet | 3 |

Weights add up to a score, the score picks a band. Ordinary messages have to come
back clean — a checker that flags everything gets ignored, so a real placement-cell
message is a test case, not an afterthought.

```
python3 api/test_rules.py
```

## Architecture

```
    Browser (Amplify Hosting)
        |  POST /scan   { text }
        v
    Lambda Function URL  ──►  pakka-api  (Python 3.12)
                                  |
                      rules.py ───┤  verdict decided here, deterministically
                                  |
                                  v
                            DynamoDB  pakka-scans
                            id · text · verdict · expires_at (30d TTL)
                                  |
                                  v
                            CloudWatch Logs
```

Two routes, one function:

| | |
|---|---|
| `POST /scan` | message in, verdict out, saved so it can be linked to |
| `GET /v/{id}` | that saved verdict, for the person you forwarded it to |

### Why these services

**Lambda, not EC2.** This is a tool people open twice a month, when something
looks wrong. Traffic is spiky and mostly zero. A server billed by the hour for a
workload measured in seconds is the wrong shape, and for a free tool the idle
cost is the whole problem.

**A Lambda Function URL, not API Gateway.** One public HTTPS endpoint with CORS
was all this needed. API Gateway would have added a second thing to configure and
a second thing to pay for once the twelve-month window closes; Function URLs carry
no additional charge at all.

**DynamoDB at 1 read and 1 write unit.** Provisioned rather than on-demand, on
purpose: on-demand is the better shape for spiky traffic but it bills from the
first request, while 1/1 provisioned sits inside the always-free 25 of each.
That is a free-tier decision, and at real traffic it should flip to on-demand.

**A 30-day TTL on every row.** A scan is evidence for the person who nearly paid,
not an archive. Rows delete themselves, storage stays near zero, and there is no
growing pile of other people's messages to look after.

**No build step.** The front end is HTML, CSS and JavaScript, so Amplify publishes
`web/` as it stands. Build minutes stay at zero and there is no npm install that
can fail at eleven at night.

### What it costs

Everything above sits inside the AWS Free Tier: 1M Lambda requests a month,
25 DynamoDB capacity units, 15 GB served by Amplify, 5 GB of CloudWatch logs.

At 1,000 scans a month — roughly one small college's worth — it stays inside the
free tier on every axis. At 100,000 scans a month the Lambda invocations are still
free, DynamoDB would move to on-demand at roughly $0.13 for the writes, and the
bill is dominated by data transfer rather than compute.

## Running it

**Locally, with no AWS account** — the Build It path. Storage falls back to a JSON
file when no table name is set, so nothing needs installing:

```
python3 api/local_server.py           # API on http://127.0.0.1:8787
cd web && python3 -m http.server 5500 # open http://127.0.0.1:5500
```

**On AWS** — the whole stack is one SAM template ([`template.yaml`](template.yaml)):
a function, a table, a function URL, and the IAM policy between them.

## Tools used

Written with AI assistance (Claude) for code and copy, reviewed and tested by me.
Smooth scrolling uses [Lenis](https://lenis.dev) (MIT). Type is Space Grotesk and
Space Mono via Google Fonts (OFL). Everything else is stdlib Python and plain
browser JavaScript.

## What it does not do

It does not detect scams it has never seen — thirty-three patterns are thirty-three
patterns, and a clean result says only that none of them fired. The page says so
rather than implying safety. It reads English and Hinglish written in Latin
script; Devanagari input is not handled yet. And it is not legal or financial
advice: when it is unclear, the right move is still not to pay.
