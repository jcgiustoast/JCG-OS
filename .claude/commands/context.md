---
description: Load Juan's full life + work state — active projects, priorities, recent reflections
---

You are loading session context from JCG-OS so the rest of this conversation is grounded in who Juan is, what he's working on, and what's on his mind right now. This command is READ-ONLY — do not modify any files.

Today is {{date}}. "Last 7 days" means entries dated within 7 calendar days of today.

## Steps

1. **Reaffirm the schema.** Re-read `CLAUDE.md` at the vault root. It tells you how the two spaces (`life/`, `content/`) are organized and what conventions apply.

2. **Scan both indexes — descriptions only.** Read `life/wiki/life-index.md` and `content/wiki/content-index.md`. Do NOT open every page they list. Just read each page's frontmatter `description:` line to get the shape of what exists. If an index is missing or sparse, note it as a gap.

3. **Open the priority pages in `life/wiki/`** (full read):
   - `identity.md` — who Juan is
   - `professional.md` — Mars Men role, team, current work
   - `projects.md` — personal/side projects
   - `strategy.md` — 1-5 year plan, financial targets
   - `learning.md` — active learning tracks

   If any of these don't exist or contain "to be filled" placeholders, note that as an open thread rather than failing.

4. **Read recent log entries.** Open `life/memory/log.md` and `content/memory/log.md`. Entries are prefixed `## [YYYY-MM-DD] type | Title`. Extract only entries dated within the last 7 days. If a log is empty or has no recent entries, say so.

5. **Synthesize the briefing.** Produce a scannable report under ~400 words with these exact sections:

   - **Who Juan is right now** — 2-3 lines, role + current focus.
   - **Active projects** — bullet list, one-line status per project. Pull from `projects.md` and any project-type entries in recent logs.
   - **Priorities this week** — extracted from recent log entries + anything flagged current in `professional.md`. If priorities aren't stated, say "not explicitly recorded — worth asking."
   - **Recent reflections / decisions** — bullets from log entries in the last 7 days (types: `decision`, `query`, `session`, `update`).
   - **Open threads** — unfinished items, stale entries, "to be filled" placeholders you noticed, missing pages referenced by others.

6. **End with:** `Ready. What do you want to work on?`

## Rules

- Cite wiki pages inline using the vault's convention: `[[life/wiki/projects]]`, `[[content/wiki/index]]`, etc.
- Do not write, edit, or commit any files. This command is purely for loading context.
- Do not read `raw/` folders — they're source material, not state.
- If a file referenced above doesn't exist, report it as a gap in Open threads. Don't guess at contents.
- Keep the output tight. Juan reads this at the start of a session — every extra word is tax.
