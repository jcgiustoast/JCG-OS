---
description: Track how an idea has evolved across the vault — first appearance, evolution, current connections
argument-hint: <topic>
---

Trace the arc of an idea across JCG-OS. READ-ONLY.

Topic: **$ARGUMENTS**

If no topic was provided, ask Juan which idea to trace and stop.

## Steps

1. Search both `life/wiki/` and `content/wiki/` for mentions of the topic (page titles, descriptions, body text). Use Grep.
2. Search both `life/memory/log.md` and `content/memory/log.md` for mentions. Extract the `## [YYYY-MM-DD]` dates.
3. For every page that mentions the topic, read its frontmatter — note `created:`, `updated:`, and `related:` arrays. The `related:` arrays are the vault's equivalent of backlinks.
4. Walk one hop of related pages: for each page that mentions the topic, read the frontmatter description of every page in its `related:` list. Do NOT read full bodies of related pages unless needed to resolve ambiguity.

## Output

A timeline + connection map:

- **First appearance** — earliest date (from log entries or `created:` frontmatter). Quote the line or summarize.
- **Evolution** — chronological bullets: date → what shifted. Pull from log entries (`update`, `decision`, `query` types) and page `updated:` changes.
- **Current state** — what the vault says about this topic today. Which pages carry it. One-paragraph synthesis.
- **Connected to now** — list of pages related to this topic, with one-line descriptions of each link's nature.
- **Gaps** — where the thread goes cold, missing context, or where the idea should have been filed but wasn't.

## Rules

- Cite every claim with `[[page]]` or `log [YYYY-MM-DD]`.
- If the topic barely appears (< 3 hits), say so — don't pad.
- Keep under ~500 words.
