---
title: "Considering Revenue in your Prioritization Framework"
description: "How to incorporate revenue potential alongside statistical detectability in experiment prioritization using Proxy Potential Revenue."
source: jcgiusto
original_url: "https://jcgiusto.com/considering-revenue-in-powered-ice/"
original_language: en
ingested: 2026-04-06
---

# Considering Revenue in your Prioritization Framework

**Author:** JC Giusto

## Overview

This article addresses a critical gap in experiment prioritization frameworks by incorporating revenue potential alongside statistical detectability.

## Core Problem

Traditional ICE Score and Powered ICE methodologies overlook a fundamental factor: "Two experiments with the same MDE aren't equal if one could generate substantially more revenue."

## The Revenue Impact Formula

The potential revenue calculation combines four key variables:
- Weekly Visitors
- Conversion Rate
- Average Order Value (AOV)
- Minimum Detectable Effect (MDE)

This produces: **Weekly Visitors x Conversion Rate x AOV x MDE**

## The Solution: Proxy Potential Revenue

Giusto proposes balancing revenue potential against detectability difficulty using an exponential decay formula:

**Proxy Potential Revenue = Potential Revenue x e^(-MDE/0.05)**

### Decay Factor Applications

The constant 0.05 targets typical A/B test MDEs (2-10%):
- At 2% MDE: penalty factor ~ 0.67
- At 5% MDE: penalty factor ~ 0.37
- At 10% MDE: penalty factor ~ 0.14

Alternative decay constants accommodate different risk profiles:
- 0.03: aggressive penalties (risk-averse organizations)
- 0.07: lenient penalties (early-stage programs)

## Implementation

The framework requires inputting journey data (page, device, segment, traffic, AOV, conversions, metrics) and pre-test MDE analysis, then automatically generates prioritization scores.

---

## Related Topics

- [[experimentation-frameworks]]
