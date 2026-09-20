"""The answer, as one chat message.

Telegram and WhatsApp differ in how a message arrives and how a reply is sent.
They do not differ in what the reply should say, so the words live here and
each channel keeps only its own plumbing.
"""
from __future__ import annotations

LIMIT = 4096


def _bullets(verdict: dict, limit: int = 4) -> str:
    lines = []
    for f in verdict["findings"][:limit]:
        quote = f["quotes"][0] if f["quotes"] else ""
        lines.append(f'• {f["name"]}' + (f' — "{quote}"' if quote else ""))
    extra = len(verdict["findings"]) - limit
    if extra > 0:
        lines.append(f"• and {extra} more")
    return "\n".join(lines)


def reply_for(verdict: dict | None, advice: dict | None, link: str | None,
              kind: str = "text", hunch: dict | None = None) -> str:
    """The whole answer as one WhatsApp message.

    No markdown beyond what WhatsApp renders, no links except the one that is
    useful, and the verdict on the first line, because on a phone the first
    line is often all that is read.
    """
    if kind != "text" or verdict is None:
        return ("I can only read text. Forward the message itself, or copy the "
                "words and send them to me, and I will tell you what is wrong "
                "with it and why.")

    # The model may raise concern and may never clear it. A headline of
    # "Nothing suspicious found" over a 90-out-of-100 reading is the one
    # failure that actually costs someone money, because the first line is all
    # many people read.
    head = verdict["label"]
    if not verdict["findings"] and hunch and hunch["p"] >= 0.8:
        head = "Nothing matched, but be careful"
    parts = [head]
    if verdict["findings"]:
        parts[0] += f"  ({verdict['score']} of {verdict['rules_checked']} checks fired)"
        parts.append("\nWhat is wrong with it:\n" + _bullets(verdict))
        if advice and advice.get("actions"):
            steps = "\n".join(f"{i}. {a}" for i, a in enumerate(advice["actions"], 1))
            parts.append("\nWhat to do now:\n" + steps)
        if advice and advice.get("forward"):
            parts.append("\nYou can send this back to whoever forwarded it:\n"
                         + advice["forward"])
    else:
        parts.append("\nNone of the checks fired. That is not a guarantee, it "
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
        parts.append(f"\nThe full breakdown: {link}")

    out = "\n".join(parts)
    return out[:4000] + "…" if len(out) > 4096 else out


