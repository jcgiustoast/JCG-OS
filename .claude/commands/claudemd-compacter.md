---
description: Audit and compact an oversized CLAUDE.md by splitting it into a .claude/ directory of @-imported topic files, archiving historical content, and updating .claudeignore. Two-phase, confirmation-gated.
---

# CLAUDE.md Compacter

Read and follow the full workflow at `~/.claude/skills/claudemd-compacter/SKILL.md`. That file is the source of truth — do not paraphrase or shortcut it.

## Quick summary

CLAUDE.md is loaded into every prompt of every session. Files >10k tokens bloat context and cause Claude to ignore its own instructions. This skill fixes that structurally by moving sometimes-relevant content into `@`-imported topic files and historical content into `.claude/archive/`.

## How to invoke

1. Read `~/.claude/skills/claudemd-compacter/SKILL.md` in full.
2. Default to the CLAUDE.md in the current working directory unless the user names another.
3. Run **Phase 1 (Audit)** end-to-end:
   - `python ~/.claude/skills/claudemd-compacter/scripts/count_tokens.py <path>`
   - Read the file, classify each section into keep-inline / split / archive / delete
   - Present the four-bucket table to the user
   - **Wait for explicit approval**
4. Run **Phase 2 (Execute)** only after approval:
   - Backup `CLAUDE.md` → `CLAUDE.md.backup`
   - Write topic files to `.claude/<topic>.md`
   - Rewrite CLAUDE.md with keep-inline content + `@import` block
   - Move archive content to `.claude/archive/<name>.md`
   - Append `.claude/archive/` to `.claudeignore`
   - Re-measure and report before → after

## Constraints (do not skip)

- Never delete content without explicit user confirmation.
- Always backup before destructive ops.
- Don't touch nested CLAUDE.md files unless asked.
- Don't rewrite or summarize content — this skill restructures, doesn't edit.
- Preserve existing `@imports`.
