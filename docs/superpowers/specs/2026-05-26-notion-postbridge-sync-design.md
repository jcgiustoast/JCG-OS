# Notion → post-bridge publish sync (v1)

**Date:** 2026-05-26
**Status:** Design — pending implementation
**Author:** Juan Cruz + Claude
**Related:**
- Handoff doc: `C:\tmp\handoff-VnPrsS.md` (ephemeral; key decisions captured below)
- Helper script: `content/scripts/notion-content.ps1`
- post-bridge SKILL: `~/.claude-personal/plugins/cache/post-bridge/post-bridge/1.0.0/skills/post-bridge/SKILL.md`

## Why

Make the **Notion Content DB the source of truth for the content calendar.** post-bridge becomes the executor, not the planner. Today the calendar lives implicitly across Notion drafts + post-bridge's scheduler; this sync unifies it: edit in Notion, post-bridge follows.

This is an architectural decision, not a time-saver. The point is one canonical calendar, not saving the ~2 min/week of manual copy-paste.

## Scope

### In scope (v1)
- One-way calendar sync **Notion → post-bridge** (creates, edits, cancels)
- Status writeback **post-bridge → Notion** (Scheduled → Published / Failed)
- Per-platform published URL writeback (after publish)
- Media upload (Notion Files property → post-bridge media_id)
- Phase 1 firewall re-check at sync time
- Crash-safe state machine via Notion intermediate status

### Out of scope (deferred to v2+)
- Analytics writeback (views, likes, comments, shares)
- Per-platform caption variants (one body = one caption for all platforms in v1)
- Notion webhooks (polling only)
- Spotify and Blog platforms (no post-bridge analog — sync ignores)

## Decisions already locked

1. **Notion = source of truth for the calendar.** Not "save clicks."
2. **Sync direction: one-way + status writeback.** No bidirectional editing.
3. **Runtime: Node.js on Railway.** Cron-based polling.
4. **Multi-platform model: 1:1** — one Notion row → one post-bridge `POST /v1/posts` with `social_accounts: [...]`.
5. **Media handling: Notion Files property.** Download signed URL → upload to post-bridge → store media_id.
6. **Caption source: page body.** Strip `**Sources:**` header that `/content` prepends. Single caption for all selected platforms.

## Architecture

Single Node.js service on Railway. Stateless — Notion + post-bridge hold all durable state. Cron-triggered every 5 minutes.

```
                    ┌─────────────┐
                    │  Railway    │
                    │  cron (5m)  │
                    └──────┬──────┘
                           │ invokes
                           ▼
                    ┌─────────────┐
                    │  tick()     │
                    │  Node.js    │
                    └──┬───────┬──┘
                       │       │
              reads/   │       │   creates/patches/deletes
              writes   ▼       ▼
                  ┌──────┐  ┌────────────┐
                  │Notion│  │post-bridge │
                  │  DB  │  │   API      │
                  └──────┘  └────────────┘
```

No database. No queue. No webhooks. State lives in Notion (`Status`, `Post Bridge ID`) and post-bridge (`status` field on post).

## State machine

`Status` field in Notion drives the sync. State transitions:

```
Idea → Researching → Drafting → Ready
                                  │  (sync sees Ready)
                                  ▼
                              Scheduling   ── intermediate, crash-safe
                                  │  (post-bridge POST succeeds)
                                  ▼
                              Scheduled  + Post Bridge ID writeback
                                  │  (post-bridge reports posted)
                                  ▼
                              Published  + Published URLs writeback

   Any step can land in: Failed (reason captured in Notes field)
```

User-driven transitions:
- `Idea → Researching → Drafting → Ready` — manual, via `/content` skill or directly in Notion
- `Scheduled → Drafting` or `Scheduled → Idea` — user reverts a scheduled post. Sync detects → DELETE in post-bridge → clears `Post Bridge ID`.

