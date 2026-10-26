# Figma post designer skill — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A `/figma-post` skill that builds Juan's carousels, single images and infographics in his Contenido Figma file, in his style, in three sizes.

**Architecture:** A one-time "🧩 Bloques JCG" page of components cloned from Juan's real slides; a Python script that turns Archimoto text into SVG outlines (Figma's scripting can't load that font); a project skill (`SKILL.md` + reference files) that tells the agent how to assemble designs from the blocks with `use_figma`.

**Tech Stack:** Python 3 + fontTools 4.62 + pytest · Figma Plugin API through the Figma MCP `use_figma` tool · Markdown skill.

**Spec:** `docs/superpowers/specs/2026-10-26-figma-post-design-skill-design.md`

## Global Constraints

- Figma file: `U2HIUwTWDYWL7EwSKCDpLd` ("Contenido"). Read `skill://figma/figma-use/SKILL.md` (and `figma-generate-library` for Task 2, `figma-generate-design` for Task 4) via `get_figma_skill` before any `use_figma` call; pass `skillNames` with the `resource:` prefix.
- Colours only: Lila `#B084D3`, Verde `#D3FF4E`, Gris `#E7E5E6`, Negro `#000000`, Blanco `#FFFFFF`; infographic tints light Lila `#D8C1EA`, deep Lila `#7E4FA6`.
- Fonts: Big Shoulders Text Regular/Bold, Archivo Regular/Bold, Inter Regular (load in Figma); Archimoto V00 Regular/Bold only as outlines from Task 1.
- Footer URL is `jcgiusto.com` — never `asteroi.co`.
- Sizes for every type: 1000×1250, 1300×1080, 1080×1920.
- Body text never below 32px on a 1000-wide frame (scale proportionally for other widths).
- Skill folder: `.claude/skills/figma-post/`.
- Juan's repo rule: **no commits during execution**; Juan is asked once at the end (Task 5).
- Never modify or move Juan's existing slides; read and clone only.

## Review Focus

1. Spanish text (¿ ¡ ñ accents) in Archimoto outlines must render, not drop characters → Task 1 test `test_spanish_characters`.
2. A character missing from the font must fail loudly, not leave a gap → Task 1 test `test_missing_glyph_raises`.
3. Clones of old slides carry `asteroi.co` → Task 2 verification: zero text nodes matching `asteroi` on the blocks page.
4. Long headings overflow fixed frames or overlap the footer → Task 4 verification per frame (text bounds inside frame, above footer).
5. Re-running a build creates duplicate pages/frames on top of each other → Task 3 recipe: new page per piece, place each size row below the previous one; Task 4 checks no overlapping top-level frames.

---

### Task 1: Archimoto outline script

**Files:**
- Create: `.claude/skills/figma-post/scripts/archimoto_svg.py`
- Test: `.claude/skills/figma-post/scripts/test_archimoto_svg.py`

**Interfaces:**
- Produces: `text_to_svg(text: str, weight: str = "regular", size: float = 150, color: str = "#B084D3", tracking: float = 0.0) -> tuple[str, float, float]` returning `(svg_markup, width_px, height_px)`. `weight` ∈ {`regular`, `bold`}; fonts at `<repo>/content/scripts/visual/assets/fonts/archimoto-<weight>.otf` (repo root = `Path(__file__).resolve().parents[4]`). `tracking` is in px added after each glyph. Height = ascender − descender scaled. Unknown weight or missing glyph → `ValueError` naming it.
- CLI: `python .claude/skills/figma-post/scripts/archimoto_svg.py "TEXT" --weight bold --size 120 --color "#D3FF4E" [--tracking 0]` prints only the SVG to stdout.

- [ ] **Step 1: Write the failing tests**

```python
from archimoto_svg import text_to_svg
import pytest

def test_returns_svg_with_path_and_colour():
    svg, w, h = text_to_svg("1.", size=150, color="#B084D3")
    assert svg.startswith("<svg") and "<path" in svg and "#B084D3" in svg
    assert w > 0 and h > 0

def test_width_scales_with_size():
    _, w1, _ = text_to_svg("PARA OPTIMIZAR", weight="bold", size=60)
    _, w2, _ = text_to_svg("PARA OPTIMIZAR", weight="bold", size=120)
    assert abs(w2 / w1 - 2) < 0.01

def test_bold_differs_from_regular():
    assert text_to_svg("10", weight="bold")[0] != text_to_svg("10")[0]

def test_spanish_characters():
    svg, w, _ = text_to_svg("¿AÑO ÚNICO?", weight="bold", size=100)
    assert svg.count("<path") >= 1 and w > text_to_svg("ANO UNICO", weight="bold", size=100)[1]

def test_missing_glyph_raises():
    with pytest.raises(ValueError, match="漢"):
        text_to_svg("A漢")

def test_unknown_weight_raises():
    with pytest.raises(ValueError, match="heavy"):
        text_to_svg("A", weight="heavy")
```

- [ ] **Step 2: Run** `python -m pytest .claude/skills/figma-post/scripts -q` → expect FAIL (module missing).
- [ ] **Step 3: Implement** with `TTFont.getGlyphSet()`, `getBestCmap()`, `hmtx` advances, `SVGPathPen`; scale = size / unitsPerEm; flip y (`transform="translate(x, ascender) scale(s, -s)"` per glyph or flip in path); one `<path fill=color>` per glyph is fine; spaces advance without a path.
- [ ] **Step 4: Run** the same pytest command → expect 6 passed. Also run the CLI once and confirm stdout starts with `<svg`.

