---
title: "Incrementality Tests: How to Discover the Real Impact of Your Campaigns"
description: "Comprehensive guide to incrementality testing for eCommerce using Geo Holdouts, including formulas, examples, and a multi-round testing roadmap."
source: asteroi-es
original_url: "https://asteroi.co/test-de-incrementalidad/"
original_language: es
ingested: 2026-04-06
---

# Incrementality Tests: How to Discover the Real Impact of Your Campaigns

## Introduction

If you are an eCommerce investing more than $30K/month in advertising and **you are not running incrementality tests, you are leaving 15-30% of profitability on the table**.

We all know we cannot trust Meta, Google, and TikTok results 100%.

It is like sending a child to grade their own homework and expecting them to tell the truth. In most cases -- _as in brand campaigns_ -- they inflate their results.

Fortunately, there is a way to know the real impact of your campaigns and make decisions based on data and experimentation.

**Incrementality tests.**

## What Is Incrementality

**Incrementality refers to the true impact of your marketing campaigns.**

It answers the question: _"How many extra sales has my marketing effort generated that would not have occurred without it?"_

To quantify not knowing the answer: _if you invest EUR 240K annually in advertising, it can mean erroneous investment decisions of EUR 60-96K per year_.

In an ideal world, **this information should be in the advertising platform dashboards, but we know we cannot trust their data**.

And not because of their fault, but because the system has structural limitations.

### Meta and Google Cannot Measure What Really Matters

In their effort to provide clarity, **the platforms report their results the best way they can** and allow you to configure when campaigns attribute sales to themselves and when they do not.

Let's look at an example.

Meta has 3 attribution settings:

* **7-Day Click**: The platform will attribute a sale when the user clicks on its ad and buys within 7 days.
* **1-Day Click**: The platform will attribute a sale when the user clicks on its ad and buys within 24 hours.
* **7-Day Click / 1-Day View**: The platform will attribute a sale when the user clicks on its ad and buys within 7 days, or when the user has seen the ad, did not click, but buys within 24 hours.

The system works but **has a fundamental limitation: it cannot distinguish correlation from causation**.

Platform attribution says _"this person saw/clicked the ad and bought. Therefore, I am responsible for the sale."_ But it ignores whether that person would have bought anyway.

The clearest example is Google brand campaigns.

In many cases, **when a person searches for your brand on Google, they already intend to buy,** but they click on the paid ad because it is what appears first.

**Google attributes that sale even though it was not responsible for generating it**, which makes your reports look spectacular, but your real sales do not increase.

### Do Not Expect the Platforms to Fix This

This is not a technical limitation of Meta, Google, and TikTok that gets solved with a new feature -- **it is structurally impossible for them to measure the true incrementality of their campaigns**, and there are several reasons:

* They cannot track people who have not seen their ads
* They cannot consider the effect of other platforms
* They cannot account for the same person across different devices
* They are increasingly limited by privacy regulations like GDPR, awareness of users using AdBlockers, and new operating systems like iOS
* It is not in their best interest to show true results

If you want to know the real impact of your marketing efforts, you need to take matters into your own hands and start developing incrementality tests.

## The Only Way to Know Your Real Numbers

Now that we understand why platforms cannot (and do not want to) measure the real incrementality of their campaigns, let's talk about how you can do it.

Several methods exist for testing incrementality, but the most effective and accessible for eCommerce is "Geo Holdouts."

In Geo Holdout tests, **geographic locations (usually provinces) are divided into two similar groups**:

* **Control**, where there will be no changes
* **Variant**, where the campaign or marketing channel to be measured is increased, decreased, or paused.

After several weeks, you measure how sales have evolved in the two regions.

The difference between them reveals the true impact of your effort.

The control group can take several forms depending on the method you use, but these are the most common:

1. **Specific locations:** You select specific geographic areas as the control group to compare with the treatment areas.
2. **Synthetic control by amalgamation:** You create a control group by combining several regions with different weights to match the treatment group (30% of A, 50% of B, and 20% of C).
3. **Algorithmic synthetic control:** You use statistical models to simulate how the treatment group would have behaved based on a control group.

