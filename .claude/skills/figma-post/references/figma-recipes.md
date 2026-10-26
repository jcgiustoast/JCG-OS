# Figma recipes — tested `use_figma` code

updated: 2026-10-26

Every snippet below ran once in Contenido on 2026-10-26, on a scratch page that was then deleted. Copy them as they are and change only the `CAPITALS` constants and the content. Positions come from `layouts.md`; block IDs from `blocks.md`.

## 0. Rules for every call

- File: `U2HIUwTWDYWL7EwSKCDpLd` (Contenido). Pass `sessionId` from `create_session` (if the tool exists) and `skillNames: "resource:figma-use,resource:figma-generate-design"` on every `use_figma` call.
- **Switch page explicitly, once per call:** `await figma.setCurrentPageAsync(page)`. The starting page is not predictable (it was the last page used in testing). `figma.currentPage = …` throws.
- Nothing persists between calls: paste node IDs from earlier returns as string literals.
- Return IDs and small evidence only (well under 48 KB). Never list the "JCG" page (977 loose nodes).
- Not available: `figma.createImageAsync`, `figma.notify`, `figma.loadAllPagesAsync`. Images come from existing hashes or `upload_assets` (recipe 7).
- **Read-only** on page "JCG" (`0:1`), page "Carousel" (`1:13975`) and the components on `🧩 Bloques JCG` (`31:21`). Only `createInstance()` from blocks; never `clone()` his slides (a failed call would leave a copy on his page).
- One call per size row is a good unit (all slides of that size). If Archimoto SVGs push the code past ~45,000 characters, split by slide.
- **Hidden layers inside an instance disappear from searches.** `figma.skipInvisibleInstanceChildren` is on in this runtime, so after `x.visible = false` on an instance child, `findOne`/`findAll` no longer see it (and an old reference throws "node … does not exist"). Hide things last. To find or re-show a hidden one, first set `figma.skipInvisibleInstanceChildren = false;` in that call (tested).
- In testing, **a thrown error rolled back the whole call** (twice: nothing it created stayed). Still obey `safeToRetryWithoutCanvasRead`; when in doubt, read the frame before re-running.
- Removing a page that is the current page throws "Removing this node is not allowed": switch to another page first (only for your own scratch pages, or when Juan asks).

## 1. Shared header — paste at the top of every build call

