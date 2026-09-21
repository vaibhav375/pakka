/* ---------- opening sequence ---------- */
document.documentElement.classList.add('loading');
(() => {
  const pre = document.getElementById('pre');
  const pct = document.getElementById('pct');
  const bar = document.getElementById('prebar');
  if (!pre) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let n = 0;
  const finish = () => {
    pre.classList.add('done');
    document.documentElement.classList.remove('loading');
    document.body.classList.add('ready');
  };
  if (reduce) return finish();
  const tick = () => {
    /* uneven steps: a real load does not advance smoothly */
    n = Math.min(100, n + Math.random() * 14 + 4);
    pct.textContent = String(Math.floor(n)).padStart(2, '0');
    bar.style.width = n + '%';
    if (n < 100) return setTimeout(tick, 70 + Math.random() * 90);
    setTimeout(finish, 320);
  };
  setTimeout(tick, 220);
})();

/* ---------- cursor ---------- */
(() => {
  const cur = document.getElementById('cur');
  if (!cur || matchMedia('(hover:none)').matches) return;
  let x = innerWidth / 2, y = innerHeight / 2, tx = x, ty = y;
  addEventListener('mousemove', (e) => { tx = e.clientX; ty = e.clientY; }, { passive: true });
  const loop = () => {
    x += (tx - x) * 0.18; y += (ty - y) * 0.18;      /* trails slightly, so it feels weighted */
    cur.style.transform = `translate(${x - 5}px, ${y - 5}px)`;
    requestAnimationFrame(loop);
  };
  loop();
  const grow = 'button, a, textarea, input, .chip';
  const label = (el) => {
    if (el.id === 'go') return 'check';
    if (el.id === 'copy' || el.id === 'copyfwd') return 'copy';
    if (el.classList.contains('chip')) return 'try';
    if (el.tagName === 'TEXTAREA') return 'paste';
    return '';
  };
  addEventListener('mouseover', (e) => {
    const el = e.target.closest(grow);
    if (!el) return;
    cur.dataset.label = label(el);
    cur.classList.add('big');
  });
  addEventListener('mouseout', (e) => e.target.closest(grow) && cur.classList.remove('big'));
})();

/* ---------- how far down the page you are ---------- */
(() => {
  const bar = document.getElementById('prog');
  if (!bar) return;
  const set = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.width = (max > 0 ? (scrollY / max) * 100 : 0) + '%';
  };
  addEventListener('scroll', set, { passive: true });
  addEventListener('resize', set);
  set();
})();

/* ---------- marquee: the actual phrases the rules look for ---------- */
(() => {
  const el = document.getElementById('marq');
  if (!el) return;
  const lines = ['registration fee', 'share the OTP', 'KYC has expired', 'within 2 hours',
    'selected without interview', 'pay to release your refund', 'token amount', 'guaranteed returns',
    'parcel held at customs', 'prepaid task', 'you have won', 'account will be blocked',
    'contact only on WhatsApp', 'I am posted abroad'];
  const once = lines.map((l) => `<b><i>&times;</i>${l}</b>`).join('');
  el.innerHTML = once + once;   /* doubled so the loop is seamless */
})();

/* ---------- the button leans toward the pointer ---------- */
(() => {
  const btn = document.getElementById('go');
  if (!btn || matchMedia('(hover:none)').matches) return;
  btn.addEventListener('mousemove', (e) => {
    const r = btn.getBoundingClientRect();
    btn.style.transform =
      `translate(${(e.clientX - r.left - r.width / 2) * 0.22}px, ${(e.clientY - r.top - r.height / 2) * 0.34}px)`;
  });
  btn.addEventListener('mouseleave', () => (btn.style.transform = ''));
})();

/* Pakka front end. No framework, no build step: one page, one fetch, and the
   one animation that matters — the flagged phrases lighting up one at a time,
   so you watch the message incriminate itself instead of reading a score. */

const API = (window.PAKKA_API && window.PAKKA_API.trim())
  || localStorage.getItem('pakka_api')
  || 'http://127.0.0.1:8787';

