---
title: Visual Carousel & Infographic Engine — Design
description: Code-first engine that turns Juan's content into on-brand LinkedIn/Instagram carousels, infographics, and single images. HTML/CSS templates rendered to PNG/PDF via Playwright. Brand = ASTEROI (jcgiusto.com footer).
type: spec
author: claude
status: draft — visual direction validated, ready to lock + write implementation plan
created: 2026-05-29
updated: 2026-05-29
confidence: high
related: [content-strategy, brand-voice]
---

# Visual Carousel & Infographic Engine — Design

> **Status:** Visual direction validated in browser against Juan's real hand-made carousel (the AOV piece). Brand spec is pinned and verified. **Not yet started:** locking this spec for implementation + writing the implementation plan. See `2026-05-29-visual-carousel-engine/HANDOFF.md` to resume.

## Goal

Give Juan a repeatable, code-first way to turn his written content into **on-brand visual assets** for LinkedIn and Instagram — carousels, single supporting images, and standalone infographics. The compounding asset is a **template library + brand theme**, not any single deck.

Primary job: **repurpose existing LinkedIn text posts into carousels/infographics.** (Auto-generation from post text is a Phase-2 feature; v1 is author-the-slides-then-render.)

## Key decisions (chronological)

1. **Production method = HTML/CSS templates rendered to PNG/PDF via headless browser (Playwright).** Rejected Gamma MCP (off-brand drift, per-piece cost, non-deterministic) and Canva. Rationale: Juan's content is structurally repetitive (frameworks, lists, contrarian reframes), he'll produce 50+ pieces, and a code-first vault should have a code-first engine. Theme file in git = version-controlled brand evolution.
2. **Authoring model = slide-library, not monolithic templates.** A carousel is a *sequence of typed slides* the user authors, not a single template auto-filled from a post. This matches how Juan actually builds carousels (the AOV piece is 22 hand-authored slides).
3. **Three output modes, one engine:** `carousel` (N slides → PNG set + PDF), `single` (1 slide), `infographic` (1 dense, often taller composition). Mode is a per-piece frontmatter field.
4. **Scope = "Lean":** the slide library + render pipeline + CLI. Auto-scaffold-from-post-text, Notion DB integration, and a web preview UI are explicitly deferred to Phase 2.
5. **Brand = ASTEROI's existing identity**, already documented as a skill (see Assets). Footer URL changed from `asteroi.co` → **`jcgiusto.com`** (Phase-1 stealth: drives traffic to Juan's personal site, not the agency; the text-content firewall still forbids ASTEROI mentions in copy, but the visual signature is acceptable as a personal-brand URL).

## Architecture

Mirrors the existing `/content` pattern (slash command + `content/scripts/` implementation).

```
JCG-OS/
├── .claude/commands/visual.md              # slash command Claude reads
├── content/
│   ├── scripts/visual/
│   │   ├── render.py                        # markdown → HTML(Jinja2) → Playwright → PNG/PDF
│   │   ├── templates/
│   │   │   ├── base.html.j2                 # 1080×1350 frame, @font-face, grain, footer
│   │   │   ├── theme.css                    # brand tokens (copied from asteroi-brand skill)
│   │   │   └── slides/<type>.html.j2        # one partial per slide type (13)
│   │   └── assets/                          # copied subset of "Asteroi Branding"
│   │       ├── fonts/   (Archimoto, Big Shoulders, Archivo)
│   │       ├── asteroids/ (Elementos cut-out PNGs)
│   │       ├── backgrounds/ (desaturated space photos)
│   │       ├── textures/ (noise tiles)
│   │       └── avatar.jpg
│   ├── raw/visuals/<slug>/
│   │   ├── piece.md                         # source: frontmatter + slide markdown
│   │   └── out/  image-01.png … N + bundle.pdf (carousel mode)
│   └── wiki/voice/carousel-templates.md     # documents the slide library
```

- **Self-contained inside JCG-OS** — brand assets copied in, not symlinked to `solari/` (which may live on a different machine).
- **Tech stack:** Python 3 + Jinja2 + Playwright (headless Chromium). Node+Puppeteer is an acceptable alternative; output identical.
- **Production note:** Playwright loads local HTML + local font/image files directly — **no base64 inlining needed**. (The mockups inline base64 only to work around the brainstorm preview server, which serves a single HTML file and 404s static assets.)

### CLI

```
/visual new <slug> --mode carousel|single|infographic   # scaffold piece.md
/visual render <slug> [--watch]                          # → out/image-NN.png
/visual pdf <slug>                                       # bundle to PDF (carousel only)
```

### `piece.md` format

```yaml
---
title: El secreto del AOV
mode: carousel        # carousel | single | infographic
aspect: 4:5           # 4:5 (1080×1350 default) | 1:1 (1080×1080) | 9:16 (1080×1920) | custom
---

# slide:cover
title: El secreto del AOV
subtitle: Que no conocías
background: space-2
accent: lila

# slide:hook-stat
text: "El **87% de los eCommerce** que conozco optimizan su AOV para fantasmas."

# slide:section-break
title: Un Caso Real Que Te Va a Impactar
...
```

## Brand spec (VERIFIED against Juan's real carousel)

