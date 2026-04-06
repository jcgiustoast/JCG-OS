---
title: eCommerce Forecasting
description: The Tree Model for data-driven eCommerce forecasting -- recurring customers (roots), organic new (trunk), paid new (branches) -- plus cohort-based calculation methods and the Awake Customers metric.
type: topic
sources: [asteroi-es-ecommerce-forecasting.md, asteroi-es-why-ecommerce-stopped-growing.md]
related: [measurement-incrementality, profitability-levers, ltv-frameworks, ecommerce-metrics-hierarchy]
created: 2026-04-06
updated: 2026-04-06
confidence: high
---

# eCommerce Forecasting

> There is no favorable wind for the one who does not know where they are going. -- Seneca

## The Forecast as Execution, Not Guessing

Most eCommerces treat forecasting as speculation -- a forgotten document in a Drive folder reviewed barely once a month. The best use it as:

- A north star that sets objectives
- A yardstick to measure results daily
- A strategy and execution exercise
- An early warning system for deviations

Growing 30% year-over-year requires substantial changes, not just repeating the previous year. The forecast must answer: what will we do differently?

## The Tree Model

Three fundamental parts of any eCommerce business:

### The Roots: Recurring Customers
- Most profitable (no re-acquisition cost)
- Easiest to forecast (consistent cohort behavior)
- Function like a fuel tank -- needs regular refueling through acquisition

### The Trunk: Organic New Customers
- Already know the brand but haven't purchased
- Social media followers, email/SMS contacts, post-interactors
- **Would buy without paid advertising**

### The Branches: Paid New Customers
- Unknown people requiring convincing through advertising
- Most expensive to acquire, hardest to forecast
- Depend on external platforms
- **Would NOT buy without advertising**

### Why This Matters

A tree without deep roots falls with the first strong wind. An eCommerce relying primarily on paid advertising risks collapse from:
- Changes in advertising rates
- Algorithm changes and privacy restrictions (GDPR, iOS)
- New competition with lower prices

As the business matures, increasing recurring customer percentage and building brand is crucial for reducing platform dependency.

## Forecasting Recurring Customers (Cohort Method)

The most reliable forecast component. Cohort analysis reveals remarkably consistent LTV curves regardless of entry month.

### Calculation

**Month 0:** Recurring buyers = Month 1 revenue from Past Customers cohort

**Month 1:** Sum of:
- Month 2 of Past Customers
- Month 1 of Month 0 cohort

**Month 2:** Sum of:
- Month 3 of Past Customers
- Month 2 of Month 0 cohort
- Month 1 of Month 1 cohort

Each new month layers additional cohorts. **Key dependency:** Recurring customer volume depends on past acquisition -- forecast both simultaneously.

### Variance Factors
Cohort behavior may shift if you:
- Add new products to the catalog
- Improve SMS/email campaigns
- Introduce subscriptions or memberships

## Forecasting New Customers (Incrementality-Adjusted)

Organic and paid new customers are conceptually separate but practically difficult to distinguish without incrementality data.

### The Practical Approach

1. Analyze historical customers per channel
2. Apply incrementality factors (see [[measurement-incrementality]])

### Worked Example

eCommerce generating 500K from new customers in October, spending 100K (30K Google, 70K Meta):

| Channel | Spend | Platform Revenue | Incrementality Factor | Real Revenue |
|---------|-------|------------------|-----------------------|-------------|
| Google Brand | 30K | 160K | 0.3 | 48K |
| Meta Ads | 70K | 250K | 1.2 | 300K |

- **Paid new customers** = 48K + 300K = 348K
- **Organic new customers** = 500K - 348K = 152K

From this:
- **Ad-driven new customers:** forecast based on planned spend
- **Organic customers:** stable base + variable component (more ad spend --> more word of mouth)

### Critical Forecasting Caveats

1. **Historical data assumes status quo** -- improvements in creatives, conversion, or incrementality will change ROAS
2. **Efficiency decreases with investment** -- cannot assume constant ROAS at 2x spend
3. **Validate incrementality factors** with real tests; benchmarks are fallback only
4. **Consider seasonality** -- some months have greater acquisition capacity

## The Awake Customers Metric

From [[profitability-levers]] -- the key health indicator for forecasting capacity:

**Awake Customers = New Customers Acquired + Active Recurring + At-Risk Recurring - Dormant Recurring**

This measures customers with high repurchase probability. Monthly tracking reveals whether your acquisition is keeping pace with natural customer decay.

If Awake Customers is declining, your forecast must either lower expectations or increase acquisition investment.

## Content Potential

Phase 1 candidates (per [[content-strategy]]):
- The Tree Model analogy (visual, intuitive, unique)
- "Your recurring customers are a fuel tank" analogy
- Cohort-based forecasting method (shows analytical depth)
- Incrementality-adjusted channel forecasting (practical, differentiated)
- "Growing 30% requires doing different things, not just repeating last year"
