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
import model as pymodel  # noqa: E402
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

# --- and the model, which is a second generated artifact with the same risk
if (ROOT / "web" / "model.generated.js").exists():
    js = f"""
globalThis.window = globalThis;
{(ROOT / 'web' / 'rules.generated.js').read_text()}
{(ROOT / 'web' / 'model.generated.js').read_text()}
{(ROOT / 'web' / 'model.js').read_text()}
const out = {json.dumps(corpus, ensure_ascii=False)}.map((t) => {{
  const r = window.pakkaModel(t);
  /* the phrases, not the offsets: Python counts code points and JavaScript
     counts code units, so after an emoji the two legitimately differ by one
     while pointing at the same characters */
  return {{ p: Math.round(r.p * 1e6) / 1e6,
           says: window.pakkaModelSpans(t, r.heat).map(([a, b]) => t.slice(a, b)) }};
}});
console.log(JSON.stringify(out));
"""
    proc = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    if proc.returncode:
        print(proc.stderr.strip()); raise SystemExit(1)
    mdrift = 0
    for text, j in zip(corpus, json.loads(proc.stdout)):
        mine = pymodel.score(text)
        if abs(mine["p"] - j["p"]) > 1e-6:
            mdrift += 1
            print(f"  DIFFER p: {text[:44]}  python {mine['p']:.6f}  node {j['p']:.6f}")
        elif [text[a:b] for a, b in mine["spans"]] != j["says"]:
            mdrift += 1
            print(f"  DIFFER phrases: {text[:44]}"
                  f"\n        python: {[text[a:b] for a, b in mine['spans']]}"
                  f"\n        node:   {j['says']}")
    print(f"  model:  {len(corpus) - mdrift}/{len(corpus)} identical probabilities "
          f"and highlighted phrases")
    bad += mdrift

bad += drift
print(f"\n  {'python and javascript agree on every case' if not bad else f'{bad} case(s) disagree'}")
raise SystemExit(1 if bad else 0)
