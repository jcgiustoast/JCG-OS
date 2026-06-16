## Page Conventions

All wiki pages use this frontmatter:

```yaml
---
title: Page Title
description: One-line summary for index scanning
type: identity | professional | project | concept | source-summary | comparison | content-idea | topic
author: juan | claude   # who owns the page
sources: []          # raw/ files referenced, if any
related: []          # other wiki pages this connects to
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
---
```

## Mobile & Desktop Capture

Ideas captured on phone (Telegram bot) or desktop (Obsidian, Telegram Desktop) land in `life/raw/inbox/`:
- `YYYY-MM-DD.md` — Telegram bot appends text + Whisper-transcribed voice notes here
- Any other `.md` file dropped into `inbox/` (e.g. from Obsidian) is also picked up
- Voice `.ogg` and photo `.jpg` files are saved alongside and referenced inline

Run `/process-inbox` to triage. Bot source: `.telegram-inbox/` (auto-starts on Windows login).

## Log Format

Entries in `memory/log.md` use parseable prefixes:

```markdown
## [YYYY-MM-DD] type | Title
- Details here
- Pages created: wiki/page.md
- Pages updated: wiki/other.md
```

Types: `ingest`, `update`, `query`, `lint`, `session`, `decision`
