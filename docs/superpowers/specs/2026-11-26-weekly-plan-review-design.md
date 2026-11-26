# Weekly plan + weekly review — design

Date: 2026-11-26. Build plan: `docs/superpowers/plans/2026-11-25-five-platform-content-system.md`, Task 11.

## Why

The five-platform calendar only runs if every Sunday someone (a) looks at what last week did and (b) fills next week's slots before the writing and filming blocks. Without it, slots go empty, evening posts get missed, and the week-four "cut the weakest format" never happens. The scheduler can't repost, so old winners also need a hand-run listing.

## Approaches

| Approach | Trade-off | Picked |
|---|---|---|
| Two commands, review first, then plan | Two things to run, but each stays short; the plan uses what the review found | **Yes (Juan, 2026-11-26)** |
| One Sunday command doing both | One thing to remember; one very long run, a stall loses both | No |
| Two commands + automatic Sunday start | Draft waiting; but reading platforms needs Juan's Chrome, so automation saves little | No |

## Decided by Juan

- Claude reads last week's numbers off each platform in Juan's Chrome (Claude in Chrome), shows them, and writes them into Notion only after his yes.
- Two commands: `/week-review` then `/week-plan`.

## Goals / non-goals / anti-goals

- **Goals:** every slot of next week has a piece or is listed as empty; every brand screened; filming list and hours known before Monday; results in Notion; weakest format proposed for cutting in week four; winners due to come back are listed.
- **Non-goals:** drafting posts (that is `/content`); scheduling (the sync does it from Date + Status); signups (empty until the email tool is wired to the checklist page, Task 8).
- **Anti-goals:** inventing topics (ideas come from Juan); any Notion write without his yes; touching Post Bridge ID / Last Sync At / Synced Edit Token / Published URLs; reading `content/.notion-config.json`.

## Constraints

- Notion only through the Notion connector. Content DB `collection://36aeedc9-595f-81f9-88f2-000b60546d69`.
- Hard limits screened on every brand: no Mars Men numbers/tests; no ASTEROI client names/numbers; no men's-health, hormone, testosterone or men's-supplement brands; no Meta ads advice.
- Both commands are read-only until Juan approves a shown list of writes.
- Chat output follows Plain Speech (no IDs as words, no numbered options).

## `/week-review` (run first, Sunday)

1. Find last week's posts: Status Published, Date Monday–Sunday of the week just ended. Use Published URLs (read only) for the links.
2. Open each in Chrome and read: views, comments, saves, follows. Where each comes from: LinkedIn post analytics; X post analytics (bookmarks = saves); Instagram insights; TikTok Studio (favorites = saves); YouTube Studio (subscribers gained = follows, no saves). Leave a number blank when the platform doesn't show it, and say so. Note each post's age, since a post from Sunday has had less time.
3. Show a table of the numbers. On Juan's yes, write Views/Comments/Saves/Follows to each row.
4. Compare per format and per platform: posts, average views, saves, comments, follows per post.
5. Best three and worst three posts by saves + comments + follows.
6. Winners: propose "Can come back on" for top posts (X top 10% → +10 weeks; LinkedIn and videos → +3 months). Write after yes.
7. Week four (and every fourth week after): propose the weakest format to cut, using results per hour spent (time per format from `content/wiki/engine/content-types.md`).
8. Draft a log entry; on yes, append to `content/memory/log.md`.

## `/week-plan` (run second, Sunday)

1. Work out the ramp week from the saved start date (asks once if missing; saved in `content/wiki/content-system-decisions.md`, Claude-authored, after yes).
2. List next week's active slots: the calendar in `content/wiki/content-strategy.md`, cut down by the ramp week (proposal below).
3. Read all Idea rows. Screen every named brand against the hard limits; a flagged idea gets no slot and is shown with the reason.
4. Match ideas to slots by format, suggesting a format for ideas that have none. Use the review's findings (formats doing best get the stronger slots). Each slot shows its sibling versions from the chains in `content/wiki/engine/repurpose.md` (carousel → LinkedIn + Instagram + X; video → Reel + TikTok + Short).
5. Empty slots are listed, and Juan is asked for ideas.
6. Filming list: every video of the week, for one sitting.
7. Hours: sum of time per format, compared with the ramp week's hours.
8. Winners due: Published rows with "Can come back on" on or before next Sunday.
9. Re-check list: sibling versions whose source piece changed after they were drafted.
10. On Juan's yes: set Date and Format on each chosen idea row. For each winner he approves, create a new row: same title, platform, format, type and page text; new Date; Status Drafting; Notes "Repost of <link>"; clear the old row's "Can come back on". LinkedIn reposts get flagged for a new first line.

### Ramp proposal (Claude's call, shown to Juan in the plan output)

| Week | Active slots |
|---|---|
| 1 | LinkedIn Mon carousel, Tue long personal, Thu long framework. X one 13:55 post Mon–Fri plus a second where ideas allow, Sunday list |
| 2 | Week 1 + Reels/TikTok/Shorts Mon and Fri, Instagram carousels Tue and Thu, Instagram story daily |
| 3 | Full LinkedIn (5), full X (~12), three videos (Mon, Wed, Fri) |
| 4+ | Full calendar, YouTube long on Tuesday, Resource post Friday every other week |

## Left to the builder

- Exact command wording, matching the style of `.claude/commands/today.md` and `closeday.md`.
- Two new rows in `.claude/slash-commands.md`.
- Dry run both against the real Notion table, read-only, before calling it done.

## Separate, same task

- Engagement-targets page (`life/wiki/engagement-targets.md`, Juan's page): its reply style says to share Mars Men numbers, which breaks the hard limit. Propose a fix and DTC-founder additions in chat; Juan edits.
