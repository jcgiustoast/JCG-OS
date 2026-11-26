# Weekly Content v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Put the approved weekly content v2 (what Juan creates, how each piece spreads) into the pages and the Sunday plan command that run the system.

**Architecture:** Markdown only. The calendar lives in `content/wiki/content-strategy.md`; decisions in `content/wiki/content-system-decisions.md`; `/week-plan` reads both. Two pages are `author: juan` and only get proposed wording in chat.

**Tech Stack:** Markdown in the JCG-OS vault; git.

**Spec:** `docs/superpowers/specs/2026-11-26-weekly-content-v2-design.md`

## Global Constraints

- Hard limits stay word for word: no Mars Men numbers, tests or implementations · no ASTEROI client names or numbers · no men's-health, hormone, testosterone or men's-supplement brands · no Meta ads, creative or ad-spend advice.
- Never edit `author: juan` pages (`content/wiki/engine/content-types.md`, `content/wiki/engine/repurpose.md`); show wording in chat.
- Every edited page: `updated: 2026-11-26`; changelog line at the bottom where the page has one.
- Weekends: Sunday X post + daily Instagram story only. Evening slots (19:00 Madrid and later) through the scheduler.
- Times in Madrid, matching the spec's week table exactly.

## Review Focus

- `/week-plan` run in ramp week 1 must not plan videos, Instagram carousels or YouTube → its ramp table must match the spec's ramp table.
- The Resource post alternates weeks → `/week-plan` must say how it knows which Friday (from the last Resource row's Date in Notion).
- Brand pages found by Claude in Chrome still pass the hard-limit screen before Juan sees them → `/week-plan` step must screen before the shortlist.
- Old calendar text left behind in `content-strategy.md` would give two conflicting calendars → grep check in Task 1.
- Notes lists and brand verdicts have no Format option in Notion → `/week-plan` slot table says what to set (Type = Infographic for single images, Format = Pages worth stealing for brand verdicts, Format = Checklist for notes lists).

---

### Task 1: Calendar and decisions pages

**Files:**
- Modify: `content/wiki/content-strategy.md` — section "### Channels & Cadence (revised 2026-11-25 …)": replace the "Per week at full speed" table, the "Weekly calendar" table and the "First four weeks" table.
- Modify: `content/wiki/content-system-decisions.md` — "## Volume and timing" table + "### Changelog".

**Interfaces:**
- Produces: heading `**Weekly calendar (v2, 2026-11-26)**`, heading `**What Juan creates each week**`, heading `**How each piece spreads**`, heading `**Two-week topic cycle**`, heading `**First four weeks**` — `/week-plan` (Task 2) points at these by name.

- [ ] **Step 1:** Replace the channel table's counts with the spec totals (X ~21 + reposts, LinkedIn 6, Instagram 8 + stories, TikTok 4, YouTube 1 long + 4 Shorts).
- [ ] **Step 2:** Replace the weekly calendar with the spec's "The week" table, copied exactly; add "What Juan creates each week" and "How each piece spreads" from the spec; add "Two-week topic cycle" from the spec's "How it all connects" section (Juan's version table, Resources, First four topics) — Max's findings stay in the spec, not the page; replace "First four weeks" with the spec's ramp table.
- [ ] **Step 3:** Add rows to "Volume and timing": the 2026-11-26 decisions from the spec's "Decisions" list (Max's way; screenshots = brand page + verdict or notes list, Claude finds pages; weekly framework carousel; long post image matches the post; one topic every two weeks, every keyword sends that topic's resource, resources hub on jcgiusto.com; kept: weekends off, 15 min replies, Threads). "Given by: Juan". Changelog line.
- [ ] **Step 4: Verify** — `grep -n "13:55/19:55 carousel: checklist\|quick fix" content/wiki/content-strategy.md` → no lines (old calendar gone); `grep -c "Weekly calendar (v2, 2026-11-26)" content/wiki/content-strategy.md` → 1.
- [ ] **Step 5: Commit** `update content-strategy.md, content-system-decisions.md — weekly content v2 calendar, creation list, ramp, decisions`

### Task 2: `/week-plan` fills the v2 week

**Files:**
- Modify: `.claude/commands/week-plan.md` — "## Before you start", steps 2, 4, 6, 7.

**Interfaces:**
- Consumes: the four headings from Task 1.

- [ ] **Step 1:** Step 2 ramp table → the spec's ramp table (week 1/2/3/4+ contents).
- [ ] **Step 2:** New step after step 3, "Brand pages": find 5 brand pages in Juan's Chrome (product page, subscribe box, checkout, cart drawer, upsell), screen each brand against the hard limits first, screenshot from the live site, show the shortlist; Juan writes the verdicts.
- [ ] **Step 3:** Step 4 slot→Notion table: brand verdict → Format Pages worth stealing, Type Infographic; notes list → Format Checklist, Type Infographic; framework carousel → Type Carousel; long post → Type Personal Post (story) or Authority (idea), with "photo of Juan" or "infographic" in the plan; keep existing rows that still apply. Resource Friday: alternate from the last Resource row's Date.
- [ ] **Step 3b:** Topic cycle: new step 1b reads the current topic and whether next week is week A or B (from the last placed rows' Notes "Topic: …" in Notion, or ask Juan); every placed piece gets Notes "Topic: <topic> · Keyword: <WORD>" in the write list; brand pages, notes lists and videos are chosen on the topic; week A Thursday carousel from Tuesday's video (week 4+); week B Friday = Resource post + an Instagram keyword Reel with a new keyword for the same resource. If the topic has no resource yet, say so and reuse the Subscription Checklist.
- [ ] **Step 4:** Sister versions in step 4 → the spec's "How Claude adapts each piece" list.
- [ ] **Step 5:** Step 6 filming list → 4 videos (3 one-page teardowns + 1 ranking/roundup, a new ranking each month); step 7 hours → the spec's per-piece estimates and ramp hours.
- [ ] **Step 6: Verify** — `grep -n "Ramp week\|Brand pages\|Pages worth stealing\|teardown" .claude/commands/week-plan.md` shows each; the four hard-limit lines unchanged (`git diff` shows no edits to them).
- [ ] **Step 7: Commit** `update week-plan — fills the v2 week: brand pages from Chrome, notes lists, framework carousel, new ramp`

### Task 3: Wording for Juan's two pages, and the build plan

**Files:**
- Modify: `docs/superpowers/plans/2026-11-25-five-platform-content-system.md` — Task 12 first item → "Run `/week-plan` for week one of the v2 ramp (spec 2026-11-26)".
- No edit: `content/wiki/engine/content-types.md`, `content/wiki/engine/repurpose.md` (author: juan).

- [ ] **Step 1:** Write in chat the exact text to paste: content-types — new "Notes-app list" and "Brand verdict (single image)" and "Framework carousel" and "Infographic" entries (what it is, platforms, check, time); repurpose — the chains from the spec's adaptation list.
- [ ] **Step 2:** Update five-platform plan Task 12 wording, and add an open item under it: "Resources hub page on jcgiusto.com listing every resource (one-off; separate site task)" and "One short resource per topic, starting with a product page checklist for weeks 3–4".
- [ ] **Step 3: Verify** — `git diff --stat` touches no `author: juan` file.
- [ ] **Step 4: Commit** `update five-platform plan Task 12 — week one follows weekly content v2`, then fast-forward master and push.
