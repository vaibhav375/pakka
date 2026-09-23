# Pakka, explained

Everything this project is, in the order it happens. Each stage says what it
does, how to explain it out loud, and what is actually going on underneath.

---

# 1. The answer to "what did you build?"

Keep this to four sentences. Everything else is follow-up.

> Pakka checks a message before you act on it. You forward it a WhatsApp text
> or a bank SMS, and it tells you whether it is a scam, quotes the exact words
> that are the problem, tells you what to do next, and writes a reply you can
> send straight back to whoever forwarded it. Forty-seven rules decide the
> verdict, so the same message always gives the same answer and every answer
> can be explained. It runs on the device, so nothing you paste leaves your
> phone unless you press Share.

Three things in that paragraph are deliberate, and each one is a door into a
longer conversation:

- **"quotes the exact words"** leads to explainability.
- **"the same answer every time"** leads to why there is no LLM making the call.
- **"runs on the device"** leads to the architecture.

Let them pick.

---

# 2. The problem, told as a story

Do not open with market size. Open with this:

> My mother forwards me messages to check. So do my juniors, about PG listings
> and internship offers. Every time, my answer has the same shape: *this line
> here is the problem, and this is why.* They usually already felt something
> was off. What they did not have was the words to explain it, or anyone to ask
> in the thirty seconds before they tapped the link.

Then name the two halves of the problem, because the second one is the one
interviewers do not expect:

**The obvious half.** Catching scams.

**The half that decides whether it works.** Not flagging ordinary messages. A
tool that shouts at everything gets ignored, and an ignored tool is worse than
no tool, because the one time it is right nobody is listening.

So the test set is built from both directions. These all have to come back
clean, and they are all in it:

- a genuine bank OTP: *"Your OTP is 452891. Never share this with anyone."*
- a real RBI periodic-KYC reminder, which tells you to visit a branch
- a delivery message containing an OTP, telling you to share it with the agent
- a friend asking for your account number to send you trip money
- marketing full of urgency: *"last chance"*, *"today only"*, *"limited time"*

If you only get thirty seconds on the problem, use it on that second half. It
is the part that shows you thought about the user rather than the algorithm.

---

# 3. Architecture

## Where the work happens

The important thing about this diagram is how little of it is in the cloud.

```
  ON THE DEVICE                      IN THE CLOUD (only if you share)
  ----------------------------       ---------------------------------

  browser / phone
      |
      |  normalise -> 47 rules -> model -> advice
      |  verdict, quoted words, what to do now
      |  12 KB of arithmetic, works with no network
      |
      +---- press Share ---------->  Lambda Function URL
                                          |
                                          v
                                     Lambda (Python 3.12)
                                          |
                                          +---> DynamoDB  (30-day TTL)
                                          +---> CloudWatch Logs

  Telegram bot      ------------->  POST /telegram  --+
  WhatsApp (Twilio) ------------->  POST /twilio    --+--> same pipeline,
  Android share sheet -----------> the page itself       same reply text
```

Say it like this:

> The verdict is computed on the device. The cloud exists for exactly one
> reason: to mint a link so you can show the verdict to whoever sent you the
> message. That means the tool works with the network off, and it means the
> message does not leave the phone unless the person chooses to share it.

## The decision pipeline

```
  message text
      |
      v
  [1] NORMALISE ............. drop accents, map digits standing in for
      |                       letters, pull spaced-out letters together.
      |                       Returns the cleaned text AND an index map
      |                       back to the original.
      v
  [2] 46 REGEX RULES ........ each carries a weight, a quoted span, and
      |                       the reason it exists.
      v
  [3] STRUCTURAL CHECKS ..... one rule is answered by code, not a pattern:
      |                       mixed scripts, punycode, digits in a brand
      |                       name, a bare IP address.
      v
  SCORE -> BAND ............. 8+  almost certainly | 5-7 likely
      |                       2-4 be careful | 1 one flag | 0 clear
      v
  [4] LINEAR MODEL .......... a calibrated probability, plus the phrases
      |                       it reacted to. Runs in parallel, not after.
      v
  [5] FUSE .................. rules decide. The model may raise concern
      |                       and may never clear a flagged message.
      v
  [6] ADVICE ................ numbered steps chosen by which rules fired,
      |                       plus a reply built only from those rules.
      v
  [7] PERSIST (optional) .... save the verdict, return a link, expire it
      |                       after 30 days.
      v
  verdict on screen, or in the chat the message arrived in
```

