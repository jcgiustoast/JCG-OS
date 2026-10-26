---
name: figma-post
description: Use when Juan wants a carousel, an infographic or a single image for LinkedIn or X ("carrusel", "infografía", "placa", "diseño en Figma") from a post, a draft, or a topic with key points — this skill builds it IN FIGMA, as editable layers in his Contenido file. For PNGs rendered from code, use `/visual` instead (the separate code-rendered engine).
---

# /figma-post — Juan's posts, designed in Figma

Turns a post (or a topic plus points) into a carousel, infographic or single image **in Juan's own look**, on a new page of his Figma file "Contenido", editable layer by layer, in all three sizes. Juan exports it himself.

Not this skill: exporting PNG/PDF or posting; writing the caption (`/content`); video or story-only pieces; HTML-rendered PNGs (`/visual` is a separate engine).

## Talking to Juan (his plain-speech rule — always)

- Plain words. Never use a node ID, layer name, file name or code as a word. Say the thing: "the chart slide", "the purple cover".
- One question at a time: **one bolded sentence ending in "?"**, then one sentence with your recommendation. Nothing else in that block.
- Concrete first, then the point. One idea per sentence. Don't number options or findings across messages; restate a choice in full each time.
- Report what he will see, not machinery: "the carousel is ready in Figma", not "frames created".
- Chat in the language he writes in. Text on the image follows the language of his post.

## Hard rules (fail even if it "works")

1. **Purple + grey only.** Verde is a small accent (list in `references/style.md`). No other colours, gradients, glassy cards, icon libraries or centred-everything sameness.
2. **Dark means the star-field image**, never flat black. No green-heavy backgrounds.
3. **The footer says jcgiusto.com.** Never asteroi.co.
4. **Readable on a phone:** slide bodies are Archivo 40 on 4x5 and story, 50 on X. Nothing under the floor (32 on 4x5, 35 on story, 40 on X) except the footer URL. Cut words; never shrink type to fit.
5. **All three sizes, every time:** 1000×1250 (LinkedIn), 1300×1080 (X), 1080×1920 (story).
6. **Agree before building** (Juan, 2026-10-26): the type before anything; the design + content brief before any Figma work; then the LinkedIn size alone, and X and story only after he OKs its screenshot. Never skip a checkpoint.
7. **Tidy, not cramped** (Juan, 2026-10-26: "the ones you created in the past were overly dense"): one idea per slide, within the word budgets and minimum gaps in `references/style.md` → Density. Whitespace is fine: never fill it with more words or elements; centre what is there.
8. **Never touch his originals.** Pages "JCG" and "Carousel" and the components on "🧩 Bloques JCG" are read-only. Build only on a new page.
9. This skill writes to Figma only (plus screenshots in the session scratchpad). No repo files, no commits.

## Before the first Figma call

1. Load the Figma tools: `ToolSearch` query `use_figma get_screenshot get_figma_skill create_session upload_assets`, max_results 8.
2. Read `skill://figma/figma-use/SKILL.md` and `skill://figma/figma-generate-design/SKILL.md` with `get_figma_skill`, and follow them.
3. `create_session` (when the tool exists) with fileKey `U2HIUwTWDYWL7EwSKCDpLd`; pass its `sessionId` on every Figma call.
4. Every `use_figma` call: that fileKey; `skillNames: "resource:figma-use,resource:figma-generate-design"`; switch page once with `await figma.setCurrentPageAsync(page)`; return only IDs and small evidence (under 48 KB). `createImageAsync` is not available.
5. Read `references/blocks.md` (block IDs, layer names, fonts) and `references/figma-recipes.md` (tested code) before writing any script.

## The steps

### 1. Read the input
A post or draft: use it. A topic only: ask once, e.g. **"Do you want me to draft the key points?"** plus one recommendation sentence. Take numbers and claims only from what Juan gave you, in the currency he used ($ stays $, € stays €; never convert).

### 2. Suggest the type — checkpoint
- **Carousel:** several separate points, or a story in steps.
- **Single image:** one idea — one number, one comparison, one quote.
- **Infographic:** a framework read in one look — hub, decision tree or mind map.

Ask, e.g.: **"Do you want this as a carousel?"** I'd go carousel: the post has five separate tips, one per slide.
For an infographic, name the layout in the question ("an infographic laid out as a decision tree"). Wait for his answer.

### 3. Design + content brief — checkpoint
Agree the look and the words before anything is built. One chat block; per slide (or infographic group) one line for the look — slide kind, background (dark / grey / purple), the visual (chart, screenshot to paste, quote box, highlight box, big number, none) — then the exact text:

**Carrusel · 5 diapositivas · primero LinkedIn, luego X y story**
- **Portada** · oscura (estrellas) · sin imagen
  «el secreto del aov»
  que **no conocías**
- **Punto 1** · gris · captura que pegas tú
  Audiencias Amplias
  Segmentar por intereses **está comiendo tu margen**.
