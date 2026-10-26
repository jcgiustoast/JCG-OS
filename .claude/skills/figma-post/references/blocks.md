# Building blocks — `🧩 Bloques JCG`

updated: 2026-10-26

- **Figma file:** Contenido, fileKey `U2HIUwTWDYWL7EwSKCDpLd`
- **Page:** `🧩 Bloques JCG`, page ID **`31:21`**
- **Source of the pieces:** cloned from his slides on page "Carousel" (`1:13975`). Never edit those originals.
- **Count:** 34 blocks = 37 component nodes (Arrow has 2 variants, Info/GroupCard has 3). The 3 newest (2026-10-26, Juan's picked infographic look) sit in their own section. The purple-strip group card (3 tones) and the three infographic footer bands are marked **old look, don't use for new pieces** below; the Lila-highlight title is old look on infographics only.

## Fonts to load

Every font/style used anywhere on the blocks page (audited 2026-10-26). Load all of them before editing any text in a block instance:

```js
for (const [family, style] of [
  ['Big Shoulders Text', 'Bold'],
  ['Big Shoulders Text', 'Regular'],
  ['Big Shoulders Display', 'Bold'],   // Button/CTA `Label` and highlight-box text only (as on his slides)
  ['Archivo', 'Regular'],
  ['Archivo', 'Bold'],
  ['Inter', 'Regular'],                 // every `URL` line
]) await figma.loadFontAsync({ family, style });
```

Archimoto V00 is not on the page as text (it can't be loaded by scripts); numerals are vector outlines named `Numeral (placeholder)`.

## How to use

- Switch to the target page, then `const c = await figma.getNodeByIdAsync('<id>'); const i = c.createInstance(); frame.appendChild(i); i.x = …; i.y = …;`. For a variant, instance the variant's own ID (e.g. `Arrow` → `Color=Negro` `32:46`).
- Slide frames must keep `clipsContent = true`: asteroids and backgrounds are whole pictures that bleed past the edge, and the frame does the cropping.
- Text overrides: find the child by layer name inside the instance, load its font, set `characters`. Layer names: `Title`, `URL`, `Quote`, `Label`, `Heading`, `Line 1…3`, `Line 1`/`Line 2`/`Subtitle`, `Hub text`, `Value 1`, `Value 2 base`, `Value 2 top`, `Label 1`, `Label 2`, `Placeholder label`.
- Numerals: layers named `Numeral (placeholder)` are outlined copies of his Archimoto "1." (the font can't be loaded by scripts). Swap them for the right number with the Archimoto outline script; keep the position and the Lila fill.
- Images: in `Card/Image`, put the picture as an image fill on the `Image` layer and hide `Placeholder label`. Resize the instance to the picture's size; the card keeps radius 20 and the shadow.
- Every URL on the page reads `jcgiusto.com` (Inter Regular 30). Zero text nodes on the page contain "asteroi".

## Colour styles (paint styles)

| Style | Hex | Style ID |
|---|---|---|
| JCG/Lila | #B084D3 | `S:819d30b962bfe9df3a178084c6ff2e31b82920b4,` |
| JCG/Verde | #D3FF4E | `S:7af192d81f99624f5b0dc2db1b92629f1356d840,` |
| JCG/Gris | #E7E5E6 | `S:9e304f2dac7b9d01a42e5c3f66d5c3103b3beff9,` |
| JCG/Negro | #000000 | `S:379b5e45ffc6721f773972ff9bbce8b361de128b,` |
| JCG/Blanco | #FFFFFF | `S:b261762cdf1ca5185557dd3c210fdc9c00c5996e,` |
| JCG/Lila Light | #D8C1EA | `S:939f59d31d7447612c4e9e2989e6523183068a77,` |
| JCG/Lila Deep | #7E4FA6 | `S:e50e9637035a77a26f4095c0e7eacba7a23c4e95,` |

Apply with `await node.setFillStyleIdAsync(id)`. The quote box uses JCG/Lila with layer opacity 0.34 (same look as his 34% paint).

## Components — size-free (section "Bloques sin tamaño")

| Name | Node ID | Size | What it's for / where it goes |
|---|---|---|---|
| Arrow (set) | `32:50` | — | Next-slide arrow. Variants below. |
| Arrow · Color=Negro | `32:46` | 96×96 | Bottom-right of every grey content slide except the last. 4x5 at 849,1121 · story at 901,1451. His X slides have no arrow. |
| Arrow · Color=Verde | `32:48` | 96×96 | Top-right of purple covers. 4x5 at 862,61 · story at 929,380. |
| Sunburst | `32:51` | 166×164 | Green sticker with hard black shadow. Bottom-right of X covers at 1104,881 (smaller copy 112×111 at 1158,934 on one cover). |
| QuoteBox | `32:54` | 945×292 | Insight box for dark slides: Lila 34% box radius 24, Lila quote marks top-left/bottom-right, `Quote` text Big Shoulders Text Bold 60 white centred. 4x5 at 27,268. Resize the instance to fit; marks stay in their corners. |
| Button/CTA | `32:60` | 881×122 | Green pill call-to-action, `Label` Big Shoulders Display Bold 70 black, uppercase. 4x5 purple CTA slide at 64,645. |
| Card/Image | `32:62` | 886×500 | White image card, radius 20, shadow 4,4 blur 16 at 25% black. Placeholder "Pega aquí la imagen". 4x5 body width: x 59, w 886. |
| Chart/Bar | `32:65` | 723×520 | Two-bar comparison chart (Lila bars, light-Lila stacked gain, dashed green guides, black label pills). Rebuilt from shapes; his originals are pictures. Layers and height rule below. |

### Chart/Bar layers and how to set bar heights

Layers (plain frame, no auto-layout; coordinates inside the 723×520 chart):

| Layer | Type | Default | Notes |
|---|---|---|---|
| `Bar 1` | rectangle, JCG/Lila, top corners 16 | x 120, y 190, 160×250 | Left column bar. |
| `Bar 2 base` | rectangle, JCG/Lila, square | x 443, y 190, 160×250 | Right column, the part equal to bar 1. |
| `Bar 2 top` | rectangle, JCG/Lila Light, top corners 16 | x 443, y 30, 160×160 | Right column, the gain stacked on top. |
| `Guide top` | dashed line, JCG/Verde 3px, dash 12/8 | x 40, y 30, 643 long | Marks the top of the tallest column. |
| `Guide middle` | dashed line, same | x 40, y 190, 643 long | Marks the top of `Bar 1` (the comparison level). |
| `Value 1` | text, Big Shoulders Text Bold 40, white, centred, 160 wide | x 120, y 291 | Value inside `Bar 1`. |
| `Value 2 base` | text, same, white | x 443, y 291 | Value inside `Bar 2 base`. |
| `Value 2 top` | text, same, **black** | x 443, y 86 | Value inside `Bar 2 top`. |
| `Label 1 pill` / `Label 2 pill` | rectangle, JCG/Negro, radius 6, 240×58 | x 80 / 403, y 440 | Black label pills; bars stand on them. |
| `Label 1` / `Label 2` | text, Big Shoulders Text Bold 32, white, centred, 240 wide | x 80 / 403, y 449 | Column names, uppercase. |

Height rule (positions can't be overridden inside an instance, so **detach the instance first**: `const chart = instance.detachInstance();`, then edit its layers):

1. Baseline = y 440 (top of the label pills). Room for bars = 410 px (y 30 → 440).
2. `scale = 410 / largestColumnTotal`. Each segment height = `round(value × scale)`.
3. `Bar 1`: height = v1 × scale, `y = 440 − height`. `Bar 2 base`: same with its value. `Bar 2 top`: height = gain × scale, `y = Bar 2 base.y − height` (sits on the base). Drop `Bar 2 top` if there is no gain, and give `Bar 2 base` the 16 top corners instead.
4. `Guide top.y` = top of the tallest column; `Guide middle.y` = `Bar 1.y`.
5. Centre each value text in its segment: `text.y = seg.y + (seg.height − text.height) / 2` (text height 48). If a segment is under ~70 px tall, move its value just above the segment and make it black.

## Components — infographic, new look (section "Infografía · nuevo look (2026-10-26)", `111:53`)

Juan's pick on 2026-10-26 (variant B, `taste.md`). Built 2026-10-26 and used in "Infografía B (arreglada)" on the variants page (audit clean). Use these for every new infographic.

| Name | Node ID | Size | What it's for |
|---|---|---|---|
| Info/GroupCard/White | `111:55` | 360 wide, height hugs (2 lines at 36: 238) | Numbered group card: white (JCG/Blanco), radius 20, the image card's shadow, clips its content. `Top edge (Lila)` 8 px rectangle across the top (absolute, stretches with the width). Vertical auto-layout, padding 32 top / 30 sides / 28 bottom, gap 20: `Head` row (gap 18, centred) = `Number slot` (53×56, holds `Numeral (placeholder)`, a Lila outline of "1." at Archimoto Regular 80, ink-tight) + `Heading` (Big Shoulders Text Bold 50, black, fills the row) · `Lines` (gap 2) = `Line 1…3`, Archivo Regular 34, lh 133.5, black. Resize the width freely; set sizes per size (`layouts.md`); swap the numeral with `swapNumeral(svg, card, slide, { center: true })`; hide `Line 3` (and `Line 2` for one line) last. The slot keeps the heading in place after the placeholder is hidden. |
| Info/TitleHighlight/Verde | `111:67` | 951×277 (hugs) | Infographic title: vertical auto-layout, centred, gap 8 · `Line 1` Big Shoulders Text Bold 110, lh 101, black · `Highlight` frame (JCG/Verde, padding 0/20) holding `Line 2` (same text style) · optional `Subtitle` Archivo 36 (hide if unused). Two lines = 230 tall. X: hide `Line 1` and put the whole title in `Line 2` at 90. |
| Info/HubCircle | `111:72` | 160×160 | Hub centre: `Hub` ellipse (JCG/Blanco fill, 4 px JCG/Lila stroke inside) + `Hub text` (Big Shoulders Text Bold 38, black, centred both ways in a fixed 130×130 box). Both scale with the instance: resize it to the size's diameter (4x5 160, X 220, story 200) and set `Hub text` size 38 / 40 / 40. |

The section also holds a note for Juan explaining the new look (text `Nota nuevo look`).

## Components — infographic (section "Infografía")

**Old look, don't use for new pieces:** the purple-strip `Info/GroupCard` (set and its three tones) and `Info/TitleHighlight` on infographics (Juan, 2026-10-26: "too purple"). Kept because his file has them and `Info/TitleHighlight` is still the single image's title. The QA audit flags the old cards anywhere and the old title on an infographic.

| Name | Node ID | Size | What it's for |
|---|---|---|---|
| Info/GroupCard (set) | `34:55` | — | **Old look, don't use for new pieces.** Numbered group box. Property `Tone`. |
| Info/GroupCard · Tone=Lila | `34:22` | 440×317 (hugs height) | **Old look.** White card radius 20, Lila header strip with number badge + `Heading` (Big Shoulders Text Bold 46, white), `Line 1…3` Archivo 32. |
| Info/GroupCard · Tone=Light | `34:33` | 440×317 | **Old look.** Same, light-Lila strip, black heading. |
| Info/GroupCard · Tone=Deep | `34:44` | 440×317 | **Old look.** Same, deep-Lila strip, white heading. |
| Info/TitleHighlight | `34:56` | 951×288 (hugs) | Single-image title: `Line 1` Big Shoulders Text Bold 110 black; `Line 2` on a Lila highlighter block; optional `Subtitle` Archivo 36 (hide if unused). Centre at the top. **On infographics it is the old look** — use `Info/TitleHighlight/Verde`. |
| Pill/Yes | `34:61` | 100×68 (hugs) | Decision-tree "SÍ" pill, Verde, Big Shoulders Text Bold 40 black. |
| Pill/No | `34:63` | 114×68 (hugs) | Decision-tree "NO" pill, Lila, Big Shoulders Text Bold 40 white. |

The `Info/FooterBand/*` blocks in the sized sections below are the **old look, don't use for new pieces**: infographics now use `Footer/Content/*` like his grey slides.

## Components — 4x5 · 1000×1250 (LinkedIn) (section `35:21`)

| Name | Node ID | Size | Place at | What it's for |
|---|---|---|---|---|
| Background/Stars/4x5 | `35:22` | 1000×1250 | 0,0 (bottom layer) | Dark slide background: his star-field image. |
| Asteroid/TopLeft/4x5 | `35:24` | 290×248 | dark −188,0 · purple −115,−63 | Whole asteroid; frame crops it. |
| Asteroid/BottomRight/4x5 | `35:26` | 412×392 | dark 758,985 · purple 752,858 | Whole asteroid; frame crops it. |
| Footer/Content/4x5 | `35:28` | 314×114 | 30,1112 | Grey content slides: avatar 114, JCGIUSTO in Lila, `URL` jcgiusto.com black. On a dark or purple slide, switch the wordmark to Verde and the URL to white (see "Footer colour on dark or purple slides" below). |
| Footer/Cover/4x5 | `35:33` | 200×217 | 400,996 (CTA slide: 400,1016) | Covers, purple and dark slides: avatar 129 centred, JCGIUSTO Verde, `URL` white. Use it as it comes; keep the wordmark Verde (see "Footer colour on dark or purple slides" below). |
| Header/Numbered/4x5 | `35:37` | 890×165 | 55,33 | Numeral placeholder (Archimoto Regular 150, Lila) + `Title` Big Shoulders Text Bold 60 Lila at +146,+61. |
| Info/FooterBand/4x5 | `35:42` | 1000×140 | 0,1110 | **Old look, don't use for new pieces.** Former infographic footer: Lila bar, avatar + JCGIUSTO Verde + jcgiusto.com white, centred. Infographics use `Footer/Content/4x5` at 30,1112. |

### Footer colour on dark or purple slides

Applies to every `Footer/Content/*` and `Footer/Cover/*` instance. His rule: wordmark **Lila on grey**, **Verde on dark (stars) or purple**; URL black on grey, white on dark or purple.

- `Footer/Content/*` defaults to the grey look (wordmark JCG/Lila, URL JCG/Negro). On a dark or purple slide, override both:
  `await inst.findOne(n => n.name === 'JCGIUSTO').setFillStyleIdAsync(<JCG/Verde id>);`
  `await inst.findOne(n => n.name === 'URL').setFillStyleIdAsync(<JCG/Blanco id>);`
- `Footer/Cover/*` defaults to the dark/purple look (wordmark JCG/Verde, URL JCG/Blanco) — keep it. One old dark slide of his ("Insight Clave") has a Lila wordmark; new work does not copy that: the wordmark is **Verde on every dark and purple slide** (`layouts.md` → insight, `style.md` → Footer).
- `JCGIUSTO` is a vector (the wordmark), `URL` is a text layer (Inter Regular 30). Fill-style overrides on both work inside instances (tested 2026-10-26); no detach needed.

## Components — x · 1300×1080 (X) (section `35:47`)

| Name | Node ID | Size | Place at | What it's for |
|---|---|---|---|---|
| Background/Stars/x | `35:48` | 1300×1080 | 0,0 | His wide star image + dashed Lila orbit line from his X covers (hide `Orbit (dashed Lila, optional)` if unwanted). |
| Asteroid/TopLeft/x | `35:51` | 290×248 | top-left −103,−79 · dark covers bottom-left −72,858 | Whole asteroid. |
| Asteroid/BottomRight/x | `35:53` | 412×392 | 1048,800 | Whole asteroid, rotated as in his X slides. |
| Footer/Content/x | `35:55` | 314×114 | 30,942 | **Not in his X originals** (none of his 44 X slides shows a footer). The footer of X single images and infographics (content ends ≤ 882). Grey look by default; on dark or purple switch `JCGIUSTO` to Verde and `URL` to white (see "Footer colour on dark or purple slides"). |
| Footer/Cover/x | `35:60` | 200×217 | 550,826 (proposed) | **Not in his X originals**; his X covers are title + chart + sunburst only. Optional. |
| Header/Numbered/x | `35:64` | 1173×165 | 67,48 | Numeral placeholder (Archimoto Bold 150, Lila) + `Title` Big Shoulders Text Bold 90 **black** at +147,+28. |
| Info/FooterBand/x | `35:69` | 1300×140 | 0,940 | **Old look, don't use for new pieces.** Former infographic footer band, landscape width. |

## Components — story · 1080×1920 (section `35:74`)

| Name | Node ID | Size | Place at | What it's for |
|---|---|---|---|---|
| Background/Stars/story | `35:75` | 1080×1920 | 0,0 | Star-field image (1118×1958, fills the frame). |
| Asteroid/TopLeft/story | `35:77` | 290×248 | dark −139,272 · purple cover −137,304 · CTA and closing −100,304 (his closing `1:14121`) | Whole asteroid (stories keep it inside the safe zone, not at the very top). |
| Asteroid/BottomRight/story | `35:79` | 412×392 | 807,1257 (purple cover 843,1261) | Whole asteroid, rotated. |
| Footer/Content/story | `35:81` | 314×114 | 82,1442 | Grey content stories; add Arrow Negro at 901,1451. On dark or purple switch `JCGIUSTO` to Verde and `URL` to white (see "Footer colour on dark or purple slides"). |
| Footer/Cover/story | `35:86` | 200×217 | 440,1268 (closing slides 415,1383) | Story covers. |
| Header/Numbered/story | `35:90` | 890×165 | 107,363 | Same as 4x5 header (Regular numeral, Lila title 60). |
| Info/FooterBand/story | `35:95` | 1080×140 | 0,1440 | **Old look, don't use for new pieces.** Former infographic footer band, story width. Infographics use `Footer/Content/story` at 82,1442. |

## Previews on the page (not components)

Assembled from block instances to check the match against his slides. Keep them as worked examples.

| Preview | Node ID | Compare with original |
|---|---|---|
| 4x5 numbered | `36:21` | `1:14330` |
| 4x5 dark quote | `36:36` | `1:14563` |
| x dark cover | `36:55` | `1:14594` |
| story numbered | `36:70` | `1:14161` |

## Measured grids

Measured from his slides on page "Carousel" on 2026-10-26. Coordinates are x,y inside the slide frame. These describe his originals; new slides use the airier body sizes, word budgets and gaps in `style.md` → Density (Juan, 2026-10-26), e.g. body Archivo 40 from y 230 and content ending by y 1032 on 4x5.

### 4x5 · 1000×1250 (twins: `1:14330`, `1:14295`, `1:14563`, `1:14471`, `1:14448`, `1:14130`, `1:14714`)

- **Margins:** text from x=55–60, width 885 (right edge ≈ 945). Footer sits 30 from the left, 24 from the bottom.
- **Numbered content slide (grey):** numeral "1." Archimoto Regular 150 Lila at 55,33 · title Big Shoulders Text Bold 60 Lila at 201,94 (line height auto, 72 tall) · body Archivo Regular/Bold 35, line height 133.5%, first paragraph at y≈188–200, ~25–30 between paragraphs · image card from y≈467–523, up to 886 wide, radius 20, shadow · his content stays above y≈1080 (his picture ends ≈ 844).
- **Content footer:** avatar 114 at 30,1112 · wordmark 163×26 at 164,1137 · URL Inter Regular 30 at 164,1169 · arrow 96 at 849,1121.
- **Cover footer:** avatar 129 at 435,996 (dark slides 429,996) · wordmark 418,1145 · URL 430,1177, white. Purple CTA slide sits 20 lower (avatar 435,1016).
- **Covers:** headline Big Shoulders Text Regular/Bold 130, line height 107% (purple) or Bold 130 / 101% (dark, e.g. "Insight Clave" at 29,102, w 929, centred). Big Archimoto numeral 250; Archimoto Bold 120 key phrase (Verde on purple, Lila on dark), centred across x 30–948. Verde arrow top-right at 862,61. Dark cover with chart: Archimoto 120 Lila at 71,124 (w 845, centred), Big Shoulders 100 white at y 388, chart card 628×389 at 186,536.
- **Dark quote slide:** title 130 at y 102 · QuoteBox at 27,268 (box 945×255 at 27,288) · quote Big Shoulders Text Bold 60 white, line height 101%, centred · body Archivo 35 white centred, x 55–59, w 885, from y≈613.
- **Purple CTA slide:** Big Shoulders Text Regular 80 white centred at y 249, Bold 80 line at y 466, Button/CTA at 64,645.

### x · 1300×1080 (twins: `1:15507`, `1:14594`, `1:14602`, plus `1:15515`, `1:15519`, `1:14632`, `1:14669`, `1:14709`, `1:14698`, `1:15630`)

- **No footer and no arrow** on any of his 44 X slides (two closing slides have the wordmark at y=1080, i.e. off the canvas). The X version is re-laid out wide, not a stretched 4x5.
- **Margins:** text x≈46–67, width ≈1173–1208; centred text uses x 54, w 1192.
- **Dark cover:** Background/Stars/x (image 1952×1140 at −32,−60 + dashed Lila orbit, 3px, dash 20/20, rotated 8°) · Archimoto Bold 120 Lila line centred (y 188–290) · Big Shoulders Text Bold/Regular 120 white line, w 820 centred (y 118–305) · picture/chart 628–818 wide centred from y 450–492, radius 20 · Sunburst at 1104,881 · asteroid bottom-left at −72,858.
- **Numbered content (grey):** numeral "1." Archimoto **Bold** 150 Lila at 67,48 · title Big Shoulders Text Bold 90 **black** at 214,76 (or Regular 80 at 227,92) · body Archivo 40, line height 158%, at x 67, w 1173, from y 242 · images up to 1194 wide.
- **Text-led content (grey):** centred; title Big Shoulders Text 70–100 (Bold for the key line); body Archivo 40 (157%) or 50 (133.5%); picture card 830–941 wide centred, radius 15–20, from y≈430–480.
- **Quote (grey):** Lila quote marks 178×125 at 54,83 and 1068,555 · Big Shoulders Text 90 black centred at 54,250, w 1192.
- **Highlight box:** Lila at 46% + 1px Lila stroke, radius 20 (e.g. 86,325, 1128×156) with Big Shoulders Display Bold 70 black.
- **Purple closing:** Big Shoulders Text Bold 100 / Regular 100–120 white centred · asteroids top-left −103,−79 and bottom-right 1048,800 (rotated).

### story · 1080×1920 (twins: `1:14053`, `1:14068`, `1:14077`, plus `1:14140`, `1:14161`, `1:15147`, `1:15423`)

- **Rule:** the story is the 4x5 layout dropped into the middle of the tall frame, shifted by about +40…+52 across and +272…+335 down. The top ~250 and bottom ~350 stay empty (phone story UI).
- **10 Meta Ads series (the blocks follow this):** numeral Archimoto Regular 150 Lila at 107,363 · title Big Shoulders Text Bold 60 Lila at 253,424 · body Archivo 35 at x 112, w 885, from y≈518 · footer: avatar 82,1442, wordmark 216,1467, URL 216,1499 · arrow 901,1451.
- **AOV / Incrementalidad series:** numeral Archimoto Bold 150 at 71,249 · title Big Shoulders Text Bold 60 **black** at 239,297 · body Archivo 40, 158%, at x 90, w 829, from y 414 · footer avatar 80,1332, wordmark 214,1357, no URL line · arrow 899,1341.
- **LTV series:** content slides have no footer · title Big Shoulders Text Bold 100 (101%) at ≈131,439 or Bold 80 (125%) · body Archivo 50–60, 133.5%, at x≈100, w 885 · Lila 20% boxes radius 24 (≈878 wide at x 104) · Verde box radius 21 for the closing line.
- **Covers:** cover footer avatar 129 at 475,1268, wordmark 458,1417, URL 470,1449 (purple cover lower: avatar 484,1348; closing slides: avatar 450,1383, wordmark 433,1532) · headline Big Shoulders Text Bold 130, 101%, white, centred at 78,354, w 929 · Archimoto Bold 200 Verde phrase.
- **Background:** star image 1118×1958 at 0,0.

### Type sizes at a glance

| Role | 4x5 | x | story |
|---|---|---|---|
| Cover headline | BS Text 130 | BS Text 120 | BS Text 130 |
| Archimoto key phrase | 120 (numeral 250) | 120 | 120–200 |
| Slide title | BS Text Bold 60 Lila | BS Text Bold 90 black (70–100) | BS Text Bold 60 (Lila or black) |
| Numeral | Archimoto 150 | Archimoto Bold 150 | Archimoto 150 |
| Body | Archivo 35 / 133.5% | Archivo 40 / 158% or 50 / 133.5% | Archivo 35–40 (LTV 50–60) |
| URL | Inter 30 | — (no footer) | Inter 30 |
