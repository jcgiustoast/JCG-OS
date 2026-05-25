---
title: Content Memory Log
description: Append-only chronological log of content-related activity. Most recent first.
type: log
created: 2026-04-06
updated: 2026-04-20
---

# Content Memory Log

*Append-only. Most recent entries at the top. Never edit past entries.*

---

## [2026-04-20] draft | LinkedIn — Your 3.0 ROAS is a 1.33
- First piece in Phase 1 execution. Week of 2026-04-20 plan: Mon LinkedIn (this), Tue Twitter thread (repurpose), Wed Twitter single (AOV), Thu LinkedIn short (60-Day LTV Multiplier), Fri Twitter.
- Hook: Economics Reveal. Format: standard LinkedIn (~1,580 chars). Voice: Contrarian Premise + three-problem breakdown + replacement hierarchy (MC → MER → segment → iROAS).
- Drafts created: `content/raw/drafts/linkedin-roas-doesnt-mean-shit.md`
- Pipeline updated: pipeline.md row 1, LinkedIn actual 0 → 1.
- Source article: `asteroi-en-roas-doesnt-mean-shit.md`. Wiki: [[measurement-incrementality]], [[ecommerce-metrics-hierarchy]].
- Next: draft Twitter thread version (Path A repurpose chain — LinkedIn seeds the thread).

---

## [2026-04-20] translate | LinkedIn archive — 30 posts to English
- Filtered 50 Spanish posts down to 30 candidates (body >200 chars, excluding 6 dated video/podcast promos + one duplicate repost).
- Wrote sibling `.en.md` file for each at `content/raw/articles/linkedin-posts/<date>-<slug>.en.md` with frontmatter linking back to the Spanish source via `translates:` field.
- Style: **adapted**, not literal — LinkedIn-English voice per [[voice/brand-voice]] + [[platforms/linkedin]]. First-line hooks, finance-literate tone, specificity retained (dollar amounts, framework names, book references). Spanish idioms replaced with English equivalents. Emojis minimized.
- Not translated: 20 posts = 14 short headlines (<100 chars) + 5 dated video/podcast promos + 1 ROAS re-post that duplicates 2026-01-28.
- Use as Phase 1 English draft inventory for [[pipeline]] — not as-is re-posts. Some (founder focus story, tree analogy, CEO vs CMO dialogue) are ready; others need a fresh hook tuned for the English audience.

---

## [2026-04-20] ingest | LinkedIn archive (50 posts)
- Ingested `content/raw/articles/linkedin-posts-2026-04-20.json` (50 posts, Sept 2025 – Feb 2026, all Spanish).
- Normalized each post into `content/raw/articles/linkedin-posts/<date>-<slug>.md` with frontmatter (post_id, url, posted_at, language, likes, comments, shares, images, scraped).
- Built themed index at [[linkedin-archive]] with 7 themes (attribution/incrementality, Meta Ads tactics, finance/P&L/metrics, forecasting, growth philosophy, ecosystem takes, content promos).
- Linked from [[content-index]] under Raw Articles section.
- **Top observations for strategy:** lead magnets dominate engagement (Andromeda guide 375 comments, P&L model 176, subscription checklist 141); short one-liners under 100 chars consistently underperform; attribution/incrementality is the most repeated signature theme (~11 of 50 posts); corpus is 100% Spanish — treat as raw material to translate/adapt for Phase 1 English channels, not re-post as-is.

---

## [2026-04-20] refactor | Skill-graph layer extracted from /content command
- Applied the "JCG Content System" skill-graph pattern (source: `Downloads/JCG Content System.txt`) to JCG-OS. Plan: `~/.claude/plans/we-are-working-on-scalable-tarjan.md`.
- **Extracted 10 new nodes** from `/content.md` and `content-strategy.md` into `content/wiki/`:
  - `voice/brand-voice.md`, `voice/platform-tone.md`
  - `platforms/twitter.md`, `platforms/linkedin.md`, `platforms/blog.md`
  - `engine/hooks.md`, `engine/repurpose.md`, `engine/content-types.md`
  - `audience/operators.md`, `audience/founders.md`
