"""Audit the rulebook against a corpus, and say which rules are not earning it.

    python3 tools/audit_rules.py

Two questions a rulebook cannot answer about itself:

  Which shapes of fraud does it not cover?   -> the rules to write next
  Which rules never fire on anything?        -> the rules to delete

The corpus used here is CloveAI/india-spam-sms, which is templated rather than
collected: 5,951 spam rows share 41 distinct skeletons. That makes it useless
for training or for any claim about accuracy, and genuinely useful for this,
because 41 skeletons is an inventory of the shapes Indian SMS fraud takes, and
an inventory is exactly what you audit coverage against. Every skeleton is
counted once, so a template repeated 353 times does not vote 353 times.
"""
from __future__ import annotations

import collections
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api")); sys.path.insert(0, str(ROOT / "tools"))
from rules import evaluate, RULES  # noqa: E402
from eval_set import FRAUD, LEGIT  # noqa: E402

PARQUET = ROOT / "data" / "india-spam-sms.parquet"
URL = ("https://huggingface.co/datasets/CloveAI/india-spam-sms/"
       "resolve/main/data/train-00000-of-00001.parquet")


def skeleton(text: str, words: int = 6) -> str:
    t = re.sub(r"\d+", "#", text)
    t = re.sub(r"https?://\S+", "<link>", t)
    return " ".join(re.sub(r"\s+", " ", t).strip().lower().split()[:words])


def load() -> list[tuple[str, int]]:
    if not PARQUET.exists():
        PARQUET.parent.mkdir(exist_ok=True)
        print(f"  downloading {URL}")
        subprocess.run(["curl", "-sSL", "-o", str(PARQUET), URL], check=True)
    sys.path.insert(0, str(ROOT / ".venv" / "lib" / "python3.12" / "site-packages"))
    import pandas as pd
    d = pd.read_parquet(PARQUET)
    seen, out = set(), []
    for text, label in zip(d.text, d.label):
        k = (skeleton(text), int(label))
        if k in seen:
            continue
        seen.add(k)
        out.append((str(text), int(label)))
    return out


def main() -> int:
    rows = load()
    spam = [t for t, l in rows if l == 1]
    ham = [t for t, l in rows if l == 0]
    print(f"\n  {len(rows)} distinct shapes: {len(spam)} fraud, {len(ham)} ordinary\n")

    missed = [t for t in spam if evaluate(t)["score"] == 0]
    fp = [(evaluate(t)["score"], t) for t in ham if evaluate(t)["score"] >= 2]
    print(f"  fraud shapes covered      {len(spam) - len(missed)}/{len(spam)}")
    print(f"  ordinary shapes flagged   {len(fp)}/{len(ham)}")

    if missed:
        print(f"\n  SHAPES NO RULE COVERS ({len(missed)}) - these are the rules to write next")
        for t in missed[:20]:
            print(f"    {t[:96]}")
    if fp:
        print(f"\n  ORDINARY SHAPES FLAGGED ({len(fp)}) - these are the rules to narrow")
        for sc, t in sorted(fp, reverse=True)[:15]:
            ids = ",".join(f["id"] for f in evaluate(t)["findings"])
            print(f"    {sc}  {ids[:34]:<36}{t[:60]}")

    # which rules fire on anything at all, here or in our own corpus
    fires = collections.Counter()
    everything = spam + ham + [t for _, t in FRAUD] + [t for _, t in LEGIT]
    for t in everything:
        for f in evaluate(t)["findings"]:
            fires[f["id"]] += 1
    dead = [r.id for r in RULES if not fires[r.id]]
    print(f"\n  rule usage across {len(everything)} messages")
    for r in sorted(RULES, key=lambda r: fires[r.id], reverse=True):
        bar = "#" * min(40, fires[r.id])
        print(f"    {fires[r.id]:>4}  {r.id:<18} {bar}")
    if dead:
        print(f"\n  NEVER FIRES ({len(dead)}) - either untested or not worth keeping")
        for d in dead:
            print(f"    {d}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
