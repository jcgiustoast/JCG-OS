---
description: Find unexpected connections between two topics using the vault's link graph
argument-hint: <topic A> | <topic B>
---

Bridge two domains using JCG-OS's link graph. READ-ONLY.

Input: **$ARGUMENTS** (expected format: `topic A | topic B`)

If input is missing or malformed, ask Juan for both topics and stop.

## Steps

1. For each topic, Grep `life/wiki/` and `content/wiki/` to find pages that mention it. Collect the hit pages into set A and set B.
2. Find direct overlap: any page in both A and B. That's the obvious bridge — note it but don't stop there.
3. Walk the `related:` frontmatter arrays. For each page in A, list its related pages. Same for B. Look for:
   - Shared related pages (both sides link to the same third page)
   - Short chains (A → X → B in two hops)
4. Grep both `memory/log.md` files for entries that mention both topics in the same entry — those are moments Juan already connected them.

## Output

- **Direct overlaps** — pages that talk about both, with a sentence on how.
- **Shared neighbors** — third pages that both topics link to. This is often where the real connection lives.
- **Two-hop bridges** — A → middle page → B. List each path with what the middle page contributes.
- **Moments Juan already connected them** — log entries mentioning both.
- **Pattern** — one paragraph: what this connection map suggests. Push a real observation, not a hedge.

## Rules

- Cite every link with `[[page]]`.
- If no real connection exists, say so. Don't manufacture one.
- Keep under ~400 words.
