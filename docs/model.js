/* The linear model, scored on the device.

   Everything here exists twice: once in tools/features.py and once here.
   tools/check_parity.py fails the build if the two ever disagree, the same way
   it does for the rules.

   A linear model is not a compromise here, it is the point. Its output is
   literally the sum of its per-feature contributions, so the characters that
   pushed a message towards "scam" can be pointed at, and nothing has to be
   taken on trust. It is also a dot product, so it runs offline with no
   runtime dependency and no network call. */
(() => {
  const M = window.PAKKA_MODEL;
  if (!M) return;
  const DIM = M.dim, NGRAMS = M.ngrams;
  const W = M.weights;                       /* sparse: only non-zero buckets */

  /* 32-bit FNV-1a, matching fnv1a() in tools/features.py. normalise() has
     already replaced astral characters, so a Python code point and a
     JavaScript code unit are the same thing by this point. */
  function fnv1a(s) {
    let h = 2166136261;
    for (let i = 0; i < s.length; i++) {
      h = Math.imul(h ^ s.charCodeAt(i), 16777619) >>> 0;
    }
    return h;
  }

  const sigmoid = (z) => 1 / (1 + Math.exp(-Math.max(-35, Math.min(35, z))));

  /* Score a message, and say which parts of it moved the needle.

     Returns the calibrated probability plus a weight per character of the
     ORIGINAL text, so the page can shade the phrases the model reacted to
     exactly as it highlights the phrases a rule matched. */
  window.pakkaModel = function (text) {
    const [flat, idx] = window.pakkaNormalise(text);
    const low = flat.toLowerCase();
    const seen = new Map();                  /* bucket -> [start, end] in the original */
    for (const n of NGRAMS) {
      for (let i = 0; i + n <= low.length; i++) {
        const bucket = fnv1a(low.slice(i, i + n)) % DIM;
        if (!seen.has(bucket) && idx.length) {
          seen.set(bucket, [idx[i], idx[Math.min(i + n, idx.length) - 1] + 1]);
        }
      }
    }
    const k = seen.size;
    if (!k) return { p: sigmoid(M.platt[0] * M.bias + M.platt[1]), z: M.bias, heat: [] };

    const v = 1 / Math.sqrt(k);
    let sum = 0;
    const heat = new Float64Array(text.length);
    for (const [bucket, [a, b]] of seen) {
      const w = W[bucket];
      if (w === undefined) continue;
      sum += w;
      const share = (w * v) / Math.max(1, b - a);
      for (let c = a; c < b && c < heat.length; c++) heat[c] += share;
    }
    const z = sum * v + M.bias;
    return { p: sigmoid(M.platt[0] * z + M.platt[1]), z, heat: Array.from(heat) };
  };

  /* The phrases the model leaned on hardest, as spans of the original text.
     Only positive contributions, and only ones that clear a floor, because a
     highlight on every other character explains nothing. */
  window.pakkaModelSpans = function (text, heat, limit = 3) {
    const out = [];
    let run = null;
    const floor = Math.max(...heat.map(Math.abs), 0) * 0.35;
    if (!floor) return out;
    for (let i = 0; i < heat.length; i++) {
      if (heat[i] >= floor) {
        if (!run) run = { a: i, b: i + 1, w: 0 };
        run.b = i + 1;
        run.w += heat[i];
      } else if (run) {
        out.push(run);
        run = null;
      }
    }
    if (run) out.push(run);
    /* character n-grams end mid-word, and "ur KY" explains nothing to a
       person, so every span grows out to the words it sits inside */
    const word = (c) => !!c && /[A-Za-z0-9_\u0900-\u097F]/.test(c);
    const whole = ([a, b]) => {
      while (a > 0 && word(text[a - 1]) && word(text[a])) a -= 1;
      while (b < text.length && word(text[b]) && word(text[b - 1])) b += 1;
      return [a, b];
    };
    return out.sort((x, y) => y.w - x.w).slice(0, limit)
              .map((r) => whole([r.a, r.b])).sort((x, y) => x[0] - y[0]);
  };
})();
