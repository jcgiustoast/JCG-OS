---
title: Life Memory Log
description: Append-only chronological log of life/professional activity. Most recent first.
type: log
created: 2026-04-05
updated: 2026-04-07
---

# Life Memory Log

*Append-only. Most recent entries at the top. Never edit past entries.*

---

## [2026-04-07] session | "What is my One Thing?" — strategic priority analysis
- Reviewed entire JCG-OS system to identify highest-impact single activity for Phase 1.
- **Conclusion: Publishing content is The One Thing.** The entire Phase 1 domino chain starts with content: content -> inbound leads -> more clients -> Tincho can leave 18PM -> capacity unblocked -> Phase 2.
- The Mars Men credential is a depreciating asset (~12 months shelf life). Every week without publishing burns irreplaceable credential value.
- 37 existing articles are ready to repurpose. The jcgiusto.com articles (11) are almost entirely in-lane (CRO, experimentation, subscription eComm, LTV, unit economics).
- **Language decision confirmed:** English only for Phase 1. Mars Men credential only resonates with US DTC audience. Spanish deferred to Phase 3+ (2028+).
- **Top 3 articles to repurpose first:** (1) "Your ROAS Doesn't Mean Shit" — contrarian, built-in Economics Reveal; (2) "The Formula You Need to Unlock Your eCom Growth" — Growth Formula framework; (3) "A New Way of Thinking About LTV" — LTV framework.
- **System gaps identified:** No content pipeline tracker, no actuals-vs-targets scorecard, no content ideas filed, memory/wiki.md not compiled.

## [2026-04-07] update | Built /content and /content-research skills in Claude Code
- Created `~/.claude/commands/content.md` — content creation skill for Twitter/X, LinkedIn, and blog. Reads JCG-OS wiki for source material, enforces Phase 1 firewall automatically, writes in Juan's voice (data-driven mentor, Economics Reveal pattern, contrarian premises, specific numbers, no fluff).
- Created `~/.claude/commands/content-research.md` — competitive intelligence skill. Scrapes reference creators via Apify to analyze what hooks, formats, and topics drive engagement.
- **Apify integration tested and working:**
  - Twitter: `apidojo/tweet-scraper` — confirmed working (690 tweets from Taylor Holiday test run)
  - LinkedIn: `apimaestro/linkedin-profile-posts` — confirmed working (uses `username` param, not `profileUrls`)
- **Voice profile extracted** from 11 raw articles: identified 5 rhetorical signature moves (Economics Reveal, contrarian premise, framework building, specific numbers, provocative headlines with rigorous bodies), sentence structure patterns, vocabulary rules, argument structure (problem -> financial reality check -> framework -> implementation).
- **Reference creators loaded:** Taylor Holiday, Nick Sharma, Cody Plofker, Barry Hott, Dara Denney.
- Skills available via `/content` and `/content-research` slash commands.

## [2026-04-06] update | Pushed 4 commits to remote
- Pushed all session work to origin/master: strategic planning session, 1-5 year strategy doc, client narrative & OPSEC, boundary script refinement.
- All files now synced with GitHub.

## [2026-04-06] update | Added client narrative, OPSEC rules, and stealth acquisition playbook
- UNIT 1 CEO flagged optics issue: Juan's LinkedIn shows Mars Men, Tincho's shows 18PM. Neither looks committed to ASTEROI.
- Created "Client Narrative & OPSEC" section in projects.md with: operator-led narrative (reframe structure as advantage, not weakness), Mars Men firewall rules (boundary script for clients, LinkedIn privacy settings, never name Mars Men), stealth client acquisition playbook (content inbound, referrals, platforms, Tincho post-18PM, DTC communities, conferences; avoid cold outbound and public agency positioning).
- Key insight: content flywheel is the primary acquisition engine during stealth. Juan publishes as "Head of eComm at 9-figure brand." Prospects reach out. Juan routes to ASTEROI privately. Content never mentions the agency.
- Updated strategy.md Phase 1 with acquisition channels and Mars Men risk mitigation.
- Pages updated: life/wiki/projects.md, life/wiki/strategy.md

