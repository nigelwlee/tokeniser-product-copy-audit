# One-off: rewrite all proposed copy in an institutional (asset-manager comms) voice,
# and add "tone" cards for casual live lines. Keeps every `before` exact.
import json
f = 'changes.json'
d = json.load(open(f))
P = {p['id']: p for p in d['pages']}
d['rules']['tone'] = 'Institutional tone'

def rw(pid, i, after, why=None, add_tone=True):
    c = P[pid]['changes'][i]
    c['after'] = after
    if why: c['why'] = why
    if add_tone and 'tone' not in c['rules']: c['rules'].append('tone')

A = '<a href="/product/superpowers/always-on">See Always-On →</a>'

# ---- Revisions to existing cards ----
rw('collateral-mobility', 0, 'Retain capital, <em>even when investors need liquidity.</em>',
   '"Your holdings" addresses the investor. The rewrite states the issuer outcome in measured terms.')
rw('collateral-mobility', 1, 'When your investors need liquidity, redemption is often the only option. This risks losing capital from your fund.',
   "Leads with the fund's exposure, in two measured sentences.")
rw('collateral-mobility', 2, 'Enable investors to borrow against their units rather than redeem. They remain invested, and your AUM is retained.')
rw('collateral-mobility', 3, 'You approve the lenders and set the terms. Investors pledge units as security, and the units remain locked until the loan is repaid.')
rw('collateral-mobility', 4, 'Today: Liquidity need → Redemption, capital leaves the fund · On Tokeniser: Units pledged → Loan funded → Repaid and released · "Capital retained."')
rw('collateral-mobility', 5, 'Units that can serve as collateral are more valuable to investors, which strengthens the case for allocating to your fund.')

rw('secondary-transfer', 0, 'Offer investors an exit, <em>without a redemption.</em>',
   '"Change hands" describes the investor\'s action. The issuer\'s value is offering an exit that does not draw on the fund.')
rw('secondary-transfer', 1, "Enable investors to exit between redemption windows by transferring their position to another eligible investor. Your fund's capital is unaffected.")
rw('secondary-transfer', 2, 'Lock-up periods that deter investors')
rw('secondary-transfer', 3, 'In most private funds, investors can exit only at scheduled redemption windows, and meeting redemptions may require the sale of assets. For many investors, this lock-up is a key reason not to invest.')
rw('secondary-transfer', 4, 'Unlike a redemption, a secondary transfer does not draw on fund capital. The position moves to a new holder, and your investment strategy is preserved.')
rw('secondary-transfer', 5, 'When two eligible investors agree to a transfer, ownership and payment are exchanged in a single step. Your eligibility rules and limits apply automatically, and every transfer is recorded on your register in real time.')

rw('real-time-transparency', 0, 'Your register, <em>current in real time.</em>')
rw('real-time-transparency', 1, 'Live holdings, statements and tax reports are always available, which reduces investor queries. Consistent, timely information builds confidence in your fund.')
rw('real-time-transparency', 2, 'Fully branded to your fund.')
rw('real-time-transparency', 3, 'Every transaction updates a single register at the point of settlement. Your team, investor portal, statements and tax reports all draw on that one record.')
rw('real-time-transparency', 4, 'Assess your readiness.')
rw('real-time-transparency', 5, 'The assessment is free, and results are delivered by email.')

rw('always-on', 0, 'Your fund operates without market hours or cut-offs. Enable investors to view, subscribe, transfer and settle at any time, on any device, with your rules applied to every transaction.')
rw('always-on', 1, 'Service that meets institutional expectations.')
rw('always-on', 2, 'Most funds operate on domestic business hours, so subscriptions received after the cut-off are processed the next working day. Offshore applications must wait for the next local processing cycle.')
rw('always-on', 3, 'Applications and settlements are processed across time zones, without waiting for the next domestic business day.')
rw('always-on', 4, "Tokeniser processes subscriptions, transfers and distributions continuously, as they are received. Each transaction is checked against your fund's rules first.")
rw('always-on', 5, 'The case for tokenisation now')
rw('always-on', 6, 'Three briefs covering the commercial case for tokenisation, the current opportunity in Australia, and the cost of delay.')