## One source of truth, generated twice

This is the diagram to draw if someone asks how the browser and the server stay
in agreement.

```
  api/rules.py            <- a rule is written here, and only here
  api/features.py         <- text becomes numbers here, and only here
      |
      |  generated, never hand-edited
      |
      +--> web/rules.generated.js      (47 rules, for the browser)
      +--> web/model.generated.js      (789 weights, for the browser)
      +--> api/model.json              (the same weights, for Lambda)
      |
      v
  tools/check_parity.py
      runs 155 messages through Python AND through Node, and compares:
        - the score, the band, which rule ids fired
        - the reason text, including generated URL explanations
        - the normalised text, character for character
        - every highlighted quote
        - the model's probability to six decimal places
      currently 155 / 155, including Hindi in Devanagari
```

The line worth saying out loud:

> A generated file is only trustworthy if something checks the generation.

---

# 4. Stage one: normalisation

## What it does

Scam messages are written to get past filters. `K Y C` spaced out. `0TP` with a
zero. `shäre` with an accent. `C-l-i-c-k` with hyphens.

You can write a pattern for each trick, or you can undo the tricks once and
keep every pattern simple. This does the second.

## How to explain it

> Before any rule runs, the text is cleaned up. Accents come off, digits that
> are standing in for letters get mapped back, and letters that have been
> spaced apart get pulled together. So one rule for "OTP" catches `0TP`,
> `O T P` and `otp` without knowing anything about those tricks.

## The technical part

Four transformations, in order:

1. **Decompose and drop combining accents.** `ä` becomes `a`.
2. **Map digits that stand in for letters** — `0`→`o`, `1`→`i`, `3`→`e` — but
   only where a letter sits directly beside the digit. `0TP` becomes `OTP`;
   a phone number and a rupee amount are untouched.
3. **Collapse spaced-out letters.** Three or more single letters separated by
   the *same* character join up: `K Y C` → `KYC`, `C-l-i-c-k` → `Click`. The
   separator must be consistent, or `W-O-N a prize` would collapse to `WONa`.
4. **Replace anything outside the basic plane with a placeholder**, so an emoji
   counts as one character rather than two.

The return value is the part worth understanding:

```python
def normalise(text: str) -> tuple[str, list[int]]:
    # the cleaned text, AND a map from each cleaned character
    # back to its position in the original
```

Without that map, a highlight computed on the cleaned copy would land in the
wrong place in the message the person actually pasted. With it, `Your K Y C has
expired` highlights `K Y C has expire` **in the original spacing**, even though
the rule matched `KYC`.

Every span is then grown out to whole words, so you never see `KYC has expire`
with a stranded `d`.

## If they push

**"Why not just lowercase and strip punctuation?"** Because the highlight has
to point back at the original. Any transformation that changes length has to
carry a map, and once you are carrying a map you may as well undo the harder
tricks too.

**"What broke here?"** The word-boundary test used `str.isalnum()`, which
returns False for a Hindi vowel sign because it is a combining mark. So a
highlight stopped mid-word and showed `ेट` where the word is `अपडेट`. The fix
was an explicit character class that includes the Devanagari block but excludes
the danda, which is punctuation that happens to live inside that same block.

---

# 5. Stage two: the rules

## What it does

Forty-seven rules. Each one knows a single shape that scams take, carries a
weight, and can point at the words that set it off.

## How to explain it

> A rule is not just a pattern. It carries the reason it exists, and that
> reason is what the person reads. So the output is never "score 8 out of 10",
> it is "this asks for your OTP, and nobody legitimate ever does."

Give them one example, and pick this one, because the reasoning is the
interesting part rather than the regex:

> **A QR code to receive money.** Scanning a QR code can only send money out of
> your account. It can never bring money in. So anyone telling you to scan one
> to claim something is describing a thing that cannot happen.

## The technical part

```python
@dataclass(frozen=True)
class Rule:
    id: str          # LOOKALIKE_DOMAIN
    name: str        # "A web address dressed up as a real company"
    why: str         # the sentence the person reads
    weight: int      # 1 to 4
    pattern: re.Pattern
```

`evaluate()` normalises once, runs every pattern against the normalised copy,
maps the spans back to the original, sums the weights, and picks a band:

| score | verdict |
|---|---|
| 8 or more | Almost certainly a scam |
| 5 to 7 | Likely a scam |
| 2 to 4 | Be careful |
| 1 | One thing to check |
| 0 | Nothing suspicious found |

**Weights are assigned on one principle:** how often is this shape wrong when it
appears in an ordinary message? Asking for an OTP is a 4, because nothing
legitimate does it. Manufactured urgency is a 1, because real messages are
sometimes genuinely urgent.

## If they push

**"Isn't this brittle?"** Yes, and that is measured rather than argued about.
Out of domain the rules catch 8% of real spam. That number is in the
documentation, and it is the entire reason there is also a model.

**"How do you decide a weight?"** By asking what it costs to be wrong. A weight
of 4 on its own reaches "Be careful", so a 4 is reserved for shapes that are
never innocent.

---

# 6. Stage three: the checks a pattern cannot express

## What it does

A pattern can look for the word "sbi". It cannot tell you that the **а** in
`аmazon.in` is Cyrillic, or that `xn--80ak6aa92e.com` is displayed in the
address bar as `аррӏе.com`.

## How to explain it

> Some things about a web address are properties of the characters, not of any
> phrase. Those get answered by code rather than a pattern, and the code
> reports its reason in words, so the person is told *the word "аmazon" is
> written in two alphabets at once* rather than just being warned.

## The technical part

Four checks on the host of every URL in the message:

- **Mixed scripts inside one word.** The letters of each label are classified by
  Unicode script. A word using two is a word pretending to be another word.
- **Punycode.** `xn--80ak6aa92e.com` is what is stored, `аррӏе.com` is what is
  shown. Browsers hand you the `xn--` form, which is exactly the form that
  hides the problem, so the browser half of this project contains an **RFC 3492
  decoder written out by hand**.
- **Digits inside a brand word.** `amaz0n-delivery.info`.
- **A bare IP address**, which is not a name anybody registered.

This is wired in as the 47th rule, with a pattern that can never match, so it
appears in the rulebook and scores like everything else while being answered
structurally.

## If they push

**"Why write your own punycode decoder?"** Because no browser exposes one.
`new URL()` returns the encoded form. The decoder is about forty lines, and the
parity check verifies it produces character-identical output to Python's IDNA
decoder across the whole corpus.

---

# 7. Stage four: the model

## What it does

Rules have perfect precision on what they describe and **no opinion at all
about anything else**. A scam phrased in words nobody wrote down scores zero.
The model covers that.

## How to explain it

> The rules are precise and narrow. A model is broad and fuzzy. I wanted both
> without letting the fuzzy one make the decision, so there is a linear model
> trained on 5,729 labelled messages that sits underneath the rules. Linear is
> the important word: a linear model's output is literally the sum of its
> per-feature contributions, so I can lay those contributions back onto the
> text and show which characters it reacted to. It never has to be trusted.

## The technical part

**Features.** The message is normalised, lowercased, and cut into every
character sequence of length 3, 4 and 5. Character n-grams rather than words,
because scam text is full of misspellings, spacing tricks and Hinglish, and
`kyc` inside `kycupdate` carries the same signal as the word alone.

Each n-gram is hashed with 32-bit FNV-1a into one of 16,384 buckets. Hashing
rather than a vocabulary means the feature space is fixed, the file is small,
and a word never seen in training still lands somewhere sensible. Buckets are
deduplicated and the vector is L2 normalised, so a long message does not simply
outvote a short one.