## [2026-04-06] update | Created life/wiki/strategy.md — 1-5 year strategy document
- Comprehensive strategy document with 5 phases from April 2026 through 2031.
- Covers: content positioning, Tincho resolution timeline, tool focus plan, financial projections, AURAL side bet parameters, key risks, and quarterly review checklist.
- Pages created: life/wiki/strategy.md
- Pages updated: life/wiki/index.md

## [2026-04-06] session | Strategic planning session — 1-5 year life strategy
- Deep strategy conversation covering financial reality, Mars Men constraints, ASTEROI scaling path, and content positioning.
- **Financial snapshot captured:** ~$100K savings (going to mortgage), $7K/month burn, ~$15K/month savings rate, ~$22.7K/month total personal income.
- **Mars Men constraints documented:** Non-compete (subscription brands in US only — current clients don't conflict), no equity path, ~12 month exit timeline. Content constraint: can discuss CRO/experimentation/subscription eComm publicly, cannot discuss Meta Ads (Raheel's domain, optics issue).
- **Tincho/18PM blocker identified:** Tincho owns 18PM agency, can't publicly represent ASTEROI until he leaves. Needs 1-2 more ASTEROI clients to sustain him full-time. This is the critical bottleneck for scaling.
- **Tool usage clarified:** Only 3 of 6 tools actively used by clients (Ad Creative System, Meta Ads Deployer, Sense). Also using Google Sheets + Looker for forecasting (manual). Priority: make active tools runnable by Tincho, stop building new tools.
- **Client acquisition channels:** 1 from The Starters (freelancer platform), 2 from LinkedIn inbound.
- **AURAL details:** $25K invested, $2K/month burn, just started. Marito operates full-time, Juan is strategist only. Keep as asymmetric bet.
- **Two-phase strategic plan created:** Phase 1 "Stealth Build" (now-Q1 2027) — build personal brand, resolve Tincho, reach $25-30K/month ASTEROI gross. Phase 2 "Transition" (Q2-Q4 2027) — leave Mars Men, go public, scale to 5-8 clients, $50-60K/month gross.
- **$5M path modeled:** Achievable by 2030-2031 (age 35-36) if ASTEROI scales to $2M/year revenue. Juan's 65% equity at 3-5x multiple = $3.9-6.5M + ~$2.4M accumulated savings.
- Pages updated: wiki/identity.md, wiki/professional.md, wiki/projects.md

## [2026-04-06] update | Split JC OS into two spaces (life + content)
- Restructured repo: life/ for professional & personal, content/ for content creation & exploration
- Root CLAUDE.md now routes between both spaces
- All existing wiki pages moved under life/
- Created content/ space with wiki/, raw/, memory/ scaffolding

## [2026-04-06] update | Aligned JC OS with Karpathy's LLM Wiki pattern
- Restructured CLAUDE.md as proper schema layer with three-layer architecture
- Added frontmatter to all wiki pages (title, description, type, sources, related, confidence)
- Created wiki/index.md as master catalog
- Added ingest, query, lint, and compile workflows to CLAUDE.md
- Adopted parseable log format with type prefixes
- Pages updated: CLAUDE.md, wiki/index.md, wiki/identity.md, wiki/professional.md, wiki/projects.md, wiki/learning.md, memory/log.md, memory/wiki.md

## [2026-04-05] session | JC OS created
- Built initial structure: CLAUDE.md, identity, professional, projects, learning, memory
- System rules defined. Morning briefing workflow established.
- Key context captured: Mars Men at $100M run rate, $27.5M Series A from L Catterton
- Juan owns CRO + retention + LP/website design & dev. Supports acquisition but does not own creatives or ad spend (that's Raheel).
- Correction applied: Clarified Juan's scope vs. Raheel's. Added Raheel as key person.
- Architecture decision: Migrated from Notion to local markdown files (Claude Code + Obsidian + GitHub).

---

**Related files:** [[wiki]] | All wiki files feed into this log.
