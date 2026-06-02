# Visual Engine — Core (Track A) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author a `piece.md` and render on-brand 1080×1350 PNG carousels/singles/infographics (and a bundled PDF) from HTML/CSS templates via headless Chromium.

**Architecture:** Python orchestrator parses `piece.md` (YAML frontmatter + typed slide blocks) → renders one self-contained HTML page (Jinja2) whose CSS is **ported verbatim from the validated mockup** `slide-library-v4-src.html` → Playwright loads it and screenshots each `.slide` element at `deviceScaleFactor=3.6` so the 300×375 CSS card exports at exactly **1080×1350** px. PNGs are bundled into a PDF with Pillow.

**Tech Stack:** Python 3.11+, Jinja2, Playwright (Chromium), Pillow, pytest.

**Source of truth:** The brand CSS + per-type markup are already validated in `docs/superpowers/specs/2026-05-29-visual-carousel-engine/slide-library-v4-src.html` (the "mockup"). This plan ports it into reusable templates — it does not redesign it. Spec: `docs/superpowers/specs/2026-05-29-visual-carousel-engine-design.md`.

**Out of scope (later plans):** Layout-QA stage (collision detect → auto-fix → pause-ask) = Plan 2. KIE generative fallback (Track B) = Plan 3. Aspect ratios other than 4:5. Auto-scaffold from a LinkedIn post.

---

## File Structure

```
content/scripts/visual/
  __init__.py
  piece.py            # parse piece.md -> Piece(meta, [Slide]); structured-field helpers
  render.py           # Piece -> HTML (Jinja2) -> Playwright PNGs -> PDF
  cli.py              # argparse entrypoint: new / render / pdf
  templates/
    base.html.j2      # full HTML doc: <head> theme.css + loop rendering each slide partial
    _footer.html.j2   # footer macro (avatar + wordmark + url + optional arrow)
    theme.css         # brand tokens + .slide + per-type CSS, ported from the mockup
    slides/
      cover.html.j2 hook-stat.html.j2 data-chart.html.j2 concept-explainer.html.j2
      section-break.html.j2 narrative.html.j2 pull-quote.html.j2 numbered-part.html.j2
      screenshot.html.j2 infographic-framework.html.j2 infographic-checklist.html.j2
      closing-cta.html.j2
  assets/             # fonts/ asteroids/ avatar.png noise.jpg  (copied from the mockup's assets)
content/raw/visuals/<slug>/
  piece.md            # source
  out/                # image-01.png … image-NN.png  +  bundle.pdf
tests/visual/
  test_piece.py
  test_render.py
  fixtures/aov.md     # full sample carousel used by the e2e test
.claude/commands/visual.md   # /visual slash command doc
```

**Responsibilities:** `piece.py` = parsing only (no rendering). `render.py` = templating + browser + PDF (no parsing logic). `cli.py` = arg handling + wiring. Templates = presentation only. This keeps each file single-purpose.

---

## Task 1: Scaffold project + dependencies

**Files:**
- Create: `content/scripts/visual/__init__.py` (empty)
- Create: `content/scripts/visual/requirements.txt`
- Create: `tests/visual/__init__.py` (empty)

- [ ] **Step 1: Create directories and empty package files**

```bash
mkdir -p content/scripts/visual/templates/slides content/scripts/visual/assets tests/visual/fixtures
printf '' > content/scripts/visual/__init__.py
printf '' > tests/visual/__init__.py
```

- [ ] **Step 2: Write requirements.txt**

Create `content/scripts/visual/requirements.txt`:

```
jinja2>=3.1
playwright>=1.44
pillow>=10.0
pytest>=8.0
```

- [ ] **Step 3: Install dependencies + Chromium**

Run:
```bash
python -m pip install -r content/scripts/visual/requirements.txt
python -m playwright install chromium
```
Expected: `pip` completes; `playwright install` prints "Chromium ... downloaded" (or "is already installed").

- [ ] **Step 4: Verify pytest runs (collects nothing yet)**

Run: `python -m pytest tests/visual -q`
Expected: `no tests ran` (exit 5) — confirms the test dir is discoverable.

- [ ] **Step 5: Commit**

```bash
git add content/scripts/visual tests/visual
git commit -m "chore(visual): scaffold core engine package + deps"
```

---

## Task 2: Copy validated brand assets into the engine

**Files:**
- Create: `content/scripts/visual/assets/fonts/*` `asteroid-{1,2,3}.png` `avatar.png` `noise.jpg`

The mockup's assets are the canonical files. Copy the subset the templates reference (fonts, asteroids, avatar, grain). `space-1.jpg` is intentionally **not** copied — the cover/quote/infographic backgrounds use a CSS starfield (`--stars`), not the asteroid photo.

