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
4. **Readable on a phone:** body at least 32px on 4x5, 35 on story, 40 on X; no text under 32 except the footer URL. Shorten the words; never shrink below the floor.
5. **All three sizes, every time:** 1000×1250 (LinkedIn), 1300×1080 (X), 1080×1920 (story).
6. **Two checkpoints with Juan:** the type before anything, the outline before any Figma work. Never skip them.
7. **Never touch his originals.** Pages "JCG" and "Carousel" and the components on "🧩 Bloques JCG" are read-only. Build only on a new page.
8. This skill writes to Figma only (plus screenshots in the session scratchpad). No repo files, no commits.

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

### 3. Outline the on-image text — checkpoint
Write every word that will be on the image, slide by slide (or group by group), in one chat block:

**Carrusel · 5 diapositivas · LinkedIn, X y story**
- Portada (oscura): «el secreto del aov»
  Que **no conocías** — foto: pega aquí tu captura
- Punto 1 · Audiencias Amplias: Segmentar por intereses **está comiendo tu margen**. …
- Gráfico · Antes y después: €60.000 → €100.000 …
- Insight: «El creativo es tu verdadero targeting» …
- Cierre: Si te ha gustado este post,
  **¡dale a me gusta y compártelo!**

- Cover: dark (stars) by default; purple when the headline leads with a number or a list ("10 estrategias…").
- Fit happens here, not in Figma: keep to the word budgets in `references/layouts.md`, mark bold with `**…**`, and say what the X version drops.
- Show the line break of every big line (cover headline, quote, closing line, box) as a real line break in the outline, so no word ends up alone on a last line (layouts → Big text). `\n` appears only inside the Figma code.
- A text-only point gets its body size from its word count, plus a highlight box under 45 words (layouts → text-only point).
- Infographics hold at most four groups (a decision tree: one question, two branches, two outcomes), each with at most three lines of 16 characters; a group with one line has no bullet. If the points don't fit that, propose a carousel.

Then ask **"Shall I build it like this?"** with one recommendation sentence. Build only after a clear yes. If he edits, update the outline; ask again only if the change is big.

### 4. Build in Figma
1. New page `YYYY-MM-DD · <short title>` (recipe 2). One page per piece.
2. Rows and empty frames for all three sizes, named `<n>-<kind>` (recipe 3).
3. Archimoto outlines for every numeral and cover phrase (recipe 5 and below).
4. Fill one size row per call: paste the shared header, then place blocks and text at the positions in `references/layouts.md` (recipes 4–8). Return the IDs.
5. Pictures: a file from Juan → upload it into the card (recipe 7). No file → leave "Pega aquí la imagen".

### 5. Check it
1. Run the QA audit (recipe 9). It also checks colours, a word alone on the last line of big text, empty room on points and above infographic bands, and lone bullets. Fix every issue (fixes listed under the recipe), except picture placeholders left on purpose.
2. Screenshot every frame inline (recipe 10) and look. Fix overlaps, badly split phrases, text crowding the footer, wrong footer colour, numerals off their title line.
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

- `references/style.md` — colours, fonts, type sizes, readability floor, grid per size, footer, how to write the words.
- `references/layouts.md` — every slide kind, single-image pattern and infographic layout, with positions per size and word budgets.
- `references/figma-recipes.md` — tested `use_figma` code: page, rows, blocks, bold text, Archimoto, chart, pictures, connectors, QA, screenshots, fixes.
- `references/blocks.md` — the building-blocks page: component IDs, sizes, layer names, fonts to load, measured grids.
- `references/img/` — Juan's three infographic references (structure only, never their colours).
- Design spec: `docs/superpowers/specs/2026-10-26-figma-post-design-skill-design.md`.
