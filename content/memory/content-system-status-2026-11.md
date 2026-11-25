---
title: Content System — What Already Runs (2026-11-25)
description: Status check before building the five-platform system. Scheduler live, all accounts connected, Notion gaps, broken local Notion key.
author: claude
created: 2026-11-25
updated: 2026-11-25
---

# What already runs (checked 2026-11-25)

Build plan: `docs/superpowers/plans/2026-11-25-five-platform-content-system.md`. Decisions: `content/wiki/content-system-decisions.md`.

## Works
- Notion → post-bridge sync is live on Railway (project jcg-content-sync), running every 5 minutes, latest deploy succeeded today.
- post-bridge has all accounts connected: LinkedIn (Juan Cruz Giusto), X (JCGiusto), Instagram (jc.giusto), TikTok, YouTube, plus Threads (jc.giusto).
- The sync already maps all six accounts. Last posts went out through it on 2026-11-16.
- Notion Content DB already has platform options Instagram, TikTok, YouTube, Threads, and a Type field (Thread, YouTube Video, Short, Carousel, Resource, Podcast, Authority, Infographic, Personal Post). Statuses: Idea → Researching → Drafting → Ready → Scheduling → Scheduled → Published / Failed.
- Notion Content DB (2026-11-25, Task 5): new fields Format (the twelve formats), Source piece / Versions (two-way link from each platform version to its source), Views, Comments, Saves, Follows, Signups. Spotify platform removed (unused); Blog kept. No separate Slot field — the Date field is the posting time, because the scheduler reads it. New view "This week" (next 7 days, board; switch its date grouping to Day by hand in Notion).
- Notion Swipes DB (new, under Content OS): Brand, Screenshot, What's good, Could feed (the twelve formats), Used?. View "Swipes unused".
- `/content` STEP 6 files drafts through the Notion connector: one source row plus one row per platform, Status Drafting, Date = slot. Tested with two rows, then trashed.

## Missing or broken
- The local Notion key in `content/.notion-config.json` is rejected ("token is invalid"). Juan's call (2026-11-25): don't renew it — use the Notion connector (MCP tools) for all Notion work, including schema changes and filing drafts. `/content` STEP 6 now files through the connector (done 2026-11-25). The Railway sync has its own key and is unaffected.
- Video posting (Reels, TikTok, Shorts, YouTube long) through the sync has never been tested.
- Not yet known: post-bridge plan and price; whether it supports recycling old X posts and automatic self-replies.
- Threads: Juan decided (2026-11-25) it gets a copy of every X post.