- [ ] **Step 1: Copy assets**

```bash
SRC="docs/superpowers/specs/2026-05-29-visual-carousel-engine/assets"
DST="content/scripts/visual/assets"
mkdir -p "$DST/fonts"
cp "$SRC/fonts/"*.otf "$SRC/fonts/"*.ttf "$DST/fonts/"
cp "$SRC/asteroid-1.png" "$SRC/asteroid-2.png" "$SRC/asteroid-3.png" "$SRC/noise.jpg" "$SRC/avatar.png" "$DST/"
```

- [ ] **Step 2: Verify the avatar and a font landed**

Run: `ls content/scripts/visual/assets content/scripts/visual/assets/fonts`
Expected: lists `avatar.png`, `noise.jpg`, `asteroid-1..3.png`, and `bigshoulders-black.ttf`, `archimoto-medium.otf`, `archimoto-bold.otf`, `archivo-regular.ttf` among the fonts.

- [ ] **Step 3: Commit**

```bash
git add content/scripts/visual/assets
git commit -m "chore(visual): copy brand fonts + asteroid/avatar/grain assets"
```

---

## Task 3: Parse frontmatter (`piece.py`)

**Files:**
- Create: `content/scripts/visual/piece.py`
- Test: `tests/visual/test_piece.py`

- [ ] **Step 1: Write the failing test**

Create `tests/visual/test_piece.py`:

```python
from content.scripts.visual.piece import parse_frontmatter

def test_parse_frontmatter_reads_keys_and_returns_body():
    text = "---\ntitle: El secreto del AOV\nmode: carousel\naspect: 4:5\n---\n# slide:cover\ntitle: Hola\n"
    meta, body = parse_frontmatter(text)
    assert meta == {"title": "El secreto del AOV", "mode": "carousel", "aspect": "4:5"}
    assert body.startswith("# slide:cover")

def test_parse_frontmatter_requires_block():
    import pytest
    with pytest.raises(ValueError):
        parse_frontmatter("no frontmatter here")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/visual/test_piece.py -q`
Expected: FAIL — `ModuleNotFoundError: ... piece`.

- [ ] **Step 3: Write minimal implementation**

Create `content/scripts/visual/piece.py`:

```python
import re

_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def parse_frontmatter(text):
    """Return (meta_dict, body_after_frontmatter). Raises ValueError if absent."""
    m = _FRONTMATTER.match(text)
    if not m:
        raise ValueError("piece.md must start with a YAML frontmatter block (--- ... ---)")
    meta = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip()
    return meta, text[m.end():]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/visual/test_piece.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add content/scripts/visual/piece.py tests/visual/test_piece.py
git commit -m "feat(visual): parse piece.md frontmatter"
```

---

## Task 4: Parse typed slide blocks (`piece.py`)

A slide block opens with `# slide:<type>` and is followed by `key: value` lines until the next block. **Repeated keys collapse into a list** (e.g. three `card:` lines → `fields["card"] == [".", ".", "."]`). Single keys stay strings. Values keep their raw string (templates/helpers split structured ones).

**Files:**
- Modify: `content/scripts/visual/piece.py`
- Test: `tests/visual/test_piece.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/visual/test_piece.py`:

```python
from content.scripts.visual.piece import parse_piece, Slide, Piece

def test_parse_piece_builds_typed_slides_with_repeated_keys():
    text = (
        "---\ntitle: T\nmode: carousel\n---\n"
        "# slide:cover\n"
        "headline: El Secreto del AOV\n"
        "subtitle: Que no conocías\n"
        "# slide:infographic-framework\n"
        "title: Las 3 Herramientas\n"
        "card: 01 | Media | tres lentes\n"
        "card: 02 | Histogramas | agrupa\n"
    )
    piece = parse_piece(text)
    assert isinstance(piece, Piece)
    assert piece.meta["mode"] == "carousel"
    assert [s.type for s in piece.slides] == ["cover", "infographic-framework"]
    assert piece.slides[0].fields["subtitle"] == "Que no conocías"
    assert piece.slides[1].fields["card"] == ["01 | Media | tres lentes", "02 | Histogramas | agrupa"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/visual/test_piece.py::test_parse_piece_builds_typed_slides_with_repeated_keys -q`
Expected: FAIL — `ImportError: cannot import name 'parse_piece'`.

- [ ] **Step 3: Write minimal implementation**

Append to `content/scripts/visual/piece.py`:

