---
description: Author + render on-brand carousels/placas (visual engine, Track A)
---
Render Juan's content into on-brand 1080×1350 images via the code-first visual engine.

Usage (run from the repo root):
- `python -m content.scripts.visual.cli new <slug>` — scaffold `content/raw/visuals/<slug>/piece.md`
- `python -m content.scripts.visual.cli render <slug>` — render `out/image-NN.png` (+ `bundle.pdf` for carousels)

Slide types (use as `# slide:<type>` blocks in piece.md):
cover · hook-stat · data-chart · concept-explainer · section-break · narrative ·
pull-quote · numbered-part · screenshot · infographic-framework ·
infographic-checklist · closing-cta.

Field conventions:
- Headlines/titles support a literal `\n` for a line break.
- Rich body fields (`text`, `body`, `quote`, `instruction`) accept inline HTML like `<b>…</b>`.
- `data-chart` bars: `bars: €10:34, €30:100*, €70:9` (`*` marks the highlighted bar).
- Pipe-structured: `card: 01 | Title | description`; `section: Header | item; item; item`.

Spec: docs/superpowers/specs/2026-05-29-visual-carousel-engine-design.md
Plan: docs/superpowers/plans/2026-06-02-visual-engine-core.md
