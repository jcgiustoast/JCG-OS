# Style — Juan's look, measured

updated: 2026-10-26

Measured from his slides on page "Carousel" in Contenido (`U2HIUwTWDYWL7EwSKCDpLd`) and single images on page "JCG". Per-block positions and the raw measurements live in `blocks.md` ("Measured grids"); slide-by-slide positions in `layouts.md`. This file is the rulebook.

## Colours

| Name | Hex | Paint style | Where it goes |
|---|---|---|---|
| Lila | `#B084D3` | JCG/Lila | Purple slide backgrounds (covers, CTA, closing), 4x5/story slide titles, numerals, bars, quote and statement boxes (34% opacity), highlight box (46%), infographic strips and title highlighter. |
| Gris | `#E7E5E6` | JCG/Gris | Background of every content slide, single image and infographic. |
| Negro | `#000000` | JCG/Negro | Body text, X slide titles, arrow, chart label pills, connectors. |
| Blanco | `#FFFFFF` | JCG/Blanco | Text on dark and purple slides, image cards, infographic cards, URL on dark/purple. |
| Verde | `#D3FF4E` | JCG/Verde | **Small accents only:** wordmark on dark/purple, CTA button, Archimoto phrase on purple covers, arrow on purple covers, sunburst, chart guide lines, "SÍ" pill, one highlighter line at most. |
| Lila Light | `#D8C1EA` | JCG/Lila Light | Infographics (second group tone) and the chart's gain segment. Nowhere else. |
| Lila Deep | `#7E4FA6` | JCG/Lila Deep | Infographics (third group tone). Nowhere else. |

Apply colours with `setFillStyleIdAsync(<style id>)` / `setStrokeStyleIdAsync` (IDs in `figma-recipes.md` header), never raw hex. That includes the Archimoto outlines: the recipe helpers link their glyphs to the matching style. A lighter look (boxes) comes from layer opacity, which keeps the style link. The QA audit fails any paint outside the 7 colours, any gradient and any unlinked solid paint.

**Backgrounds:** Gris (content), Lila (covers, CTA, closing), or the star-field image (dark covers, insight slides). Never flat black, never white slides, never a Verde background, never gradients.

## Fonts (exact Figma names)

| Font | Styles | Role |
|---|---|---|
| Big Shoulders Text | Regular, Bold | Headlines, slide titles, quotes, chart values/labels, infographic headings. Mix Regular and Bold inside one headline for emphasis. |
| Big Shoulders Display | Bold | Only two places: the CTA button label (inside `Button/CTA`) and the text in a highlight box (as on his X slides, see `blocks.md` → Measured grids). Nowhere else. |
| Archivo | Regular, Bold | Body text and infographic lines. Bold marks 1–2 key phrases per paragraph. |
| Inter | Regular | Only the `jcgiusto.com` line inside footer blocks. |
| Archimoto V00 | Regular, Bold | Numerals and cover key phrases. **Scripts can't load it** → vector outlines from `scripts/archimoto_svg.py` (see `figma-recipes.md` §5). |

No other fonts. Letter spacing 0. Text case as typed (CTA labels and chart labels typed in capitals).

## Type sizes

