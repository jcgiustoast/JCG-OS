# JC OS — Juan Cruz's Personal Operating System

> This is the root schema. Claude reads this file automatically at session start. It routes between two spaces and defines shared rules.

## About Juan Cruz
- **Based in:** Madrid, Spain (originally from Argentina)
- **Role:** Head of eCommerce at Mars Men (mengotomars.com)
- **Email:** juan@mengotomars.com
- **Reports to:** Raheel (Head of Growth — owns creatives + ad spend)
- **Works with:** Zach Stuck (Co-founder/Growth), Benjamin Smith (Co-founder/Brand)
- **Time zone:** CET/CEST — company is US-based, Juan works across time zones
- **Languages:** Spanish (native), English (professional)

## Two Spaces

JC OS is split into two spaces. Read the relevant index before drilling into pages.

### life/ — Professional & Personal
Career, role, team, projects, learning, goals, finances, personal development. Everything about who Juan is and what he's building.

- **Index:** `life/wiki/index.md`
- **Wiki:** `life/wiki/` — identity, professional context, projects, learning tracks
- **Raw:** `life/raw/` — articles, notes, screenshots, data
- **Memory:** `life/memory/` — log and compiled knowledge

### content/ — Content & Exploration
Ideas for content Juan wants to create, topics to explore, research for articles/posts/videos, drafts, references. The creative workshop.

- **Index:** `content/wiki/index.md`
- **Wiki:** `content/wiki/` — topic pages, content ideas, research
- **Raw:** `content/raw/` — reference articles, inspiration, drafts
- **Memory:** `content/memory/` — log of content activity

## Architecture