```python
from dataclasses import dataclass, field

@dataclass
class Slide:
    type: str
    fields: dict = field(default_factory=dict)

@dataclass
class Piece:
    meta: dict
    slides: list

_SLIDE_HEADER = re.compile(r"^#\s*slide:([a-z0-9-]+)\s*$", re.IGNORECASE)

def _add(fields, key, val):
    if key in fields:
        if not isinstance(fields[key], list):
            fields[key] = [fields[key]]
        fields[key].append(val)
    else:
        fields[key] = val

def parse_piece(text):
    meta, body = parse_frontmatter(text)
    slides, current = [], None
    for raw in body.splitlines():
        header = _SLIDE_HEADER.match(raw.strip())
        if header:
            current = Slide(type=header.group(1).lower())
            slides.append(current)
            continue
        if current is None:
            continue
        line = raw.strip()
        if not line:
            continue
        key, sep, val = line.partition(":")
        if not sep:
            continue
        _add(current.fields, key.strip(), val.strip())
    return Piece(meta=meta, slides=slides)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/visual/test_piece.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Add structured-field helpers + test**

Append to `tests/visual/test_piece.py`:

```python
from content.scripts.visual.piece import parse_bars, parse_pipes

def test_parse_bars_marks_highlight_with_star():
    bars = parse_bars("€10:34, €30:100*, €70:9")
    assert bars == [
        {"label": "€10", "height": 34, "hi": False},
        {"label": "€30", "height": 100, "hi": True},
        {"label": "€70", "height": 9, "hi": False},
    ]

def test_parse_pipes_splits_and_strips():
    assert parse_pipes("01 | Media | tres lentes") == ["01", "Media", "tres lentes"]
```

Append to `content/scripts/visual/piece.py`:

```python
def parse_pipes(value):
    """'a | b | c' -> ['a','b','c'] (stripped)."""
    return [p.strip() for p in value.split("|")]

def parse_bars(value):
    """'€10:34, €30:100*' -> [{label,height,hi}]. Trailing '*' marks the highlighted bar."""
    out = []
    for chunk in value.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        label, _, h = chunk.rpartition(":")
        hi = h.endswith("*")
        out.append({"label": label.strip(), "height": int(h.rstrip("*")), "hi": hi})
    return out
