# First Commit submission answers

Project: Pakka, check before you pay
GitHub: https://github.com/vaibhav375/pakka
Live: https://main.d1nvlrv96k8kj1.amplifyapp.com/
Tracks: Build It and Ship It

---

## 1a. What does your project do?

Pakka checks a message before you act on it. You paste in a text, a WhatsApp
forward, an email, anything, and it answers in plain sentences: whether this
looks like a scam, which specific parts of it are the problem, and why. It
quotes the exact words that set off each flag instead of just handing you a
score and expecting you to trust it.

Then it does the part most tools skip. It tells you what to do next. Do not
pay, do not share the OTP, report it at cybercrime.gov.in or call 1930, and do
that inside the first hour while the money can still be frozen. It also writes
a short reply you can send straight back to whoever forwarded the message to
you, so you are not stuck trying to find the words.

The check itself is twenty-one rules written in ordinary Python. No model gets a
vote. That means the same message always produces the same verdict, and every
verdict can be explained line by line. The rules are generated into JavaScript
at build time, so the whole check runs on your own device. Nothing you paste
ever leaves your phone unless you choose to create a shareable link.

## 1b. What problem does it solve, and who is it for?

Most people who get a scam message already sense that something is off. That is
not where they get stuck. They get stuck on two things: they cannot point at
what exactly is wrong, and there is nobody to ask in the thirty seconds before
they tap the link. So they either pay, or they forward it to whoever in the
family is considered good with phones and wait.

I am that person in my family. My mother forwards me messages to check. So do
my juniors, PG listings, internship offers, "your KYC has expired" texts. Every
single time the answer has the same shape: this line here is the problem, and
this is why. Pakka is that answer, available without me.

It is for anyone in India who gets sent something that smells wrong and has
nobody to ask. Parents and grandparents especially, but also students getting
fake internship offers and first job letters, and people being contacted about
a courier stuck at customs or an electricity bill about to be cut tonight.

There is a second half of the problem that is harder than catching scams, and
it is the reason most tools like this fail. If the tool flags everything, people
stop listening to it, and then it is worse than useless. So an ordinary message
has to come back clean. A real message from a college placement cell is a test
case in the repository, and it has to score zero, every time.

## 2. How did you use AWS?

Everything runs in ap-south-1, Mumbai, because the people using this are in
India and their messages should not leave the country to be checked.

### Ship it: AWS services

**AWS Lambda** runs the API on Python 3.12. One function, two routes, scan a
message and fetch a saved verdict. Traffic for a tool people open only when
something looks wrong is spiky and mostly zero, so paying for a server by the
hour is the wrong shape for it.

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
got the thing working tonight.

**AWS IAM** for the execution role scoped to just that one table.

On cost: at a thousand scans a month the whole stack stays inside the free
tier. At a hundred thousand, the Lambda invocations are still free and the only
line that starts costing anything is the DynamoDB writes.

### Build it: AWS open source stack

**AWS SAM**, the Serverless Application Model. The entire stack is described in
one `template.yaml` in the repository: the function, the table, the TTL
attribute, the Function URL and its CORS config. Anyone can deploy their own
copy of this from that file.

**boto3**, the AWS SDK for Python, for all DynamoDB access. The client is built
at module import so it lands in the Lambda init phase, which gets more CPU and
is not billed, which fixed a cold start that was losing the share link.

**Amplify build spec**, the `amplify.yml` in the repository, so the hosting
configuration lives in git rather than in a console form.

The same handler also runs with no AWS account at all. Storage falls back to a
local JSON file when no table name is set, and `python3 api/local_server.py`
wraps the Lambda handler in a standard library HTTP server with nothing to
install. And `tools/build_rules_js.py` generates the browser copy of the rules
from the Python source, with `tools/check_parity.py` asserting that Python and
JavaScript agree on every single case, so the on device check and the cloud
check can never drift apart.

## 3. Team leader's contributions

Solo project, so all of it is mine.

- The rules engine: twenty-one detection rules in Python with weights, quoted spans
  and stated reasons, plus the advice and auto reply generator.
- The test set, including the false positive cases that ordinary messages have
  to pass.