Sync-driven transitions (only the sync touches these):
- `Ready → Scheduling → Scheduled` — normal path
- `Scheduled → Published` — on post-bridge `posted`
- `* → Failed` — on any sync-level error

## `tick()` reconciliation loop

Runs every 5 minutes on Railway cron. Single-shot, idempotent within a tick.

```
for row in notion.query(Status ∈ {Ready, Scheduling, Scheduled}):
    case row.Status:
        Ready:
            -> firewall_check(row) -- if blocked: mark Failed, continue
            -> notion.update(row, Status='Scheduling')
            -> media_id = upload_media_if_present(row)
            -> post_id = post_bridge.create({
                   caption, social_accounts, scheduled_at, media: [media_id]
               })
            -> notion.update(row, Status='Scheduled', PostBridgeID=post_id)

        Scheduling:
            -- crash recovery: previous tick crashed between create and writeback
            -> candidate = post_bridge.find_recent_by_caption_hash_and_schedule(row)
            -> if candidate exists:
                   notion.update(row, Status='Scheduled', PostBridgeID=candidate.id)
               else:
                   -- retry the create as if Ready
                   retry as Ready

        Scheduled:
            -> pb_post = post_bridge.get(row.PostBridgeID)
            -> case pb_post.status:
                   posted   -> results = post_bridge.results(row.PostBridgeID)
                               urls = format_per_platform_urls(results)
                               notion.update(row, Status='Published',
                                             PublishedURLs=urls)
                   failed   -> notion.update(row, Status='Failed',
                                             Notes=pb_post.error)
                   scheduled-> -- still pending; check for edits below
                               if notion.last_edited(row) > last_sync_stamp:
                                   post_bridge.patch(row.PostBridgeID, {
                                       caption, scheduled_at, social_accounts
                                   })
```

Edit detection: compare Notion's auto-managed `last_edited_time` (returned on every page read) against `Last Sync At` (a sync-managed property — written on every successful create/patch). If `last_edited_time > Last Sync At`, the row was edited since the last sync — propagate via PATCH. Keeps all state inside Notion; no external store.

Revert/cancel detection: a separate query for rows where `Post Bridge ID` is set AND `Status ∈ {Idea, Drafting, Ready}` (user reverted a Scheduled row). For each: `DELETE` in post-bridge, clear `Post Bridge ID`.

## Schema changes (one-off, applied manually before first sync)

Five changes to the Notion Content DB:

1. **`Status` (select):** add two options: `Scheduling` (sync-internal intermediate) and `Failed`. Keep existing `Ready` — do not rename to `Ready to Publish` (existing `/content` script depends on the current spelling).
2. **`Post Bridge ID` (text):** new property. Stores post-bridge post ID for cancel/edit/poll.
3. **`Media` (files & media):** new property. User attaches images/videos here.
4. **`Published URL` (url) → `Published URLs` (rich text):** changed type. Sync writes formatted multi-line:
   ```
   LinkedIn: https://www.linkedin.com/posts/...
   Twitter: https://twitter.com/...
   Threads: https://www.threads.net/...
   ```
5. **`Notes` (rich text):** new property. Sync writes `Failed`-reason strings here.

Hidden / sync-internal property:

6. **`Last Sync At` (date):** new property. Sync writes timestamp on every successful create/patch. Used for edit detection.

## Caption + media handling

