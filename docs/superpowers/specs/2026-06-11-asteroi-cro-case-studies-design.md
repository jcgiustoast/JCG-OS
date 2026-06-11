---
title: ASTEROI CRO Case Studies — Design Spec
description: 3 ASTEROI-branded HTML case studies — one per client (GLAMRDiP, Parachute, David Protein), each featuring 3 experiments under a program context band. A CRO sales asset that frames a repeatable system, not lucky wins.
type: project
author: claude
sources: [content/scripts/visual/templates/theme.css, experimentation-os/clients/mars-men/schema.md]
related: [carousel-engine, professional]
created: 2026-06-11
updated: 2026-06-11
confidence: high
---

# ASTEROI CRO Case Studies — Design Spec

## Purpose & audience

A **sales asset for ASTEROI**. Goal: convert a DTC growth prospect by proving ASTEROI
runs CRO/experimentation as a *repeatable system*, evidenced by named-client wins told in depth.

First-principles framing: one win reads as luck; a program reads as a machine. So each
client file opens with program-level proof (themes + scoreboard), *then* drills into 3
experiments. The reader should leave thinking "they run an engine," not "they got a lift once."

## Scope — 3 clients × 3 experiments

| File | Client | Experiments |
|------|--------|-------------|
| `glamrdip.html` | GLAMRDiP | Improve the Kit Selector · Explain What the Kit Includes (IG Stories) · Replace First Kit Image with Video |
| `parachute.html` | Parachute | Make the search bar more prominent · Add Installments Price on PDP · **3rd TBD** (duplicate link supplied) |
| `david-protein.html` | David Protein | Subscription Preselected on PDP · Huberman Quote on PDP · Add option to subscribe on PLP |

Source Notion pages (private `jcgiusto` workspace):
- GLAMRDiP — `1fbeedc9595f804999b6dc2e4670dd50`
- Parachute — `1fbeedc9595f80d5b770c2b63a53e6dc`
- David Protein — `27feedc9595f812d9415cb43565400bb`

## Locked decisions

| Decision | Resolution |
|----------|------------|
| Primary use | ASTEROI sales asset (persuasive, outcome-led) |
| Format | **3 separate, self-contained HTML files — one per client** |
| Unit per file | Client context band → **3 experiment deep-dives** → CTA |
| Brand naming | **Named clients** (GLAMRDiP, Parachute, David Protein) — the earlier Mars-Men anonymization is moot |
| Control/variant visuals | **Real screenshots** from the Notion cards, used as-is |
| $ figures | Exact figures from the dashboard; dial back per-client if desired |
| ICE / method block | Included (differentiates ASTEROI as systematic) |

## Deliverable architecture

```
content/case-studies/
├── glamrdip.html
├── parachute.html
├── david-protein.html
└── assets/
    ├── fonts/            # Archimoto (.otf), Archivo (.ttf), Big Shoulders (.ttf) — copied from visual engine
    ├── asteroid-1.png  asteroid-2.png  asteroid-3.png
    ├── noise.jpg        # grain overlay
    ├── logo / avatar    # ASTEROI mark for footer
    └── screenshots/
        ├── glamrdip/        # control + variant per experiment
        ├── parachute/
        └── david-protein/
```

Each file references `./assets/...` with relative paths; the folder travels as a unit.
Optional later: base64-inlined "email-ready" variant per file.

## Brand system (reuse, don't reinvent)

Tokens lifted verbatim from `content/scripts/visual/templates/theme.css`:

- **Colors:** `--negro #0a0a0c` · `--blanco #fff` · `--verde #D3FF4E` · `--lila #B084D3` · `--gris-warm #EDEBEC`
- **Fonts:** Archimoto (display / UPPERCASE eyebrows + numerals), Big Shoulders Text (heavy headlines), Archivo (body)
- **Motifs:** star-field radial-gradient backgrounds, asteroid PNGs at corners, grain/noise overlay on every surface, lila + verde as the two accents
- **Surface logic:** dark cosmic = hero/quote/CTA; warm-gray = body/narrative; verde = punctuation/CTA; lila = featured panels + numerals