const $ = (id) => document.getElementById(id);
const t = $('t'), go = $('go'), out = $('out'), card = $('card');

/* smooth scroll, the one piece of borrowed machinery */
if (window.Lenis && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const lenis = new Lenis({ duration: 1.1, smoothWheel: true });
  const raf = (time) => { lenis.raf(time); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
}

/* reveal on scroll */
const io = new IntersectionObserver(
  (es) => es.forEach((e) => e.isIntersecting && e.target.classList.add('in')),
  { threshold: 0.18 }
);
document.querySelectorAll('.rise').forEach((el, i) => {
  el.style.transitionDelay = `${(i % 4) * 70}ms`;
  io.observe(el);
});
/* stat odometers, once, when they first come into view */
new IntersectionObserver((es, obs) => es.forEach((e) => {
  if (!e.isIntersecting) return;
  e.target.querySelectorAll('b[data-to]').forEach((el) => countUp(el, +el.dataset.to));
  obs.unobserve(e.target);
}), { threshold: 0.4 }).observe(document.querySelector('.stats'));

addEventListener('scroll', () => $('bar').classList.toggle('on', scrollY > 30), { passive: true });

/* examples — real shapes of the messages people actually get forwarded */
const EXAMPLES = {
  'Fake internship':
    'Congratulations! You have been selected without interview for the Data Entry ' +
    'position, salary Rs 25,000 for 2 hours daily work from home. Pay registration fee ' +
    'of Rs 1,499 within 2 hours to confirm your seat. Contact us only on WhatsApp. ' +
    'hr.hiring2026@gmail.com',
  'KYC message':
    'Dear Customer, your KYC has expired and your account will be blocked today. ' +
    'Update immediately at bit.ly/kyc-verify-now or share the OTP with our executive ' +
    'to avoid deactivation.',
  'PG listing':
    'Single room near PES RR campus, fully furnished, 7500/month including wifi. ' +
    'I am currently abroad so I cannot show the room, please transfer the token amount ' +
    'to 9845012345 on google pay and I will block it for you.',
  'Parcel stuck':
    'Your parcel is held at customs due to incomplete documents. Pay the customs ' +
    'clearance charge of Rs 850 within 24 hours or the shipment will be returned. ' +
    'Track at cutt.ly/parcel-release',
  'Lottery win':
    'Congratulations!! You have won KBC lucky draw prize of Rs 25,00,000. To claim your ' +
    'prize pay the processing charge of Rs 6,500 and share your bank details. ' +
    'Contact us only on WhatsApp immediately.',
  'Task scheme':
    'Join our part time team. Complete 5 simple tasks daily, like and subscribe videos, ' +
    'earn Rs 3,000 per day from home. First prepaid task of Rs 1,000 required to unlock ' +
    'commission. Join our telegram.',
  'Loan app':
    'Your loan payment is overdue. If not cleared today we will inform your contacts ' +
    'and family and take legal action. An FIR will be filed against you.',
  'Electricity cut':
    'Dear consumer, your electricity will be disconnected tonight at 9:30 pm because ' +
    'your previous bill was not updated. Immediately contact our officer on 9812345678.',
  'Marketplace seller':
    'I am an army officer posted in Leh so I cannot meet you. Pay the token amount ' +
    'to 9845012345 on google pay and the bike will be delivered by CSD courier.',
  'A normal message':
    'Hi Vaibhav, this is Priya from the placement cell. Your Infosys interview is on ' +
    'Monday at 10am in Seminar Hall 2. Please carry two copies of your resume.',
};
$('chips').innerHTML = Object.keys(EXAMPLES)
  .map((k) => `<button class="chip" data-k="${k}">${k}</button>`).join('');
$('chips').onclick = (e) => {
  const k = e.target.dataset.k;
  if (!k) return;
  t.value = EXAMPLES[k];
  sync();
  t.focus();
};

const sync = () => {
  const n = t.value.trim().length;
  $('count').textContent = `${n} / 4000`;
  go.disabled = n === 0 || n > 4000;
};
t.addEventListener('input', sync);
t.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'Enter' && !go.disabled) check();
});
sync();

