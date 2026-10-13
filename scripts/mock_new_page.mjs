// Renders each draft new page into the live template page it is modelled on,
// by swapping section text in the DOM, then saves the result as a standalone HTML page
// (assets load from the QA site via <base>) with a draft banner and review notes.
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'node:fs';

const data = JSON.parse(readFileSync(new URL('../changes.json', import.meta.url)));
const browser = await chromium.launch({ channel: 'chrome' });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
const failures = [];

for (const np of data.newPages || []) {
  const p = await ctx.newPage();
  await p.goto(data.base + np.template, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: `[class*="cookie" i],[id*="cookie" i]{display:none!important}
    *{animation:none!important;transition:none!important}
    [class*="reveal"],[data-reveal],[data-aos]{opacity:1!important;transform:none!important}` });
  await p.evaluate(() => document.fonts.ready);

  for (const s of np.sections.filter((s) => s.swap)) {
    const res = await p.evaluate(({ swap, copy }) => {
      const norm = (el) => {
        const c = el.cloneNode(true);
        c.querySelectorAll('br').forEach((b) => b.replaceWith(' '));
        return c.textContent.replace(/\s+/g, ' ').trim();
      };
      const all = [...document.querySelectorAll('body *')].filter(
        (el) => !el.closest('nav, header, footer, script, style') && norm(el) === swap
      );
      const m = all.filter((el) => !all.some((o) => o !== el && el.contains(o)));
      if (m.length !== 1) return `found ${m.length}`;
      m[0].innerHTML = copy;
      const tmp = document.createElement('div');
      tmp.innerHTML = copy;
      return norm(m[0]) === norm(tmp) ? 'ok' : 'swap mismatch';
    }, s);
    if (res !== 'ok') failures.push(`${np.id} · ${s.label}: ${res}`);
  }

  // Replace the "How it works" diagram with a labelled placeholder.
  await p.evaluate(() => {
    document.querySelectorAll('img[src*="how-it-works"], picture:has(img[src*="how-it-works"])').forEach((el) => {
      const ph = document.createElement('div');
      ph.textContent = 'Diagram to be designed. See the diagram brief in the review site.';
      ph.style.cssText = 'border:2px dashed #9aa0ad;border-radius:12px;padding:72px 24px;text-align:center;font:500 16px Montserrat,sans-serif;color:#6b6f7e;background:#fff';
      (el.closest('picture') || el).replaceWith(ph);
    });
  });
  // Strip scripts, cookie UI and analytics so the copy is static; add banner + review notes.
  await p.evaluate(({ np, base }) => {
    document.querySelectorAll('script, noscript, iframe, [class*="cookie" i], [id*="cookie" i]').forEach((el) => el.remove());
    const esc = (t) => t.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const b = document.createElement('base');
    b.href = base + '/';
    document.head.prepend(b);
    document.title = `${np.name} (draft) - Tokeniser Superpower`;
    const meta = (n, c) => { const m = document.createElement('meta'); m.name = n; m.content = c; document.head.append(m); };
    meta('robots', 'noindex');
    meta('description', np.metaDescription);
    const style = document.createElement('style');
    // The icon font is blocked cross-origin, so serve a copy from the audit site.
    style.textContent = `@font-face{font-family:'Phosphor-Thin';src:url('https://tokeniser-product-copy-audit.vercel.app/assets/phosphor-thin.woff2') format('woff2');font-weight:normal;font-style:normal;font-display:swap}
      .draft-bar{position:sticky;top:0;z-index:9999;background:#fff4dc;color:#8a5a00;font:600 14px Montserrat,system-ui,sans-serif;padding:10px 16px;text-align:center;border-bottom:1px solid #f0d9a8}
      .draft-bar a{color:#8a5a00}
      .review-notes{background:#fff9ec;border-top:4px solid #f0d9a8;padding:56px 16px;font:15px/1.6 Montserrat,system-ui,sans-serif;color:#2f3240}
      .review-notes>div{max-width:1120px;margin:0 auto}
      .review-notes h2{font-size:26px;margin:0 0 6px}.review-notes h3{font-size:17px;margin:26px 0 6px}
      .review-notes ul,.review-notes ol{margin:0;padding-left:20px}.review-notes li{margin:4px 0}
      .review-notes .kv{color:#6b6f7e}.review-notes .kv b{color:#2f3240}`;
    document.head.append(style);
    const bar = document.createElement('div');
    bar.className = 'draft-bar';
    bar.innerHTML = `Draft page for review. Hold until confirmed live. Review notes are at the bottom. · <a href="https://tokeniser-product-copy-audit.vercel.app/">← Back to the copy audit</a>`;
    document.body.prepend(bar);
    const brief = np.sections.find((x) => x.label.includes('diagram')).copy;
    const notes = document.createElement('section');
    notes.className = 'review-notes';
    notes.id = 'review-notes';
    notes.innerHTML = `<div><h2>Review notes</h2>
      <p class="kv"><b>Status:</b> ${esc(np.status)}<br><b>Proposed URL:</b> ${esc(np.path)}<br><b>Menu:</b> ${esc(np.navNote)}<br><b>Meta description:</b> ${esc(np.metaDescription)}</p>
      <h3>"How it works" diagram brief</h3><p>${brief}</p>
      <h3>Holds applied</h3><ul>${np.holds.map((h) => `<li>${esc(h)}</li>`).join('')}</ul>
      <h3>Open questions for the team</h3><ol>${np.openQuestions.map((q) => `<li>${esc(q)}</li>`).join('')}</ol></div>`;
    (document.querySelector('footer') || document.body.lastElementChild).before(notes);
  }, { np, base: data.base });
  // Make the diagram placeholder carry the brief too.
  await p.evaluate((brief) => {
    const ph = [...document.querySelectorAll('div')].find((d) => d.textContent.startsWith('Diagram to be designed'));
    if (ph) { ph.innerHTML = `<b>Diagram to be designed</b><br><span style="font-size:14px;display:block;max-width:720px;margin:10px auto 0">${brief}</span>`; ph.style.padding = '48px 24px'; }
  }, np.sections.find((x) => x.label.includes('diagram')).copy);
  const html = '<!doctype html>\n' + (await p.evaluate(() => document.documentElement.outerHTML));
  const path = `${np.id}.html`;
  writeFileSync(new URL(`../${path}`, import.meta.url), html);
  console.log(`✓ ${np.id} → ${path}`);
  await p.close();
}

await browser.close();
if (failures.length) {
  console.error('FAILURES:\n' + failures.join('\n'));
  process.exit(1);
}
