# /content-research — Scout What's Performing in the DTC Content Landscape

Scrape reference creators on Twitter/X and LinkedIn to understand what topics, hooks, and formats are driving engagement. Returns a competitive intelligence brief that feeds into `/content`.

---

## ARGUMENTS

```
/content-research [platform] [topic]
/content-research twitter LTV
/content-research linkedin experimentation
/content-research all                      # scrape all creators, both platforms, full scan
```

If no platform is specified, scrape both. If no topic is specified, do a general top-posts scan.

---

## APIFY CONFIGURATION

**Environment variable:** `APIFY_API_KEY` (already set in env)

### Twitter/X Scraper: `apidojo/tweet-scraper`

```bash
# Start run
curl -s -X POST "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"handles":["HANDLE"],"tweetsDesired":N,"addUserInfo":true}'

# Check status (poll until SUCCEEDED)
curl -s "https://api.apify.com/v2/actor-runs/{runId}?token=$APIFY_API_KEY"

# Get results
curl -s "https://api.apify.com/v2/actor-runs/{runId}/dataset/items?token=$APIFY_API_KEY"
```

**Response fields:** `text`, `fullText`, `likeCount`, `retweetCount`, `replyCount`, `viewCount`, `createdAt`, `url`

### LinkedIn Scraper: `apimaestro/linkedin-profile-posts`

```bash
# Start run
curl -s -X POST "https://api.apify.com/v2/acts/apimaestro~linkedin-profile-posts/runs?token=$APIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username":"USERNAME","limit":N}'

# Check status and get results (same pattern as Twitter)
```

**Response fields:** `text`, `stats.total_reactions`, `stats.comments`, `stats.reposts`, `posted_at.date`, `url`

**Important:** Both scrapers are async. Start the run, get `runId` from `response.data.id`, poll status until `SUCCEEDED`, then fetch dataset items.

---

## REFERENCE CREATORS

| Creator | Twitter Handle | LinkedIn Username | Niche | Priority |
|---------|---------------|-------------------|-------|----------|
| Taylor Holiday | TaylorHoliday | taylor-holiday-ctc | DTC growth, CTC/SEAN, forecasting | High |
| Nick Sharma | nicaboricua | nicksharma | DTC growth, retention, newsletter | High |
| Cody Plofker | cikimaker | cikimaker | DTC CMO, eComm finance, Meta Ads | Medium |
| Barry Hott | barryhott | -- | Creative strategy, DTC ads | Medium |
| Dara Denney | daradenney | -- | Creative strategy, performance | Medium |

**To add a creator:** Juan can say "add [name] to reference creators" and Claude should update this file.

### Topic-to-Creator Mapping

| Topic | Best Creators to Scrape |
|-------|------------------------|
| LTV, subscription economics | Taylor Holiday, Nick Sharma |
| CRO, experimentation | Taylor Holiday, Cody Plofker |
| Profitability, unit economics | Taylor Holiday, Cody Plofker |
| Metrics, measurement | Taylor Holiday |
| Retention, churn | Nick Sharma |
| General DTC landscape | All |

---

## WORKFLOW

### 1. Scrape (parallel when possible)

Launch scraper runs for the relevant creators on the target platform. Use parallel bash calls when scraping multiple creators.

- **Twitter:** Request `tweetsDesired: 50` per creator (last ~50 tweets)
- **LinkedIn:** Request `limit: 30` per creator (last ~30 posts)

### 2. Filter by Topic (if specified)

If Juan specified a topic (e.g., "LTV"), filter scraped posts to only those mentioning relevant keywords:

| Topic | Keywords to Filter |
|-------|-------------------|
| LTV | ltv, lifetime value, payback, cohort, retention |
| CRO | conversion, cro, experimentation, test, a/b, variant |
| Profitability | margin, contribution, profit, cogs, unit economics, p&l |
| Metrics | roas, mer, cac, ncac, metric, kpi, dashboard |
| Subscription | subscription, churn, recurring, subscriber, renewal |
| Experimentation | experiment, test, hypothesis, significance, powered ice |
| Forecasting | forecast, projection, model, predict, plan |

### 3. Rank by Engagement

**Twitter:** Sort by `likeCount + retweetCount`. Show `viewCount` for context.
**LinkedIn:** Sort by `stats.total_reactions + stats.comments`.

### 4. Analyze Top Posts

For the top 10 posts across all creators:

Extract:
- **Hook type:** Contrarian, question, scenario, data point, story
- **Format:** Single post, thread (how many), list, story, case study
- **Topic angle:** What specific sub-topic within the broader area
- **Length:** Short (<100 words), medium (100-300), long (300+)
- **Engagement level:** Absolute numbers + relative to creator's average

### 5. Identify Gaps and Angles

Compare what's performing against Juan's wiki content. Look for:
- **Gaps:** Topics Juan has deep content on (from wiki) that nobody is posting about
- **Saturated:** Topics everyone is posting about (differentiation needed)
- **Juan's edge:** Where his frameworks (Powered ICE, Metric Tree, Growth Formula) offer a unique angle
- **Format opportunities:** If everyone posts threads, maybe a single punchy take stands out (or vice versa)

### 6. Output Format

```markdown
## Content Research Brief — [Platform] — [Topic]
**Date:** YYYY-MM-DD
**Creators scraped:** [list]
**Posts analyzed:** [N]

### Top Performing Posts (Last 30 Days)

| # | Creator | Hook (first line) | Format | Likes | Comments | Link |
|---|---------|-------------------|--------|-------|----------|------|
| 1 | ... | "..." | Thread (5) | 342 | 87 | url |
| 2 | ... | "..." | Single | 218 | 45 | url |

### Hook Patterns That Work
- [Pattern 1]: Used by [creator], avg [X] likes. Example: "..."
- [Pattern 2]: ...

### Topic Angles Being Covered
- [Angle 1]: [Creator] posts about this frequently. Engagement: [high/medium/low]
- [Angle 2]: ...

### Gaps Juan Can Own
- **[Gap 1]:** Nobody is talking about [X]. Juan's wiki page [[page]] has deep content on this.
- **[Gap 2]:** ...

### Recommended Content Angles
1. **[Angle]:** [Why it would work] — Source: [[wiki-page]]
2. **[Angle]:** [Why it would work] — Source: [[wiki-page]]
3. **[Angle]:** [Why it would work] — Source: [[wiki-page]]
```

### 7. Save Research

Save the brief to `C:\Users\jcgiu\Documents\JCG-OS\content\raw\research\[date]-[platform]-[topic].md` for future reference.

Log in `content/memory/log.md`:
```markdown
## [YYYY-MM-DD] research | Content research — [platform] — [topic]
- Scraped [N] creators, analyzed [N] posts
- Top performing: [creator] on [topic] ([N] likes)
- Gaps identified: [list]
- Recommended angles: [list]
- Brief saved: content/raw/research/[filename]
```

---

## CONSTRAINTS

- Do NOT scrape Juan's own accounts (this is about competitors, not self-analysis)
- Do NOT use scraped content verbatim -- it's for pattern analysis only
- Respect rate limits -- don't scrape more than 5 creators per session
- If a scraper returns 0 results or errors, note it and move on -- don't retry more than once
- Research is a means to better content, not an end. Always conclude with actionable angles.
