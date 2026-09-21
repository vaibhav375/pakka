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
from advice import CLAUSE, IMPERSONATION, JOB, MONEY, PROPERTY  # noqa: E402
from rules import BANDS, RULES  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "web" / "rules.generated.js"

rules = [
    {"id": r.id, "name": r.name, "why": r.why, "weight": r.weight, "re": r.pattern.pattern}
    for r in RULES
]
bands = [[t, k, l] for t, k, l in BANDS]

# the advice tables travel with the rules, so the on-device answer can say what
# to do next without a round trip and without a second copy to keep in step
advice = {
    "clause": CLAUSE,
    "money": sorted(MONEY),
    "job": sorted(JOB),
    "impersonation": sorted(IMPERSONATION),
    "property": sorted(PROPERTY),
}

OUT.write_text(f"""/* Generated from api/rules.py by tools/build_rules_js.py — do not edit.
   Running the check here means the message never leaves the device unless the
   person presses Share. */
window.PAKKA_RULES = {json.dumps(rules, indent=2, ensure_ascii=False)};
window.PAKKA_ADVICE = {json.dumps(advice, indent=2, ensure_ascii=False)};
window.PAKKA_BANDS = {json.dumps(bands)};

/* The same normalisation as normalise() in api/rules.py. Change one, change
   both: tools/check_parity.py fails the build if they disagree. */
const PAKKA_LEET = {{ '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't' }};
const pakkaAlpha = (c) => !!c && /^[A-Za-z]$/.test(c);
const pakkaAlnum = (c) => !!c && /^[A-Za-z0-9]$/.test(c);

window.pakkaNormalise = function (text) {{
  const chars = [], idx = [], ends = [];
  let at = 0;
  for (const ch of text) {{                       /* by code point, as Python does */
    for (const c of ch.normalize('NFD')) {{
      if (c >= '\u0300' && c <= '\u036f') continue;   /* a combining accent */
      /* an emoji is two code units here and one character in Python, so it
         becomes one placeholder and every quantifier counts the same */
      chars.push(c.length > 1 ? '\ufffd' : c);
      idx.push(at); ends.push(at + ch.length);
    }}
    at += ch.length;                              /* but index by code unit, for slice */
  }}
  for (let j = 0; j < chars.length; j++) {{
    if (PAKKA_LEET[chars[j]] !== undefined) {{
      const prev = j ? chars[j - 1] : '', next = chars[j + 1] || '';
      if (pakkaAlpha(prev) || pakkaAlpha(next)) chars[j] = PAKKA_LEET[chars[j]];
    }}
  }}
  const n = chars.length;
  const lone = (q) => pakkaAlpha(chars[q])
    && (q === 0 || !pakkaAlnum(chars[q - 1]))
    && (q + 1 >= n || !pakkaAlnum(chars[q + 1]));
  let out = '', oidx = [], oend = [], i = 0;
  while (i < n) {{
    if (lone(i)) {{
      const run = [i];
      let j = i;
      const sep = i + 1 < n ? chars[i + 1] : '';
      while (j + 2 < n && chars[j + 1] === sep && ' .-'.indexOf(sep) !== -1 && lone(j + 2)) {{
        run.push(j + 2); j += 2;
      }}
      if (run.length >= 3) {{
        for (const k of run) {{ out += chars[k]; oidx.push(idx[k]); oend.push(ends[k]); }}
        i = j + 1;
        continue;
      }}
    }}
    out += chars[i]; oidx.push(idx[i]); oend.push(ends[i]); i += 1;
  }}
  return [out, oidx, oend];
}};

/* grow a span out to word edges, so a highlight never cuts "expired" into
   "expire" and a stranded "d" */
const pakkaWord = (c) => !!c && /[A-Za-z0-9_\u0900-\u0963\u0966-\u097F]/.test(c);
function pakkaWholeWords(text, a, b) {{
  while (a > 0 && pakkaWord(text[a - 1]) && pakkaWord(text[a])) a -= 1;
  while (b < text.length && pakkaWord(text[b]) && pakkaWord(text[b - 1])) b += 1;
  return [a, b];
}}

window.pakkaEvaluate = function (text) {{
  const [norm, idx, ends] = window.pakkaNormalise(text);
  const findings = [];
  let deferred = null;
  for (const r of window.PAKKA_RULES) {{
    /* the one check that is about the characters rather than the words, so it
       is answered by web/urls.js instead of by a pattern */
    if (r.id === 'LOOKALIKE_URL') {{
      /* held back and pushed after the loop, because api/rules.py appends it
         last and equal weights would otherwise tie in a different order */
      const hits = (window.pakkaUrls ? window.pakkaUrls(text) : []);
      if (hits.length) {{
        const why = [...new Set(hits.map(([, reason]) => reason))].join('; ');
        const sp = [...new Set(hits.map(([, , a, b]) => a + ':' + b))]
          .map((k) => k.split(':').map(Number)).sort((x, y) => x[0] - y[0]);
        deferred = {{ id: r.id, name: r.name, why, weight: r.weight,
                     spans: sp, quotes: sp.map(([a, b]) => text.slice(a, b)) }};
      }}
      continue;
    }}
    const re = new RegExp(r.re, 'gi');
    const spans = [];
    let m;
    while ((m = re.exec(norm)) !== null) {{
      if (m[0] === '') {{ re.lastIndex++; continue; }}
      const a = m.index, b = m.index + m[0].length;
      if (idx.length) spans.push(pakkaWholeWords(text, idx[a], ends[Math.min(b, ends.length) - 1]));
    }}
    if (spans.length) findings.push({{
      id: r.id, name: r.name, why: r.why, weight: r.weight,
      spans, quotes: spans.map(([a, b]) => text.slice(a, b)),
    }});
  }}
  if (deferred) findings.push(deferred);
  const score = findings.reduce((s, f) => s + f.weight, 0);
  const [, band, label] = window.PAKKA_BANDS.find(([t]) => score >= t);
  findings.sort((a, b) => b.weight - a.weight);
  return {{ text, score, band, label, findings, rules_checked: window.PAKKA_RULES.length }};
}};
""", encoding="utf-8")
print(f"  wrote {OUT.relative_to(OUT.parent.parent)} — {len(rules)} rules")