/* build the message with <mark> around every flagged span, merging overlaps so
   nested matches don't produce broken tags */
function highlight(text, findings) {
  const spans = findings.flatMap((f) => f.spans.map(([a, b]) => ({ a, b, id: f.id })))
    .sort((x, y) => x.a - y.a);
  const merged = [];
  for (const s of spans) {
    const last = merged[merged.length - 1];
    if (last && s.a <= last.b) last.b = Math.max(last.b, s.b);
    else merged.push({ ...s });
  }
  let html = '', at = 0;
  const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  for (const s of merged) {
    html += esc(text.slice(at, s.a)) + `<mark data-id="${s.id}">${esc(text.slice(s.a, s.b))}</mark>`;
    at = s.b;
  }
  return html + esc(text.slice(at));
}

const countUp = (el, to) => {
  const started = performance.now(), dur = 700;
  const step = (now) => {
    const k = Math.min(1, (now - started) / dur);
    el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3)));
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
};

/* what to do next, assembled from the rules that fired — the same tables the
   server uses, shipped with the rules so it works with no network */
function adviceFor(findings) {
  const A = window.PAKKA_ADVICE;
  if (!A) return { actions: [], forward: '' };
  const ids = findings.map((f) => f.id);
  const has = (group) => ids.some((id) => A[group].includes(id));
  if (!ids.length) {
    return {
      actions: [
        'Nothing matched, but that is not proof it is safe — it means this message ' +
        `does not use any of the ${(window.PAKKA_RULES || []).length} patterns Pakka knows.`,
        'If it still feels wrong, verify on a number you already had, not one from the message.',
      ],
      forward: '',
    };
  }
  const actions = ['Do not pay anything and do not share any code, however small the amount.'];
  if (ids.includes('ASKS_FOR_SECRET'))
    actions.push('Never share an OTP, PIN or CVV. No bank, delivery agent or employer will ever ask for one.');
  if (has('money'))
    actions.push('Money sent to a personal UPI ID or account is very hard to get back, which is exactly why they ask for it that way.');
  if (has('job'))
    actions.push('Search the company name with the word careers and apply only from its own site.');
  if (has('impersonation'))
    actions.push('If you think it might be genuine, call the number printed on your own bill, card or the official website — never the one in the message.');
  if (has('property'))
    actions.push('See the place in person and meet the owner before any money moves. No photo, video call or document replaces that.');
  actions.push('Report it at cybercrime.gov.in or call 1930. If money has already gone, report within the first hour, while it can still be frozen.');
  actions.push('Block the sender, then tell whoever forwarded it to you.');

  const top = ids.slice(0, 2).map((id) => A.clause[id]).filter(Boolean);
  const reasons = top.length ? top.join(' and ') : 'it matches known scam patterns';
  return {
    actions,
    forward: `I checked this before replying — ${reasons}. That is how this kind of scam ` +
             `works, so I am not paying or sharing anything. Please do not send money ` +
             `either. (Checked with Pakka)`,
  };
}