```js
const S = { // JCG paint styles
  lila: 'S:819d30b962bfe9df3a178084c6ff2e31b82920b4,', verde: 'S:7af192d81f99624f5b0dc2db1b92629f1356d840,',
  gris: 'S:9e304f2dac7b9d01a42e5c3f66d5c3103b3beff9,', negro: 'S:379b5e45ffc6721f773972ff9bbce8b361de128b,',
  blanco: 'S:b261762cdf1ca5185557dd3c210fdc9c00c5996e,', lilaLight: 'S:939f59d31d7447612c4e9e2989e6523183068a77,',
  lilaDeep: 'S:e50e9637035a77a26f4095c0e7eacba7a23c4e95,',
};
const B = { // block component IDs (page 🧩 Bloques JCG)
  '4x5':  { stars: '35:22', astTL: '35:24', astBR: '35:26', footContent: '35:28', footCover: '35:33', header: '35:37', band: '35:42' },
  x:      { stars: '35:48', astTL: '35:51', astBR: '35:53', footContent: '35:55', footCover: '35:60', header: '35:64', band: '35:69' },
  story:  { stars: '35:75', astTL: '35:77', astBR: '35:79', footContent: '35:81', footCover: '35:86', header: '35:90', band: '35:95' },
  any: { arrowNegro: '32:46', arrowVerde: '32:48', sunburst: '32:51', quote: '32:54', cta: '32:60', card: '32:62', chart: '32:65',
         groupLila: '34:22', groupLight: '34:33', groupDeep: '34:44', title: '34:56', yes: '34:61', no: '34:63' },
};
const REACTIONS_HASH = 'dc96ff4cd82a30a64340256744f2896c2a32d64f'; // his LinkedIn reactions strip, 644×129
for (const [family, style] of [['Big Shoulders Text','Bold'],['Big Shoulders Text','Regular'],['Big Shoulders Display','Bold'],['Archivo','Regular'],['Archivo','Bold'],['Inter','Regular']])
  await figma.loadFontAsync({ family, style });
const created = [];
// Instance a block into a frame at x,y.
const place = async (blockId, parent, x, y) => {
  const inst = (await figma.getNodeByIdAsync(blockId)).createInstance();
  parent.appendChild(inst); inst.x = x; inst.y = y; created.push(inst.id); return inst;
};
// Override a text layer inside an instance by its layer name.
const setText = (inst, layer, text) => { const t = inst.findOne(n => n.type === 'TEXT' && n.name === layer); t.characters = text; return t; };
// "**bold**" markers → plain text + bold ranges.
const parseBold = (src) => { let text = ''; const ranges = []; src.split('**').forEach((p, k) => { if (k % 2) ranges.push([text.length, text.length + p.length]); text += p; }); return { text, ranges }; };
// New wrapping text. Defaults = 4x5/story slide body (Archivo 40, 133.5%, paragraph gap 40, black; X: size 50, paraGap 50). "**…**" → Bold of the same family.
const addText = async (parent, o) => {
  const { family = 'Archivo', size = 40, lh = 133.5, color = S.negro, align = 'LEFT', paraGap = 40, name } = o;
  const { text, ranges } = parseBold(o.text);
  const t = figma.createText();
  parent.appendChild(t);
  t.fontName = { family, style: o.style || 'Regular' };
  t.characters = text;
  t.fontSize = size;
  t.lineHeight = lh ? { unit: 'PERCENT', value: lh } : { unit: 'AUTO' };
  t.paragraphSpacing = paraGap;
  t.textAlignHorizontal = align;
  t.textAutoResize = 'HEIGHT';
  t.resize(o.w, t.height);
  t.x = o.x; t.y = o.y;
  for (const [a, b] of ranges) t.setRangeFontName(a, b, { family, style: 'Bold' });
  await t.setFillStyleIdAsync(color);
  if (name) t.name = name;
  created.push(t.id); return t;
};
// Archimoto outlines arrive with raw hex fills: link every glyph to the JCG paint style of its colour.
const STYLE_OF = { b084d3: S.lila, d3ff4e: S.verde, ffffff: S.blanco, '000000': S.negro };
const hexOf = (c) => [c.r, c.g, c.b].map(v => Math.round(v * 255).toString(16).padStart(2, '0')).join('');
const linkStyles = async (node) => {
  for (const v of node.findAll(n => n.type === 'VECTOR')) {
    const id = STYLE_OF[hexOf(v.fills[0].color)];
    if (!id) throw new Error(`outline colour #${hexOf(v.fills[0].color)} is not a JCG colour`);
    await v.setFillStyleIdAsync(id);
  }
};
// Archimoto outline (SVG from the script) into a frame. x may be 'center'.
const placeSvg = async (svg, parent, { x, y, name }) => {
  const node = figma.createNodeFromSvg(svg);
  parent.appendChild(node);
  node.name = name || 'Archimoto (outline)';
  node.x = x === 'center' ? Math.round((parent.width - node.width) / 2) : x; node.y = y;
  await linkStyles(node);
  created.push(node.id); return node;
};
// Replace the "Numeral (placeholder)" inside a header or group-card instance with a real numeral.
// The new outline goes into the slide frame, ink aligned to the placeholder's ink (bottom-left, or centred for badges).
// Place the card at its final x,y first: the numeral is a sibling in the slide and does not follow a moved card.
const swapNumeral = async (svg, inst, slide, { center = false } = {}) => {
  const ph = inst.findOne(n => n.name === 'Numeral (placeholder)');
  const p = ph.absoluteBoundingBox, s = slide.absoluteBoundingBox;
  const node = figma.createNodeFromSvg(svg);
  slide.appendChild(node);
  node.name = 'Numeral (Archimoto outline)';
  const inkL = Math.min(...node.children.map(c => c.x)), inkR = Math.max(...node.children.map(c => c.x + c.width));
  const inkB = Math.max(...node.children.map(c => c.y + c.height));
  node.x = Math.round(center ? p.x - s.x + (p.width - (inkR - inkL)) / 2 - inkL : p.x - s.x - inkL);
  node.y = Math.round(p.y + p.height - s.y - inkB);
  await linkStyles(node);
  ph.visible = false;
  created.push(node.id); return node;
};
```

End every build call with `return { created, ... };` plus any bounds you need for the next call. Both Archimoto helpers are async: always `await placeSvg(…)` / `await swapNumeral(…)`.

## 2. New page `YYYY-MM-DD · <title>`

Never reuses or edits an older page; a re-run gets a ` (2)` suffix.

```js
const TITLE = '2026-10-26 · El secreto del AOV';
let name = TITLE, k = 2;
while (figma.root.children.some(p => p.name === name)) name = `${TITLE} (${k++})`;
const page = figma.createPage();
page.name = name;
return { pageId: page.id, name };
```

## 3. Rows and empty frames (one section per size)

Rows stack top to bottom: LinkedIn, then X, then story. **Build the LinkedIn row first** (`SIZES = ['4x5']`), show Juan its screenshot, and only after his OK run this again with `SIZES = ['x', 'story']`: new rows go under the ones already on the page. Frames are named `<n>-<kind>` (kinds in `layouts.md`), sit 100 apart inside the section, clip their content, and get their background. Stars slides also get the star-field block here.

```js
const PAGE_ID = 'PAGE_ID';
const SIZES = ['4x5'];              // first pass; after Juan's OK: ['x', 'story']
const SLIDES = [ // bg: 'stars' | 'gris' | 'lila'
  { n: 1, kind: 'portada', bg: 'stars' },
  { n: 2, kind: 'punto',   bg: 'gris' },
  { n: 3, kind: 'grafico', bg: 'gris' },
  { n: 4, kind: 'cierre',  bg: 'lila' },
];
const S = { lila: 'S:819d30b962bfe9df3a178084c6ff2e31b82920b4,', gris: 'S:9e304f2dac7b9d01a42e5c3f66d5c3103b3beff9,', negro: 'S:379b5e45ffc6721f773972ff9bbce8b361de128b,' };
const ROWS = [
  { size: '4x5',   w: 1000, h: 1250, label: 'LinkedIn · 1000×1250', stars: '35:22' },
  { size: 'x',     w: 1300, h: 1080, label: 'X · 1300×1080',        stars: '35:48' },
  { size: 'story', w: 1080, h: 1920, label: 'Story · 1080×1920',    stars: '35:75' },
];
const PAD = 100, GAP = 100, ROW_GAP = 300;
const page = await figma.getNodeByIdAsync(PAGE_ID);
await figma.setCurrentPageAsync(page);
let y = Math.max(0, ...page.children.map(n => n.y + n.height + ROW_GAP)); const out = {}; // under any row already there
for (const row of ROWS.filter(r => SIZES.includes(r.size))) {
  const sec = figma.createSection();
  sec.name = row.label;
  sec.x = 0; sec.y = y;
  out[row.size] = { sectionId: sec.id, frames: {} };
  for (const [i, s] of SLIDES.entries()) {
    const f = figma.createFrame();
    sec.appendChild(f);
    f.name = `${s.n}-${s.kind}`;
    f.resize(row.w, row.h);
    f.x = PAD + i * (row.w + GAP); f.y = PAD;
    f.clipsContent = true;
    await f.setFillStyleIdAsync(s.bg === 'stars' ? S.negro : S[s.bg]);
    if (s.bg === 'stars') {
      const bg = (await figma.getNodeByIdAsync(row.stars)).createInstance();
      f.appendChild(bg); bg.x = 0; bg.y = 0;
      // X: his dashed orbit line only appears on covers
      if (row.size === 'x' && s.kind !== 'portada') bg.findOne(n => n.name === 'Orbit (dashed Lila, optional)').visible = false;
    }
    out[row.size].frames[f.name] = f.id;
  }
  sec.resizeWithoutConstraints(PAD * 2 + SLIDES.length * row.w + (SLIDES.length - 1) * GAP, row.h + PAD * 2);
  y += row.h + PAD * 2 + ROW_GAP;
}
return out;
```

Single image: one slide `{ n: 1, kind: 'placa', bg: 'gris' }`. Infographic: `{ n: 1, kind: 'infografia', bg: 'gris' }`; for a 1000×1500 infographic change the 4x5 row to `h: 1500` (the label too).

## 4. Fill slides — worked example (tested)

Header + body with bold phrases + image card + footer + arrow (4x5 numbered slide), and a dark cover. Positions and gaps from `layouts.md` (body y 230, body → visual 70, content ends ≤ 1032 on 4x5).

```js
// [shared header here]
const page = await figma.getNodeByIdAsync('PAGE_ID');
await figma.setCurrentPageAsync(page);
// numbered slide: ≤ 25 words, ≤ 2 short paragraphs, Archivo 40 (the addText default)
const pt = await figma.getNodeByIdAsync('FRAME_ID_2_PUNTO');
const header = await place(B['4x5'].header, pt, 55, 33);
setText(header, 'Title', 'Audiencias Amplias');
await swapNumeral(`SVG_FOR_"2."`, header, pt);
const body = await addText(pt, { x: 60, y: 230, w: 885,
  text: 'Segmentar **por intereses** está **comiendo tu margen**.\nDeja la audiencia **lo más amplia posible**: solo sexo, edad y país.' });
