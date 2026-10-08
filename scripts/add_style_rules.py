# One-off: apply copy rules #2 (no contractions, body max 2 sentences, no AI tells) to changes.json.
import json
f = 'changes.json'
d = json.load(open(f))
P = {p['id']: p for p in d['pages']}

def find(pid, before):
    return next(c for c in P[pid]['changes'] if c['before'] == before)

# Existing lens cards: tag rules, and fix "after" copy that broke the new rules.
for p in d['pages']:
    for c in p['changes']:
        c.setdefault('rules', ['lens'])
c = find('collateral-mobility', "When an investor in a private fund needs cash, redeeming is usually the only option. Their units cannot easily be used as security for a loan, because lenders cannot hold or move them quickly. So the investor leaves, and your fund loses the capital.")
c['after'] = "When your investors need cash, redemption is usually their only option, because lenders cannot easily hold or move fund units as security. So the investor leaves, and the capital leaves with them."
c['rules'] = ['lens', 'length']
c['why'] = "Leads with the fund's cost instead of the investor's predicament, and cuts three sentences to two. The facts are unchanged."
c = find('collateral-mobility', "An investor pledges their units to an approved lender. The units are held as security and cannot be sold or transferred while the loan is open. When the loan is repaid, they are released straight back. You decide which lenders can take part and on what terms.")
c['after'] = "You approve the lenders and set the terms. An investor pledges units as security, and the units stay locked until the loan is repaid."
c['rules'] = ['lens', 'length']
c['why'] = "Moves the issuer's control from the last sentence to the first, and cuts four sentences to two."
c = find('distribution', "Investors transact directly with asset issuers, other investors or protocols. Settlement is instant. T+0 is the new normal.")
c['after'] = "Your investors transact directly with you, with each other or with protocols, and settle instantly at T+0."
c['rules'] = ['lens', 'length', 'ai']
c['why'] = "\"With asset issuers\" is written from the investor's side and makes the reader a third party. The rewrite also cuts three sentences to one and drops the cliché \"the new normal\"."
c = find('liquidity', "Trade around the clock, without waiting for a window.")
c['why'] = "This is an instruction to the investor. The issuer does not trade its own units here; it offers the trading."

def add(pid, section, before, after, why, rules, tier='style'):
    P[pid]['changes'].append(dict(section=section, before=before, after=after, tier=tier, rules=rules, why=why))

# Superpowers
add('collateral-mobility', "Easier to raise into · body",
    "Units that can be used as collateral are worth more to the investors who hold them. That makes your fund an easier allocation to justify.",
    "Units that work as collateral are worth more to investors, which makes your fund an easier allocation to justify.",
    "Two sentences become one plain sentence with the same claim.", ['length'])

add('secondary-transfer', "The problem today · body",
    "In most private funds, an investor who wants out has one option: wait for the next redemption window. When the window arrives, the fund has to find the cash, sometimes by selling assets it would rather keep. For many investors, that lock-up is the reason they say no in the first place.",
    "In most private funds, an investor who wants out must wait for the next redemption window, and the fund may have to sell assets to pay them. For many investors, that lock-up is the reason they say no in the first place.",
    "Cuts three sentences to two and drops the dramatic colon set-up (\"has one option: wait…\").", ['length', 'ai'])
add('secondary-transfer', "What changes · Capital stays in the fund",
    "Redemptions drain the fund. Secondary transfers do not. The position simply moves to a new holder, and your strategy stays intact.",
    "Unlike a redemption, a secondary transfer does not draw on the fund. The position moves to a new holder, and your strategy stays intact.",
    "The clipped \"X does. Y does not.\" pair and the filler \"simply\" are AI tells. Also cuts three sentences to two.", ['length', 'ai'])