async function check() {
  const text = t.value;

  /* decided here, on the device — instant, and the message has not gone
     anywhere yet */
  const local = window.pakkaEvaluate(text);
  render(local);
  hunch(text, local);

  /* the only reason to talk to the cloud is to mint a link worth forwarding */
  if (!API || API.startsWith('http://127.0.0.1')) {
    $('link').value = 'Sharing needs the deployed API';
    return;
  }
  $('link').value = 'Creating link…';
  try {
    const res = await fetch(`${API.replace(/\/$/, '')}/scan`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    const d = await res.json();
    if (!res.ok || !d.id) throw new Error(d.error || 'no id');
    $('link').value = `${location.origin}${location.pathname}#${d.id}`;
  } catch {
    $('link').value = 'Could not create a link — the verdict above still stands';
  }
}
go.onclick = check;

/* Arriving from another app's share sheet.

   Installed on Android, Pakka registers as a share target, so a message in
   WhatsApp can be long-pressed, shared to Pakka, and answered without anyone
   copying or pasting anything. The share arrives as an ordinary query string,
   which is then wiped from the address bar so a stranger's message is not left
   sitting in the history. */
(() => {
  const q = new URLSearchParams(location.search);
  const shared = [q.get('title'), q.get('text'), q.get('url')]
    .filter(Boolean).join(' ').trim();
  if (!shared) return;
  history.replaceState(null, '', location.pathname + location.hash);
  t.value = shared;
  t.dispatchEvent(new Event('input', { bubbles: true }));
  addEventListener('load', () => setTimeout(() => {
    check();
    document.getElementById('out')?.scrollIntoView({ behavior: 'smooth' });
  }, 350));
})();

/* the service worker is what makes the app installable, and installing is what
   puts it in the share sheet */
if ('serviceWorker' in navigator) {
  addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
}

function render(d) {
  remember(d);
  /* the constellation lights from the same findings that draw the cards */
  window.PakkaScene?.light((d.findings || []).map((f) => f.id));
  const glc = document.getElementById('glcount');
  if (glc) glc.textContent = (d.findings || []).length;

  out.classList.add('show');
  card.className = `verdict band-${d.band}`;
  $('vlabel').textContent = d.label;
  countUp($('vscore'), d.score);
  const g = document.getElementById('gfill');
  if (g) {                       /* 198 is the dash length of the three-quarter arc */
    const frac = Math.max(0, Math.min(1, d.score / 10));
    setTimeout(() => (g.style.strokeDashoffset = String(198 - 198 * frac)), 60);
  }
  $('msg').innerHTML = highlight(d.text, d.findings);

  /* the score, shown as the pieces it is made of */
  const total = d.findings.reduce((n, f) => n + f.weight, 0) || 1;
  $('weights').innerHTML = d.findings
    .map((f) => `<i style="width:${(f.weight / total) * 100}%" title="${f.name} +${f.weight}"></i>`)
    .join('');

  $('flags').innerHTML = d.findings.map((f) => `
    <div class="flag" data-id="${f.id}">
      <div class="w">+${f.weight}</div>
      <div>
        <h4>${f.name}</h4>
        <p>${f.why}</p>
        ${f.quotes.length ? `<div class="quote">\u201c${f.quotes.slice(0, 3).join('\u201d \u00b7 \u201c')}\u201d</div>` : ''}
      </div>
    </div>`).join('') || `
    <div class="flag in"><div class="w" style="color:var(--acid)">\u2713</div>
      <div><h4>None of the ${(window.PAKKA_RULES || []).length} checks fired</h4>
      <p>That is not a guarantee \u2014 it means this message does not use any of the
         patterns Pakka knows about. If something still feels wrong, trust that.</p></div></div>`;

  /* what to do about it, and what to send back */
  const adv = d.advice || adviceFor(d.findings || []);
  $('advice').hidden = !adv.actions.length;
  $('actions').innerHTML = adv.actions.map((a) => `<li>${a}</li>`).join('');
  $('fwd').hidden = !adv.forward;
  $('fwdtext').value = adv.forward || '';

  $('link').value = d.id
    ? `${location.origin}${location.pathname}#${d.id}`
    : 'Could not create a link \u2014 the verdict above still stands';

  if (window.pakkaScene) window.pakkaScene(d.findings.map((f) => f.id), d.band);

  out.scrollIntoView({ behavior: 'smooth', block: 'start' });

  const msg = $('msg');
  msg.classList.remove('scanning');
  void msg.offsetWidth;                /* restart the sweep on a repeat check */
  msg.classList.add('scanning');
  /* the sweep is a pass over the text, not a bar that stays: clear the class
     when it finishes or the gradient snaps back to the top and sits there */
  setTimeout(() => msg.classList.remove('scanning'), 1150);

  /* the sweep passes first, then each phrase lights as it is found, then its
     explanation slides in beside it */
  /* point at a rule and its evidence lights up in the message above */
  const flagsBox = $('flags');
  /* a hover idea only. On a touch screen the tap fires mouseover and leaves a
     phrase stuck in the peek colour with nothing pointing at it. */
  const canHover = matchMedia('(hover: hover)').matches;
  flagsBox.onmouseover = !canHover ? null : (e) => {
    const card = e.target.closest('.flag');
    if (!card || !card.dataset.id) return;
    flagsBox.classList.add('dim');
    card.classList.add('peek');
    msg.querySelectorAll(`mark[data-id="${card.dataset.id}"]`).forEach((m) => m.classList.add('peek'));
  };
  flagsBox.onmouseout = !canHover ? null : () => {
    flagsBox.classList.remove('dim');
    flagsBox.querySelectorAll('.peek').forEach((el) => el.classList.remove('peek'));
    msg.querySelectorAll('mark.peek').forEach((m) => m.classList.remove('peek'));
  };

  const marks = [...msg.querySelectorAll('mark')];
  const cards = [...$('flags').querySelectorAll('.flag')];
  marks.forEach((m, i) => setTimeout(() => m.classList.add('lit'), 900 + i * 170));
  cards.forEach((c, i) => setTimeout(() => c.classList.add('in'), 1040 + i * 170));
  setTimeout(() => $('weights').querySelectorAll('i')
    .forEach((b, i) => setTimeout(() => b.classList.add('in'), i * 90)), 900);
}

/* hovering a flag lights only its own phrases, and the reverse — the link
   between an explanation and the words it is about should not need reading */
const linkHover = (on) => (e) => {
  const flag = e.target.closest('.flag');
  const mk = e.target.closest('mark');
  const id = flag?.dataset.id || mk?.dataset.id;
  if (!id) return;
  document.querySelectorAll(`mark[data-id="${id}"]`).forEach((m) => m.classList.toggle('focus', on));
  document.querySelectorAll(`.flag[data-id="${id}"]`).forEach((f) => f.classList.toggle('focus', on));
};
document.addEventListener('mouseover', linkHover(true));
document.addEventListener('mouseout', linkHover(false));

/* the rulebook, generated from the same file the API runs */
fetch('rules.json')
  .then((r) => r.json())
  .then((rules) => {
    const g = document.getElementById('rulegrid');
    if (g) g.innerHTML = rules
      .sort((a, b) => b.weight - a.weight)
      .map((r) => `<div class="rulecard"><div class="w">+${r.weight}</div>
        <h4>${r.name}</h4><p>${r.why}</p></div>`).join('');
  })
  .catch(() => {});

/* every count on the page comes from the generated rules, so none of them can
   go stale when a rule is added */
(() => {
  const n = (window.PAKKA_RULES || []).length;
  if (!n) return;
  ['rulecount', 'gltotal'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.textContent = n;
  });
  document.querySelectorAll('b[data-to="39"]').forEach((el) => { el.dataset.to = n; });
})();

