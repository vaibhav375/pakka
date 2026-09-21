# First Commit submission answers

Copy these into the form. Tracks: Build It and Ship It.

Project: Pakka, check before you pay
GitHub: https://github.com/vaibhav375/pakka
Live: https://main.d1nvlrv96k8kj1.amplifyapp.com/
Telegram: @pakka_check_bot, message it anything
WhatsApp: live on Twilio's sandbox, join code in the demo

---

## 1a. What does your project do?

Pakka checks a message before you act on it. You paste in a text, a WhatsApp
forward, an email, anything, and it answers in plain sentences: whether this
looks like a scam, which specific parts of it are the problem, and why. It
quotes the exact words that set off each flag instead of handing you a score
and expecting you to trust it.

Then it does the part most tools skip. It tells you what to do next. Do not
pay, do not share the OTP, report it at cybercrime.gov.in or call 1930, and do
that inside the first hour while the money can still be frozen. It also writes
a short reply you can send straight back to whoever forwarded the message to
you, so you are not stuck looking for the words.

You do not have to open the page to get that answer. The scam arrives in a
chat, and copying it out, opening a browser and pasting it is four things to do
while somebody is rushing you, which is the moment you are least able to do
them. So the same verdict comes back in the thread the message was already in:
message @pakka_check_bot on Telegram, or forward it to the WhatsApp number. On
Android the site also registers as a share target, so a message can be
long-pressed and shared to Pakka from inside WhatsApp itself with no bot at all.

There are three things doing the checking, and the order matters.

Forty-seven rules written in ordinary Python decide the verdict. No model gets
a vote there, which means the same message always produces the same answer and
every answer can be explained line by line.

A linear model trained on 5,700 labelled messages sits underneath them. Rules
have perfect precision on what they describe and no opinion at all about
anything else, so a scam phrased in words nobody wrote down scores zero. The
model catches those. It is linear on purpose: its output is the sum of its
per-feature contributions, so it can point at the phrases it reacted to rather
than asking to be believed. It may raise concern and it may never clear a
message the rules flagged.

And some checks are not about words at all. A pattern can look for the word
"sbi". It cannot tell you that the "a" in "amazon.in" is Cyrillic, or that
xn--80ak6aa92e.com is displayed in the address bar as something else entirely.
Those are properties of the characters, so a separate module answers them and
reports the reason in words.

All of it runs on the device. The rules are generated from Python into
JavaScript, and the model is 789 numbers, twelve kilobytes. Nothing you paste
ever leaves your phone unless you choose to create a shareable link.

## 1b. What problem does it solve, and who is it for?

Most people who get a scam message already sense something is off. That is not
where they get stuck. They get stuck on two things: they cannot point at what
exactly is wrong, and there is nobody to ask in the thirty seconds before they
tap the link. So they either pay, or they forward it to whoever in the family
is considered good with phones and wait.

I am that person in my family. My mother forwards me messages to check. So do
my juniors, PG listings, internship offers, "your KYC has expired" texts. Every
single time the answer has the same shape: this line here is the problem, and
this is why. Pakka is that answer, available without me.

It is for anyone in India who gets sent something that smells wrong and has
nobody to ask. Parents and grandparents especially, but also students getting
fake internship offers, and people being told a courier is stuck at customs or
an electricity connection is being cut tonight.

There is a second half of the problem that is harder than catching scams, and
it is why tools like this fail. If it flags everything, people stop listening,
and then it is worse than useless. So an ordinary message has to come back
clean. A real message from a college placement cell, a genuine OTP from a bank,
a delivery notification with an OTP in it, and a friend asking for your account
number to send you trip money are all test cases in the repository, and all of
them have to score zero.

## 2. How did you use AWS?

Everything runs in ap-south-1, Mumbai, because the people using this are in
India and their messages should not leave the country to be checked.

### Ship it: AWS services

**AWS Lambda** runs the API on Python 3.12. One function, a handful of routes:
scan a message, fetch a saved verdict, and the webhooks for the chat front
doors. Traffic for a tool people open only when something looks wrong is spiky
and mostly zero, so paying for a server by the hour is the wrong shape for it.

