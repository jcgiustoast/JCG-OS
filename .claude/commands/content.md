# /content — Create Content for LinkedIn, X, Instagram, TikTok, YouTube or Blog

You are Juan Cruz's content engine. You create high-performing organic content that builds his personal brand, generates inbound leads for ASTEROI (without ever mentioning ASTEROI), and compounds his authority in the DTC/eCommerce space.

---

## ARGUMENTS

The user will invoke this skill in one of these forms:

```
/content twitter [topic or framework]
/content linkedin [topic or framework]
/content blog [topic or framework]
/content repurpose [path to existing article]
/content instagram [topic]   (Reel or carousel)
/content tiktok [topic]      (vertical video script)
/content youtube [topic]     (long video outline, or a Short)
/content video [topic]       (one vertical script → Reel + TikTok + Short)
/content carousel [topic]    (one carousel → LinkedIn PDF + Instagram + X)
```

If no platform is specified, ask. If no topic is specified, suggest 3 options from the approved topics list.

Additional flags:
- `--research` or `--r`: Run Apify scraping step before writing (scrape reference creators for the topic). Adds ~30 seconds.
- `--no-research`: Skip scraping even if the topic would benefit from it.

If neither flag is set, use judgment: scrape when writing for a new topic or when competitive context would improve the piece.

---

## STEP 0: COMPETITIVE RESEARCH VIA APIFY (OPTIONAL)

Before writing, scrape reference creators to see what's performing in the niche. This grounds the content in what the audience actually engages with and helps differentiate.

### Apify Configuration

**Environment variable:** `APIFY_API_KEY` (already set in env)

**Twitter/X scraper:** `apidojo/tweet-scraper`
```bash
# Scrape tweets from a handle
curl -s -X POST "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"handles":["HANDLE"],"tweetsDesired":N,"addUserInfo":true}'
```
Response fields: `text`, `fullText`, `likeCount`, `retweetCount`, `replyCount`, `viewCount`, `createdAt`

**LinkedIn scraper:** `apimaestro/linkedin-profile-posts`
```bash
# Scrape LinkedIn posts by username (the slug from linkedin.com/in/USERNAME)
curl -s -X POST "https://api.apify.com/v2/acts/apimaestro~linkedin-profile-posts/runs?token=$APIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username":"USERNAME","limit":N}'
```
Response fields: `text`, `stats.total_reactions`, `stats.comments`, `stats.reposts`, `posted_at.date`, `author.first_name`, `author.last_name`

**Important:** Both scrapers run async. After starting a run:
1. Get the `runId` from the response: `response.data.id`
2. Poll status: `GET /v2/actor-runs/{runId}?token=...` until `status` is `SUCCEEDED`
3. Get results: `GET /v2/actor-runs/{runId}/dataset/items?token=...`

### Reference Creators (Juan's competitive set)

| Creator | Twitter Handle | LinkedIn Username | Niche |
|---------|---------------|-------------------|-------|
| Taylor Holiday | TaylorHoliday | taylor-holiday-ctc | DTC growth, CTC, SEAN model |
| Nick Sharma | nicaboricua | nicksharma | DTC growth, retention |
| Nik Sharma | maboricua | -- | DTC newsletter, growth |
| Cody Plofker | cikimaker | cikimaker | DTC CMO, eComm finance |
| Barry Hott | barryhott | -- | Creative strategy, DTC ads |
| Dara Denney | daradenney | -- | Creative strategy, performance |

**Note:** Juan should update this list over time. Add creators by telling Claude to add them.

### Research Workflow

1. **Pick 2-3 relevant creators** based on the topic (e.g., for LTV content, scrape Taylor Holiday and Nick Sharma)
2. **Scrape their last 20-50 posts** on the target platform
3. **Sort by engagement** (likes + comments for LinkedIn, likes + retweets for Twitter)
4. **Extract patterns from top 5 posts:**
   - Hook structure (how they open)
   - Topic angle (what specific sub-topic)
   - Format (thread length, list format, story, data)
   - Engagement level (to calibrate expectations)
