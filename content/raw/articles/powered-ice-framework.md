---
title: "Powered ICE - Prioritizing Experiments for Multimillion eCom Brands"
description: "Enhanced ICE scoring framework that incorporates statistical power for mature e-commerce experimentation programs"
source: jcgiusto
original_url: "https://jcgiusto.com/powered-ice/"
original_language: en
ingested: 2026-04-06
---

# Powered ICE - Prioritizing Experiments for Multimillion eCom Brands

## TLDR

The traditional ICE Score framework lacks a critical component for scaling brands: statistical power. As e-commerce businesses grow beyond $5-10 million in revenue, they pursue incremental improvements that require detecting smaller effect sizes. The solution introduces "Powered ICE," which incorporates a Power rating (1-5) based on minimum detectable effect (MDE) thresholds.

## Why Power Matters

Mature e-commerce brands face a unique challenge: "detecting those 5% improvements with confidence is hard." Traditional ICE scoring overlooks the statistical power needed to identify positive results reliably.

The framework demonstrates this through a practical example comparing two experiments:

- **Mobile landing page**: 3,700 weekly visitors, 2.7% conversion rate -- requires 10% uplift detection
- **Cart Slider**: 7,053 weekly visitors, 26.6% conversion rate -- requires only 6% uplift detection

Since detecting improvements in the Cart Slider requires smaller effect sizes, it should receive prioritization priority.

## Powered ICE Power Scoring

The enhanced framework assigns Power ratings based on MDE ranges:

- **Power 1**: MDE higher than 10%
- **Power 2**: MDE between 8-10%
- **Power 3**: MDE between 6-8%
- **Power 4**: MDE between 4-6%
- **Power 5**: MDE between 2-4%

When MDE falls below 2%, the recommendation is to reconsider the p-value threshold.

## Implementation

The accompanying spreadsheet automates power scoring by requiring:

1. Journey specifics (test page, device, segment)
2. Traffic metrics (weekly visitors, conversions)
3. Pre-test MDE calculation

## MDE Calculation Guidelines

Author JC Giusto recommends:

- Run experiments for maximum 4 weeks (due to cookie deletion)
- Use 3-4 week testing windows
- Avoid MDEs below 2-3% at 90% significance without adjustments

## Conclusion

While ICE scoring remains valuable for resource-constrained startups, mature organizations implementing rigorous experimentation programs benefit significantly from incorporating statistical power into prioritization decisions.

---

## Related Topics

- [[experimentation-frameworks]]
