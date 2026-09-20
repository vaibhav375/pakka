#!/bin/sh
# The catalogue the page shows is generated from the rules the API runs, so the
# two cannot drift apart. Re-run after editing api/rules.py.
python3 - <<'PY'
import sys, json; sys.path.insert(0, 'api')
from rules import RULES
json.dump([{"id": r.id, "name": r.name, "why": r.why, "weight": r.weight} for r in RULES],
          open('web/rules.json', 'w'), indent=1)
print(f"web/rules.json regenerated ({len(RULES)} rules)")
PY