- The API: Lambda handler, routing, DynamoDB storage layer with the local file
  fallback, and JSON error reporting so failures name themselves instead of
  collapsing into a bare 502.
- Infrastructure: the SAM template, and the live deploy on Lambda, DynamoDB,
  Amplify and CloudWatch.
- The rules to JavaScript generator and the parity check that keeps the two
  implementations honest.
- The entire front end: offline first scanning, the verdict card, the three.js
  rule constellation, and all of the motion work.
- Documentation, README, architecture notes, and the demo video.

Built with AI assistance (Claude) for code and copy. Every line was reviewed and
tested by me, and the disclosure is in the README as the rules require.

## 4. What I did not like about the AWS services

I had never deployed anything on AWS before this. Four things cost me real time,
and all four are the same failure: a default that is wrong for the obvious use
case, paired with an error message that does not say which layer broke.

**Lambda Function URLs default to AWS_IAM auth.** You create a Function URL,
which exists specifically to make a function publicly reachable, and the default
makes it not publicly reachable. Calling it returns `{"Message":"Forbidden"}`
with no mention of authentication, no mention of the setting, and no link. Four
possible causes, one useless message. The creation screen could reasonably ask
"is this endpoint public?" instead of silently picking the answer that breaks.

**Uploading a .zip does not update the handler string.** The console creates a
function expecting `lambda_function.lambda_handler`. My file was `handler.py`,
so it failed with a 502 and a completely empty body. The upload dialog has just
read the archive and knows exactly what filenames are in it. It could tell me
that no file matching the configured handler exists, right there, instead of
letting me deploy something that cannot possibly start.

**The three second default timeout.** A hello world fits inside it. A first
DynamoDB call on a cold start does not. It surfaces as `Internal Server Error`
with nothing indicating that time was the issue. I only worked it out because I
noticed the request had taken 3.13 seconds and happened to know the default. A
timeout is a known, measured condition, and Lambda could say "function timed
out after 3s" in the response body the way it does in the logs.

**Function URL CORS stacks silently with application CORS.** With CORS
configured on the Function URL, AWS adds the headers itself. My handler was also
adding them, so every response went out with
`Access-Control-Allow-Origin: *, *`, which every browser rejects. The worst part
is how it fails: curl was perfectly happy, the endpoint looked completely fine
from the terminal, and only the actual web page broke. Nothing in the console
warns that both layers will write the same header.

One smaller one: **boto3 returns DynamoDB numbers as `Decimal`**, which
`json.dumps` cannot serialise. It is documented, but it means the very first
thing anyone does with a stored item, hand it back as JSON, throws a `TypeError`
from inside the standard library rather than anywhere near the DynamoDB call.

## 5. What I did like about the AWS services

**Lambda Function URLs removed an entire service from my design.** I had assumed
API Gateway was mandatory for an HTTP endpoint and had already started reading
about stages and deployments. One screen, one CORS checkbox, and that whole
service was gone from the architecture, at no extra cost. For a project this
size that is the difference between shipping tonight and not.

**DynamoDB TTL is one attribute name in a settings panel.** I typed
`expires_at`, set a timestamp when writing, and the rows delete themselves. Data
that expires by default is exactly the right shape for something holding other
people's private messages, and it took thirty seconds instead of a cleanup job I
would have had to write, schedule, monitor and eventually get wrong. Provisioned
capacity at 1 and 1 also let me be certain about cost rather than hopeful, which
matters a lot when you are on free tier.

**Amplify Hosting connected straight to GitHub and stayed out of the way.** No
pipeline to configure. It found the `amplify.yml` in my repository and did not
make me guess at build settings for a site that has no build. Every `git push`
redeployed in about a minute, which meant I could fix something and check it
live immediately.

**CloudWatch Logs had the answer every single time.** Every one of the 502s I
described above named itself in the traceback. The moment I stopped guessing and
started reading the log group, each problem took a couple of minutes instead of
twenty. The log stream appearing automatically with no configuration at all is
the reason a first time AWS user like me could debug this at midnight.

**AWS SAM** let me describe the function, the table, the TTL and the Function
URL in one readable file, so the deploy is reviewable in a pull request and
anyone can reproduce my stack instead of clicking through the console the way I
did the first time.
