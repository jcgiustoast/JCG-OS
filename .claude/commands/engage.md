# /engage — Daily Engagement Briefing

Pull last-24h posts from curated DTC targets on Twitter and LinkedIn, score each for reply opportunity, and output a single briefing of 40-50 candidates so Juan can pick 20-40 worth replying to.

**Voice:** Juan writes all replies himself. This command is discovery + curation only — it does NOT post anything.

---

## ARGUMENTS

```
/engage              # full run, both platforms
/engage twitter      # Twitter only
/engage linkedin     # LinkedIn only
/engage quick        # ICPs only, skip Peers (smaller briefing)
/engage --dry-run    # parse targets + show counts, no Apify calls
```

If no platform specified, run both.

---

## INPUT SOURCE

Reads `life/wiki/engagement-targets.md`. Parses markdown tables in:
- Twitter → ASTEROI ICPs → US
- Twitter → ASTEROI ICPs → Spanish market
- Twitter → Peers
- LinkedIn → ASTEROI ICPs → US
- LinkedIn → ASTEROI ICPs → Spanish market
- LinkedIn → Peers

**Skip rows where:**
- Handle/username column is `_verify_`, `_add_`, or empty
- Row is in the "Brands to investigate" research list (not a real handle)

Also reads from the same file:
- Signal Filters section (reply-worthy + skip signals)
- Topic priorities + deprioritizations
- Daily Quota section

---

## APIFY CONFIGURATION

See `~/.claude-personal/projects/C--Users-jcgiu-Documents-JCG-OS/memory/apify-scrapers.md` for full call pattern.

**Quick reference:**
- Twitter: `apidojo/tweet-scraper` — batch all handles in ONE run, `tweetsDesired: 5` per handle
- LinkedIn: `apimaestro/linkedin-profile-posts` — single username per run, `limit: 5` each. Parallelize across usernames but cap at 10 concurrent runs.

Both async: POST → poll `runId` until `SUCCEEDED` → GET `/dataset/items`.

---

## WORKFLOW

### 1. Parse targets

Extract handle/slug lists from the engagement-targets.md tables. Skip placeholders. Tag each entry with its tier (`icp_us`, `icp_es`, `peer`).

If `--dry-run`, output the parsed counts and stop:
```
Twitter: 18 ICPs (12 US + 6 ES) + 14 Peers = 32 handles
LinkedIn: 17 ICPs (11 US + 6 ES) + 15 Peers = 32 usernames
Estimated Apify cost: ~$2-4
```

### 2. Fetch last-24h posts

**Twitter** — one batched Apify run:
```json
{"handles": ["handle1", "handle2", ...], "tweetsDesired": 5, "addUserInfo": true}
```

**LinkedIn** — parallel runs, one per username. Cap concurrency at 10. If a run fails or returns 0 results, log to "Errors" section but continue. No retries beyond 1.

### 3. Filter to last 24h

Drop posts where `createdAt` (Twitter) or `posted_at.date` (LinkedIn) is more than 24h ago. Targets with no fresh posts go to "Stale targets" section.

### 4. Score each post

Score = **Relevance × Opportunity × Visibility** − **Anti-signals**

**Relevance (0-10)** — topic match against Juan's priorities (from engagement-targets.md):
- CAC, unit economics, profitability at scale
- Post-purchase, LTV, subscription economics
- Creative testing systems
- DTC operator's view of agency relationships
- Building internal tools / AI for ops

**Opportunity (0-10):**
- +3 author asks a genuine question (invites reply)
- +2 author shares a specific number / test result (you can respond with your own data)
- +2 contrarian or counter-intuitive take (room for nuance)
- +2 < 12h old (boost) · +0 if 12-24h
- +1 high engagement-to-followers ratio (mid-virality, your reply will be seen)

**Visibility (0-10):**
- Author follower size (relative)
- Post engagement (likes + comments)
- Reply count: <20 = strong, 20-100 = ok, >100 = bury risk

**Anti-signals (subtract from total):**
- −3 generic motivational / quote post
- −3 self-promotional product launch
- −2 poll
- −5 if >100 replies (bury risk)
- Skip entirely if >24h old

**Tier multipliers:**
- ICPs: ×1.0
- Peers: ×0.85 (slight deprioritization vs ICPs, since ICP visibility is the primary goal)
- ICPs Spanish: ×1.1 (Spanish-language engagement = differentiator)

### 5. Rank + group

Take top 40-50 across both platforms. Group output by:
1. Platform (Twitter → LinkedIn)
2. Tier (ICPs US → ICPs ES → Peers)

Sort within each group by score descending.

### 6. Output briefing

Save to `content/raw/engagement/YYYY-MM-DD.md`:

```markdown
# Engagement Briefing — YYYY-MM-DD

**Posts surfaced:** N | **ICP:** N | **Peer:** N
**Top scoring:** [author] (score X)
**Estimated time:** ~N min

---

## Twitter — ICPs (US)

### 1. @SeanEcom — Sean Frank — score 87
"Just hit $2M MRR and our CAC is up 40% YoY. Performance creative
is dead. Anyone else seeing this?"
🔗 https://x.com/... · 4h ago · 142 ❤ · 12 💬

**Why:** ICP. Real number. Question = reply window. 4h old, mid-virality.
**Angle:** You've seen CAC spike at Mars Men in Q1 — share what you tested
when MER dropped (specific channel + delta). Don't pitch ASTEROI.

### 2. ...

## Twitter — ICPs (Spanish)
...

## Twitter — Peers
...

## LinkedIn — ICPs (US)
...

## LinkedIn — ICPs (Spanish)
...

## LinkedIn — Peers
...

---

## Stale targets (no posts in 24h)
- @handle1 (Twitter) — last post 3 days ago
- username2 (LinkedIn) — last post 5 days ago

## Errors (couldn't fetch)
- username3 (LinkedIn) — actor returned 0 results, slug likely wrong → flag for verification
```

### 7. Log

Append to `content/memory/log.md`:

```markdown
## [YYYY-MM-DD] engagement | Daily briefing
- Surfaced N posts (Twitter: X, LinkedIn: Y)
- Top scoring: [author] (score N)
- Stale targets: N
- Slug errors (need verification): N
- Briefing: content/raw/engagement/[file].md
```

---

## CONSTRAINTS

- **DO NOT post replies.** Discovery + curation only. Juan writes all replies himself.
- **DO NOT fabricate post content.** If a scraper returns 0 results for a target, log it under "Stale targets" or "Errors" — never invent posts.
- **DO NOT include posts older than 24h** in the main briefing.
- **Cost guardrails:** Twitter batched run is cheap (~$0.10). LinkedIn parallel is ~$0.05-0.10 per username × ~30 usernames = ~$2-3 per day. If daily LinkedIn cost > $5, suggest running LinkedIn every-other-day or trimming the target list.
- **Slug error escalation:** If >5 LinkedIn usernames return 0 results, recommend Juan run a one-shot verification pass before next briefing.
- **Empty briefing:** If <10 candidates after filtering, surface this to Juan — either the target list is too small, or signal filters are too strict.

---

## FUTURE ENHANCEMENTS (not in v1)

- **Reply-graph discovery** — scrape replies to top-scoring posts to surface new candidate accounts; see [[engagement-discovery-via-replies]] memory note. Requires additional Apify actors (post-comments scrapers).
- **Outcome tracking** — Juan logs which replies got DM / follow / quote-tweet outcomes. Train scoring weights from this over time.
- **Auto-update target list** — promote frequently-replying-to-Juan accounts into Peers tier automatically.