Let's go through an example using specific locations to make it clearer.

_Note: This is a simplified example to illustrate the concept. In practice, we work with more sophisticated statistical models._

### Incrementality Test Example

We invest $40,000 on Meta in 2 similar cities, Madrid and Barcelona ($20K in each).

Each city generates $100,000/month in revenue.

In its reports, Meta says we are generating $50K in each region. That is, a ROAS of 2.5.

**To validate this, we run an incrementality test.**

We pause Madrid for one month and see how its revenue evolves.

After 30 days, we see that Madrid went from generating $100,000 to $60,000, while Barcelona continues generating $100,000.

**This test tells us that Meta actually generates $40,000, not $50,000.**

That is, it is attributing more sales than it should, and its ROAS is not 2.5 -- it is 2.

Now we know the real impact of our Meta campaign, but what can we do with it?

### Incrementality Factor

To "counteract" the extra attribution (or in some cases the lack of attribution) from the platform, we can apply what is called the "Incrementality Factor."

> Formula: Real Test ROAS / Platform-Reported ROAS

In our case: 2/2.5 = 0.8 or 80%

The next time you look at Ads Manager, you know that **Meta's results need to be reduced by 20% to reflect real incrementality and over-attribution**.

This allows you to control spending and prevent platform ROAS from misleading you.

#### How Incrementality Tests Protect Your Profitability

For example, suppose **the maximum you can afford is a ROAS of 3, and you have a Google Branded Search campaign with a ROAS of 10** that, although your agency says is spectacular, you suspect is inflated.

You run an incrementality test and discover that this campaign **has an incrementality factor of 20%.** That is, the ROAS that was previously 10 is actually 2.

**What previously seemed profitable, you now know loses money**. That is the power of these experiments.

One of our clients in the clothing sector discovered that their Google Branded Shopping campaign, which reported a ROAS of 8, had a real incrementality of just 3.

Pausing it and redistributing that budget to channels with higher incrementality generated 15% more in net sales.

### Life After the First Incrementality Test

After your first incrementality test, the real work has just begun.

Like CRO -- where I come from -- **you start seeing the real returns of these practices after months and multiple experiments.**

Running a single test is fine to validate a specific hypothesis and introduce yourself to this world, but **marketing is not static**: platforms change their algorithms, your audiences evolve, you develop new products, and new competition appears.

Moreover, you can become increasingly granular or test new channels.

This is an example of a roadmap we built for one of our clients:

* **Round 1**: Incrementality by platform (Google, Meta, TikTok)
* **Round 2**: Incrementality by campaign type (Google Branded Search, PMax, YouTube)
* **Round 3**: Incrementality by creative: Although it may not seem like it, the creative can drastically change a campaign's incrementality
* **Round 4**: Start over after 6 months

The value is in making experimentation part of your culture.

This way **you ensure you are not making decisions based on outdated data, but on recent experiments**.

And if your eCommerce sells through other channels like Retail or Amazon, incrementality will be an essential tool to determine the real value your campaigns produce, not only on your website but across all points of sale.

## Conclusion

Incrementality tests are where data-driven marketing, experimentation, and finance converge.

**Introducing them into your operations will not only make your efforts more efficient** -- it will give you the confidence of knowing that every euro invested is generating real returns.

What is also true is that existing platforms are expensive and do not go below $2,000 per month.

That is why **we developed an internal methodology that allows us to run these tests at no additional cost for our clients.**

We know it is the only way to have real clarity on the impact of our work.

And that without this clarity, **both we and our clients risk optimizing metrics that do not translate into real growth**.

If you manage a considerable budget and are interested in validating the real incrementality of your channels, we can review your specific situation and explore how these tests could be applied.

---

## Related Topics

- [[measurement-incrementality]]
- [[ecommerce-forecasting]]
- [[ecommerce-metrics-hierarchy]]
