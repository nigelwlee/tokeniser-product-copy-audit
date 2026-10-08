// Captures before/after screenshots of each changed section on the live QA site.
// "After" shots swap the proposed copy into the live DOM, so they show real rendering.
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const data = JSON.parse(readFileSync(new URL('../changes.json', import.meta.url)));
const only = process.argv[2];

// Runs in the page: normalised text of an element, treating <br> as a space.
const helpers = () => {
  window.__norm = (el) => {
    const c = el.cloneNode(true);
    c.querySelectorAll('br').forEach((b) => b.replaceWith(' '));
    return c.textContent.replace(/\s+/g, ' ').trim();
  };
  window.__find = (text) => {
    const all = [...document.querySelectorAll('body *')].filter(
      (el) => !el.closest('nav, header, footer, script, style') && window.__norm(el) === text
    );
    // Deepest match wins (no other match inside it).
    return all.filter((el) => !all.some((o) => o !== el && el.contains(o)));
  };
};

const browser = await chromium.launch({ channel: 'chrome' });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
const failures = [];

for (const page of data.pages) {
  if (only && page.id !== only) continue;
  if (!page.changes.length) continue;
  mkdirSync(new URL(`../shots/${page.id}/`, import.meta.url), { recursive: true });
  const p = await ctx.newPage();
  await p.goto(data.base + page.path, { waitUntil: 'networkidle' });
  await p.evaluate(helpers);
  // Remove cookie UI and force any scroll-reveal content visible.
  await p.addStyleTag({ content: `[class*="cookie" i],[id*="cookie" i]{display:none!important}
    *{animation:none!important;transition:none!important}
    [class*="reveal"],[data-reveal],[data-aos]{opacity:1!important;transform:none!important}` });
  await p.evaluate(() => document.fonts.ready);
  // Hide fixed/sticky chrome so it doesn't overlap section shots.
  await p.evaluate(() => document.querySelectorAll('body *').forEach((el) => {
    const pos = getComputedStyle(el).position;
    if (pos === 'fixed' || pos === 'sticky') el.style.visibility = 'hidden';
  }));

  // Locate every target first, tag it and its enclosing section.
  for (const [i, ch] of page.changes.entries()) {
    const n = await p.evaluate(({ text, i, asset }) => {
      const m = asset
        ? [...document.querySelectorAll('img')].filter((im) => im.currentSrc.includes(asset) && im.offsetWidth)
        : window.__find(text);
      if (m.length) {
        m[0].setAttribute('data-chg', i);
        const sec = m[0].closest('section') || m[0].parentElement;
        sec.setAttribute(`data-sec-${i}`, '');
      }
      return m.length;
    }, { text: ch.before, i, asset: ch.asset });
    if (n !== 1) failures.push(`${page.id} #${i}: found ${n} matches for "${ch.before}"`);
    ch._ok = n >= 1;
  }

  const shoot = async (i, suffix) => {
    const tab = page.changes[i].tab;
    if (tab) await p.getByRole('button', { name: tab, exact: true }).click();
    const sec = p.locator(`[data-sec-${i}]`).first();
    await sec.scrollIntoViewIfNeeded();
    await p.waitForTimeout(400);
    const box = await sec.boundingBox();
    const path = `shots/${page.id}/${i}-${suffix}.jpg`;
    const isHero = await sec.evaluate((el) => /hero/.test(el.className));
    if (isHero || page.changes[i].asset) {
      await sec.screenshot({ path, type: 'jpeg', quality: 85 });
    } else {
      // Crop tightly around the changed text (plus context) so it reads at thumbnail size.
      await p.locator(`[data-chg="${i}"]`).evaluate((e) => e.scrollIntoView({ block: 'center' }));
      await p.waitForTimeout(200);
      const box = await sec.boundingBox();
      const el = await p.locator(`[data-chg="${i}"]`).boundingBox();
      const w = Math.min(box.width, Math.max(el.width + 120, 820));
      const x = Math.max(box.x, Math.min(el.x - 60, box.x + box.width - w));
      const y = Math.max(box.y, el.y - 160, 0);
      const h = Math.min(box.y + box.height, el.y + el.height + 160, 900) - y;
      await p.screenshot({ path, type: 'jpeg', quality: 85, clip: { x, y, width: w, height: h } });
    }
    return path;
  };

  for (const [i, ch] of page.changes.entries()) {
    if (!ch._ok) continue;
    ch.shotBefore = await shoot(i, 'before');
    if (ch.asset) { delete ch._ok; console.log(`✓ ${page.id} #${i} (asset)`); continue; }
    const ok = await p.evaluate(({ i, html, before }) => {
      const el = document.querySelector(`[data-chg="${i}"]`);
      el.dataset.orig = el.innerHTML;
      el.innerHTML = html;
      const tmp = document.createElement('div');
      tmp.innerHTML = html;
      return window.__norm(el) === window.__norm(tmp) && window.__norm(el) !== before;
    }, { i, html: ch.after, before: ch.before });
    if (!ok) failures.push(`${page.id} #${i}: swap assertion failed`);
    ch.shotAfter = await shoot(i, 'after');
    // Restore so later shots in the same section show only their own change.
    await p.evaluate((i) => {
      const el = document.querySelector(`[data-chg="${i}"]`);
      el.innerHTML = el.dataset.orig;
    }, i);
    delete ch._ok;
    console.log(`✓ ${page.id} #${i} ${ch.section}`);
  }
  await p.close();
}

await browser.close();
writeFileSync(new URL('../changes.json', import.meta.url), JSON.stringify(data, null, 2) + '\n');
if (failures.length) {
  console.error('FAILURES:\n' + failures.join('\n'));
  process.exit(1);
}