rw('instant-settlement', 0, 'Every subscription, redemption and transfer remains unsettled for two business days in listed funds, and often longer in private assets. During this period, capital cannot be used by investors or deployed by your fund.')
rw('instant-settlement', 1, 'Subscriptions settle on receipt, so capital is available to invest immediately and cash drag is removed.')
rw('instant-settlement', 2, 'When the trade and the register update together, reconciliation is no longer required and settlement breaks are reduced.')
rw('instant-settlement', 3, 'Today, cash and units move separately, and records are updated days later. On Tokeniser, cash and units are exchanged in a single step and the register updates simultaneously, or the transaction does not proceed.')

rw('automated-compliance', 0, "Eligibility is built into every asset and transaction, so each trade is checked against your fund's rules before execution.")
rw('automated-compliance', 1, 'Trades that breach your rules cannot proceed, and every check is recorded for audit.')
rw('automated-compliance', 2, "Before any trade proceeds, the investor's identity, eligibility (including wholesale or sophisticated status where required) and your limits are verified automatically. Trades that fail a check do not proceed, and every check is logged.")

rw('overview', 0, 'Offer liquidity while retaining capital')
rw('overview', 1, 'Enable investors to borrow against their holdings or exit between redemption windows, while capital remains in your fund. Continuous pricing and 24/7 settlement change how your asset is valued.')
rw('overview', 2, 'Tokeniser makes protocol finance accessible, credible and practical for asset issuers.', add_tone=False)
rw('overview', 3, 'Migrate your existing registry and move holders in stages, from centralised custody to self-custody. Technology and back-office changes can proceed independently.')
rw('overview', 4, 'Speak with our team about your path to tokenisation.')

rw('distribution', 0, 'Your investors transact directly with you, with other investors or with protocols, with instant T+0 settlement.')
rw('distribution', 1, 'Reconciliation across siloed systems is no longer required. Provide investors with a single view of your asset, including its live status and governing rules.')
rw('distribution', 2, 'Enable investors to hold their positions directly. Fewer intermediaries between your asset and its holders reduces cost and increases control.')
rw('distribution', 3, 'Provide investors with live visibility of their holdings and the rules that govern them.')
rw('distribution', 4, 'Traditional channels add cost through multiple layers of intermediaries. Protocol finance removes these layers and connects your asset directly to investors through AI-driven networks.')
rw('distribution', 5, 'Launch a mobile-first investor portal configured to your brand, requirements and fund structure. Introduce further protocol finance capabilities as your asset matures.')
rw('distribution', 6, "The portal carries your fund's name and branding.")
rw('distribution', 7, f'Investors increasingly expect mobile access, so your asset is available to them at any time. {A}')
rw('distribution', 8, 'Develop your own investor experience using our registry APIs.')

rw('liquidity', 0, 'Enable investors to borrow against their units in real time')
rw('liquidity', 1, 'Enable investors to trade at any time, without waiting for a redemption window.')
rw('liquidity', 2, 'Enable investors to access liquidity without exiting their position.')
rw('liquidity', 3, 'Investors can exit only at scheduled redemption windows. Capital remains idle between dates.')
rw('liquidity', 4, 'Enable investors to pledge units as collateral at any time, accessing liquidity without redemption while capital remains in your fund.')
rw('liquidity', 5, 'Investor liquidity without redemptions')
rw('liquidity', 6, 'Enable investors to trade their holdings at any time, without waiting for a redemption window.')
rw('liquidity', 7, 'Enable investors to borrow against their holdings while capital remains in your fund.')
rw('liquidity', 9, "Protocol finance enables you to publish an asset's rules on a public blockchain. You can then offer new liquidity options without intermediary fees, lowering your cost of capital from day one.")
rw('liquidity', 10, "Enable investors to enter and exit positions at any time, within controls you configure for your fund's structure.")
rw('liquidity', 11, 'Collateral, available at any time')

rw('efficiency', 0, 'Subscriptions, redemptions and distributions settle instantly in a single step, without idle cash or mismatched records.')