```

- [ ] **Step 6: Run test to verify it passes**

Run: `python -m pytest tests/visual/test_piece.py -q`
Expected: PASS (5 passed).

- [ ] **Step 7: Commit**

```bash
git add content/scripts/visual/piece.py tests/visual/test_piece.py
git commit -m "feat(visual): parse typed slide blocks + structured-field helpers"
```

---

## Task 5: Port the brand CSS into `theme.css`

The mockup's `<style>` block (lines 7–187 of `slide-library-v4-src.html`) is the validated brand layer. Port it verbatim **except** the page-chrome rules that only existed for the preview grid.

**Files:**
- Create: `content/scripts/visual/templates/theme.css`

- [ ] **Step 1: Copy the CSS**

Open `docs/superpowers/specs/2026-05-29-visual-carousel-engine/slide-library-v4-src.html`. Copy the contents **between** `<style>` (line 6) and `</style>` (line 187) into `content/scripts/visual/templates/theme.css`, then **delete** these preview-only selectors (they style the mockup gallery, not the slides):
- `body{...}` (line 26) — replace with `body{margin:0;background:#fff;}`
- `h1`, `.sub`, `.sub code`, `.section-head`, `.grid`, `.wrap`, `.lbl`, `.lbl b`, `.note` (lines 27–35)

Keep everything else unchanged: all `@font-face`, `:root` (incl. `--stars`), `*`, `.slide`, `.slide::after` (grain), `.ft*` (footer), and every per-type block (`.cover`, `.hook`, `.chart`, `.con`, `.brk`, `.nar`, `.quo`, `.num`, `.shot`, `.igf`, `.igc`, `.cta`).

- [ ] **Step 2: Fix the font + asset URLs**

In `theme.css`, the `url('./assets/...')` paths are relative to the HTML file. Rendering writes HTML to `out/`, so assets must resolve from there. Replace every `url('./assets/` with `url('{{ assets }}/` — **no**, CSS can't take Jinja. Instead leave the paths as `url('assets/...')` (drop the leading `./`) and in Task 8 the HTML is written into the slug's `out/` dir with a sibling `assets/` symlink/copy. Concretely: run this in-place replacement on the file:

```bash
python - <<'PY'
import re, pathlib
p = pathlib.Path("content/scripts/visual/templates/theme.css")
p.write_text(p.read_text(encoding="utf-8").replace("url('./assets/", "url('assets/"), encoding="utf-8")
print("rewrote", p)
PY
```

- [ ] **Step 3: Sanity check the file**

Run: `grep -c "@font-face" content/scripts/visual/templates/theme.css`
Expected: `13` (the 13 `@font-face` rules, incl. `archimoto-bold`).

Run: `grep -c "url('assets/" content/scripts/visual/templates/theme.css`
Expected: a non-zero count and **no** remaining `url('./assets/`.

- [ ] **Step 4: Commit**

```bash
git add content/scripts/visual/templates/theme.css
git commit -m "feat(visual): port validated brand CSS into theme.css"
```

---

## Task 6: Base template + footer macro

**Files:**
- Create: `content/scripts/visual/templates/_footer.html.j2`
- Create: `content/scripts/visual/templates/base.html.j2`

- [ ] **Step 1: Write the footer macro**

Create `content/scripts/visual/templates/_footer.html.j2`:

```jinja
{% macro footer(variant="light", arrow=true) %}
<div class="ft {{ variant }}">
  <div class="av"></div>
  <div class="id"><div class="wm"><span class="jc">JC</span>GIUSTO</div><div class="url">jcgiusto.com</div></div>
  {% if arrow and "center" not in variant %}<div class="ar">→</div>{% endif %}
</div>
{% endmacro %}
```

- [ ] **Step 2: Write the base document**

Create `content/scripts/visual/templates/base.html.j2`:

```jinja
<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<style>{{ theme_css | safe }}</style>  {# |safe: theme_css is trusted CSS, must not be HTML-escaped #}
<style>
  body{margin:0;background:#fff;}
  /* one slide per row so each screenshots cleanly */
  .stage{display:flex;flex-direction:column;gap:0;}
</style>
</head><body>
<div class="stage">
{% for slide in slides %}
{% include "slides/" ~ slide.type ~ ".html.j2" %}
{% endfor %}
</div>
</body></html>
```

Note: `theme_css` is injected as a string by `render.py` (Step in Task 8) so the stylesheet is inline and the only external refs are the `url('assets/...')` images/fonts.

- [ ] **Step 3: Commit**

```bash
git add content/scripts/visual/templates/_footer.html.j2 content/scripts/visual/templates/base.html.j2
git commit -m "feat(visual): base template + footer macro"
```

---

## Task 7: Cover slide partial (the porting pattern)

Each partial reproduces the mockup markup for that type, with text swapped for `slide.fields` lookups and the footer from the macro. The cover is the reference pattern; Task 10 ports the other 11 the same way.

**Files:**
- Create: `content/scripts/visual/templates/slides/cover.html.j2`

- [ ] **Step 1: Write the cover partial**

Mockup source: `slide-library-v4-src.html` lines 199–203. Create `content/scripts/visual/templates/slides/cover.html.j2`:

```jinja
{% from "_footer.html.j2" import footer %}
<div class="slide cover">
  <div class="bg"></div><div class="vig"></div><div class="a1"></div><div class="a2"></div>
  <div class="h">{{ slide.fields.headline | replace("\n", "<br>") | safe }}</div>
  {% if slide.fields.subtitle %}<div class="s">{{ slide.fields.subtitle }}</div>{% endif %}
  {% if slide.fields.card_value %}
  <div class="card"><div class="chrome"><i></i><i></i><i></i></div>
    <div class="bd"><div class="t">{{ slide.fields.card_label }}</div>
      <span class="v">{{ slide.fields.card_value }}</span>
      {% if slide.fields.card_delta %}<span class="d">{{ slide.fields.card_delta }}</span>{% endif %}</div></div>
  {% endif %}
  {{ footer("dark center", arrow=false) }}
</div>
```

- [ ] **Step 2: Render-smoke it (test added in Task 9)**

No standalone test here; the cover is exercised by the render test in Task 9 and the e2e in Task 13. Proceed.

- [ ] **Step 3: Commit**

```bash
git add content/scripts/visual/templates/slides/cover.html.j2
git commit -m "feat(visual): cover slide partial"
```

---

## Task 8: `render.py` — Piece → HTML

**Files:**
- Create: `content/scripts/visual/render.py`
- Test: `tests/visual/test_render.py`

- [ ] **Step 1: Write the failing test**

Create `tests/visual/test_render.py`:

```python
from pathlib import Path
from content.scripts.visual.piece import parse_piece
from content.scripts.visual.render import render_html

def test_render_html_includes_slide_markup_and_inline_css(tmp_path):
    piece = parse_piece("---\ntitle: T\nmode: single\n---\n# slide:cover\nheadline: El Secreto\nsubtitle: Que no conocías\n")
    html = render_html(piece)
    assert "<div class=\"slide cover\">" in html
    assert "El Secreto" in html
    assert "Que no conocías" in html
    assert "@font-face" in html          # theme.css inlined
    assert "GIUSTO" in html              # footer macro rendered
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/visual/test_render.py -q`
Expected: FAIL — `ModuleNotFoundError: ... render`.

- [ ] **Step 3: Write minimal implementation**

Create `content/scripts/visual/render.py`:

```python
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

_TPL_DIR = Path(__file__).parent / "templates"

def _env():
    return Environment(
        loader=FileSystemLoader(str(_TPL_DIR)),
        autoescape=select_autoescape(enabled_extensions=("j2",)),
    )

def render_html(piece):
    """Render a Piece into a single self-contained HTML string (CSS inlined)."""
    theme_css = (_TPL_DIR / "theme.css").read_text(encoding="utf-8")
    env = _env()
    return env.get_template("base.html.j2").render(slides=piece.slides, theme_css=theme_css)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/visual/test_render.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add content/scripts/visual/render.py tests/visual/test_render.py
git commit -m "feat(visual): render Piece to inline-CSS HTML"
```

---

## Task 9: `render.py` — HTML → 1080×1350 PNGs via Playwright

The 4:5 slide is 300×375 CSS px in the ported theme. Rendering at `device_scale_factor=3.6` exports each `.slide` element at exactly 1080×1350 px. Assets resolve because we write `index.html` into `out/` and copy `assets/` beside it.

**Files:**
- Modify: `content/scripts/visual/render.py`
- Test: `tests/visual/test_render.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/visual/test_render.py`:

```python
from PIL import Image
from content.scripts.visual.render import render_piece

def test_render_piece_writes_1080x1350_pngs(tmp_path):
    piece = parse_piece(
        "---\ntitle: T\nmode: carousel\n---\n"
        "# slide:cover\nheadline: El Secreto del AOV\nsubtitle: Que no conocías\n"
        "# slide:section-break\neyebrow: Capítulo 02\nheadline: Un Caso Real\n"
    )
    out = render_piece(piece, tmp_path)
    assert [p.name for p in out] == ["image-01.png", "image-02.png"]
    for p in out:
        assert p.exists()
        w, h = Image.open(p).size
        assert (w, h) == (1080, 1350)
```

(Requires `section-break.html.j2`, which lands in Task 10. If running tasks in order, temporarily reduce this test to a single `cover` slide, then restore the two-slide version after Task 10. Note the dependency in the commit.)

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/visual/test_render.py::test_render_piece_writes_1080x1350_pngs -q`
Expected: FAIL — `ImportError: cannot import name 'render_piece'`.

- [ ] **Step 3: Write minimal implementation**

Append to `content/scripts/visual/render.py`:

```python
import shutil
from playwright.sync_api import sync_playwright

ARTBOARD = {"4:5": (300, 375)}       # CSS px; * device_scale_factor 3.6 = 1080x1350
SCALE = 3.6

def render_piece(piece, out_dir):
    """Render every slide to out_dir/image-NN.png at 1080x1350. Returns list of Paths."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    # assets must sit beside the html for url('assets/...') to resolve
    assets_src = _TPL_DIR / "assets"
    assets_dst = out_dir / "assets"
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(assets_src, assets_dst)

    html = render_html(piece)
    (out_dir / "index.html").write_text(html, encoding="utf-8")

    w, h = ARTBOARD.get(piece.meta.get("aspect", "4:5"), (300, 375))
    paths = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_context(device_scale_factor=SCALE).new_page()
        page.goto((out_dir / "index.html").as_uri())
        page.wait_for_timeout(300)  # let webfonts settle
        slides = page.locator(".slide")
        for i in range(slides.count()):
            dst = out_dir / f"image-{i + 1:02d}.png"
            slides.nth(i).screenshot(path=str(dst))
            paths.append(dst)
        browser.close()
    return paths
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/visual/test_render.py::test_render_piece_writes_1080x1350_pngs -q`
Expected: PASS (after Task 10 provides `section-break`; with the temporary single-slide version it passes now).

- [ ] **Step 5: Commit**

```bash
git add content/scripts/visual/render.py tests/visual/test_render.py
git commit -m "feat(visual): screenshot slides to 1080x1350 PNGs via Playwright"
```

---

## Task 10: Port the remaining 11 slide partials

Same pattern as the cover (Task 7): copy the mockup markup, swap text → `slide.fields.*`, swap the footer for the macro. Below is the exact source mapping and the field/footer contract for each. **Write each partial in full** (no shared includes beyond the footer macro).

**Files:** Create one `content/scripts/visual/templates/slides/<type>.html.j2` per row.

| Partial | Mockup lines | Footer call | Fields → markup |
|---|---|---|---|
| `hook-stat` | 208–210 | `footer("light")` | `text` → `.b` (rich, `|safe`); static `.qo/.qc/.gh` |
| `data-chart` | 215–226 | `footer("light")` | `title`→`h2`; `caption`→`.cap`; `tag`→`.tag`; `bars` via the `bars` filter → loop emitting `<div class="bar{{ ' hi' if b.hi else '' }}" style="height:{{ b.height }}%"{% if b.hi %} data-val="{{ b.label }}"{% endif %}><span>{{ b.label }}</span></div>`. **One CSS tweak in theme.css:** change `.chart .bar.hi::after{content:"€30";…}` to `content:attr(data-val)` so the highlighted bar's top €-label is dynamic. |
| `concept-explainer` | 231–234 | `footer("light")` | `title`→`h2` (`replace("\n","<br>")|safe`); static `.ul`; `pill`→`.pill`; `body`→`.b` (`|safe`) |
| `section-break` | 239–241 | `footer("light")` | `eyebrow`→`.ey`; `headline`→`.h`; static `.a1/.a2` |
| `narrative` | 246–248 | `footer("light")` | `body`→`.b` (`|safe`); static `.a` |
| `pull-quote` | 253–257 | `footer("dark center", arrow=false)` | `title`→`.title`; `quote`→`.panel .b`; static `.bg/.vig/.a1/.a2/.qo/.qc` |
| `numbered-part` | 262–264 | `footer("light")` | `number`→`.n` (e.g. "01."); `title`→`h2`; `body`→`.b` (`|safe`) |
| `screenshot` | 269–276 | `footer("light")` | `title`→`h2`; `callout`→`.co`; `.frame` body: if `image` field present, `<img src="assets/{{image}}" style="width:100%;display:block">`, else keep the placeholder chrome+rows from the mockup |
| `infographic-framework` | 284–290 | `footer("dark", arrow=false)` | `title`→`.h`; `card` (list; each via `parse_pipes` → `[n, nm, d]`) → loop `.c`; static `.bg/.vig/.a1/.a` |
| `infographic-checklist` | 295–300 | `footer("light", arrow=false)` | `title`→`h2`; static `.ul`; `section` (list; each `Header | item; item; item` → split `|` then `;`) → loop `.s` with `.h` + `.it` rows each prefixed `<span class="ck">✓</span>`; static `.a` |
| `closing-cta` | 308–312 | inline footer (keep the dark-text override from mockup line 312) | `headline`→`.h`; `instruction`→`.i` (`|safe`); `button`→`.btn` |

- [ ] **Step 1: Write all 11 partials** per the table. Example — `section-break.html.j2`:

```jinja
{% from "_footer.html.j2" import footer %}
<div class="slide brk">
  <div class="a1"></div><div class="a2"></div>
  {% if slide.fields.eyebrow %}<div class="ey">{{ slide.fields.eyebrow }}</div>{% endif %}
  <div class="h">{{ slide.fields.headline }}</div>
  {{ footer("light") }}
</div>
```

Example — `infographic-framework.html.j2` (shows the `card` list + `parse_pipes` usage; the helper is exposed to Jinja as a filter in Step 2):

```jinja
{% from "_footer.html.j2" import footer %}
<div class="slide igf">
  <div class="bg"></div><div class="vig"></div><div class="a1"></div>
  <div class="h">{{ slide.fields.title }}</div>
  <div class="cards">
  {% for c in (slide.fields.card if slide.fields.card is iterable and slide.fields.card is not string else [slide.fields.card]) %}
    {% set parts = c | pipes %}
    <div class="c"><div class="n">{{ parts[0] }}</div><div><div class="nm">{{ parts[1] }}</div><div class="d">{{ parts[2] }}</div></div></div>
  {% endfor %}
  </div>
  <div class="a"></div>
  {{ footer("dark", arrow=false) }}
</div>
```

- [ ] **Step 2: Expose the structured-field helpers to Jinja as filters**

Modify `_env()` in `content/scripts/visual/render.py`:

```python
from content.scripts.visual.piece import parse_pipes, parse_bars

def _env():
    env = Environment(
        loader=FileSystemLoader(str(_TPL_DIR)),
        autoescape=select_autoescape(enabled_extensions=("j2",)),
    )
    env.filters["pipes"] = parse_pipes
    env.filters["bars"] = parse_bars
    return env
```

- [ ] **Step 3: Restore the two-slide render test**

If you reduced `test_render_piece_writes_1080x1350_pngs` to one slide in Task 9, restore the `cover` + `section-break` version now.

- [ ] **Step 4: Run the full suite**

Run: `python -m pytest tests/visual -q`
Expected: PASS (all tests; the two-slide render asserts both PNGs are 1080×1350).

- [ ] **Step 5: Commit**

```bash
git add content/scripts/visual/templates/slides content/scripts/visual/render.py tests/visual/test_render.py
git commit -m "feat(visual): port remaining 11 slide partials + jinja filters"
```

---

## Task 11: Bundle a carousel into a PDF

**Files:**
- Modify: `content/scripts/visual/render.py`
- Test: `tests/visual/test_render.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/visual/test_render.py`:

```python
from content.scripts.visual.render import bundle_pdf

def test_bundle_pdf_combines_pngs(tmp_path):
    piece = parse_piece("---\ntitle: T\nmode: carousel\n---\n# slide:cover\nheadline: A\n# slide:narrative\nbody: B\n")
    pngs = render_piece(piece, tmp_path)
    pdf = bundle_pdf(pngs, tmp_path)
    assert pdf.name == "bundle.pdf"
    assert pdf.exists() and pdf.stat().st_size > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/visual/test_render.py::test_bundle_pdf_combines_pngs -q`
Expected: FAIL — `ImportError: cannot import name 'bundle_pdf'`.

- [ ] **Step 3: Write minimal implementation**

Append to `content/scripts/visual/render.py`:

```python
from PIL import Image

def bundle_pdf(png_paths, out_dir):
    """Combine PNGs (in order) into out_dir/bundle.pdf. Returns the Path."""
    out_dir = Path(out_dir)
    imgs = [Image.open(p).convert("RGB") for p in png_paths]
    pdf = out_dir / "bundle.pdf"
    imgs[0].save(pdf, save_all=True, append_images=imgs[1:])
    return pdf
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/visual/test_render.py::test_bundle_pdf_combines_pngs -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add content/scripts/visual/render.py tests/visual/test_render.py
git commit -m "feat(visual): bundle carousel PNGs into a PDF"
```

---

## Task 12: CLI (`cli.py`) + `/visual` command doc

**Files:**
- Create: `content/scripts/visual/cli.py`
- Create: `.claude/commands/visual.md`

- [ ] **Step 1: Write the CLI**

Create `content/scripts/visual/cli.py`:

```python
import argparse
from pathlib import Path
from content.scripts.visual.piece import parse_piece
from content.scripts.visual.render import render_piece, bundle_pdf

ROOT = Path("content/raw/visuals")

_SCAFFOLD = """---
title: {slug}
mode: carousel
aspect: 4:5
---
# slide:cover
headline: Tu titular
subtitle: Subtítulo corto
"""

def _piece_dir(slug):
    return ROOT / slug

def cmd_new(args):
    d = _piece_dir(args.slug)
    d.mkdir(parents=True, exist_ok=True)
    pm = d / "piece.md"
    if not pm.exists():
        pm.write_text(_SCAFFOLD.format(slug=args.slug), encoding="utf-8")
    print(f"scaffolded {pm}")

def cmd_render(args):
    d = _piece_dir(args.slug)
    piece = parse_piece((d / "piece.md").read_text(encoding="utf-8"))
    pngs = render_piece(piece, d / "out")
    print(f"rendered {len(pngs)} slide(s) -> {d / 'out'}")
    if piece.meta.get("mode") == "carousel":
        print(f"pdf -> {bundle_pdf(pngs, d / 'out')}")

def main(argv=None):
    p = argparse.ArgumentParser(prog="visual")
    sub = p.add_subparsers(required=True)
    n = sub.add_parser("new"); n.add_argument("slug"); n.set_defaults(func=cmd_new)
    r = sub.add_parser("render"); r.add_argument("slug"); r.set_defaults(func=cmd_render)
    args = p.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Manual smoke test**

Run:
```bash
python -m content.scripts.visual.cli new demo
python -m content.scripts.visual.cli render demo
```
Expected: prints `scaffolded …/demo/piece.md`, then `rendered 1 slide(s) -> …/demo/out` and a PNG exists at `content/raw/visuals/demo/out/image-01.png` (1080×1350).

- [ ] **Step 3: Write the slash-command doc**

Create `.claude/commands/visual.md`:

```markdown
---
description: Author + render on-brand carousels/placas (visual engine, Track A)
---
Render Juan's content into on-brand 1080×1350 images.

Usage:
- `python -m content.scripts.visual.cli new <slug>` — scaffold `content/raw/visuals/<slug>/piece.md`
- `python -m content.scripts.visual.cli render <slug>` — render `out/image-NN.png` (+ `bundle.pdf` for carousels)

Slide types: cover, hook-stat, data-chart, concept-explainer, section-break,
narrative, pull-quote, numbered-part, screenshot, infographic-framework,
infographic-checklist, closing-cta. See the spec for each type's fields.
```

- [ ] **Step 4: Commit**

```bash
git add content/scripts/visual/cli.py .claude/commands/visual.md
git commit -m "feat(visual): CLI (new/render) + /visual command doc"
```

---

## Task 13: End-to-end test with the real AOV carousel

**Files:**
- Create: `tests/visual/fixtures/aov.md`
- Test: `tests/visual/test_render.py`

- [ ] **Step 1: Write the fixture**

Create `tests/visual/fixtures/aov.md` — one block per type so the e2e exercises all 12 partials:

```markdown
---
title: El secreto del AOV
mode: carousel
aspect: 4:5
---
# slide:cover
headline: El Secreto\ndel AOV
subtitle: Que no conocías
card_label: Average order value over time
card_value: €60
card_delta: ↗ 10%
# slide:hook-stat
text: El <b>87% de los eCommerce</b> que conozco optimizan su AOV para fantasmas.
# slide:data-chart
title: La trampa del promedio
caption: Distribución real de 1.000 órdenes
bars: €10:34, €20:52, €30:100*, €40:70, €50:40, €60:18, €70:9
tag: ¡Ni una orden de €60!
# slide:concept-explainer
title: El Problema\nOculto del AOV
pill: AOV = Facturación / Núm. Órdenes
body: La fórmula parece básica, ¿verdad? <b>Ahí está el problema.</b>
# slide:section-break
eyebrow: Capítulo 02
headline: Un Caso Real Que Te Va a Impactar
# slide:narrative
body: Regalaste envío gratis a <b>350 personas</b> que iban a comprar igualmente.
# slide:pull-quote
title: Insight Clave
quote: Todo sistema diseñado para el promedio está destinado al fracaso. – Todd Rose
# slide:numbered-part
number: 01.
title: Media, Moda y Mediana
body: <b>Media:</b> el promedio. <b>Moda:</b> el valor más frecuente.
# slide:screenshot
title: Native sube su ticket medio con un popup
callout: Upsell de €10 en el carrito
# slide:infographic-framework
title: Las 3 Herramientas del CMO
card: 01 | Media, Moda y Mediana | Tres lentes para leer tu AOV.
card: 02 | Histogramas | Agrupa pedidos por intervalo.
card: 03 | Segmentos | Demográficos, comportamiento y valor.
# slide:infographic-checklist
title: Checklist Suscripción
section: Adquisición | Quiz de onboarding; Discount-stack; Upsell post-purchase
section: Retención | Skip-month; Pause con incentivo
# slide:closing-cta
headline: ¿Quieres el link?
instruction: Comenta <b>"GPT"</b> abajo y te lo envío.
button: Comenta GPT abajo
```

- [ ] **Step 2: Write the e2e test**

Append to `tests/visual/test_render.py`:

```python
def test_e2e_aov_renders_all_types(tmp_path):
    text = Path("tests/visual/fixtures/aov.md").read_text(encoding="utf-8")
    piece = parse_piece(text)
    assert len(piece.slides) == 12
    pngs = render_piece(piece, tmp_path)
    assert len(pngs) == 12
    for p in pngs:
        assert Image.open(p).size == (1080, 1350)
    pdf = bundle_pdf(pngs, tmp_path)
    assert pdf.exists()
```

- [ ] **Step 3: Run the e2e**

Run: `python -m pytest tests/visual/test_render.py::test_e2e_aov_renders_all_types -q`
Expected: PASS — 12 PNGs at 1080×1350 + a PDF. (This is the proof the engine renders every slide type without crashing.)

- [ ] **Step 4: Eyeball the output**

Run: `python -m content.scripts.visual.cli new aov && cp tests/visual/fixtures/aov.md content/raw/visuals/aov/piece.md && python -m content.scripts.visual.cli render aov`
Open `content/raw/visuals/aov/out/bundle.pdf` and confirm it matches the mockup (`slide-library-v4.html`). Note any visual drift as follow-up; do not block the commit.

- [ ] **Step 5: Commit**

```bash
git add tests/visual/fixtures/aov.md tests/visual/test_render.py
git commit -m "test(visual): e2e renders all 12 slide types from AOV fixture"
```

---

## Done criteria

- `python -m pytest tests/visual -q` passes.
- `python -m content.scripts.visual.cli render aov` produces 12× 1080×1350 PNGs + `bundle.pdf` that visually match the mockup.
- No external network at render time; all fonts/images load from `out/assets/`.

## Follow-ups (next plans)

- **Plan 2 — Layout QA:** geometry collision detection (`elementFromPoint` over glyph rects) → bounded auto-fix ladder (reposition/reflow/scale-to-floor) → pause-and-ask routed to the content agent; the cover-vs-list headline-cap rule.
- **Plan 3 — Track B (KIE):** `illustration: kie` field → generate brandless illustration → brand-grade (grayscale/brightness/grain) → composite as a CSS layer; `layer`/`raw`/`bare` flavors; image cache; API key via env.
- Real **starfield photo** swap for the CSS `--stars` placeholder (Juan to provide the file).
- Aspect ratios `1:1` / `9:16` (add to `ARTBOARD`, add slide-size CSS variants).
