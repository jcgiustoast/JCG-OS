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

## Missing or broken
- The local Notion key in `content/.notion-config.json` is rejected ("token is invalid"). Juan's call (2026-11-25): don't renew it — use the Notion connector (MCP tools) for all Notion work, including schema changes and filing drafts. `/content` STEP 6 should be switched from `notion-content.ps1` to the connector. The Railway sync has its own key and is unaffected.
- Notion Content DB lacks: format (ranking, checklist…), a link from each version to its source piece, result numbers, and a swipes database.
- Video posting (Reels, TikTok, Shorts, YouTube long) through the sync has never been tested.
- Not yet known: post-bridge plan and price; whether it supports recycling old X posts and automatic self-replies.
- Threads: Juan decided (2026-11-25) it gets a copy of every X post.
