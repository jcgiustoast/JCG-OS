---
title: Content System — What Already Runs (2026-11-25)
description: Status check for the five-platform system. Scheduler live, all accounts connected, what post-bridge can't do (reposting, long YouTube), tool prices, sync fixes pending deploy.
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
- Swipes table: dropped 2026-11-25 (in Notion trash, restorable). No swipe collection — ideas come from Juan in chat.
- `/content` STEP 6 files drafts through the Notion connector: one source row plus one row per platform, Status Drafting, Date = slot. Tested with two rows, then trashed.

## Missing or broken
- The local Notion key in `content/.notion-config.json` is rejected ("token is invalid"). Juan's call (2026-11-25): don't renew it — use the Notion connector (MCP tools) for all Notion work, including schema changes and filing drafts. `/content` STEP 6 now files through the connector (done 2026-11-25). The Railway sync has its own key and is unaffected.
- Video posting (Reels, TikTok, Shorts) through the sync has never been tested. Test pending: needs a short clip from Juan.
- Not yet known: which post-bridge plan Juan is on.
- Threads: Juan decided (2026-11-25) it gets a copy of every X post.

## What post-bridge can and can't do (checked 2026-11-25, public API spec)
- **No reposting.** No recycle or evergreen feature. The repost rule (from ~Feb 2027) runs by hand: the Sunday plan lists posts whose "Can come back on" date has arrived; after Juan's yes, Claude copies them into new Notion rows with a new date.
- **First comment works** on X, LinkedIn, Instagram, Threads, Facebook. So the X self-reply needs no add-on.
- **X links get stripped.** post-bridge silently removes links from X posts. Fix written: links move into the first comment, and the 280-character check counts the text without them.
- **Video limits:** MP4 or MOV, 3 seconds to 5 minutes, up to 500 MB.
- **YouTube long videos can't go through post-bridge** (5-minute cap). Juan uploads those by hand.
- Also available, not used yet: X/Threads threads, TikTok private/draft posting, YouTube title and scheduled publish time, Instagram stories, LinkedIn PDF carousels.

## Tools under $60/month (prices checked 2026-11-25)
- post-bridge Marketer: $39/mo, API included.
- Kit (email for jcgiusto.com): free up to 10k subscribers, freebie delivery included; email sequences from $39.
- ManyChat (Instagram keyword DMs): pricing page blocked, likely ~$15 — Juan to check.
- CapCut: free (Pro €29.99). Captions app $24.99 — skip.
- Total ≈ $54/mo if Juan is on Marketer. Nothing paid or signed up.

## Sync fixes written, not live yet (pending Juan's yes to deploy)
- X posts with links: links go to the first comment (see above).
- YouTube posts get their title from the Notion Title. Empty or over 100 characters → row marked Failed.
- Rows not yet scheduled with a posting time in the next 2 hours get one warning line in Notes ("NOT SCHEDULED").
- Known gap, left on purpose: changing a YouTube title after it's scheduled doesn't reach post-bridge.
