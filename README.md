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

**Thirty-four rules, in plain Python. No model gets a vote.**

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
| 22 | Asks for your Aadhaar or PAN | 3 |
| 23 | A personal mobile posing as a helpline | 2 |
| 24 | Asks you to approve something to receive money | 4 |
| 25 | A stranger opening with money talk | 2 |
| 26 | An inheritance or fortune from a stranger | 3 |
| 27 | Wants your account number to send you money | 3 |
| 28 | Threatens to block your SIM or connection | 3 |
| 29 | A new number that needs money | 3 |
| 30 | Stranded somewhere and needs money now | 2 |
| 31 | Loan-app style pressure | 3 |
| 32 | Guaranteed returns or a tips group | 3 |
| 33 | Prepaid task or commission work | 3 |
| 34 | Claims to be posted far away and cannot meet | 3 |

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

## Answering where the message actually arrives

A scam arrives in a chat. Asking someone to copy it, open a browser, paste it
and read a page is asking them to do four things while they are being rushed,
which is the moment they are least able to. So the verdict comes back in the
thread the message was already in.

```
POST /telegram    an update from a Telegram bot, answered in the same chat
GET  /whatsapp    Meta's one-time webhook verification handshake
POST /whatsapp    the same idea on WhatsApp, if you can get through Meta's setup
```

Both channels share `api/chat.py`, which writes the reply. They differ only in
how a message arrives and how one is sent.

### Share straight from WhatsApp, with no Meta account at all