**Training.** Logistic regression by stochastic gradient descent, written out
rather than imported, so the maths is auditable. Three details carry the result:

- **Positives are upweighted**, because the data is about eight to one against
  them.
- **The Indian corpus is upweighted twelvefold** on top of that, because it is
  2% of the rows and 100% of the domain that matters.
- **L1 regularisation by soft thresholding.** Plain magnitude pruning barely
  dented the model, because SGD leaves almost every bucket slightly non-zero.
  L1 drives the useless ones to exactly zero, which took the shipped file from
  **245 KB to 12 KB**. That is the difference between shipping a model to a
  phone and not.

**Calibration.** The raw output of a logistic regression is a number between 0
and 1, but it is not a probability you can quote. A second one-dimensional
logistic fit is applied on top, fitted **only on out-of-fold predictions**,
never on anything the model trained on:

| predicted | actually fraud |
|---|---|
| 0.0 – 0.2 | 0.20 |
| 0.2 – 0.4 | 0.32 |
| 0.4 – 0.6 | 0.45 |
| 0.6 – 0.8 | 0.68 |
| 0.8 – 1.0 | 0.94 |

**That table is load-bearing, not decoration.** It is why the interface requires
0.75 before it will say "this reads like a scam": at 0.6 the odds are only about
seven in ten, and telling somebody their delivery notification is a scam on
those odds is how a tool stops being believed.

**Explainability.** Each bucket's weight is divided across the characters its
n-gram came from, producing a heat value per character. Contiguous runs above a
threshold are the phrases the model reacted to, grown out to whole words before
being shown. That is how it can say *"it reacted most to Your KYC, share, now
within"* instead of asking you to trust a number.

## Does it earn its place?

The Indian corpus cannot answer that, because the rules were written against it
and score 100% on it. An external corpus can, honestly, because no rule here has
ever seen a 2012 British SMS. On 1,115 held-out messages from it:

| | precision | recall |
|---|---|---|
| rules alone | 0.79 | **0.08** |
| model alone | 0.93 | **0.90** |

The rules are nearly blind out of domain. The model catches **120 spam messages
no rule fires on**. That is the whole argument for it, and it is a measurement
rather than a claim.

## If they push

**"Why not a transformer?"** Three reasons in order: it has to run on the
device with no network, it has to give the same answer every time, and it has to
be explainable to the person who nearly paid. A linear model over hashed
n-grams satisfies all three at 12 KB. A transformer satisfies none of them here.

**"Isn't 16,384 buckets a lot of collisions?"** Some, and that is the trade for
a fixed-size model. It is measurable: the calibration table and the
out-of-domain numbers are what they are *with* those collisions.

---

# 8. Stage five: fusion, and who gets the last word

## What it does

Combines three sources of evidence without letting the fuzzy one overrule the
precise one.

## How to explain it

This is the single most important design decision in the project, so say it as
a rule:

> Rules decide. The model may raise concern, and it may never clear a message
> the rules flagged.

And then say why the asymmetry matters:

> The dangerous failure is not a false alarm. It is a headline that says
> "nothing suspicious found" over a message the model scored 90 out of 100,
> because the headline is all many people read.

## The technical part

Four combinations, and each says something different to the person:

| rules | model | what the interface says |
|---|---|---|
| fired | high | "The model agrees with the rules independently." |
| fired | low | "The model is less sure. The rules above quote the exact words, so they are the ones to read." |
| nothing | ≥ 0.75 | "**No rule fired, but this still reads like a scam.**" The headline becomes *Nothing matched, but be careful*, and the dial switches from the rule score to the model's number. |
| nothing | 0.5–0.75 | "Nothing matched, and the model is not certain either. Around half the messages it reads that way are fine." |

That third row is also the **rule-discovery pipeline**. Every message where the
model is confident and no rule can explain why is a candidate for the next rule,
with the evidence already attached.

## If they push

**"Give me an example of that discovery loop working."** A message reading
*"claim your free tablet now by clicking on this link"* scored zero on the rules
and 90 on the model. Investigating why produced three new rules: the prize list
knew about free iPhones but not free tablets, nothing covered "claim … now", and
nothing covered a link with no destination named. That last one has the best
reasoning of any rule in the project: **messages you can trust tell you where
they are sending you, by name.**

