# Notion Content System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate Juan's content operational layer (ideas, pipeline, drafts, research) into Notion while keeping the knowledge wiki canonical in local markdown. Claude reads local, writes to Notion via `ntn` CLI.

**Architecture:** Two-layer system. Local markdown = canonical knowledge (wiki, raw articles). Notion = canonical operations (Content DB lifecycle, Research DB briefs). One-way sync (local → Notion mirror) on manual trigger.

**Tech Stack:** Notion CLI (`ntn`), Notion Markdown Content API, Claude Code skills (markdown), Apify (existing — for `/content-research`), git for version control.

**Spec:** `docs/superpowers/specs/2026-05-24-notion-content-system-design.md`

---

## File Inventory

**New files:**
- `~/.claude/commands/content-sync.md` — new sync skill
- `C:\Users\jcgiu\Documents\JCG-OS\content\.notion-config.json` — DB and parent page IDs (gitignored)
- `C:\Users\jcgiu\Documents\JCG-OS\content\memory\notion-sync-state.json` — sync state map (gitignored)
- `C:\Users\jcgiu\Documents\JCG-OS\.gitignore` (modify if exists, create if not) — ignore config + state

**Modified files:**
- `~/.claude/commands/content.md` — change output target from local file to Notion DB
- `~/.claude/commands/content-research.md` — change output target from local file to Notion DB
- `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\content-index.md` — remove embedded ideas list, point Tooling section at Notion
- `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\pipeline.md` — prepend header marking as historical
- `C:\Users\jcgiu\Documents\JCG-OS\content\memory\log.md` — append migration entry

**Read-only references:**
- `content/wiki/topics/*`, `content/wiki/voice/*`, `content/wiki/platforms/*`, `content/wiki/engine/*` — pushed to Notion mirror but not modified
- `content/raw/articles/*` — pushed to Notion mirror but not modified

---

## Phase 1: Notion Setup

### Task 1: Install and authenticate the `ntn` CLI

**Files:**
- None (CLI install)

- [ ] **Step 1: Check if `ntn` is already installed**

Run: `ntn --version`
Expected: prints a version string. If "command not found", proceed to install.

- [ ] **Step 2: Install `ntn` if missing**

Per Notion's official docs (https://developers.notion.com/cli/get-started/overview), follow the install instructions for the current platform. On Windows, typical options are `npm i -g @notionhq/ntn` or downloading the binary. Verify exact command from the docs page above at install time.

After install:
Run: `ntn --version`
Expected: prints a version string.

- [ ] **Step 3: Authenticate**

Run: `ntn auth login` (verify exact subcommand in the docs page above at install time; older releases may use `ntn login`).
Follow the OAuth flow in the browser. Sign in to Juan's Notion workspace.

- [ ] **Step 4: Verify auth**

Run: `ntn auth status` (or equivalent — check `ntn --help`).
Expected: shows Juan's workspace as the active connection.

- [ ] **Step 5: Smoke test the API**

Run: `ntn pages create --parent workspace --content "# Notion CLI smoke test\n\nIf you can see this, ntn works."`
Expected: prints a Notion page URL or page ID.

Open the URL in a browser to confirm the page exists. Delete the test page in Notion after verifying.

- [ ] **Step 6: Commit (nothing to commit yet — phase setup only)**

No commit. Move to Task 2.

---

### Task 2: Create the Content DB in Notion

**Files:**
- None (manual UI step in Notion)

- [ ] **Step 1: Create a top-level page in Notion**

In the Notion web app, create a new top-level page in Juan's workspace called `Content OS`. This will be the parent for both DBs and the knowledge mirror.

- [ ] **Step 2: Create the Content DB as a sub-page of Content OS**

Inside `Content OS`, add a new database. Name it `Content`. Choose "Full page" database (not inline).

- [ ] **Step 3: Add all schema fields to the Content DB**

Per the spec, add these properties (Notion property type in parens):

| Field name | Notion type | Configuration |
|---|---|---|
| Title | Title | (auto, already exists) |
| Status | Select | Options: Idea, Researching, Drafting, Ready, Scheduled, Published |
| Platform | Select | Options: Twitter, LinkedIn, Blog |
| Topic | Select | Options: LTV, CRO, Profitability, Subscription, Metrics, Forecasting, Incrementality |
| Hook type | Select | Options: Economics Reveal, Contrarian Premise, Framework-First, Specificity, Credential Anchor |
| Source wiki | Multi-select | Leave options empty for now; populate as content is created |
| Source articles | Multi-select | Leave options empty for now |
| Scheduled date | Date | |
| Published date | Date | |
| Published URL | URL | |
| Engagement | Text | (Use text for free-form notes like "412 likes / 87 comments") |

Skip "Source research" relation field for now — it requires the Research DB to exist first. Add it in Task 3.

- [ ] **Step 4: Add the six default views**

In the Content DB:
- View 1: Kanban — group by Status
- View 2: Calendar — date field = Scheduled date
- View 3: Ideas backlog — Table view, filter Status=Idea, sort by Created descending
- View 4: Active drafts — Table view, filter Status=Drafting OR Status=Ready
- View 5: Published log — Table view, filter Status=Published, sort by Published date descending
- View 6: By Platform — Table view, group by Platform

