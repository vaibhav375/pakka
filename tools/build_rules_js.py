"""Generate the browser copy of the rules from the Python ones.

There is exactly one place a rule is written down: api/rules.py. This script
translates that table into JavaScript so the check can also run on the device,
which keeps the message private until someone chooses to share it. Because the
JS is generated rather than hand-kept, the two copies cannot drift.

    python3 tools/build_rules_js.py
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "api"))
from rules import BANDS, RULES  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "web" / "rules.generated.js"

rules = [
    {"id": r.id, "name": r.name, "why": r.why, "weight": r.weight, "re": r.pattern.pattern}
    for r in RULES
]
bands = [[t, k, l] for t, k, l in BANDS]

OUT.write_text(f"""/* Generated from api/rules.py by tools/build_rules_js.py — do not edit.
   Running the check here means the message never leaves the device unless the
   person presses Share. */
window.PAKKA_RULES = {json.dumps(rules, indent=2, ensure_ascii=False)};
window.PAKKA_BANDS = {json.dumps(bands)};

window.pakkaEvaluate = function (text) {{
  const findings = [];
  for (const r of window.PAKKA_RULES) {{
    const re = new RegExp(r.re, 'gi');
    const spans = [];
    let m;
    while ((m = re.exec(text)) !== null) {{
      if (m[0] === '') {{ re.lastIndex++; continue; }}
      spans.push([m.index, m.index + m[0].length]);
    }}
    if (spans.length) findings.push({{
      id: r.id, name: r.name, why: r.why, weight: r.weight,
      spans, quotes: spans.map(([a, b]) => text.slice(a, b)),
    }});
  }}
  const score = findings.reduce((s, f) => s + f.weight, 0);
  const [, band, label] = window.PAKKA_BANDS.find(([t]) => score >= t);
  findings.sort((a, b) => b.weight - a.weight);
  return {{ text, score, band, label, findings, rules_checked: window.PAKKA_RULES.length }};
}};
""", encoding="utf-8")
print(f"  wrote {OUT.relative_to(OUT.parent.parent)} — {len(rules)} rules")