---

# 9. Stage six: advice, and the reply

## What it does

Turns a verdict into something a person can act on, and into words they can
send back.

## How to explain it

> Telling somebody "this is a scam" is the easy part and not the useful part.
> They need to know what to do in the next ten minutes, and they need something
> to say to the person who sent it. So the rules that fired choose the steps,
> and they also write the reply.

## The technical part

**The steps are selected by which rules fired**, not printed as a fixed list.
If the OTP rule fired, the never-share-an-OTP line appears. If the message
impersonates an institution, the call-the-number-on-your-own-card line appears.
Then the universal ones, including the one that actually matters most:

> Report at cybercrime.gov.in or call 1930. If money has already gone, report
> within the first hour, while it can still be frozen.

That first-hour detail is the single most useful sentence in the product, and it
is worth knowing why: India's cybercrime system can freeze a transfer in transit,
and the window is short.

**The forwardable reply is built only from the rules that actually fired**, which
means it structurally cannot overstate the verdict:

> I checked this before replying — it uses a KYC or account-block scare and it
> asks for your OTP. That is how this kind of scam works, so I am not paying or
> sharing anything. Please do not send money either. (Checked with Pakka)

## If they push

**"Why does the reply matter?"** Because the person who forwarded it to you is
usually not the scammer, they are the next victim. Giving someone the words to
warn them is how one check protects more than one person.

---

# 10. Stage seven: persistence, and the only reason the cloud exists

## What it does

Saves a verdict so it can be linked to, and deletes it again.

## How to explain it

> Nothing is stored unless the person presses Share. When they do, the verdict
> is saved so the link can be opened by whoever sent them the message, and it
> deletes itself after thirty days. That table holds other people's private
> messages, so data that expires by default is the only shape I was comfortable
> with.

## The technical part

One DynamoDB table, one partition key, one item per scan. No queries, no scans,
no secondary indexes — the access pattern is literally "give me this one id".

The expiry is a single attribute:

```python
item["expires_at"] = int(time.time()) + 30 * 24 * 3600
```

DynamoDB's time-to-live feature deletes the item after that timestamp, for free,
in the background. It replaces a cleanup job you would otherwise write,
schedule, monitor and eventually get wrong.

---

# 11. The AWS layer, service by service

Six services. For each one: what it is, what it does here, and why it beat the
obvious alternative.

## What "serverless" actually means

There is no machine that belongs to this project. Nothing is running right now.

When a request arrives, AWS finds a spare slot on a machine it already has,
unzips a 90 KB bundle of Python into it, runs one function, sends the answer
back, and eventually throws the slot away. Between requests nothing exists and
nothing is billed.

Say it like this:

> For a tool people open only when something looks wrong, traffic is spiky and
> mostly zero. A server rented by the hour would sit idle almost all the time
> and still cost money every hour. That is the whole argument for serverless
> here, and it is also why the free tier is enough.

## AWS Lambda

**What it is.** A service that runs a single function in response to an event.
You hand it a zip file and the name of a function inside it. AWS handles
machines, scaling, patching and restarts.

**What it does here.** One function receives every request as a dictionary
describing the HTTP call, reads the path, and dispatches:

| path | what happens |
|---|---|
| `POST /scan` | scan a message, save the verdict, return it with an id |
| `GET /v/{id}` | fetch a saved verdict, for whoever received the link |
| `POST /telegram` | a Telegram message, answered in the same chat |
| `POST /twilio` | a WhatsApp message, answered in the HTTP response itself |
| `GET /whatsapp` | Meta's one-time webhook verification handshake |
| `GET /` | a health check reporting how many rules are loaded |

**The configuration that matters:** Python 3.12, 256 MB, **10 second timeout**.
The default timeout is 3 seconds, and that is a trap — a hello world fits inside
it, a first DynamoDB call on a cold start does not, and it surfaces as
`Internal Server Error` with an empty body and no hint that time was the issue.

