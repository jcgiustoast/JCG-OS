---
title: Notion Content System Design
description: Move the operational layer of Juan's content system (ideas, pipeline, drafts, research) into Notion while keeping the knowledge wiki canonical in local markdown.
type: design-spec
author: claude
created: 2026-05-24
updated: 2026-05-24
status: pending-review
---

# Notion Content System Design

## Context

Juan currently runs his content system entirely from local markdown inside JCG-OS:

- **Knowledge layer** in `content/wiki/`: topic pages (subscription-metrics, ltv-frameworks, etc.), voice nodes (`voice/`), platform nodes (`platforms/`), engine nodes (`engine/`), and 37 ingested raw articles in `content/raw/articles/`.
- **Operational layer** scattered across markdown files: ideas live as bullets in `content-index.md`, the pipeline tracker is `pipeline.md`, drafts are individual `.md` files in `content/raw/drafts/`, and research briefs are `.md` files in `content/raw/research/`.
- **Two Claude Code skills** drive the system: `/content [platform] [topic]` generates platform-ready drafts, and `/content-research [platform] [topic]` scrapes reference creators via Apify and produces competitive intelligence briefs.

The system works but has three friction points:

1. **No visual tracking.** No calendar, no kanban — pipeline status is just a markdown file.
2. **No mobile access.** Capturing ideas, reviewing drafts, or marking pieces as published requires a terminal.
3. **Operational data is fragmented.** Ideas in one file, drafts in another folder, research briefs in a third, pipeline in a fourth.

Notion announced two relevant capabilities in 2026:

- **Markdown Content API** (Feb 26, 2026): single API call to read/create/update pages as markdown strings.
- **Notion CLI `ntn`** (May 13, 2026): official command-line tool with `ntn pages get`, `ntn pages create --content '...'`, authentication, Workers deployment, and full API coverage.

These make a hybrid local-canonical + Notion-operational architecture viable.

## Goals

After the migration, Juan should be able to:

1. **See his content pipeline visually** — kanban by status, calendar by scheduled date, filtered views per platform/topic.
2. **Capture ideas and review drafts from anywhere** — phone, tablet, web browser; no terminal required.
3. **Operate from a single Notion workspace** for all content activities (ideas, drafts, scheduling, publishing, research).
4. **Browse the knowledge wiki on mobile** as a read-only reference.
5. **Keep Claude's generation speed unchanged** — Claude continues to read knowledge from local markdown, not over the Notion API.

Non-goals (out of scope for v1):

- Two-way sync of the knowledge wiki (one-way local → Notion only).
- Auto-pulling published-post engagement metrics (manual entry for now).
- Migrating `life/` space to Notion (this spec is content-only).
- Background file watchers or scheduled sync (sync runs on manual `/content-sync` trigger).

## Architecture

Two layers with clear boundaries:

```
LOCAL (canonical, git-tracked)              NOTION (canonical for operations)
==============================              ==================================

content/wiki/                               Content DB
  topics/                  --[mirror]-->      Lifecycle: Idea → Researching → Drafting
  voice/                                       → Ready → Scheduled → Published
  platforms/                                 Views: Kanban / Calendar / Backlog / Active / Published
  engine/
content/raw/articles/      --[mirror]-->    Research DB
content/memory/log.md                        Competitive intel briefs
                                             Relates to: Content DB

[Claude reads local for speed]              [Juan operates from here — mobile, calendar, kanban]
[Knowledge mirror is read-only in Notion]   [Claude writes drafts/briefs here via ntn CLI]
```

**Knowledge layer** (canonical: local)
- All wiki pages and raw articles stay in `content/wiki/` and `content/raw/articles/` as markdown.
- Edits happen locally (Obsidian, editor, Claude).
- Pushed one-way to Notion as a read-only mirror via `/content-sync`.
- Claude always reads from local — no Notion API latency during `/content` runs.

**Operational layer** (canonical: Notion)
- Two databases: Content DB (lifecycle) and Research DB (briefs).
- Juan captures ideas, reviews drafts, updates status, and tracks publishing entirely in Notion.
- Claude writes new drafts and briefs to Notion via `ntn pages create`.

**Sync direction**
- Local → Notion only. Operations never sync back to local.
- No conflict resolution required.

## Notion Schema

### Content DB

