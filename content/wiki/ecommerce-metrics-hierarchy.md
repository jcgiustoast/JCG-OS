---
title: eCommerce Metrics Hierarchy
description: The 4-level metrics pyramid (Financial > Business > Customer > Platform), the Control vs Precision paradoxes, key metrics definitions (MER, aMER, nCAC), and why AOV lies.
type: topic
sources: [asteroi-en-ecommerce-metrics-framework.md, asteroi-es-ecommerce-metrics-hierarchy.md, asteroi-es-aov-is-lying-to-you.md, asteroi-es-10-ecommerce-growth-finance-metrics.md, asteroi-en-worst-mistake-7-figure-ecommerce.md]
related: [profitability-levers, measurement-incrementality, ecommerce-growth-formula, ltv-frameworks]
created: 2026-04-06
updated: 2026-04-06
confidence: high
---

# eCommerce Metrics Hierarchy

> There is no king metric. You need all levels simultaneously.

## The 4-Level Metrics Pyramid

### Level 1: Financial Metrics (True North)

Closest to reality. The ultimate objective.

**Contribution Margin = Revenue - Variable Costs (COGS + Shipping + Commissions) - Advertising Investment**

In eCommerce, advertising investment should be treated as a variable cost (15-35% of revenue in 7-8 figure businesses). It scales directly with revenue.

This margin funds three things:
1. Coverage of fixed operational costs
2. Inventory investment to sustain growth
3. Dividend distribution

**Profit = Contribution Margin - Fixed Expenses**

More complex to measure daily, but essential for strategic decisions.

### Level 2: Business Metrics (Health Indicators)

Reveal operational health without excessive tactical detail.

- **Revenue** -- gross sales minus discounts
- **Advertising Investment** -- total spend aimed at direct sales (prorate across channels if multi-channel)
- **MER (Marketing Efficiency Ratio)** = Revenue / Advertising Investment

**MER Warning:** Avoid over-optimizing MER alone. Pursuing high MER risks under-investing in advertising, limiting long-term growth for short-term efficiency.

### Level 3: Customer Metrics (Protecting the Future)

Ensure short-term optimization doesn't compromise future performance.

**Key risk:** Increasing revenue through excessive recurring customer emails advances sales that would occur naturally, depleting future potential. Prioritize new customer acquisition while maintaining recurring engagement.

- **New vs Recurring Customer counts** -- absolute numbers AND the relationship
- **aMER (Acquisition MER)** = New Customer Revenue / Advertising Investment (reveals true ad efficiency since ads primarily target new customers)
- **nCAC (New Customer Acquisition Cost)** = Advertising Investment / Number of New Customers
- **First Order Gross Margin / nCAC** -- use gross margin not AOV. Ratio below 1 = acquisition losses. **Keep above 1.**
- **AOV by segment** (new vs recurring) -- reveals product mix promoted across channels

### Level 4: Platform Metrics (Directional Only)

**Critical warning:** Furthest from financial reality. Indicative, not absolute.

- **ROAS** = Platform-Attributed Revenue / Ad Spend on Platform
- **iROAS** = ROAS adjusted by incrementality factor (see [[measurement-incrementality]])
- **In-Platform CAC** = Ad Spend / Platform-Attributed Sales

These provide directional guidance, not truth. See [[measurement-incrementality]] for why.

## The Two Paradoxes

### The Control Paradox
Lower pyramid levels offer greater control and action capacity. You can't directly move contribution margin, but you can improve Meta ROAS through new creatives or campaign restructuring.

### The Precision Paradox
Higher pyramid levels are closer to financial reality. Reliability decreases moving downward. **You must consider all levels simultaneously** to avoid biased decisions that optimize one level at another's expense.

## Why AOV Lies

87% of eCommerce businesses optimize AOV for a customer that doesn't exist.

### The Average Trap

A store with AOV of EUR 60:
- 450 orders at EUR 30
- 350 orders at EUR 65
- 200 orders at EUR 120

**Not a single order at EUR 60.** Setting a free shipping threshold at EUR 65 gave free shipping to 350 people who were buying the EUR 65 product anyway --> marginal contribution dropped.

### Three Problems with Averages

1. **Susceptible to outliers** -- 10 wholesale orders of EUR 1,000 inflate average from EUR 65 to EUR 70
2. **Zero distribution information** -- two stores with identical EUR 56 AOV can have completely different customer bases
3. **Destructive simplification** -- reducing complex segment behavior to one number

### The 3 Tools to Replace AOV

1. **Mean, Mode, Median** -- when mean < median, you have a left-tailed distribution. The mode (most common order value) tells you where most customers actually are.

2. **Histogram Analysis** -- group orders into intervals. The strategic question changes from "increase EUR 65 average" to "convert EUR 30 buyers into higher-value buyers."

3. **Segment Analysis** -- investigate demographics, behavior, and financial value per cluster:
   - Origin, age, gender
   - Preferred products, acquisition channel
   - 60-day and 360-day LTV per segment

### Data-Driven AOV Strategies

Instead of blanket tactics:
- If EUR 30 orders come from Meta with CPA of EUR 20 --> redirect to more profitable product campaigns
- For EUR 30 product users --> create upselling flows targeting EUR 35+
- Value incentive: gift for purchases above specific thresholds

## From Metrics to Forecasting

Real differentiation requires:
- Forecasts for each metric
- Specific daily expectations
- Early warning systems for deviations

Different problems demand different solutions: low new customer revenue requires different action than low recurring customer performance. See [[ecommerce-forecasting]].

## Content Potential

Phase 1 candidates (per [[content-strategy]]):
- The 4-level pyramid (infographic potential, high shareability)
- "The Control Paradox" and "The Precision Paradox" (unique frameworks)
- MER/aMER/nCAC definitions (educational, proves depth)
- "87% of eCommerces optimize AOV for a customer that doesn't exist" (attention-grabbing hook)
- The EUR 60 AOV example (relatable, concrete)
- "First Order Gross Margin / nCAC must be > 1" (simple rule, non-obvious)
- Histogram vs average visualization (data storytelling)
