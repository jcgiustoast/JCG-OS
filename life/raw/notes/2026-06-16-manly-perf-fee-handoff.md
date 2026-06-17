# Handoff — Design the Manly performance fee

> Working handoff note. Created 2026-06-16. Pick up in a fresh session.

## Focus
Manly (men's grooming for teens) has **verbally agreed to close**: full plan at **$9K/mo base + a performance fee**, **6-month commitment**. Base and scope are settled. **The performance fee is the one open commercial term** to design before the contract. Deliver a concrete, contract-ready fee structure **plus a casual client-facing line in Juan's voice**.

## Locked decisions — do not re-litigate
- **Base:** $9K/mo, 6-month commitment. Full plan = LP + full CRO program.
- **Performance fees attach to Paid Media, not CRO/LP** — now `asteroi-rate-card` **principle 8**. CRO/LP stay flat retainers.
- A bespoke CRO attribution model (% of validated incremental margin per shipped experiment) was **considered and dropped** — too noisy to attribute, becomes a monthly invoice fight. Do not revive it.
- Manly's fee must follow the **Paid Media contribution-margin logic** — model off the rate card's `$5K base + 10% of CM` Paid Media section.

## Open questions to resolve
1. **What base does the fee ride on?** Manly is a CRO/LP client but the fee uses paid-media CM logic — clarify with Juan whether the deal includes a media-buying component (clean CM base) or the fee is a CM-share on the whole DTC P&L. **This is the crux and is currently ambiguous.**
2. $9K is already ~2x the paid-media $5K base → if the fee rides on total CM, the **% should likely be below 10%**. Model a few scenarios.
3. Total vs incremental (baseline-relative) CM.
4. CM definition (rev − COGS − variable − ad spend; specify which variable costs) — written in-contract.
5. P&L / data-access requirement; settlement cadence (monthly/quarterly); credit window so wins aren't paid forever.
6. Cap / floor — base protects the floor; keep simple for a first deal.
7. **Tincho dependency** — if a media component is involved it's Tincho-operated, and he's not off 18PM until ~Sept 2026 (same collision as VAHDAM). Factor the ramp.

## Constraints
- Juan is in **stealth phase** (Head of eComm at Mars Men, unaware of ASTEROI). Paid media is his off-limits zone — Tincho must front/run it.
- Parallel deal **VAHDAM** (~$100K/mo, Paid Media $5K + 10% CM) is also closing and also leans on Tincho. Keep both models coherent so neither anchor undercuts the other.

## Reference artifacts (read, don't duplicate)
- `life/wiki/asteroi-rate-card.md` — Paid Media section, principle 8, changelog.
- `life/wiki/projects.md` — Pipeline → Manly entry (negotiation path + open items).
- `life/memory/log.md` — `[2026-06-16] decision` entry.
- Draft PR: https://github.com/jcgiustoast/JCG-OS/pull/7
- Working branch: `claude/manly-proposal-d0b4og`

## Juan's voice
No em-dashes in client copy. Plain and direct, LinkedIn-DM register. Recommendation-first, not a survey.

## Suggested skills for the next session
- `/challenge` — pressure-test the fee structure (esp. total-vs-incremental CM and the data-access ask) before it ships.
- `/ghost` — draft the client-facing line in Juan's voice.
- `/close` — commit + log + PR the resolved terms when done.
