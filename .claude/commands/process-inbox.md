---
description: Review the Telegram inbox, file entries into the wiki, then clear the inbox
---

# /process-inbox

Process pending captures from the Telegram bot.

## Steps

1. **Read** every file in `life/raw/inbox/` (daily markdown files + referenced audio/images).
2. **Group** entries by theme — tasks, ideas, facts about Juan/work, content ideas, references.
3. **For each entry**, propose one of:
   - File into an existing wiki page (cite which)
   - Create a new wiki page (follow frontmatter conventions + authorship rule)
   - Log-only (append to the relevant `memory/log.md`)
   - Drop (trivial, already captured)
4. **Show Juan the full proposal** as a table: entry → destination → action. Wait for approval. Do NOT write anything yet.
5. **After approval**: apply writes, then move processed daily inbox files to `life/raw/inbox/processed/` (preserving audio/image files so links stay valid). Never delete — archive.
6. **Commit** the result if Juan approves.

## Rules

- Respect `author: juan` pages — propose edits, do not write them yourself unless Juan says so.
- Voice transcripts may be messy — clean them up when filing, keep the raw line in the inbox archive.
- If an entry is ambiguous, ask Juan before filing.
- If the inbox is empty, say so and stop.