rw('getting-started', 0, 'Adopt tokenisation in stages, without changing your back office all at once. Our practitioners tailor the implementation to your firm.')
rw('getting-started', 1, 'Identifying where to begin with tokenisation can be complex. Tokeniser provides a clear, guided path that you adopt at your own pace.')
rw('getting-started', 2, 'A modern registry with familiar workflows and protocol finance capabilities built in.')
rw('getting-started', 3, 'Update your investor experience without overhauling internal processes all at once.')
rw('getting-started', 4, 'Access <a href="/product/distribution">lower-cost capital</a>, <a href="/product/liquidity">24/7 liquidity</a> and <a href="/product/superpowers/collateral-mobility">leverage in place</a>, adopted in stages.')
rw('getting-started', 5, 'Detailed documentation guides your team through each phase of adoption.')
rw('getting-started', 6, 'Support is most intensive at the outset and reduces as your team builds confidence.')
rw('getting-started', 7, 'Your back-office compliance involves many moving parts that must be upgraded to realise the benefits of protocol finance. Below are our recommended steps, from setup to secondary trading.')
rw('getting-started', 8, 'Begin with our investor portal, then establish bilateral or protocol distribution agreements to broaden your reach. <a href="/product/distribution">See Distribution →</a>')

# Replace "Let investors" phrasing in why-text that quotes the old after.
for p in d['pages']:
    for c in p['changes']:
        c['why'] = c['why'].replace('("Let investors…", "Give investors…")', '("Enable investors…")')

# ---- New tone cards for casual live lines ----
def add(pid, section, before, after, why, rules=('tone',), tier='style', **kw):
    P[pid]['changes'].append(dict(section=section, before=before, after=after, tier=tier, rules=list(rules), why=why, **kw))

T = 'Casual phrasing. The rewrite uses measured, precise financial language.'

add('collateral-mobility', 'Hero · subtitle',
    'Give your investors a way to raise cash without leaving your fund. Their units become collateral in minutes, and your fund keeps the capital.',
    'Give your investors access to liquidity without leaving your fund. Their units can be pledged as collateral in minutes, and your fund retains the capital.',
    '"Raise cash" and "keeps the capital" are conversational. "Liquidity" and "retains" are the terms an institutional reader expects.')
add('collateral-mobility', 'The problem today · H2', 'Cash needed, fund redeemed', 'Liquidity needs lead to redemptions', T)
add('collateral-mobility', 'What changes · H3', 'Easier to raise into.', 'Stronger capital raising.', '"Raise into" is industry slang. The rewrite names the outcome plainly.')
add('collateral-mobility', 'What changes · H3', 'An investor-first fund.', 'A competitive differentiator.', 'Names the issuer benefit, which the body describes.')
add('collateral-mobility', 'What changes · An investor-first fund · body',
    'Very few private funds let investors borrow against their units without redeeming. Offer it, and your fund has an edge when investors compare their options.',
    'Few private funds allow investors to borrow against their units without redeeming. Offering it differentiates your fund when investors compare options.', T)
add('collateral-mobility', 'Get ready now · H2', 'Set up today, switch on when you are ready', 'Prepare now, activate when ready', T)

add('secondary-transfer', 'What changes · H3', 'Easier to raise into.', 'Stronger capital raising.', '"Raise into" is industry slang. The rewrite names the outcome plainly.')
add('secondary-transfer', 'What changes · Easier to raise into · body',
    'Investors commit more readily when they know there is a way out. A clear exit path removes one of the biggest objections to a private fund, and helps you grow AUM.',
    'Investors commit more readily when an exit path is available. This addresses a common objection to private funds and supports AUM growth.', T)
add('secondary-transfer', 'What changes · H3', 'A liquidity edge.', 'A structural advantage.', T)
add('secondary-transfer', 'What changes · A liquidity edge · body',
    'Liquidity between windows is rare in private markets. Offering secondary transfers gives your fund a structural advantage that traditional operators cannot easily match.',
    'Liquidity between redemption windows is uncommon in private markets. Offering secondary transfers differentiates your fund from traditional operators.', T)
add('secondary-transfer', 'Get ready now · H2', 'Set up today, switch on when you are ready', 'Prepare now, activate when ready', T)

add('real-time-transparency', 'Hero · subtitle',
    'One portal, live holdings, in your brand. Your register updates itself with every trade, and your investors see the change the moment it happens.',
    'A single branded portal with live holdings. Your register updates with every trade, and investors see each change immediately.', T)
add('real-time-transparency', 'The problem today · H2', 'Spreadsheets, reconciliations and quarter-end guesswork',
    'Manual reconciliation<br />and delayed reporting', '"Guesswork" is informal. The rewrite names the operational problem.')
add('real-time-transparency', 'The problem today · body',
    'Most fund registers are updated after the fact, across several systems that have to be reconciled by hand. Investors wait for statements, call when something looks wrong, and rarely see an accurate picture between reporting dates.',
    'Most fund registers are updated after the fact, across several systems that require manual reconciliation. Between reporting dates, investors rarely have an accurate view of their holdings.', T)
