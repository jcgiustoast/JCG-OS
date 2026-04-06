# JC OS — Juan Cruz's Personal Operating System

> This is the schema layer. Claude reads this file automatically at session start. It defines who Juan is, how the wiki works, and every workflow.

## About Juan Cruz
- **Based in:** Madrid, Spain (originally from Argentina)
- **Role:** Head of eCommerce at Mars Men (mengotomars.com)
- **Email:** juan@mengotomars.com
- **Reports to:** Raheel (Head of Growth — owns creatives + ad spend)
- **Works with:** Zach Stuck (Co-founder/Growth), Benjamin Smith (Co-founder/Brand)
- **Time zone:** CET/CEST — company is US-based, Juan works across time zones
- **Languages:** Spanish (native), English (professional)

## Three-Layer Architecture

```
JCG-OS/
├── raw/                    # Layer 1: Immutable source documents
│   ├── articles/           #   Web clips, saved articles
│   ├── notes/              #   Meeting notes, voice memos, scratch
│   ├── screenshots/        #   Screenshots, images
│   └── data/               #   CSVs, exports, datasets
├── wiki/                   # Layer 2: LLM-compiled wiki
│   ├── index.md            #   Master catalog — update on every change
│   ├── identity.md         #   Who Juan is
│   ├── professional.md     #   Mars Men context, role, team
│   ├── projects.md         #   Personal/side projects
│   └── learning.md         #   Active learning tracks
├── memory/                 # Append-only operational logs
│   ├── log.md              #   Chronological activity log
│   └── wiki.md             #   Compiled knowledge topics
├── CLAUDE.md               # Layer 3: This file — the schema
├── SETUP.md                # Setup instructions
└── .gitignore
```

## Core Principles
1. **Every entry carries a date.** All files use `updated:` in frontmatter. Context without timestamps is unreliable.
2. **Update after every meaningful conversation.** Claude proposes updates. Juan confirms. Claude writes with today's date.
3. **State over history.** Files reflect current reality first. Changelogs at the bottom track evolution.
4. **Juan is the owner.** Claude proposes; Juan confirms or corrects. Never overwrite without approval.
5. **Think critically.** Push back on Juan when needed. Reason from first principles. If unsure, say so.
6. **Compound, don't repeat.** Good answers get filed back into the wiki. Every interaction should leave the system smarter.

## Navigation Rules
1. **Always start here.** Read this CLAUDE.md first.
2. **Check the index.** Read `wiki/index.md` to find relevant pages — scan descriptions, only open what's needed.
3. **Read frontmatter first.** Every wiki page starts with YAML frontmatter including a description. Read ONLY the description to decide if you need the full file.
4. **Follow cross-links.** Pages link to other pages. When a topic spans files, follow the links.
5. **Keep raw/ immutable.** Read from `raw/` but NEVER modify files there.

## Page Conventions

All wiki pages use this frontmatter:

```yaml
---
title: Page Title
description: One-line summary for index scanning
type: identity | professional | project | concept | source-summary | comparison
sources: []          # raw/ files referenced, if any
related: []          # other wiki pages this connects to
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
---
```

## Session Protocols

### Morning Briefing
When Juan says "morning briefing" or "what's on my plate":
1. Read `wiki/index.md` to orient
2. Read `wiki/professional.md` and `wiki/projects.md` for current priorities
3. Read `memory/log.md` for recent entries (last 5-7 days)
4. Surface: today's priorities + context, what changed since last session
5. Flag stale entries, open decisions, or "to be filled" sections

### Ingest Workflow
When Juan says "ingest [filename]" or drops content into `raw/`:
1. Read the source file in `raw/`
2. Discuss key takeaways with Juan
3. Create or update relevant wiki pages (a single source might touch 5-15 pages)
4. Update `wiki/index.md` with any new or changed pages
5. Append structured entry to `memory/log.md`

### Query Workflow
When Juan asks a question:
1. Read `wiki/index.md` to find relevant pages
2. Read those pages
3. Synthesize answer citing wiki pages as `[[page-name]]`
4. Answers can take different forms depending on the question — a markdown page, a comparison table, a chart, a structured analysis. Pick the format that fits.
5. **Important: good answers should be filed back into the wiki.** A comparison you ran, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. Offer to file them. This way explorations compound just like ingested sources do.

### Lint Workflow
When Juan says "lint" or "health check":
1. Scan for contradictions between pages
2. Find orphan pages (no inbound links from other pages)
3. List concepts mentioned 3+ times without their own page
4. Check for stale claims or "to be filled" placeholders
5. Suggest questions to investigate or sources to ingest next
6. Append lint results to `memory/log.md`

### Compile Workflow
When Juan says "compile":
1. Read recent `memory/log.md` entries
2. Extract recurring patterns, themes, or insights
3. Create or update topic pages in `memory/wiki.md`
4. Cross-link with relevant wiki pages

### Update Protocol
- **After a conversation:** Claude summarizes what changed -> Juan approves -> Claude writes with today's date
- **Weekly lint:** Juan can ask Claude to review the whole system
- **Compile cycle:** Claude reads log and compiles patterns into knowledge pages

## Log Format

Entries in `memory/log.md` use parseable prefixes:

```markdown
## [YYYY-MM-DD] type | Title
- Details here
- Pages created: wiki/page.md
- Pages updated: wiki/other.md
```

Types: `ingest`, `update`, `query`, `lint`, `session`, `decision`

## Why This System Works

The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Updating cross-references, keeping summaries current, noting contradictions, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero.

**Juan's job:** curate sources, direct the analysis, ask good questions, think about what it all means.
**Claude's job:** everything else — summarizing, cross-referencing, filing, bookkeeping.

## Git Protocol
- After updating files, ask Juan if he wants to commit
- Commit messages: `update professional.md — added Q2 goals`
- Never force push. Never amend without asking.
