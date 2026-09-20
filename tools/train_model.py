"""Train the linear model that sits beside the rules, and measure it honestly.

    python3 tools/train_model.py

Why a linear model and not something bigger: the whole claim of this project is
that every verdict can be explained. A linear model's output IS the sum of its
per-feature contributions, so the weights that pushed a message towards "scam"
can be pointed at in the text, the same way a rule is. It also runs as a dot
product, which means it works offline on the device with no runtime dependency
at all. The only thing numpy is used for here is the training, and training
happens on a laptop, not on a phone.

The rules keep perfect precision on what they describe and have no opinion on
anything else. The model has an opinion about everything and is wrong more
often. They are better together than either is alone.
"""
from __future__ import annotations

import json
import pathlib
import random
import sys
import urllib.request

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "api"))
from features import DIM, NGRAMS, buckets  # noqa: E402
from eval_set import FRAUD, LEGIT  # noqa: E402

UCI_URL = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
UCI_PATH = ROOT / "data" / "sms.tsv"
OUT = ROOT / "web" / "model.generated.js"
API_OUT = ROOT / "api" / "model.json"
SEED = 20260921
LOCAL_WEIGHT = 12.0      # the Indian corpus is 2% of the rows and all of the domain
PRUNE = 0.02             # weights smaller than this are noise and bytes


def load_uci() -> list[tuple[str, int]]:
    """The UCI SMS Spam Collection: 5,574 real SMS, 747 of them spam.

    It is British SMS spam from 2012, so it teaches the model "free", "win",
    "claim" and "txt" and teaches it nothing whatsoever about KYC, UPI, APK
    sideloading or AnyDesk. That is exactly why every number this script
    reports is measured on the Indian set instead.
    """
    if not UCI_PATH.exists():
        UCI_PATH.parent.mkdir(exist_ok=True)
        print(f"  downloading {UCI_URL}")
        try:
            urllib.request.urlretrieve(UCI_URL, UCI_PATH)
        except Exception as exc:
            # a python.org install on macOS often ships without CA certificates,
            # and curl is right there
            print(f"    urllib could not fetch it ({type(exc).__name__}), trying curl")
            import subprocess
            subprocess.run(["curl", "-sSL", "-o", str(UCI_PATH), UCI_URL], check=True)
    rows = []
    for line in UCI_PATH.read_text(encoding="utf-8", errors="replace").splitlines():
        if "\t" not in line:
            continue
        label, text = line.split("\t", 1)
        rows.append((text, 1 if label.strip() == "spam" else 0))
    return rows


def load_local() -> list[tuple[str, int]]:
    return [(t, 1) for _, t in FRAUD] + [(t, 0) for _, t in LEGIT]


def vectorise(texts: list[str]) -> list[np.ndarray]:
    return [np.array(buckets(t), dtype=np.int32) for t in texts]


def train(rows: list[np.ndarray], y: np.ndarray, sw: np.ndarray | None = None, *,
          epochs=40, lr=0.5, l2=3e-5, l1=2e-4, seed=SEED) -> tuple[np.ndarray, float]:
    """Logistic regression by stochastic gradient descent, written out in full.

    Each message is a sparse binary vector, L2 normalised so a long message
    does not simply outvote a short one. Positives are upweighted because the
    data is about eight to one against them, and the Indian corpus is upweighted
    again on top of that, because it is 2% of the rows and 100% of the domain
    anyone actually cares about here.
    """
    rng = random.Random(seed)
    w = np.zeros(DIM, dtype=np.float64)
    b = 0.0
    pos_weight = float((y == 0).sum()) / max(1, int((y == 1).sum()))
    order = list(range(len(rows)))
    for epoch in range(epochs):
        rng.shuffle(order)
        step = lr / (1 + epoch * 0.15)
        for i in order:
            idx = rows[i]
            if idx.size == 0:
                continue
            v = 1.0 / np.sqrt(idx.size)
            z = w[idx].sum() * v + b
            p = 1.0 / (1.0 + np.exp(-max(-35.0, min(35.0, z))))
            g = (p - y[i]) * (pos_weight if y[i] == 1 else 1.0)
            if sw is not None:
                g *= sw[i]
            w[idx] -= step * (g * v + l2 * w[idx])
            b -= step * g
        # L1 by soft thresholding, once an epoch. Plain magnitude pruning
        # barely dents this model because SGD leaves almost every bucket
        # slightly non-zero; this drives the useless ones to exactly zero, and
        # a smaller file is the difference between shipping the model to a
        # phone and not.
        if l1:
            shrink = l1 * step * len(rows)
            w = np.sign(w) * np.maximum(0.0, np.abs(w) - shrink)
    return w, b


def logit(w, b, idx) -> float:
    if idx.size == 0:
        return b
    return float(w[idx].sum() / np.sqrt(idx.size) + b)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -35, 35)))


def auc(y, s) -> float:
    y, s = np.asarray(y), np.asarray(s)
    pos, neg = s[y == 1], s[y == 0]
    if not len(pos) or not len(neg):
        return float("nan")
    order = np.argsort(np.concatenate([pos, neg]))
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(order) + 1)
    return float((ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2)
                 / (len(pos) * len(neg)))