add('secondary-transfer', "How it works · body",
    "When an incoming and outgoing investor agree to a transaction, ownership and payment swap in a single step. Only investors who meet your fund's eligibility rules can participate, and your limits apply automatically. Every transfer is recorded on your register the moment it happens.",
    "When two investors agree a transfer, ownership and payment swap in a single step, and only investors who meet your eligibility rules can take part. Your limits apply automatically, and every transfer is recorded on your register as it happens.",
    "Three sentences become two, with nothing dropped.", ['length'])

add('real-time-transparency', "What changes · Investors who trust you more",
    "Live holdings, statements and tax reports are always available, so investors stop calling to check. Fewer queries, more confidence in your fund, and more reason to invest again.",
    "Live holdings, statements and tax reports are always available, so investors stop calling to check. That means fewer queries and more confidence in your fund.",
    "The verbless triple (\"Fewer…, more…, and more…\") is an AI tell. This version is a plain sentence.", ['ai'])
add('real-time-transparency', "What changes · H3",
    "Your brand, not ours.",
    "Your brand on every screen.",
    "\"X, not Y\" contrasts are a common AI tell. The rewrite states the benefit directly.", ['ai'])
add('real-time-transparency', "How it works · body",
    "Every transaction updates a single register at the moment it settles. Your team works from that record, your investors see it in your portal, and statements and tax reports are produced from it. Everyone sees the same numbers, at the same time.",
    "Every transaction updates a single register the moment it settles. Your team, your investor portal, and your statements and tax reports all work from that one record.",
    "Cuts three sentences to two. The closing tagline repeated the point.", ['length', 'ai'])
add('real-time-transparency', "Readiness Index block · H2 (shared: also on Automated Compliance, Distribution)",
    "Find out where you actually stand.",
    "Find out where you stand.",
    "\"Actually\" is filler. This block is shared, so one fix updates all three pages.", ['ai'])
add('real-time-transparency', "Readiness Index block · footnote (shared: also on Automated Compliance, Distribution)",
    "Free to complete. No consultant required. Results delivered by email.",
    "Free to complete, with results sent by email.",
    "Three clipped fragments are an AI tell. \"No consultant required\" adds little. This block is shared.", ['length', 'ai'])

add('always-on', "The problem today · body",
    "Most funds run on strict domestic business hours. Subscriptions that arrive after the afternoon cut-off wait until the next working day. Traditional registry systems pause outside local operation windows, forcing international applications to wait for a local processing cycle before anything moves.",
    "Most funds run on domestic business hours, so subscriptions that arrive after the afternoon cut-off wait until the next working day. Offshore applications wait for the next local processing cycle before anything moves.",
    "Three long sentences become two shorter ones.", ['length'])
add('always-on', "What changes · Processing without friction",
    "Applications and settlement events can occur across varying time zones without waiting for the next domestic business cycle. Capital moves efficiently.",
    "Applications and settlements go through in any time zone, without waiting for the next domestic business day.",
    "\"Capital moves efficiently.\" is a filler closer. The rest is simplified.", ['ai'])
add('always-on', "How it works · body",
    "Tokeniser runs around the clock. Subscriptions, transfers and distributions are processed whenever they come in, and every one is checked against your fund's rules first, day or night. Nothing queues for the morning.",
    "Tokeniser processes subscriptions, transfers and distributions around the clock, as they come in. Each one is checked against your fund's rules first.",
    "Cuts three sentences to two. \"Day or night\" and \"Nothing queues for the morning\" restate \"around the clock\".", ['length', 'ai'])
add('always-on', "Briefs block · H2 (shared: also on Collateral Mobility, Secondary Transfer, Getting Started)",
    "Three briefs. One argument.",
    "The case for tokenising now",
    "Two clipped fragments are an AI tell. This block is shared across four pages.", ['ai'])
add('always-on', "Briefs block · body (shared: also on Collateral Mobility, Secondary Transfer, Getting Started)",
    "The commercial case for tokenisation, the window of opportunity now open in Australia, and the cost of waiting. Each brief stands alone; together they make the complete case.",
    "Three short briefs on the commercial case for tokenisation, why Australia's window is open now, and the cost of waiting.",
    "The first \"sentence\" has no verb, and \"stands alone; together…\" is a rhetorical flourish. This version is one plain sentence.", ['ai'])