/* ---------- rules gallery: a column that walks itself ---------- */
(() => {
  const col = document.getElementById('gcol');
  const R = window.PAKKA_RULES || [];
  if (!col || !R.length) return;

  /* the first alternative of a rule's pattern, tidied into something readable:
     what that rule is actually hunting for */
  const hunts = (re) => (re || '').split('|')[0]
    .replace(/\(\?:/g, '').replace(/\\b/g, '')
    .replace(/\.\{[^}]*\}/g, ' … ').replace(/\\s\?/g, ' ')
    .replace(/\\\./g, '.').replace(/[()?\[\]]/g, '')
    .replace(/\s+/g, ' ').trim();
  col.innerHTML = '<ul>' + R.map((r, i) =>
    `<li data-i="${i}"><b>${String(i + 1).padStart(2, '0')}</b>${r.name}</li>`).join('') + '</ul>';
  const ul = col.querySelector('ul');
  const items = [...col.querySelectorAll('li')];
  const ROW = 44, VIEW = 8;
  let i = 0, timer = null;

  const show = (n) => {
    i = (n + R.length) % R.length;
    items.forEach((el, k) => el.classList.toggle('on', k === i));
    /* keep the active row near the middle of the window */
    const top = Math.max(0, Math.min(i - Math.floor(VIEW / 2), R.length - VIEW));
    ul.style.transform = `translateY(${-top * ROW}px)`;
    $('gnum').textContent = String(i + 1).padStart(2, '0') + ' / ' + (window.PAKKA_RULES || []).length;
    $('gname').textContent = R[i].name;
    $('ghunt').textContent = '“' + hunts(R[i].re) + '”';
  };
  const play = () => { clearInterval(timer); timer = setInterval(() => show(i + 1), 2300); };
  items.forEach((el) => el.addEventListener('click', () => { show(+el.dataset.i); play(); }));
  col.addEventListener('mouseenter', () => clearInterval(timer));
  col.addEventListener('mouseleave', play);
  show(0);
  new IntersectionObserver((es) => (es[0].isIntersecting ? play() : clearInterval(timer)),
    { threshold: 0.25 }).observe(col);
})();