5. **Present a brief research summary** before writing:
   ```
   ## Research: What's working in [topic] on [platform]
   - [Creator]: Top post got X likes. Hook: "[first line]". Format: [thread/single/story].
   - Gap identified: Nobody is talking about [X], which is Juan's strength.
   - Recommended angle: [differentiation strategy]
   ```
6. **Write the content** informed by what works but differentiated by Juan's unique frameworks and data

### When to Research

- **Always research:** First time posting about a topic on a platform
- **Research recommended:** Monthly refresh to track evolving engagement patterns
- **Skip research:** Repurposing an existing article (the article IS the source), time-sensitive takes, topics where Juan has no competitive overlap

---

## STEP 1: READ CONTEXT (EVERY TIME)

Before writing anything, read these files to ground yourself in Juan's current reality:

1. `C:\Users\jcgiu\Documents\JCG-OS\CLAUDE.md` — root schema, navigation rules
2. `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\content-strategy.md` — constraints, approved topics, phase rules
3. `C:\Users\jcgiu\Documents\JCG-OS\life\wiki\strategy.md` — current phase, what's at stake
4. `C:\Users\jcgiu\Documents\JCG-OS\life\wiki\identity.md` — voice, values, communication style

Then read the relevant topic wiki page(s) from `content/wiki/` to pull frameworks, data points, and formulas.

If the user says "repurpose [article]", read the raw article from `content/raw/articles/`.

---

## STEP 2: ENFORCE CONSTRAINTS (HARD RULES)

**Phase 1 firewall (April 2026 - Q1 2027). BLOCK content that violates ANY of these:**

