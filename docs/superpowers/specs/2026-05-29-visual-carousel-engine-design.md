---
title: Visual Carousel & Infographic Engine — Design
description: Code-first engine that turns Juan's content into on-brand LinkedIn/Instagram carousels, infographics, and single images. HTML/CSS templates rendered to PNG/PDF via Playwright. Brand = ASTEROI (jcgiusto.com footer). Track B adds an optional KIE-generated illustration layer for visuals no template fits.
type: spec
author: claude
status: draft — visual direction validated, ready to lock + write implementation plan
created: 2026-05-29
updated: 2026-06-02
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
6. **Layout QA is a pipeline stage, not manual review** (added 2026-06-02). Every slide is checked for hidden/clipped text using browser *geometry* (not vision), with a bounded auto-fix ladder and **pause-and-ask** escalation routed to the content agent. See the Layout QA section.
7. **Track B = generative fallback via KIE** (added 2026-06-02). When no template fits an evocative/illustration visual, KIE generates a *brandless, text-free illustration* that the HTML engine composites and brand-grades; bare raw images are allowed as an explicit opt-out. Templates (Track A) remain the ~80% default. See the Track B section.

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

## Layout QA stage (collision detection → bounded auto-fix → pause-and-ask)

A render-pipeline stage that runs **per slide, between Playwright render and PNG export**. Guarantees no text is hidden behind other text or shapes, and no text is clipped at the frame. Brand-independent; applies to all slides and all three modes.

**Why geometry, not vision.** Because slides are HTML, we don't analyze PNG pixels to guess overlaps — we query the browser. The check hit-tests every visible text node via the browser's own paint order: for each text node's glyph rectangles (`Range.getClientRects()`), sample points and call `elementFromPoint`. If the topmost element at a glyph's pixels isn't that text's own node (nor an inline descendant), the text is occluded. Deterministic, instant, no model, runs inside the same Playwright session that renders the slide.

**Three failure modes detected:**
1. **Text-on-text** — two text elements overlapping.
2. **Text-under-shape** — an opaque element (callout, bar, panel) painted over text.
3. **Text clipped at frame** — text overflowing the 1080×1350 (or aspect-specific) artboard or an `overflow:hidden` container.

**Auto-fix ladder** (per colliding slide; cheapest/safest move first; bounded):
1. **Reposition** the floating element to its nearest *legal* anchor — each floating component (e.g. callout) declares a whitelist of anchor points; pick the closest collision-free one.
2. **Reflow** — wrap text / trim padding within the element's own box.
3. **Scale font down** — only to a **per-role floor** (headline / label / body floor). Never below the floor.
4. **Re-check** after each pass; loop capped at **3 passes** (prevents fix-A-breaks-B ping-pong).
5. Every change is **logged** ("headline 64→56px; callout TR→BR") — no silent design drift.