This is the canonical brand layer. Sourced from the `asteroi-brand` skill + Juan's hand-made AOV carousel + high-res font comparison.

### Palette
| Role | Name | Hex |
|---|---|---|
| Primary | Negro | `#000000` |
| Contrast | Blanco | `#FFFFFF` |
| Accent 1 (hero) | Verde | `#D3FF4E` |
| Accent 2 (secondary) | Lila | `#B084D3` |
| Auxiliary | Gris | `#E7E5E6` |

### Typography (THE critical correction — confirmed by side-by-side render)
| Font | Role |
|---|---|
| **Archimoto V00 — Medium (500)** | Cover hero headline, big numbers (`01.`), the JCGIUSTO wordmark, quote attribution. The stencil "spice". **Medium weight — NOT Heavy** (Heavy is too thick; Juan's is airy/open-cut). |
| **Big Shoulders Text — Black (900)** | **ALL headlines** — section breaks, concept titles, infographic titles, numbered-part titles. Condensed-tall. (Earlier mistake: Archivo Black was wrongly used here — too wide/round, looked "robotic".) |
| **Archivo** | Body copy, labels, captions, bullets, cover subtitle. |

### Visual rules
- **Wordmark is two-tone:** `JC` = Verde-on-dark / Lila-on-light; `GIUSTO` = Blanco-on-dark / Negro-on-light. Avatar sits on a Lila circle.
- **Footer variants:** **centered, no arrow** on cover & quote slides; **left-aligned + bold arrow →** on content slides.
- **Dark slides use a desaturated space photo background** (`grayscale(1) brightness(~.45)`) + dark overlay — **never flat black**. Applies to cover, pull-quote, dark infographics.
- **Asteroids** = grayscale cut-out PNGs, **corner-anchored, bleeding off-canvas, in asymmetric pairs** (e.g. top-left + bottom-right). Never centered.
- **Grain texture** overlay (~10%, `mix-blend-mode: overlay`) on every slide for the tactile/analog quality.
- **Color discipline:** one Verde moment per slide max; Verde & Lila never at equal weight in the same block.
- **Pull-quote ("Insight Clave") composition:** space-photo bg + big WHITE centered Big-Shoulders title + a **translucent Lila rounded panel** holding the quote + large bracketing Lila quote marks + centered footer.
- **CTA composition:** Lila full-bleed bg + Big-Shoulders headline + a **Verde pill button**.
- **Section-break:** Verde full-bleed + condensed black headline + eyebrow label + corner asteroids.

## Slide-type library (13)

Carousel (8): `cover` · `hook-stat` · `data-chart` · `concept-explainer` · `section-break` · `narrative-paragraph` · `pull-quote` · `numbered-part`
Infographic (2): `infographic-framework` · `infographic-checklist`
Utility (1, any mode): `closing-cta`
Evidence types (the authenticity drivers, NEW from studying real work): `data-chart` (brand-colored histograms/bars — dark bars, one Lila highlight, Verde annotation) · `screenshot` (real product UI embedded in a browser frame + hand-placed Lila callout).

Each type's inputs + visual recipe are demonstrated in `slide-library-v4-src.html` (the editable source) and rendered in `RENDER-verified-v4d.png`. The full per-type input schema is TODO during the writing-plans step.

## Asset locations (on Juan's machine)

- **Brand assets:** `C:\Users\jcgiu\Documents\Asteroi Branding\` — logos (SVG/PNG/JPG, all color variants), fonts (`Tipografías/Archimoto V00`, `Big Shoulders Text`, `Archivo`), `Recursos/Elementos` (asteroid cut-outs), `Recursos/Imagenes` (space photos), `Recursos/Texturas y Fondos` (noise), `Manual de Marca.pdf`.
- **Brand skill (canonical brand rules + tokens.css):** `C:\Users\jcgiu\Documents\solari\.claude\skills\asteroi-brand\` (SKILL.md, assets/tokens.css, noise-texture.css, references/aesthetic-guide.md, logo-usage.md, color-print.md).
- A working font + image subset is copied into this spec's `2026-05-29-visual-carousel-engine/assets/`.

## Out of scope (Phase 2)

- Auto-scaffold `piece.md` from an existing LinkedIn post (Claude can draft manually for now).
- Notion Content DB integration (attach rendered PNGs to the post row).
- Web preview UI / live editor.
- `infographic-comparison`, `infographic-formula` slide types.

## Next steps (for the new chat)

1. Open `slide-library-v4.html` in a browser (it's self-contained) and review against `reference/` crops + `RENDER-verified-v4d.png`.
2. Decide any final visual tweaks (candidate open items below).
3. Lock this spec → invoke `superpowers:writing-plans` to produce the implementation plan.
4. Implement on a git worktree per repo policy.

### Open visual items to confirm before/while implementing
- Exact Archimoto weight for the cover hero (Medium confirmed close; could test Regular vs SemiBold).
- Real `data-chart` rendering approach (Chart.js in the HTML vs. pre-rendered matplotlib/SVG).
- `screenshot` slide: workflow for dropping in real Shopify/product screenshots (manual path in `piece.md`).
- Whether cover subtitle is Archivo (current) or Big Shoulders.
```
