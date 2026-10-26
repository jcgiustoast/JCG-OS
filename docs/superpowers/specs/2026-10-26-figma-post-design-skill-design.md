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
- Cramped slides: more than one idea per slide, paragraphs of small text, every gap filled (decision 9).
- Empty slides: a box in the middle and a big empty band under it, or an infographic that stops well above its footer (decision 10).
- Too much purple: purple card headers, a purple hub, a purple footer band (decision 10). Purple is an accent.

## Decisions Juan made

1. Footer URL is **jcgiusto.com**.
2. Flow: Juan gives a post or topic + points → Claude writes the text → Claude builds it on a new page in Contenido.
3. Type is defined first, every time.
4. Infographics follow his three references (hub, decision tree, mind map — images in `.claude/skills/figma-post/references/img/`, see "References") but in his style.
5. Infographic colours: purple and grey, his style. Groups are told apart by lighter/darker purple, not by new colours. *(Revised by decision 10: every group is a white card with a thin Lila edge; the numerals tell them apart, and purple stays an accent.)*
6. **Every type comes in all three sizes**: 1000×1250 (LinkedIn), 1300×1080 (X), 1080×1920 (story).
7. The building blocks page is approved.
8. **2026-10-26 — "Remember to be aligned in terms of design and content before you create the image."** Before any Figma work Claude shows a design + content brief in chat: per slide (or infographic group) one line for the look — slide kind, background (dark / grey / purple), the visual (chart, screenshot placeholder, quote box, big number, none) — and the exact text. Nothing is built until Juan says yes; any change he asks for is shown again before building. Then the LinkedIn 4:5 size is built first and its screenshot shown to him; X and story are built only after his OK, so a design miss is caught once, not three times.
9. **2026-10-26 — "Make sure it's tidy and not all cramped. The ones you created in the past were overly dense."** The first test run put 2–3 paragraphs of 35px text on each point slide and four 3-line cards on the infographic. New rules: one idea per slide; a point slide body ≤ 25 words in ≤ 2 short paragraphs, set at 40px on 4:5 and story (50 on X) — fewer words, bigger type; minimum gaps (title → body 64, paragraphs 40, body → visual 70, 80 clear above the footer on 4:5); a single image is one headline, one visual and at most one short line; infographics prefer 3 groups (max 4), ≤ 2 lines per group, a title of ≤ 5 words, decision trees at most two levels below the question. Whitespace is fine and intended: never pad space with extra words or elements; centre the block instead. The earlier "no more than 35% empty" and "end within 120px of the footer band" rules are withdrawn. Exact numbers live in the skill's `references/style.md` → Density. *(The "whitespace is fine, never fill it" part was revised by decision 10.)*
10. **2026-10-26 — Juan's picks from the variants page** (Figma page "2026-10-26 · Variantes para elegir", three slide and three infographic variants). The airy revision went too far the other way: a text-only point with a box mid-slide and empty space below had *"too many open spaces"*; the infographic with purple strips, a purple hub and a purple footer band was *"too purple"*. He picked:
    - **Point slide = variant A, "text + chart":** numbered header, at most two short paragraphs at Archivo 40, then a visual (chart, picture card or big number) that fills the lower half down to 80 above the footer. A text-only point is the exception and must still fill (bigger body, the highlight box closing the slide at the bottom).
    - **Infographic = variant B, "green title highlight",** with one fix he expected: B left an empty strip above the footer, so the cards must fill the space between the title and the footer in a balanced way (cards grow within the budgets, rows spread). The rebuilt version, "Infografía B (arreglada)", sits on the same page.
    - New rules that follow: purple is an accent (grey, white and black carry most of the area; no full purple bands, no purple-filled card headers on infographics; the audit flags more than 20% purple-filled area on a grey frame); no empty strip above the footer wider than 130 px on 4:5 and story, 120 on X (the audit checks it).
11. **2026-10-26 — "Keep doing this, I feel it's very useful so you understand my taste."** Every run, after the brief is approved and before the full build, Claude builds 2–3 visibly different variants of one representative slide at LinkedIn size, shows them side by side labelled A/B/C and asks Juan to pick. His picks and rejections, with his reasons in his words, are logged in the skill's `references/taste.md`, which Claude reads before proposing variants. The step is skipped only when the log already covers that exact kind of slide and Juan says to go straight to building.

## The style (measured from his slides, 1000×1250 frames)