add('real-time-transparency', 'What changes · H3', 'A lighter back office.', 'Lower operating overhead.', T)
add('real-time-transparency', 'What changes · A lighter back office · body',
    'Subscriptions, redemptions, transfers and distributions update the register as they happen. There is nothing to reconcile, and the spreadsheet can be retired.',
    'Subscriptions, redemptions, transfers and distributions update the register as they occur. Manual reconciliation and spreadsheets are no longer required.', T)
add('real-time-transparency', 'What changes · H3', 'Investors who trust you more.', 'Greater investor confidence.', T)
add('real-time-transparency', 'What changes · Your brand · body',
    'The investor portal carries your name and your look, on any device. Every time investors log in, they are reminded of your fund.',
    "The investor portal carries your fund's name and branding on every device. Each login reinforces your relationship with investors.", T)

add('always-on', 'The problem today · H2', 'Closed nights, weekends and public holidays', 'Constrained by local business hours', T)
add('always-on', 'What changes · A global investor base · body',
    'Your fund is open when your investors are, including those offshore, in their own time zone. That gives an Australian fund a real edge in winning international capital and growing AUM.',
    'Your fund is accessible to investors in every time zone, including offshore. This positions an Australian fund to attract international capital and grow AUM.', T)
add('always-on', 'What changes · H3', 'Processing without friction.', 'Continuous processing.', T)
add('always-on', 'What changes · Service · body',
    'Holdings, statements and transactions are available any time, on any device. Sophisticated investors notice a fund that matches their institutional pace.',
    'Holdings, statements and transactions are available at any time, on any device. This meets the service expectations of sophisticated investors.', T)
add('always-on', 'How it works · H2', 'Built on infrastructure that never closes', 'Built on infrastructure<br />that operates continuously', '"Never closes" is informal. "Operates continuously" is precise.')

add('instant-settlement', 'Hero · H1', 'Settlement that is already done.', 'Settlement, <em>at the point of trade.</em>', T)
add('instant-settlement', 'Hero · subtitle',
    'T+2 becomes T+0. The capital tied up waiting for trades to settle goes back to work the moment a trade is struck.',
    'Move from T+2 to T+0 settlement. Capital that would await settlement is available the moment a trade is executed.', T)
add('instant-settlement', 'The problem today · H2', 'Two days of waiting, on every trade', 'Two-day settlement on every trade', T)
add('instant-settlement', 'The problem today · statistic',
    'At a 5% cost of capital, a $1b fund pays roughly $274,000 a year just to wait two days.',
    'At a 5% cost of capital, a $1b fund incurs roughly $274,000 a year from a two-day settlement delay.', '"Just to wait" is conversational. The figure is unchanged.')
add('instant-settlement', 'What changes · H3', 'Capital back to work.', 'Capital deployed sooner.', T)
add('instant-settlement', 'What changes · H3', 'A fund investors choose.', 'Meeting investor expectations.', T)
add('instant-settlement', 'What changes · A fund investors choose · body',
    'Instant settlement is fast becoming the standard investors compare against. Be the fund that already offers it, and win the allocations that follow.',
    'Instant settlement is becoming the benchmark investors use to compare funds. Offering it now positions your fund to win allocations.', T)
add('instant-settlement', 'What changes · H3', 'A lighter back office.', 'Lower operating overhead.', T)

add('automated-compliance', 'Hero · H1', 'Rules that cannot be skipped.', 'Compliance, <em>enforced on every trade.</em>', T)
add('automated-compliance', 'The problem today · H2', 'Checked by hand, caught too late', 'Manual checks and late detection', T)
add('automated-compliance', 'The problem today · body',
    'Investor eligibility, holder limits and transfer restrictions are usually managed across spreadsheets, emails and manual sign-offs. Checks take time, and when something slips through, it is found after the trade, when fixing it is slow and costly.',
    'Investor eligibility, holder limits and transfer restrictions are typically managed through spreadsheets, emails and manual sign-offs. Breaches are often identified after the trade, when remediation is slow and costly.', T)
add('automated-compliance', 'What changes · Lower compliance cost · body',
    'Checks run automatically on every trade, so your team spends less time checking and fixing.',
    'Checks run automatically on every trade, reducing the time your team spends on review and remediation.', T)
