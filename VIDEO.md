# Demo video — 2:50, shot by shot

Unlisted YouTube. Screen recording with voice over it. One take is fine.
Two browser windows open before you start: the site, and the AWS console with
three tabs already loaded — **DynamoDB → Tables → pakka-scans → Explore items**,
**Lambda → pakka**, **CloudWatch → Log groups → /aws/lambda/pakka**.

---

**0:00–0:20 — the problem, on the hero**

> My mother forwards me messages to check. So do my juniors. Every time, the
> answer has the same shape: this line here is the problem, and this is why.
> They usually already felt something was off — what they didn't have was the
> confidence to say no.

Scroll slowly through the hero while you say it. Don't touch anything yet.

**0:20–1:05 — paste a scam, get the verdict**

Click the **KYC expired** example chip. Hit **Check it**.

> Twenty-one rules, plain Python. It names what fired, quotes the exact words, and
> scores it. Nothing here is a model guessing — the same message always gives
> the same verdict, and every line of it can be explained.

Point at the highlighted phrases as the gauge fills. Hover one rule card so the
others dim and its phrases light up in the message.

> What most tools stop at is "this is a scam." That isn't the useful part.

Scroll to **What to do now** and **the reply**.

> Report at cybercrime dot gov dot in, or 1930 — inside the first hour, while
> the money can still be frozen. And this is a reply you can send straight back
> to whoever forwarded it.

**1:05–1:25 — the thing that's harder than catching scams**

Click the **placement cell** example. Check it.

> A real message from a college placement cell. It has to come back clean, or
> the tool cries wolf and people stop listening. That message is a test case in
> the repo.

**1:25–1:45 — offline**

Open DevTools → Network → **Offline**. Run a scan.

> The rules are generated from the Python into JavaScript, so the check runs on
> the device. No message leaves your phone unless you ask for a link. A build
> step asserts the two agree on every case.

**1:45–2:30 — AWS, on screen**

Back online. Click **Copy link**, open it in a new tab so the shared verdict loads.

> That link is the only thing that touches the cloud.

Switch to the AWS tabs, one at a time, roughly ten seconds each:

- **DynamoDB → Explore items** — scroll the rows. "Every scan, with a 30-day TTL. Provisioned at one read and one write unit, inside the always-free tier."
- **Lambda → pakka** — show the Function URL. "One function behind a Function URL. No API Gateway — one public endpoint with CORS was all this needed, and it costs nothing extra."
- **CloudWatch → log group** — open tonight's stream, scroll to a real traceback. "And these are tonight's mistakes. Every 502 I hit named itself in here."

**2:30–2:50 — close**

Back to the site, on the constellation.

> Twenty-one rules, one Lambda, one table. It works with the network off, it
> explains itself, and it gives you the words to say no.

---

**Delivery**

- Point at things. It's what makes it sound like explaining rather than reciting.
- Three lines worth slowing down for: *"what they didn't have was the confidence
  to say no"*, *"that isn't the useful part"*, *"it has to come back clean, or
  the tool cries wolf."*
- Pause after *"these are tonight's mistakes."*
- Small stumbles sound like a person. Only restart if you lose the thread.