**The cold-start idea worth knowing.** The first request into a new slot pays
for unzipping and importing. That phase is called **init**, and it has two
useful properties: it gets more CPU than the request itself, and it is **not
billed**. So anything expensive should happen at import time:

```python
# api/store.py — at module level, not inside the request
_ddb = boto3.resource("dynamodb", config=Config(
    connect_timeout=3, read_timeout=3, retries={"max_attempts": 2}))
```

That was a real bug here. Building the client inside the handler meant the first
scan after an idle period ran out of time and came back with no share link,
while every scan after it worked. Moving one line up a scope fixed it.

**Cost.** One million requests a month are always free, plus 400,000 GB-seconds
of compute. At 256 MB and roughly 80 ms a scan, this would need about twenty
million scans a month to leave the free tier.

## Lambda Function URLs

**What it is.** A permanent HTTPS address attached directly to a Lambda
function. Anything posted to it invokes the function.

**What it does here.** It is the entire API — the page calls it to mint a share
link, and both bots call it with incoming messages.

**Why not API Gateway**, which is what every tutorial reaches for. API Gateway
is a full HTTP router with stages, deployments, request validation, throttling
and usage plans. This needs exactly one public endpoint with CORS. Function URLs
carry **no additional charge**, while the API Gateway free tier expires after
twelve months — so a project meant to stay free forever would start costing
money in year two for a feature it never used.

**Two things that will bite you**, and both are good interview answers because
they show you debugged rather than followed a tutorial:

- **The default auth is `AWS_IAM`.** You create a Function URL, whose entire
  purpose is to make a function publicly reachable, and the default makes it
  unreachable. It returns `{"Message":"Forbidden"}` with no mention of
  authentication and no link.
- **CORS stacks.** Configure CORS on the Function URL and AWS adds the headers
  itself. If the code also adds them, every response carries
  `Access-Control-Allow-Origin: *, *`, which every browser rejects. The evil
  part is how it fails: `curl` is perfectly happy and only the real page breaks.

## Amazon DynamoDB

**What it is.** A managed key-value and document database. No server, no SQL, no
index management unless you want it. Each item has a **partition key**, and you
fetch by that key.

**What it does here.** One table, partition key `id`, one item per saved scan.

**Provisioned at 1 read unit and 1 write unit.** DynamoDB has two billing modes.
On-demand charges per request and needs no thinking. Provisioned reserves
capacity, and the always-free tier includes **25 read units and 25 write units
forever**. Setting 1 and 1 means the cost is not merely low, it is *certainly*
zero — which matters more than optimal for a tool that has to stay free.

**Time to live** is the best thing in this stack, for the reason given in stage
seven: this table holds other people's private messages.

**The gotcha worth mentioning.** boto3 returns DynamoDB numbers as `Decimal`,
which `json.dumps` refuses. So the very first thing anyone does with a stored
item — hand it back as JSON — throws a `TypeError` from inside the standard
library, nowhere near the DynamoDB call.

## AWS Amplify Hosting

**What it is.** Static hosting wired to a git repository, with a CDN and HTTPS.
Push to a branch and it redeploys.

**What it does here.** Serves the front end. The build configuration lives in
the repository and the build step is deliberately **empty**: there is no
bundler, no framework, no transpiler. The front end is HTML, CSS and JavaScript
that browsers already understand.

Why that is a decision and not laziness:

> Build minutes stay at zero, there is nothing to keep up to date, and nothing
> that can fail at deploy time. The generated files are generated on a laptop
> and committed, so what is in git is exactly what ships.

## Amazon CloudWatch Logs

**What it is.** Where Lambda's output goes. Every print and every uncaught
traceback lands in a log group, split into streams.

**What it does here.** It is the reason any of this works. Every problem listed
above named itself in a traceback.

The handler is built to cooperate with it. An uncaught exception in Lambda
becomes a bare 502 with an empty body, which tells the caller nothing and the
developer less. So it is caught, logged, and answered in the same JSON shape as
everything else, with a truncated exception type and message in a `detail`
field. That is the difference between "it's broken" and knowing which line
broke without opening the console.

