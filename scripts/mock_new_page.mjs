// Renders each draft new page into the live template page it is modelled on,
// by swapping section text in the DOM, then takes a full-page screenshot.
import { chromium } from 'playwright';
import { readFileSync, mkdirSync } from 'node:fs';

const data = JSON.parse(readFileSync(new URL('../changes.json', import.meta.url)));
const browser = await chromium.launch({ channel: 'chrome' });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
const failures = [];
mkdirSync(new URL('../shots/new/', import.meta.url), { recursive: true });

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
  // Hide fixed/sticky chrome (cookie button, floating widgets) for a clean capture.
  await p.evaluate(() => document.querySelectorAll('body *').forEach((el) => {
    const pos = getComputedStyle(el).position;
    if (pos === 'fixed') el.style.visibility = 'hidden';
  }));
  await p.waitForTimeout(500);
  const path = `shots/new/${np.id}.jpg`;
  await p.screenshot({ path, type: 'jpeg', quality: 80, fullPage: true });
  console.log(`✓ ${np.id} → ${path}`);
  await p.close();
}

await browser.close();
if (failures.length) {
  console.error('FAILURES:\n' + failures.join('\n'));
  process.exit(1);
}
