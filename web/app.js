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
  const marks = [...$('msg').querySelectorAll('mark')];
  const cards = [...$('flags').querySelectorAll('.flag')];
  marks.forEach((m, i) => setTimeout(() => m.classList.add('lit'), 380 + i * 170));
  cards.forEach((c, i) => setTimeout(() => c.classList.add('in'), 520 + i * 170));
}

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
