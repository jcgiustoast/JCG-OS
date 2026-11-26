---
description: Sunday plan for next week's five-platform posts — fill each slot from Notion ideas, screen brands, filming list, hours, winners due back; writes to Notion only after approval
---

Weekly plan for the five-platform content system. Run it on Sunday, AFTER `/week-review`. READ-ONLY until Juan approves a shown list of writes.

Today is {{date}}. "Next week" = the Monday to Sunday that starts tomorrow (Madrid time).

## Before you start

- Notion ONLY through the Notion connector (`notion-*` MCP tools; load with ToolSearch). Never `content/.notion-config.json` or `content/scripts/`.
- Content table: `collection://36aeedc9-595f-81f9-88f2-000b60546d69`. Never write Post Bridge ID, Last Sync At, Synced Edit Token or Published URLs. The Date field is the posting time, and the scheduler reads it.
- Read: the weekly calendar and ramp in `content/wiki/content-strategy.md` (Phase 1 "Channels & Cadence"); formats and time per format in `content/wiki/engine/content-types.md`; chains and winners-come-back rules in `content/wiki/engine/repurpose.md`; this week's `/week-review` entry at the top of `content/memory/log.md` (if it's missing, say so and plan without it).
- Ideas come from Juan. Never invent topics to fill a slot.
- Talk to Juan in plain words (CLAUDE.md "Plain Speech"): "Monday's LinkedIn carousel", not a slot code.

## Steps

1. **Ramp week.** Read "Ramp week one starts" in `content/wiki/content-system-decisions.md`. If it's missing, ask Juan for the Monday his week one starts. On his answer, add the line to the "Volume and timing" table and set `updated:`. Next week's number = weeks since that Monday + 1.
2. **Open slots.** Take the calendar and keep only the slots open in that ramp week:

   | Ramp week | Open slots |
   |---|---|
   | 1 | LinkedIn: Mon carousel, Tue long personal, Thu long framework. X: one post Mon–Fri at 13:55 ET / 19:55 Madrid, a second at 19:00 ET / 01:00 Madrid where ideas allow, Sunday life-lesson list |
   | 2 | Week 1 + vertical video Mon and Fri (Reel + TikTok + Short, same file), Instagram carousel Tue and Thu (Monday's and Wednesday's LinkedIn carousel), Instagram story daily |
   | 3 | Full LinkedIn (5 a week), full X (~12 a week), three videos (Mon, Wed, Fri) |
   | 4 and after | Full calendar: YouTube long on Tuesday, Resource post on LinkedIn every other Friday |

   Show this row to Juan as part of the plan, so he can change it.
3. **Ideas and the brand check.** Query all rows with Status = Idea (title, notes, format, platform, created). For every brand or person named in an idea, check the hard limits:
   - no Mars Men numbers, tests or implementations;
   - no ASTEROI client names or numbers;
   - no men's-health, hormone, testosterone or men's-supplement brands in rankings or studies;
   - no Meta ads, creative or ad-spend advice.
   If you aren't sure what a brand sells, look it up before placing it. A flagged idea gets no slot. List it with the reason.
4. **Fill the slots.** Match each slot to an idea whose format fits. If an idea has no format, suggest one from `content-types.md`. Give the stronger slots (Monday, Wednesday, the video slots) to the formats that did best in the review. Oldest ideas go first when two fit equally. For each slot, list its sister versions from the chains: a carousel → LinkedIn PDF, Instagram the next morning, X images; a video → Reel, TikTok, Short. Check each sister against the platform limits table before planning it.
5. **Empty slots.** List every slot with no fitting idea, and ask Juan for ideas: `Give me ideas for these and I'll place them.`
6. **Filming list.** Every vertical video of the week, plus the YouTube long from week 4, in shooting order for one sitting: the idea, the format and what to have ready (screenshots from the brand's live site, the script).
7. **Hours.** Add up the time per format for every planned piece (sisters made from the same file add only caption time). Compare with the ramp week's hours (week 1: 8–10, week 2: 13–16, week 3: 20–25, week 4: 27–37). If it's over, say what to drop.
8. **Winners due back.** Query Status = Published with "Can come back on" on or before next Sunday. For each: the post, platform, when it first ran, its numbers and how it comes back (X word for word; LinkedIn needs a new first line or a carousel rebuild; video re-uploaded or refilmed).
9. **Re-check list.** For next week's pieces that already have versions (Versions not empty), fetch the source and each version. List any version last edited before its source, so Juan re-checks it matches.

## Show the plan

One message:
- the ramp row being used;
- a day-by-day table (day, time Madrid, platform, format, idea, sister versions);
- ideas held back by the brand check, with the reason;
- empty slots;
- filming list;
- hours against the target;
- winners due back;
- versions to re-check.

Then ask: `Write these dates and formats to Notion, and copy the winners?`

## On Juan's yes

- For each placed idea: set Date (the slot's posting time, Madrid) and Format on its row. Status stays Idea. `/content` drafts it and creates the sister rows.
- For each approved winner: create a new row with the same Title, Platform, Format, Type and page text, a new Date, Status Drafting, and Notes "Repost of <old row link>". If the Media files can't be copied through the connector, say so; Juan re-attaches them. Clear "Can come back on" on the old row. Flag LinkedIn reposts: they need a new first line before they're marked Ready.
- Report what was written, with links.

## Rules

- Never write to Notion or any file without a yes on the exact list shown.
- Never schedule by hand. Every evening slot (19:00 Madrid and later) goes through the scheduler.
- Weekends: only the Sunday X post and the daily Instagram story.
- Keep the chat output under ~500 words, plus the tables.
