"""The linear model, scored server side.

Same weights, same features and same arithmetic as web/model.js, so a verdict
delivered over Telegram says what the page would have said. The model is a
JSON file of 727 numbers; scoring it is a dot product, which is why it can run
in a Lambda cold start and in a browser without anyone noticing either.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from features import spans_for  # noqa: E402

HERE = pathlib.Path(__file__).parent
_M: dict | None = None


def _model() -> dict | None:
    global _M
    if _M is None:
        path = HERE / "model.json"
        _M = json.loads(path.read_text()) if path.exists() else {}
        if _M:
            _M["weights"] = {int(k): v for k, v in _M["weights"].items()}
    return _M or None


def score(text: str) -> dict | None:
    """Return the calibrated probability and the spans that drove it.

    None when no model file is present, which is a supported state: the rules
    are the product and the model is an addition to it, so a deployment
    without one degrades to exactly what shipped before.
    """
    m = _model()
    if not m:
        return None
    seen: dict[int, tuple[int, int]] = {}
    for bucket, a, b in spans_for(text):
        seen.setdefault(bucket, (a, b))
    if not seen:
        z = m["bias"]
        return {"p": _sig(m["platt"][0] * z + m["platt"][1]), "z": z, "spans": []}

    # Exactly what web/model.js does, step for step. A linear model's output is
    # the sum of its per-feature contributions, so each weight is laid back
    # down on the characters its n-gram came from, and the hottest runs are the
    # phrases the model actually reacted to.
    v = 1.0 / math.sqrt(len(seen))
    total = 0.0
    heat = [0.0] * len(text)
    for bucket, (a, b) in seen.items():
        w = m["weights"].get(bucket)
        if w is None:
            continue
        total += w
        share = (w * v) / max(1, b - a)
        for c in range(a, min(b, len(heat))):
            heat[c] += share
    z = total * v + m["bias"]

    return {"p": _sig(m["platt"][0] * z + m["platt"][1]), "z": z,
            "spans": _hot_spans(text, heat)}


def _hot_spans(text: str, heat: list[float], limit: int = 3) -> list[tuple[int, int]]:
    floor = max((abs(h) for h in heat), default=0.0) * 0.35
    if not floor:
        return []
    runs: list[tuple[int, int, float]] = []
    run: list[float] | None = None
    a = 0
    for i, h in enumerate(heat):
        if h >= floor:
            if run is None:
                a, run = i, [0.0]
            run[0] += h
            b = i + 1
        elif run is not None:
            runs.append((a, b, run[0]))
            run = None
    if run is not None:
        runs.append((a, b, run[0]))
    runs.sort(key=lambda r: -r[2])
    return sorted(_whole(text, a, b) for a, b, _ in runs[:limit])


def _word(c: str) -> bool:
    return c.isalnum() or c == "_"


def _whole(text: str, a: int, b: int) -> tuple[int, int]:
    """An n-gram ends mid-word, and "ur KY" explains nothing to a person."""
    while a > 0 and _word(text[a - 1]) and _word(text[a]):
        a -= 1
    while b < len(text) and _word(text[b]) and _word(text[b - 1]):
        b += 1
    return a, b


def _sig(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-35.0, min(35.0, z))))
