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

## Authorship Rule (CRITICAL)

Every wiki page declares an `author` in frontmatter:

- **`author: juan`** — Juan's own notes, thinking, voice. Claude **must not create or edit** these pages. Claude may only propose changes in chat; Juan writes them himself. The only exceptions: (a) Juan explicitly says "write this to [page]" or "edit [page]", or (b) mechanical updates to the `updated:` date after Juan-approved edits.
- **`author: claude`** — Summaries, source compilations, ingested material, comparison tables. Claude creates and maintains these freely (still with Juan's approval per the Update Protocol).

Default for new pages: if Juan is the one thinking out loud, it's `author: juan`. If Claude is compiling from `raw/` or from logs, it's `author: claude`.

`memory/` files (logs, compiled wiki) are always Claude-authored. `raw/` is immutable regardless of author.

## Hard Rules
1. Read this CLAUDE.md first, then the relevant `wiki/index.md` before opening pages.
2. `raw/` is immutable — read from it but NEVER modify files there.
3. Never create or edit `author: juan` pages, except (a) Juan explicitly says "write this to [page]" / "edit [page]", or (b) mechanical `updated:` date bumps after Juan-approved edits.
4. Claude proposes; Juan confirms. Never overwrite or write files without approval.
5. Every file carries a date — set `updated:` to today on every write.
6. State over history: files reflect current reality first; changelogs at the bottom track evolution.
7. Only `/closeday`, `/graduate`, and `/process-inbox` write files, and all require explicit approval first. All other slash commands are READ-ONLY.
8. Good answers get filed back into the wiki — offer to file them.
9. Think critically: push back when needed, reason from first principles, say so if unsure.
10. After updating files, ask Juan if he wants to commit. Never force push. Never amend without asking.

## Git Protocol
- After updating files, ask Juan if he wants to commit
- Commit messages: `update life/professional.md — added Q2 goals`
- Never force push. Never amend without asking.

## Detailed guides
@.claude/architecture.md
@.claude/conventions.md
@.claude/workflows.md
@.claude/slash-commands.md
