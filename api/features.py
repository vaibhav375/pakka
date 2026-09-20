"""Turning a message into numbers, identically in Python and in JavaScript.

Every choice here exists twice: once in this file and once in web/model.js.
tools/check_parity.py fails the build if they ever drift, the same way it does
for the rules.

Character n-grams rather than words, because scam messages are full of
misspellings, spacing tricks and Hinglish, and "kyc" inside "kycupdate" carries
the same signal as the word on its own. The text is normalised first by the
same function the rules use, so the model sees "0TP" and "O T P" as "otp" too.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from rules import normalise  # noqa: E402

DIM = 1 << 14          # 16384 buckets
NGRAMS = (3, 4, 5)
MASK = 0xFFFFFFFF


def fnv1a(s: str) -> int:
    """32-bit FNV-1a over UTF-16 code units.

    normalise() has already replaced everything outside the basic plane with a
    placeholder, so a Python code point and a JavaScript code unit are the same
    thing by the time we get here, and both languages hash to the same bucket.
    """
    h = 2166136261
    for ch in s:
        h = ((h ^ ord(ch)) * 16777619) & MASK
    return h


def buckets(text: str) -> list[int]:
    """The hashed n-gram indices present in a message, deduplicated."""
    flat = normalise(text)[0].lower()
    seen = set()
    for n in NGRAMS:
        for i in range(len(flat) - n + 1):
            seen.add(fnv1a(flat[i:i + n]) % DIM)
    return sorted(seen)


def spans_for(text: str) -> list[tuple[int, int, int]]:
    """Every n-gram as (bucket, start, end) in the ORIGINAL text.

    This is what lets a linear model point at the words it reacted to: each
    n-gram carries a weight, and the weights land back on the characters they
    came from.
    """
    flat, idx = normalise(text)
    low = flat.lower()
    out = []
    for n in NGRAMS:
        for i in range(len(low) - n + 1):
            if idx:
                out.append((fnv1a(low[i:i + n]) % DIM,
                            idx[i], idx[min(i + n, len(idx)) - 1] + 1))
    return out