## AWS IAM

**What it is.** Identity and Access Management — who may do what.

**What it does here.** The function runs as an **execution role** that grants
exactly two things: write to its own log group, and read and write **one**
DynamoDB table. It cannot touch another table, create resources, or read
secrets. If the function were compromised, the blast radius is one table of
expiring scans.

The principle, stated plainly: **a function should hold the smallest set of
permissions that lets it do its job**, because permissions are the only thing
standing between a bug and a breach.

## AWS SAM

**What it is.** The Serverless Application Model, an extension of
CloudFormation — infrastructure described in YAML instead of clicked in a
console.

**What it does here.** One template describes the function, the table, the TTL
attribute, the Function URL and its CORS configuration. Two reasons that
matters: anyone can deploy their own copy from that file, and any change to the
infrastructure is reviewable in a pull request rather than being something
somebody once clicked and cannot remember.

## The part that is not AWS at all

The same handler runs with **no AWS account whatsoever**. Storage falls back to
a local JSON file, and a standard-library HTTP server wraps the identical Lambda
handler.

That exists to guarantee that what runs on a laptop is the code that runs in
production rather than a sibling of it — and it earned its keep. It was once
passing the path with the query string still attached and never building the
query parameters, so a route matched on Lambda and missed locally. That is
precisely the drift it exists to prevent.

---

# 12. Reach: four front doors, and two languages

## Why the doors matter

> The scam arrives in a chat. Copying it out, opening a browser and pasting it
> is four things to do while somebody is rushing you, which is the moment they
> are least able to do them. So the answer comes back where the message already
> is.

| door | how it works |
|---|---|
| **The page** | offline-first; the cloud is only for minting a link |
| **Telegram** | Telegram has no request signature, so it echoes back a secret registered with the webhook, on every call |
| **WhatsApp via Twilio** | the reply is returned **in the HTTP response body** as TwiML, so there is no outbound API call and no access token to store. Requests are verified with an HMAC-SHA1 signature over the URL plus every parameter in sorted order |
| **Android share sheet** | the page declares a Web Share Target, so once installed it appears in the share sheet of every app. Long-press in WhatsApp, Share, Pakka. The shared text arrives as a query string, which is then wiped from the address bar so a stranger's message is not left in browser history |

A fifth exists — Meta's own WhatsApp Cloud API — written and tested and behind
unset environment variables, because Meta requires a business account and an app
review.

All of them share one module that writes the reply. They differ only in how a
message arrives and how one is sent. Every one returns 200 as soon as the
signature passes, because both Telegram and Twilio retry anything else, and a
retry would scan the message again and answer twice.

## Hindi

The engine read Devanagari and Hinglish before the interface did, which is a
strange thing for a tool built for people who mostly do not read English
comfortably.

Every line a person reads has a Hindi version: the five bands, all 47 rule
names, all 47 reasons, the advice, the forwardable reply, the labels. It is kept
beside the rules rather than inside them, so a rule stays one idea in one place
and a translation is a lookup. Anything missing falls back to English, which is
the right failure: an untranslated line is readable, a blank one is not.

Two details decide whether it reads as translated or as written:

- **Devanagari does not take letter-spacing.** The wide tracking used on English
  labels pulls conjuncts apart and makes Hindi look broken.
- **The bots detect the script and answer in it.** Somebody forwarding a Hindi
  scam is not helped by an English explanation of it, and asking them to pick a
  language first is one more step at the worst possible moment.

---

# 13. How well it actually works

This is the section to be most careful about, because it is where it is easiest
to fool yourself — and where being honest is worth more than being impressive.

## The corpus I wrote

155 labelled messages: 93 fraud across 22 families, and 62 legitimate ones
chosen to be hard. **93 of 93 caught, 0 of 62 false positives.**

Say the caveat in the same breath as the number:

> That flatters the rules, because the same person wrote both the rules and the
> test set.

## Somebody else's data

An external Indian SMS corpus, used to audit coverage. It turns out to be
**templated rather than collected**: its 5,951 spam rows share 41 distinct
skeletons, 0.7% unique. Useless for training. Genuinely useful as an **inventory
of shapes**, counted once each so a template repeated 353 times does not vote
353 times.

