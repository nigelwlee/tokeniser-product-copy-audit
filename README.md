# Tokeniser: issuer-lens copy audit (Product + Superpowers)

A before/after review site for **Fix #1**: reframing the Product and Superpowers pages so the copy speaks to the **service provider / asset issuer**, not the investor.

- Audited source: QA preview PR-159, https://es-tokeniser-qa-website--pr-159-8p0z3ri2.web.app/product
- `changes.json`: every proposed edit (before, after, tier, reason), other notes and draft meta descriptions
- `index.html`: the review site (static; reads `changes.json`)
- `scripts/shoot.mjs`: regenerates `shots/`. It loads each live page, screenshots the section, swaps in the proposed copy and screenshots it again. It fails if a "before" string is no longer found on the live page.

```sh
npm install
node scripts/shoot.mjs            # all pages
node scripts/shoot.mjs liquidity  # one page
```

Tiers: **Must fix**: "you/your" addresses the investor, or the line tells the investor what to do. **Review**: a third-person investor line, reworked so the issuer's outcome comes first.
