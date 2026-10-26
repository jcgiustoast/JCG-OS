# Layouts — what goes where, per slide kind and size

updated: 2026-10-26

Coordinates are x,y inside the frame. Block names → IDs in `blocks.md` (and the `B` table in `figma-recipes.md`). "Measured" = copied from his slides; "derived" = my layout in his grid, not in his file — check it on the screenshot.

Frames are named `<n>-<kind>`. Kinds: `portada`, `punto`, `grafico`, `imagen`, `insight`, `cta`, `cierre` (carousel) · `placa` (single image) · `infografia` (infographic).

## Carousel

### Shape of a carousel

- Always: `portada` first, `cierre` last. `cta` before `cierre` only when the post has an offer or a "write me" ask.
- Cover look: **dark (stars) by default.** Purple when the headline leads with a number or a list ("10 estrategias…", "5 errores…").
- Middle: one slide per point. `punto` by default; `grafico` when the point is a before/after number; `imagen` when the point is a screenshot or picture; one `insight` around the middle for the key idea (a quote from the post).
- Numerals count the points in order (`punto` and `grafico` slides): 1., 2., 3. … `imagen`, `insight`, `cta` and `cierre` have none.
- Background per kind (the `bg` in recipe 3): `portada` → `stars` (dark) or `lila` (purple) · `punto`, `grafico`, `imagen` → `gris` · `insight` → `stars` · `cta`, `cierre` → `lila`.
- Arrows, as in his file: black arrow bottom-right on the grey slides (`punto`, `grafico`, `imagen`) of 4x5 and story; Verde arrow top-right on a purple cover. None on dark slides, `cta` or `cierre`, and none anywhere on X.
- Picture cards with no picture yet: full content width (4x5 886, X 1000 centred, story 842 centred), height = the room left above the content limit, at most 500 (X 560).
- 5 slides: `1-portada` · `2-punto` · `3-grafico` · `4-insight` · `5-cierre`. 6–10 slides: add points.

### Word budgets (fit the text in the outline, not in Figma)

| Kind | 4x5 / story | X |
|---|---|---|
| Slide title | ≤ 28 characters (one line) | ≤ 24 characters |
| `punto` body with a picture | ≤ 45 words, 2 short paragraphs | ≤ 30 words |
| `punto` body, text only | ≤ 100 words; body size by word count ("Text-only point" below) | ≤ 70 words |
| Highlight box (text-only point under 45 words) | one line, ≤ 6 words / 32 characters | same |
| `grafico` body | ≤ 30 words | ≤ 9 words and ≤ 58 characters — one line (measured: 59 characters = 1068 px at Archivo 40 in the 1173 box) |
| Insight title | a short label ≤ 16 characters ("Insight Clave", "La clave", "Ojo con esto"; Big Shoulders Bold 130 is ≈ 51 px a character, so 18 would fill the 929 box) | same |
| Insight quote / body | ≤ 14 words, two lines with a hand break / ≤ 40 words | ≤ 14 words / none |
| Cover | Archimoto phrase 2–3 words + headline ≤ 6 words | same |
| CTA | question ≤ 14 words + one bold line ≤ 6 words + button ≤ 20 characters | same |

The same words go on all three sizes, except X drops the insight body and trims long bodies (say so in the outline).

### Big text: never one word alone on the last line

Any text at 60 px or more (cover headline, insight title and quote, CTA and closing lines, statement and highlight boxes, single-image headings) must not end with a single word on its last line (e.g. "**creces**" alone under "…por qué no").
- **In the outline**, show the break of every headline, quote, closing line and box line as a real line break, the same break in all three sizes:
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

