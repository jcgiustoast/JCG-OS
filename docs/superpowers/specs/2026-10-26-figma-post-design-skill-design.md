---
title: Figma post designer skill — design
created: 2026-10-26
updated: 2026-10-26
status: approved by Juan 2026-10-26
---

# Figma post designer skill (`/figma-post`)

## Intent

Juan wants to turn a post (or a topic plus key points) into finished LinkedIn and X visuals **in his own look, inside Figma**, so he only tweaks and exports instead of designing by hand. His past work lives in the Figma file "Contenido" (`U2HIUwTWDYWL7EwSKCDpLd`); new work must look like it belongs next to it.

Three types: **carousel**, **infographic**, **single image**.

Related but separate: the code-first `/visual` engine (`.claude/commands/visual.md`, spec `2026-05-29-visual-carousel-engine-design.md`) renders PNGs from HTML. This skill does not replace or reuse it, except the font files on disk.

## Goals

- Designs that are recognisably Juan's: same fonts, colours, grid, footer, asteroids and starry backgrounds as his Contenido slides.
- Every request starts by **choosing the type**. Claude suggests one; Juan confirms.
- Claude writes the on-image text from Juan's post or points (same language as the input; usually Spanish).
- Output lands in the Contenido file, editable layer by layer, ready for Juan to export.

## Non-goals

- Exporting PNG/PDF or posting. Juan exports from Figma.
- Writing the post caption itself (that is `/content`).
- Video, motion, or story-only pieces.

## Anti-goals (fail even if it "works")

- Generic AI look: gradients, glassy cards, random icon sets, centred-everything sameness.
- Multi-colour palettes like the reference infographics. **Purple + grey only**, green as a small accent.
- Green-heavy or flat-black backgrounds (dark = starry image, never flat black).
- Footer saying asteroi.co. **Always jcgiusto.com.**
- Text too small to read on a phone (body never below 32px on a 1000px-wide frame).

## Decisions Juan made

1. Footer URL is **jcgiusto.com**.
2. Flow: Juan gives a post or topic + points → Claude writes the text → Claude builds it on a new page in Contenido.
3. Type is defined first, every time.
4. Infographics follow his three references (hub, decision tree, mind map — images in `.claude/skills/figma-post/references/img/`, see "References") but in his style.
5. Infographic colours: purple and grey, his style. Groups are told apart by lighter/darker purple, not by new colours.
6. **Every type comes in all three sizes**: 1000×1250 (LinkedIn), 1300×1080 (X), 1080×1920 (story).
7. The building blocks page is approved.

## The style (measured from his slides, 1000×1250 frames)

- **Colours:** Lila `#B084D3`, Verde `#D3FF4E`, Gris `#E7E5E6`, Negro `#000000`, Blanco `#FFFFFF`. Quote box = Lila at 34% opacity, radius 24.
- **Fonts:**
  - Big Shoulders Text Regular/Bold — headlines (cover 130px, slide titles 60px, line height ~101–107%).
  - Archimoto V00 Regular — big numerals (150–250px). Archimoto V00 Bold — uppercase key phrase on covers (120px), in Verde or Lila.
  - Archivo Regular/Bold 35px, line height 133.5% — body, with bold key phrases.
  - URL line: Inter Regular 30px.
- **Content slide grid:** numeral "1." at (55,33) in Lila; title Big Shoulders Bold 60 Lila at (201,94); body from x=55, width 885, starting y≈190. Images sit in white cards, radius 20, soft drop shadow.
- **Footer, content slides:** avatar 114px bottom-left (30,1112) · JCGIUSTO wordmark (vector, 163×26) at (164,1137), Lila on grey / Verde on dark or purple · jcgiusto.com under it · black arrow (96×96) bottom-right on every slide except the last.
- **Footer, covers:** avatar 129px centred, wordmark and URL centred under it, white URL.
- **Dark slides:** star-field image background; asteroid images anchored to opposite corners, bleeding off the edge.
- **Landscape (1300×1080) covers:** add the green sunburst sticker bottom-right.
- Sample slides to copy from (node IDs in Contenido, page "Carousel"): purple cover `1:14295`, numbered slide `1:14330`, dark quote `1:14563`, slide with bar chart `1:14471`, purple call-to-action `1:14448`, dark cover with chart `1:14714` and its landscape twin `1:14594`, call-to-action `1:14130`, closing slides `1:14045` (4:5) and `1:14121` (story). Single-image style on page "JCG": chart `1:3715`, "lo que te cuentan / la realidad" `1:5753`, quote card `1:1318`.

## Types and sizes

