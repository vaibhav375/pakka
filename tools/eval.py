"""Measure the rules against the labelled set.

    python3 tools/eval.py           summary
    python3 tools/eval.py -v        plus every miss and every false positive

A fraud message counts as caught at score >= 1, and as caught clearly at
score >= 2, which is the point the page stops saying "one flag" and starts
saying "be careful". A legit message scoring >= 2 is a real false positive.
One scoring exactly 1 is noise: visible, but the gentlest band there is.
"""
import sys, pathlib, collections
ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "api")); sys.path.insert(0, str(ROOT / "tools"))
from rules import evaluate, RULES
from eval_set import FRAUD, LEGIT

VERBOSE = "-v" in sys.argv

def main() -> int:
    fam = collections.defaultdict(lambda: [0, 0])
    missed, weak, fps, noise = [], [], [], []
    for family, text in FRAUD:
        v = evaluate(text)
        fam[family][1] += 1
        if v["score"] >= 1:
            fam[family][0] += 1
        else:
            missed.append((family, text))
        if 1 <= v["score"] < 2:
            weak.append((v["score"], text))
    for family, text in LEGIT:
        v = evaluate(text)
        if v["score"] >= 2:
            fps.append((v, text))
        elif v["score"] == 1:
            noise.append((v, text))

    caught = len(FRAUD) - len(missed)
    clear = caught - len(weak)
    print(f"\n  {len(RULES)} rules, {len(FRAUD)} fraud, {len(LEGIT)} legit\n")
    print(f"  caught at all            {caught}/{len(FRAUD)}   {caught/len(FRAUD):6.1%}")
    print(f"  caught clearly (>=2)     {clear}/{len(FRAUD)}   {clear/len(FRAUD):6.1%}")
    print(f"  false positives (>=2)    {len(fps)}/{len(LEGIT)}   {len(fps)/len(LEGIT):6.1%}")
    print(f"  noise (exactly 1)        {len(noise)}/{len(LEGIT)}   {len(noise)/len(LEGIT):6.1%}")

    print("\n  by family")
    for f in sorted(fam, key=lambda k: (fam[k][0] / fam[k][1], k)):
        hit, tot = fam[f]
        bar = "#" * hit + "." * (tot - hit)
        print(f"    {f:<14}{hit}/{tot}  {bar}")

    bands = collections.Counter(evaluate(t)["band"] for _, t in FRAUD)
    print("\n  where the fraud lands")
    for b in ["almost_certainly", "likely", "careful", "one_flag", "clear"]:
        print(f"    {b:<18}{bands.get(b, 0)}")

    if missed:
        print(f"\n  MISSED ({len(missed)})")
        for f, t in missed:
            print(f"    [{f}] {t[:88]}")
    if fps:
        print(f"\n  FALSE POSITIVES ({len(fps)})")
        for v, t in fps:
            print(f"    {v['score']}  {','.join(x['id'] for x in v['findings'])[:38]:<40}{t[:60]}")
    if VERBOSE and noise:
        print(f"\n  noise ({len(noise)})")
        for v, t in noise:
            print(f"    1  {','.join(x['id'] for x in v['findings'])[:38]:<40}{t[:60]}")
    if VERBOSE and weak:
        print(f"\n  caught but only just ({len(weak)})")
        for sc, t in weak:
            print(f"    {sc}  {t[:88]}")
    print()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