def prf(y, s, thr=0.5):
    y, p = np.asarray(y), np.asarray(s) >= thr
    tp = int((p & (y == 1)).sum()); fp = int((p & (y == 0)).sum())
    fn = int((~p & (y == 1)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    return prec, rec


def platt(logits, y, iters=300, lr=0.1):
    """One more logistic fit, on the model's own output, so that 0.8 means
    roughly eight in ten rather than just 'high'. Fitted on out-of-fold
    predictions only, never on anything the model was trained on."""
    a, c = 1.0, 0.0
    z = np.asarray(logits); y = np.asarray(y, dtype=float)
    for _ in range(iters):
        p = sigmoid(a * z + c)
        ga = float(((p - y) * z).mean()); gc = float((p - y).mean())
        a -= lr * ga; c -= lr * gc
    return float(a), float(c)


def main() -> int:
    print("\n  loading")
    uci = load_uci()
    local = load_local()
    print(f"    UCI SMS Spam Collection  {len(uci)} messages, {sum(l for _, l in uci)} spam")
    print(f"    this project's corpus    {len(local)} messages, {sum(l for _, l in local)} fraud")

    uci_X = vectorise([t for t, _ in uci]); uci_y = np.array([l for _, l in uci])
    loc_X = vectorise([t for t, _ in local]); loc_y = np.array([l for _, l in local])

    # --- five-fold cross validation on the Indian corpus, UCI always in train
    rng = random.Random(SEED)
    fold_of = [i % 5 for i in range(len(local))]
    rng.shuffle(fold_of)
    oof = np.zeros(len(local))
    print("\n  five-fold cross validation, measured on the Indian corpus only")
    for k in range(5):
        tr = [i for i in range(len(local)) if fold_of[i] != k]
        te = [i for i in range(len(local)) if fold_of[i] == k]
        X = uci_X + [loc_X[i] for i in tr]
        Y = np.concatenate([uci_y, loc_y[tr]])
        S = np.concatenate([np.ones(len(uci_X)), np.full(len(tr), LOCAL_WEIGHT)])
        w, b = train(X, Y, S)
        w = np.where(np.abs(w) > PRUNE, w, 0.0)   # the shipped model is pruned
        for i in te:
            oof[i] = logit(w, b, loc_X[i])
        p, r = prf(loc_y[te], sigmoid(oof[te]))
        print(f"    fold {k + 1}  n={len(te):>3}  precision {p:.2f}  recall {r:.2f}")

    a, c = platt(oof, loc_y)
    cal = sigmoid(a * oof + c)
    P, R = prf(loc_y, cal)
    print(f"\n    held out overall: AUC {auc(loc_y, oof):.3f}  "
          f"precision {P:.2f}  recall {R:.2f}")

    print("\n  calibration on the held-out predictions")
    edges = [0, .2, .4, .6, .8, 1.01]
    for lo, hi in zip(edges, edges[1:]):
        m = (cal >= lo) & (cal < hi)
        if m.sum():
            print(f"    predicted {lo:.1f}-{min(hi,1):.1f}   n={int(m.sum()):>3}   "
                  f"actually fraud {loc_y[m].mean():.2f}")

    # --- does any of this earn its place next to the rules?
    #
    # The Indian corpus cannot answer that: the rules were written against it,
    # so they score 100% on it and there is nothing left to add. UCI can, and
    # honestly, because no rule here has ever seen a 2012 British SMS.
    from rules import evaluate as rule_eval
    split = int(len(uci) * 0.8)
    holdout = list(range(split, len(uci)))
    w_h, b_h = train(uci_X[:split] + loc_X,
                     np.concatenate([uci_y[:split], loc_y]),
                     np.concatenate([np.ones(split), np.full(len(loc_X), LOCAL_WEIGHT)]))
    w_h = np.where(np.abs(w_h) > PRUNE, w_h, 0.0)
    hy = uci_y[holdout]
    hm = sigmoid(a * np.array([logit(w_h, b_h, uci_X[i]) for i in holdout]) + c)
    hr = np.array([rule_eval(uci[i][0])["score"] for i in holdout])

    print(f"\n  out of domain: {len(holdout)} UCI messages no rule was written for")
    for name, pred in (("rules alone (score >= 2)", hr >= 2),
                       ("model alone (p >= 0.6)", hm >= 0.6),
                       ("both together", (hr >= 2) | (hm >= 0.6))):
        tp = int((pred & (hy == 1)).sum()); fp = int((pred & (hy == 0)).sum())
        fn = int(((~pred) & (hy == 1)).sum())
        pr = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        print(f"    {name:<26} precision {pr:.2f}  recall {rc:.2f}")
    caught = int(((hm >= 0.6) & (hr < 2) & (hy == 1)).sum())
    print(f"    the model catches {caught} spam messages that no rule fires on")

    # --- the shipped model is trained on everything
    print("\n  training the final model on all of it")
    w, b = train(uci_X + loc_X, np.concatenate([uci_y, loc_y]),
                 np.concatenate([np.ones(len(uci_X)),
                                 np.full(len(loc_X), LOCAL_WEIGHT)]))
    keep = np.abs(w) > PRUNE
    sparse = {int(i): round(float(w[i]), 5) for i in np.nonzero(keep)[0]}
    print(f"    {len(sparse)} weights kept of {DIM} buckets")

    payload = json.dumps({
        "version": 1,
        "dim": DIM,
        "ngrams": list(NGRAMS),
        "bias": round(float(b), 5),
        "platt": [round(a, 5), round(c, 5)],
        "weights": sparse,
        "trained_on": {"uci_sms_spam": len(uci), "pakka_corpus": len(local)},
        "held_out": {"auc": round(auc(loc_y, oof), 3),
                     "precision": round(P, 3), "recall": round(R, 3)},
    }, separators=(",", ":"))
    # a .js assignment rather than a .json fetch, so the page keeps working
    # with the network off and from a file:// path
    OUT.write_text("/* Generated by tools/train_model.py - do not edit. */\n"
                   "window.PAKKA_MODEL = " + payload + ";\n")
    API_OUT.write_text(payload)
    print(f"    wrote {OUT.relative_to(ROOT)} and {API_OUT.relative_to(ROOT)}  "
          f"({OUT.stat().st_size / 1024:.0f} KB)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