add('automated-compliance', 'What changes · H3', 'Room to grow.', 'Scalable operations.', T)
add('automated-compliance', 'What changes · Room to grow · body',
    'Take on more investors and more transactions without adding compliance headcount. Your rules scale with your fund.',
    'Grow your investor base and transaction volumes without adding compliance headcount.', T)

add('overview', 'Hero · subtitle',
    'All you need from a registry, with a powerful protocol finance unlock. End-to-end management of funds, equities, loans and notes.',
    'A complete registry, with protocol finance capabilities built in. End-to-end management of funds, equities, loans and notes.', '"A powerful protocol finance unlock" is marketing slang.')
add('overview', 'Why this matters · H2', 'Ingredients for differentiation and real growth', 'The foundations for differentiation and growth', T)
add('overview', 'Getting started · body',
    'Tokeniser decouples your IT infrastructure from your back-office workflows, so each can transform at its own pace. Our practitioners guide you through each stage, keeping risk low and momentum steady.',
    'Tokeniser separates your IT infrastructure from your back-office workflows, so each can change at its own pace. Our practitioners guide you through each stage to manage risk and maintain progress.', T)

add('distribution', 'Hero · subtitle',
    'Replace high-cost channels with direct reach that lowers your cost of capital, while unlocking new global markets through compliant rails.',
    'Replace high-cost channels with direct investor access that lowers your cost of capital and opens new global markets through compliant infrastructure.', T)
add('distribution', 'Benefits · Custody · H3', 'Investor custody cuts out intermediaries', 'Direct investor custody', T)

add('liquidity', 'Hero · subtitle',
    'Unlock secondary liquidity, collateralisation, and atomic settlement for your assets under your existing regulatory licence.',
    'Offer secondary liquidity, collateralisation and atomic settlement for your assets under your existing regulatory licence.', T)
add('liquidity', 'Trade · H2', 'Markets on demand', 'Continuous market access', T)
add('liquidity', 'Custody · H2', 'Go direct', 'Direct investor custody', T)

add('efficiency', 'Getting Started · H2', 'Efficiency without a big-bang project', 'Efficiency without a large-scale transformation', T)
add('efficiency', 'Impact Calculator · H2', 'Take the drag out of your back office.', 'Reduce cost across your <span>back office.</span>', T)

add('getting-started', 'Adoption · H2', 'A journey you control', 'A phased approach you control', T)
add('getting-started', 'Adoption · Full potential · H3', 'Arrive at sophisticated protocol finance value', 'Realise the full value of protocol finance', T, tab='Full potential')
add('getting-started', 'Guidance · body', 'Tokeniser brings seasoned practitioners who coach you through each stage.',
    'Experienced practitioners support your team through each stage.', T)
add('getting-started', 'Guidance · Stage two',
    'When questions arise you get answers from practitioners who have solved these problems before.',
    'When questions arise, your team receives answers from practitioners with direct experience.', T)
add('getting-started', 'Journey · Initial state · body',
    'Adopt Tokeniser from the situation you are in, an existing registry service, spreadsheets, or a greenfield feeder fund, to get started easily.',
    'Adopt Tokeniser from your current position, whether an existing registry service, spreadsheets or a greenfield feeder fund.', T)
add('getting-started', 'Journey · Initial state · body (2)',
    'Operate with a shadow-registry for pre-migration, or dive in with your company or a fully digitised feeder fund to launch straight into the opportunity.',
    'Operate a shadow registry ahead of migration, or begin directly with your company or a fully digitised feeder fund.', '"Dive in" and "launch straight into the opportunity" are informal.')
add('getting-started', 'Journey · Prepare compliance',
    'Explore compliance with the new AML/KYC paradigm, and design new processes to suit. See how Automated Compliance works →',
    'Review your compliance approach under the new AML/KYC model, and design processes to suit. <a href="/product/superpowers/automated-compliance">See how Automated Compliance works →</a>', T)
add('getting-started', 'Journey · Digitised feeder fund',
    'For a simple start, create a digitised feeder fund in days, bypassing legacy challenges.',
    'For a straightforward start, establish a digitised feeder fund in days, without legacy constraints.', T)

for p in d['pages']:
    for c in p['changes']:
        c.pop('shotBefore', None); c.pop('shotAfter', None)
json.dump(d, open(f, 'w'), indent=2, ensure_ascii=False)
open(f, 'a').write('\n')
print(sum(len(p['changes']) for p in d['pages']))