/* ---------- what you have checked this session ---------- */
const HIST = [];
function remember(d) {
  const text = d.text || t.value;
  if (HIST.some((h) => h.text === text)) return;
  HIST.unshift({ text, band: d.band, label: d.label, score: d.score });
  HIST.length = Math.min(HIST.length, 6);
  const box = $('hist');
  box.classList.add('on');
  box.innerHTML = '<span class="mono" style="color:var(--dim)">This session</span>' +
    HIST.map((h, i) =>
      `<button data-h="${i}" title="${h.label}"><i class="${h.band}"></i>` +
      `${h.text.slice(0, 26).replace(/[<>&]/g, '')}…<span class="mono">${h.score}</span></button>`
    ).join('');
  box.onclick = (e) => {
    const b = e.target.closest('button[data-h]');
    if (!b) return;
    t.value = HIST[+b.dataset.h].text;
    sync();
    check();
  };
}

$('copyfwd').onclick = async () => {
  const v = $('fwdtext').value;
  if (!v) return;
  try { await navigator.clipboard.writeText(v); } catch {}
  $('copyfwd').textContent = 'Copied';
  setTimeout(() => ($('copyfwd').textContent = 'Copy message'), 1600);
};

$('copy').onclick = async () => {
  const v = $('link').value;
  if (v === '—') return;
  try { await navigator.clipboard.writeText(v); } catch {}
  $('copy').textContent = 'Copied';
  setTimeout(() => ($('copy').textContent = 'Copy link'), 1600);
};

/* opening a shared link loads that saved scan */
if (location.hash.length > 1) {
  fetch(`${API.replace(/\/$/, '')}/v/${location.hash.slice(1)}`)
    .then((r) => (r.ok ? r.json() : null))
    .then((d) => { if (d) { t.value = d.text; sync(); render(d); } })
    .catch(() => {});
}

/* ---------- the two front doors ---------- */
(() => {
  const bot = (window.PAKKA_TELEGRAM || '').replace(/^@/, '').trim();
  const link = document.getElementById('tg');
  const note = document.getElementById('tgnote');
  if (bot && link) {
    link.href = `https://t.me/${bot}`;
    link.hidden = false;
    link.target = '_blank';
    link.rel = 'noopener';
    if (note) note.textContent = `@${bot} · works on every phone and on desktop`;
  }

  /* Chrome fires this when the app is installable. Until then the button would
     do nothing, so it says what to do by hand instead of lying. */
  const btn = document.getElementById('install');
  const inote = document.getElementById('installnote');
  if (!btn) return;
  let prompt = null;
  addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    prompt = e;
    btn.disabled = false;
  });
  const standalone = matchMedia('(display-mode: standalone)').matches;
  if (standalone) {
    btn.disabled = true;
    btn.textContent = 'Already installed';
    if (inote) inote.textContent = 'Share a message to Pakka from any app on this phone.';
  } else {
    btn.disabled = true;                 /* until the browser says it is installable */
  }
  btn.onclick = async () => {
    if (!prompt) return;
    btn.disabled = true;
    prompt.prompt();
    const { outcome } = await prompt.userChoice;
    prompt = null;
    if (inote) inote.textContent = outcome === 'accepted'
      ? 'Installed. Long-press a message in WhatsApp, Share, then Pakka.'
      : 'Not installed. You can add it later from the browser menu.';
  };
})();

