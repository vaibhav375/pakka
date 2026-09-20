"""Things about a web address that a pattern cannot see.

A rule can look for the word "sbi". It cannot tell you that the "а" in
"аmazon.in" is Cyrillic, that "xn--80ak6aa92e.com" renders as something else
entirely in the address bar, or that a hostname made of digits is not a
hostname anyone chose. Those are properties of the characters and the
structure, not of any phrase, so they live here and the rules call in.

Every check returns a reason in plain words, because a finding nobody can
explain is worth nothing.
"""
from __future__ import annotations

import re
import unicodedata

URL = re.compile(r"\b(?:https?://|www\.)[^\s<>\"']+", re.I)
HOST = re.compile(r"^(?:https?://)?([^/?#\s]+)", re.I)
IPV4 = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?$")

# The scripts a single word can be written in without anything being wrong.
# A word mixing two of them is a word pretending to be another word.
def _script(ch: str) -> str:
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return "OTHER"
    for s in ("LATIN", "CYRILLIC", "GREEK", "ARMENIAN", "DEVANAGARI"):
        if name.startswith(s):
            return s
    return "OTHER"


def hosts(text: str) -> list[str]:
    out = []
    for m in URL.finditer(text):
        h = HOST.match(m.group(0))
        if h:
            out.append(h.group(1).rstrip(".").lower())
    return out


def suspicious(text: str) -> list[tuple[str, str, int, int]]:
    """Every problem found, as (host, reason, start, end) in the text."""
    found = []
    for m in URL.finditer(text):
        h = HOST.match(m.group(0))
        if not h:
            continue
        host = h.group(1).rstrip(".").lower()
        for reason in _problems(host):
            found.append((host, reason, m.start(), m.end()))
    return found


def _problems(host: str) -> list[str]:
    out = []
    label_parts = host.split(":")[0].split(".")

    # A word written in two alphabets at once. This is how a lookalike domain
    # is built: one Latin letter swapped for a Cyrillic one that renders the
    # same, and the address reads correctly to a human and resolves somewhere
    # else entirely.
    for part in label_parts:
        scripts = {_script(c) for c in part if c.isalpha()}
        scripts.discard("OTHER")
        if len(scripts) > 1:
            out.append(f"the word \"{part}\" is written in two alphabets at once "
                       f"({', '.join(sorted(s.title() for s in scripts))}), which is "
                       f"how an address is made to look like a different one")
            break

    # Punycode: what the address bar shows and what the address is are not the
    # same string.
    if any(p.startswith("xn--") for p in label_parts):
        try:
            shown = host.encode("ascii").decode("idna")
        except Exception:
            shown = host
        out.append(f"the address is punycode: it is stored as \"{host}\" and displayed "
                   f"as \"{shown}\", which is not the same thing")

    # A bare IP address is not a company.
    if IPV4.match(host):
        out.append("it is a bare IP address, not a name anyone registered")

    # Digits inside a brand word, the poor version of the same trick.
    for part in label_parts[:-1]:
        letters = sum(c.isalpha() for c in part)
        digits = sum(c.isdigit() for c in part)
        if letters >= 4 and 0 < digits <= 2 and not part.isdigit():
            inner = re.search(r"[a-z]\d+[a-z]", part)
            if inner:
                out.append(f"\"{part}\" has digits standing in for letters inside a word")
                break
    return out
