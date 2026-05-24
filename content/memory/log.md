---
title: Content Memory Log
description: Append-only chronological log of content-related activity. Most recent first.
type: log
created: 2026-04-06
updated: 2026-05-24
---

# Content Memory Log

*Append-only. Most recent entries at the top. Never edit past entries.*

---

## [2026-05-24] migration | Content operational layer moved to Notion

- **Notion DBs created** (Content OS workspace):
  - Content DB (lifecycle: Idea -> Researching -> Drafting -> Ready -> Scheduled -> Published) with 11 properties incl. Hook type, Source wiki, Source articles, Published URL.
  - Research DB (competitive intel briefs) with Date, Platform, Topic, Creators scraped, Posts analyzed, Informed pieces relation.
  - Two-way relation: Content.Source research <-> Research.Informed pieces.
- **Knowledge Mirror created** under "JCG-OS Knowledge" sub-page. 50 pages pushed (13 wiki + 37 raw articles) via new `/content-sync` skill.
- **Skills updated:**
  - `/content` -> drafts now filed to Notion Content DB (Status=Drafting); no-args mode promotes oldest Idea from backlog.
  - `/content-research` -> briefs filed to Notion Research DB.
  - `/content-sync` (new) -> idempotent one-way sync of local markdown to Notion mirror.
- **Helper scripts** (`content/scripts/`):
  - `notion-sync.ps1` — knowledge mirror sync (create/update/archive, rate-limited).
  - `notion-content.ps1` — Content DB query-ideas / create-draft / promote-idea.
  - `notion-research.ps1` — Research DB create-brief.
- **Local archived:** `pipeline.md` marked historical; `content/raw/drafts/` and `content/raw/research/` no longer written to.
- **Backfilled:** 12 Idea rows from priority repurposing queue (7 items split per platform).
- **Tech choice:** Notion HTTP API directly via PowerShell Invoke-RestMethod (the official `ntn` CLI doesn't support Windows yet). Markdown Content API + data sources, Notion-Version `2026-03-11`.
- **Config:** `content/.notion-config.json` (gitignored) — integration token, DB IDs, data source IDs.
- **State:** `content/memory/notion-sync-state.json` (gitignored) — local-path -> Notion-page-ID map (50 entries).
- **Spec:** `docs/superpowers/specs/2026-05-24-notion-content-system-design.md`
- **Plan:** `docs/superpowers/plans/2026-05-24-notion-content-system.md`

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