| Field | Type | Notes |
|---|---|---|
| Title | Title | Headline of the piece |
| Status | Select | Idea / Researching / Drafting / Ready / Scheduled / Published |
| Platform | Select | Twitter / LinkedIn / Blog |
| Topic | Select | LTV / CRO / Profitability / Subscription / Metrics / Forecasting / Incrementality (matches wiki taxonomy) |
| Hook type | Select | Economics Reveal / Contrarian Premise / Framework-First / Specificity / Credential Anchor |
| Body | Page content | The actual draft (markdown) |
| Source wiki | Multi-select | Which wiki pages fed this piece (options seeded from wiki page slugs) |
| Source articles | Multi-select | Which raw articles fed this piece (options seeded from article filenames) |
| Source research | Relation → Research DB | Which brief (if any) informed this |
| Scheduled date | Date | When Juan plans to post |
| Published date | Date | When it actually went live |
| Published URL | URL | Link to the live post |
| Engagement | Number or text | Likes, comments, views (manual entry post-publish) |
| Created | Created time | Auto |

**Views**:
- Kanban by Status
- Calendar by Scheduled date
- Ideas backlog (filter: Status = Idea)
- Active drafts (filter: Status = Drafting or Ready)
- Published log (filter: Status = Published)
- By Platform
- By Topic

### Research DB

| Field | Type | Notes |
|---|---|---|
| Title | Title | e.g. "Twitter — LTV — 2026-05-24" |
| Date | Date | When the brief was generated |
| Platform | Select | Twitter / LinkedIn / Both |
| Topic | Select | Same taxonomy as Content DB |
| Creators scraped | Multi-select | Taylor Holiday, Nick Sharma, Cody Plofker, etc. |
| Posts analyzed | Number | Count of posts in the analysis |
| Top posts | Page content | Table of top performers |
| Hook patterns | Page content | What's working |
| Gaps Juan can own | Page content | The actionable section |
| Recommended angles | Page content | 3 angles, each linked to wiki pages |
| Informed pieces | Relation → Content DB | Which content used this brief |

### Knowledge mirror

The local knowledge wiki is mirrored into a single Notion parent page (e.g., "JCG-OS Knowledge") with sub-pages preserving the folder hierarchy:

```
JCG-OS Knowledge (Notion page)
├── topics/
│   ├── subscription-metrics
│   ├── ltv-frameworks
│   └── ...
├── voice/
├── platforms/
├── engine/
└── articles/
    ├── (37 raw articles)
```

These are read-only from Juan's perspective. Edits in Notion are NOT pulled back to local. If Juan wants to edit a wiki page, he edits the local file and re-runs `/content-sync`.

## Sync Layer

`/content-sync` is a new Claude Code skill that walks the local knowledge layer and pushes it to the Notion mirror via the `ntn` CLI.

**Behavior**:
1. Read configuration: Notion parent page ID for the knowledge mirror, file paths to include, path of the sync state file.
2. Load sync state: `content/memory/notion-sync-state.json` maps `{local-relative-path → notion-page-id}`. Empty on first run.
3. For each local markdown file under `content/wiki/` and `content/raw/articles/`:
   - If the path is NOT in the state file: `ntn pages create --parent <hierarchy-parent> --content <markdown>`, capture the returned Notion page ID, save it to the state file.
   - If the path IS in the state file: update the existing page using the Notion API's page-update operation with the new markdown content (the exact `ntn` subcommand for update should be verified against current Notion CLI docs during implementation; fall back to a direct API call if no CLI wrapper exists).
