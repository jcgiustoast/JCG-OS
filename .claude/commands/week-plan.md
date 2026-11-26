---
description: Sunday plan for next week's five-platform posts — fill each slot from Notion ideas, screen brands, filming list, hours, winners due back; writes to Notion only after approval
updated: 2026-11-26
---

Weekly plan for the five-platform content system. Run it on Sunday, AFTER `/week-review`. READ-ONLY until Juan approves a shown list of writes.

Today is {{date}}. "Next week" = the next Monday to Sunday (Madrid time). On a Sunday that is the week starting tomorrow.

## Before you start

- Notion ONLY through the Notion connector (`notion-*` MCP tools; load with ToolSearch). Never `content/.notion-config.json` or `content/scripts/`.
- Content table: `collection://36aeedc9-595f-81f9-88f2-000b60546d69`. Never write Post Bridge ID, Last Sync At, Synced Edit Token or Published URLs. The Date field is the posting time, and the scheduler reads it. X is called "Twitter" in the Platform field. A 01:00 slot belongs to the night after its day: Monday's 01:00 is Tuesday 01:00 in the Date field.
- Read: in `content/wiki/content-strategy.md` (Phase 1 "Channels & Cadence"), the parts **Weekly calendar (v2, 2026-11-26)**, **Shapes**, **Stories**, **What Juan creates each week, and his hours**, **How each piece spreads**, **Two-week topic cycle**, **First five weeks** and **First-ever week**; in `content/wiki/content-system-decisions.md`, the **Topic cycle** and **Resources and keywords** tables; formats and time per format in `content/wiki/engine/content-types.md` (if the notes-app list, brand verdict, framework carousel or infographic aren't there yet, use the hours table); chains and winners-come-back rules in `content/wiki/engine/repurpose.md` (where it still mentions cutting the long video into Shorts, the strategy page wins: Shorts are filmed on their own); this week's `/week-review` entry at the top of `content/memory/log.md` (if it's missing, say so and plan without it).
- Brand pages: through Claude in Chrome only (`mcp__claude-in-chrome__*` tools; load with ToolSearch), in a new tab of Juan's Chrome.
- Ideas come from Juan. Never invent topics to fill a slot. A piece that comes from a format rather than an idea (the X images of a carousel, the summary infographic, the long X post, the "new video" post, week A's clip, the keyword Reel's row) is not an invented topic: propose a new row for it in the write list.
- Talk to Juan in plain words (CLAUDE.md "Plain Speech"): "Monday's LinkedIn carousel", not a slot code.

## Steps

1. **Ramp week.** Read "Ramp week one starts" in `content/wiki/content-system-decisions.md`. If it's missing, ask Juan for the Monday his week one starts, and put the line in the write list (see "On Juan's yes"). Next week's number = weeks since that Monday + 1. If next week is ramp week 1, it's the first-ever week: use **First-ever week** for the pieces that lean on last week (Monday's carousel from the Resource, no X images of last Thursday's framework, no old X image on Instagram, no week A clip).
1b. **Topic and week A or B.** Read the **Topic cycle** table on the decisions page first: the topic, its start Monday and its keyword. Weeks 1–3 are subscriptions (no A/B; the long post alternates idea and story); from week 4 each topic runs a week A, then a week B. Only if the table doesn't settle it, query the rows placed most recently (latest Dates) and read "Topic: …" in their Notes; if that doesn't settle it either, ask Juan. Then take the topic's Resource and keyword from **Resources and keywords**. If the topic has no Resource yet, say so and reuse the Subscription Checklist (keyword CHECKLIST). If the topic is new, put its start Monday into the Topic cycle row in the write list.
   - From ramp week 4, every week has a long YouTube video on the topic (Tuesday 17:00), and Thursday's framework carousel comes from it. Pick the YouTube idea and the framework together. If Juan hasn't given a YouTube idea for this week of the topic, ask him for one (one per week, two per topic).
   - Week A: if the topic's Resource doesn't exist, put "build [Resource]" on Juan's list, due before week B's Friday (product pages: the product page checklist, during week 4, ready before week 5's Friday).
   - Week B: Thursday 14:00 a clip under 2:20 of week A's video goes on X with a link (X takes 2 min 20 s at most through the scheduler). Friday is the Resource post on LinkedIn, and Friday's video is the keyword Reel (one of the four, not a fifth) with a new keyword for the same Resource. Ask Juan for the new keyword. Put "set up the automatic DM for [KEYWORD]" on Juan's list, due before Friday, and the new keyword row in the write list.
   - Before the first YouTube week (ramp week 3's plan): put "verify the YouTube channel by phone" on Juan's list. Until it's verified, YouTube caps long videos at 15 minutes.
2. **Open slots.** Take **Weekly calendar (v2, 2026-11-26)** (times from it, Madrid) and keep only the slots open in that ramp week, per **First five weeks**:

   | Ramp week | Open slots |
   |---|---|
   | 1 | LinkedIn: Mon checklist carousel, Tue long post, Thu framework carousel. X: daily brand verdict, notes lists, quote reactions, contrarian take, the long X post, carousel images, Sunday list (if lessons) |
   | 2 | Week 1 + 2 videos (Mon, Fri), Instagram carousels + stories, Wednesday carousel, keyword auto-DM for CHECKLIST |
   | 3 | Everything except YouTube and the Resource post: 4 videos, LinkedIn 5 |
   | 4 | + YouTube long (product pages, week A), first format-cut review |
   | 5 and after | Full calendar: + the Resource post and keyword Reel every week B |

   Ramp week 1 plans no videos, no Instagram and no YouTube. The Sunday life-lesson list runs only if Juan has added life lessons to Notion; otherwise skip Sunday. Show this row to Juan as part of the plan, so he can change it.
3. **Ideas and the brand check.** Query all rows with Status = Idea (title, notes, format, type, platform, created), then fetch each idea's page: brands, sources and framing rules are often only in the page text. If the page links a source article, open it too and check it for agency client names or numbers. Rows with the same title are one idea already split by platform: place each row on its own platform and don't plan new sister rows for platforms it already has. Rows on Blog have no weekly slot; list them apart as "for the monthly jcgiusto.com piece". For every brand or person named in an idea or its source, check the hard limits:
   - no Mars Men numbers, tests or implementations;
   - no ASTEROI client names or numbers;
   - no men's-health, hormone, testosterone or men's-supplement brands in rankings or studies; protein and functional foods count as supplement-adjacent; no men's grooming or men's wellness brands either (near competitors of Mars Men);
   - no Meta ads, creative or ad-spend advice.
   If you aren't sure what a brand sells, look it up before placing it. A flagged idea gets no slot. List it with the reason. If its page already carries a framing rule meant to keep it inside the limits (for example "share the belief, never the number or the implementation"), quote that rule next to it, so Juan can clear it himself. The seven held "CRO things we got right at Mars Men" threads: if Juan clears one, it becomes a single long X post (no threads).
3b. **Brand pages.** Find 7 real brand pages in Juan's Chrome: 5 for the weekday brand verdicts, 2 for the weekend stories (or reuse the week's best two on the weekend; say which). Page types: product page, subscribe box, checkout, cart drawer, upsell; pick the ones that fit the week's topic (subscription weeks → subscribe boxes; checkout weeks → checkouts). Screen each brand against the hard limits in step 3 first, before it goes on any list; if you aren't sure what a brand sells, look it up. Drop a flagged brand and say why. Then screenshot each page from the live site and show the shortlist: brand, page type, link, screenshot. Juan writes the verdicts (1–2 lines each), all on Sunday, so Wednesday's carousel can hold all five. Claude never writes a verdict.
4. **Fill the slots.** Match each slot to an idea whose format fits, on the week's topic (brand pages, notes lists and videos are chosen on the topic; ask Juan for notes lists on it). Monday's contrarian take may be off the topic, as long as it's one of Juan's approved topics. If an idea has no format, suggest one from `content-types.md`. Set what this table says:

   | Slot | Set in Notion |
   |---|---|
   | LinkedIn long post | Type = Personal Post (life/career story) or Authority (idea). Say "photo of Juan" (story) or "infographic" (idea) in the plan |
   | Wednesday long X post (from Tuesday's long post) | Platform = Twitter + Threads, same Type as the long post, Source piece = the long post's row |
   | Brand verdict (single image) | Format = Brand verdict, Type = Infographic |
   | Notes-app list (screenshot) | Format = Notes list, Type = Infographic |
   | Monday checklist carousel | Format = Checklist, Type = Carousel |
   | Wednesday "Pages worth stealing" carousel | Format = Pages worth stealing, Type = Carousel |
   | Framework carousel | Type = Carousel |
   | Summary infographic (from the framework carousel) | Type = Infographic, Source piece = the framework carousel's row |
   | Carousel as X images (cover + 3 best) | Platform = Twitter + Threads, same Format as the carousel, Type = Carousel, Source piece = the carousel's row |
   | Short teardown video (one page) | Format = Brand verdict, Type = Short |
   | Ranking or roundup video | Format = Ranking (or Pages worth stealing for a roundup), Type = Short |
   | Keyword Reel (week B Friday) | Format = Resource, Type = Short |
   | YouTube long | Format = Brand study or Yearly tutorial, Type = YouTube Video |
   | X "new video" post | Platform = Twitter + Threads, Source piece = the YouTube row |
   | Week A's clip on X (week B Thursday) | Platform = Twitter + Threads, Type = Short, Source piece = week A's YouTube row |
   | Resource post | Format = Resource, Type = Resource |
   | Quote reaction | Format = Quote reaction |
   | Contrarian take | Format = Contrarian take |
   | X Sunday life-lesson list | Format = Life-lesson list |

   **Resource Friday:** the Resource post runs on week B's Friday, from ramp week 5. Check it against the last row with Format = Resource: the next one is two weeks after it. If there's no such row, the first one is ramp week 5's Friday. On a non-Resource Friday, LinkedIn gets the week's best brand verdict or a notes-list image.

   Give the stronger slots (Monday, Wednesday, the video slots) to the formats that did best in the review. Oldest ideas go first when two fit equally. For each slot, list its sister versions per **How each piece spreads**:
   - Long post → LinkedIn Tue (+ photo or infographic) → one long single X post Wed 14:00 (no threads).
   - Brand verdict (×5) → X image the same day → Instagram story → best one as a LinkedIn image (Fri, non-Resource weeks) → all five into Wednesday's carousel → Instagram Wed → X images Wed (cover + 3 best; X allows 4 images).
   - Notes list (×3) → X image → one expanded into next Monday's checklist carousel → Instagram the same day → X images Fri (cover + 3 best).
   - Framework (×1) → Thursday carousel (Figma, `/figma-post`), on the topic; in video weeks it comes from Tuesday's video → LinkedIn + Instagram Thu → one summary infographic → Instagram Fri + X next Mon. Last slide: "Comment [KEYWORD]" for the topic's Resource.
   - Video (×4) → same file to Reel, TikTok, Short, X; caption per platform.
   - Long YouTube video → Tue 17:00 + X "new video" post → Thursday's framework carousel → week B: a clip under 2:20 on X (Thu 14:00). No cut-downs to Shorts.
   - Quote reactions → X only, by hand, Tue/Wed/Thu 18:00.
   - From Notion ideas → Claude drafts Monday's contrarian take and the Sunday life-lesson list (only if Juan has added lessons); Juan approves.
   - Free copies → Threads (every X post); X images to Instagram weeks later (in a 4:5 frame); old X winners auto-repost.

   Every carousel's last slide and every Instagram caption carries the topic's keyword. Carousels and infographics are 1080×1350; notes-app screenshots go to Instagram in a 4:5 frame. Check each sister against the platform limits table before planning it. Until it's confirmed the scheduler can post Instagram stories, put "post the stories by hand, daytime" on Juan's list.
5. **Empty slots.** List every slot with no fitting idea, and ask Juan for ideas: `Give me ideas for these and I'll place them.`
6. **Filming list.** Every vertical video of the week, in shooting order for one sitting: at full speed 4 videos, 3 one-page teardowns + 1 ranking or roundup (a new ranking each month), all on the topic; ramp week 2 has 2. In week B, Friday's video is the keyword Reel and ends "Comment [NEW KEYWORD]". Plus the YouTube long from week 4. For each: the idea, the format and what Claude preps (the pages, screenshots from the brand's live site, the script).
7. **Hours.** Add up Juan's time for every planned piece from the hours table (**What Juan creates each week, and his hours**), including the checking time, the Resource post, a new Resource and any one-offs. Sisters made from the same piece add only checking time. Compare with the ramp week's figure in **First five weeks**. Above 27 h, warn. Above 37 h, drop pieces in the table's default order (quote reactions → the ranking video → one notes list → a lighter YouTube video → week B's YouTube video) until it fits, and show what was dropped.
8. **Winners due back.** Query Status = Published with "Can come back on" on or before next Sunday. For each: the post, platform, when it first ran, its numbers and how it comes back (X word for word; LinkedIn needs a new first line or a carousel rebuild; video re-uploaded or refilmed).
9. **Re-check list.** For next week's pieces that already have versions (Versions not empty), fetch the source and each version. List any version last edited before its source, so Juan re-checks it matches.

## Show the plan

One message:
- the ramp row being used;
- the topic, week A or B, its Resource and keyword (and whether next Friday is a Resource Friday);
- the brand page shortlist, waiting for Juan's verdicts, and any brand dropped by the screen;
- a day-by-day table (day, time Madrid, platform, format, idea, sister versions);
- ideas held back by the brand check, with the reason;
- empty slots;
- filming list;
- hours against the target, and anything dropped;
- Juan's list: things only he can do this week (verdicts, notes lists, YouTube idea, new keyword and its automatic DM, building a new Resource, verifying the YouTube channel, posting stories by hand);
- winners due back;
- versions to re-check.

Then ask: `Write these dates and formats to Notion, and copy the winners?`

## On Juan's yes

- If it was missing: add "Ramp week one starts" with Juan's Monday to the "Volume and timing" table in `content/wiki/content-system-decisions.md`, fill the start Mondays in its Topic cycle table, and set `updated:`. Same for a new topic's start Monday or a new keyword row.
- For each placed idea: set Date (the slot's posting time, Madrid) and Format and/or Type (per the table in step 4) on its row, and add "Topic: <topic> · Keyword: <WORD> · Long post: story or idea" to its Notes (keep what's already there; the long-post part only on the long post). Every placed piece gets that Notes line; show it in the write list. Status stays Idea. `/content` drafts it and creates the sister rows.
- For each piece that comes from a format, not an idea: create the row shown in the write list (Title, Platform, Format/Type, Date, Source piece, Notes line), Status Idea.
- For each approved winner: create a new row with the same Title, Platform, Format, Type and page text, a new Date, Status Drafting, and Notes "Repost of <old row link>". If the Media files can't be copied through the connector, say so; Juan re-attaches them. Clear "Can come back on" on the old row. Flag LinkedIn reposts: they need a new first line before they're marked Ready.
- Report what was written, with links.

## Rules

- Never write to Notion or any file without a yes on the exact list shown.
- Never schedule by hand. Every evening slot (19:00 Madrid and later) goes through the scheduler.
- Weekends: only the Sunday X post (if Juan has lessons) and the daily Instagram story.
- Keep the chat output under ~500 words, plus the tables.

Changelog: 2026-11-26 — dry-run fixes: decisions-page topic cycle first, first-ever week fallbacks, week A clip on X, keyword Reel and its DM on Juan's list, wider brand screen and source-article check, 7 brand pages, full format mapping (Notes list, Brand verdict), format-made rows, ramp-start write moved to "On Juan's yes", YouTube phone check, one hours table with drop order, Resource Friday from week 5.
