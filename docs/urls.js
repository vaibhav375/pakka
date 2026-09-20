/* Things about a web address that a pattern cannot see.

   The mirror of api/urls.py, line for line, including the reason strings,
   because tools/check_parity.py compares those too.

   A rule can look for the word "sbi". It cannot tell you that the "а" in
   "аmazon.in" is Cyrillic, or that "xn--80ak6aa92e.com" is displayed as
   something else entirely. Those are properties of the characters, not of any
   phrase. */
(() => {
  const URL_RE = /\b(?:https?:\/\/|www\.)[^\s<>"']+/gi;
  const HOST_RE = /^(?:https?:\/\/)?([^/?#\s]+)/i;
  const IPV4 = /^\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?$/;

  const SCRIPTS = [
    ['LATIN', /\p{Script=Latin}/u], ['CYRILLIC', /\p{Script=Cyrillic}/u],
    ['GREEK', /\p{Script=Greek}/u], ['ARMENIAN', /\p{Script=Armenian}/u],
    ['DEVANAGARI', /\p{Script=Devanagari}/u],
  ];
  const script = (ch) => (SCRIPTS.find(([, re]) => re.test(ch)) || ['OTHER'])[0];
  const title = (s) => s[0] + s.slice(1).toLowerCase();

  /* RFC 3492 decode. Browsers will not decode punycode for you: the URL API
     hands back the xn-- form, which is exactly the form that hides the
     problem. */
  function puny(label) {
    if (!label.startsWith('xn--')) return label;
    const input = label.slice(4);
    const out = [];
    let n = 128, i = 0, bias = 72;
    const split = input.lastIndexOf('-');
    if (split > 0) for (const c of input.slice(0, split)) out.push(c.codePointAt(0));
    let at = split > 0 ? split + 1 : 0;
    const digit = (c) => {
      const v = c.codePointAt(0);
      if (v - 48 < 10) return v - 22;
      if (v - 65 < 26) return v - 65;
      if (v - 97 < 26) return v - 97;
      return 36;
    };
    const adapt = (delta, points, first) => {
      delta = first ? Math.floor(delta / 700) : delta >> 1;
      delta += Math.floor(delta / points);
      let k = 0;
      while (delta > 455) { delta = Math.floor(delta / 35); k += 36; }
      return k + Math.floor((36 * delta) / (delta + 38));
    };
    while (at < input.length) {
      const old = i;
      for (let w = 1, k = 36; ; k += 36) {
        if (at >= input.length) return label;
        const d = digit(input[at++]);
        if (d >= 36) return label;
        i += d * w;
        const t = k <= bias ? 1 : k >= bias + 26 ? 26 : k - bias;
        if (d < t) break;
        w *= 36 - t;
      }
      bias = adapt(i - old, out.length + 1, old === 0);
      n += Math.floor(i / (out.length + 1));
      i %= out.length + 1;
      out.splice(i++, 0, n);
    }
    return String.fromCodePoint(...out);
  }

  function problems(host) {
    const out = [];
    const parts = host.split(':')[0].split('.');

    for (const part of parts) {
      const scripts = new Set();
      for (const c of part) if (/\p{L}/u.test(c)) { const s = script(c); if (s !== 'OTHER') scripts.add(s); }
      if (scripts.size > 1) {
        const names = [...scripts].map(title).sort().join(', ');
        out.push(`the word "${part}" is written in two alphabets at once (${names}), `
               + 'which is how an address is made to look like a different one');
        break;
      }
    }

    if (parts.some((p) => p.startsWith('xn--'))) {
      const shown = parts.map(puny).join('.');
      out.push(`the address is punycode: it is stored as "${host}" and displayed as `
             + `"${shown}", which is not the same thing`);
    }

    if (IPV4.test(host)) out.push('it is a bare IP address, not a name anyone registered');

    for (const part of parts.slice(0, -1)) {
      const letters = [...part].filter((c) => /[a-z]/i.test(c)).length;
      const digits = [...part].filter((c) => /\d/.test(c)).length;
      if (letters >= 4 && digits > 0 && digits <= 2 && !/^\d+$/.test(part)
          && /[a-z]\d+[a-z]/i.test(part)) {
        out.push(`"${part}" has digits standing in for letters inside a word`);
        break;
      }
    }
    return out;
  }

  window.pakkaUrls = function (text) {
    const found = [];
    for (const m of text.matchAll(URL_RE)) {
      const h = HOST_RE.exec(m[0]);
      if (!h) continue;
      const host = h[1].replace(/\.+$/, '').toLowerCase();
      for (const reason of problems(host)) {
        found.push([host, reason, m.index, m.index + m[0].length]);
      }
    }
    return found;
  };
})();