**Escalation = pause-and-ask** (ladder exhausted: still colliding after the cap, or a fix would breach a floor). The engine stops on that slide and emits a **decision packet**:
- a render of the failed slide with the collision **boxed in red** (see it, don't read about it),
- the ladder steps tried + why each failed, with **miss magnitude** ("callout needs 18px less width than the largest legal anchor"),
- an **action menu**: shorten text *(default suggestion)* · allow one-time floor breach · hand-tweak · skip slide · accept best-effort.

**Who answers the pause.** In an agent-driven run the packet goes to the **content agent first** — it authored the copy, so its first move is to rewrite tighter and on-brand. It escalates to Juan only when shortening would change the message. Rationale: most *unfixable* collisions are **content-length** problems, not layout problems — no geometric move fits 12 words into a callout sized for 5.

**Layout rule this forces (folds into the slide library):** *cover* and *list/content* are distinct archetypes. Any slide combining a headline with content below it gets a **hard-capped headline zone** — the headline must fit its band (triggering the ladder) *before* it can overrun the content beneath. Prevents the observed failure where a 4-line cover headline ("Las 3 Herramientas del CMO Inteligente") crashed into the first list item.

**Config knobs (theme-level):** per-role font floors · retry cap (default 3) · `strict` toggle (turns pause-and-ask into a hard block for any future unattended batch) · optional post-export **vision legibility pass** — flags low-contrast text on busy/space-photo backgrounds; off by default, never used for collision detection.

> Implementation TODOs (resolve during writing-plans): per-component anchor whitelists, the per-role font-floor values, and the decision-packet surface (CLI prompt vs. written report the agent reads).

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

## Track B — Generative fallback (KIE image layer)

Track A (templates) is the default and handles ~80%+ of content. **Track B uses the KIE API to generate an *illustration* when no template fits** — under strict brand discipline so it never reintroduces the off-brand / mangled-text problems templates exist to prevent.

### When to use Track B (routing)

Decision rule — *is the visual carrying information or evoking something?*
- **Information** (list, steps, stats, framework, comparison, quote, chart) → **Track A template.**
- **Evocation** (metaphor, mood, a scene/object that can't be drawn with type + shapes) → **Track B.**

Exact tiebreaker — the **capability test**: *"Can it be built from type + shapes + a few hand-drawn marks?"* Yes → template. Needs a *rendered picture* → KIE.

**Default bias: when in doubt, template.** KIE costs credits, is non-deterministic, and isn't precisely re-editable. The bar for KIE is "the illustration *is* the point," not "an illustration would be nice."

### Three output flavors (a spectrum, not a binary)
1. **Pure template** (Track A) — most content.
2. **Template + KIE illustration layer** — *the default KIE case.* KIE generates the illustration; the HTML engine composites it as a background/hero layer and renders all text, wordmark, footer, asteroids, and accents on top.
3. **Raw KIE image** — a generated image with no template structure. Two sub-modes:
   - `raw` (default for this flavor): KIE output **+ brand grade + grain + footer**. No template, but still brand-treated.
   - `bare`: the unmodified KIE output — no treatment, no footer. Explicit opt-out, used sparingly, for a genuinely raw atmospheric image.

### The non-negotiable brand discipline
- **No text baked into the generated image — ever.** Text is the one thing image models botch and the one thing we don't need them for; all copy is rendered by the HTML layer in brand fonts. The KIE prompt explicitly forbids text / lettering / watermarks.
- **Brand normalization is enforced downstream, not trusted to the model.** Every KIE image (flavors 2 and 3-`raw`) passes through the *same* treatment the brand already applies to space-photo backgrounds — `grayscale(1) brightness(~.45)` + dark overlay + ~10% grain (`mix-blend-mode: overlay`). This makes the model's color/style choices irrelevant: output is forced into the ASTEROI monochrome-plus-accent look regardless of what KIE returns. **Brand coherence does not depend on prompt obedience.**
- **Brand accents are added by the engine, not generated.** Verde/Lila moments, the wordmark, hand-drawn marks = HTML/CSS, following existing color discipline (one Verde moment per slide; Verde & Lila never equal-weight). KIE produces only a desaturated base, never brand color.
- **Text-safe composition.** The KIE prompt requests generous negative space where the HTML text will sit, so the overlay has room. Layout QA then runs normally on the HTML text (flavors 2 and 3-`raw`). The `bare` flavor has no HTML text → QA N/A.

### KIE prompting best practices (encode in the engine; refine in writing-plans)
- Fixed **brand style suffix** appended to every prompt: *monochrome / desaturated / editorial or flat illustration / high contrast / strong negative space / no text, no words, no letters, no watermark.*
- **Aspect ratio = the piece's artboard** (4:5 / 1:1 / 9:16); generate at ≥2× artboard resolution for crispness.
- **Deterministic seed** where the model supports it — makes re-runs reproducible, blunting the non-determinism caveat.
- Optional **brand reference image** (img2img / style reference) if the selected model supports it, to nudge style.
- **Model selection within KIE deferred to writing-plans** (KIE aggregates several models; we want strong *illustration/style* control — text rendering is irrelevant since text is HTML's job).

### Pipeline placement & dependency
Track B composites into the same HTML → Playwright → PNG pipeline as Track A (the KIE image is a CSS background/hero layer), so it **depends on Track A existing first.** A generated image is fetched once and **cached** in the piece's `raw/visuals/<slug>/` dir, so re-renders don't re-spend credits or change the image.

### `piece.md` additions
```yaml
# slide:cover
illustration: kie                 # omit this field = template-only (Track A)
illustration_prompt: "a single coin frozen mid-flip in deep space, editorial flat illustration"
illustration_flavor: layer        # layer (default) | raw | bare
illustration_seed: 12345          # optional, for reproducibility
```

### Caveats (why Track B stays the exception)
Credits per image · non-deterministic across runs (mitigated by seed + caching) · not precisely re-editable (a template is; a raster isn't). Prefer Track A whenever a template can carry the message.

> Implementation TODOs (writing-plans): KIE API integration + key handling (env/secret, **never committed**), model choice, the generate→cache→composite flow, and the brand-grade CSS layer (reused from the dark-slide rule).

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