| Role | 4x5 · 1000×1250 | X · 1300×1080 | Story · 1080×1920 |
|---|---|---|---|
| Cover headline | BS Text 130 (101–107%), Regular with key words Bold; 100 when the cover has a picture | BS Text 120 (with or without a picture) | BS Text 130; 100 when the cover has a picture |
| Cover Archimoto phrase | Bold 120 (numeral Regular 250) | Bold 120 | Bold 120 |
| Slide title (numbered) | BS Text Bold 60, Lila | BS Text Bold 90, **black** | BS Text Bold 60, Lila |
| Header numeral | Archimoto Regular 150, Lila | Archimoto **Bold** 150, Lila | Archimoto Regular 150, Lila |
| Insight title / quote | BS Bold 130 / BS Bold 60 white | BS Bold 130 / BS Bold **70** white | BS Bold 130 / BS Bold 60 white |
| CTA / closing text | BS Text 80 white | BS Text 100–120 white | BS Text 80 white |
| Body (`punto`, `grafico`, `insight`; with or without a picture) | **Archivo 40**, 133.5%, paragraph gap 40 | **Archivo 50**, 133.5%, paragraph gap 50 | **Archivo 40**, 133.5%, paragraph gap 40 |
| Highlight box text | BS Display Bold 60 black | BS Display Bold 70 black | BS Display Bold 60 black |
| Infographic title | BS Bold 110, two lines (block) | BS Bold 90, one highlighted line | BS Bold 110, two lines |
| Infographic subtitle (only if essential, 4x5 only) | Archivo 36 (block) | hidden | hidden |
| Infographic heading / line | BS Bold 46 / Archivo 32 | BS Bold 50 / Archivo 40 | BS Bold 46 / Archivo 35 |
| Footer URL | Inter 30 (in block) | Inter 30 (in block) | Inter 30 (in block) |

## Readability floor (hard rule)

- **Body (Archivo): at least 32 on 4x5, 35 on story, 40 on X.** 4x5 is the spec's 32px on a 1000-wide frame; story scales it to 1080; X uses 40 because that is what his X slides use (controller ruling 2026-10-26).
- **Nothing below 32px anywhere,** except the Inter 30 URL inside his footer blocks.
- Slide bodies sit well above the floor (40 / 50 / 40, table above). Text that doesn't fit is cut in the brief or moved to another slide, never shrunk (see "Density" below).

## Density — tidy, not cramped (Juan, 2026-10-26)

Juan: *"make sure it's tidy and not all cramped. The ones you created in the past were overly dense."* The first test run put 2–3 paragraphs of 35 px text on each point and four 3-line cards on the infographic. These limits replace that.

- **One idea per slide.** A second idea is a second slide, or it is cut.
- **Fewer words, bigger type.** Cut words before anything else; never shrink type to make words fit.
- **Whitespace is fine and intended.** Never fill empty room with extra words or elements. Balance the page instead: centre the visual (or the whole block) in the room it has.

**Word budgets** (the same words go on all three sizes; `layouts.md` has the per-kind table):

| Piece | Limit |
|---|---|
| `punto` body | ≤ 25 words, at most 2 short paragraphs |
| `grafico` body | ≤ 20 words, one paragraph (X: one line, ≤ 45 characters) |
| `insight` body (optional) | ≤ 20 words, one paragraph; X drops it |
| Highlight box / statement box | one line ≤ 6 words / two lines ≤ 12 words |
| Single image (`placa`) | one headline (≤ 28 characters) + one visual + at most one short supporting line (≤ 12 words) |
| Infographic | 3 groups preferred, 4 at most · ≤ 2 lines per group (≤ 16 characters each) · heading ≤ 11 characters · title ≤ 5 words · subtitle only if essential · decision tree: a question + two answers, at most one more level (two outcomes) |

**Minimum gaps** (measured from the text box or card edge; chosen against his slides, where the body sits ~30 px under the title and the picture ends ~270 px above the footer):

| Gap | 4x5 | X | Story |
|---|---|---|---|
| Slide title text → body | 64 (body at y 230) | 66 (body at y 250) | 64 (body at y 560) |
| Paragraph → paragraph | 40 | 50 | 40 |
| Body → visual (picture, chart, box) | 70 | 60 | 70 |
| Last element → footer | 80 (content ends ≤ 1032) | 60 to the frame bottom (≤ 1020; single image: 60 above its footer, ≤ 882) | 80 (≤ 1362) |
| Infographic: title → first card · last card → band | 60 · 60 | 60 · 60 | 60 · 60 |
| Infographic: card ↔ card · card ↔ hub circle · pill ↔ card | 60 · 40 · 12 | same | same |

The QA audit (`figma-recipes.md` §9) checks the budgets, the gaps and the body sizes.

## Grid per size