First pass covered **29 of 41**. The twelve misses became three new rules and
several widened patterns. Now **41 of 41**, with no new false positives.

## Real messages, measured three times

Three sets of real scam messages quoted from published sources, including the
government's own fact-check unit. Each was measured **once while frozen**, then
deliberately spent fixing what it exposed, and a fresh set collected from
different sources to find out whether the fixes generalised or only memorised.

| round | messages | rules reach "be careful" | what it exposed |
|---|---|---|---|
| one | 25 | **52%** | fake transaction alerts, reward-point expiry, digital arrest, demands for secrecy, service suspension, failed-delivery address updates |
| two | 20 | **75%** | traffic challans, bills that ask to be "updated", mixed Latin and Devanagari in one message |
| three | 10 | **80%** | government scheme names used as bait |

**52%, then 75%, then 80% — each on messages the rules had never seen — against
100% on the corpus I wrote.**

If an interviewer asks for one number, give them that progression and the reason
the last one is lower than the first. It is the most useful thing this project
measured about itself, and it is also the clearest argument for the model, which
caught 24 of those first 25 where the rules caught 13.

---

# 14. What is weak

Say these before anyone finds them. Volunteering a limitation is worth more than
defending against one.

1. **Every corpus is self-written or published-example.** All three holdout sets
   are now spent. The next honest number needs real forwards from real phones,
   which is the highest-value thing anyone could contribute.
2. **Published examples skew** towards campaigns big enough to be written about.
3. **Ten-message sets cannot resolve a percentage** better than about ten points.
4. **Forty-seven rules is forty-seven shapes.** A genuinely novel scam is
   invisible to all of them, and the model is the only thing behind them.
5. **The model's training data is mostly foreign.** The bulk of it is British SMS
   spam from 2012, which teaches "free", "win" and "claim" and nothing about UPI,
   APK sideloading or remote-access apps.
6. **The WhatsApp sandbox only answers numbers that sent a join code**, and the
   join expires after 72 hours of inactivity.
7. **The share target is Android and Chrome.** iOS does not implement it.

---

# 15. The questions, with answers

**"Why not just use an LLM?"**
Three reasons in order. A verdict has to be the same every time, and a model
asked the same question twice may answer differently. It has to survive being
explained to the person who nearly paid, and "the model said so" does not. And
it has to run on their phone with the network off, because the message is
already on that phone and sending it somewhere is the thing they are afraid of.
There *is* a model in here — it just does not get the last word.

**"Isn't this just regex?"**
The rules are, and that is both their strength and their ceiling. Out of domain
they catch 8% of real spam. That is exactly why there is a calibrated linear
model that catches 90%, and why the two are fused with the model explicitly
subordinate. The rules give reasons, the model gives reach, and both are
measured separately so you can see which is carrying which case.

**"How do you know it works?"**
I measured it three times on messages I did not write, before using any of them
to change anything, and the first number was 52%. It is 80% on the last set.
Every number is reproducible from the repository.

**"What was the hardest part?"**
Keeping two implementations honest. The rules run in Python on the server and in
JavaScript on the device, generated from one source. A parity check runs 155
messages through both and compares scores, bands, rule ids, reason text,
normalised text, every highlighted quote and the model's probability to six
decimal places. Three real bugs were caught only by that check, and all three
were the same shape: Python and JavaScript disagreeing about what a character
is. An emoji is one character to Python and two to JavaScript, so a
quantifier spanned different amounts of text.

**"What broke that you did not expect?"**
A rule for "asks you to keep it from your family" fired on *"Never share this
with anyone"* in a genuine bank OTP message. Safety advice read as a scam
signal, the exact inverse of the intent. The fix was recognising that the tell is
being told not to **talk to** someone, not being told to keep a code to
yourself. It is the best example of why the false-positive half of the test set
matters as much as the other half.

**"What would you do next?"**
Collect forty real forwards and build a holdout that is genuinely frozen.
Everything else is a smaller gain than that one.
