"""Prove the browser rules and the server rules agree.

A generated file is only trustworthy if something checks the generation. This
runs the same messages through Python and through Node and fails if the two
disagree about which rules fired or what the score was.

    python3 tools/check_parity.py
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))
from rules import evaluate, normalise  # noqa: E402
sys.path.insert(0, str(ROOT / "api"))
from test_rules import CASES  # noqa: E402
sys.path.insert(0, str(ROOT / "tools"))
from eval_set import FRAUD, LEGIT  # noqa: E402

texts = [t for _, t, _ in CASES]
js = f"""
globalThis.window = globalThis;
{(ROOT / 'web' / 'rules.generated.js').read_text()}
const out = {json.dumps(texts)}.map((t) => {{
  const r = window.pakkaEvaluate(t);
  return {{ score: r.score, band: r.band, ids: r.findings.map((f) => f.id).sort() }};
}});
console.log(JSON.stringify(out));
"""
proc = subprocess.run(["node", "-e", js], capture_output=True, text=True)
if proc.returncode:
    print(proc.stderr.strip()); raise SystemExit(1)
from_js = json.loads(proc.stdout)

bad = 0
for (name, text, _), j in zip(CASES, from_js):
    p = evaluate(text)
    mine = {"score": p["score"], "band": p["band"], "ids": sorted(f["id"] for f in p["findings"])}
    ok = mine == j
    bad += not ok
    print(f"  {'match' if ok else 'DIFFER'}  {name:<34} score={mine['score']}")
    if not ok:
        print(f"        python: {mine}\n        node:   {j}")

# The named cases above check the rules. This checks the whole labelled corpus,
# and compares the normalised text and every highlighted quote as well, because
# the highlighting is what the person actually reads.
corpus = [t for _, t in FRAUD] + [t for _, t in LEGIT]
js = f"""
globalThis.window = globalThis;
{(ROOT / 'web' / 'rules.generated.js').read_text()}
const out = {json.dumps(corpus, ensure_ascii=False)}.map((t) => {{
  const r = window.pakkaEvaluate(t);
  return {{ score: r.score, band: r.band, ids: r.findings.map((f) => f.id).sort(),
           norm: window.pakkaNormalise(t)[0],
           quotes: r.findings.map((f) => f.quotes.join('|')) }};
}});
console.log(JSON.stringify(out));
"""
proc = subprocess.run(["node", "-e", js], capture_output=True, text=True)
if proc.returncode:
    print(proc.stderr.strip()); raise SystemExit(1)
drift = 0
for text, j in zip(corpus, json.loads(proc.stdout)):
    p = evaluate(text)
    mine = {"score": p["score"], "band": p["band"],
            "ids": sorted(f["id"] for f in p["findings"]),
            "norm": normalise(text)[0],
            "quotes": ["|".join(f["quotes"]) for f in p["findings"]]}
    for key in ("score", "band", "ids", "norm", "quotes"):
        if mine[key] != j[key]:
            drift += 1
            print(f"  DIFFER {key}: {text[:46]}")
            print(f"        python: {mine[key]!r}\n        node:   {j[key]!r}")
            break
print(f"  corpus: {len(corpus) - drift}/{len(corpus)} identical, "
      f"including normalised text and every quote")

bad += drift
print(f"\n  {'python and javascript agree on every case' if not bad else f'{bad} case(s) disagree'}")
raise SystemExit(1 if bad else 0)