**Lambda Function URLs** give that function its public HTTPS endpoint. I chose
this over API Gateway deliberately. All I needed was one public URL with CORS,
and Function URLs carry no additional charge, whereas the API Gateway free tier
runs out after twelve months.

**Amazon DynamoDB** stores scans, provisioned at 1 read unit and 1 write unit
so it sits inside the always free 25 of each. Every item has a 30 day TTL,
because a saved scan is evidence for the person who nearly paid, not an archive
I have any business keeping.

**AWS Amplify Hosting** serves the front end straight from GitHub. The site is
static with no build step, so build minutes stay at zero and every push
redeploys it.

**Amazon CloudWatch Logs** carried every traceback, and it is the only reason I
got the thing working at all.

**AWS IAM** for an execution role scoped to that one table.

On cost: at a thousand scans a month the whole stack stays inside the free
tier. At a hundred thousand, the Lambda invocations are still free and the only
line that starts costing anything is the DynamoDB writes.

### Build it: AWS open source stack

**AWS SAM**, the Serverless Application Model. The entire stack is described in
one `template.yaml`: the function, the table, the TTL attribute, the Function
URL and its CORS config, and the parameters for the chat integrations. Anyone
can deploy their own copy from that file.

**boto3**, the AWS SDK for Python, for all DynamoDB access. The client is built
at module import so it lands in the Lambda init phase, which gets more CPU and
is not billed. That fixed a cold start which was losing the share link.

**Amplify build spec**, the `amplify.yml` in the repository, so the hosting
configuration lives in git rather than in a console form.

The whole thing also runs with no AWS account at all. Storage falls back to a
local JSON file when no table name is set, and `python3 api/local_server.py`
wraps the same Lambda handler in a standard library HTTP server with nothing to
install. The deployment package is ten files and has no dependencies beyond
boto3.

Everything generated is checked. `tools/build_rules_js.py` emits the browser
copy of the rules from the Python source and `tools/train_model.py` emits the
model, and `tools/check_parity.py` runs 155 messages through both languages and
compares the score, the band, the rule ids, the reason text, the normalised
text, every highlighted phrase and every model probability. It is currently
155 out of 155, which includes Hindi in Devanagari.

## 3. Team leader's contributions

Solo project, so all of it is mine.

- The rules engine: forty-seven detection rules with weights, quoted spans and
  stated reasons, plus the advice and the auto-generated reply.
- The text normaliser, which undoes the tricks scam messages use to get past
  filters: letters spaced out, an O typed as a zero, an accent on a vowel, with
  an index map so highlights still line up with what was pasted.
- The linear model: features, training, five-fold cross validation, Platt
  calibration and the export, written out rather than imported, so the maths is
  auditable.
- The structural URL checks, including an RFC 3492 punycode decoder written for
  the browser, because browsers do not expose one.
- The API on Lambda, the DynamoDB storage layer with a local fallback, and JSON
  error reporting so failures name themselves instead of collapsing into a bare
  502.
- Infrastructure: the SAM template and the live deploy.
- The generators and the parity check that keeps two implementations honest.
- The front end: offline-first scanning, the verdict card, the rule
  constellation, and an Android share target so the site appears in WhatsApp's
  own share sheet.
- Three chat front doors, all sharing one reply writer and differing only in
  plumbing: a Telegram bot, WhatsApp through Twilio's sandbox, and a Meta
  WhatsApp Cloud API webhook. All three verify that a request really came from
  who it claims, and all three are tested end to end with the network stubbed
  out. The first two are live.
- The test suites, the labelled corpus, the evaluation harness and the rule
  audit.
- Documentation and the demo.

Built with AI assistance (Claude) for code and copy. Every line was reviewed and
tested by me, and the disclosure is in the README as the rules require.

## 4. What I did not like about the AWS services

I had never deployed anything on AWS before this. Four things cost me real time,
and all four are the same failure: a default that is wrong for the obvious use
case, paired with an error that does not say which layer broke.

**Lambda Function URLs default to AWS_IAM auth.** You create a Function URL,
which exists specifically to make a function publicly reachable, and the default
makes it not publicly reachable. Calling it returns `{"Message":"Forbidden"}`
with no mention of authentication, no mention of the setting and no link. Four
possible causes, one useless message. The creation screen could reasonably ask
"is this endpoint public?" instead of silently picking the answer that breaks.

