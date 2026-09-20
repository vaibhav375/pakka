"""Check messages against the rules without opening a browser.

    python3 tools/try.py "paste a message here"
    python3 tools/try.py < messages.txt      (one message per line)

Prints the score, the band, and every rule that fired with the exact words
that set it off. Use it to find gaps: anything suspicious that comes back
clean is a missing rule, not a tuning problem.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "api"))
from rules import evaluate
from advice import build

def show(text: str) -> None:
    text = text.strip()
    if not text:
        return
    v = evaluate(text)
    print(f"\n  {text[:100]}")
    print(f"  score {v['score']}  {v['label']}")
    for f in v["findings"]:
        print(f"    +{f['weight']}  {f['id']:<18} {'; '.join(f['quotes'])[:70]}")
    if not v["findings"]:
        print("    nothing fired")

def main() -> None:
    args = [a for a in sys.argv[1:]]
    if args:
        for a in args:
            show(a)
    else:
        for line in sys.stdin:
            show(line)
    print()

if __name__ == "__main__":
    main()
