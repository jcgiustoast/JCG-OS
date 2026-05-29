# HANDOFF — Visual Carousel & Infographic Engine

**For the next chat.** This brainstorm designed a code-first engine to turn Juan's content into on-brand LinkedIn/Instagram carousels, infographics, and single images. We validated the *visual direction* exhaustively against Juan's real hand-made carousel. We did **not** start implementation.

## Read these first
1. `../2026-05-29-visual-carousel-engine-design.md` — the full design + verified brand spec.
2. Open **`slide-library-v4.html`** in any browser — self-contained mockup of all 13 slide types (fonts + images inlined; no server needed).
3. `RENDER-verified-v4d.png` — screenshot of that mockup.
4. `reference/` — Juan's ACTUAL carousel pages rendered from his PDF, for side-by-side comparison:
   - `contact-sheet-1/2.png` (whole carousel), `page-12.png` (quote), `page-13.png` (section break)
   - `font-match.png` — proof his headline font is **Big Shoulders Black**, not Archivo Black
   - `cover-headline.png`, `weight-compare.png` — Archimoto weight evidence (Medium, not Heavy)

## State of play
- ✅ Method chosen: HTML/CSS templates → Playwright → PNG/PDF (not Gamma).
- ✅ Model chosen: slide-library (author typed slides), 3 modes (carousel/single/infographic), Lean scope.
- ✅ Brand spec pinned & verified: palette, 3-font system with **correct roles**, two-tone wordmark, space-photo dark slides, corner asteroids, grain, footer variants, 13 slide types.
- ✅ Footer URL = `jcgiusto.com` (not asteroi.co).
- ⏳ NOT done: final visual sign-off, locking the spec, the implementation plan, any real code.

## Hard-won corrections (do not regress)
- **Headlines = Big Shoulders Text Black** (condensed). Archivo Black was wrong — too wide, looked "robotic".
- **Archimoto = Medium (500)**, not Heavy. Heavy is too thick; Juan's is airy/open-cut.
- **Dark slides use a desaturated space photo bg**, never flat black.
- **Asteroids are corner-anchored and bleed off-canvas**, asymmetric — never centered/decorative-only.
- Production rendering needs **no base64 inlining** — that was only to defeat the brainstorm preview server (which 404s static assets and serves the newest HTML at the root URL `/`).

## How to rebuild the mockup
`tooling/build_selfcontained.py` reads `slide-library-v4-src.html` (editable source, references `./assets/...`) and inlines fonts+images → `slide-library-v4.html`. Paths in the script point at the old brainstorm session dir — repoint `SESSION/CONTENT/ASSETS` to this folder (`assets/` is here) before rerunning. `tooling/render_pdf.py` + `font_match.py` regenerate the `reference/` crops from Juan's PDF (`C:\Users\jcgiu\Downloads\1766137890132.pdf`).

## Next action
Review v4 → confirm/tweak → **invoke `superpowers:writing-plans`** to produce the implementation plan → build on a git worktree.