4. Handle deletions: if a path exists in the state file but no longer exists locally, archive the corresponding Notion page (don't delete — keep as historical).
5. Report: pages created, pages updated, pages archived, errors.

**Triggering**:
- Manual: Juan runs `/content-sync` when he wants the Notion mirror refreshed.
- Optional later: a git post-commit hook in JCG-OS that triggers sync after wiki edits land.

**Idempotency**:
- Sync must be safe to re-run. Same input → same Notion state.
- A small state file (`content/memory/notion-sync-state.json`) maps local file paths to Notion page IDs to avoid duplicate page creation.

## Command Surface

Three commands total — down from the current two, plus the new sync command.

### `/content [platform] [topic]`

Existing skill, modified output.

**Reads** (local, unchanged):
- `content/wiki/content-strategy.md` for phase constraints
- `content/wiki/topics/<topic>.md` for source material
- `content/wiki/voice/*` for voice
- `content/wiki/platforms/<platform>.md` for format
- `content/wiki/engine/hooks.md` to pick a hook

**Writes** (new):
- Creates a row in Notion Content DB via `ntn pages create --parent database:<content-db-id> --content <draft-markdown>`.
- Sets fields: Status=Drafting, Platform, Topic, Hook type, Source wiki, Source articles.
- Returns the Notion page URL.

**Argument changes**:
- If invoked with no args: query Notion Content DB for the oldest row with Status=Idea, promote it (set Status=Drafting, write body).
- Existing args (`/content twitter LTV`, `/content repurpose <article>`, `--research` flag) unchanged in semantics.

### `/content-research [platform] [topic]`

Existing skill, modified output.

**Reads** (unchanged): Apify scrapers, wiki for gap analysis.

**Writes** (new):
- Creates a row in Notion Research DB via `ntn pages create --parent database:<research-db-id>`.
- Fills fields: Date, Platform, Topic, Creators scraped, Posts analyzed.
- Writes Top posts / Hook patterns / Gaps / Recommended angles as page body.
- Returns the Notion page URL.

### `/content-sync` (new)

Push local knowledge to the Notion mirror. See Sync Layer above.

### Removed from the flow

- Saving drafts as `.md` files in `content/raw/drafts/`. New drafts live only in Notion.
- Updating `content/wiki/pipeline.md`. Status tracking happens in Notion now.
- Appending to `content/memory/log.md` for content events. Notion Created/Updated timestamps and Status transitions are the log.

## Migration Path

One-time migration steps, in order:

1. **Create Notion DBs**. Manually in the Notion UI:
   - Content DB with the schema above. Create all six views.
   - Research DB with the schema above.
   - Knowledge mirror parent page ("JCG-OS Knowledge").
2. **Configure `ntn` CLI**. Run the official Notion CLI auth command (verify exact subcommand in `ntn` docs at implementation time) to connect to Juan's Notion workspace. Save three IDs to a git-ignored config file in JCG-OS (e.g., `content/.notion-config.json`):
   - Content DB ID
   - Research DB ID
   - Knowledge mirror parent page ID
3. **Push knowledge mirror**. Run `/content-sync` to populate the mirror with all wiki pages and raw articles.
4. **Backfill Content DB**:
   - Each item in the "Priority Repurposing Queue" from `content-index.md` → Content DB row with Status=Idea.
   - Each `.md` file in `content/raw/drafts/` → Content DB row with Status=Drafting and body=draft content.
   - Each of the 37 published articles in `content/raw/articles/` → Content DB row with Status=Published, Published URL, source attribution. (Optional — only worth doing if Juan wants the historical log in Notion.)
5. **Archive local operational files**.
   - `content/wiki/pipeline.md`: prepend a header noting it's historical, point readers to the Notion Content DB.
   - `content/raw/drafts/`: keep as historical, no new files added.
6. **Update skill files**.
   - `/content` command (`~/.claude/commands/content.md`): change the "FILE TO PIPELINE" step to write to Notion via `ntn`.
   - `/content-research` command (`~/.claude/commands/content-research.md`): change the "Save Research" step to write to Notion.
   - Add new `/content-sync` command.
7. **Update `content/wiki/content-index.md`** to point to Notion as the operational source of truth, remove the embedded ideas list, update the Tooling section.

## Open Questions and Future Work

These are intentionally deferred from v1:

- **Two-way sync for the knowledge layer.** If Juan finds himself wanting to edit wiki pages on mobile, revisit with the community CLIs that support two-way sync (mk-notes, go-notion-md-sync) or a custom Notion Worker.
- **Auto-fetched engagement metrics.** A Notion Worker could pull post engagement from Twitter/LinkedIn APIs and populate the Engagement field. Free to build until Aug 11, 2026 when Workers start consuming Notion credits.
- **Scheduled publishing.** No auto-publish in v1 — Juan posts manually and updates Notion after. A future Worker could publish to platforms directly.
- **Repurposing relationships.** When a Twitter thread comes from a LinkedIn post (or vice versa), capture the relationship via a self-relation field in Content DB ("Repurposed from"). Skipped in v1 for simplicity.
- **GitHub-triggered sync.** Optional later: a post-commit hook on JCG-OS that runs `/content-sync` automatically after wiki edits.

## References

- [Notion CLI overview](https://developers.notion.com/cli/get-started/overview)
- [Notion 3.5 Developer Platform release notes (May 13, 2026)](https://www.notion.com/releases/2026-05-13)
- [Notion Markdown Content API guide](https://developers.notion.com/guides/data-apis/working-with-markdown-content)
- [Notion turns its workspace into a hub for AI agents — TechCrunch](https://techcrunch.com/2026/05/13/notion-just-turned-its-workspace-into-a-hub-for-ai-agents/)
