# Style — Juan's look, measured

updated: 2026-11-10

Measured from his slides on page "Carousel" in Contenido (`U2HIUwTWDYWL7EwSKCDpLd`) and single images on page "JCG". Per-block positions and the raw measurements live in `blocks.md` ("Measured grids"); slide-by-slide positions in `layouts.md`. This file is the rulebook.

## Colours

| Name | Hex | Paint style | Where it goes |
|---|---|---|---|
| Lila | `#B084D3` | JCG/Lila | Purple slide backgrounds (covers, CTA, closing), 4x5/story slide titles, numerals, bars, quote and statement boxes (34% opacity), highlight box (46%), the thin top edge of infographic cards, the hub circle's outline, the single image's title highlighter. |
| Gris | `#E7E5E6` | JCG/Gris | Background of every content slide, single image and infographic. |
| Negro | `#000000` | JCG/Negro | Body text, X slide titles, infographic titles and card headings, arrow, chart label pills, connectors. |
| Blanco | `#FFFFFF` | JCG/Blanco | Text on dark and purple slides, image cards, infographic cards and hub circle, URL on dark/purple. |
| Verde | `#D3FF4E` | JCG/Verde | **Small accents only:** wordmark on dark/purple, CTA button, Archimoto phrase on purple covers, arrow on purple covers, sunburst, chart guide lines, "SÍ" pill, the infographic title's highlight (one line). One highlighter line per piece at most. |
| Lila Light | `#D8C1EA` | JCG/Lila Light | The chart's gain segment. Nowhere else (the old infographic look used it as a group tone; the new one doesn't). |
| Lila Deep | `#7E4FA6` | JCG/Lila Deep | Not used in the new look (it was the old infographic's third group tone). Keep the style; don't use it. |

### Purple is an accent (Juan, 2026-10-26: "too purple")

Grey, white and black carry most of the area of every grey slide, single image and infographic; purple marks things. Concretely:
- **No full purple bands** on grey frames: no purple footer band (infographics use his normal avatar footer bottom-left), no purple shape spanning the frame's width.
- **No purple-filled card headers on infographics:** cards are white with a thin Lila top edge (8 px) and black headings; the hub is white with a Lila outline.
- **At most 20% of a grey frame is purple-filled** (Lila, Lila Light, Lila Deep; each shape's area × its opacity; text, footer and arrow don't count). His point slide with a three-column chart is 14%; the old all-purple infographic was 25–34%. The QA audit (`figma-recipes.md` §9) measures it.
- Exceptions: purple covers, CTA and closing slides (a purple background is his look there; the check only runs on grey frames), and the single image's quote card (his measured `Quote card`, ≈ 47%).

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
| CTA / closing text | CTA BS Text 80 white · closing **100** (Juan's pick 2026-10-27) | BS Text 100–120 white | CTA 80 · closing 100 |
| Body (`punto`, `grafico`, `insight`; with or without a picture) | **Archivo 40**, 133.5%, paragraph gap 40 | **Archivo 50**, 133.5%, paragraph gap 50 | **Archivo 40**, 133.5%, paragraph gap 40 |
| Highlight box text | BS Display Bold 60 black | BS Display Bold 70 black | BS Display Bold 60 black |
| Infographic title (`Info/TitleHighlight/Verde`, black, on Verde) | BS Bold 72, two lines (second on Verde) | BS Bold 72, one line on Verde | BS Bold 72, one line on Verde |
| Infographic subtitle (always) | Archivo 24 | Archivo 24 | Archivo 24 |
| Infographic card heading / explanation and list items | BS Bold 30 black / Archivo 19, lh 128% (list sub-headings Archivo Bold 19) | same | same |
| Infographic closing question (inside the relaunch card) | BS Bold 27 | same | same |
| Infographic numeral (in the card's head row) | Archimoto Regular 44, Lila | same | same |
| YES / NO pills (`Pill/Yes`, `Pill/No` scaled 0.45) | BS Bold 18 | same | same |
| Hub text (`Info/HubCircle`, thin hub only — not rebuilt dense yet) | BS Bold 38 black (Ø 160) | BS Bold 40 (Ø 220) | BS Bold 40 (Ø 200) |
| Footer URL | Inter 30 (in block) | Inter 30 (in block) | Inter 30 (in block) |

Infographic sizes are Juan's dense decision tree as built (2026-10-29 → 11-10, `layouts.md` → Dense decision tree): as big as the words allow inside the fixed frame, one set of sizes per piece, the same on all three sizes when it fits. The old thin-card sizes (title 110, heading 50, lines 36/40/38, numeral 80) are superseded.

## Readability floor (hard rule)

- **Body (Archivo): at least 32 on 4x5, 35 on story, 40 on X.** **Infographic exception (Juan, 2026-10-29): 18 on every size.** He chose reference-level information over the 32 px floor for infographics; the frame stays ≤ 1000×1500 and the text shrinks to fit (built at Archivo 19, pills 18). Carousels and single images keep 32 / 35 / 40. 4x5 is the spec's 32px on a 1000-wide frame; story scales it to 1080; X uses 40 because that is what his X slides use (controller ruling 2026-10-26).
- **Nothing below 32px anywhere** (infographics: 18), except the Inter 30 URL inside his footer blocks.
- Slide bodies sit well above the floor (40 / 50 / 40, table above). Text that doesn't fit is cut in the brief or moved to another slide, never shrunk (see "Density" below).

## Density — neither dense nor empty (Juan, 2026-10-26)

Juan, first: *"make sure it's tidy and not all cramped. The ones you created in the past were overly dense."* The first test run put 2–3 paragraphs of 35 px text on each point and four 3-line cards on the infographic. Then the airy revision overcorrected: a text-only point with a box mid-slide and empty space below had *"too many open spaces"*. He picked the middle (`taste.md`): short text on top, a visual filling the lower half; infographic cards filling the space between title and footer.

- **One idea per slide.** A second idea is a second slide, or it is cut.
- **Fewer words, bigger type.** Cut words before anything else; never shrink type to make words fit.
- **Fill the slide with the visual, not with words.** The lower part of a grey slide carries a visual (chart, picture, big number) that reaches down to the content end. Infographic rows run from just under the title (≥ 18) to the content end; leftover room is shared evenly between the row gaps. Never add words or extra elements to fill room; grow the visual or spread the rows.
- **No empty strip above the footer:** between the last content and the footer's top there are at least 80 and at most **130 px** on 4x5 and story; on X at least 60 and at most **120 px** (to the footer on a single image or infographic, to the frame bottom on carousel slides). Variant A measured 80; the fixed infographic 80; variant B, the one Juan flagged, 147. The audit checks it on `punto`, `grafico`, `imagen`, `placa` and `infografia`.

**Word budgets** (the same words go on all three sizes; `layouts.md` has the per-kind table):

| Piece | Limit |
|---|---|
| `punto` body | ≤ 25 words, at most 2 short paragraphs |
| `grafico` body | ≤ 20 words, one paragraph (X: one line, ≤ 45 characters) |
| `insight` body (optional) | ≤ 20 words, one paragraph; X drops it |
| Highlight box / statement box | one line ≤ 6 words / two lines ≤ 12 words |
| Single image (`placa`) | one headline (≤ 28 characters) + one visual + at most one short supporting line (≤ 12 words) |
| Infographic (decision tree, Juan 2026-10-28 → 11-10) | Reference-level information, not thin cards: title ≤ 5 words + a subtitle (one line at 24) · every question card a heading (≤ 22 characters) + a one-line explanation · per branch a "Possible causes" and a "What you can do" list, 3–5 items each, ≤ ~26 characters per item · a closing check (relaunch card with its question → NO / YES outcomes) · ≈ 50 lines in all on 1000×1500. The old "≤ 2 lines of 16 characters, 3–5 cards" budget is superseded for infographics. |

**Minimum gaps** (measured from the text box or card edge; chosen against his slides, where the body sits ~30 px under the title and the picture ends ~270 px above the footer):

| Gap | 4x5 | X | Story |
|---|---|---|---|
| Slide title text → body | 64 (body at y 230) | 66 (body at y 250) | 64 (body at y 560) |
| Paragraph → paragraph | 40 | 50 | 40 |
| Body → visual (picture, chart, box) | 70 | 60 | 70 |
| Last element → footer (min – max) | 80–130 (content ends 982–1032) | 60–120 to the frame bottom (960–1020; single image and infographic: to their footer, 822–882) | 80–130 (1312–1362) |
| Infographic: title → first card | ≥ 18 (built 32) | ≥ 18 (built 27) | ≥ 18 (built 18) |
| Infographic: card ↔ card · card ↔ hub circle · pill ↔ card | 30 · 40 · 12 (dense, Juan's OK 2026-10-29; the thin layouts used 60) | same | same |

The QA audit (`figma-recipes.md` §9) checks the budgets, the gaps, the body sizes, the empty strip and the purple share.

## Grid per size

| | 4x5 · 1000×1250 | X · 1300×1080 | Story · 1080×1920 |
|---|---|---|---|
| Left text edge / width | x 55–60, w 885 | x 67, w 1173 (centred text: x 54, w 1192) | x 112, w 885 |
| Top of content | header at y 33; body from y 230 | header at y 48; body from y 250 | header at y 363; body from y 560 |
| **Content must end above** | y 1032 (content slides, single image, infographic: 80 above the footer; 1282 on a 1000×1500 infographic) / 960 (cover footer slides) | y 1020 (carousel) / 882 (single image and infographic, 60 above their footer) | y 1362 (content: 80 above the footer) / 1240 (cover footer slides) |
| **…and reach down to** (grey slides, no empty strip) | y 982 | y 960 (carousel) / 822 | y 1312 |
| Footer | content 30,1112 (also single image and infographic) · cover 400,996 | **none on carousel slides**; single image and infographic `Footer/Content` 30,942 | content 82,1442 (also single image and infographic) · cover 440,1268 |
| Arrow (grey slides + purple cover) | Negro 849,1121 on grey · Verde 862,61 on purple covers · none on dark, CTA, closing | none | Negro 901,1451 · Verde 929,380 on purple covers |
| Safe zone | whole frame | whole frame | keep text, pictures, charts and cards between y 250 and 1580 (phone story bars). Footers and arrows sit at his measured story positions and end by y 1600 at the latest (the CTA and closing footer at 415,1383 is the lowest); infographics use the content footer at 82,1442 |

Story rule of thumb: the story is the 4x5 slide dropped into the middle — left-aligned content +52 across, centred content re-centred in 1080, everything about +330 down; footers, arrows and asteroids use the story positions in `blocks.md`.

## Shapes and effects

- Image card: white, radius 20, shadow 4,4 blur 16 at 25% black (the `Card/Image` block).
- Quote box: Lila at 34%, radius 24, Lila quote marks top-left and bottom-right (`QuoteBox` block).
- Statement box (a sentence above a picture, e.g. his "Las plataformas no pueden distinguir…" slide in all three sizes): Lila at 34%, radius 24, **no stroke** — same look as the quote box without marks. Used by the `imagen` kind, and (Juan's pick 2026-10-26) as the box that holds a big number or two columns on a point slide, with black text inside.
- Highlight box (one key line or number, see `blocks.md` → Measured grids): Lila at 46% + 1px Lila stroke, radius 20, text **Big Shoulders Display Bold black, centred** (70 on X as measured; 60 on 4x5 and story). Measured on three of his X slides. It is the visual of a text-only `punto` (the exception; `layouts.md` → text-only point), sitting at the bottom of the room so the slide fills (recipe `highlightBox`). Build it as one rectangle with fill and stroke linked to JCG/Lila and layer opacity 0.46.
- Infographic card, dense (as built 2026-10-29): a plain auto-layout frame named `Card · <heading>` — white, radius 16, the image card's shadow, a 6 px Lila top edge, padding 16 top / 18 sides / 14 bottom, gap 7; a head row (Lila Archimoto numeral 44 + BS Bold 30 heading); then explanation and lists. When two cards share a row and one is shorter, both take the row's height and the shorter one's content is centred vertically (top-aligned left a hollow white band; Juan OK'd the centred "Kill it", 2026-10-29). The `Info/GroupCard/White` block (radius 20, 8 px edge, three line slots) is the thin look; it can't hold a list. Hub (`Info/HubCircle`): white circle, 4 px Lila outline, black Big Shoulders Bold text. Title (`Info/TitleHighlight/Verde`): black, the second line on a Verde block.
- CTA button: Verde pill (`Button/CTA`).
- Reactions strip on closing slides: his image, radius 40.
- Asteroids: whole pictures bleeding off opposite corners; the slide frame crops them (`clipsContent` on).
- Infographic connectors: black 3px, right angles (hub spokes are short straight diagonals), arrowhead where the direction matters.
- Icons: none by default — the numerals carry the groups. Offer his 3D images only when they can be big: at 52 px beside a 30 px heading they read as stamps and he picked the version without them (2026-10-29). Only four 3D images exist, all on page "Carousel": cart (`5556fc59…`, node `1:13980`; its 1024² picture has "LTV" lettering on top — crop with `imageTransform [[0.72,0,0.24],[0,0.5719,0.4281]]`, aspect ≈ 1.26), piggy bank (`41081043…`, `1:14044`), ghost (`2b1f9b28…`, `1:14603`, portrait, use FIT), "AD BREAK" bubble letters (`4b68f2e2…`, `1:14262`). Full hashes in `figma-recipes.md` §7. No icon library, no drawn icons.

## Footer

Always **jcgiusto.com**. Never asteroi.co (his old slides say it; new work must not). Infographics and single images use the same content footer as his grey slides (avatar bottom-left), never a purple band. Wordmark Lila on grey, Verde on dark or purple — always, even where one of his old dark slides used Lila; URL black on grey, white on dark or purple (`figma-recipes.md` §4).

## Words on the image

- Same language as Juan's input (usually Spanish). Talk to the reader as "tú" like his slides ("¿Quieres saber si…?", "tu cuenta").
- **Money stays in the currency of his source.** A post or article in $ stays in $; one in € stays in €. Never convert silently; if a mix seems odd, ask him. Spanish digits either way: dot for thousands, comma for decimals (`€60.000`, `$60.000`, `$10K`, `1,5x`).
- Big text (60 px and up) gets its line breaks written in the brief, so no word ends up alone on the last line (`layouts.md` → Big text).
- Short. A slide carries one idea, within the budgets under "Density". Titles in title case like his ("Audiencias Amplias"), ≤ 28 characters on 4x5/story.
- Bold one key phrase per paragraph, two at most (write them as `**…**` in the brief).
- Cover: a hook in two to four short lines; the Archimoto phrase is the punchline (2–3 words).
- Keep his voice: direct, practical, first person ("Te aseguro que…"). Don't invent numbers; take them from his post.