add('instant-settlement', "The problem today · body",
    "Every subscription, redemption and transfer in your fund sits in limbo until it settles. That is two business days for listed funds, and often much longer for private assets. It is capital your investors cannot use, cash your fund cannot deploy, and a cost someone is paying.",
    "Every subscription, redemption and transfer in your fund waits until it settles, which takes two business days for listed funds and often longer for private assets. Until then, your investors cannot use the capital and your fund cannot deploy the cash.",
    "Cuts three sentences to two and drops the rhetorical triple (\"…and a cost someone is paying\").", ['length', 'ai'])
add('instant-settlement', "What changes · Capital back to work",
    "Subscriptions settle the moment they arrive, so cash is ready to invest straight away. No more cash drag on performance.",
    "Subscriptions settle the moment they arrive, so cash is ready to invest with no drag on performance.",
    "Folds the \"No more…\" fragment into the sentence.", ['ai'])
add('instant-settlement', "What changes · A lighter back office",
    "When the trade and the record update together, there is nothing to reconcile. Fewer breaks, fewer late fixes.",
    "When the trade and the record update together, there is nothing to reconcile and fewer breaks to fix.",
    "The clipped \"Fewer X, fewer Y.\" closer is an AI tell.", ['ai'])
add('instant-settlement', "How it works · body",
    "Today, cash and units move separately, and records catch up days later. On Tokeniser, cash and units swap in a single step, and your register updates at the same moment. If either side cannot complete, neither does.",
    "Today, cash and units move separately, and records catch up days later. On Tokeniser, cash and units swap in a single step and your register updates at the same moment, or neither side completes.",
    "Three sentences become two, with nothing dropped.", ['length'])

add('automated-compliance', "Hero · subtitle",
    "Eligibility is built into every asset and transaction. Every trade is checked against your fund's rules before it happens, not after.",
    "Eligibility is built into every asset and transaction, so every trade is checked against your fund's rules before it happens.",
    "\"…before it happens, not after\" is an AI-style contrast. \"Before\" already says it.", ['ai'])
add('automated-compliance', "What changes · Less risk, fewer breaches",
    "A trade that breaks your rules simply cannot go through. Your fiduciary duty is protected by design, and every check is recorded for your auditors.",
    "A trade that breaks your rules cannot go through, and every check is recorded for your auditors.",
    "Drops the filler \"simply\" and the stock phrase \"protected by design\".", ['ai'])
add('automated-compliance', "How it works · body",
    "Before any trade goes through, the investor is checked automatically: identity verified, eligibility confirmed (including wholesale or sophisticated status where required), and your limits applied. If a check fails, the trade does not happen. Every check is logged.",
    "Before any trade goes through, the investor's identity, eligibility (including wholesale or sophisticated status where required) and your limits are checked automatically. If a check fails, the trade does not happen, and every check is logged.",
    "Three sentences become two, with nothing dropped.", ['length'])

# Product
add('overview', "Why this matters · body",
    "Tokeniser was designed to make protocol finance accessible, credible and practical. Tokenisation is inevitable; now it feels attainable.",
    "Tokeniser makes protocol finance accessible, credible and practical for asset issuers.",
    "\"X is inevitable; now it feels attainable\" is a rhetorical AI tell. The rewrite also names the reader.", ['ai'])
add('overview', "Why this matters · A straightforward path",
    "Bringing an existing registry? Onboard progressively, taking your holders from centralised custody to self-custody. Decouple IT change from back-office change and tokenise on your terms.",
    "Bring your existing registry and move holders in stages, from centralised custody to self-custody. Change your IT and your back office at separate paces.",
    "Cuts three sentences to two and drops the question opener and the stock phrase \"on your terms\".", ['length', 'ai'])