**Dark cover without a picture** (derived, tested twice): headline Big Shoulders Text 130 (X 120), **Regular with the key words Bold** (the outline's `**…**`), lh 101, white, centred, with its hand break (see "Big text"); Archimoto phrase 10 above it; centre the whole stack vertically in the band below, keeping the same asteroids, sunburst and footer:

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

### `punto` — numbered point (grey) · measured

| Element | 4x5 | X | Story |
|---|---|---|---|
| Header | `Header/Numbered` 55,33 · `Title` Lila 60 · numeral Regular 150 | `Header/Numbered` 67,48 · `Title` black 90 · numeral **Bold** 150 | `Header/Numbered` 107,363 |
| Body (`addText`) | x 60, w 885, y 200, Archivo 35 | x 67, w 1173, y 242, Archivo 40, lh 158 | x 112, w 885, y 518, Archivo 35 |
| Picture (`Card/Image`) | x 59, w 886, y = body bottom + 40, ends ≤ 1080 | centred, w ≤ 1194, y = body bottom + 40, ends ≤ 1020 | centred, w 842, y = body bottom + 40, ends ≤ 1420 |
| Footer | `Footer/Content` 30,1112 | none | `Footer/Content` 82,1442 |
| Arrow | `Arrow` Negro 849,1121 | none | Negro 901,1451 |

A two-line title (over the budget) pushes the body down 70.

### Text-only point (no picture) · derived, tested 2026-10-26

Rule: **no more than 35% of the content area may stay empty** (the area runs from where the body starts to the content limit: 4x5 y 200 → 1080, X 242 → 1020, story 518 → 1420). His own text-only slides use a bigger body (his LTV series: Archivo 50–60), so grow the body first, then add a highlight box if it is still short.

Pick the body size from the word count (measured with 30, 46, 75 and 102-word bodies; empty share in brackets):

| Body words | 4x5 / story | X |
|---|---|---|
| 85–100 | Archivo 35, lh 133.5 (102 words: 18% / 20%) | — (X budget is 70) |
| 70–84 | Archivo 40, lh 133.5 (75 words: 24% / 26%) | Archivo 40, lh 158 |
| 55–69 | Archivo 45, lh 133.5 | Archivo 40, lh 158 (75 words: 8%) |
| 45–54 | Archivo 50, lh 133.5 (46 words: 33% / 34%) | Archivo 50, lh 133.5 (46 words: 33%) |
| under 45 | Archivo 50 **plus a highlight box** (30 words + box: 21% / 22%) | Archivo 50 plus a highlight box (30 words + box: 21%) |

- Paragraph gap stays 28. Positions stay as in the table above (4x5 x 60 w 885 y 200 · X x 67 w 1173 y 242 · story x 112 w 885 y 518).
- **Highlight box** (style.md → highlight box): the key line or number of the point, one line ≤ 6 words, Big Shoulders Display Bold black, centred — 60 on 4x5/story, 70 on X. Box = body width (4x5 x 60 w 885 · X x 67 w 1173 · story x 112 w 885), height = text + 70, **centred in the free room between the body's bottom and the content limit** (recipe `highlightBox`, figma-recipes §4).
- Same body size on all three sizes when the word count allows it; the audit's empty-room check (figma-recipes §9) is the final judge — if it still flags a slide, step the body up once more (never past 50) or add the box.

### `grafico` — point with a bar chart · derived from his chart slide

Same header, footer and arrow as `punto`. Body first, then `Chart/Bar` (detach + `setBars`, recipe 6):

| | 4x5 | X | Story |
|---|---|---|---|
| Body | x 60, w 885, y 200 (≤ 30 words) | x 67, w 1173, y 242, one line | x 112, w 885, y 518 |
| Chart | 723×520, x 138, y = body bottom + 40, ends ≤ 1080 | ×1.25 → 904×650, x 198, y = body bottom + 40, ends ≤ 1020 | 723×520, x 178, y = body bottom + 40, ends ≤ 1420 |

### `imagen` — picture slide with a statement box (grey) · derived

Positions copied from his "Las plataformas no pueden distinguir correlación de causación" slide in all three sizes; box heights and the picture card are derived. The box is the **statement box** from `style.md` (Lila 34%, radius 24, no stroke) — not the 46% stroked highlight box.

| Element | 4x5 | X | Story |
|---|---|---|---|
| Statement box (rectangle, JCG/Lila, opacity 0.34, radius 24, no stroke) | 30,129, 929 × (text + 60) | 61,72, 1178 × (text + 110) | 70,322, 929 × (text + 60) |
| Text in the box, BS Text Bold 60 black, lh 101, centred | x 60, w 869, vertically centred in the box | BS Text Bold 80, x 104, w 1092 | x 100, w 869 |
| Picture (`Card/Image`, radius stays 20) | 929 wide at 30, y = box bottom + 40, ends ≤ 1080 | 969 wide at 165, y = box bottom + 30, ends ≤ 1020 | 929 wide at 70, y = box bottom + 40, ends ≤ 1420 |
| Footer / arrow | as `punto` | none | as `punto` |

Box: `const r = figma.createRectangle(); slide.appendChild(r); r.resize(929, h); r.x = 30; r.y = 129; r.cornerRadius = 24; await r.setFillStyleIdAsync(S.lila); r.opacity = 0.34;` — create it **before** the text so the text sits on top; set `h` from the text height (`addText` first off-slide, or estimate 2 lines = 121 at 60px).

### `insight` — dark quote slide · measured

| Element | 4x5 | X | Story |
|---|---|---|---|
| Background | Stars | Stars | Stars |
| Asteroids | TopLeft −188,0 · BottomRight 758,985 | TopLeft −104,46 · BottomRight 1048,800 | TopLeft −139,272 · BottomRight 807,1257 |
| Title (short label, see budgets), BS Text Bold 130, lh 101, white, centred | x 29, w 929, y 102 | x 120, w 1060, y 200 | x 75, w 929, y 417 |
| `QuoteBox` (layer `Quote`, BS Text Bold, written as two lines with a hand break) | 27,268 · 945×292 · quote 60 | 118,420 · resize 1064 wide · **quote 70** · height `max(320, quote + 170)` | 67,583 · 945×292 · quote 60 |
| Body, Archivo 35 white, centred | x 57, w 885, y = box bottom + 50, ends ≤ 960 | none | x 97, w 885, y = box bottom + 50, ends ≤ 1240 |
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
| Visual zone | y 330 → 1080 | y 290 → 910 | y 580 → 1420 |

Patterns for the visual zone:

- **Chart:** `Chart/Bar` detached and rescaled to the zone (4x5 ×1.2 → 868×624; X ×1.2; story ×1.3), centred.
- **Comparison** (his "Lo que te cuentan / La realidad"; built in all three sizes in the first test run and it looked right):

| | 4x5 | X | Story |
|---|---|---|---|
| Columns (x, w) | 40 and 520, w 440 | 67 and 680, w 553 | 40 and 560, w 480 |
| Heading | BS Text Bold 60 black, one line ≤ 18 characters, centred in its column | same | same |
| Highlighter behind the heading | JCG/Lila rectangle, width = heading text width + 24, height = the lower 60% of the heading (43 of 72), created first so it sits behind | same | same |
| Amount | Archimoto Regular 180 Lila outline, centred in the column, y = heading bottom + 30 ("€100" is 416 wide; wider than the column → 150) | same | same |
| Column text | Archivo 35, centred, two lines with a hand break, y = amount bottom − 15 | Archivo 40 | Archivo 35 |
| Conclusion | BS Text Bold 50 black, one line ≤ 26 characters, centred on a Verde rectangle (text + 40 wide, text + 12 tall) at column text bottom + 54 — the only Verde on the slide | same | same |
| Whole block | centred vertically in the visual zone (4x5 test: headings y 462 → conclusion ends 949) | same | same |

  A column can hold a picture card (column width, ≤ 300 tall) instead of the amount. Title budget for every `placa`: ≤ 28 characters, two lines on 4x5/story (`Line 1` / `Line 2`), one line at 90 on X.
- **Quote card:** Lila rectangle radius 20, Archimoto Bold 120 black label inside ("#1"), Archivo 50 black text with bold phrases, 70 in from the card's left edge.
- **Stat:** Archimoto Regular 250 Lila number centred, a BS Text Bold 60 black line under it, Archivo body under that.

Quote card and stat positions — X and story are **derived, not yet built** (check them on the screenshot); 4x5 card size is from his single images:

| | 4x5 | X | Story |
|---|---|---|---|
| Quote card | x 30, w 940, ≈ 500 tall | x 54, w 1192, ≈ 460 tall | x 70, w 940, ≈ 500 tall |
| Inside the card | label at card x + 70, card y + 50 · text x = card x + 70, w = card w − 140, y = label bottom + 30 · card height = text bottom + 60 − card y | same, text Archivo 50 | same, text Archivo 50 |
| Stat number | Archimoto Regular 250 Lila, centred | Archimoto Regular **220** (the zone is 620 tall) | Archimoto Regular 250 |
| Stat line, one line | BS Text Bold 60, x 40, w 920, centred, y = number bottom + 30 | BS Text Bold 70, x 54, w 1192 | BS Text Bold 60, x 80, w 920 |
| Stat body, centred, ≤ 2 lines | Archivo 35, x 57, w 885, y = line bottom + 30 | Archivo 40, x 54, w 1192 | Archivo 35, x 97, w 885 |
| Vertical position | card or stack centred in the visual zone (y 330 → 1080) | centred in y 290 → 910 | centred in y 580 → 1420 |

## Infographic (`1-infografia`) · derived

Use the three reference pictures in `img/` for structure only; colours stay purple + grey. Background Gris. Groups are `Info/GroupCard` (Tone Lila → Light → Deep, then repeat), each with its numeral swapped in (recipe 5, `center: true`) — 1., 2., 3. in reading order; a decision tree numbers by level instead (see there). Connectors: recipe 8, black 3px. **Icons: none by default** — the numbered badges carry the groups. Only if Juan asks, reuse his 3D-emoji images already in the file (by image hash, recipe 7); never an icon library or drawn icons.

**Budgets (measured 2026-10-26, Archivo Regular: ≈ 14.6 px per character at 32 on average, up to 15.7; 17.2 at 35; 19.6 at 40):**

- **Lines:** at most **16 characters** including "• " (2–3 words: "• Revisa el CPM" ✓, "• Revisa el CPM cada semana" ✗ = 424 px). At most **3 lines per group**, on every layout and size. **Bullets only for 2–3 lines:** a group with a single line (often the decision-tree root's context line) writes it plain — "en paid media", not "• en paid media".
- **Group heading:** at most **11 characters**, one line (the heading box is the card width minus 146; at width 370 on X that's 224 px ≈ 11 characters of Big Shoulders Bold 50). Decision-tree root question: at most 22 characters; on X it wraps onto two heading lines of about 11 characters each, so put the natural break near the middle and keep symbols glued to their number ("¿Más de $10K/mes?" ✓; "¿Inviertes +$10K/mes?" broke after the "+").
- **Groups:** 3 or 4 (hub, mind map); a decision tree is exactly 1 question + 2 branches + 2 outcomes. More points → propose a carousel.
- **Title:** hub and mind map — at most **28 characters in total**: split into two lines on 4x5/story, one highlighted line on X (28 characters at 90 ≈ 1000 px; measured 31 characters = 1349 px at 110, ≈ 43.5 px each). Decision tree — one highlighted line everywhere, so at most **21 characters** (fits 1000 wide at 110).
- **Subtitle:** avoid. If Juan wants one, it goes on the 4x5 version only (hub → 1000×1500 frame; decision tree → shift everything down 63). Hide it on X (Archivo 36 is under the X floor) and story.

**Text sizes and measured card heights** (one-line heading; height for 1 / 2 / 3 lines). Set them with `.fontSize` overrides (recipe 8):

| | 4x5 | X | Story |
|---|---|---|---|
| Heading / lines | BS Bold 46 / Archivo 32 | BS Bold **50** / Archivo **40** | BS Bold 46 / Archivo 35 |
| Card height, 1 / 2 / 3 lines | 207 / 262 / 317 | 217 / 282 / 347 | 211 / 270 / 329 |
| Minimum card width (16 characters fit) | 310 | 370 | 335 |

Positions below assume 3-line cards; shorter cards keep the same top-left position.

**Title, band and content zone:**

| | 4x5 · 1000×1250 | 4x5 · 1000×1500 | X · 1300×1080 | Story · 1080×1920 |
|---|---|---|---|---|
| Title (`Info/TitleHighlight`, centred) | y 40, two lines (230 tall) | y 40 | y 30, one line: hide `Line 1`, whole title in `Line 2` at `fontSize` 90 (90 tall) | y 250, two lines (230 tall) |
| Footer band (`Info/FooterBand`) | 0,1110 | 0,1360 | 0,940 | 0,1440 (ends 1580, inside the story safe zone) |
| Content zone (QA limit = band top − 10) | y 300 → 1100 | y 300 → 1350 | y 160 → 930 | y 510 → 1430 |

**Fill the infographic down to the band:** the lowest card must end **within 120 px of the footer band** (QA checks it; the first decision tree left 169 px of empty grey). The positions below already do this for 3-line cards. With shorter cards, or a 1000×1500 frame, spread the rows: pin the lowest row to end about 40 above the band (band top − 40 − card height) and share the remaining space evenly between the gaps — never closer than the gaps in the tables.

### Hub — centre idea + groups around it (`img/infographic-ref-hub.webp`) · derived, tested 2026-10-26

Centre: Lila circle with the idea in Big Shoulders Text Bold white, centred, text box = circle Ø − 30, max 2 lines. Groups clockwise from top-left; a spoke from each card's inner corner to the circle edge, arrowhead at the circle (recipe 8).

| | 4x5 · 1000×1250 | 4x5 · 1000×1500 (with subtitle) | X | Story |
|---|---|---|---|---|
| Card width | 400 | 400 | 460 | 470 |
| 4 groups (x,y) | 30,300 · 570,300 · 570,783 · 30,783 | 30,360 · 570,360 · 570,1033 · 30,1033 | 40,160 · 800,160 · 800,583 · 40,583 | 40,510 · 570,510 · 570,1101 · 40,1101 |
| 4 groups: circle | Ø 200, centre 500,700 | Ø 300, centre 500,855 | Ø 280, centre 650,545 | Ø 240, centre 540,970 |
| 3 groups (x,y · width) | 30,300 · 590,300 (both **w 380**) · 300,783 (w 400) | 30,360 · 570,360 · 300,1033 (w 400) | 40,160 · 40,583 · 800,371 (w 460) | 40,510 · 640,510 (both **w 400**) · 305,1101 (w 470) |
| 3 groups: circle | Ø 160, centre **500,675** | Ø 300, centre 500,855 | **Ø 240**, centre 650,545 | Ø 240, centre **540,950** |

**3 groups: keep a visible gap of at least 24 px between the circle and every card.** The old 4x5 numbers left 3 px between the circle and the third card. The fix narrows the two top cards so the circle can rise into the space between them. Tested 2026-10-26 in all three sizes: gaps 27 / 35 / 29 px (4x5 / X / story), audit clean. The spoke recipe (figma-recipes §8) gives the centred third card a straight spoke from the middle of its top edge (X: of its left edge).

Centre-idea budget (Big Shoulders Bold is ≈ 16.5 px per character at 40 for long words like "Conversión"): 1–3 words; the longest word must fit the smallest circle you use.

| Circle | Text size | Longest word |
|---|---|---|
| Ø 160 | 36 | 8 characters |
| Ø 200 | 40 | 10 characters ("Rentabilidad", 12, breaks mid-word) |
| Ø 240 | 40 | 12 characters (also the X 3-group circle) |
| Ø 280 / Ø 300 | 50 | 12 characters |

So with the same words in every size: 4 groups → no word over 10 characters; 3 groups → over 8.

### Decision tree — question → yes/no branches (`img/infographic-ref-decision-tree.webp`) · derived

Always 1000×1500 on LinkedIn. Root = `Info/GroupCard` Lila (heading = the question, one plain context line with no bullet). Branches = Light cards (next question or cause, ≤ 3 lines). Outcomes = Deep cards ("qué hacer", ≤ 3 lines). `Pill/Yes` on the left/top branch, `Pill/No` on the right/bottom one. **Numerals by level**, since a tree has no reading order: root "1.", both branches "2.", both outcomes "3." (reads as steps; tested).

On 4x5 and story the gap G between levels is computed so the tree reaches down to the band: `G = max(80, round((band − 40 − root y − root h − branch h − outcome h) / 2))`, heights from the card table above. With 3-line cards: 4x5 G = 145 (tree ends 1321, band 1360); story G = 80 (ends 1419, band 1440). The old fixed 80 left 169 px of empty grey on 4x5.

| | 4x5 · 1000×1500 (band 1360) | X, left → right (band 940) | Story (band 1440) |
|---|---|---|---|
| Card widths | root 600 · branches and outcomes 440 | **all 370** (the X minimum) | root 600 · others 470 |
| Root | 200,190 (1 line: 207 tall) | x 20, y = 545 − h/2 (question on 2 heading lines + 1 line = 245 tall → y 423) | 240,390 (211 tall) |
| Branches | x 40 and 520, y = root bottom + G | x 510; upper y 160, lower y = 930 − h (583 with 3 lines) | x 40 and 570, y = root bottom + G |
| Outcomes | under each branch, y = branch bottom + G | x 910, same y as its branch | under each branch, y = branch bottom + G |
| Split connector (arrowhead at the end) | root bottom-centre (500) → down G/2 → across → down into each branch's top-centre (260 / 740) | root right-middle (390) → right to x 450 → up/down to each branch's middle → into its left edge (510) | as 4x5 from x 540 to 275 / 805 |
| Pills | on the horizontal, y = split y − 34: Yes x 330 · No x 563 | on the vertical at x 450, **clear of the root**: Yes x 400, y = root top − 80 (ends 12 above the root) · No x 393, y = root bottom + 12 | Yes x 357 · No x 616, y = split y − 34 |
| Branch → outcome | straight down from each branch's bottom-centre (arrow) | straight right, 30 long: (880, branch middle) → (910, same) | as 4x5 |

X was rebuilt after the first test: with 386 cards the pills sat on the branches' number badges and the split stub was only 41 px wide. Pills beside the root ended 3 px from it, so they now sit above and below it on the split line. Tested 2026-10-26: X pills at 400,343 and 393,680 for a root at y 423–668; audit clean in all three sizes.

### Mind map — title block + branches (`img/infographic-ref-mindmap.webp`) · derived, tested 2026-10-26 (3 and 4 groups)

No `Info/TitleHighlight`: the title lives in a Lila block (rectangle radius 20, JCG/Lila) with Big Shoulders Text Bold 70 white, centred, vertically centred in the block (one line ≤ 28 characters, or two lines with a hand break on 4x5/story).

**4 groups** (tested 2026-10-26 in all three sizes, audit clean): four GroupCards in a 2×2 grid, numbered 1–2 on the first row and 3–4 on the second. One spine runs down the middle gutter from the block's bottom-centre to the second row's mid-height, with no arrowhead. Four short stubs with arrowheads go from the spine into each card's inner edge, at that card's mid-height (`Math.round(card y + card height / 2)`).

**3 groups** (tested 2026-10-26 in all three sizes, audit clean): two cards on the first row as in the 2×2 grid, the third centred under them. The spine runs from the block's bottom-centre straight into the third card's top-centre (arrowhead there); two stubs go from the spine into the first-row cards at their mid-height.

| | 4x5 · 1000×1250 | X | Story |
|---|---|---|---|
| Title block | 30,40 · 940×220 | 30,40 · 1240×110 (one line) | 40,250 · 1000×220 |
| Cards (w) | 440 at x 30 and 530 | 590 at x 30 and 680 | 470 at x 40 and 570 |
| Rows (y) | 300 and 720 | 190 and 575 | **575 and 1005** (the old 540 / 930 left 181 px empty above the band) |
| 3 groups: third card | 440 at x 280, y 720 | 590 at x 355, y 575 | 470 at x 305, y 1005 |
| Spine, 3 groups (arrowhead into the third card's top) | x 500, block bottom 260 → 720 | x 650, 150 → 575 | x 540, 470 → 1005 |
| Spine, 4 groups (no arrowhead) | x 500, 260 → 879 (row 2 mid-height) | x 650, 150 → 749 | x 540, 470 → 1170 |
| Stubs into row 1 (3 and 4 groups; mid-height of 3-line cards) | y 459: 500 → 470 and 500 → 530 | y 364: 650 → 620 and 650 → 680 | y 740: 540 → 510 and 540 → 570 |
| Stubs into row 2 (4 groups) | y 879: 500 → 470 and 500 → 530 | y 749: 650 → 620 and 650 → 680 | y 1170: 540 → 510 and 540 → 570 |
| Lowest card ends (3 lines) / band gap | 1037 / 73 | 922 / 18 | 1334 / 106 |
