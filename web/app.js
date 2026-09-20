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
  addEventListener('mouseover', (e) => e.target.closest(grow) && cur.classList.add('big'));
  addEventListener('mouseout', (e) => e.target.closest(grow) && cur.classList.remove('big'));
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
  'Parcel at customs':
    'Your international parcel is held at customs. Pay Rs 850 clearance charge ' +
    'within 2 hours to release the shipment, otherwise it will be returned to sender.',
  'Prize message':
    'Congratulations! Your number has won KBC lucky draw of Rs 25,00,000. To claim ' +
    'your prize pay Rs 6,500 processing charge and share your bank details.',
  'Work from home':
    'Complete 5 simple tasks daily like rating hotels and earn Rs 3,000. Start with ' +
    'a prepaid task of Rs 1,000, fully refundable with commission. Join our telegram.',
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

async function check() {
  const text = t.value;

  /* decided here, on the device — instant, and the message has not gone
     anywhere yet */
  const local = window.pakkaEvaluate(text);
  render(local);

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

function render(d) {
  out.classList.add('show');
  card.className = `verdict band-${d.band}`;
  $('vlabel').textContent = d.label;
  countUp($('vscore'), d.score);
  $('msg').innerHTML = highlight(d.text, d.findings);

  $('flags').innerHTML = d.findings.map((f) => `
    <div class="flag" data-id="${f.id}">
      <div class="w">+${f.weight}</div>
      <div>
        <h4>${f.name}</h4>
        <p>${f.why}</p>
        ${f.quotes.length ? `<div class="quote">“${f.quotes.slice(0, 3).join('” · “')}”</div>` : ''}
      </div>
    </div>`).join('') || `
    <div class="flag in"><div class="w" style="color:var(--acid)">✓</div>
      <div><h4>None of the thirteen checks fired</h4>
      <p>That is not a guarantee — it means this message does not use any of the
         patterns Pakka knows about. If something still feels wrong, trust that.</p></div></div>`;

  out.scrollIntoView({ behavior: 'smooth', block: 'start' });

  /* the signature moment: phrases ignite in sequence, each one a beat after the
     last, and its card slides in with it */
  if (window.pakkaScene) window.pakkaScene(d.findings.map((f) => f.id), d.band);

  const msg = $('msg');
  msg.classList.remove('scanning');
  void msg.offsetWidth;            /* restart the sweep on a repeat check */
  msg.classList.add('scanning');
  setTimeout(() => msg.classList.remove('scanning'), 1120);  /* clear it, don't park it */

  const marks = [...msg.querySelectorAll('mark')];
  const cards = [...$('flags').querySelectorAll('.flag')];
  /* the sweep passes first, then each phrase lights as it is "found" */
  marks.forEach((m, i) => setTimeout(() => m.classList.add('lit'), 900 + i * 170));
  cards.forEach((c, i) => setTimeout(() => c.classList.add('in'), 1040 + i * 170));
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
