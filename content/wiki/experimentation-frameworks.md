---
title: Experimentation Frameworks
description: Comprehensive experimentation methodology for eCommerce -- Powered ICE prioritization, subscription experimentation nuances, the 10 program elements, 5 critical experimentation areas, and P&L-driven experimentation.
type: topic
sources: [powered-ice-framework.md, considering-revenue-powered-ice.md, art-science-subscription-experimentation.md, ecom-growth-experimentation-program.md, five-elements-subscription-experimentation.md, unlock-pl-with-experimentation.md, ultimate-subscription-ecommerce-checklist.md]
related: [subscription-metrics, ecommerce-growth-formula, profitability-levers, ltv-frameworks]
created: 2026-04-06
updated: 2026-04-06
confidence: high
---

# Experimentation Frameworks

> Growth ideas fail more often than they succeed -- and that's normal. If our ideas are based on research and creativity, it's only a matter of time before one hits a home run.

## Powered ICE: Prioritization for Mature Brands

Traditional ICE (Impact, Confidence, Effort) works for startups but misses a critical factor for brands past $5-10M: **statistical power**.

### The Problem

Mature brands pursue incremental improvements (5% uplifts) that require detecting smaller effect sizes. Without considering power, you waste time on experiments you literally cannot detect.

### Power Scoring (1-5)

Based on Minimum Detectable Effect (MDE):

| Power Score | MDE Range | Interpretation |
|-------------|-----------|----------------|
| 5 | 2-4% | Excellent -- high traffic, can detect small changes |
| 4 | 4-6% | Good |
| 3 | 6-8% | Moderate |
| 2 | 8-10% | Limited |
| 1 | >10% | Poor -- consider if experiment is worth running |

When MDE falls below 2%, reconsider the p-value threshold.

### Example: Why Power Matters

- **Mobile landing page**: 3,700 weekly visitors, 2.7% CR -- requires 10% uplift detection (Power 1)
- **Cart Slider**: 7,053 weekly visitors, 26.6% CR -- requires only 6% uplift detection (Power 3)

The Cart Slider should be prioritized despite potentially lower Impact score.

### MDE Calculation Guidelines

- Run experiments for maximum 4 weeks (cookie deletion risk)
- Use 3-4 week testing windows
- Avoid MDEs below 2-3% at 90% significance without adjustments

### Revenue Extension: Proxy Potential Revenue

The Powered ICE framework can be extended by incorporating revenue potential into prioritization. The "Considering Revenue" extension adds a Proxy Potential Revenue calculation that weights the expected revenue impact of an experiment, not just its statistical feasibility.

## Subscription Experimentation: The 60-Day Rule

Subscription experiments differ fundamentally from standard A/B tests.

### The Core Problem

Standard metrics (conversion rate, AOV) fail to capture full subscription impact. A variant might decrease conversion by 1.25% but increase 60-day LTV by 7%.

**Key insight:** Evaluate subscription experiments by **Average Revenue per User after 30/60/90 days**, which encompasses conversion, AOV, retention, and time.

### Implementation Requirements

1. **Integration** -- connect A/B testing platform (Intelligems) with eCommerce store (Shopify)
2. **Customer Tagging** -- label customers by test group for later cohort analysis
3. **Cohort Tracking** -- monitor LTV progression across segments (Looker Studio, Excel)
4. **Statistical Analysis** -- use continuous metric testing (not binary conversion analysis) with revenue standard deviation

## 10 Elements of a Successful Experimentation Program

### 1. North Star Metric
A guiding compass beyond just revenue. Examples:
- Airbnb: Nights Booked
- TrueClassic: Customers purchasing 5+ t-shirts
- AG1: Number achieving fitness goals

### 2. High-Quality Data
Completeness + trustworthiness. As programs mature, capture: revenue, COGS, customer IDs, return rates. Trust is critical -- discovering errors erodes confidence in all results.

### 3. Research Framework
Not "throwing spaghetti at the wall." Essential methods:
- GA4 data analysis for friction/bottleneck detection
- Heatmaps + screen recordings
- Post-purchase surveys
- User testing
- Motivation surveys
- Business modeling (identifying highest leverage points)

### 4. Multidisciplinary Team
Include SEO, email, paid ads, product/UX, engineering, data analysis. Per David Epstein's Range: diverse teams produce more breakthroughs.

### 5. Prioritization Framework
Use Powered ICE (see above). For beginners, standard ICE is sufficient.

### 6. Documentation Platform
"The most important element." Centralized results enable:
- Team visibility into what worked/didn't
- Informed future experiments
- Cross-team learning (paid ads and UX teams learn from each other)

### 7. Communication Channels
Bottom-up idea capture. Jeff Bezos didn't invent Prime -- a junior engineer did. Build systems for ideas to reach the top.

### 8. A/B Testing Tool
Positive effects compound while negative effects are discarded. Results don't add -- they multiply.

### 9. Statistical Knowledge
Non-negotiable. Critical concepts: peeking, false positives/negatives, false discovery rates, non-binomial analysis.

### 10. Willingness to Embrace Failure
Accept failure as part of the process. Research and creativity reduce risk but never guarantee success.

## 5 Critical Experimentation Areas for Subscription eCommerce

1. **Offer structure** -- subscription discounts, prepaid plans, gift options, bundling
2. **Onboarding flow** -- first 60 days, portal tour, renewal preparation
3. **Retention mechanics** -- cancel flow, pause options, win-back campaigns
4. **Pricing and packaging** -- price testing, bundle composition, frequency options
5. **Expansion revenue** -- upsells, cross-sells, add-on timing

## P&L-Driven Experimentation

Experimentation should extend beyond traditional CRO into every line of the P&L:

- **Revenue experiments**: pricing, bundling, subscription take rate, upsells
- **Variable cost experiments**: shipping optimization, COGS reduction (HexClad example: reducing bundle from 13 to 12 units), return rate reduction
- **Fixed cost experiments**: AI vs human support, FAQ improvement reducing tickets, evaluating incremental revenue from affiliate/SMS platforms

See [[profitability-levers]] for the 11 specific levers to experiment on.

## Experiment Opportunities (Data Points)

| Experiment | Result | Source |
|-----------|--------|--------|
| Pre-selecting subscription option | Take rate 12% --> 23% | metric-tree |
| 10% discount + free gift vs flat 20% discount | Higher margins, same conversion | metric-tree |
| Portal tour email at 48 hours | First-month churn -34% | metric-tree |
| Email segmentation by purchase behavior | Second purchases +22% | metric-tree |
| Eliminating 2-month frequency option | Short-term LTV increase | metric-tree |
| Personalized cancel flow | Save rate 8% --> 24% | metric-tree |
| Escalating loyalty benefits | 360-day LTV +15% | metric-tree |
| Quick-add buttons in order emails | Add-on purchases +9% | metric-tree |
| Two-sided referral program | Referral rates doubled | metric-tree |
| Product bundling strategies | AOV +27% through starter kits | metric-tree |
| Price increase 8% | Conversion maintained, +180K EUR EBITDA | 11-profitability-levers |

## Content Potential

Strong for Phase 1 repurposing (per [[content-strategy]]):
- Powered ICE framework explanation (unique framework, high shareability)
- "Why subscription A/B tests need 60 days, not 2 weeks" (contrarian take)
- The 10 elements as a checklist thread
- Experiment results table (data-rich, proves depth)
- P&L experimentation concept (goes beyond CRO, shows business acumen)