- **Slimmed `/content.md`**: STEP 3 (voice) and STEP 4 (platform format) now read the extracted nodes instead of embedding rules. Added STEP 4.5 (hooks) and STEP 4.6 (chain order).
- **Added Engine section to `content-index.md`** indexing all 10 nodes.
- **Juan-specific adaptations vs the source article:**
  - Kept 3-platform scope (Twitter + LinkedIn + blog), not 10 — matches Phase 1 reality
  - Reversed the article's X-first chain: Juan's repurpose chain is long-form-first (blog/LinkedIn seed → Twitter compression) because the Economics Reveal needs math room
  - Codified Juan's 4 signature rhetorical moves as hook formulas (Economics Reveal, Contrarian Premise, Framework-First, Specificity) + added Credential Anchor flagged Phase-1-only
  - Phase 1 firewall duplicated into each platform node for format-time catching, not just constraint-time
- **Next step:** test `/content twitter ltv` and `/content linkedin powered-ice` to verify output quality is preserved (or improved by explicit hook surfacing). Tune individual nodes based on output.

## [2026-04-07] decision | Content engine built — ready to publish
- Built `/content` skill (Claude Code command) for creating Twitter, LinkedIn, and blog content grounded in JCG-OS wiki pages. Enforces Phase 1 firewall, writes in Juan's voice, formats per platform.
- Built `/content-research` skill for competitive intelligence via Apify scraping. Scrapes reference creators (Taylor Holiday, Nick Sharma, Cody Plofker, Barry Hott, Dara Denney) to analyze top-performing hooks, formats, and topics.
- **Confirmed priority repurposing queue:**
  1. "Your ROAS Doesn't Mean Shit" — Twitter thread + LinkedIn
  2. "The Formula You Need to Unlock Your eCom Growth" — LinkedIn long post
  3. "A New Way of Thinking About LTV" — all 3 platforms
- **In-lane filter applied:** Of 37 articles, jcgiusto.com (11) and several ASTEROI EN articles are fully in-lane. Meta Ads articles (Andromeda, 10 ROI strategies, making Meta profitable) are off-limits for Phase 1.
- **Next step:** Run `/content-research` to scan competitive landscape, then produce first batch of repurposed content.

## [2026-04-06] ingest | Full content ingestion — 37 articles from 3 sources
- Ingested 11 articles from jcgiusto.com (Subscription eCommerce Lab)
- Ingested 9 articles from asteroi.co/en (ASTEROI Blog English)
- Ingested 17 articles from asteroi.co (ASTEROI Blog Spanish) — translated to English
- 2 articles partially ingested (gated content): ultimate-subscription-ecommerce-checklist.md, summary-69-best-growth-books.md
- All saved to content/raw/articles/ with YAML frontmatter
- Created 8 wiki synthesis topic pages: subscription-metrics, experimentation-frameworks, profitability-levers, ltv-frameworks, ecommerce-growth-formula, measurement-incrementality, ecommerce-forecasting, ecommerce-metrics-hierarchy, meta-ads-optimization
- Each topic page extracts frameworks, formulas, data points, and flags content repurposing candidates for Phase 1
- Updated content-index.md with full article inventory and topic page catalog
- Pages created: wiki/subscription-metrics.md, wiki/experimentation-frameworks.md, wiki/profitability-levers.md, wiki/ltv-frameworks.md, wiki/ecommerce-growth-formula.md, wiki/measurement-incrementality.md, wiki/ecommerce-forecasting.md, wiki/ecommerce-metrics-hierarchy.md, wiki/meta-ads-optimization.md
- Pages updated: wiki/content-index.md

---

## [2026-04-06] session | Content space created
- Set up content/ space within JC OS for content creation and topic exploration.
- Structure: wiki/ for topic pages and ideas, raw/ for references and drafts, memory/ for this log.

---

**Related files:** [[content-index]]
