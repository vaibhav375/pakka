/* Language, kept in one place.

   The engine has read Devanagari and Hinglish for a while. The interface
   answered in English only, which is a strange thing for a tool built for
   people who do not read English comfortably.

   Anything without a translation falls back to English. That is the right
   failure for this: an untranslated line is still readable, a blank one is
   not. */
(() => {
  const KEY = 'pakka-lang';
  let lang = 'en';
  try { lang = localStorage.getItem(KEY) || 'en'; } catch { /* private window */ }
  if (lang !== 'hi') lang = 'en';

  const HI = () => window.PAKKA_HI || {};

  window.PakkaLang = {
    get: () => lang,
    hi: () => lang === 'hi',
    /* a UI string */
    t: (key, fallback) => (lang === 'hi' && HI().ui && HI().ui[key]) || fallback,
    /* a rule's name and reason */
    rule: (id, name, why) => {
      const r = lang === 'hi' && HI().rules && HI().rules[id];
      return r ? { name: r[0], why: r[1] } : { name, why };
    },
    band: (key, label) => (lang === 'hi' && HI().bands && HI().bands[key]) || label,
    action: (key, fallback) => (lang === 'hi' && HI().actions && HI().actions[key]) || fallback,
    clause: (id, fallback) => (lang === 'hi' && HI().clause && HI().clause[id]) || fallback,
    set(next) {
      lang = next === 'hi' ? 'hi' : 'en';
      try { localStorage.setItem(KEY, lang); } catch { /* ignore */ }
      document.documentElement.lang = lang;
      document.dispatchEvent(new CustomEvent('pakka:lang', { detail: lang }));
    },
  };
  document.documentElement.lang = lang;
})();
