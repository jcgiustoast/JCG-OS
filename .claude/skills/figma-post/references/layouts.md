# Layouts — what goes where, per slide kind and size

updated: 2026-10-26

Coordinates are x,y inside the frame. Block names → IDs in `blocks.md` (and the `B` table in `figma-recipes.md`). "Measured" = copied from his slides; "derived" = my layout in his grid, not in his file — check it on the screenshot.

Frames are named `<n>-<kind>`. Kinds: `portada`, `punto`, `grafico`, `imagen`, `insight`, `cta`, `cierre` (carousel) · `placa` (single image) · `infografia` (infographic).

## Carousel

### Shape of a carousel

- Always: `portada` first, `cierre` last. `cta` before `cierre` only when the post has an offer or a "write me" ask.
- Cover look: **dark (stars) by default.** Purple when the headline leads with a number or a list ("10 estrategias…", "5 errores…").
- Middle: one slide per point. `punto` by default — **text on top, a visual filling the lower half** (Juan's pick 2026-10-26: a chart, a picture card or a big number); `grafico` when the whole point is one before/after number; `imagen` when the point is a screenshot with a statement; one `insight` around the middle for the key idea (a quote from the post). A text-only point is the exception (only when Juan asks).
- Numerals count the points in order (`punto` and `grafico` slides): 1., 2., 3. … `imagen`, `insight`, `cta` and `cierre` have none.
- Background per kind (the `bg` in recipe 3): `portada` → `stars` (dark) or `lila` (purple) · `punto`, `grafico`, `imagen` → `gris` · `insight` → `stars` · `cta`, `cierre` → `lila`.
- Arrows, as in his file: black arrow bottom-right on the grey slides (`punto`, `grafico`, `imagen`) of 4x5 and story; Verde arrow top-right on a purple cover. None on dark slides, `cta` or `cierre`, and none anywhere on X.
- Picture cards with no picture yet: full content width (4x5 886, X 1000 centred, story 842 centred), height = the whole room under the body: from body bottom + 70 (X 60) down to the content end. A real picture keeps its proportions, grows until it fills the room's width or height, sits centred across and ends at the content end (any leftover room goes above it, not below).
- 5 slides: `1-portada` · `2-punto` · `3-grafico` · `4-insight` · `5-cierre`. 6–10 slides: add points. One idea per slide: a point that needs more words becomes two slides.

### Word budgets (fit the text in the brief, not in Figma)

Neither dense nor empty (Juan, 2026-10-26; `style.md` → Density). Cut words before anything else; room left over goes to the visual, never to more words.

| Kind | 4x5 / story | X |
|---|---|---|
| Slide title | ≤ 28 characters (one line) | ≤ 24 characters |
| `punto` body (with its visual, or text only) | ≤ 25 words, at most 2 short paragraphs | same words |
| Highlight box (the visual of a text-only point, the exception) | one line, ≤ 6 words / 30 characters (70 px) | same (80 px in the 1173 box) |
| `grafico` body | ≤ 20 words, one paragraph (3 lines at most) | one line, ≤ 45 characters (≈ 7 words; Archivo 50 in the 1173 box) |
| `imagen` statement box | two lines, ≤ 12 words | same |
| Insight title | a short label ≤ 16 characters ("Insight Clave", "La clave", "Ojo con esto"; Big Shoulders Bold 130 is ≈ 51 px a character, so 18 would fill the 929 box) | same |
| Insight quote / body | ≤ 14 words, two lines with a hand break / ≤ 20 words, optional | ≤ 14 words / none |
| Cover | Archimoto phrase 2–3 words + headline ≤ 6 words | same |
| CTA | question ≤ 14 words + one bold line ≤ 6 words + button ≤ 20 characters | same |

The same words go on all three sizes, except X drops the insight body and keeps the `grafico` body to one line (say so in the brief).

### Gaps (content slides)

| Gap | 4x5 | X | Story |
|---|---|---|---|
| Slide title text → body | 64: body at y 230 (title ends 166) | 66: body at y 250 (title ends 184) | 64: body at y 560 (title ends 496) |
| Paragraph → paragraph (`paraGap`) | 40 | 50 | 40 |
| Body → visual (picture, chart, highlight box) | 70 | 60 | 70 |
| Last element → footer | 80: ends ≤ 1032 | 60 to the frame bottom: ends ≤ 1020 | 80: ends ≤ 1362 |
| …but no empty strip: last element → footer at most | 130: ends ≥ 982 | 120 to the frame bottom: ends ≥ 960 | 130: ends ≥ 1312 |

The visual takes the room: it starts at body bottom + the body → visual gap and ends at the content end (1032 / 1020 / 1362). Leftover room never sits under the visual (Juan: "too many open spaces"); the audit flags a strip above the footer wider than 130 (X 120).

### Big text: never one word alone on the last line

Any text at 60 px or more (cover headline, insight title and quote, CTA and closing lines, statement and highlight boxes, single-image headings) must not end with a single word on its last line (e.g. "**creces**" alone under "…por qué no").
- **In the brief**, show the break of every headline, quote, closing line and box line as a real line break, the same break in all three sizes:
  que explica
  **por qué no creces**
  Only the Figma code writes it as `\n`: `'que explica\n**por qué no creces**'`, `'Bajar un 2% tus costes variables\n= subir un 2% tu ARPU'`.
- **Each line must fit its box on its own.** Rough fit: Big Shoulders Bold takes ≈ 0.38 × size px per character (Regular a little less), so a box holds `width ÷ (0.38 × size)` characters: 4x5 cover 900 at 130 ≈ 18 · X cover 1192 at 120 ≈ 26 · closing 4x5 915 at 80 ≈ 30, X 1220 at 100 ≈ 32 · quote 844 at 60 ≈ 37, X 963 at 70 ≈ 36.
- **If the audit still flags one** (it measures every 60 px+ text), move the break or widen the box to the size's full centred width (4x5 x 40 w 920 · X x 54 w 1192 · story x 80 w 920). Never shrink the text below the sizes in these tables.
- Keep a number with its unit and a symbol with its number on the same line ("$10K", "2%", "1,5x").

### `portada` — dark cover (stars) · measured

| Element | 4x5 · 1000×1250 | X · 1300×1080 | Story · 1080×1920 |
|---|---|---|---|
| Background | `Background/Stars` (placed by recipe 3) | same | same |
| Asteroids | `Asteroid/TopLeft` −188,0 · `Asteroid/BottomRight` 758,985 | `Asteroid/TopLeft` at −72,858 (bottom-left) only | `Asteroid/TopLeft` −139,272 · `Asteroid/BottomRight` 807,1257 |
| Archimoto phrase, Bold 120, Lila | centred, y 130 (a second line y 262) | centred, y 194 | centred, y 402 (second line 534) |
| Headline, BS Text 100 white, key words **Bold** | x 84, w 832, centred, y = phrase bottom + 10 | BS Text 120, x 240, w 820, centred, y 305 | x 130, w 820, centred, y = phrase bottom + 10 |
| Picture (`Card/Image`) or chart | 628×389, x 186, y = headline bottom + 30 (his: 536), ends ≤ 960 · or `Chart/Bar` at x 138 | 628×389 at 336,492 | 628×389, x 226, y = headline bottom + 30 (his: 808), ends ≤ 1240 |
| Sunburst | — | 1104,881 | — |
| Footer | `Footer/Cover` 400,996 | none | `Footer/Cover` 440,1268 |

An Archimoto line must fit: ≤ 900 wide on 4x5, ≤ 1200 on X, ≤ 960 on story (the SVG's `width`). Longer → split at a word into two lines, one SVG each, 132 apart ("el secreto" / "del aov" on 4x5; one line on X). X variant from his "Mega-Guía": headline at y 118, Archimoto phrase y 296, picture 818×499 at 241,450.

**X star backgrounds:** keep the dashed Lila orbit line on X covers (both of his X dark covers have it) and hide it on every other X star slide (his X insight has none): `bg.findOne(n => n.name === 'Orbit (dashed Lila, optional)').visible = false;`.

**Dark cover without a picture** (derived, tested twice): headline Big Shoulders Text 130 (X 120), **Regular with the key words Bold** (the brief's `**…**`), lh 101, white, centred, with its hand break (see "Big text"); Archimoto phrase 10 above it; centre the whole stack vertically in the band below, keeping the same asteroids, sunburst and footer:

| | 4x5 | X | Story |
|---|---|---|---|
| Stack centred between | y 200 and 900 | y 150 and 850 | y 420 and 1200 |
| Headline box | x 50, w 900 | x 54, w 1192 (his centred width; the old 1100 box left "creces" alone) | x 90, w 900 |

### `portada` — purple cover · measured on 4x5/story, derived on X

| Element | 4x5 | X | Story |
|---|---|---|---|
| Background | Lila | Lila | Lila |
| Asteroids | TopLeft −115,−63 · BottomRight 752,858 | TopLeft −103,−79 · BottomRight 1048,800 | TopLeft −137,304 · BottomRight 843,1261 |
| Arrow | `Arrow` Verde 862,61 | none | Verde 929,380 |
| Text stack, centred | lines from y 177 to ≤ 900 | lines from y 150 to ≤ 860 | 4x5 stack + 365 down |
| Sunburst | — | 1104,881 | — |
| Footer | `Footer/Cover` 400,996 | none | `Footer/Cover` 449,1348 |

His example ("10 Estrategias para optimizar Meta Ads en eCommerce"): Archimoto Regular 250 white "10" at 118,177 beside BS Text Regular 130 white "Estrategias" at 420,252 · Archimoto Bold 120 **Verde** phrase centred at y 448 · "Meta **Ads**" line at y 587 · "en eCommerce" BS Text Regular 130 at y 745. Line pitch ≈ 140–160.

Line order on every size: (1) the number (Archimoto Regular, white) beside the first word(s) (Big Shoulders Text Regular, white), (2) the Archimoto Bold Verde phrase, (3–4) the rest of the headline in Big Shoulders Text, key word Bold. At most 4 lines.

| Line sizes | 4x5 | X (derived) | Story |
|---|---|---|---|
| Number | Archimoto Regular 250 | Archimoto Regular 220 | Archimoto Regular 250 |
| Words | BS Text 130, lh 107 | BS Text 120, lh 107 | BS Text 130, lh 107 |
| Verde phrase | Archimoto Bold 120 | Archimoto Bold 120 | Archimoto Bold 120 |
| Line pitch | ≈ 150 | ≈ 140 (4 lines fill y 150–860) | ≈ 150 |

### `punto` — point: text on top, a visual filling the lower half (grey) · Juan's pick 2026-10-26

Variant A on the variants page ("Diapositiva A · Texto + gráfico", measured): header, ≤ 2 short paragraphs at Archivo 40, then one visual that fills the room down to the content end.

| Element | 4x5 | X | Story |
|---|---|---|---|
| Header | `Header/Numbered` 55,33 · `Title` Lila 60 · numeral Regular 150 | `Header/Numbered` 67,48 · `Title` black 90 · numeral **Bold** 150 | `Header/Numbered` 107,363 |
| Body (`addText`, ≤ 25 words, ≤ 2 paragraphs) | x 60, w 885, y 230, Archivo 40, lh 133.5, `paraGap` 40 | x 67, w 1173, y 250, Archivo 50, lh 133.5, `paraGap` 50 | x 112, w 885, y 560, Archivo 40, lh 133.5, `paraGap` 40 |
| Room for the visual | body bottom + 70 → 1032 | body bottom + 60 → 1020 | body bottom + 70 → 1362 |
| Footer | `Footer/Content` 30,1112 | none | `Footer/Content` 82,1442 |
| Arrow | `Arrow` Negro 849,1121 | none | Negro 901,1451 |

Measured on variant A (4x5): title ends 166 · body 230–482 (25 words, two paragraphs of two lines) · chart 885×480 at 60,552 → ends 1032, 80 above the footer · audit clean, purple 14%.

**The visual — pick one in the brief:**
- **Chart, two columns:** `Chart/Bar` detached (recipe 6), rescaled to fill the room: `k = min(room height / 520, max width / 723)` with max width 885 (4x5, story) or 1173 (X); centred across, bottom at the content end.
- **Chart, three columns** (variant A, built from shapes, measured; frame `Chart/Bar · 3 columnas`, 885 × room at x 60): legend at the frame's top-left — 30×30 squares, radius 6, Lila "HOY" at 0,6 and Lila Light "AL CRECER" at 128,6, labels Big Shoulders Text Bold 34 black 12 to the right of each square; bars 200 wide at x 48, 343 and 638 inside the frame, standing on black label pills 240×58 (radius 6, at x 28, 323, 618, bottom of the frame) with Big Shoulders Text Bold 32 white labels centred; today in Lila, the growth stacked on top in Lila Light (top corners 16); Verde 3 px guides across the full width at the tops being compared; the tallest column reaches 90 under the frame top.
- **Picture card:** `Card/Image` filling the room (see "Shape of a carousel" → picture cards).
- **Big number** (derived, not yet built): Archimoto Regular Lila outline centred, plus one Big Shoulders Text Bold 60 black line under it (≤ 12 words, 30 below, X 70); size the number so the stack fills the room (start at 300 on 4x5/story, 280 on X; up to 400) and put the stack's bottom at the content end.

A two-line title (over the budget) pushes the body down 70.

### Text-only point (no visual) · the exception · derived

Only when Juan asks for no visual. It must still fill (Juan: a box mid-slide with empty space below had "too many open spaces"):
- Body one step bigger: Archivo 48 on 4x5/story, 60 on X (still ≤ 25 words, ≤ 2 paragraphs, `paraGap` = the size).
- **Highlight box** (style.md → highlight box) closes the slide at the bottom: the key line, one line ≤ 6 words, Big Shoulders Display Bold black centred, 70 on 4x5/story, 80 on X. Box = body width (4x5 x 60 w 885 · X x 67 w 1173 · story x 112 w 885), height = text + 70, **ending at the content end** (4x5 1032 · X 1020 · story 1362; recipe `highlightBox` with `anchor: 'bottom'`, figma-recipes §4).
- If the room between body and box comes out over ≈ 250, the point is too thin for text only: give it a visual instead. No box line worth showing → also a visual.

### `grafico` — the whole point is one before/after number · derived from his chart slide

Same header, footer and arrow as `punto`, a shorter body, and `Chart/Bar` (detach + `setBars`, recipe 6) filling the room, as in `punto`:

| | 4x5 | X | Story |
|---|---|---|---|
| Body | x 60, w 885, y 230, Archivo 40 (≤ 20 words, one paragraph) | x 67, w 1173, y 250, Archivo 50, one line ≤ 45 characters | x 112, w 885, y 560, Archivo 40 |
| Chart | `k = min((1032 − top) / 520, 885 / 723)`, centred across, ends at 1032 (3-line body: top 460, k 1.1 → 795×572 at x 102) | `k = min((1020 − top) / 520, 1173 / 723)`, ends at 1020 (one-line body: top 377, k ≈ 1.24 → 894×643) | as 4x5, ends at 1362 |

### `imagen` — picture slide with a statement box (grey) · derived

Positions copied from his "Las plataformas no pueden distinguir correlación de causación" slide in all three sizes; box heights and the picture card are derived. The box is the **statement box** from `style.md` (Lila 34%, radius 24, no stroke) — not the 46% stroked highlight box.

| Element | 4x5 | X | Story |
|---|---|---|---|
| Statement box (rectangle, JCG/Lila, opacity 0.34, radius 24, no stroke) | 30,129, 929 × (text + 60) | 61,72, 1178 × (text + 110) | 70,322, 929 × (text + 60) |
| Text in the box, BS Text Bold 60 black, lh 101, centred | x 60, w 869, vertically centred in the box | BS Text Bold 80, x 104, w 1092 | x 100, w 869 |
| Picture (`Card/Image`, radius stays 20) — fills the room | 929 wide at 30, from box bottom + 60 down to 1032 | 969 wide at 165, from box bottom + 50 down to 1020 | 929 wide at 70, from box bottom + 60 down to 1362 |
| Footer / arrow | as `punto` | none | as `punto` |

Box: `const r = figma.createRectangle(); slide.appendChild(r); r.resize(929, h); r.x = 30; r.y = 129; r.cornerRadius = 24; await r.setFillStyleIdAsync(S.lila); r.opacity = 0.34;` — create it **before** the text so the text sits on top; set `h` from the text height (`addText` first off-slide, or estimate 2 lines = 121 at 60px).

### `insight` — dark quote slide · measured

| Element | 4x5 | X | Story |
|---|---|---|---|
| Background | Stars | Stars | Stars |
| Asteroids | TopLeft −188,0 · BottomRight 758,985 | TopLeft −104,46 · BottomRight 1048,800 | TopLeft −139,272 · BottomRight 807,1257 |
| Title (short label, see budgets), BS Text Bold 130, lh 101, white, centred | x 29, w 929, y 102 | x 120, w 1060, y 200 | x 75, w 929, y 417 |
| `QuoteBox` (layer `Quote`, BS Text Bold, written as two lines with a hand break) | 27,268 · 945×292 · quote 60 | 118,420 · resize 1064 wide · **quote 70** · height `max(320, quote + 170)` | 67,583 · 945×292 · quote 60 |
| Body (optional, ≤ 20 words), Archivo 40 white, centred | x 57, w 885, y = box bottom + 60, ends ≤ 960 | none | x 97, w 885, y = box bottom + 60, ends ≤ 1240 |
| Footer | `Footer/Cover` 400,996 | none | `Footer/Cover` 440,1268 |

On X set the size after the text: `setText(qb, 'Quote', '…').fontSize = 70` (a 60 quote sat small in the 1064 box; tested at 70: two lines, box 320). A three-line quote: grow the box (`qb.resize(qb.width, Math.max(292, Math.round(quote.height + 170)))`, tested; X `Math.max(320, …)`); the marks follow the corners. No arrow (none on his dark slides). Footer: `Footer/Cover` as it comes — Verde wordmark, white URL, the dark-slide look; don't switch it. On X, hide the orbit line of the star background.

### `cta` — purple call to action · measured

| Element | 4x5 | X | Story |
|---|---|---|---|
| Background / asteroids | Lila · TopLeft −115,−63 · BottomRight 752,858 | Lila · TopLeft −103,−79 · BottomRight 1048,800 | Lila · TopLeft −100,304 · BottomRight 843,1261 |
| Question, BS Text Regular 80 white, centred | x 40, w 920, y 249 | BS Text Bold 100, x 68, w 1164, y 300 | x 80, w 920, y 616 |
| Bold line, BS Text Bold 80 white, centred | x 40, w 920, y 466 | BS Text Regular 120, centred, y = question bottom + 30 | x 80, w 920, y 833 |
| `Button/CTA` (`Label`, uppercase) | 64,645 | 210, y = bold line bottom + 50 | 100,1012 |
| Footer | `Footer/Cover` 400,1016 | none | `Footer/Cover` 415,1383 |

Story top-left asteroid: **−100,304 on `cta` and `cierre`** (his story closing slide `1:14121`), **−137,304 on the purple cover** (his story cover). Both are measured; the 37 px difference is his, not a typo.

### `cierre` — closing · measured

| Element | 4x5 | X | Story |
|---|---|---|---|
| Background / asteroids | as `cta` | as `cta` | as `cta` |
| Text, BS Text 80 white, centred: "Si te ha gustado este post,\n**¡dale a me gusta y compártelo!**" | x 42, w 915, y 381 | size 100, **x 40, w 1220**, y 330 (two lines, 240 tall; the old 1104 box left "compártelo!" alone) | x 82, w 915, y 748 |
| Reactions strip (rectangle 644×129, radius 40, `REACTIONS_HASH`) | 178,625 | 328, y = text bottom + 50 | 218,992 |
| Footer | `Footer/Cover` 400,1016 | none | `Footer/Cover` 415,1383 |

No arrow. If the post is in English, translate the line.

## Single image (`1-placa`) · derived from his single images on page "JCG"

One composed slide per size, grey, no arrow, with footer (`Footer/Content`: 4x5 30,1112 · X 30,942 · story 82,1442).

| Zone | 4x5 | X | Story |
|---|---|---|---|
| Title (`Info/TitleHighlight`, centred; hide `Subtitle` unless needed — on X set it to `fontSize` 40 or hide it, 36 is under the X floor) | y 50 | y 40 | y 300 |
| Visual zone | y 330 → 1032 | y 290 → 882 | y 580 → 1362 |

**One headline, one visual, at most one short supporting line** (≤ 12 words). Nothing else: no body paragraph, no second visual. The zone ends 80 above the footer (X: 60). **Fill the zone** (Juan, 2026-10-26: "too many open spaces"): grow the visual within the sizes below and put its bottom at the zone end; any leftover room goes between the title and the visual, never under it (audit: empty strip ≤ 130, X 120). The single image's title keeps his Lila highlighter (`Info/TitleHighlight`); the Verde one is for infographics.

Patterns for the visual zone:

- **Chart:** `Chart/Bar` detached and rescaled to the zone (4x5 ×1.2 → 868×624; X ×1.1 → 795×572; story ×1.3 → 940×676), centred across, bottom at the zone end. Its labels carry the words; a supporting line, if any, is the stat line below it (60 under the chart, chart scaled down to leave room).
- **Comparison** (his "Lo que te cuentan / La realidad"; built in all three sizes in the first test run and it looked right):

| | 4x5 | X | Story |
|---|---|---|---|
| Columns (x, w) | 40 and 520, w 440 | 67 and 680, w 553 | 40 and 560, w 480 |
| Heading | BS Text Bold 60 black, one line ≤ 18 characters, centred in its column | same | same |
| Highlighter behind the heading | JCG/Lila rectangle, width = heading text width + 24, height = the lower 60% of the heading (43 of 72), created first so it sits behind | same | same |
| Amount | Archimoto Regular 180 Lila outline, centred in the column, y = heading bottom + 30 ("€100" is 416 wide; wider than the column → 150) | same | same |
| Column text (optional) | Archivo 40, centred, **one line ≤ 20 characters**, y = amount bottom − 15 | Archivo 50 | Archivo 40 |
| Conclusion (the one supporting line) | BS Text Bold 50 black, one line ≤ 26 characters, centred on a Verde rectangle (text + 40 wide, text + 12 tall) at column text (or amount) bottom + 60 — the only Verde on the slide | same | same |
| Whole block | conclusion ending at the zone end (4x5 1032, X 882, story 1362); spread leftover room evenly between title → headings and amount → conclusion (first test: headings y 462 → conclusion ends 949, a 163 px strip — too much under the new rule) | same | same |

  A column can hold a picture card (column width, ≤ 300 tall) instead of the amount. Title budget for every `placa`: ≤ 28 characters, two lines on 4x5/story (`Line 1` / `Line 2`), one line at 90 on X.
- **Quote card:** Lila rectangle radius 20, named `Quote card` (his measured look; the one shape exempt from the purple-share check), Archimoto Bold 120 black label inside ("#1"), Archivo 50 black text with bold phrases (≤ 20 words), 70 in from the card's left edge.
- **Stat:** Archimoto Regular Lila number centred (250, grown up to 400 to fill the zone), one BS Text Bold 60 black line under it (the supporting line). No body under it.

Quote card and stat positions — X and story are **derived, not yet built** (check them on the screenshot); 4x5 card size is from his single images:

| | 4x5 | X | Story |
|---|---|---|---|
| Quote card | x 30, w 940, ≈ 500 tall | x 54, w 1192, ≈ 460 tall | x 70, w 940, ≈ 500 tall |
| Inside the card | label at card x + 70, card y + 50 · text x = card x + 70, w = card w − 140, y = label bottom + 30 · card height = text bottom + 60 − card y | same, text Archivo 50 | same, text Archivo 50 |
| Stat number | Archimoto Regular 250 Lila, centred | Archimoto Regular **220** (the zone is 592 tall) | Archimoto Regular 250 |
| Stat line, one line ≤ 12 words | BS Text Bold 60, x 40, w 920, centred, y = number bottom + 40 | BS Text Bold 70, x 54, w 1192 | BS Text Bold 60, x 80, w 920 |
| Vertical position | card or stack ending at the zone end, 1032 (zone y 330 → 1032) | ending at 882 (zone 290 → 882) | ending at 1362 (zone 580 → 1362) |

## Infographic (`1-infografia`) · Juan's pick 2026-10-26: variant B, with the bottom gap fixed

Use the three reference pictures in `img/` for structure only. **The look** (variant B on the variants page; the 4x5 hub was rebuilt with the fix as "Infografía B (arreglada)" and audited clean): Gris background · white group cards `Info/GroupCard/White` with a thin Lila top edge and a black Big Shoulders heading · Lila Archimoto numerals (Regular 80, recipe 5 with `center: true`) — 1., 2., 3. in reading order; a decision tree numbers by level · the title `Info/TitleHighlight/Verde`, black, its second line on a Verde block · a white hub `Info/HubCircle` with a Lila outline and black text · black 3 px connectors (recipe 8) · his normal avatar footer bottom-left (`Footer/Content`), **no purple band**. Purple stays an accent (`style.md` → Purple is an accent): no purple card headers, no purple hub, no purple band. The old purple-strip cards, Lila title highlight and footer band are the old look (`blocks.md`). **Icons: none by default** — the numerals carry the groups. Only if Juan asks, reuse his 3D-emoji images already in the file (by image hash, recipe 7); never an icon library or drawn icons.

**Budgets** (measured Archivo Regular ≈ 16.4 px per character at 36, 17.3 at 38, 19.6 at 40 on average):

- **Groups:** **3 preferred, 4 at most** (hub, mind map). Decision tree: one question + two answers (3 cards) by default; at most one more level below the answers (two outcomes, 5 cards), never deeper. More points → propose a carousel.
- **Lines:** at most **2 lines per group**, each at most **16 characters** including "• " ("• Revisa el CPM" ✓, "• Revisa el CPM cada semana" ✗). **Bullets only for 2 lines:** a group with a single line (often the decision-tree root's context line) writes it plain — "en paid media", not "• en paid media".
- **Group heading:** at most **11 characters**, one line. The heading box is the card width minus 131 (padding, numeral and gap): 229 px on a 360 card, ≈ 11 characters of Big Shoulders Bold 50 ("Devoluciones", 12, wrapped in the test). Decision-tree root question: at most 22 characters; on X it wraps onto two heading lines, so put the natural break near the middle and keep symbols glued to their number ("¿Más de $10K/mes?" ✓; "¿Inviertes +$10K/mes?" broke after the "+").
- **Title:** **at most 5 words and 28 characters**: two lines on 4x5 and story, one highlighted line on X. A 5-card decision tree: at most 21 characters (one line on story, see there).
- **Subtitle:** only if essential, 4x5 only (use the 1000×1500 frame). Hide it on X (Archivo 36 is under the X floor) and story.

**Text sizes and measured card heights** (2026-10-26, one-line heading; set with `.fontSize` overrides, recipe 8):

| | 4x5 | X | Story |
|---|---|---|---|
| Heading / lines | BS Bold 50 / Archivo 36 | BS Bold 50 / Archivo 40 | BS Bold 50 / Archivo 38 |
| Card height, 1 / 2 lines | 188 / 238 | 193 / 248 (a two-line question + one line: 253) | 191 / 244 |
| Minimum card width (16 characters fit) | 330 | 380 | 345 |

**Title, footer and the zone to fill:**

| | 4x5 · 1000×1250 | 4x5 · 1000×1500 | X · 1300×1080 | Story · 1080×1920 |
|---|---|---|---|---|
| Title (`Info/TitleHighlight/Verde`, centred, `Subtitle` hidden) | y 40, two lines (230 tall, ends 270) | y 40, ends 270 (with a subtitle: 317) | y 30, one line: hide `Line 1`, whole title in `Line 2` at `fontSize` 90 (ends 121) | y 250, two lines (ends 480; one line ends 361) |
| Footer (`Footer/Content`, no arrow) | 30,1112 | 30,1362 | 30,942 | 82,1442 |
| Zone: first row → last card's bottom | 340 → 1032 | 340 → 1282 (with a subtitle: 387 → 1282) | 190 → 882 | 550 → 1362 |

**Fill the zone** (Juan, 2026-10-26: variant B left an empty strip above the footer). The first row starts 70 under the title (X 69; at least 60). The last card ends at the content end, 80 above the footer (X 60). The rows in between spread evenly, and the hub, pills and connectors sit in the gaps. The audit allows at most 130 (X 120) between the last card and the footer. Positions below assume 2-line cards (1-line roots on the trees). With 1-line cards, keep the first row and move the last row down so it still ends at the content end. Never fill with extra lines or groups.

### Hub — centre idea + groups around it (`img/infographic-ref-hub.webp`)

Centre: `Info/HubCircle`, resized to the diameter below, text in `Hub text` (max 2 lines). Groups clockwise from top-left; a spoke from each card to the circle edge, arrowhead at the circle (recipe 8).

| | 4x5 · 1000×1250 | X | Story |
|---|---|---|---|
| Card width | 360 (3 groups: bottom card 400) | 460 | 360 (3 groups: bottom card 400) |
| 3 groups (x,y) | 40,340 · 600,340 · 300,794 | left column 40,190 · 40,634 · right card 800,412 | 80,550 · 640,550 · 340,1118 |
| 3 groups: hub | Ø 160 (text 38), centre 500,660 | Ø 220 (text 40), centre 650,536 | Ø 200 (text 40), centre 540,956 |
| 4 groups (x,y) | 40,340 · 600,340 · 600,794 · 40,794 | 40,190 · 800,190 · 800,634 · 40,634 | 80,550 · 640,550 · 640,1118 · 80,1118 |
| 4 groups: hub | Ø 160, centre 500,686 | Ø 220, centre 650,536 | Ø 200, centre 540,956 |
| Title → cards / last card → footer | 70 / 80 | 69 / 60 | 70 / 80 |
| Hub ↔ cards (min 40) | 3 groups: 49 to the top cards, 54 to the bottom one · 4 groups: 67 | 69 to the corners, 40 to the right card | 90 · bottom card 62 |
| Status | 3 groups **built and audited** 2026-10-26 ("Infografía B (arreglada)": strip above the footer 80, purple 1.2%) | derived | derived |

- **Where the circle goes.** On 4x5 and story the gap between the two top cards (200) is too narrow for the circle, so it sits under them: its centre is far enough below their inner corners to leave 40 px (`√(100² + lift²) ≥ Ø/2 + 40`), and the bottom card starts at least 40 under the circle. On X the gutter between the columns is 300 wide and the circle sits in it, 40 from the cards on each side.
- **Spokes** (recipe 8): a card that the circle's centre line crosses gets a straight spoke from the middle of its facing edge (the bottom card on 4x5/story, the right card on X); the others go from their inner corner.
- **With a subtitle** (4x5 only): the 1000×1500 frame; first row at 387, last row ending at 1282, the hub in the middle of the gap.

Centre-idea budget (Big Shoulders Bold ≈ 16.5 px per character at 40): 1–3 words; the longest word must fit the smallest circle you use.

| Circle | Text size | Longest word |
|---|---|---|
| Ø 160 | 38 | 8 characters |
| Ø 200 | 40 | 10 characters ("Rentabilidad", 12, breaks mid-word) |
| Ø 220 | 40 | 11 characters |

So with the same words in every size (4x5 uses Ø 160): **no word over 8 characters** in the centre.

### Decision tree — question → yes/no answers (`img/infographic-ref-decision-tree.webp`) · derived in the new look

Root = `Info/GroupCard/White` (heading = the question, one plain context line with no bullet). Answers = cards with ≤ 2 lines. Outcomes ("qué hacer", ≤ 2 lines) — **only when the answers need a next step; never a third level.** Every card is white; the level shows in the numeral: root "1.", both answers "2.", both outcomes "3.". `Pill/Yes` (Verde) on the left/top answer, `Pill/No` (Lila) on the right/bottom one.

LinkedIn frame: **1000×1250 for 3 cards**, **1000×1500 for 5 cards**.

**4x5 and story, top → down:**

| | 4x5 · 3 cards | 4x5 · 5 cards (1500) | Story · 3 cards | Story · 5 cards (one-line title, ends 361) |
|---|---|---|---|---|
| Card widths | root 600 · answers and outcomes 410 | same | root 600 · others 460 | same |
| Root (1 line: 188 / 191 tall) | 200,340 | 200,340 | 240,550 | 240,431 |
| Answers (4x5 x 50 and 540 · story x 40 and 580) | y 794 | y 667 | y 1118 | y 748 |
| Outcomes, under each answer | — | y 1044 | — | y 1118 |
| Gap root → answers / answers → outcomes | 266 | 139 / 139 | 377 | 126 / 126 |
| Split line (root bottom + half the first gap) | y 661 | y 598 | y 930 | y 685 |
| Pills (y = split − 34) | Yes x 328 · No x 566, y 627 | same x, y 564 | Yes x 355 · No x 618, y 896 | same x, y 651 |
| Title → root / last card → footer | 70 / 80 | 70 / 80 | 70 / 80 | 70 / 80 |

Split connector (arrowhead at the end): root bottom-centre (4x5 500 · story 540) → down to the split line → across → down into each answer's top-centre (4x5 255 / 745 · story 270 / 810). Answer → outcome: straight down from the answer's bottom-centre. Every pill sits at least 29 px clear of the cards.

**X, left → right** (all cards 380; root = two-line question + one line, 253 tall):

| | X · 3 cards | X · 5 cards |
|---|---|---|
| Columns (x) | root 238 · answers 683 | root 25 · answers 460 · outcomes 895 |
| Root | y 410 (centred on 536) | same |
| Answers (and outcomes, same y as their answer) | upper y 190, lower y 634 | same |
| Root → answers | from the root's top-centre up to the upper answer's mid-height (y 314), then right into its left edge; from the bottom-centre down to y 758, then right | same (root centre x 215) |
| Pills, on those horizontal legs | Yes 506,280 · No 499,724 | Yes 288,280 · No 281,724 |
| Answer → outcome | — | straight right, 55 long, at each answer's mid-height (840 → 895) |
| Title → cards / last card → footer | 69 / 60 | 69 / 60 |

The pills ride on the legs above and below the root, 61–62 px clear of it.

### Mind map — title + branches (`img/infographic-ref-mindmap.webp`) · derived in the new look

The title is `Info/TitleHighlight/Verde`, as on the hub (the old Lila `Title block` is the old look: a near-full-width purple band). The spine starts 15 under the title's bottom-centre.

**4 groups:** four cards in a 2×2 grid, numbered 1–2 on the first row and 3–4 on the second. One spine runs down the middle gutter to the second row's mid-height, with no arrowhead. Four short stubs with arrowheads go from the spine into each card's inner edge, at that card's mid-height (`Math.round(card y + card height / 2)`).

**3 groups:** two cards on the first row as in the 2×2 grid, the third centred under them. The spine runs straight into the third card's top-centre (arrowhead there); two stubs go from the spine into the first-row cards at their mid-height.

| | 4x5 · 1000×1250 | X | Story |
|---|---|---|---|
| Cards (w) | 430 at x 30 and 540 | 580 at x 30 and 690 | 460 at x 40 and 580 |
| Rows (y) | 340 and 794 | 190 and 634 | 550 and 1118 |
| 3 groups: third card | 430 at x 285, y 794 | 580 at x 360, y 634 | 460 at x 310, y 1118 |
| Spine, 3 groups (arrowhead into the third card's top) | x 500, 285 → 794 | x 650, 136 → 634 | x 540, 495 → 1118 |
| Spine, 4 groups (no arrowhead) | x 500, 285 → 913 (row 2 mid-height) | x 650, 136 → 758 | x 540, 495 → 1240 |
| Stubs into row 1 (mid-height of 2-line cards) | y 459: 500 → 460 and 500 → 540 | y 314: 650 → 610 and 650 → 690 | y 672: 540 → 500 and 540 → 580 |
| Stubs into row 2 (4 groups) | y 913, same x | y 758, same x | y 1240, same x |
| Title → row 1 / last row → footer | 70 / 80 | 69 / 60 | 70 / 80 |