- **Colours:** Lila `#B084D3`, Verde `#D3FF4E`, Gris `#E7E5E6`, Negro `#000000`, Blanco `#FFFFFF`. Quote box = Lila at 34% opacity, radius 24.
- **Fonts:**
  - Big Shoulders Text Regular/Bold — headlines (cover 130px, slide titles 60px, line height ~101–107%).
  - Archimoto V00 Regular — big numerals (150–250px). Archimoto V00 Bold — uppercase key phrase on covers (120px), in Verde or Lila.
  - Archivo Regular/Bold 35px, line height 133.5% — body, with bold key phrases (his slides; new slides use 40px with fewer words — decision 9).
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
| Infographic | 1000×1250 (taller 1000×1500 when a decision tree needs it), 1300×1080, 1080×1920 — the landscape one is re-laid out side by side, not squeezed | Big black title with its second line on a Verde highlight · numbered white cards with a thin Lila top edge · short lines · white hub with a Lila outline · his normal avatar footer (decision 10) |

Infographic layouts: **hub** (centre idea + groups around it), **decision tree** (questions → branches with arrows), **mind map** (title block + branches to lists).

Other sizes: measure the landscape and story grids from his existing twins before building their blocks — landscape `1:15507`, `1:14594`, `1:14602`; story `1:14053`, `1:14068`, `1:14077` (each is the same slide as a 1000×1250 one in the same section).

### Infographic look *(Juan's pick, 2026-10-26 — variant B with the bottom gap fixed; decision 10)*

- Background Gris `#E7E5E6`. Groups are white cards (radius 20, soft shadow) with a thin (8px) Lila top edge and a **black** Big Shoulders Bold heading (50px). No purple header strips, no group tones: every card is white.
- Group numbers: Archimoto Regular in Lila (outlined, see Constraints), beside the heading. Lines Archivo 36px on 4:5 (40 on landscape, 38 on story).
- Title: Big Shoulders Text Bold 110px, black; the second line sits on a **Verde** highlight block. Optional one-line subtitle in Archivo (4:5 only).
- Hub: a white circle with a Lila outline and black text.
- Connectors: black 3px lines/arrows; decision-tree "yes/no" pills in Verde / Lila.
- Footer: his normal avatar footer bottom-left (avatar, JCGIUSTO, jcgiusto.com), as on his grey slides. **No purple footer band.**
- The block of cards fills the space between the title and the footer: first row ~70px under the title, last card 80px above the footer.
- Purple is an accent: grey, white and black carry most of the area.
- Icons: none by default; his 3D-emoji images already in the file only if he asks. No new icon library.
- *Superseded (my first call, rejected as "too purple"):* white cards with a Lila / light-Lila / deep-Lila header strip, a Lila highlighter on the title, a Lila hub and a full-width Lila footer band.

### When text doesn't fit *(my call, tightened by decision 9)*

Fitting happens in step 3, not silently in Figma: Claude cuts the wording in the design + content brief Juan approves, or splits a point into two slides. Type is never shrunk to make words fit, and empty space is never filled. If an infographic still won't fit its budget, a decision tree may grow to 1000×1500; beyond that Claude proposes a carousel instead.

### Images *(my call)*

Images already in Contenido are reused. Anything new (a screenshot, a product photo) gets a white placeholder card labelled "Pega aquí la imagen" at the right size; Juan drops the image in. If he gives a file on disk, try Figma's asset upload tool first.

## How it works (the skill's steps)

1. Read the input. If it's a topic, ask for the 3–7 key points or offer to draft them.
2. Suggest the type (and infographic layout), one line why. Juan confirms.
3. Show the design + content brief in chat (decision 8): per slide or group, the look in one line and the exact text, within the density budgets (decision 9). Nothing is built until Juan says yes; changes are shown again first.
4. Build 2–3 variants of one representative slide at LinkedIn size on the piece's new page, show them side by side labelled A/B/C, and let Juan pick; log the pick in `taste.md` (decision 11).
5. Build in Contenido on that **new page** named `YYYY-MM-DD · <title>`, frames named `<n>-<kind>` so order is obvious — **the LinkedIn row first**, in the picked direction. Check it, show Juan its screenshot, and build the X and story rows only after his OK.
6. Screenshot each frame; fix overflow, overlaps, clipped text, anything cramped and any empty band. Respect the readability floor, the density rules and purple as an accent (the QA audit checks them).
7. Give Juan the Figma link and a screenshot of the set.

## Building blocks page *(approved)*

A one-time page in Contenido, "🧩 Bloques JCG", holding reusable components the skill assembles from: footers (light / cover), starry background, asteroids, arrow, sunburst, quote box with marks, number + title header, call-to-action button, image card, chart bars, infographic group box, infographic footer band, and colour styles for the five colours. Juan can restyle a block once and every future design picks it up. The building blocks are made by cloning the real pieces from his existing slides, so they match exactly (including the avatar and asteroid images). On 2026-10-26 three blocks for the picked infographic look were added beside the old ones (white group card with a Lila top edge, Verde title highlight, white hub with a Lila outline); the purple-strip group card and the purple footer band stay on the page but are marked "old look, don't use for new pieces".

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
