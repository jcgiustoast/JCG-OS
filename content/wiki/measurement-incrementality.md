---
title: Measurement & Incrementality
description: Why ROAS is unreliable (3 core problems), incrementality testing via Geo Holdouts, the Incrementality Factor formula, and a multi-round testing roadmap.
type: topic
sources: [asteroi-en-roas-doesnt-mean-shit.md, asteroi-es-roas-doesnt-mean-shit.md, asteroi-es-incrementality-testing.md, asteroi-en-ecommerce-metrics-framework.md, asteroi-es-ecommerce-metrics-hierarchy.md]
related: [ecommerce-metrics-hierarchy, profitability-levers, ecommerce-forecasting, ecommerce-growth-formula]
created: 2026-04-06
updated: 2026-04-06
confidence: high
---

# Measurement & Incrementality

> Incrementality tests are where data-driven marketing, experimentation, and finance converge.

## Why ROAS Doesn't Mean Shit

Three fundamental problems with ROAS as a decision-making metric:

### Problem 1: ROAS Is Manipulated and Unreliable

Platforms inflate reported ROAS to encourage higher spending.

- **Meta** uses default attribution: "Click 7 Days / 1 Day View" -- attributes sales from people who merely saw an ad and bought within 24 hours
- **Google** applies 30-day post-click attribution -- delayed purchases attributed to paid channels
- **Google Brand campaigns** exaggerate results up to 5x -- people searching your brand already intend to buy, but Google takes credit

Without incrementality testing, businesses may overestimate ROI by 150-300%.

**Recommendations by budget:**
- **>$10K/month:** Implement incrementality tests (mandatory)
- **<$10K/month:** Exclude recent buyers, use tighter attribution windows (7 or 1-day click), employ top-of-funnel creatives

### Problem 2: ROAS Ignores Business Economics

A 3.0 ROAS ($33 spent per $100 revenue) masks actual economics:

| Line Item | Amount |
|-----------|--------|
| Revenue | $100 |
| Acquisition cost | -$33 |
| VAT (10%) | -$10 |
| Product cost (30%) | -$30 |
| Shipping (5%) | -$5 |
| Returns (10%) | -$10 |
| Payment processing (5%) | -$5 |
| **Real margin** | **$7** |

**Effective real ROAS: 1.33** (not 3.0). Fixed costs further erode profitability.

### Problem 3: ROAS Lacks Holistic Context

Optimizing ROAS in isolation ignores interdependencies. The correct priority order:

1. **Total Marginal Contribution** (see [[profitability-levers]])
2. **Total MER** (Revenue / Advertising Investment)
3. **Customer segmentation** (new vs recurring, LTV windows)
4. **Incremental ROAS** (only then)

**Example:** If new customer LTV increases 70% by day 90, accepting breakeven ROAS is strategically sound -- invisible when examining ROAS alone.

## Incrementality Testing: Geo Holdouts

The most effective and accessible method for eCommerce.

### How It Works

Geographic locations (usually provinces/cities) divided into two groups:
- **Control** -- no changes
- **Variant** -- campaign/channel increased, decreased, or paused

After several weeks, measure sales evolution in both regions. The difference reveals true campaign impact.

### Control Group Methods

1. **Specific locations** -- select geographic areas as control
2. **Synthetic control by amalgamation** -- combine regions with different weights (30% of A, 50% of B, 20% of C)
3. **Algorithmic synthetic control** -- statistical models simulate expected behavior

### Worked Example

Two similar cities, Madrid and Barcelona. $20K Meta spend each. Each generates $100K/month revenue. Meta reports $50K attributed revenue per city (ROAS 2.5).

**Test:** Pause Madrid for one month.

**Result:** Madrid drops from $100K to $60K. Barcelona stays at $100K.

**Finding:** Meta actually generates $40K per city, not $50K. Real ROAS is 2.0, not 2.5.

### The Incrementality Factor

> **Incrementality Factor = Real Test ROAS / Platform-Reported ROAS**

In the example: 2.0 / 2.5 = **0.8 (80%)**

Apply this factor to all future platform reporting to get real numbers. Meta's results need to be reduced by 20%.

### Protecting Profitability

If your maximum affordable ROAS is 3.0, and Google Brand Search reports 10.0 ROAS:
- Incrementality factor of 20% --> real ROAS is 2.0
- What seemed profitable actually loses money

**Case study:** A clothing client discovered Google Branded Shopping (reported ROAS 8) had real incrementality of just 3. Pausing and redistributing budget generated 15% more in net sales.

## Multi-Round Testing Roadmap

Marketing is not static. A single test validates one hypothesis, but platforms change algorithms, audiences evolve, products change, competition shifts.

Recommended roadmap:
1. **Round 1:** Incrementality by platform (Google, Meta, TikTok)
2. **Round 2:** Incrementality by campaign type (Google Branded Search, PMax, YouTube)
3. **Round 3:** Incrementality by creative (creatives can drastically change campaign incrementality)
4. **Round 4:** Start over after 6 months

### Why Platforms Can't Fix This

Structurally impossible for platforms to measure true incrementality:
- Cannot track people who haven't seen their ads
- Cannot consider effects of other platforms
- Cannot account for cross-device behavior
- Increasingly limited by GDPR, AdBlockers, iOS privacy
- Not in their interest to show true results

## Integration with Forecasting

Incrementality factors are essential inputs for [[ecommerce-forecasting]]:

| Channel | Spend | Platform Revenue | Incrementality Factor | Real Revenue |
|---------|-------|------------------|-----------------------|-------------|
| Google Brand | 30K | 160K | 0.3 | 48K |
| Meta Ads | 70K | 250K | 1.2 | 300K |

Organic new customers = Total new customer revenue - Real paid new customer revenue.

## Content Potential

Phase 1 content candidates (per [[content-strategy]]):
- "Your ROAS Doesn't Mean Shit" (already published, high engagement potential -- repurpose as thread)
- The 3.0 ROAS --> 1.33 real ROAS breakdown (visual, shareable)
- Incrementality Factor formula (simple, actionable)
- Google Brand Search 5x exaggeration stat
- The Madrid/Barcelona example (concrete, memorable)
- Multi-round testing roadmap (shows systematic thinking)
- "150-300% ROI overestimation without testing" (attention-grabbing stat)