- [ ] **Step 5: Capture the Content DB ID**

Open the Content DB as a full page in Notion. Copy the URL. The DB ID is the 32-char hex string in the URL (e.g., `https://www.notion.so/<workspace>/<dbid>?v=<viewid>`).

Save this somewhere temporary — it goes into the config file in Task 5.

Also run: `ntn databases list` (or `ntn pages list` filtered by type — check `ntn --help`).
Expected: the new Content DB appears with its ID.

- [ ] **Step 6: Commit (nothing to commit yet)**

No commit. Move to Task 3.

---

### Task 3: Create the Research DB in Notion

**Files:**
- None (manual UI step)

- [ ] **Step 1: Create the Research DB as a sub-page of Content OS**

Inside the `Content OS` parent page, add a new full-page database called `Research`.

- [ ] **Step 2: Add all schema fields to the Research DB**

Per the spec:

| Field name | Notion type | Configuration |
|---|---|---|
| Title | Title | (auto) |
| Date | Date | |
| Platform | Select | Options: Twitter, LinkedIn, Both |
| Topic | Select | Options: LTV, CRO, Profitability, Subscription, Metrics, Forecasting, Incrementality |
| Creators scraped | Multi-select | Pre-populate options: Taylor Holiday, Nick Sharma, Cody Plofker, Barry Hott, Dara Denney |
| Posts analyzed | Number | |
| Informed pieces | Relation | Relation target = Content DB; allow two-way relation |

The page body fields (Top posts, Hook patterns, Gaps Juan can own, Recommended angles) live inside the page content, not as DB properties.

- [ ] **Step 3: Add a "Source research" relation back to Content DB**

Go back to the Content DB. Add a new property:
- Name: Source research
- Type: Relation
- Target: Research DB

If you allowed two-way relation in Task 3 Step 2, this may already be auto-created on the Content DB side. If so, just rename it to "Source research".

- [ ] **Step 4: Add default views to Research DB**

- View 1: Table — default, sort by Date descending
- View 2: By Topic — group by Topic

- [ ] **Step 5: Capture the Research DB ID**

Same method as Task 2 Step 5. Save the ID for the config file.

- [ ] **Step 6: Commit (nothing to commit yet)**

No commit. Move to Task 4.

---

### Task 4: Create the Knowledge Mirror parent page

**Files:**
- None (manual UI step)

- [ ] **Step 1: Create the Knowledge Mirror parent page**

Inside the `Content OS` page, add a new sub-page called `JCG-OS Knowledge`. This will be the root of the read-only mirror of `content/wiki/` and `content/raw/articles/`.

Leave the page body empty for now. The `/content-sync` skill will populate it.

- [ ] **Step 2: Capture the Knowledge Mirror parent page ID**

Open the page as a full page. Copy the URL. The page ID is the 32-char hex at the end of the URL.

Save the ID for the config file.

- [ ] **Step 3: Commit (nothing to commit yet)**

No commit. Move to Task 5.

---

### Task 5: Write the config file and update .gitignore

**Files:**
- Create: `C:\Users\jcgiu\Documents\JCG-OS\content\.notion-config.json`
- Create or modify: `C:\Users\jcgiu\Documents\JCG-OS\.gitignore`

- [ ] **Step 1: Create the config file**

Path: `content/.notion-config.json`

Contents (replace the three IDs with the ones captured in Tasks 2-4):

```json
{
  "contentDbId": "REPLACE_WITH_CONTENT_DB_ID",
  "researchDbId": "REPLACE_WITH_RESEARCH_DB_ID",
  "knowledgeMirrorParentId": "REPLACE_WITH_KNOWLEDGE_MIRROR_PAGE_ID",
  "workspaceName": "Juan's Workspace"
}
```

- [ ] **Step 2: Verify .gitignore exists and ignore the config + state files**

Read `C:\Users\jcgiu\Documents\JCG-OS\.gitignore`. If it exists, append these lines (skip any already present). If it doesn't exist, create it with these contents:

```
# Notion sync — workspace-specific IDs, not for version control
content/.notion-config.json
content/memory/notion-sync-state.json
```

- [ ] **Step 3: Verify both files are ignored**

