---
description: Extract undeveloped ideas from recent logs and promote them into standalone wiki pages
---

Find half-formed thoughts in logs and propose standalone pages for them. Writes files ONLY after Juan approves each one.

## Steps

1. Read `life/memory/log.md` and `content/memory/log.md`. Extract entries from the last 14 days.
2. Find paragraphs, bullets, or asides that:
   - State a claim, observation, or framework in more than one line
   - Aren't already captured in a wiki page (check both indexes: `life/wiki/life-index.md` and `content/wiki/content-index.md`)
   - Would earn their own page if written up
3. For each candidate, draft a proposal: title, one-line description, which space (life/ or content/), type (concept, topic, project, etc.), and a 2-4 sentence summary of what the page would say.

## Output

- **Candidates** — numbered list. For each:
  - Proposed title
  - Proposed path: `life/wiki/<name>.md` or `content/wiki/<name>.md`
  - One-line description (frontmatter style)
  - Source: which log entry it came from, with date
  - 2-4 sentence summary of the page's core claim
  - Proposed `author:` — `juan` if it's Juan's thinking/voice (most cases), `claude` if it's a compiled summary
  - Related pages it should link to (from frontmatter `related:` arrays)

Then ask: `Which of these should I graduate into real pages? Reply with numbers (e.g. 1,3,5) or "none."`

## On approval

When Juan picks which to graduate:
1. Create each approved file with full frontmatter per `CLAUDE.md` convention: `title`, `description`, `type`, `author`, `sources`, `related`, `created: today`, `updated: today`, `confidence: low` unless otherwise obvious.
2. For `author: juan` pages: write a skeleton — the core claim, sources, and related links — but leave expansion for Juan. Flag clearly that he should own the prose.
3. Update the relevant index (`life/wiki/life-index.md` or `content/wiki/content-index.md`) to add the new entry.
4. Append an entry to the relevant `memory/log.md`:
   ```
   ## [YYYY-MM-DD] update | Graduated N ideas into pages
   - Pages created: wiki/foo.md, wiki/bar.md
   ```
5. Ask Juan if he wants to commit.

## Rules

- Don't create files without explicit approval.
- Don't graduate things already covered by existing pages — check first.
- Respect the authorship rule: `author: juan` pages get skeletons, not full drafts. Juan owns his voice.
- `confidence: low` for anything still speculative. That's fine — compounds later.