Meta's own API needs a business account and an app review. The share sheet does
not. Pakka ships a web app manifest that declares a
[share target](https://developer.mozilla.org/docs/Web/Manifest/share_target), so
once the site is installed to an Android home screen it appears in the share
sheet of every app on the phone, WhatsApp included.

Long-press the message, Share, Pakka. No copying, no pasting, no browser, and
the verdict is on screen before you have finished reading the scam.

The share arrives as an ordinary query string, so the page needs no new code
path to read it, and the query is wiped from the address bar immediately so a
stranger's message is not left sitting in browser history. A service worker
makes the app installable and keeps it working with the network off, which it
could already do, since the rules run on the device.

This is Android and Chrome. iOS does not implement share targets, and the
honest answer there is the Telegram bot below or the web page.

### Telegram, which takes about two minutes

No business account, no app review, nothing to verify. Telegram also matters on
its own here: a good share of the scams these rules describe are run out of
Telegram groups.

1. Message **@BotFather** on Telegram, send `/newbot`, pick a name. It gives
   you a token.
2. Put it in **Lambda → Configuration → Environment variables** as
   `TELEGRAM_TOKEN`, with `TELEGRAM_SECRET` set to any string you invent.
3. Register the webhook, using the same secret:

```
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<FUNCTION_URL>/telegram&secret_token=<SECRET>"
```

4. Message your bot.

Telegram has no request signature. Instead it sends the secret you registered
back in a header on every call, which is the same guarantee by a simpler route,
and the webhook refuses anything without it.

Locally, with no bot at all:

```
python3 api/test_telegram.py     # the webhook end to end, network stubbed out
```

## The WhatsApp front door

The scam arrives on WhatsApp. Asking someone to copy it, open a browser, paste
it and read a page is asking them to do four things while they are being
rushed, which is the moment they are least able to. So Pakka is also a number
you forward the message to, and the answer comes back in the same thread.

```
GET  /whatsapp    Meta's one-time verification handshake
POST /whatsapp    a forwarded message, answered in the same thread
```

The webhook checks Meta's `X-Hub-Signature-256` against the app secret before
it reads anything, refuses verification when no token is configured rather than
accepting whoever asks, and always answers 200 once the signature passes,
because Meta retries anything else and a retry would send the answer twice.

Meta requires a business account and an app review, and the dashboard is
frequently unreachable depending on where you are, which is why Telegram is the
path of least resistance above. The code is here and tested either way. Four
environment variables switch it on, and with none of them set nothing else
about the project changes:

| | |
|---|---|
| `WHATSAPP_VERIFY_TOKEN` | any string you choose, echoed back once |
| `WHATSAPP_TOKEN` | access token from the Meta app dashboard |
| `WHATSAPP_PHONE_ID` | phone number ID from the same dashboard |
| `WHATSAPP_APP_SECRET` | app secret, used to check the signature |
| `PAKKA_PUBLIC_URL` | where scans are readable, so the reply can link to one |

Setting it up, all on free tiers:

1. **developers.facebook.com/apps** → Create app → Business → add the
   **WhatsApp** product. You get a test number and a temporary token.
2. **WhatsApp → API Setup** gives you the phone number ID and the token.
   **App settings → Basic** gives you the app secret.
3. Put all four in **Lambda → Configuration → Environment variables**.
4. **WhatsApp → Configuration → Edit** the webhook. Callback URL is your
   Function URL with `/whatsapp` on the end; verify token is the string you
   chose. Subscribe to the **messages** field.
5. Send anything to the test number from the phone you registered.

Run it locally with no Meta account at all:

```
WHATSAPP_VERIFY_TOKEN=test python3 api/local_server.py
curl "localhost:8787/whatsapp?hub.mode=subscribe&hub.verify_token=test&hub.challenge=HELLO"
python3 api/test_whatsapp.py     # the webhook, end to end, network stubbed out
```

## The model that sits beside the rules

Rules have perfect precision on what they describe and no opinion at all about
anything else. That is their strength and it is also the ceiling: a scam phrased
in words nobody wrote down scores zero.

So there is a linear model too, trained on the
[UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
(5,574 labelled messages) plus this project's own corpus. It runs on the device
like the rules do, as a dot product over hashed character n-grams of the same
normalised text, which means `0TP` and `O T P` reach it as `otp` too.

```
python3 tools/train_model.py     # train, cross validate, calibrate, export
```

**Why linear and not something bigger.** A linear model's output *is* the sum
of its per-feature contributions. Lay each weight back on the characters its
n-gram came from and the model can point at the phrases it reacted to, the same
way a rule quotes the words that matched. Nothing has to be taken on trust. It
is also 727 numbers, 11 KB, which is small enough to ship to a phone and run
with the network off.

**Does it earn its place?** The Indian corpus cannot answer that, because the
rules were written against it and score 100% on it. The UCI set can, honestly,
because no rule here has ever seen a 2012 British SMS. On 1,115 held-out UCI
messages:

| | precision | recall |
|---|---|---|
| rules alone | 0.75 | 0.04 |
| model alone | 0.89 | 0.93 |
| both together | 0.89 | 0.93 |

The rules are nearly blind out of domain. The model catches **129 spam messages
that no rule fires on**. That is the entire argument for it.

**And on the domain that matters**, five-fold cross validation on the Indian
corpus with UCI always in the training half: AUC 0.78, precision 0.74, recall
0.79. Worse than the rules score there, which is the honest way round: the rules
were built for exactly these messages.

**Calibration.** The probability is Platt-scaled on out-of-fold predictions
only, so 0.8 means roughly eight in ten rather than just "high":

| predicted | actually fraud |
|---|---|
| 0.0 – 0.2 | 0.25 |
| 0.2 – 0.4 | 0.29 |
| 0.4 – 0.6 | 0.54 |
| 0.6 – 0.8 | 0.67 |
| 0.8 – 1.0 | 0.90 |

**The boundary.** Rules decide. The model is shown underneath them, never
instead of them. It may raise concern and it may never clear it: a headline of
"Nothing suspicious found" over a 90-out-of-100 reading is the one failure that
actually costs somebody money. When no rule fires and the model is confident,
the page says so plainly, and that bucket is also where the next rule comes
from.

**What it is trained on, and the limits of that.** UCI is British SMS spam from
2012. It teaches the model "free", "win", "claim" and "txt" and teaches it
nothing about KYC, UPI, APK sideloading or AnyDesk. The Indian corpus supplies
those and is upweighted twelvefold in training to stop 2% of the rows being
drowned out, but 129 messages is 129 messages. Real forwards would help more
than any change to the model.

## How well does it actually work

`tools/eval_set.py` holds 129 labelled messages: 76 fraud across 20 families and
53 legitimate ones chosen to be hard — real bank OTP alerts, a real RBI KYC
reminder, real delivery notifications with OTPs in them, recruiters, marketing
with urgency words in it, and friends talking about money and account numbers.

```
python3 tools/eval.py          # the numbers below
python3 tools/eval.py -v       # plus every miss and every false positive
```

| | |
|---|---|
| fraud caught | 76/76 |
| caught clearly, score 2 or more | 73/76 |
| false positives on legitimate messages | 0/53 |
| legitimate messages raising a single low flag | 4/53 |

The fraud set includes messages written to get past filters — `K Y C` spaced
out, `0TP` with a zero, `shäre` with an accent, `C-l-i-c-k` — and Hinglish,
which is how a large share of these actually arrive. Both are handled by
normalising the text before matching and mapping the result back, so the
highlighted words still line up with what was pasted.

These numbers are honest about one thing: I wrote the test set. It is built from
scam patterns that are well documented in India, and the legitimate half is
deliberately adversarial, but a set written by the same person who wrote the
rules will always flatter them. The useful claim is not the percentage, it is
that the set exists, it is in the repository, and you can add a message to it
and watch it fail.

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

It does not detect scams it has never seen — thirty-four patterns are thirty-four
patterns, and a clean result says only that none of them fired. The page says so
rather than implying safety. It reads English and Hinglish written in Latin
script; Devanagari input is not handled yet. And it is not legal or financial
advice: when it is unclear, the right move is still not to pay.