---

### Task 2: Building blocks page in Figma

**Files:**
- Create: `.claude/skills/figma-post/references/blocks.md` (inventory written from the build's returned IDs)

**Interfaces:**
- Consumes: nothing (Task 1 not needed; numerals inside blocks are placeholders the skill replaces).
- Produces: a page named `🧩 Bloques JCG` with **components** named `<Block>/<size>` where size ∈ `4x5` (1000×1250), `x` (1300×1080), `story` (1080×1920), plus size-free ones. Required blocks: `Background/Stars`, `Asteroid/TopLeft`, `Asteroid/BottomRight`, `Footer/Content`, `Footer/Cover`, `Arrow`, `Sunburst`, `QuoteBox`, `Header/Numbered`, `Button/CTA`, `Card/Image` (placeholder text "Pega aquí la imagen"), `Chart/Bar`, `Info/GroupCard` (variants Lila / Light / Deep), `Info/TitleHighlight`, `Info/FooterBand`, `Pill/Yes`, `Pill/No`. Paint styles `JCG/Lila`, `JCG/Verde`, `JCG/Gris`, `JCG/Negro`, `JCG/Blanco`, `JCG/Lila Light`, `JCG/Lila Deep`. `blocks.md` lists every component: name, node ID, size, what it's for.

- [ ] **Step 1: Inspect** the sample slides named in the spec (and the landscape/story twins) and record each size's grid: margins, footer positions, title/body sizes. Return compact data only (<48KB).
- [ ] **Step 2: Create** the page and paint styles; build the components by **cloning** the real nodes (avatar, wordmark vector, asteroids, star background, arrow, sunburst, quote marks) and re-creating text with the loaded fonts. URL text = `jcgiusto.com`. Lay the page out in labelled rows per size.
- [ ] **Step 3: Verify:** return all component names + IDs; `page.findAll(n => n.type==='TEXT' && /asteroi/i.test(n.characters)).length === 0`; one screenshot of the page next to one original slide per size — they must match visually.
- [ ] **Step 4: Write** `blocks.md` from the returned inventory.

---

### Task 3: The skill

**Files:**
- Create: `.claude/skills/figma-post/SKILL.md`
- Create: `.claude/skills/figma-post/references/style.md` (measured tokens + grids per size from Task 2 Step 1)
- Create: `.claude/skills/figma-post/references/layouts.md` (carousel slide kinds; single-image patterns; infographic hub / decision tree / mind map — positions per size)
- Create: `.claude/skills/figma-post/references/figma-recipes.md` (tested `use_figma` snippets: new page `YYYY-MM-DD · <title>`; instance a block by ID and detach; place an Archimoto outline via `figma.createNodeFromSvg(svg)`; Archivo text with bold ranges via `setRangeFontName`; frame naming `<n>-<kind>`; row placement per size; screenshot QA)
- Copy: the three infographic references into `.claude/skills/figma-post/references/img/` (from the handoff folder named in the spec)
- Modify: `.claude/slash-commands.md` (add a `/figma-post` row; note it writes to Figma only)

**Interfaces:**
- Consumes: `text_to_svg` / CLI (Task 1); block names + IDs in `blocks.md` (Task 2).
- Produces: `SKILL.md` frontmatter `name: figma-post`, description that triggers on "carousel", "infographic", "single image", "placa", "diseño en Figma" for LinkedIn/X. Body = the spec's six steps (input → suggest type → outline for approval → build all three sizes → screenshot QA → link + screenshot), the anti-goals as hard rules, and links to the three references.

- [ ] **Step 1: Write** the four files. `SKILL.md` stays under ~150 lines; detail lives in references.
- [ ] **Step 2: Prove the recipes:** run each snippet in `figma-recipes.md` once against a scratch page in Contenido, then delete the scratch page. Fix any snippet that errors.
- [ ] **Step 3: Cold read:** a fresh subagent reads only `SKILL.md` + references and lists anything it would have to guess to build a 5-slide carousel. Fix the gaps it names.

---

### Task 4: Test one design per type

**Files:** none on disk (output lives in Figma).

**Interfaces:**
- Consumes: the finished skill (Task 3).

- [ ] **Step 1:** A fresh subagent follows `/figma-post` end to end for three real topics from `content/wiki/content-index.md` (one carousel of ~6 slides, one single image, one infographic — pick the infographic layout that fits the topic). It skips the "wait for Juan" checkpoints only for this test and says so.
- [ ] **Step 2: Verify each frame** (script, compact return): every text node's bounds inside its frame and above the footer zone; no text below 32px-equivalent; no `asteroi`; no top-level frames overlapping on the page; all three sizes present for each piece.
- [ ] **Step 3:** Screenshot each set; compare against Juan's original slides for the same size. Fix what's off, re-screenshot once.

---

### Task 5: Close out

- [ ] **Step 1:** Update memory `jcg-os-brand-spec` (Figma uses Big Shoulders Text Regular/Bold; Archimoto can't load in Figma scripting → outline script; footer jcgiusto.com reconfirmed 2026-10-26) and add a memory for the `figma-post` skill + blocks page.
- [ ] **Step 2:** Show Juan the Figma link and screenshots; ask whether to commit (`.claude/skills/figma-post/`, spec, plan, `slash-commands.md`).