add('overview', "Closing CTA · body",
    "Let's talk about your path forward and what's possible.",
    "Talk to us about your path to tokenisation.",
    "Has two contractions (\"Let's\", \"what's\"), and \"what's possible\" is vague.", ['contraction', 'ai'])

add('distribution', "Distribution that costs less · body",
    "Traditional channels bleed capital through layers of intermediaries. Protocol finance strips out the middlemen and connects your asset directly to investors through AI-driven networks.",
    "Traditional channels add cost through layers of intermediaries. Protocol finance removes them and connects your asset directly to investors through AI-driven networks.",
    "Tones down the dramatic verbs (\"bleed\", \"strips out\") into plain ones.", ['ai'])
add('distribution', "Investor Portal · body",
    "Launch with a modern, mobile-first investor portal that makes life easy for your investors. Configure it to your brand, your requirements, and your fund structure. Introduce more sophisticated protocol finance options as your asset seasons.",
    "Launch a mobile-first investor portal configured to your brand, requirements and fund structure. Add more protocol finance options as your asset matures.",
    "Cuts three sentences to two. \"As your asset seasons\" is jargon.", ['length'])
add('distribution', "Investor Portal · White label",
    "Your brand, your rules. The portal carries your name and your identity.",
    "The portal carries your name and your brand.",
    "The \"Your X, your Y.\" fragment is an AI tell.", ['ai'])
add('distribution', "Investor Portal · Mobile first",
    "Investors are looking for convenience, and convenience is mobile. Your asset is available to them around the clock, not just in business hours. See Always-On →",
    "Investors expect to transact on mobile, so your asset is available to them around the clock. <a href=\"/product/superpowers/always-on\">See Always-On →</a>",
    "The repetition (\"convenience, and convenience is…\") and the \"not just…\" contrast are AI tells.", ['ai'])
add('distribution', "Investor Portal · API",
    "Take the reins of your investor experience, and integrate with our registry APIs.",
    "Build your own investor experience on our registry APIs.",
    "\"Take the reins\" is a stock phrase. The rewrite says what the API does.", ['ai'])

add('liquidity', "Capital · H2",
    "Lower cost of capital is an unfair advantage",
    "A lower cost of capital, <span class=\"nowrap\">from day one</span>",
    "\"Unfair advantage\" is a cliché. The body already makes the \"from day one\" claim.", ['ai'])
add('liquidity', "Capital · body",
    "Protocol finance allows you to programmatically publish rules for an asset on a public blockchain. This allows you to offer previously inaccessible liquidity capabilities without the traditional middlemen and their fees, lowering your cost of capital from day one.",
    "Protocol finance lets you publish an asset's rules on a public blockchain. You can then offer new liquidity options without middlemen and their fees, lowering your cost of capital from day one.",
    "Plainer words with the same claims (\"allows you to… This allows you to…\", \"previously inaccessible liquidity capabilities\").", ['length'])
add('liquidity', "Markets on demand · body",
    "Give investors the freedom to enter and exit positions around the clock, with controls you configure to match your fund's structure. Liquidity no longer sleeps, and neither does their opportunity.",
    "Let investors enter and exit positions around the clock, with controls you configure to match your fund's structure.",
    "\"Liquidity no longer sleeps, and neither does…\" is a decorative AI-style closer.", ['ai'])
add('liquidity', "Borrow · H2",
    "Collateral that never sleeps",
    "Collateral at any hour",
    "\"Never sleeps\" personification is an AI tell, and it is repeated from the section above.", ['ai'])

add('efficiency', "Settlement · body",
    "Subscriptions, redemptions and distributions settle instantly, in a single step. No waiting on T+ cycles, no cash sitting idle, and no chasing mismatched records.",
    "Subscriptions, redemptions and distributions settle instantly in a single step, with no idle cash and no mismatched records to chase.",
    "The \"No X, no Y, and no Z.\" fragment is an AI tell.", ['ai'])

