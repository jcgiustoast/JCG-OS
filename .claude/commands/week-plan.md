---
description: Sunday plan for next week's five-platform posts — fill each slot from Notion ideas, screen brands, filming list, hours, winners due back; writes to Notion only after approval
---

Weekly plan for the five-platform content system. Run it on Sunday, AFTER `/week-review`. READ-ONLY until Juan approves a shown list of writes.

Today is {{date}}. "Next week" = the next Monday to Sunday (Madrid time). On a Sunday that is the week starting tomorrow.

## Before you start

- Notion ONLY through the Notion connector (`notion-*` MCP tools; load with ToolSearch). Never `content/.notion-config.json` or `content/scripts/`.
- Content table: `collection://36aeedc9-595f-81f9-88f2-000b60546d69`. Never write Post Bridge ID, Last Sync At, Synced Edit Token or Published URLs. The Date field is the posting time, and the scheduler reads it. X is called "Twitter" in the Platform field.
- Read: in `content/wiki/content-strategy.md` (Phase 1 "Channels & Cadence"), the parts **Weekly calendar (v2, 2026-11-26)**, **What Juan creates each week**, **How each piece spreads**, **Two-week topic cycle** and **First four weeks**; formats and time per format in `content/wiki/engine/content-types.md` (if the notes-app list, brand verdict, framework carousel or infographic aren't there yet, use "What Juan creates each week"); chains and winners-come-back rules in `content/wiki/engine/repurpose.md`; this week's `/week-review` entry at the top of `content/memory/log.md` (if it's missing, say so and plan without it).
- Brand pages: through Claude in Chrome only (`mcp__claude-in-chrome__*` tools; load with ToolSearch), in a new tab of Juan's Chrome.
- Ideas come from Juan. Never invent topics to fill a slot.
- Talk to Juan in plain words (CLAUDE.md "Plain Speech"): "Monday's LinkedIn carousel", not a slot code.

## Steps

1. **Ramp week.** Read "Ramp week one starts" in `content/wiki/content-system-decisions.md`. If it's missing, ask Juan for the Monday his week one starts. On his answer, add the line to the "Volume and timing" table and set `updated:`. Next week's number = weeks since that Monday + 1.
1b. **Topic and week A or B.** One topic runs for two weeks (week A, then week B), per **Two-week topic cycle**. Query the rows placed most recently (latest Dates) and read "Topic: …" in their Notes. If that topic's first rows are dated last week, next week is its week B. If it has already run two weeks, or no row has a topic, next week is week A of a new topic: propose the next one from "First four topics" and ask Juan to confirm. If the Notes don't settle it, ask Juan. Then find the topic's resource and keyword. If the topic has no resource yet, say so and reuse the Subscription Checklist (keyword CHECKLIST). Week A: from ramp week 4, Thursday's framework carousel comes from Tuesday's YouTube video. Week B: Friday is the Resource post, plus an Instagram keyword Reel with a new keyword for the same resource.
2. **Open slots.** Take **Weekly calendar (v2, 2026-11-26)** (times from it, Madrid) and keep only the slots open in that ramp week, per **First four weeks**:

   | Ramp week | Open slots |
   |---|---|
   | 1 | LinkedIn: Mon checklist carousel, Tue long post, Thu framework carousel. X: daily brand verdict, notes lists, quote reactions, Sunday list |
   | 2 | Week 1 + 2 videos (Mon, Fri), Instagram carousels + stories, Wednesday carousel, keyword auto-DM |
   | 3 | Everything except YouTube and the Resource post: 4 videos, LinkedIn 6 |
   | 4 and after | Full calendar: + YouTube long, first Resource post (then every other Friday), first format-cut review |

   Ramp week 1 plans no videos, no Instagram carousels and no YouTube. Show this row to Juan as part of the plan, so he can change it.
3. **Ideas and the brand check.** Query all rows with Status = Idea (title, notes, format, type, platform, created), then fetch each idea's page: brands, sources and framing rules are often only in the page text. Rows with the same title are one idea already split by platform: place each row on its own platform and don't plan new sister rows for platforms it already has. Rows on Blog have no weekly slot; list them apart as "for the monthly jcgiusto.com piece". For every brand or person named in an idea, check the hard limits:
   - no Mars Men numbers, tests or implementations;
   - no ASTEROI client names or numbers;
   - no men's-health, hormone, testosterone or men's-supplement brands in rankings or studies;
   - no Meta ads, creative or ad-spend advice.
   If you aren't sure what a brand sells, look it up before placing it. A flagged idea gets no slot. List it with the reason. If its page already carries a framing rule meant to keep it inside the limits (for example "share the belief, never the number or the implementation"), quote that rule next to it, so Juan can clear it himself.
3b. **Brand pages.** Find 5 real brand pages in Juan's Chrome, one per weekday brand verdict. Page types: product page, subscribe box, checkout, cart drawer, upsell; pick the ones that fit the week's topic (subscription week → subscribe boxes; checkout week → checkouts). Screen each brand against the hard limits in step 3 first, before it goes on any list; if you aren't sure what a brand sells, look it up. Drop a flagged brand and say why. Then screenshot each page from the live site and show the shortlist: brand, page type, link, screenshot. Juan writes the verdicts (1–2 lines each). Claude never writes a verdict.
4. **Fill the slots.** Match each slot to an idea whose format fits, on the week's topic (brand pages, notes lists and videos are chosen on the topic; ask Juan for notes lists on it). If an idea has no format, suggest one from `content-types.md`. Some pieces have no Format option of their own in Notion; set what this table says:

   | Slot | Set in Notion |
   |---|---|
   | LinkedIn long post | Type = Personal Post (life/career story) or Authority (idea). Say "photo of Juan" (story) or "infographic" (idea) in the plan |
   | Brand verdict (single image) | Format = Pages worth stealing, Type = Infographic |
   | Notes-app list (screenshot) | Format = Checklist, Type = Infographic |
   | Framework carousel | Type = Carousel |
   | Wednesday "Pages worth stealing" carousel | Format = Pages worth stealing |
   | Monday checklist carousel | Format = Checklist |
   | X Sunday life-lesson list | Type = Thread |

   **Resource Friday:** the Resource post runs every other Friday, from ramp week 4. Find the last row with Format = Resource and read its Date: the next Resource Friday is two weeks after it. If there's no such row, the first one is ramp week 4's Friday. On a non-Resource Friday, LinkedIn gets the week's best brand verdict or a notes-list image.

   Give the stronger slots (Monday, Wednesday, the video slots) to the formats that did best in the review. Oldest ideas go first when two fit equally. For each slot, list its sister versions per **How each piece spreads**:
   - Long post → LinkedIn Tue (+ photo or infographic) → one long single X post Wed (no threads).
   - Brand verdict (×5) → X image same day → Instagram story → best one as a LinkedIn image (Fri, non-Resource weeks) → all five into Wednesday's carousel → Instagram Thu → X images Wed.
   - Notes list (×3) → X image → one expanded into next Monday's checklist carousel → Instagram the same day → X images Fri.
   - Framework (×1) → Thursday carousel (Figma, `/figma-post`), on the topic; in video weeks it comes from Tuesday's video → one summary infographic → Instagram (Fri, per the calendar) + X Mon. Last slide: "Comment [KEYWORD]" for the topic's resource.
   - Video (×4) → same file to Reel, TikTok, Short, X; caption per platform.
   - Quote reactions → X only.
   - From Notion ideas → Claude drafts Monday's contrarian take and the Sunday life-lesson list; Juan approves.
   - Free copies → Threads (every X post); X images to Instagram weeks later; old X winners auto-repost.

   Every carousel's last slide and every Instagram caption carries the topic's keyword. Check each sister against the platform limits table before planning it.
5. **Empty slots.** List every slot with no fitting idea, and ask Juan for ideas: `Give me ideas for these and I'll place them.`
6. **Filming list.** Every vertical video of the week, in shooting order for one sitting: at full speed 4 videos, 3 one-page teardowns + 1 ranking or roundup (a new ranking each month), all on the topic; ramp week 2 has 2. Plus the YouTube long from week 4. For each: the idea, the format and what Claude preps (the pages, screenshots from the brand's live site, the script). In week B, one Reel ends "Comment [KEYWORD]".
7. **Hours.** Add up Juan's time for every planned piece, per **What Juan creates each week**: long post 1–1.5 h; 5 brand verdicts ~30 min; 3 notes lists ~1 h; framework ~1 h; 4 short videos ~3.5 h; 3 quote reactions ~30 min; X replies ~1.75 h; YouTube long 10–18 h. Sisters made from the same piece add only caption time. Compare with the ramp week's hours (week 1: ~7–8, week 2: ~11–13, week 3: ~14–16, week 4 and after: ~24–29; limit 27–37). If it's over, say what to drop.
8. **Winners due back.** Query Status = Published with "Can come back on" on or before next Sunday. For each: the post, platform, when it first ran, its numbers and how it comes back (X word for word; LinkedIn needs a new first line or a carousel rebuild; video re-uploaded or refilmed).
9. **Re-check list.** For next week's pieces that already have versions (Versions not empty), fetch the source and each version. List any version last edited before its source, so Juan re-checks it matches.

## Show the plan

One message:
- the ramp row being used;
- the topic, week A or B, its resource and keyword (and whether next Friday is a Resource Friday);
- the brand page shortlist, waiting for Juan's verdicts, and any brand dropped by the screen;
- a day-by-day table (day, time Madrid, platform, format, idea, sister versions);
- ideas held back by the brand check, with the reason;
- empty slots;
- filming list;
- hours against the target;
- winners due back;
- versions to re-check.

Then ask: `Write these dates and formats to Notion, and copy the winners?`

## On Juan's yes

- For each placed idea: set Date (the slot's posting time, Madrid) and Format and/or Type (per the table in step 4) on its row, and add "Topic: <topic> · Keyword: <WORD>" to its Notes (keep what's already there). Every placed piece gets that Notes line; show it in the write list. Status stays Idea. `/content` drafts it and creates the sister rows.
- For each approved winner: create a new row with the same Title, Platform, Format, Type and page text, a new Date, Status Drafting, and Notes "Repost of <old row link>". If the Media files can't be copied through the connector, say so; Juan re-attaches them. Clear "Can come back on" on the old row. Flag LinkedIn reposts: they need a new first line before they're marked Ready.
- Report what was written, with links.

## Rules

- Never write to Notion or any file without a yes on the exact list shown.
- Never schedule by hand. Every evening slot (19:00 Madrid and later) goes through the scheduler.
- Weekends: only the Sunday X post and the daily Instagram story.
- Keep the chat output under ~500 words, plus the tables.