Run: `git status`
Expected: `.notion-config.json` does NOT appear under untracked files. `.gitignore` itself DOES appear (it's a new file or has new lines).

- [ ] **Step 4: Smoke test — read a DB via ntn using the IDs**

Run: `ntn pages get <contentDbId>` (the ID from the config file).
Expected: prints the Content DB metadata as markdown. Confirms auth + ID are correct.

Repeat for the Research DB ID and the Knowledge Mirror parent page ID.

- [ ] **Step 5: Commit .gitignore (only — config and state are ignored)**

```bash
git add .gitignore
git commit -m "chore: ignore Notion sync config and state files"
```

---

## Phase 2: /content-sync skill

### Task 6: Write the /content-sync skill markdown

**Files:**
- Create: `C:\Users\jcgiu\.claude\commands\content-sync.md`

- [ ] **Step 1: Create the skill markdown file**

Path: `C:\Users\jcgiu\.claude\commands\content-sync.md`

Contents:

````markdown
# /content-sync — Push local knowledge to Notion mirror

Walk `content/wiki/` and `content/raw/articles/` in JCG-OS, push each markdown file as a Notion page under the Knowledge Mirror parent. Idempotent — re-runs update existing pages instead of creating duplicates.

---

## ARGUMENTS

```
/content-sync                       # Full sync (wiki + raw articles)
/content-sync wiki                  # Only content/wiki/
/content-sync articles              # Only content/raw/articles/
/content-sync --dry-run             # Print what would happen without calling ntn
```

---

## STEP 1: LOAD CONFIG AND STATE

Read `C:\Users\jcgiu\Documents\JCG-OS\content\.notion-config.json`. Extract `knowledgeMirrorParentId`. If the file doesn't exist, error out with: "Run Phase 1 setup tasks first — Notion config missing."

Read `C:\Users\jcgiu\Documents\JCG-OS\content\memory\notion-sync-state.json`. If the file doesn't exist, treat as empty: `{}`. Otherwise parse as an object mapping `{relativeFilePath: notionPageId}`.

---

## STEP 2: ENUMERATE LOCAL FILES

Based on the argument:
- No arg or no recognized subset: include both `content/wiki/**/*.md` and `content/raw/articles/**/*.md`
- `wiki`: only `content/wiki/**/*.md`
- `articles`: only `content/raw/articles/**/*.md`

Exclude:
- `content/wiki/content-index.md` (index page, not a knowledge page)
- `content/wiki/pipeline.md` (operational, not knowledge)
- Any file matching `.notion-config.json` or `notion-sync-state.json`

Build a list of `{relativePath, absolutePath, markdownBody}` records.

---

## STEP 3: SYNC EACH FILE

For each file:

1. Compute `relativePath` (relative to the JCG-OS root, forward slashes).
2. Look up `state[relativePath]`. If present, it's an existing Notion page ID.
3. If `--dry-run`: print "WOULD CREATE: <relativePath>" or "WOULD UPDATE: <pageId> ← <relativePath>" and continue.
4. Otherwise:
   - **Create** (no entry in state):
     Run `ntn pages create --parent page:<knowledgeMirrorParentId> --content "<markdownBody>" --title "<title from frontmatter or filename>"`
     (Verify exact `--title` flag against `ntn pages create --help` at execution time.)
     Capture the returned page ID from stdout. Add to state: `state[relativePath] = newPageId`.
   - **Update** (entry exists):
     Run the Notion page-update command via `ntn` (check `ntn pages update --help` or `ntn pages set-content --help`; if no CLI subcommand exists, fall back to `ntn api PATCH /v1/pages/<pageId>` per https://developers.notion.com/guides/data-apis/working-with-markdown-content).
     Replace the page body with the new markdown.

5. Track outcome per file: created / updated / skipped / error.

---

## STEP 4: HANDLE DELETIONS

For each entry in `state` whose `relativePath` no longer exists locally:
- Archive the Notion page: `ntn pages archive <pageId>` (or equivalent — check the docs).
- Remove the entry from state.
- Track outcome: archived.

---

## STEP 5: WRITE STATE BACK

Write the updated state map to `content/memory/notion-sync-state.json` as pretty-printed JSON.

---

## STEP 6: REPORT

Print a summary:
```
Sync complete.
  Created:  N pages
  Updated:  N pages
  Archived: N pages
  Errors:   N (list them)
  State:    content/memory/notion-sync-state.json
```

---

## CONSTRAINTS

- One-way only. Never read content FROM Notion to write to local files in this skill.
- Idempotent. Re-running must be safe.
- If any single file errors out, log it and continue with the rest. Don't abort the whole run.
- Skip files larger than 1 MB (Notion has a body size limit; very large articles may need splitting — out of scope for v1).
````

- [ ] **Step 2: Verify the file is in place**

Run: `ls "C:\Users\jcgiu\.claude\commands\content-sync.md"`
Expected: the file is listed.

Open the file and confirm it looks correct.

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\jcgiu\Documents\JCG-OS"
# (skill file lives outside the repo — no commit in JCG-OS for this task)
```

The skill file at `~/.claude/commands/content-sync.md` is NOT tracked in the JCG-OS repo. If Juan has a separate dotfiles repo for `~/.claude/`, commit there. Otherwise, no commit for this task.

---

### Task 7: Dry-run sync on a 2-file subset

**Files:**
- Read-only: 2 files in `content/wiki/topics/`

- [ ] **Step 1: Pick 2 small wiki files to use as a test subset**

For example: `content/wiki/topics/ltv-frameworks.md` and `content/wiki/topics/profitability-levers.md`.

- [ ] **Step 2: Manually run the sync logic on just these 2 files in dry-run mode**

Invoke: `/content-sync wiki --dry-run`

Expected stdout includes lines like:
```
WOULD CREATE: content/wiki/topics/ltv-frameworks.md
WOULD CREATE: content/wiki/topics/profitability-levers.md
...
```

(All wiki files will appear, not just 2 — but verify the 2 specific ones are listed.)

- [ ] **Step 3: Verify state file is NOT created by dry-run**

Run: `ls "C:\Users\jcgiu\Documents\JCG-OS\content\memory\notion-sync-state.json"`
Expected: file does not exist (dry-run must not write state).

- [ ] **Step 4: Real run on a single file to validate end-to-end**

To test creation without doing a full sync, temporarily move all wiki files except `ltv-frameworks.md` into a quarantine folder, OR modify the skill invocation to filter to one file. (Simplest: run a temporary glob filter inline.)

Invoke a one-file create: ask Claude to run the create branch of the sync skill manually for just `content/wiki/topics/ltv-frameworks.md`.

Expected:
- `ntn pages create ...` succeeds
- New page appears in Notion under "JCG-OS Knowledge"
- State file is written: `{"content/wiki/topics/ltv-frameworks.md": "<page-id>"}`

- [ ] **Step 5: Re-run to verify idempotency (update branch)**

Re-run the same one-file sync.

Expected:
- `ntn pages` update/set-content runs (not create)
- Same Notion page is updated (no duplicate)
- State file unchanged

- [ ] **Step 6: Delete the test page from Notion and clear state**

Manually delete the test page in Notion. Delete `content/memory/notion-sync-state.json`.

Reason: keeps the workspace clean before the real full sync in Task 8.

- [ ] **Step 7: Commit (nothing to commit — state file is gitignored, skill already in place)**

No commit.

---

### Task 8: Full initial sync of knowledge layer

**Files:**
- Reads: all of `content/wiki/` and `content/raw/articles/`
- Writes: `content/memory/notion-sync-state.json` (gitignored)

- [ ] **Step 1: Verify state file is absent (clean start)**

Run: `ls "C:\Users\jcgiu\Documents\JCG-OS\content\memory\notion-sync-state.json"`
Expected: file does not exist. If it does, delete it.

- [ ] **Step 2: Verify Notion Knowledge Mirror parent page is empty**

In Notion, open "JCG-OS Knowledge". Confirm it has no children. If it has leftovers from Task 7, delete them.

- [ ] **Step 3: Run full sync**

Invoke: `/content-sync`

Expected console output (approximate counts):
```
Sync complete.
  Created:  ~60 pages (wiki ~20 + articles 37 = ~57; exact count depends on current wiki size)
  Updated:  0
  Archived: 0
  Errors:   0
```

Run time: ~1-2 minutes assuming Notion rate limits (3 req/sec).

- [ ] **Step 4: Spot-check 3 pages in Notion**

Open "JCG-OS Knowledge" in Notion. Verify:
- `content/wiki/topics/ltv-frameworks.md` appears (or its title), body matches local file
- `content/raw/articles/asteroi-en-roas-doesnt-mean-shit.md` appears, body matches
- One voice/platform/engine page appears, body matches

- [ ] **Step 5: Verify state file**

Read `content/memory/notion-sync-state.json`. Confirm it has ~60 entries, each mapping a local path to a Notion page ID.

- [ ] **Step 6: Re-run to verify all-update mode**

Invoke: `/content-sync` again.

Expected:
```
  Created:  0
  Updated:  ~60
  Archived: 0
```

No duplicates in Notion.

- [ ] **Step 7: Commit (nothing — state file is gitignored)**

No commit.

---

## Phase 3: Update /content skill

### Task 9: Update /content to write drafts to Notion Content DB

**Files:**
- Modify: `C:\Users\jcgiu\.claude\commands\content.md`

- [ ] **Step 1: Read the current /content skill**

Read `~/.claude/commands/content.md` end-to-end. Note STEP 6: FILE TO PIPELINE currently writes to local files.

- [ ] **Step 2: Replace STEP 6 (FILE TO PIPELINE) with a Notion write step**

Find the section starting with `## STEP 6: FILE TO PIPELINE (IF APPROVED)` and replace with:

```markdown
## STEP 6: WRITE TO NOTION (IF APPROVED)

If Juan approves the piece, write it to the Notion Content DB.

1. Read `C:\Users\jcgiu\Documents\JCG-OS\content\.notion-config.json` for `contentDbId`.
2. Run:
   ```
   ntn pages create --parent database:<contentDbId> --content "<draft markdown>" \
     --property Title="<title>" \
     --property Status="Drafting" \
     --property Platform="<platform>" \
     --property Topic="<topic>" \
     --property "Hook type"="<hook>" \
     --property "Source wiki"="<comma-separated wiki page slugs>" \
     --property "Source articles"="<comma-separated article filenames>"
   ```
   (Verify exact `--property` flag syntax against `ntn pages create --help` at execution time. If property flags aren't supported, use `ntn api POST /v1/pages` with a JSON body per https://developers.notion.com/guides/data-apis/working-with-markdown-content.)
3. Capture the returned page URL from stdout.
4. Report to Juan: "Filed to Notion Content DB. URL: <url>. Status: Drafting."

If the user requests a different status (e.g., "save as idea, I'll write the body later"), set Status accordingly.

DO NOT write the draft to `content/raw/drafts/` — that location is historical only.
DO NOT update `content/wiki/pipeline.md` — that file is historical only.
```

- [ ] **Step 3: Add new STEP 0.5 — handle no-args invocation**

Insert this section right after STEP 0 (or before STEP 1 if STEP 0 doesn't exist):

```markdown
## STEP 0.5: NO-ARGS MODE — PROMOTE FROM IDEAS BACKLOG

If the user invokes `/content` with no platform AND no topic, do this instead of asking:

1. Read `content/.notion-config.json` for `contentDbId`.
2. Query the Content DB for rows where Status=Idea, sorted by Created ascending (oldest first).
   Run: `ntn databases query <contentDbId> --filter '{"property":"Status","select":{"equals":"Idea"}}' --sort '[{"property":"Created","direction":"ascending"}]'`
   (Verify exact filter/sort syntax against `ntn databases query --help`.)
3. Take the first result. Read its Title, Platform, Topic properties.
4. Tell Juan: "Promoting oldest idea: '<title>' (<platform>, <topic>). Generating draft."
5. Proceed with the normal flow using that platform/topic.
6. In STEP 6, instead of creating a new page, UPDATE the existing idea row: set Status=Drafting and replace the page body with the draft.

If no Idea-status rows exist, tell Juan: "No ideas in backlog. Provide a platform and topic explicitly." Stop.
```

- [ ] **Step 4: Update the file header to reflect new behavior**

Find the opening paragraph and add a sentence:
> Drafts are filed to the Notion Content DB (Status=Drafting). Idea capture and status tracking happen in Notion. Claude reads source material from local markdown only.

- [ ] **Step 5: Verify the file**

Read `~/.claude/commands/content.md`. Spot-check that:
- STEP 6 no longer references `content/raw/drafts/`
- STEP 6 no longer references `content/wiki/pipeline.md`
- STEP 0.5 (no-args mode) is present
- The Notion write commands include all six relevant properties

- [ ] **Step 6: Commit (skill file is outside JCG-OS repo)**

If `~/.claude/` is under version control elsewhere, commit there. Otherwise no commit.

---

### Task 10: End-to-end test — generate a draft to Notion

**Files:**
- None (test step)

- [ ] **Step 1: Pick a topic + platform**

Choose something concrete: `/content twitter LTV`.

- [ ] **Step 2: Run the skill**

Invoke `/content twitter LTV`.

Expected:
- Claude reads `content/wiki/topics/ltv-frameworks.md` (and other relevant local files)
- Generates a Twitter thread draft
- Presents the draft and asks for approval (per current STEP 5)
- On approval, calls `ntn pages create` to file to Content DB

- [ ] **Step 3: Verify the row in Notion**

Open Content DB in Notion. Find the new row.

Verify:
- Title is set
- Status = Drafting
- Platform = Twitter
- Topic = LTV
- Hook type is filled
- Source wiki is filled
- Page body contains the draft

- [ ] **Step 4: Verify nothing was written to local drafts folder**

Run: `ls "C:\Users\jcgiu\Documents\JCG-OS\content\raw\drafts\"`
Expected: no new files since the migration started.

- [ ] **Step 5: Verify pipeline.md was not touched**

Run: `git status content/wiki/pipeline.md`
Expected: unchanged.

- [ ] **Step 6: Commit (nothing — no JCG-OS file changes)**

No commit. Skill file changes happen in `~/.claude/` outside the repo.

---

### Task 11: End-to-end test — no-args mode promotes an idea

**Files:**
- None (test step — requires at least one Idea-status row in Notion, which Task 15 will create. If running tasks strictly in order, defer this test until after Task 15.)

- [ ] **Step 1: Confirm at least one Idea-status row exists**

In Notion Content DB, filter Status=Idea. If no rows, manually create one with Title="ROAS doesn't mean shit", Platform=Twitter, Topic=Metrics, Status=Idea. (Task 15 will do this in bulk; this is just to enable the test.)

- [ ] **Step 2: Run /content with no args**

Invoke: `/content`

Expected:
- Claude responds: "Promoting oldest idea: '<title>'..."
- Generates draft using that idea's platform/topic
- Updates the same Notion row (does NOT create a new one)
- Sets Status=Drafting and writes body

- [ ] **Step 3: Verify in Notion**

Filter Status=Idea — confirm the promoted row is no longer in this view.
Filter Status=Drafting — confirm it appears here with the draft body.

- [ ] **Step 4: Commit (nothing)**

No commit.

---

## Phase 4: Update /content-research skill

### Task 12: Update /content-research to write briefs to Notion Research DB

**Files:**
- Modify: `C:\Users\jcgiu\.claude\commands\content-research.md`

- [ ] **Step 1: Read the current /content-research skill**

Read `~/.claude/commands/content-research.md` end-to-end. Note step "7. Save Research" currently writes to `content/raw/research/`.

- [ ] **Step 2: Replace the "Save Research" step**

Find the section:
```
### 7. Save Research

Save the brief to `C:\Users\jcgiu\Documents\JCG-OS\content\raw\research\[date]-[platform]-[topic].md` for future reference.
```

Replace with:

```markdown
### 7. Save Research to Notion

Write the brief to the Notion Research DB.

1. Read `C:\Users\jcgiu\Documents\JCG-OS\content\.notion-config.json` for `researchDbId`.
2. Build the page body (markdown) including:
   - Top Performing Posts table
   - Hook Patterns section
   - Topic Angles section
   - Gaps Juan Can Own section
   - Recommended Content Angles section
3. Run:
   ```
   ntn pages create --parent database:<researchDbId> --content "<page body markdown>" \
     --property Title="<platform> — <topic> — <YYYY-MM-DD>" \
     --property Date="<YYYY-MM-DD>" \
     --property Platform="<platform>" \
     --property Topic="<topic>" \
     --property "Creators scraped"="<comma-separated names>" \
     --property "Posts analyzed"=<number>
   ```
4. Capture the returned page URL from stdout.
5. Report to Juan: "Brief filed to Notion Research DB. URL: <url>."

DO NOT write the brief to `content/raw/research/` — that location is historical only.
```

- [ ] **Step 3: Update the log entry step**

Find the section that appends to `content/memory/log.md`. Replace with a smaller log entry pointing to Notion:

```markdown
### 8. Log activity (optional)

Append a single line to `content/memory/log.md`:

```
## [YYYY-MM-DD] research | <platform> — <topic>
- Brief filed to Notion: <page URL>
```
```

Keep this lightweight — the brief itself lives in Notion now, not in local logs.

- [ ] **Step 4: Update the file header**

Add a sentence to the opening paragraph:
> Briefs are filed to the Notion Research DB. Page body contains the analysis; properties capture metadata (date, platform, topic, creators, post counts).

- [ ] **Step 5: Verify the file**

Read the updated `content-research.md`. Confirm:
- Step 7 writes to Notion via `ntn pages create`
- No references to `content/raw/research/` as a write target
- All six relevant properties are populated

- [ ] **Step 6: Commit (skill file outside JCG-OS repo)**

If `~/.claude/` is version-controlled elsewhere, commit there. Otherwise no commit.

---

### Task 13: End-to-end test — research brief writes to Notion

**Files:**
- None (test step)

- [ ] **Step 1: Run /content-research on a small scope**

Invoke: `/content-research twitter LTV`

Expected:
- Claude scrapes Taylor Holiday and Nick Sharma via Apify
- Generates a brief
- Calls `ntn pages create` to file to Research DB

- [ ] **Step 2: Verify the row in Notion**

Open Research DB in Notion. Find the new row.

Verify:
- Title is in format "Twitter — LTV — YYYY-MM-DD"
- Date is set
- Platform = Twitter
- Topic = LTV
- Creators scraped = Taylor Holiday, Nick Sharma
- Posts analyzed = N (some positive number)
- Page body contains Top Posts / Hook Patterns / Gaps / Recommended Angles sections

- [ ] **Step 3: Verify nothing was written to local research folder**

Run: `ls "C:\Users\jcgiu\Documents\JCG-OS\content\raw\research\"`
Expected: no new files since migration started.

- [ ] **Step 4: Commit (nothing)**

No commit.

---

## Phase 5: Backfill

### Task 14: Backfill priority repurposing queue → Content DB (Status=Idea)

**Files:**
- Read: `content/wiki/content-index.md`
- Writes: rows in Notion Content DB

- [ ] **Step 1: Read the current Priority Repurposing Queue**

Read `content/wiki/content-index.md`. Locate the section "Priority Repurposing Queue (Phase 1 — in-lane articles)". Capture the 7 items.

- [ ] **Step 2: Create 7 idea rows in Notion via `ntn`**

For each item, run:
```
ntn pages create --parent database:<contentDbId> \
  --property Title="<item title>" \
  --property Status="Idea" \
  --property Platform="<best platform from the line>" \
  --property Topic="<inferred from title>" \
  --property "Source articles"="<source filename if mentioned>"
```

For example, item 1: "Your ROAS Doesn't Mean Shit" — contrarian, built-in Economics Reveal. Best for: Twitter thread + LinkedIn post.
→ Create one row with Platform=Twitter, one with Platform=LinkedIn, both Topic=Metrics, Source articles=asteroi-en-roas-doesnt-mean-shit.md (or the ES version).

Note: items that say "Best for: Twitter + LinkedIn" should become TWO separate rows (one per platform).

- [ ] **Step 3: Verify in Notion**

Open Content DB, filter Status=Idea. Confirm all expected rows are present.

- [ ] **Step 4: Commit (nothing — Notion writes only)**

No commit.

---

### Task 15: Backfill existing local drafts → Content DB (Status=Drafting)

**Files:**
- Read: `content/raw/drafts/*` (if any exist)
- Writes: rows in Notion Content DB

- [ ] **Step 1: Enumerate existing local drafts**

Run: `ls "C:\Users\jcgiu\Documents\JCG-OS\content\raw\drafts\"`

If empty: skip this task and proceed to Task 16.

If files present: for each file, capture the title, platform, body.

- [ ] **Step 2: Create one Content DB row per local draft**

For each draft file, run:
```
ntn pages create --parent database:<contentDbId> --content "<draft body>" \
  --property Title="<title>" \
  --property Status="Drafting" \
  --property Platform="<from filename or frontmatter>" \
  --property Topic="<inferred>"
```

- [ ] **Step 3: Verify in Notion**

Filter Content DB by Status=Drafting. Confirm each backfilled draft appears with body intact.

- [ ] **Step 4: Commit (nothing)**

No commit.

---

### Task 16: (Optional) Backfill 37 published articles → Content DB (Status=Published)

**Files:**
- Read: `content/raw/articles/*`
- Writes: rows in Notion Content DB

**Decision gate:** Confirm with Juan before running this task. The 37 articles are already in the Knowledge Mirror as reference pages. Backfilling them as Content DB rows is only worth doing if Juan wants the historical published log in Notion. If skipping, mark this task complete with no action.

- [ ] **Step 1: Confirm with Juan whether to proceed**

If Juan says skip → mark all sub-steps complete and move to Task 17.

If Juan says proceed → continue.

- [ ] **Step 2: Enumerate articles**

For each `.md` file in `content/raw/articles/`, capture:
- Title (from frontmatter or filename)
- Platform = Blog (since these are all blog posts)
- Topic (best inference from title — LTV, CRO, Profitability, etc.)
- Published URL (from frontmatter `url:` field — confirm each article has one; if not, derive from filename + content-index.md)

- [ ] **Step 3: Create 37 published rows**

For each article, run:
```
ntn pages create --parent database:<contentDbId> \
  --property Title="<title>" \
  --property Status="Published" \
  --property Platform="Blog" \
  --property Topic="<inferred>" \
  --property "Published URL"="<url>" \
  --property "Source articles"="<filename>"
```

Body can be left empty for these backfill rows — the full article lives in the Knowledge Mirror, and the row's purpose is just to log it in the published history.

- [ ] **Step 4: Verify in Notion**

Filter Content DB by Status=Published. Confirm 37 rows appear (or however many were processed). Spot-check 3 to confirm Published URL works.

- [ ] **Step 5: Commit (nothing)**

No commit.

---

## Phase 6: Cleanup and docs

### Task 17: Archive local pipeline.md

**Files:**
- Modify: `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\pipeline.md`

- [ ] **Step 1: Read the current pipeline.md**

Read the file. Capture its current contents.

- [ ] **Step 2: Prepend a historical-notice header**

Modify the file so the very top reads:

```markdown
---
title: Pipeline (Historical)
description: Historical pipeline tracker. Active tracking now lives in Notion Content DB. This file is retained for reference only and not updated going forward.
type: archive
author: claude
created: <preserve original>
updated: 2026-05-24
status: historical
---

> **This file is no longer updated.** Active content pipeline tracking lives in the Notion Content DB. Open Content OS → Content in Notion to view the current pipeline.
>
> The content below reflects the state of the pipeline as of 2026-05-24, before the migration to Notion.

---

[original contents below — preserve verbatim]
```

Preserve the original frontmatter values for `created` and any other fields that existed.

- [ ] **Step 3: Verify the file**

Read the updated file. Confirm the header is in place and the original content is preserved below.

- [ ] **Step 4: Commit**

```bash
cd "C:\Users\jcgiu\Documents\JCG-OS"
git add content/wiki/pipeline.md
git commit -m "docs(content): archive pipeline.md — active tracking moved to Notion"
```

---

### Task 18: Update content-index.md to point at Notion

**Files:**
- Modify: `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\content-index.md`

- [ ] **Step 1: Read the current content-index.md**

Read the file. Identify three sections that need changes:
1. The "Strategy & Pipeline" section — the bullet for `[[pipeline]]` should note historical status
2. The "Tooling" section — add `/content-sync` and update `/content` / `/content-research` descriptions
3. The "Content Ideas" / "Priority Repurposing Queue" section — remove (now in Notion)

- [ ] **Step 2: Update "Strategy & Pipeline" section**

Replace the `[[pipeline]]` bullet with:

```markdown
- [[pipeline]] — Historical pipeline tracker (pre-2026-05-24). Active pipeline is now in the Notion Content DB. (confidence: high)
- **Notion Content DB** — Active operational layer. Ideas, drafts, scheduling, publishing, performance. Open: Content OS → Content in Notion.
```

- [ ] **Step 3: Update "Tooling" section**

Find the `/content` and `/content-research` entries. Update each description to mention Notion as the output target.

Add a new entry for `/content-sync`:

```markdown
### /content-sync — Push Local Knowledge to Notion Mirror
Walks `content/wiki/` and `content/raw/articles/`, pushes each file as a Notion page under the Knowledge Mirror parent. Idempotent. One-way (local → Notion).
- **Location:** `~/.claude/commands/content-sync.md`
- **Usage:** `/content-sync` (full), `/content-sync wiki`, `/content-sync articles`, `/content-sync --dry-run`
```

- [ ] **Step 4: Replace the "Content Ideas" section**

Replace the entire "Content Ideas" section (Priority Repurposing Queue + Off-Limits + "Add new ideas by telling Claude") with:

```markdown
## Content Ideas

Ideas now live in the Notion Content DB with Status=Idea. Open Content OS → Content → Ideas backlog view to see, add, or promote.

The Phase 1 firewall (off-limits topics) is enforced in the `/content` skill — see `~/.claude/commands/content.md` STEP 2 and `content-strategy.md`.
```

- [ ] **Step 5: Update the Research section**

Find the "Research" section. Replace with:

```markdown
## Research

Research briefs from `/content-research` are filed to the Notion Research DB. Open Content OS → Research to browse.

Historical briefs (pre-migration) in `content/raw/research/` are retained but not updated.
```

- [ ] **Step 6: Update the frontmatter `updated:` field**

Change the `updated:` field to `2026-05-24`.

- [ ] **Step 7: Verify the file**

Read the updated content-index.md end-to-end. Confirm no stale references to local pipeline/drafts/research as the active source of truth.

- [ ] **Step 8: Commit**

```bash
cd "C:\Users\jcgiu\Documents\JCG-OS"
git add content/wiki/content-index.md
git commit -m "docs(content): point content-index at Notion as operational source of truth"
```

---

### Task 19: Append migration entry to content memory log

**Files:**
- Modify: `C:\Users\jcgiu\Documents\JCG-OS\content\memory\log.md`

- [ ] **Step 1: Append a migration log entry**

Add to the top of `content/memory/log.md` (most-recent-first):

```markdown
## [2026-05-24] migration | Content system moved to Notion

- Notion DBs created: Content DB (lifecycle), Research DB (briefs)
- Knowledge mirror created under "JCG-OS Knowledge" — wiki + raw articles pushed via `/content-sync`
- Skills updated: `/content` and `/content-research` now write to Notion DBs; new `/content-sync` skill added
- Local archived: `pipeline.md` marked historical; `content/raw/drafts/` and `content/raw/research/` no longer written to
- Spec: `docs/superpowers/specs/2026-05-24-notion-content-system-design.md`
- Plan: `docs/superpowers/plans/2026-05-24-notion-content-system.md`
- Backfilled to Content DB: priority repurposing queue (Status=Idea), existing local drafts (Status=Drafting), optionally 37 published articles (Status=Published)
- Config: `content/.notion-config.json` (gitignored)
- Sync state: `content/memory/notion-sync-state.json` (gitignored)
```

- [ ] **Step 2: Verify the file**

Read the log. Confirm the entry is at the top and well-formed.

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\jcgiu\Documents\JCG-OS"
git add content/memory/log.md
git commit -m "docs(content): log Notion migration"
```

---

### Task 20: Final verification

**Files:**
- None (verification only)

- [ ] **Step 1: Verify all DBs in Notion**

Open Notion. Confirm:
- Content OS page exists
- Content DB has all schema fields and views
- Research DB has all schema fields and views
- JCG-OS Knowledge page has children (wiki + articles)

- [ ] **Step 2: Verify all skill files**

Run: `ls ~/.claude/commands/content*.md`
Expected: `content.md`, `content-research.md`, `content-sync.md` all present.

Spot-read each to confirm Notion integration is wired up.

- [ ] **Step 3: Verify gitignore**

Run: `git status`
Expected: no `.notion-config.json` or `notion-sync-state.json` in tracked or untracked files.

- [ ] **Step 4: Verify JCG-OS commits**

Run: `git log --oneline -10`
Expected: recent commits include:
- spec commit
- chore: ignore Notion sync config and state files
- docs(content): archive pipeline.md
- docs(content): point content-index at Notion
- docs(content): log Notion migration

- [ ] **Step 5: End-to-end smoke test**

Run a full content cycle:
1. Capture a new idea directly in Notion (mobile or web) → row appears with Status=Idea
2. Run `/content` (no args) → idea is promoted to Status=Drafting with generated body
3. Edit the draft in Notion → save
4. Manually mark Status=Ready, then Status=Scheduled with a Scheduled date
5. Confirm the calendar view shows the upcoming post
6. Mark Status=Published manually after posting, fill Published URL
7. Confirm the Published log view shows it

- [ ] **Step 6: Tell Juan the migration is complete**

Summary message:
- Three skills work: `/content`, `/content-research`, `/content-sync`
- All operational data is in Notion
- Knowledge wiki canonical in local markdown, mirrored read-only to Notion
- Pipeline.md is historical; new pipeline tracking is in Notion
- Mobile access enabled via Notion mobile app
- Document any rough edges discovered during testing for follow-up

---

## Follow-up (out of scope but worth tracking)

These are explicitly deferred per the spec — log them for later:

- Two-way sync for knowledge wiki (community CLI or custom Worker)
- Auto-fetched engagement metrics (Notion Worker, free until Aug 11, 2026)
- Scheduled publishing (Worker → platform APIs)
- "Repurposed from" self-relation on Content DB
- GitHub-triggered sync via post-commit hook