```
JCG-OS/
├── CLAUDE.md                # This file — root schema
├── life/                    # Space 1: Professional & Personal
│   ├── wiki/
│   │   ├── life-index.md    #   Master catalog for life/
│   │   ├── identity.md      #   Who Juan is
│   │   ├── professional.md  #   Mars Men context, role, team
│   │   ├── projects.md      #   Personal/side projects
│   │   ├── strategy.md      #   1-5 year plan, financial targets
│   │   └── learning.md      #   Active learning tracks
│   ├── raw/                 #   Immutable sources
│   │   ├── articles/
│   │   ├── notes/
│   │   ├── screenshots/
│   │   └── data/
│   └── memory/
│       ├── log.md           #   Chronological activity log
│       └── wiki.md          #   Compiled knowledge topics
├── content/                 # Space 2: Content & Exploration
│   ├── wiki/
│   │   ├── content-index.md  #   Master catalog for content/
│   │   ├── content-strategy.md # Phased content plan (bridges both spaces)
│   │   └── ...              #   Topic pages, content ideas
│   ├── raw/
│   │   ├── articles/        #   Reference material
│   │   ├── references/      #   Inspiration, examples
│   │   └── drafts/          #   Work-in-progress drafts
│   └── memory/
│       └── log.md           #   Content activity log
├── SETUP.md
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
2. **Determine which space.** Is the conversation about life/career/learning or about content/exploration? Route accordingly.
3. **Check the index.** Read the relevant index — `life/wiki/life-index.md` or `content/wiki/content-index.md` — to find pages. Scan descriptions, only open what's needed.
4. **Read frontmatter first.** Every wiki page has YAML frontmatter with a description. Read ONLY the description to decide if you need the full file.
5. **Cross-reference between spaces.** Content ideas often draw from professional knowledge. Use `[[life/wiki/page]]` or `[[content/wiki/page]]` to link across spaces.
6. **Keep raw/ immutable.** Read from `raw/` but NEVER modify files there.

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

## Authorship Rule (CRITICAL)

Every wiki page declares an `author` in frontmatter:

- **`author: juan`** — Juan's own notes, thinking, voice. Claude **must not create or edit** these pages. Claude may only propose changes in chat; Juan writes them himself. The only exceptions: (a) Juan explicitly says "write this to [page]" or "edit [page]", or (b) mechanical updates to the `updated:` date after Juan-approved edits.
- **`author: claude`** — Summaries, source compilations, ingested material, comparison tables. Claude creates and maintains these freely (still with Juan's approval per the Update Protocol).

Default for new pages: if Juan is the one thinking out loud, it's `author: juan`. If Claude is compiling from `raw/` or from logs, it's `author: claude`.

`memory/` files (logs, compiled wiki) are always Claude-authored. `raw/` is immutable regardless of author.

## Session Protocols

### Morning Briefing
When Juan says "morning briefing" or "what's on my plate":
1. Read both `life/wiki/index.md` and `content/wiki/index.md`
2. Read `life/wiki/professional.md` and `life/wiki/projects.md` for priorities
3. Read `life/memory/log.md` and `content/memory/log.md` for recent entries
4. Surface: today's priorities + context, what changed since last session
5. Flag stale entries, open decisions, or "to be filled" sections

### Ingest Workflow
When Juan says "ingest [filename]":
1. Read the source file in the relevant `raw/` folder
2. Discuss key takeaways with Juan
3. Create or update relevant wiki pages (a single source might touch 5-15 pages across both spaces)
4. Update the relevant `wiki/index.md`
5. Append structured entry to the relevant `memory/log.md`

### Query Workflow
When Juan asks a question:
1. Read the relevant `wiki/index.md` to find pages (check both spaces if topic spans them)
2. Read those pages
3. Synthesize answer citing wiki pages as `[[page-name]]`
4. Answers can take different forms — markdown page, comparison table, chart, structured analysis. Pick the format that fits.
5. **Good answers should be filed back into the wiki.** Offer to file them. Explorations compound just like ingested sources.

### Lint Workflow
When Juan says "lint" or "health check":
1. Scan for contradictions between pages
2. Find orphan pages (no inbound links)
3. List concepts mentioned 3+ times without their own page
4. Check for stale claims or "to be filled" placeholders
5. Suggest questions to investigate or sources to ingest next
6. Append lint results to the relevant `memory/log.md`

### Compile Workflow
When Juan says "compile":
1. Read recent `memory/log.md` entries from both spaces
2. Extract recurring patterns, themes, or insights
3. Create or update topic pages in `memory/wiki.md`
4. Cross-link with relevant wiki pages

### Update Protocol
- **After a conversation:** Claude summarizes what changed -> Juan approves -> Claude writes with today's date
- **Weekly lint:** Juan can ask Claude to review the whole system
- **Compile cycle:** Claude reads logs and compiles patterns into knowledge pages

## Slash Commands

Custom commands live in `.claude/commands/`. Each is a markdown prompt invoked by filename. All are READ-ONLY unless noted.

| Command | Purpose |
|---------|---------|
| `/context` | Load full state — active projects, priorities, last 7 days of logs |
| `/today` | Prioritized plan for today from recent logs + stated priorities |
| `/closeday` | End-of-day recap; writes to `memory/log.md` after approval |
| `/trace <topic>` | Timeline of how an idea evolved across the vault |
| `/connect <A> \| <B>` | Find connections between two topics via link graph |
| `/ghost <question>` | Draft a response in Juan's voice from stated beliefs |
| `/challenge <topic>` | Pressure-test positions — contradictions, weak assumptions |
| `/ideas` | Generate tools/people/topics/writing ideas grounded in the vault |
| `/graduate` | Promote log asides to standalone pages; writes after approval |
| `/drift` | Surface recurring patterns Juan hasn't labeled yet |
| `/emerge` | Clusters ready to become a project, essay, or product |
| `/schedule` | Map stated priorities to a suggested weekly shape |

Only `/closeday` and `/graduate` write files, and both require explicit approval before doing so.

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
- Commit messages: `update life/professional.md — added Q2 goals`
- Never force push. Never amend without asking.
