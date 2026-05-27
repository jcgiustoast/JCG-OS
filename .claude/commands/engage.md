# /engage — Daily Engagement Briefing (Twitter)

Pull last-24h tweets from curated DTC targets, score each for reply opportunity, and output a single briefing of 30-40 candidates so Juan can pick 20-30 worth replying to.

**Scope:** Twitter / X only. LinkedIn engagement is handled manually by Juan via LinkedIn lists / notifications — not automated through this command. The LinkedIn sections in `engagement-targets.md` exist as reference for Juan's manual list maintenance.

**Voice:** Juan writes all replies himself. This command is discovery + curation only — it does NOT post anything.

---

## ARGUMENTS

```
/engage              # full run
/engage quick        # ICPs only, skip Peers (smaller briefing)
/engage --dry-run    # parse targets + show counts, no Apify calls
```

---

## INPUT SOURCE

Reads `life/wiki/engagement-targets.md`. Parses markdown tables in:
- Twitter → ASTEROI ICPs → US
- Twitter → ASTEROI ICPs → Spanish market
- Twitter → Peers

**Ignore the LinkedIn sections entirely** — those are manually maintained by Juan, not automated.

**Skip rows where:**
- Handle column is `_verify_`, `_add_`, or empty
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

Async: POST → poll `runId` until `SUCCEEDED` → GET `/dataset/items`.

**Cost:** ~$0.10 per daily run (one batched request, ~250 tweets). Trivial.

---

## WORKFLOW

### 1. Parse targets

Extract handle lists from the Twitter tables in engagement-targets.md. Skip placeholders (`_verify_`, `_add_`, empty). Tag each entry with its tier (`icp_us`, `icp_es`, `peer`).

If `--dry-run`, output the parsed counts and stop:
```
Twitter ICPs (US):       N handles
Twitter ICPs (Spanish):  N handles
Twitter Peers:           N handles
Total:                   N handles
Estimated Apify cost:   ~$0.10
```

### 2. Fetch last-24h tweets

One batched Apify run:
```json
{"handles": ["handle1", "handle2", ...], "tweetsDesired": 5, "addUserInfo": true}
```

### 3. Filter to last 24h

Drop tweets where `createdAt` is more than 24h ago. Handles with no fresh tweets go to "Stale targets" section.

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

Take top 30-40 tweets. Group output by tier (ICPs US → ICPs ES → Peers). Sort within each group by score descending.

### 6. Output briefing

Save to `content/raw/engagement/YYYY-MM-DD.md`:

```markdown
# Engagement Briefing — YYYY-MM-DD

**Tweets surfaced:** N | **ICP:** N | **Peer:** N
**Top scoring:** [author] (score X)
**Estimated time:** ~N min

---

## ICPs (US)

### 1. @SeanEcom — Sean Frank — score 87
"Just hit $2M MRR and our CAC is up 40% YoY. Performance creative
is dead. Anyone else seeing this?"
🔗 https://x.com/... · 4h ago · 142 ❤ · 12 💬

**Why:** ICP. Real number. Question = reply window. 4h old, mid-virality.
**Angle:** You've seen CAC spike at Mars Men in Q1 — share what you tested
when MER dropped (specific channel + delta). Don't pitch ASTEROI.

### 2. ...

## ICPs (Spanish)
...

## Peers
...

---

## Stale targets (no posts in 24h)
- @handle1 — last post 3 days ago
- @handle2 — last post 5 days ago

## Errors (handle returned 0 results)
- @handle3 — flag for handle verification
```

### 7. Log

Append to `content/memory/log.md`:

```markdown
## [YYYY-MM-DD] engagement | Daily briefing
- Surfaced N tweets
- Top scoring: [author] (score N)
- Stale targets: N
- Handle errors: N
- Briefing: content/raw/engagement/[file].md
```

---

## CONSTRAINTS

- **DO NOT post replies.** Discovery + curation only. Juan writes all replies himself.
- **DO NOT fabricate tweet content.** If the scraper returns 0 results for a handle, log it under "Stale targets" or "Errors" — never invent tweets.
- **DO NOT include tweets older than 24h** in the main briefing.
- **LinkedIn out of scope.** Skip those sections entirely.
- **Empty briefing:** If <10 candidates after filtering, surface this to Juan — either the target list is too small, or signal filters are too strict.

---

## FUTURE ENHANCEMENTS (not in v1)

- **Reply-graph discovery** — scrape replies to top-scoring posts to surface new candidate accounts; see [[engagement-discovery-via-replies]] memory note. Requires additional Apify actors (post-comments scrapers).
- **Outcome tracking** — Juan logs which replies got DM / follow / quote-tweet outcomes. Train scoring weights from this over time.
- **Auto-update target list** — promote frequently-replying-to-Juan accounts into Peers tier automatically.
