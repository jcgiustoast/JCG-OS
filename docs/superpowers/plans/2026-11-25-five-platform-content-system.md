# Five-Platform Content System — Build Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Juan's five-platform weekly calendar (LinkedIn, X, Instagram, YouTube, TikTok) runnable: strategy written down, every format templated, ideas and drafts flowing through Notion, posts scheduled automatically, one free guide collecting emails, and a weekly loop that reviews results.

**Architecture:** Reuse what exists. Notion Content DB stays the single place a piece lives (idea → draft → ready → scheduled → published → results). The existing Notion → post-bridge sync (`automation/notion-pb-sync/`) is the scheduler path, extended to the three new platforms if needed. Wiki pages in `content/wiki/engine/` and `content/wiki/platforms/` are the reference the `/content` command reads. Visual templates come from `/figma-post`.

**Tech Stack:** Markdown wiki pages, Notion via the Notion connector (MCP tools — Juan chose this over renewing the local key, 2026-11-25), Node.js sync service on Railway (vitest), Figma (via `/figma-post`), post-bridge, ManyChat (Instagram), an email tool for jcgiusto.com.

**Spec:** `content/wiki/content-system-decisions.md` (Juan's answers) + `content/raw/research/max-wellcopy-2026-11/playbook.md` sections 4, 5, 9, 10.

## Global Constraints

- Every user-facing text (posts, bios, guide, emails, signup page, strategy page wording) is drafted by Claude and approved by Juan before it is written, published or pasted. Notion schema changes and any paid tool are shown to Juan before they happen.
- Hard limits on every piece: no Mars Men numbers, tests or implementations; no ASTEROI client names or numbers; no men's-health, hormone, testosterone or men's-supplement brands in rankings or studies; no Meta ads, creative or ad-spend advice.
- ASTEROI is not named publicly until spring 2027.
- Bio line: "Head of eCommerce at a $100M subscription brand" — Mars Men is not named in bios.
- Audience: DTC founders, $2–50M a year. Topics: CRO, subscriptions, unit economics, measurement, landing pages, Claude for CRO.
- Goal of every funnel: the email list (signup page on jcgiusto.com). MentorPass is the one paid link.
- Tools total under $60/month. No paid tool sponsorships. No editor until after month one.
- Weekends: one Sunday post on X only. Daily: 15 min of X replies (via `/engage`).
- Filming: Juan on camera at his desk, no green screen.
- Handles: jcgiusto on TikTok, X, YouTube, LinkedIn; jc.giusto on Instagram.
- Vault rules: `raw/` immutable; `updated:` set on every write; never edit `author: juan` pages without his say-so; ask before every commit.
- Drafts sound like Juan (memory `writing-voice.md`, `/humanize`).

## Review Focus

- A piece cross-posted from one source breaks another platform's limits (X 280 chars, LinkedIn PDF carousel, TikTok/Shorts length, Instagram 10-slide max) → each platform version is checked against its limit before it is marked Ready (Task 4 limits table, Task 7 sync validation).
- A ranking or brand study slips in a men's-health or supplement brand → every brand list is screened against the hard limits before drafting (Task 4 checklist line, Task 11 review step).
- The 01:00 Madrid slots (7pm ET) are missed when posting by hand → every evening slot is scheduled, never "live" (Task 2 calendar, Task 7).
- Someone comments the keyword on LinkedIn or X and never gets the guide → a daily keyword check is part of the 15-minute reply block, with a saved reply (Task 8).
- The source piece is edited after its five versions exist and they drift apart → Notion "Source piece" link lets the weekly plan list siblings to re-check (Task 5, Task 11).

---

### Task 1: Check what already runs

**Files:** Create `content/memory/content-system-status-2026-11.md` (author: claude, short).

- [ ] Check whether the Notion → post-bridge sync is deployed on Railway and running (Railway tools: list services, recent logs).
- [ ] Check which accounts are connected in post-bridge and whether post-bridge supports Instagram Reels + carousels, TikTok, YouTube (long + Shorts), LinkedIn PDF, X threads/images, evergreen recycling and auto self-replies — from post-bridge docs and its API.
- [ ] Read the Notion Content DB schema (properties, select options) and the Research DB.
- [ ] Write the status note: what works, what's missing, current post-bridge plan and price.
- [ ] Show Juan the note in plain words. No changes yet.

### Task 2: Rewrite the near-term posting plan

**Files:** Modify `content/wiki/content-strategy.md` — Phase 1 "Channels & Cadence" and "What NOT to Post" only; changelog line.

- [ ] Draft the new Phase 1 table: five platforms, weekly volume per platform, purpose, from playbook section 10. Keep jcgiusto.com 1/month; ASTEROI blog stays paused.
- [ ] Add the weekly calendar (playbook section 10, every evening slot marked scheduled) and the 4-week ramp with hours (8–10 → 13–16 → 20–25 → 27–37; first YouTube long in week 4).
- [ ] Add to "What NOT to Post": paid tool sponsorships while at Mars Men; men's-health brands in rankings; Mars Men named in bios.
- [ ] Add "Funnel" paragraph: email list via jcgiusto.com, MentorPass as the one paid link.
- [ ] Show Juan the exact new text; write only after his yes. Set `updated: <today>`, add changelog.

### Task 3: Playbooks for the three new platforms

**Files:** Create `content/wiki/platforms/instagram.md`, `youtube.md`, `tiktok.md` (author: claude, same shape as `platforms/linkedin.md`). Modify `platforms/linkedin.md`, `platforms/twitter.md` (cadence sections only).

- [ ] Each new page: what works on the platform (from `content/raw/research/max-wellcopy-2026-11/<platform>/findings.md`), formats Juan uses there, posting slots, length/size limits, caption and hashtag rules, what not to copy (playbook section 8).
- [ ] Update LinkedIn and X cadence to match Task 2.
- [ ] Add the three pages to `content/wiki/content-index.md`.
- [ ] Juan approves before write.

### Task 4: Format catalog and one-to-five chains

**Files:** Modify `content/wiki/engine/content-types.md`, `content/wiki/engine/repurpose.md`, `content/wiki/engine/hooks.md`.

- [x] Add one entry per format from playbook section 9: ranking ladder, 10/10 to steal, non-negotiables list, brand study, yearly how-to, mega-class, life-lesson list, learning diary, keyword lead magnet, contrarian, quote reaction, live brand fix. Each entry: structure (beat by beat), draft hook pattern, platforms, hard-limit check line, time cost.
- [x] Add a platform limits table (characters, slides, video length, aspect ratio) used before any piece is marked Ready.
- [x] Rewrite `repurpose.md` chains: vertical video → Reel + TikTok + Short; carousel → LinkedIn PDF + IG carousel + X images; YouTube long → cut-downs + LinkedIn lead magnet; X winners recycled after ~6 months. Keep Juan's existing long-form-first chain.
- [x] Add Max-derived hook patterns to `hooks.md`, rewritten as patterns, no copied lines.
- [x] Update `/content` (`.claude/commands/content.md`) platform list to five and point it at the new pages.
- [x] Juan approves before write.

### Task 5: Notion Content DB for five platforms

**Files:** Notion schema (via the Notion connector); modify `.claude/commands/content.md` STEP 6 to file drafts through the connector instead of `content/scripts/notion-content.ps1`.

- [x] Propose schema changes to Juan: Platform options + Instagram, YouTube, TikTok (remove stale ones if unused); new `Format` select (Task 4 names); `Source piece` relation to the same DB (links the five versions to their source); `Slot` date-time; result numbers `Views`, `Comments`, `Saves`, `Follows`, `Signups`; `Swipes` database (screenshot, brand, what's good, format it could feed, Used? checkbox).
- [x] Apply after Juan's yes, with the Notion connector.
- [x] Switch `/content` filing to the connector, with Format, Source piece and Slot set; file one test row, then move it to trash.
- [x] Add a "This week" view grouped by day and a "Swipes unused" view.

### Task 6: Swipe intake — DROPPED (2026-11-25)

Juan's call: no raw-material collection. Ideas come from Juan; research comes from Max Wellcopy and other DTC thought leaders. The Notion Swipes table was moved to Notion's trash (restorable). No inbox change, no brand list.

### Task 7: Scheduling all five platforms

**Files:** `automation/notion-pb-sync/` (worktree, branch `feat/five-platform-sync`), only if Task 1 shows gaps.

- [x] Show Juan a tool table within $60/month: post-bridge plan, ManyChat (IG keyword DMs), email tool for jcgiusto.com, CapCut/Captions. Current prices checked on each site. Nothing paid until he says yes; account sign-ups are his. (Shown 2026-11-25: ≈$54/mo if on post-bridge Marketer; Juan to confirm his plan and ManyChat price. Table in `content/memory/content-system-status-2026-11.md`.)
- [x] If the sync lacks Instagram/TikTok/YouTube or video media: write failing vitest tests first for each new platform mapping (post type, media, caption limit rejection), then implement in `src/post-bridge.js` / `src/media.js`, run `npm test`. (Platforms were already mapped. Added: YouTube title from Notion Title, X links moved to first comment. 96 tests pass.)
- [ ] Video test: post one short clip privately (TikTok private, YouTube private; Reel has no private mode — Juan decides). YouTube long can't go through post-bridge (5-min cap) — upload by hand. **2026-11-26: Instagram Reel passed. TikTok passed after reconnect (private). YouTube still fails ("invalid_grant") after reconnect — re-run YouTube once its connection works.**
- [x] Add evening-slot check: a row with a Slot but no schedule 2 h before → flagged in Notion. (Written: one "NOT SCHEDULED" line appended to Notes. Not deployed.)
- [x] X recycling and auto self-reply plug: use post-bridge if supported; else propose the cheapest add-on inside budget. (Self-reply = post-bridge first comment, no add-on. No recycling in post-bridge → repost rule runs through `/week-plan`, Task 11.)
- [x] Deploy to Railway only after Juan approves; ask before commit/PR. (Deployed 2026-11-25 after Juan's yes; runs clean every 5 min, checked 2026-11-26.)

### Task 8: First resource and email signup

**Changed 2026-11-26:** the format is now called "Resource". The first one is Juan's existing eCom Subscription Checklist (jcgiusto.com/the-ultimate-subscription-ecommerce-checklist/), already behind a name + email form, so no new guide, design or signup page is needed. Obvi (a supplement brand) is named in the checklist — flagged to Juan 2026-11-26, his call.

**Files:** email tool automation; `content/wiki/lead-magnets.md` (author: claude).

- [ ] Find which email tool the checklist page's form uses and what the delivery email says. Juan confirms it still works.
- [ ] Keyword flow: ManyChat on Instagram (keyword "CHECKLIST" → DM with link); LinkedIn and X by hand with one saved reply, checked inside the daily 15-minute block.
- [ ] Test end to end with a test email address Juan supplies.
- [ ] Record the guide, keyword, link and delivery steps in `lead-magnets.md`.

### Task 9: Visual and video templates

**Files:** Figma Contenido file (via `/figma-post`); `content/wiki/engine/templates.md` (author: claude).

- [ ] Carousel card in the post-style look, purple + grey, all three sizes. Agree design + text with Juan before building (memory `feedback-visuals-align-and-airy.md`).
- [ ] YouTube thumbnail template (product shot + one number badge). Juan approves.
- [ ] Reel template spec for CapCut/Captions: caption style, score sticker for rankings, intro length, end card. Juan saves it in the app.
- [ ] YouTube description + pinned comment text template (signup link, MentorPass link). Juan approves.

### Task 10: Bios on all five platforms

**Files:** `content/wiki/bios.md` (author: claude).

- [ ] Draft one bio per platform within each platform's length limit, using the approved bio line, link to the jcgiusto.com signup page and MentorPass; no ASTEROI, no Mars Men name.
- [ ] Juan approves; he pastes them himself (account settings are his). Flag the Spanish-primary LinkedIn profile for him to check.

### Task 11: Weekly plan and weekly review

**Files:** Create `.claude/commands/week-plan.md`, `.claude/commands/week-review.md` (read-only commands; writes to Notion only after approval). Modify `.claude/slash-commands.md`; check `life/wiki/engagement-targets.md` fits $2–50M DTC founders.

- [x] `/week-plan` (Sunday): fill each calendar slot from Notion ideas, list the one-to-five siblings, the filming list for the batch session, and the hours estimate for the week; screen every brand against the hard limits. Also list posts whose "Can come back on" date has arrived; on Juan's yes, copy them into new Notion rows with a new Date (post-bridge has no repost feature).
- [x] `/week-review`: pull last week's results from Notion, compare formats and platforms, list best and worst; in week 4, propose the weakest format to cut. Append summary to `content/memory/log.md` after approval. **2026-11-26: both written (design `docs/superpowers/specs/2026-11-26-weekly-plan-review-design.md`); read-only dry run against Notion done 2026-11-26 (19 ideas, nothing published): fixed the week dates for non-Sunday runs, the "nothing published yet" path, X = "Twitter" in Notion, duplicate rows per platform, slots with no Format option, reading each idea's page for the brand check. Reading numbers in Chrome untested until a post is live.**
- [ ] Propose additions to `engagement-targets.md` for DTC founders in range; Juan approves.

### Task 12: Week-one batch

- [ ] Run `/week-plan` for week one of the ramp: LinkedIn 3, X 1–2/day, first carousel.
- [ ] Draft each piece with `/content`, run `/humanize`, Juan approves each; file to Notion as Ready with Slots.
- [ ] Confirm each scheduled post shows in post-bridge.

---

## Order and dependencies

Task 1 first (it decides Task 7's scope). Tasks 2–4 are writing and can run side by side. Task 5 before 6, 7, 11. Task 9 before 8's design and 12's carousel. Task 12 last.