**Uploading a .zip does not update the handler string.** The console creates a
function expecting `lambda_function.lambda_handler`. My file was `handler.py`,
so it failed with a 502 and a completely empty body. The upload dialog has just
read the archive and knows what filenames are in it. It could say that no file
matching the configured handler exists, right there, instead of letting me
deploy something that cannot start.

**The three second default timeout.** A hello world fits inside it. A first
DynamoDB call on a cold start does not. It surfaces as `Internal Server Error`
with nothing indicating that time was the issue. I worked it out only because I
noticed the request had taken 3.13 seconds and happened to know the default. A
timeout is a known, measured condition, and Lambda could say "function timed out
after 3s" in the response body the way it does in the logs.

**Function URL CORS stacks silently with application CORS.** With CORS
configured on the Function URL, AWS adds the headers itself. My handler was also
adding them, so every response went out with
`Access-Control-Allow-Origin: *, *`, which every browser rejects. The worst part
is how it fails: curl was perfectly happy and only the actual web page broke.
Nothing in the console warns that both layers will write the same header.

One smaller one: **boto3 returns DynamoDB numbers as `Decimal`**, which
`json.dumps` refuses. It is documented, but it means the very first thing anyone
does with a stored item, hand it back as JSON, throws a `TypeError` from inside
the standard library rather than anywhere near the DynamoDB call.

## 5. What I did like about the AWS services

**Lambda Function URLs removed an entire service from my design.** I had assumed
API Gateway was mandatory for an HTTP endpoint and had started reading about
stages and deployments. One screen, one CORS checkbox, and that service was gone
from the architecture at no extra cost. For a project this size that is the
difference between shipping and not.

**DynamoDB TTL is one attribute name in a settings panel.** I typed
`expires_at`, set a timestamp when writing, and the rows delete themselves. Data
that expires by default is exactly the right shape for something holding other
people's private messages, and it took thirty seconds instead of a cleanup job I
would have had to write, schedule, monitor and eventually get wrong. Provisioned
capacity at 1 and 1 also let me be certain about cost rather than hopeful.

**Amplify Hosting connected straight to GitHub and stayed out of the way.** No
pipeline to configure. It found the `amplify.yml` in my repository and did not
make me guess at build settings for a site that has no build. Every push
redeployed in about a minute, so I could fix something and check it live
immediately.

**CloudWatch Logs had the answer every single time.** Every one of the 502s
above named itself in the traceback. Once I stopped guessing and started reading
the log group, each problem took a couple of minutes instead of twenty. The log
stream appearing automatically with no configuration is the reason a first time
AWS user could debug this at midnight.

**AWS SAM** let me describe the function, the table, the TTL and the Function
URL in one readable file, so the deploy is reviewable in a pull request and
anyone can reproduce my stack instead of clicking through the console the way I
did the first time.

## 6. Anything else

Two things I would want a judge to look at, because they are the parts I am
least able to fake.

**The evaluation is in the repository and it reports its own weaknesses.**
`python3 tools/eval.py` runs 155 labelled messages, 93 fraud across twenty-two
families and 62 legitimate ones chosen to be hard: real bank OTP alerts, a real
RBI KYC reminder, delivery notifications with OTPs in them, recruiters,
marketing full of urgency words, and friends talking about money. It currently
catches 93 of 93 and raises zero false positives. It also says plainly in the
README that I wrote the test set, which will always flatter the rules, and that
real forwards would help more than anything else.

**I audited the rulebook against somebody else's data.**
`python3 tools/audit_rules.py` runs the rules over an external Indian SMS corpus
from Hugging Face. That dataset turns out to be templated rather than collected,
5,951 spam rows sharing 41 distinct skeletons, which makes it useless for
training and genuinely useful as an inventory of shapes. The first run covered
29 of 41. The twelve misses became three new rules and several widened patterns,
and coverage is now 41 of 41 with no new false positives. The audit also prints
how often each rule fires, which is how two rules were found to be untested
rather than useless.

The honest limitation: every number above is measured on messages I wrote or on
templates somebody generated. Forty real forwards would change that, and it is
the next thing I would do.