| | 4x5 · 1000×1250 | X · 1300×1080 | Story · 1080×1920 |
|---|---|---|---|
| Left text edge / width | x 55–60, w 885 | x 67, w 1173 (centred text: x 54, w 1192) | x 112, w 885 |
| Top of content | header at y 33; body from y 230 | header at y 48; body from y 250 | header at y 363; body from y 560 |
| **Content must end above** | y 1032 (content slides and single image: 80 above the footer) / 960 (cover footer slides) | y 1020 (carousel) / 882 (single image, 60 above its footer) | y 1362 (content: 80 above the footer) / 1240 (cover footer slides) |
| Footer | content 30,1112 · cover 400,996 | **none on carousel slides**; single image/infographic only | content 82,1442 · cover 440,1268 |
| Arrow (grey slides + purple cover) | Negro 849,1121 on grey · Verde 862,61 on purple covers · none on dark, CTA, closing | none | Negro 901,1451 · Verde 929,380 on purple covers |
| Safe zone | whole frame | whole frame | keep text, pictures, charts and cards between y 250 and 1580 (phone story bars). Footers and arrows sit at his measured story positions and end by y 1600 at the latest (the CTA and closing footer at 415,1383 is the lowest); the infographic footer band goes at y 1440 (ends 1580), not lower |

Story rule of thumb: the story is the 4x5 slide dropped into the middle — left-aligned content +52 across, centred content re-centred in 1080, everything about +330 down; footers, arrows and asteroids use the story positions in `blocks.md`.

## Shapes and effects

- Image card: white, radius 20, shadow 4,4 blur 16 at 25% black (the `Card/Image` block).
- Quote box: Lila at 34%, radius 24, Lila quote marks top-left and bottom-right (`QuoteBox` block).
- Statement box (a sentence above a picture, e.g. his "Las plataformas no pueden distinguir…" slide in all three sizes): Lila at 34%, radius 24, **no stroke** — same look as the quote box without marks. Used by the `imagen` kind.
- Highlight box (one key line or number, see `blocks.md` → Measured grids): Lila at 46% + 1px Lila stroke, radius 20, text **Big Shoulders Display Bold black, centred** (70 on X as measured; 60 on 4x5 and story). Measured on three of his X slides. It is the one visual of a text-only `punto`, centred in the room under the body (`layouts.md` → text-only point; recipe `highlightBox`). Build it as one rectangle with fill and stroke linked to JCG/Lila and layer opacity 0.46.
- CTA button: Verde pill (`Button/CTA`).
- Reactions strip on closing slides: his image, radius 40.
- Asteroids: whole pictures bleeding off opposite corners; the slide frame crops them (`clipsContent` on).
- Infographic connectors: black 3px, right angles (hub spokes are short straight diagonals), arrowhead where the direction matters.
- Icons: none by default — the numbered badges carry the groups. Only if Juan asks, reuse his 3D-emoji images already in the file (by image hash); no icon library, no drawn icons.

## Footer

Always **jcgiusto.com**. Never asteroi.co (his old slides say it; new work must not). Wordmark Lila on grey, Verde on dark or purple — always, even where one of his old dark slides used Lila; URL black on grey, white on dark or purple (`figma-recipes.md` §4).

## Words on the image

- Same language as Juan's input (usually Spanish). Talk to the reader as "tú" like his slides ("¿Quieres saber si…?", "tu cuenta").
- **Money stays in the currency of his source.** A post or article in $ stays in $; one in € stays in €. Never convert silently; if a mix seems odd, ask him. Spanish digits either way: dot for thousands, comma for decimals (`€60.000`, `$60.000`, `$10K`, `1,5x`).
- Big text (60 px and up) gets its line breaks written in the brief, so no word ends up alone on the last line (`layouts.md` → Big text).
- Short. A slide carries one idea, within the budgets under "Density". Titles in title case like his ("Audiencias Amplias"), ≤ 28 characters on 4x5/story.
- Bold one key phrase per paragraph, two at most (write them as `**…**` in the brief).
- Cover: a hook in two to four short lines; the Archimoto phrase is the punchline (2–3 words).
- Keep his voice: direct, practical, first person ("Te aseguro que…"). Don't invent numbers; take them from his post.