/* ---------- what the model makes of it ----------

   The rules decide. This is shown underneath them and never instead of them,
   because it is the part that can be wrong. It earns its place in one
   situation in particular: when no rule fires at all and the message still
   reads like every scam the model was trained on. Rules are blind to
   phrasings nobody wrote down, and out of domain they catch about one in
   twenty-five. The model catches most of the rest. */
function hunch(text, verdict) {
  const box = document.getElementById('hunch');
  const out = document.getElementById('hunchtext');
  if (!box || !out || !window.pakkaModel) return;
  const r = window.pakkaModel(text);
  const pct = Math.round(r.p * 100);
  const fired = (verdict.findings || []).length;
  box.classList.toggle('high', r.p >= 0.6);

  /* The model may raise concern and may never clear it: a headline of
     "Nothing suspicious found" over a 90-out-of-100 reading is the one failure
     that actually costs someone money.

     The dial has to move with it. A green 0 beside an amber warning reads as
     "safe" to anyone glancing at it, and the number is the part people glance
     at, so when the warning comes from the model the dial shows the model's
     number instead of a rule score of zero. */
  const label = document.getElementById('vlabel');
  const dial = document.getElementById('diallabel');
  const card = document.getElementById('card');
  const gauge = document.getElementById('gfill');
  const modelLed = !fired && r.p >= 0.8;
  if (modelLed && label) {
    label.textContent = 'Nothing matched, but be careful';
    label.classList.add('warn');
    if (card) card.className = 'verdict band-careful';
    if (dial) dial.textContent = 'Model reading';
    countUp($('vscore'), pct);
    if (gauge) setTimeout(() => (gauge.style.strokeDashoffset = String(198 - 198 * r.p)), 60);
  } else {
    if (label) label.classList.remove('warn');
    if (dial) dial.textContent = 'Risk score';
  }

  /* 0.75, not 0.6. The calibration table says 0.6 to 0.8 is only about seven in
     ten, and telling somebody their delivery notification reads like a scam on
     those odds is how a tool stops being believed. */
  let line;
  if (!fired && r.p >= 0.75) {
    line = `<b>No rule fired, but this still reads like a scam.</b> The model puts it at
            ${pct} out of 100, which is where about nine in ten messages turn out to be
            fraud. That is a reason to be careful, not proof, and it is also how new
            rules get found.`;
  } else if (!fired && r.p >= 0.5) {
    line = `Nothing matched, and the model is not certain either, at ${pct} out of 100.
            Around half of the messages it reads that way are fine.`;
  } else if (fired && r.p >= 0.6) {
    line = `The model agrees with the rules independently, putting this at ${pct} out of 100.`;
  } else if (fired) {
    line = `The model is less sure, at ${pct} out of 100. The rules above quote the exact
            words, so they are the ones to read.`;
  } else {
    line = `The model puts this at ${pct} out of 100, which is where most messages sit.
            Nothing here looks like the fraud it was trained on.`;
  }

  const safe = (x) => x.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const spans = window.pakkaModelSpans(text, r.heat || []);
  if (spans.length && r.p >= 0.5) {
    const bits = spans.map(([a, b]) => safe(text.slice(a, b).trim())).filter(Boolean);
    if (bits.length) {
      line += ` It reacted most to <mark class="hunch-mark">`
            + bits.join('</mark>, <mark class="hunch-mark">') + '</mark>.';
    }
  }
  out.innerHTML = line;
  box.hidden = false;
}