- **Gráfico** · gris · barras €60.000 → €100.000 …
- **Insight** · oscura · caja de cita: «El creativo es tu verdadero targeting»
- **Cierre** · morada · reacciones
  Si te ha gustado este post,
  **¡dale a me gusta y compártelo!**

- Plain words; no layer names or IDs. Cover: dark by default; purple when the headline leads with a number or a list ("10 estrategias…").
- Fit happens here, never in Figma (budgets in `references/style.md` → Density): a point ≤ 25 words in ≤ 2 short paragraphs (a chart point ≤ 20); a single image = one headline, one visual, at most one short line; an infographic = 3 groups (4 at most), ≤ 2 lines of 16 characters each, title ≤ 5 words, a decision tree at most one level under the answers. More than that → split into another slide, cut, or propose a carousel. Prefer cutting words.
- Mark bold with `**…**` (one phrase per paragraph). Show every big line's break (cover, quote, closing, box) as a real line break (layouts → Big text); `\n` appears only in the Figma code. Say what the X version drops.

Then ask **"Shall I build it like this?"** with one recommendation sentence. Nothing is built until he says yes. Any change he asks for: show the updated brief and wait for a yes again.

### 4. Build in Figma — LinkedIn first
1. New page `YYYY-MM-DD · <short title>` (recipe 2). One page per piece.
2. The LinkedIn row only (recipe 3, `SIZES = ['4x5']`), frames named `<n>-<kind>`; Archimoto outlines (recipe 5); blocks and text at the positions and gaps in `references/layouts.md` (recipes 4–8). Pictures: a file from Juan → upload it (recipe 7); none → leave "Pega aquí la imagen".
3. Check it (step 5, `SIZES_EXPECTED = 1`), screenshot the row (step 6) and show it to Juan: **"Does the LinkedIn version look right?"** plus one recommendation sentence. Fix what he asks and show it again.
4. Only after his OK: the X and story rows (recipe 3, `SIZES = ['x', 'story']`), same words, positions per size; then check everything again (`SIZES_EXPECTED = 3`).

### 5. Check it
1. Run the QA audit (recipe 9). It checks density (words, paragraphs, body size, gaps), position, colours, a word alone on the last line of big text, and lone bullets. Fix every issue by cutting or moving, never by shrinking type (fixes under the recipe); only a picture placeholder left on purpose may stay.
2. Screenshot every frame inline (recipe 10) and look. Fix overlaps, badly split phrases, cramped spots, wrong footer colour, numerals off their title line.
3. After fixes: one more audit and one more screenshot pass. Stop when both are clean.

### 6. Hand off
Screenshot each row with `get_screenshot` (the row's section, maxDimension 2400) and download it into the session scratchpad. Then tell Juan, in a few plain lines: the Figma link to the page, the screenshot file paths, which slides still need a picture, and anything you cut for X. Ask nothing unless something needs his decision.

## Archimoto (numerals and cover phrases)

Figma scripts can't load the Archimoto font, so its words become vector shapes. The script needs `fonttools` (`pip install fonttools`). From the repo root:
`python .claude/skills/figma-post/scripts/archimoto_svg.py --weight bold --size 120 --color "#B084D3" -- "el secreto del aov"`
prints one SVG; insert it with the async helpers `placeSvg` / `swapNumeral` in the recipes (they also link its colour to the JCG paint style). Options go first and `--` goes last, right before the text. The letters are shapes, not text: Juan can retype them in Figma desktop if needed. No kerning is applied: if a letter pair looks loose on the screenshot, re-run with tracking and compare:
`python .claude/skills/figma-post/scripts/archimoto_svg.py --weight bold --size 120 --color "#B084D3" --tracking -2 -- "el secreto del aov"`

## When things go wrong

- A `use_figma` error: obey `safeToRetryWithoutCanvasRead`. If false, read the frame, clear it (recipe 11) and redo only that frame.
- A block looks wrong or doesn't fit: don't edit the blocks page. Build that piece from plain shapes in his colours and tell Juan.
- Juan asks for changes later: edit the same page in place. A full rebuild goes on a new page.

## References

- `references/style.md` — colours, fonts, type sizes, readability floor, density (word budgets, minimum gaps), grid per size, footer, how to write the words.
- `references/layouts.md` — every slide kind, single-image pattern and infographic layout, with positions, gaps and word budgets per size.
- `references/figma-recipes.md` — tested `use_figma` code: page, rows, blocks, bold text, Archimoto, chart, pictures, connectors, QA, screenshots, fixes.
- `references/blocks.md` — the building-blocks page: component IDs, sizes, layer names, fonts to load, measured grids.
- `references/img/` — Juan's three infographic references (structure only, never their colours).
- Design spec: `docs/superpowers/specs/2026-10-26-figma-post-design-skill-design.md`.
