"""The answer, as one chat message.

Telegram and WhatsApp differ in how a message arrives and how a reply is sent.
They do not differ in what the reply should say, so the words live here and
each channel keeps only its own plumbing.
"""
from __future__ import annotations

import hindi

LIMIT = 4096


def devanagari(text: str) -> bool:
    """Answer in the language the message arrived in.

    Somebody who forwards a Hindi scam is not helped by an English
    explanation of it, and asking them to pick a language first is one more
    step at the worst possible moment.
    """
    return any("\u0900" <= c <= "\u097f" for c in text or "")


def _bullets(verdict: dict, limit: int = 4, hi: bool = False) -> str:
    lines = []
    for f in verdict["findings"][:limit]:
        quote = f["quotes"][0] if f["quotes"] else ""
        name = hindi.RULES.get(f["id"], (f["name"],))[0] if hi else f["name"]
        lines.append(f"• {name}" + (f' — "{quote}"' if quote else ""))
    extra = len(verdict["findings"]) - limit
    if extra > 0:
        lines.append(f"• और {extra} और" if hi else f"• and {extra} more")
    return "\n".join(lines)


def reply_for(verdict: dict | None, advice: dict | None, link: str | None,
              kind: str = "text", hunch: dict | None = None,
              lang: str = "en") -> str:
    """The whole answer as one WhatsApp message.

    No markdown beyond what WhatsApp renders, no links except the one that is
    useful, and the verdict on the first line, because on a phone the first
    line is often all that is read.
    """
    hi = lang == "hi"
    if kind != "text" or verdict is None:
        if hi:
            return ("मैं सिर्फ़ लिखा हुआ पढ़ सकता हूँ। संदेश खुद आगे भेजिए, या उसके शब्द "
                    "कॉपी करके भेजिए, और मैं बताऊँगा कि उसमें क्या गलत है और क्यों।")
        return ("I can only read text. Forward the message itself, or copy the "
                "words and send them to me, and I will tell you what is wrong "
                "with it and why.")

    # The model may raise concern and may never clear it. A headline of
    # "Nothing suspicious found" over a 90-out-of-100 reading is the one
    # failure that actually costs someone money, because the first line is all
    # many people read.
    head = hindi.BANDS.get(verdict["band"], verdict["label"]) if hi else verdict["label"]
    if not verdict["findings"] and hunch and hunch["p"] >= 0.8:
        head = "कुछ नहीं मिला, पर सावधान रहिए" if hi else "Nothing matched, but be careful"
    parts = [head]
    if verdict["findings"]:
        parts[0] += (f"  ({verdict['score']} / {verdict['rules_checked']} जाँचें चलीं)" if hi
                     else f"  ({verdict['score']} of {verdict['rules_checked']} checks fired)")
        parts.append(("\nइसमें क्या गलत है:\n" if hi else "\nWhat is wrong with it:\n")
                     + _bullets(verdict, hi=hi))
        if advice and advice.get("actions"):
            steps = "\n".join(f"{i}. {a}" for i, a in enumerate(advice["actions"], 1))
            parts.append(("\nअब क्या कीजिए:\n" if hi else "\nWhat to do now:\n") + steps)
        if advice and advice.get("forward"):
            parts.append(("\nजिसने भेजा है उसे यह वापस भेज सकते हैं:\n" if hi
                          else "\nYou can send this back to whoever forwarded it:\n")
                         + advice["forward"])
    else:
        parts.append("\nकोई जाँच नहीं चली। यह गारंटी नहीं है, इसका मतलब सिर्फ़ यह है कि "
                     "इसमें वे तरीके नहीं हैं जो मैं जानता हूँ। फिर भी कुछ गलत लगे तो उस पर "
                     "भरोसा कीजिए।" if hi else
                     "\nNone of the checks fired. That is not a guarantee, it "
                     "means this message does not use any of the patterns I "
                     "know about. If something still feels wrong, trust that.")

    # The rules decide. This is shown underneath and never instead, because it
    # is the part that can be wrong. It earns its place when no rule fires and
    # the message still reads like fraud, which is where rules are blind.
    if hunch is not None:
        pct = round(hunch["p"] * 100)
        if not verdict["findings"] and hunch["p"] >= 0.75:
            parts.append(f"\nNo rule fired, but this still reads like a scam to the "
                         f"model, at {pct} out of 100. Treat that as a reason to be "
                         f"careful rather than proof.")
        elif verdict["findings"] and hunch["p"] >= 0.6:
            parts.append(f"\nThe model agrees with the rules independently, at "
                         f"{pct} out of 100.")
    if link:
        parts.append(f"\nपूरा ब्यौरा: {link}" if hi else f"\nThe full breakdown: {link}")

    out = "\n".join(parts)
    return out[:4000] + "…" if len(out) > 4096 else out