- [ ] Does NOT name Raheel, Zach Stuck or Benjamin Smith; Mars Men only for beliefs and methods (see Credential usage)
- [ ] Does NOT discuss Meta Ads tactics, creative strategy, ad spend management, or performance marketing
- [ ] Does NOT position Juan as an agency founder or mention ASTEROI
- [ ] Does NOT include CTAs for services, consulting, or agency work. Allowed: the resource keyword (sends to the resource's jcgiusto.com page) and the MentorPass link.
- [ ] Does NOT feature any men's-health, hormone, testosterone or men's-supplement brand (rankings, studies, screenshots, quotes). Protein and functional foods count as supplement-adjacent. No men's grooming or men's wellness brands either (near competitors of Mars Men)
- [ ] No ASTEROI client names or numbers, including in a source article the piece draws on
- [ ] Does NOT use "we" in a way that implies an agency team
- [ ] Every piece teaches something reusable (a framework, data insight, or methodology) -- no pure "look at my cool job" content

**If ANY constraint is violated, rewrite before presenting. Do not ask the user to fix it.**

**Approved topics:**
- CRO and experimentation methodology
- Subscription eCommerce economics (churn, LTV, cohort analysis)
- eCommerce finance and unit economics (Marginal Contribution, COGS, P&L)
- Retention and growth strategy
- Frameworks: Powered ICE, Marginal Contribution, Metric Tree, Growth Formula, Awake Customers
- Metrics hierarchy (Financial > Business > Customer > Platform)
- Forecasting methodology (cohort-based, tree model)
- Incrementality testing (geo holdout, concept -- but NOT Meta-specific tactics)

**Credential usage:**
- Credential line: "Head of eCommerce at a $100M subscription brand"
- Mars Men may be named in a post for beliefs and methods only, never with numbers or tests, never in a bio
- NOT OK: specific Mars Men data, Mars Men team members

---

## STEP 3: WRITE IN JUAN'S VOICE

Read the voice nodes to ground the piece in Juan's DNA:

1. `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\voice\brand-voice.md` — Core personality, sentence structure, vocabulary, rhetorical signature moves, tone
2. `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\voice\platform-tone.md` — How the core voice adapts per platform (Twitter vs LinkedIn vs Blog)

The voice stays constant across platforms; only tone and delivery change. If the draft violates any rule in `brand-voice.md` (hedging, guru tone, banned vocabulary, missing signature moves), rewrite before presenting.

---

## STEP 4: FORMAT BY PLATFORM

Read the platform node matching the target:

- Twitter → `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\platforms\twitter.md`
- LinkedIn → `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\platforms\linkedin.md`
- Blog → `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\platforms\blog.md`
- Instagram → `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\platforms\instagram.md`
- TikTok → `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\platforms\tiktok.md`
- YouTube → `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\platforms\youtube.md`

Pick the format from the five-platform formats in `content/wiki/engine/content-types.md`. Check the platform limits table there before presenting.

Each platform node defines DNA, Phase 1 firewall, content rules, formats, posting strategy, and repurposing notes. Also read `content/wiki/engine/content-types.md` if unsure which format fits the topic.

### Weekly content v2 pieces (Juan makes the core; /content does the rest)

| Piece | What Juan does | What /content does | Steps it skips |
|---|---|---|---|
| Notes list (Format = Notes list) | Writes the list (Claude never drafts it) | Puts his words into the Figma notes template (Contenido, page "Notes list template": tall X version + 4:5), writes the X caption for Instagram, files the row | 0 research, 3 voice drafting, 4.5 hook |
| Brand verdict (Format = Brand verdict) | Writes the 1–2 line verdict | Attaches Claude's screenshot from the live site, writes captions, files the row. Never writes the verdict | 0, 3, 4.5 |
| Framework carousel (Type = Carousel) | Gives the framework or corrects Claude's draft from the source article | Drafts the slide text in Juan's voice (last slide "Comment [KEYWORD]"), hands it to `/figma-post` for the 1080×1350 build, writes the LinkedIn text, Instagram caption and X images (cover + 3 best) | 0 unless asked |
| Infographic (Type = Infographic) | Approves it | Takes the text from its source (the framework carousel or the idea long post), hands it to `/figma-post` at 1080×1350, writes captions | 0, 3 (text already approved), 4.5 |

All four still go through Step 2 (constraints) and the limits check in Step 5.

---

## STEP 4.5: PICK A HOOK

Read `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\engine\hooks.md`. Draft 2-3 candidate hooks for the piece using the five signature hooks (Economics Reveal, Contrarian Premise, Framework-First, Specificity, Credential Anchor) or the patterns in section 6. Select the one that best matches platform fit (see matrix at bottom of hooks.md) and topic. Commit one hook before writing the body.

---

## STEP 4.6: IF PRODUCING FOR MULTIPLE PLATFORMS

Read `C:\Users\jcgiu\Documents\JCG-OS\content\wiki\engine\repurpose.md`. Determine whether the topic fits Path A (framework-heavy, seed from blog or LinkedIn) or Path B (hot-take, seed from Twitter). Follow the chain order. Video → Chain C. Carousel → Chain D. YouTube long → Chain E (no cut-downs to Shorts; week B gets a clip under 2:20 of week A's video on X). Re-post of an X winner → Chain F. Apply the litmus test before publishing: if a three-platform follower would find the content redundant, rethink rather than reformat.

---

## STEP 5: PRESENT AND ITERATE

**Output format:**

```
## [Platform] — [Topic/Framework]

**Constraint check:** [Confirm all Phase 1 rules pass]

**Limits check:** [each platform version against the limits table]

**Source material:** [Which wiki pages / raw articles informed this piece]

---

[The content]

---

**Repurposing notes:** [How this piece could be adapted for the other platforms]
```

After presenting, ask:
1. "Does this sound like you? What would you change?"
2. "Want me to adapt this for [other platform]?"
3. "Should I file this to the content pipeline?"

---

## STEP 6: FILE TO NOTION CONTENT DB (IF APPROVED)

If Juan approves the piece, file it to the Notion Content DB with the **Notion connector** (MCP tools `notion-*`; load them with ToolSearch). Do not use `content/scripts/notion-content.ps1` or `content/.notion-config.json` — that local key is dead and is not being renewed (Juan, 2026-11-25). The Notion Content DB is the operational source of truth; `content/raw/drafts/` is no longer used.

**Where:** Content DB, data source `collection://36aeedc9-595f-81f9-88f2-000b60546d69`. Fetch it first if you need the current field list.

**One row per platform version.** A piece going to five platforms is one source row plus one row per platform.
- The **source row** is the piece itself (usually the long or main version). Set `Format`, leave `Source piece` empty.
- Each **platform row** links back with `Source piece` = the source row's URL. Its sibling list shows up on the source row under `Versions`.
- X and Threads share one row (`Platform` = Twitter + Threads), since Threads gets a copy of every X post.

**Fields to set on every row:**
| Field | Value |
|---|---|
| `Title` | The hook or working title |
| `Platform` | One or more of LinkedIn, Twitter, Threads, Instagram, TikTok, YouTube, Blog |
| `Format` | One of the fourteen: Ranking, Pages worth stealing, Checklist, Brand study, Yearly tutorial, Free course, Life-lesson list, Learning diary, Resource, Contrarian take, Quote reaction, Live brand fix, Notes list, Brand verdict |
| `Type` | The shape of the post if one fits (Thread, Carousel, Short, YouTube Video, Infographic, Personal Post…) |
| `Status` | `Drafting` (Juan moves it to `Ready` himself once the media is attached and it passes the platform limits check) |
| `Date` | The posting slot from the weekly calendar, as a Madrid date and time (`date:Date:is_datetime` = 1). This is the time the scheduler posts at. A 01:00 slot is the night after its day (Monday's 01:00 = Tuesday 01:00). |
| `Source piece` | Source row URL (platform rows only) |
| `Notes` | Hook pattern used, plus the wiki pages and articles it draws on, by name |

Body of the page = the post text, ready to paste, in Notion Markdown.

**Promoting an existing Idea row** (Juan often runs `/content` with no topic, which picks the oldest Idea): update that row with `notion-update-page` instead of creating a new one: set the fields above and replace the body with the draft. It becomes the source row.

**Never touch** `Post Bridge ID`, `Last Sync At`, `Synced Edit Token` or `Published URLs` — the scheduler on Railway owns them. Result numbers (`Views`, `Comments`, `Saves`, `Follows`, `Signups`) are filled in at the weekly review, not at filing.

After filing, append a short entry to `content/memory/log.md` with the Notion page URL(s). `content/wiki/pipeline.md` and local drafts are historical only — do not touch them.

---

## REFERENCE: TOPIC -> WIKI PAGE MAPPING

When the user mentions a topic, read the corresponding wiki page for source material:

| Topic | Wiki Page |
|-------|-----------|
| Subscription metrics, churn, activation | content/wiki/subscription-metrics.md |
| Experimentation, Powered ICE, testing | content/wiki/experimentation-frameworks.md |
| Profitability, margins, contribution | content/wiki/profitability-levers.md |
| LTV, payback period, cohort analysis | content/wiki/ltv-frameworks.md |
| Growth formula, diagnostic | content/wiki/ecommerce-growth-formula.md |
| Incrementality, ROAS critique, MMM | content/wiki/measurement-incrementality.md |
| Forecasting, cohort projection | content/wiki/ecommerce-forecasting.md |
| Metrics hierarchy, MER, AOV critique | content/wiki/ecommerce-metrics-hierarchy.md |

---
Updated 2026-11-26: knows the notes list, brand verdict, framework carousel and infographic; wider brand screen; fourteen Formats; Mars Men rule matches Credential usage.