// picture card: 70 under the body, at most 460 tall, centred in the room down to 1032 (X: gap 60, end 1020 · story: 70, 1362)
const top = Math.round(body.y + body.height + 70), room = 1032 - top, h = Math.min(460, room);
const card = await place(B.any.card, pt, 59, top + Math.round((room - h) / 2)); card.resize(886, h);
await place(B['4x5'].footContent, pt, 30, 1112);
await place(B.any.arrowNegro, pt, 849, 1121);
// dark cover (stars already placed by recipe 3)
const cover = await figma.getNodeByIdAsync('FRAME_ID_1_PORTADA');
await place(B['4x5'].astTL, cover, -188, 0);
await place(B['4x5'].astBR, cover, 758, 985);
await placeSvg(`SVG_FOR_PHRASE`, cover, { x: 'center', y: 130, name: 'Archimoto "el secreto del aov"' });
await addText(cover, { x: 84, y: 388, w: 832, text: 'Que **no conocías**', family: 'Big Shoulders Text', size: 100, lh: null, color: S.blanco, align: 'CENTER', paraGap: 0 });
const pic = await place(B.any.card, cover, 186, 536); pic.resize(628, 389);
await place(B['4x5'].footCover, cover, 400, 996);
return { created, bodyBottom: Math.round(body.y + body.height) };
```

- `\n` in the text = new paragraph (gap 40 on 4x5/story; on X pass `size: 50, paraGap: 50`). Headlines use `lh: null` (auto) and `paraGap: 0`; give Big Shoulders lines `lh: 101`–`107` when you want his tighter covers.
- Mixed Regular/Bold headline ("Que **no conocías**"): `family: 'Big Shoulders Text'` plus `**…**`.
- Any text override in an instance: `setText(inst, '<layer>', '…')`. Layer names per block are in `blocks.md`. Font sizes can be overridden too (`setText(...).fontSize = 40`). `setText` does not read `**…**` — strip the markers (header titles and quotes are already bold).
- Hide what you don't use: `inst.findOne(n => n.name === 'Subtitle').visible = false;`.

### Footer colour on dark or purple slides (tested)

```js
const fc = await place(B.story.footContent, slide, 82, 1442);
await fc.findOne(n => n.name === 'JCGIUSTO').setFillStyleIdAsync(S.verde);
await fc.findOne(n => n.name === 'URL').setFillStyleIdAsync(S.blanco);
```

`Footer/Cover/*` is already Verde + white on dark and purple slides; keep it that way.

### Highlight box on a text-only point (tested 2026-10-26, airy revision)

The one visual of a text-only `punto` (see `layouts.md` → text-only point), centred in the room under the body so the space above and below it is equal. The rectangle goes first so the text sits on top; layer opacity 0.46 keeps both colours linked to JCG/Lila.

```js
const highlightBox = async (slide, { x, w, text, size, top, bottom }) => { // top = body bottom, bottom = content end (4x5 1032)
  const r = figma.createRectangle(); slide.appendChild(r); r.name = 'Highlight box'; r.cornerRadius = 20;
  await r.setFillStyleIdAsync(S.lila); await r.setStrokeStyleIdAsync(S.lila); r.strokeWeight = 1; r.strokeAlign = 'INSIDE'; r.opacity = 0.46;
  const t = await addText(slide, { x: x + 30, y: 0, w: w - 60, text, family: 'Big Shoulders Display', style: 'Bold', size, lh: null, align: 'CENTER', paraGap: 0, name: 'Highlight text' });
  const h = Math.round(t.height + 70); r.resize(w, h); r.x = x;
  r.y = Math.round(top + (bottom - top - h) / 2); t.y = r.y + 35; created.push(r.id); return r;
};
await highlightBox(pt, { x: 60, w: 885, text: 'Es operativo, no marketing', size: 60, top: body.y + body.height, bottom: 1032 });
// X: { x: 67, w: 1173, size: 70, bottom: 1020 } · story: { x: 112, w: 885, size: 60, bottom: 1362 }
```

## 5. Archimoto outlines (numerals, cover key phrases)

Figma scripts can't load Archimoto, so the words become vector shapes. Run the script with Bash, then paste its output into the `use_figma` code inside a template literal.

```bash
python .claude/skills/figma-post/scripts/archimoto_svg.py --weight regular --size 150 --color "#B084D3" -- "2."
python .claude/skills/figma-post/scripts/archimoto_svg.py --weight bold --size 120 --color "#B084D3" -- "el secreto del aov"
```

- Options first, then `--`, then the text — `--` must be the last thing before the text. Output is one `<svg …>` line; errors print `error: …` and exit 1 (e.g. a character the font lacks — rephrase).
- Paste as `` const svg = `<svg …>`; `` (the SVG has no backticks). Each glyph is one `<path>`; long phrases are a few KB each. Generate each SVG once and reuse it in every row that needs the same weight and size (the cover phrase is 120 in all three; header numerals are Regular on 4x5/story, Bold on X).
- **Colour:** use only `#B084D3` (Lila), `#D3FF4E` (Verde), `#FFFFFF` or `#000000` as `--color`. The helpers link each glyph to the matching JCG paint style (so recolouring the style reaches the numerals); any other hex makes the call throw.
- **Which numeral:** header 4x5/story → `--weight regular --size 150`; header X → `--weight bold --size 150`; group-card badge → `--weight regular --size 74` with `await swapNumeral(svg, card, slide, { center: true })`. Colour `#B084D3` (Lila). Write "2." with the period, as he does.
- **Cover phrase:** `--weight bold --size 120`, Lila on dark slides, Verde `#D3FF4E` on purple ones. Type it lowercase like his originals ("para optimizar"); the font draws capitals. One SVG per line.
- **Placing a phrase where one of his Archimoto text boxes sat** at (x, y): use y + 0.05 × size (Figma adds half the line gap above the text; the SVG box doesn't). With accents (Á, Ñ, Ú) the SVG grows upwards only; centred placement is unaffected.
- **No kerning is applied.** If a pair looks loose (e.g. "AV", "TA"), re-run with tracking (px per glyph, placed before `--`) and compare; keep one tracking per line:
  `python .claude/skills/figma-post/scripts/archimoto_svg.py --weight bold --size 120 --color "#B084D3" --tracking -2 -- "el secreto del aov"`
- Proven: "AÑO ÚNICO" (bold 120) imported as 8 vectors, every one inside its 577×134 box — accents not clipped; "2." regular 150 swapped into `Header/Numbered/4x5` landed at 55,40, matching his "1." position.

## 6. Bar chart — detach, then set heights

Positions can't be overridden inside an instance, so detach first. `setBars` handles both directions: bar 2 higher (stacked gain in light Lila) and bar 2 lower (gain hidden, bar 2 gets the rounded top, guides mark both tops).

```js
const setBars = async (chart, { v1, v2, text1, text2, textGain, label1, label2 }) => {
  const L = (n) => chart.findOne(c => c.name === n);
  const BASE = 440, ROOM = 410, MIN_INSIDE = 70;
  const k = ROOM / Math.max(v1, v2);
  const bar1 = L('Bar 1'), base = L('Bar 2 base'), top = L('Bar 2 top');
  const put = (r, h, bottom) => { r.resize(r.width, Math.max(1, h)); r.y = bottom - Math.max(1, h); };
  const rise = v2 > v1;
  put(bar1, Math.round(v1 * k), BASE);
  put(base, rise ? bar1.height : Math.round(v2 * k), BASE);
  if (rise) { put(top, Math.round((v2 - v1) * k), base.y); base.topLeftRadius = 0; base.topRightRadius = 0; }
  else { top.visible = false; L('Value 2 top').visible = false; base.topLeftRadius = 16; base.topRightRadius = 16; }
  const col2Top = rise ? top.y : base.y;
  L('Guide top').y = Math.min(bar1.y, col2Top);
  L('Guide middle').y = Math.max(bar1.y, col2Top);
  const value = async (name, text, seg) => {
    const t = L(name); t.characters = text;
    if (seg.height >= MIN_INSIDE) t.y = Math.round(seg.y + (seg.height - t.height) / 2);
    else { t.y = Math.round(seg.y - t.height - 8); await t.setFillStyleIdAsync(S.negro); }
  };
  await value('Value 1', text1, bar1);
  if (rise && base.height < MIN_INSIDE) L('Value 2 base').visible = false; else await value('Value 2 base', text2, base);
  if (rise) await value('Value 2 top', textGain, top);
  L('Label 1').characters = label1; L('Label 2').characters = label2;
};
const chart = (await place(B.any.chart, slide, 138, CHART_Y)).detachInstance();
chart.name = 'Chart/Bar';
await setBars(chart, { v1: 60000, v2: 100000, text1: '€60.000', text2: '€60.000', textGain: '+€40.000', label1: 'SIN META', label2: 'CON META' });
// X only: make it bigger (labels 38px), then centre it; ×1.2 keeps 60 under a one-line body and ends ≤ 1020
// chart.rescale(1.2); chart.x = Math.round((1300 - chart.width) / 2);
// then centre it in the room under the body: chart.y = top + Math.round((END - top - chart.height) / 2), top = body bottom + gap
```

- Values are numbers for the heights; `text…` are what's printed. Format them yourself in **the currency of Juan's source** (never convert $ to €), Spanish digits: `€60.000`, `$60.000`, `1,5x`. Labels uppercase, ≤ 12 characters.
- `rescale(1.2)` leaves the chart 867.6 wide; that's fine. Round only the position (`Math.round` as above).
- Tested: drop (100.000 → 60.000) and rise (60.000 → 100.000, rescaled ×1.25 on X to 904×650, labels 40px — before the airy revision; ×1.2 gives 868×624, labels 38px).
- Two values only. More than two bars → not this block; say so in the brief and pick a different visual.

## 7. Images

**Reuse a picture already in the file** (no upload): set its hash as a fill. Tested with the reactions strip on the closing slide. (Inside a build call that already switched to the page; on its own, start with the two page lines below.)

```js
const page = await figma.getNodeByIdAsync('PAGE_ID');
await figma.setCurrentPageAsync(page);
const slide = await figma.getNodeByIdAsync('FRAME_ID_CIERRE');
const re = figma.createRectangle(); slide.appendChild(re);
re.name = 'Reacciones'; re.resize(644, 129); re.x = 178; re.y = 625; re.cornerRadius = 40;
re.fills = [{ type: 'IMAGE', imageHash: REACTIONS_HASH, scaleMode: 'FILL' }];
```

**Put Juan's picture (a file on disk) in an image card** — three steps, tested:

1. `use_figma`: detach the card so its picture layer has a plain ID:
   ```js
   const page = await figma.getNodeByIdAsync('PAGE_ID');
   await figma.setCurrentPageAsync(page);
   const card = (await figma.getNodeByIdAsync('CARD_INSTANCE_ID')).detachInstance();
   card.name = 'Card/Image';
   return { imageRectId: card.findOne(n => n.name === 'Image').id, labelId: card.findOne(n => n.name === 'Placeholder label').id };
   ```
2. `upload_assets` with `count: 1`, `nodeIds: ["<imageRectId>"]`, `scaleMode: "FILL"`, `currentPageId`. Then POST the file to the returned `submitUrl`:
   `curl -s -X POST -F "file=@<path>;type=image/png" "<submitUrl>"` → `{"success":true,"imageHash":…}`.
3. `use_figma`: hide the label and fit the card to the picture's proportions:
   ```js
   const page = await figma.getNodeByIdAsync('PAGE_ID');
   await figma.setCurrentPageAsync(page);
   const card = await figma.getNodeByIdAsync('CARD_ID');
   card.findOne(n => n.name === 'Placeholder label').visible = false;
   const img = card.findOne(n => n.name === 'Image');
   const { width, height } = await figma.getImageByHash(img.fills[0].imageHash).getSizeAsync();
   const MAX_H = CONTENT_BOTTOM - card.y; // 1032 on 4x5, 1020 on X, 1362 on story (80 / 60 / 80 above the footer)
   let w = card.width, h = Math.round(w * height / width);
   if (h > MAX_H) { h = MAX_H; w = Math.round(h * width / height); card.x = Math.round((FRAME_W - w) / 2); }
   card.resize(w, h);
   ```

No picture yet → leave the card with "Pega aquí la imagen" and tell Juan which slide needs it.

## 8. Infographic parts (tested on a story frame)

```js
const HEAD_SIZE = 46, LINE_SIZE = 32;                            // X: 50 / 40 · story: 46 / 35
const title = await place(B.any.title, inf, 0, TITLE_Y);
title.findOne(n => n.name === 'Subtitle').visible = false;      // subtitles: 4x5 only, see layouts.md
if (ONE_LINE_TITLE) {                                            // X, and every decision tree
  title.findOne(n => n.name === 'Line 1').visible = false;
  setText(title, 'Line 2', 'Dónde te descubren tus clientes').fontSize = ONE_LINE_SIZE; // 90 on X, 110 elsewhere
} else { setText(title, 'Line 1', 'Dónde te descubren'); setText(title, 'Line 2', 'tus clientes hoy'); }
title.x = Math.round((inf.width - title.width) / 2);
const g1 = await place(B.any.groupLila, inf, CARD_X, CARD_Y);   // final x,y (from layouts.md) before the numeral swap
g1.resize(CARD_W, g1.height);                                    // width is free; height hugs the lines
setText(g1, 'Heading', 'Buscadores').fontSize = HEAD_SIZE;
for (const [i, line] of ['• Google y Bing', '• ChatGPT'].entries()) setText(g1, `Line ${i + 1}`, line).fontSize = LINE_SIZE;
await swapNumeral(`SVG_FOR_"1."_SIZE_74`, g1, inf, { center: true });
g1.findOne(n => n.name === 'Line 3').visible = false;            // two lines at most: always hide Line 3, last
// a single line has no bullet: setText(root, 'Line 1', 'en paid media'), not '• en paid media'; then hide Line 2 as well
await place(B.any.yes, inf, PILL_X, PILL_Y);                     // B.any.no for "NO"
await place(B[SIZE].band, inf, 0, BAND_Y);
```

- Sizes: heading 46 / lines 32 on 4x5, 50 / 40 on X, 46 / 35 on story (the block's 32 is under the floor on story and X). Tested: the overrides stick on the instance, and these sizes give the card heights in `layouts.md` (4x5 207/262, X 217/282, story 211/270 for 1/2 lines; a third line, over budget, adds ≈ 55–65).
- Tested 2026-10-26 (fix round, before the 2-line budget): the hub built this way in all three sizes with 3-line groups, the one-line X title (hide `Line 1`, `Line 2` at 90) and the story band at y 1440 — audit clean.
- Decide one-line or two-line before setting text: once `Line 1` is hidden, scripts can't see it (see §0 on hidden instance layers).
- Card width: the heading sits beside a 72px badge, so the heading box is the card width minus 146. **A word longer than that box breaks mid-word** ("Buscado-res" at width 340). Use the widths in `layouts.md` and keep headings ≤ 11 characters.
- Position from the measured heights in `layouts.md` before placing anything: the numeral is a separate outline in the slide and stays behind if a card moves after `swapNumeral`. Hide unused lines last.
- **Bullets only for 2 lines.** A group (or the decision-tree root) with one line writes it plain, without "• ". The audit flags a lone bullet.
- **A third line: only if Juan insists** (the budget is two lines). Leave `Line 3` visible (the card grows ≈ 55–65 px), move everything under that card down by the growth, and re-run the audit: it will still report the group as over budget — that one stays, with Juan's say-so.

**Connectors** — black 3px polyline, arrowhead on the last point (tested):

```js
const connector = async (parent, pts, { arrow = true, name = 'Connector' } = {}) => {
  const v = figma.createVector();
  parent.appendChild(v);
  await v.setVectorNetworkAsync({
    vertices: pts.map(([x, y], i) => ({ x, y, strokeCap: arrow && i === pts.length - 1 ? 'ARROW_LINES' : 'NONE' })),
    segments: pts.slice(1).map((_, i) => ({ start: i, end: i + 1 })),
  });
  v.strokeWeight = 3; v.strokeJoin = 'MITER';
  await v.setStrokeStyleIdAsync(S.negro);
  v.name = name; created.push(v.id); return v;
};
await connector(inf, [[260, g1.y + g1.height], [260, 1150], [820, 1150], [820, g2.y + g2.height]]);
```

Points are frame coordinates. Use right-angle elbows (horizontal/vertical segments only). Never draw lines with rotated rectangles.

**Hub centre and spokes** (tested):

```js
const D = 160, CX = 500, CY = 663, CTR = 36;           // 4x5 hub, 3 groups; other sizes + text size in layouts.md
const c = figma.createEllipse(); inf.appendChild(c); c.name = 'Hub';
c.resize(D, D); c.x = CX - D / 2; c.y = CY - D / 2; await c.setFillStyleIdAsync(S.lila); created.push(c.id);
const ct = await addText(inf, { x: CX - (D - 30) / 2, y: 0, w: D - 30, text: 'Visibilidad de marca', family: 'Big Shoulders Text', style: 'Bold', size: CTR, lh: null, color: S.blanco, align: 'CENTER', paraGap: 0 });
ct.y = Math.round(CY - ct.height / 2);
for (const card of cards) {                             // inner corner of each card → circle edge
  const spansX = card.x < CX && card.x + card.width > CX, spansY = card.y < CY && card.y + card.height > CY;
  // a card centred under/over the circle (3 groups) gets a straight spoke from the middle of its facing edge
  const inner = [spansX ? CX : card.x + (card.x < CX ? card.width : 0), spansY ? CY : card.y + (card.y < CY ? card.height : 0)];
  const dx = inner[0] - CX, dy = inner[1] - CY, len = Math.hypot(dx, dy);
  await connector(inf, [inner, [Math.round(CX + D / 2 * dx / len), Math.round(CY + D / 2 * dy / len)]]);
}
```

These spokes are the one place a diagonal is fine (vector network, not a rotated shape). Tested in the fix wave: 3-group hubs in all three sizes. Tested again in the airy revision (4x5, 3 groups, the constants above, 2-line cards at 40,334 · 600,334 · 300,783): every card 40 px from the circle, spokes ≈ 40 px, title → cards 64, cards → band 65, audit clean.

## 9. QA audit (leaves the page unchanged, tested)

Run after every build or fix. It checks every slide on the page:
- **Position and air above the footer:** text and top-level shapes (cards, charts, outlines) inside the frame and above the content end — 80 above a content footer on 4x5/story and 60 on X (default ends 1032 / 1020 / 1362), 60 above an infographic band, and the measured cover rule above a `Footer/Cover` (4x5 cover 960, story cover 1240, i.e. 36 / 28 above the footer).
- **Density (Juan, 2026-10-26: tidy, not cramped):** words per slide over budget (`punto` 25, `grafico` 20, `insight` body 20, single image 25; X `grafico` one line ≤ 45 characters), too many paragraphs, a slide body under 40 px (X 50), a paragraph gap under 40 (X 50), title → body under 60, body → visual under 70 (X 60). Infographics: more than 4 groups (5 cards for a decision tree), more than 2 lines in a group, a line over 16 characters, a heading over 11 (a question over 22), a title over 5 words, cards closer than 60, a card closer than 40 to the hub circle, a pill closer than 12 to a card, the first card closer than 60 to the title.
- **Type:** sizes at or above the floor (the "Pega aquí la imagen" label inside `Card/Image` is exempt), the four fonts, the word "asteroi", leftover placeholder text, text-on-text overlaps.
- **Colour:** every fill and stroke is one of the 7 JCG colours, no gradients, and every solid paint outside a block instance is linked to its JCG paint style (outlines, boxes, circles, connectors, text).
- **Big text (60 px and up):** the last word must not sit alone on its last line. It measures a temporary copy of the text with and without its last word, then deletes the copy.
- **Bullets:** a group card with a single line must not start it with "• ".
- **Page:** clipping on, frame names, overlapping rows, all expected sizes (`SIZES_EXPECTED`: 1 while only the LinkedIn row exists, then 3) and the same slide count per row.

It no longer checks for empty room: whitespace is intended (the old "max 35% empty" and "within 120 px of the band" checks pushed the first designs toward density and are gone).

Tested 2026-10-26 (fix wave): on Juan's three test pages it flagged the lone-bullet root line ×3; on a scratch build it flagged a lonely "creces" (X cover), a lonely "compártelo!" (X closing) and an unlinked Archimoto outline, then passed with 0 issues after the fixes. Tested again 2026-10-26 (airy revision, LinkedIn row with `SIZES_EXPECTED = 1`): the airy text-only point and 3-group hub passed with 0 issues. A deliberately dense copy (43 words in 3 paragraphs at 35 px with gap 28 starting at y 200; cards with a third, 22-character line) was flagged on all of it: words, paragraphs, paragraph gap, body size, title → body 34 px, 3 lines per group, line length, the hub circle 21 px from a card and the cards ending past the band limit.

```js
const PAGE_ID = 'PAGE_ID';
const page = await figma.getNodeByIdAsync(PAGE_ID);
await figma.setCurrentPageAsync(page);
const SIZES_EXPECTED = 3;                              // 1 while only the LinkedIn row is built (first pass)
const SIZE = (f) => f.width === 1300 ? 'x' : f.width === 1080 ? 'story' : '4x5';
const BODY_MIN = { '4x5': 32, story: 35, x: 40 };      // Archivo floor, every text
const BODY = { '4x5': 40, x: 50, story: 40 };          // slide body size (punto, grafico, insight)
const BOTTOM = { '4x5': 1032, x: 1020, story: 1362 };  // default content end (y)
const FOOT_GAP = { '4x5': 80, x: 60, story: 80 };      // last element → Footer/Content
const COVER_GAP = { '4x5': 36, x: 36, story: 28 };     // content ends this far above a Footer/Cover: 996 → 960 (4x5), 1268 → 1240 (story), as in style.md's grid
const GAP = { title: 60, para: { '4x5': 40, x: 50, story: 40 }, visual: { '4x5': 70, x: 60, story: 70 }, band: 60, card: 60, circle: 40, pill: 12 };
const WORDS = { punto: 25, grafico: 20, insight: 20, placa: 25 }, PARAS = { punto: 2, grafico: 1, insight: 1 };
const FONTS = ['Big Shoulders Text', 'Big Shoulders Display', 'Archivo', 'Inter'];
const HEX = ['b084d3', 'e7e5e6', '000000', 'ffffff', 'd3ff4e', 'd8c1ea', '7e4fa6']; // the 7 JCG colours
const STYLES = ['S:819d30b962bfe9df3a178084c6ff2e31b82920b4,', 'S:7af192d81f99624f5b0dc2db1b92629f1356d840,', 'S:9e304f2dac7b9d01a42e5c3f66d5c3103b3beff9,', 'S:379b5e45ffc6721f773972ff9bbce8b361de128b,', 'S:b261762cdf1ca5185557dd3c210fdc9c00c5996e,', 'S:939f59d31d7447612c4e9e2989e6523183068a77,', 'S:e50e9637035a77a26f4095c0e7eacba7a23c4e95,'];
const PLACEHOLDER = /Título del punto|Pega aquí la imagen|Frase clave|Línea corta|Título grande|línea destacada|Subtítulo opcional|Título del grupo/;
const FURNITURE = /^(Background|Asteroid|Footer|Info\/FooterBand|Arrow|Sunburst)/; // allowed to bleed or sit low
const inFooter = (n, frame) => { for (let p = n.parent; p && p !== frame; p = p.parent) if (p.type === 'INSTANCE' && /^(Footer|Info\/FooterBand)/.test(p.name)) return true; return false; };
const visible = (n, frame) => { for (let p = n; p && p !== frame; p = p.parent) if (!p.visible) return false; return true; };
const inInstance = (n, frame) => { for (let p = n; p && p !== frame; p = p.parent) if (p.type === 'INSTANCE') return true; return false; };
const hexOf = (c) => [c.r, c.g, c.b].map(v => Math.round(v * 255).toString(16).padStart(2, '0')).join('');
const words = (s) => s.replace(/•/g, ' ').split(/\s+/).filter(Boolean).length;
const box = (n) => ({ x: n.x, y: n.y, r: n.x + n.width, b: n.y + n.height });
const gapOf = (a, c) => { const dx = Math.max(c.x - a.r, a.x - c.r), dy = Math.max(c.y - a.b, a.y - c.b); return dx > 0 && dy > 0 ? Math.hypot(dx, dy) : Math.max(dx, dy); };
const issues = new Set(); const rows = {}; const big = [];
const paints = (list, styleId, where, own) => {           // own = not inside a block instance
  if (!Array.isArray(list)) return;
  for (const p of list) {
    if (p.visible === false) continue;
    if (p.type.startsWith('GRADIENT')) issues.add(`${where}: gradient`);
    else if (p.type === 'SOLID' && !HEX.includes(hexOf(p.color))) issues.add(`${where}: colour #${hexOf(p.color)} is not one of the 7`);
    else if (p.type === 'SOLID' && own && !STYLES.includes(styleId)) issues.add(`${where}: #${hexOf(p.color)} not linked to its JCG paint style`);
  }
};
for (const sec of page.children) {
  const frames = sec.type === 'SECTION' ? sec.children.filter(c => c.type === 'FRAME') : sec.type === 'FRAME' ? [sec] : [];
  for (const f of frames) {
    const size = SIZE(f); (rows[size] = rows[size] || []).push(f.name);
    if (!/^\d+-[a-záéíóúñ]+/.test(f.name)) issues.add(`${size} ${f.name}: frame name is not <n>-<kind>`);
    if (!f.clipsContent) issues.add(`${size} ${f.name}: clipsContent is off`);
    // content end: 60 above an infographic band; 80 (X 60) above a content footer; the cover rule above a Footer/Cover
    const band = f.children.find(c => c.visible && /^Info\/FooterBand/.test(c.name));
    const footers = f.children.filter(c => c.visible && /^Footer/.test(c.name));
    const limit = band ? band.y - GAP.band : Math.min(BOTTOM[size], ...footers.map(c => c.y - (/^Footer\/Cover/.test(c.name) ? COVER_GAP[size] : FOOT_GAP[size])));
    const content = f.children.filter(c => c.visible && !FURNITURE.test(c.name));
    for (const c of content) {
      if (c.x < -1 || c.x + c.width > f.width + 1 || c.y < -1) issues.add(`${size} ${f.name} [${c.name}]: sticks out of the frame`);
      if (c.y + c.height > limit + 1) issues.add(`${size} ${f.name} [${c.name}]: ends at y ${Math.round(c.y + c.height)}, past the content end ${limit} (not enough air above the footer)`);
    }
    // density — tidy, not cramped (Juan 2026-10-26): words, paragraphs, body size, gaps
    const kind = (f.name.match(/^\d+-([a-záéíóúñ]+)/) || [])[1];
    const fam = (t) => t.getRangeFontName(0, 1).family;
    const own = f.children.filter(c => c.visible && c.type === 'TEXT');                 // free-standing text, not inside blocks
    const bodies = own.filter(t => fam(t) === 'Archivo').sort((a, c) => a.y - c.y);
    if (WORDS[kind]) {
      const n = (kind === 'placa' ? own : bodies).reduce((a, t) => a + words(t.characters), 0);
      if (n > WORDS[kind]) issues.add(`${size} ${f.name}: ${n} words, budget ${WORDS[kind]} — cut words or split the slide`);
    }
    if (PARAS[kind]) for (const t of bodies) {
      const tag = `${size} ${f.name} "${t.characters.slice(0, 24)}"`, paras = t.characters.split('\n').filter(s => s.trim()).length;
      if (paras > PARAS[kind]) issues.add(`${tag}: ${paras} paragraphs, max ${PARAS[kind]}`);
      if (paras > 1 && t.paragraphSpacing < GAP.para[size]) issues.add(`${tag}: paragraph gap ${t.paragraphSpacing}, min ${GAP.para[size]}`);
      const fs = Math.min(...t.getStyledTextSegments(['fontSize']).map(s => s.fontSize));
      if (fs < BODY[size]) issues.add(`${tag}: body ${fs}px — slide bodies use ${BODY[size]}`);
      if (size === 'x' && kind === 'grafico' && t.characters.length > 45) issues.add(`${tag}: X chart body is one line, ≤ 45 characters`);
    }
    if (kind === 'punto' || kind === 'grafico') {
      const head = f.children.find(c => c.visible && /^Header\/Numbered/.test(c.name)), body = bodies[0];
      if (head && body) {
        const tb = head.findOne(n => n.name === 'Title').absoluteBoundingBox, titleBottom = tb.y + tb.height - f.absoluteBoundingBox.y;
        if (body.y - titleBottom < GAP.title - 1) issues.add(`${size} ${f.name}: title → body ${Math.round(body.y - titleBottom)} px, min ${GAP.title}`);
        const below = content.filter(c => c !== body && c.y > body.y), next = below.sort((a, c) => a.y - c.y)[0];
        if (next && next.y - (body.y + body.height) < GAP.visual[size] - 1) issues.add(`${size} ${f.name}: body → [${next.name}] ${Math.round(next.y - body.y - body.height)} px, min ${GAP.visual[size]}`);
      }
    }
    if (kind === 'infografia') {
      const cards = content.filter(c => /^Info\/GroupCard/.test(c.name)), pills = content.filter(c => /^Pill/.test(c.name));
      const hub = content.find(c => c.type === 'ELLIPSE' && c.name === 'Hub');
      if (cards.length > (pills.length ? 5 : 4)) issues.add(`${size} ${f.name}: ${cards.length} groups, max ${pills.length ? '5 cards in a tree' : 4} (3 preferred)`);
      for (const c of cards) {
        const head = c.findOne(n => n.type === 'TEXT' && n.name === 'Heading'), tag = `${size} ${f.name} "${head.characters}"`;
        const lines = c.findAll(n => n.type === 'TEXT' && /^Line \d/.test(n.name) && visible(n, f));
        if (lines.length > 2) issues.add(`${tag}: ${lines.length} lines, max 2`);
        for (const l of lines) if (l.characters.length > 16) issues.add(`${tag} "${l.characters}": ${l.characters.length} characters, max 16`);
        if (head.characters.length > (/[¿?]/.test(head.characters) ? 22 : 11)) issues.add(`${tag}: heading too long (max 11, a question 22)`);
      }
      // title: the Info/TitleHighlight instance, or on a mind map the 'Title block' rectangle with its text named 'Title'
      const title = content.find(c => /^Info\/TitleHighlight/.test(c.name)) || content.find(c => c.name === 'Title block');
      const tTexts = !title ? [] : 'findAll' in title ? title.findAll(n => n.type === 'TEXT' && visible(n, f) && n.name !== 'Subtitle') : own.filter(t => t.name === 'Title');
      const titleWords = tTexts.reduce((a, t) => a + words(t.characters), 0);
      if (titleWords > 5) issues.add(`${size} ${f.name}: title has ${titleWords} words, max 5`);
      const first = Math.min(...cards.map(c => c.y), hub ? hub.y : Infinity);
      if (title && first - (title.y + title.height) < GAP.title - 1) issues.add(`${size} ${f.name}: title → first card ${Math.round(first - title.y - title.height)} px, min ${GAP.title}`);
      for (let i = 0; i < cards.length; i++) for (let j = i + 1; j < cards.length; j++) {
        const g = gapOf(box(cards[i]), box(cards[j]));
        if (g < GAP.card - 1) issues.add(`${size} ${f.name}: two cards ${Math.round(g)} px apart, min ${GAP.card}`);
      }
      if (hub) for (const c of cards) {
        const cx = hub.x + hub.width / 2, cy = hub.y + hub.height / 2, b = box(c);
        const g = Math.hypot(cx - Math.min(Math.max(cx, b.x), b.r), cy - Math.min(Math.max(cy, b.y), b.b)) - hub.width / 2;
        if (g < GAP.circle - 1) issues.add(`${size} ${f.name}: hub circle ${Math.round(g)} px from a card, min ${GAP.circle}`);
      }
      for (const p of pills) for (const c of cards) if (gapOf(box(p), box(c)) < GAP.pill) issues.add(`${size} ${f.name}: [${p.name}] ${Math.round(gapOf(box(p), box(c)))} px from a card, min ${GAP.pill}`);
    }
    // colours: only the 7, no gradients, own solid paints linked to a JCG style
    for (const n of [f, ...f.findAll(n => visible(n, f))]) {
      const own = !inInstance(n, f), where = `${size} ${f.name} [${n.name.slice(0, 24)}]`;
      if (n.type === 'TEXT') { for (const s of n.getStyledTextSegments(['fills', 'fillStyleId'])) paints(s.fills, s.fillStyleId, where, own); }
      else if ('fills' in n) paints(n.fills, n.fillStyleId, where, own);
      if ('strokes' in n) paints(n.strokes, n.strokeStyleId, where, own);
    }
    const fb = f.absoluteBoundingBox;
    const texts = f.findAllWithCriteria({ types: ['TEXT'] }).filter(t => visible(t, f));
    const boxes = [];
    for (const t of texts) {
      const b = t.absoluteBoundingBox, x = b.x - fb.x, y = b.y - fb.y, tag = `${size} ${f.name} "${t.characters.slice(0, 24)}"`;
      if (x < -1 || y < -1 || x + b.width > f.width + 1 || y + b.height > f.height + 1) issues.add(`${tag}: outside the frame`);
      const footer = inFooter(t, f), exempt = t.name === 'Placeholder label'; // "Pega aquí la imagen" in Card/Image
      if (!footer && y + b.height > limit + 1) issues.add(`${tag}: ends at y ${Math.round(y + b.height)}, limit ${limit}`);
      const segs = t.getStyledTextSegments(['fontName', 'fontSize']);
      for (const s of segs) {
        if (!FONTS.includes(s.fontName.family)) issues.add(`${tag}: font ${s.fontName.family}`);
        if (exempt) continue;
        if (s.fontSize < 32 && !(t.name === 'URL' && s.fontSize === 30)) issues.add(`${tag}: ${s.fontSize}px is under 32`);
        if (s.fontName.family === 'Archivo' && s.fontSize < BODY_MIN[size]) issues.add(`${tag}: body ${s.fontSize}px under ${BODY_MIN[size]}`);
      }
      if (/asteroi/i.test(t.characters)) issues.add(`${tag}: says asteroi`);
      if (PLACEHOLDER.test(t.characters)) issues.add(`${tag}: placeholder text left`);
      if (!footer) boxes.push({ tag, x, y, r: x + b.width, btm: y + b.height });
      if (!footer && Math.max(...segs.map(s => s.fontSize)) >= 60 && /\S\s+\S/.test(t.characters.trim())) big.push({ t, tag });
    }
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], c = boxes[j];
      if (a.x < c.r - 2 && c.x < a.r - 2 && a.y < c.btm - 2 && c.y < a.btm - 2) issues.add(`${a.tag} overlaps ${c.tag.split(' ').slice(2).join(' ')}`);
    }
    // a group card with a single line: no bullet
    for (const card of f.findAll(n => 'children' in n && n.children.some(c => c.name === 'Lines'))) {
      const lines = card.findAll(n => n.type === 'TEXT' && /^Line \d/.test(n.name) && visible(n, f));
      if (lines.length === 1 && /^\s*•/.test(lines[0].characters)) issues.add(`${size} ${f.name} "${lines[0].characters}": a line on its own takes no bullet`);
    }
  }
}
// big text (60px+): is the last word alone on its last line? Measure a copy with and without that word.
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
const tmp = [];
try {
  for (const { t, tag } of big) {
    const segs = t.getStyledTextSegments(['fontName', 'fontSize', 'lineHeight', 'letterSpacing']);
    for (const s of segs) await figma.loadFontAsync(s.fontName);
    const m = figma.createText(); tmp.push(m); m.x = -5000;
    m.characters = t.characters;
    for (const s of segs) { m.setRangeFontName(s.start, s.end, s.fontName); m.setRangeFontSize(s.start, s.end, s.fontSize); m.setRangeLineHeight(s.start, s.end, s.lineHeight); m.setRangeLetterSpacing(s.start, s.end, s.letterSpacing); }
    m.paragraphSpacing = t.paragraphSpacing;
    if (t.textAutoResize === 'WIDTH_AND_HEIGHT') m.textAutoResize = 'WIDTH_AND_HEIGHT'; else { m.textAutoResize = 'HEIGHT'; m.resize(t.width, m.height); }
    const before = m.height;
    m.deleteCharacters(m.characters.replace(/\s*\S+\s*$/, '').length, m.characters.length);
    if (m.height < before - 1) issues.add(`${tag}: last word alone on its last line — break the lines by hand or change the box width`);
  }
} finally { for (const m of tmp) m.remove(); }   // the page is left exactly as it was
const tops = page.children.map(n => n.absoluteBoundingBox);
for (let i = 0; i < tops.length; i++) for (let j = i + 1; j < tops.length; j++) {
  const a = tops[i], b = tops[j];
  if (a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height) issues.add(`top-level overlap: ${page.children[i].name} / ${page.children[j].name}`);
}
const sizes = Object.keys(rows);
if (sizes.length < SIZES_EXPECTED) issues.add(`only ${sizes.join(', ')} present`);
const counts = sizes.map(s => rows[s].length);
if (new Set(counts).size > 1) issues.add(`rows have different slide counts: ${JSON.stringify(rows)}`);
const all = [...issues];
return { frames: counts.reduce((a, b) => a + b, 0), rows, issues: all.slice(0, 60), more: Math.max(0, all.length - 60) };
```

How to fix what it reports:
- **Last word alone:** move the hand break (`\n`) or widen the box to the size's full centred width (`layouts.md` → "Big text"). Never shrink below the sizes in the tables.
- **Over a word, paragraph or line budget:** cut words, or split the point into two slides (an infographic group: shorten the lines; too many groups → propose a carousel). Never shrink the type to make it fit; tell Juan what you cut.
- **Body under 40 (X 50), paragraph gap under the minimum:** set the size and `paragraphSpacing` from `layouts.md` (a longer body then breaks the word budget: cut).
- **A gap under the minimum** (title → body, body → visual, cards, circle, pills, or "past the content end"): move the piece to the positions in `layouts.md`; if it still does not fit, the slide has too much on it — cut, don't squeeze.
- **Not linked to its JCG paint style:** `await node.setFillStyleIdAsync(S.<colour>)` (or `setStrokeStyleIdAsync`); outlines made with the helpers above are linked already.

It does not see a shape covering text (a card over a paragraph), words hidden behind an asteroid, or a break that splits a phrase badly (a line ending "…= subir un" with "2% tu ARPU" below it) — that's what the screenshots are for. "Pega aquí la imagen" is the only placeholder allowed to stay, and only for a picture Juan will paste.

## 10. Screenshots

**For your own visual check** — inline, several frames per call (tested):

```js
const page = await figma.getNodeByIdAsync('PAGE_ID');
await figma.setCurrentPageAsync(page);
for (const id of ['FRAME_ID_1', 'FRAME_ID_2']) await (await figma.getNodeByIdAsync(id)).screenshot({ scale: 0.4 });
return 'ok';
```

Look for: text cut off or crowding the footer, words hidden behind asteroids, cards over text, a numeral sitting off its title line, a line break that splits a phrase or a number from its unit, wrong footer colour, any flat black area, a pill touching a card.

**For Juan** — one image per row (tested): `get_screenshot` with `nodeId` = the row's section ID and `maxDimension: 2400`, then download with the `curl -f -L -o <file> "<url>"` it prints, into the session scratchpad as `<page title> - <size>.png`. The URL is short-lived; download right away. The image includes the section's white padding around the frames (a one-frame section comes back a little larger than the frame); that is expected.

**Link to the page:** `https://www.figma.com/design/U2HIUwTWDYWL7EwSKCDpLd/Contenido?node-id=<page id with ":" replaced by "-">`.

## 11. Fixing and re-running

- Fix in place with targeted edits on the same page (move, resize, re-set text). Don't rebuild a whole row for one problem.
- A build call failed half-way and `safeToRetryWithoutCanvasRead` is false → empty that frame and redo it:
  ```js
  const page = await figma.getNodeByIdAsync('PAGE_ID');
  await figma.setCurrentPageAsync(page);
  const f = await figma.getNodeByIdAsync('FRAME_ID');
  for (const c of [...f.children]) if (!c.name.startsWith('Background/')) c.remove();
  ```
- Rebuild of the whole piece → new page (recipe 2 adds the suffix). Never delete an older page without Juan saying so.