These are *case-study web pages*, NOT 300×375 carousel slides. Reuse tokens + motifs; ignore slide dimensions.

## Per-file anatomy

### A. Client context band (top of each file)

| Element | Source | Treatment |
|---------|--------|-----------|
| Client header | Client name + 1-line descriptor | Dark band, logo if available |
| Strategic themes | Themes the program surfaced (Name + 1-line problem) | Theme chips — shows diagnosis, not guessing |
| Program scoreboard | Aggregated from that client's experiments | Stat row: velocity · win rate · validated revenue · monthly $ added. **If only the 3 experiments are documented, downgrade to a "3 wins at a glance" highlights strip** rather than claiming program-wide velocity/win-rate. |

### B. Experiment deep-dive (×3 per file)

| # | Section | Fields | Treatment |
|---|---------|--------|-----------|
| 1 | **Header** | Name, Uplift %, hero $, Code, Location, Device, Type | Dark/cosmic band, lila eyebrow, Big Shoulders headline, verde hero stat |
| 2 | **At a glance** | Type, Location, Device, Growth Lever, Success Metric, Running Dates, Impact Spectrum | Compact meta strip |
| 3 | **The problem** | Parent Idea + supporting Insights | Warm-gray narrative — the "why" |
| 4 | **Hypothesis** | "If→then→because" | Featured lila panel |
| 5 | **The change** | Control vs Variant screenshots | Side-by-side + short "what changed" caption |
| 6 | **Results** | Result, Uplift %, Monthly + 1-Yr Revenue & Gross Profit (+ significance/sample if present) | Bold KPI block, verde/negro; Positive badge |
| 7 | **Method & rigor** | ICE (I/C/E) + Total | Bar gauges |
| 8 | **Learning & next step** | Learning text, Next Steps | Shows the flywheel |

A single **ASTEROI CTA** + footer closes the file (after the 3rd experiment), not each experiment.

## Program scoreboard — methodology (honest stats)

- **Velocity** — experiments run ÷ window (state it).
- **Win rate** — Positive ÷ completed; state the denominator.
- **Monthly revenue added** — Σ Monthly Revenue Impact across implemented wins.
- **CVR uplift** — do **NOT** average Uplift % across tests. Use cumulative validated revenue, or a traffic-weighted blended lift explicitly labeled. Show the method.
- If a client only has the 3 documented experiments, present the highlights strip — never imply a larger program than exists.

## Data inputs required (from Juan)

No Notion connection in this session (private `jcgiusto` workspace; URLs hit a login wall; no Notion MCP). Data arrives as **file exports** or via **browser-driven extraction** — see the open decision. Per client we need:

- All experiment card fields (hypothesis, type, location, device, lever, ICE, running dates, result, uplift %, revenue/profit impact, learning).
- Parent Idea + supporting Insight text (for §3 The problem).
- Control + variant **screenshot image files**.
- The client's strategic themes (name + problem) + full experiment list (for the scoreboard, if available).

## Tech approach

- One self-contained `.html` per client; shared `./assets/`. Hand-authored from a shared structure (no build step).
- `@font-face` from `./assets/fonts/`.
- `@media print` → clean PDF export per file.
- Responsive down to mobile.

## Non-goals

- Not a single deck or one long scrolling page (3 files).
- No live Notion integration / no automated render pipeline.
- Not built on the carousel slide system (only its brand tokens/motifs).

## Open items

1. **Parachute 3rd experiment** — the supplied link duplicates the 2nd (Installments Price). Need the real 3rd.
2. **Attribution framing** — Parachute + David Protein are Sharma-era clients; GLAMRDiP is current. Decide: "ASTEROI's work" vs "experiments Juan led" across roles.
3. **Data delivery** — export vs browser-driven (see below).
4. Per-client $ precision (default exact); client one-line descriptors; ASTEROI footer URL + CTA copy.

## Implementation sequence

1. Resolve data delivery → Juan provides exports / I extract via browser.
2. Build **one reference file** (strongest client) end-to-end → Juan signs off on look/feel.
3. Populate the other two from the same structure.
4. (Optional) email-inlined variants.