| Type | Sizes | Parts |
|---|---|---|
| Carousel | 1000×1250 (LinkedIn), 1300×1080 (X), 1080×1920 (story) — like his file | Cover (dark or purple) · numbered point · insight/quote (dark) · chart · image card · call-to-action (purple or green, green button) · closing ("si te ha gustado…" + reactions) |
| Single image | 1000×1250, 1300×1080, 1080×1920 | One composed slide: headline + one visual (chart, comparison, quote, stat) + footer |
| Infographic | 1000×1250 (taller 1000×1500 when a decision tree needs it), 1300×1080, 1080×1920 — the landscape one is re-laid out side by side, not squeezed | Big title with highlighted line · numbered purple groups · short lines · simple icons · footer band (avatar, JCGIUSTO, jcgiusto.com) |

Infographic layouts: **hub** (centre idea + groups around it), **decision tree** (questions → branches with arrows), **mind map** (title block + branches to lists).

Other sizes: measure the landscape and story grids from his existing twins before building their blocks — landscape `1:15507`, `1:14594`, `1:14602`; story `1:14053`, `1:14068`, `1:14077` (each is the same slide as a 1000×1250 one in the same section).

### Infographic look *(my calls — Juan judges them at the test)*

- Background Gris `#E7E5E6`. Groups are white cards (radius 20) with a Lila header strip; three purple strengths to separate groups: Lila `#B084D3`, light Lila `#D8C1EA`, deep Lila `#7E4FA6`.
- Title: Big Shoulders Text Bold, black, ~110px; the second line sits on a Lila highlighter block (like his "Costo por Resultado" single image). Optional one-line subtitle in Archivo.
- Group numbers: Archimoto Regular in Lila (outlined, see Constraints). Group headings Big Shoulders Bold 44–50px; lines Archivo 32px min.
- Connectors: black 3px lines/arrows; decision-tree "yes/no" pills in Lila / Verde.
- Footer band: full-width Lila bar ~140px tall with avatar, JCGIUSTO in Verde, jcgiusto.com in white.
- Icons: simple shapes drawn in Lila, or his 3D-emoji images already in the file. No new icon library.

### When text doesn't fit *(my call)*

Fitting happens in step 3, not silently in Figma: Claude shortens the wording in the outline Juan approves. If it still won't fit at the readability floor, the infographic may grow to 1000×1500; beyond that Claude proposes a carousel instead.

### Images *(my call)*

Images already in Contenido are reused. Anything new (a screenshot, a product photo) gets a white placeholder card labelled "Pega aquí la imagen" at the right size; Juan drops the image in. If he gives a file on disk, try Figma's asset upload tool first.

## How it works (the skill's steps)

1. Read the input. If it's a topic, ask for the 3–7 key points or offer to draft them.
2. Suggest the type (and infographic layout), one line why. Juan confirms.
3. Write the on-image text as a short outline in chat (slide by slide, or group by group). Juan OKs or edits. *(My call: a cheap checkpoint before any Figma work.)*
4. Build in Contenido on a **new page** named `YYYY-MM-DD · <title>`, one row per size, frames named `<n>-<kind>` so order is obvious.
5. Screenshot each frame; fix overflow, overlaps, clipped text. Respect the readability floor.
6. Give Juan the Figma link and a screenshot of the set.

## Building blocks page *(approved)*

A one-time page in Contenido, "🧩 Bloques JCG", holding reusable components the skill assembles from: footers (light / cover), starry background, asteroids, arrow, sunburst, quote box with marks, number + title header, call-to-action button, image card, chart bars, infographic group box, infographic footer band, and colour styles for the five colours. Juan can restyle a block once and every future design picks it up. The building blocks are made by cloning the real pieces from his existing slides, so they match exactly (including the avatar and asteroid images).

## Constraints

- **Archimoto can't be loaded by Figma's scripting tools** (verified: "font family does not exist"; Big Shoulders, Archivo and Inter load fine). Plan: a small script turns Archimoto text into vector outlines from the font files already in the repo (`content/scripts/visual/assets/fonts/archimoto-*.otf`) and drops them into Figma. Trade-off: those words are shapes, not editable text; Juan retypes them in Figma desktop (where he has the font) if needed. Verified that existing Archimoto text can be outlined in Figma.
- Image creation from bytes isn't supported by the scripting tool, so images (avatar, asteroids, backgrounds) are reused from existing nodes.
- Figma script calls must switch page once and keep returned data small; the "JCG" page is very large.

## Where it lives

Project skill in this repo: `.claude/skills/figma-post/` (`SKILL.md` + style reference + the Archimoto outline script). It depends on this vault's brand and Figma file, so it doesn't belong in the global jcg plugin.

## Left to the builder

Exact component structure and naming, auto-layout details, how the outline script is called, icon approach for infographics (simple shapes in Lila drawn in Figma, or Juan's 3D-emoji images already in the file — no new icon library), and the test topics.

## Done means

- The building blocks page exists and matches his slides side by side.
- `/figma-post` produces one carousel, one single image and one infographic from real topics in the vault, and Juan says they look like his.
- The brand memory is corrected (fonts in Figma, footer URL).

## References

- Infographic references (hub, decision tree, mind map; structure only): `.claude/skills/figma-post/references/img/`.
