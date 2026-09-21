"""Score the frozen holdout. Run it, report it, do not tune against it.

    python3 tools/run_holdout.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api")); sys.path.insert(0, str(ROOT / "tools"))
from rules import evaluate  # noqa: E402
import model  # noqa: E402
from holdout import FRAUD, SOURCES  # noqa: E402


def main() -> int:
    rows = []
    for src, text in FRAUD:
        v = evaluate(text)
        m = model.score(text) or {"p": 0.0}
        rows.append((src, text, v, m["p"]))

    n = len(rows)
    rules_any = sum(1 for _, _, v, _ in rows if v["score"] >= 1)
    rules_clear = sum(1 for _, _, v, _ in rows if v["score"] >= 2)
    model_hit = sum(1 for _, _, _, p in rows if p >= 0.6)
    either = sum(1 for _, _, v, p in rows if v["score"] >= 2 or p >= 0.75)

    print(f"\n  {n} real messages, quoted from {len(SOURCES)} published sources,")
    print("  none of which were used to write a rule or train the model.\n")
    print(f"  rules fire at all          {rules_any}/{n}   {rules_any/n:6.1%}")
    print(f"  rules reach 'be careful'   {rules_clear}/{n}   {rules_clear/n:6.1%}")
    print(f"  model alone (p >= 0.6)     {model_hit}/{n}   {model_hit/n:6.1%}")
    print(f"  what the page would warn   {either}/{n}   {either/n:6.1%}")

    missed = [(s, t, v, p) for s, t, v, p in rows if v["score"] < 2 and p < 0.75]
    if missed:
        print(f"\n  WOULD NOT HAVE WARNED ({len(missed)})")
        for s, t, v, p in missed:
            print(f"    rules {v['score']}  model {p:.2f}  [{s}]  {t[:70]}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