**Caption extraction:**
1. `GET /v1/blocks/{page_id}/children` → recursively flatten to markdown.
2. Strip leading `**Sources:** ...\n\n---\n\n` block (the header `/content` prepends for Juan's reference).
3. Validate per-platform char limits:
   - Twitter: 280 chars → if over, mark `Failed`.
   - LinkedIn, Threads, Instagram, TikTok, YouTube: no hard cap enforced in v1 (post-bridge handles).
4. Pass single caption to post-bridge `POST /v1/posts`.

**Media flow** (only if `Media` property has files):
1. Read row → Notion returns array of file objects with signed URLs (expire ~1h).
2. For each file: download to buffer → `POST /v1/media/create-upload-url` (post-bridge) → `PUT` binary to returned URL → collect `media_id`.
3. Pass `media: [media_id, ...]` to post-bridge post create.

## Platform mapping

Multi-select `Platform` field maps to post-bridge `social_accounts` array. Hardcoded in sync config:

| Notion option | post-bridge account ID | Platform name |
|---|---|---|
| LinkedIn | 25903 | linkedin |
| Threads | 25902 | threads |
| TikTok | 25901 | tiktok |
| YouTube | 25900 | youtube |
| Twitter | 25899 | twitter |
| Instagram | 25898 | instagram |
| Blog | — | (skipped, no post-bridge target) |
| Spotify | — | (skipped, no post-bridge target) |

Account IDs verified live as of 2026-05-26 (from handoff doc). If post-bridge reconnects an account and ID changes, the mapping needs an update.

## Phase 1 firewall

Re-check at sync time (not trust upstream `/content`). Blocklist regex on `title + body` (case-insensitive):

```
/(mars\s*men|meta\s*ads|asteroi\s*founder)/i
```

Match → row → `Status: Failed`, `Notes: "Phase 1 firewall: matched <pattern>"`. No post-bridge call made.

Source of truth for the blocklist: `content/wiki/content-strategy.md`. v1 hardcodes; v2 could read from the file.

## Failure handling + crash safety

### The crash scenarios

1. **Sync crashes between `POST /v1/posts` and Notion writeback.** Without intermediate status, next tick re-creates → duplicate posts.
2. **Notion update fails after post-bridge success.** Same as (1) effectively.
3. **post-bridge call fails.** No state change needed; row stays `Ready`. Next tick retries.
4. **Notion update succeeds but post-bridge call never returns (timeout).** Status is `Scheduling`, post may or may not exist in post-bridge.

### The recovery

**Intermediate `Scheduling` status** + **caption-hash lookup** in post-bridge:

1. Sync sees `Ready` → flip Notion to `Scheduling` first (single Notion PATCH).
2. Then post-bridge POST.
3. On success: flip Notion to `Scheduled` + write `Post Bridge ID`.

On next tick, if any row is still `Scheduling`:
- List post-bridge posts created in the last ~30 minutes.
- Match by `(sha256(caption).slice(0,12), scheduled_at)` tuple.
- If match: claim it — writeback ID + flip to `Scheduled`.
- If no match: retry as if `Ready`.

This is not perfectly idempotent (rare race: two `Ready` rows with identical caption + scheduled_at would collide), but in practice posts have distinct captions. The collision window is also bounded to a single 30-min lookback.

### Notion writeback failures

If post-bridge POST succeeds but the Notion writeback fails (network blip): log + continue to next row. The row stays in `Scheduling`; next tick's recovery step resolves it.

## Configuration

Env vars on Railway:

| Var | Source | Purpose |
|---|---|---|
| `NOTION_TOKEN` | from `content/.notion-config.json` | Notion API auth |
| `NOTION_CONTENT_DB_ID` | from same | Target DB |
| `NOTION_CONTENT_DATA_SOURCE_ID` | from same | Target data source for queries |
| `POST_BRIDGE_API_KEY` | env: `pb_live_HU5jbGRxRDW5XWQyfRVReV` | post-bridge auth |
| `PB_ACCOUNT_LINKEDIN` | `25903` | platform mapping |
| `PB_ACCOUNT_THREADS` | `25902` | |
| `PB_ACCOUNT_TIKTOK` | `25901` | |
| `PB_ACCOUNT_YOUTUBE` | `25900` | |
| `PB_ACCOUNT_TWITTER` | `25899` | |
| `PB_ACCOUNT_INSTAGRAM` | `25898` | |

No file-system state. No DB connection. No queues.

## Cron cadence

**5 minutes.** Lag tolerance: a row marked `Ready` at 09:00 will be in post-bridge by 09:05 latest. Notion → publish total lag never exceeds 5 minutes regardless of when in the cycle the user flips Status.

Per-tick cost (estimated for current volume of ~1-2 posts/week):
- 1 Notion query (small)
- ~0-2 post-bridge writes
- Negligible compute

## File layout (Node.js service)

```
notion-pb-sync/
├── package.json
├── railway.toml          # or similar Railway config
├── src/
│   ├── index.js          # cron entry; calls tick()
│   ├── tick.js           # the reconciliation loop
│   ├── notion.js         # Notion API client (query, update, fetch body)
│   ├── post-bridge.js    # post-bridge API client
│   ├── media.js          # Notion file download → post-bridge upload
│   ├── caption.js        # body → caption (strip header, validate limits)
│   ├── firewall.js       # Phase 1 keyword blocklist
│   └── state.js          # state machine transitions, status enum
└── test/
    ├── tick.test.js
    ├── caption.test.js
    ├── firewall.test.js
    └── ...
```

Repo location: `automation/notion-pb-sync/` inside JCG-OS. Single-repo simplicity; can split into its own repo later if it grows beyond this scope.

## Testing strategy

TDD throughout per Juan's testing rule (80% minimum coverage).

**Unit:**
- `caption.js`: header stripping, char-limit validation, edge cases (empty body, only header, very long body)
- `firewall.js`: regex matches case-insensitive across title + body, no false positives
- `state.js`: valid transitions, illegal transitions raise

**Integration (mocked HTTP):**
- `tick.js` with mocked Notion + post-bridge clients
- Each state transition: `Ready → Scheduling → Scheduled`, edit propagation, revert/cancel, crash recovery via `Scheduling` lookup

**End-to-end (manual, with test data):**
- Create a `Ready` row in Notion → wait 5 min → verify post-bridge has draft → verify Notion writeback
- Edit caption → verify post-bridge PATCH
- Revert to `Drafting` → verify post-bridge DELETE

## Open questions resolved

| Q (from handoff) | Resolution |
|---|---|
| Schema: what's actually in the Content DB? | Audited (see "Schema changes" section). |
| Cron cadence: 5/15 min? | 5 min. |
| Media: Notion attachment or external URL? | Notion Files property, download + upload to post-bridge (media_id, not media_urls). |
| Multi-platform: 1 post w/ many accounts, or N posts? | 1:1. |
| Failure handling / idempotency? | `Scheduling` intermediate status + caption-hash recovery lookup. |
| Phase 1 firewall: trust upstream or re-check? | Re-check at sync time. |

## What's explicitly NOT changing

- `/content` skill (the local drafting flow): untouched. Continues to write rows as `Drafting`. The user then flips `Drafting → Ready` to trigger the sync.
- `notion-content.ps1`: untouched (no `Ready` rename means no script edits).
- `notion-sync.ps1`: untouched (different sync, different purpose — Knowledge Mirror).

## Risks + mitigations

| Risk | Mitigation |
|---|---|
| Account ID changes on post-bridge reconnect | Env vars in Railway, easy to bump. Worst case: row goes to `Failed`. |
| Two rows with identical caption + scheduled_at collide in recovery | In practice distinct captions; documented. |
| Notion signed URL expires before media upload completes | Sync downloads immediately at tick time, well under 1h. |
| Phase 1 firewall regex misses a new banned topic | Update the regex; redeploy. |
| post-bridge API rate limits | Single tick = handful of calls; well under any reasonable rate limit. |

## Deployment

1. Apply schema changes manually in Notion (one-off).
2. Push Node.js service to a Railway project.
3. Set env vars (see Configuration).
4. Configure Railway cron (5 min).
5. Deploy → first tick runs.
6. Test with a single `Ready` row, observe full Ready → Scheduled → Published cycle.

Initial monitoring: Railway logs only. If a `Failed` row appears, read `Notes`.
