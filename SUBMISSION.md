# Submission fields — First Commit

Copy these into the form. Tracks: submit to **both** Build It and Ship It.

**Project title:** Pakka — check before you pay
**GitHub:** https://github.com/vaibhav375/pakka
**Deployed:** https://main.d1nvlrv96k8kj1.amplifyapp.com/

---

## What does your project do?

My mother forwards me messages to check. So do my juniors — PG listings,
internship offers, "your KYC has expired" texts. Every time, the answer has the
same shape: this line here is the problem, and this is why. The person asking
usually already felt something was off. What they lacked was the confidence to
say no and the words to explain it to whoever sent it.

Pakka takes a pasted message and answers in sentences. It names which parts are
a problem, quotes the exact words, tells you what to do next — do not pay,
report at cybercrime.gov.in or 1930, report inside the first hour while the
money can still be frozen — and writes a reply you can send straight back.

The check is twenty rules in plain Python, generated into JavaScript so the same
rules run on the device. No model gets a vote, which means the same message
always produces the same verdict and every verdict can be explained. Ordinary
messages have to come back clean or the tool cries wolf, so a real placement-cell
message is a test case in the repo.

It is for anyone in India who gets sent something that smells wrong and has
nobody to ask.

## How did you use AWS?

**Ship It.** The front end is static and deploys from GitHub on **Amplify
Hosting** with no build step, so build minutes stay at zero. The API is one
**Lambda** (Python 3.12) behind a **Lambda Function URL** — chosen over API
Gateway because one public HTTPS endpoint with CORS was all this needed, and
Function URLs carry no additional charge where API Gateway's free tier expires
after twelve months. Scans are stored in **DynamoDB**, provisioned at 1 read and
1 write unit so it sits inside the always-free 25 of each, with a 30-day TTL
because a scan is evidence for the person who nearly paid, not an archive.
**CloudWatch Logs** carries the traces, and the whole stack is described as one
**AWS SAM** template in the repo.

Cost reasoning: traffic for a tool people open when something looks wrong is
spiky and mostly zero, so a server billed by the hour is the wrong shape. At
1,000 scans a month everything stays inside the free tier; at 100,000 the Lambda
invocations are still free and DynamoDB would move to on-demand at roughly $0.13
for the writes.

**Build It.** The same handler runs locally with no AWS account: storage falls
back to a JSON file when no table name is set, and `python3 api/local_server.py`
wraps the Lambda handler in a stdlib HTTP server. The SAM template is the
open-source AWS piece, and `tools/build_rules_js.py` generates the browser copy
of the rules from `api/rules.py` so the two cannot drift — `tools/check_parity.py`
asserts Python and JavaScript agree on every case.

## What you did NOT like about the AWS services

Four things cost me real time tonight, all of them the same failure: a default
that is wrong for the obvious use case, and an error that does not say so.

**Lambda Function URLs default to AWS_IAM auth.** Creating one for a public API
and forgetting to switch it returns `{"Message":"Forbidden"}` — no mention of
auth, no mention of the setting, no pointer. Four possible causes, one message.

**Uploading a .zip does not update the handler string.** The console creates the
function expecting `lambda_function.lambda_handler`; my file was `handler.py`. It
fails as a 502 with an empty body. The upload dialog knows the filenames in the
archive and could say so.

**The 3-second default timeout.** A hello-world fits in it; a first DynamoDB call
from a cold start does not. It surfaces as `Internal Server Error` with no hint
that time was the problem — I only found it by noticing the request took 3.13
seconds and knowing the default.

**Function URL CORS stacks with application CORS silently.** With CORS configured
on the Function URL, AWS adds the headers itself. My handler added them too, so
responses carried `Access-Control-Allow-Origin: *, *`, which every browser
rejects. The API answered curl perfectly and failed from the page. Nothing in the
console warns that the two layers will both write the header.

## What you DID like

**Lambda Function URLs** removed a whole service from the design. I had assumed
API Gateway was mandatory for an HTTP endpoint; one screen and a CORS checkbox
replaced it, and it costs nothing extra.

**DynamoDB TTL** is a single attribute name in a settings panel and the rows
delete themselves. Data that expires by default is the right shape for something
holding other people's messages, and it took thirty seconds rather than a cleanup
job I would have had to write, schedule and monitor.

**Amplify connecting straight to GitHub** meant every `git push` redeployed the
site with no pipeline to configure — it even read the `amplify.yml` in the repo
and did not ask me to guess build settings for a site with no build.

**CloudWatch had the answer every time.** Once I stopped guessing at the 502s and
read the log group, each failure named itself in the traceback.

## Learning and growth

I had never deployed anything on AWS before tonight. The specific thing I learned
is less about any one service and more about how serverless fails: the request
path has four or five layers — auth, runtime config, handler resolution, timeout,
CORS — and each one fails with a generic HTTP error that does not name the layer.
A 502 with an empty body can be a handler mismatch, a timeout or an exception,
and those are three different fixes. I learned to stop guessing, read CloudWatch,
and then make the function report its own errors as JSON rather than collapsing
into a bare 502 — which is now in the code.

The other thing: a Function URL with CORS configured adds the header itself, so
adding it in the application produces a duplicate the browser refuses while curl
sails through. I would not have found that without testing in an actual browser,
and I now test both.

## Contributions — Vaibhav Handoo (solo)

Everything: the rule engine and its tests, the Lambda API and DynamoDB storage,
the SAM template, the rules-to-JavaScript generator and parity check, the
offline-first front end including the three.js rule constellation, the AWS
deploy, and the writeup. Built with AI assistance (Claude) for code and copy,
reviewed and tested by me.