add('getting-started', "Hero · subtitle",
    "Tokenise fast. Decouple tech changes from back-office workflows. Our staged adoption methodology delivers protocol finance suited to your firm.",
    "Tokenise quickly, in stages, without changing your back office all at once. Our practitioners shape the rollout to suit your firm.",
    "Cuts three sentences to two, replaces the clipped imperatives, and drops \"staged adoption methodology delivers\".", ['length', 'ai'])
add('getting-started', "Adoption · body",
    "Tokenisation is now inevitable, but knowing where to start is hard. Tokeniser provides a clear, guided path that you can adopt at your own speed.",
    "Knowing where to start with tokenisation is hard. Tokeniser gives you a clear, guided path to adopt at your own pace.",
    "\"Tokenisation is now inevitable\" is a sweeping AI-style claim that appears on two pages.", ['ai'])
add('getting-started', "Adoption · Familiar form factor",
    "Familiar workflows embedded with protocol finance. No complexity, just a modern registry that works.",
    "A modern registry with familiar workflows and protocol finance built in.",
    "\"No X, just Y\" is an AI tell.", ['ai'])
add('getting-started', "Adoption · Decouple systems",
    "Take the heavy lift out of it. You change your investor experience without overhauling internal processes all at once.",
    "Change your investor experience without overhauling your internal processes all at once.",
    "\"Take the heavy lift out of it\" is a filler opener.", ['ai'])
add('getting-started', "Adoption · Full potential",
    "Access cheaper capital, 24/7 liquidity, and leverage in place. The full promise of tokenisation, reached methodically.",
    "Access <a href=\"/product/distribution\">cheaper capital</a>, <a href=\"/product/liquidity\">24/7 liquidity</a> and <a href=\"/product/superpowers/collateral-mobility\">leverage in place</a>, step by step.",
    "\"The full promise of tokenisation, reached methodically.\" is a verbless flourish. The links are kept.", ['ai'])
add('getting-started', "Guidance · Stage one",
    "Detailed documentation walks your team through each phase of adoption. No guesswork, just a proven path.",
    "Detailed guides walk your team through each phase of adoption.",
    "\"No X, just Y\" is an AI tell.", ['ai'])
add('getting-started', "Guidance · Stage three",
    "You get the right level of help at the right time. Intensive early, lighter as your team builds confidence.",
    "Support is intensive early and lighter as your team builds confidence.",
    "\"Right level… right time\" is filler, and the verbless fragment is an AI tell.", ['ai'])
add('getting-started', "Journey · body",
    "Asset issuers have a significant back-office compliance obligation, with many moving parts that need to be levelled up to achieve the gains of protocol finance. From setup to secondary trading, here are our recommended steps.",
    "Your back-office compliance has many moving parts to level up before you see the gains of protocol finance. Here are our recommended steps, from setup to secondary trading.",
    "\"Asset issuers have…\" talks about the reader in the third person. \"You\" is the issuer.", ['lens'], tier='tighten')
add('getting-started', "Journey · Direct to Investor",
    "With our investor portal as a start, create bi-lateral or protocol distribution agreements to gain improved digital distribution reach. See Distribution →",
    "Start with our investor portal, then add bilateral or protocol distribution agreements to reach more investors. <a href=\"/product/distribution\">See Distribution →</a>",
    "Simpler wording (\"to gain improved digital distribution reach\").", ['length'])

for p in d['pages']:
    for c in p['changes']:
        c.pop('shotBefore', None); c.pop('shotAfter', None)
d['rules'] = {
    'lens': 'Lens', 'contraction': 'No contractions', 'length': 'Short & simple', 'ai': 'AI tell'
}
json.dump(d, open(f, 'w'), indent=2, ensure_ascii=False)
open(f, 'a').write('\n')
print(sum(len(p['changes']) for p in d['pages']))
