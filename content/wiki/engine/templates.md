---
title: Visual and Video Templates
description: The two carousel templates (X-post look for quick tactics, "space" designed deck for brand studies), built as Figma kits of slide kinds that fit each post's copy. Thumbnail, Reel and YouTube description still to come.
type: concept
author: claude
sources: [content/raw/research/max-wellcopy-2026-11/playbook.md]
related: [engine/content-types, engine/repurpose, engine/hooks, max-wellcopy-playbook]
created: 2026-11-26
updated: 2026-11-26
confidence: high
---

# Visual and Video Templates

> A template is a look plus a kit of slide kinds. The copy comes first and picks the kinds it needs, in any order and any number. Nothing is a fixed outline, not even the last slide (Juan, 2026-11-26: "The template should fit the copy"; the comment-keyword slide is "case by case").

Both carousel templates live in Juan's Figma file **Contenido**. Every kind exists in the three sizes: 1000×1250 (LinkedIn, Instagram), 1300×1080 (X) and 1080×1920 (story). Each kind is an auto-layout component, so editing the text reflows the slide. Build new carousels from instances through `/figma-post`.

Review page with Max's examples and every variant Juan saw: https://claude.ai/artifact/H7QrbuqMrrDFdgwWxbS1HM

## Carousel 1 · Post look (quick tactics)

**What it's for:** one tactic, a few tips, screenshots. Most of Max's carousels (61 of 75) use this look.

**Look (picked 2026-11-26):** it passes for a real X post. Max's dark grey #111111, Juan's photo, "Juan Cruz Giusto" with X's blue badge, @jcgiusto underneath, text in Inter (X's Chirp isn't available in Figma) in X's colours (#E7E9EA text, #71767B handle). Screenshots are attached the way X attaches an image (rounded corners, thin #2F3336 border). The only brand colour is a Lila box around the key part of a screenshot. No footer, no like/view counts and no timestamp, so nothing is faked and reposts never look dated.

**Kinds:** cover line · text only · text + wide screenshot · text + tall screenshot · comment slide (resource) · video slide (keyword sends the YouTube breakdown, thumbnail attached).

**Figma:** page "Template · Post look (X)" (`236:21`), Kit section `236:22`, example carousel `236:295`, video slide set `244:171`. Header text is Inter; edit text straight in each instance.

## Carousel 2 · Designed deck, "space" (brand studies)

**What it's for:** "how these brands did it" posts. It's modelled on Max's magazine deck (his look since 13 Nov 2026) with far fewer words per slide.

**Look (picked 2026-11-26):** dark slides and white slides alternate, like Max's. Covers and comment slides sit on Juan's star background; brand openers are full-bleed dark photos with brand tabs across the top, a Lila pill and a big Lila Archimoto numeral. Text slides are white, with the accented headline line in Lila words. Lila pills on photos, Lila check circles, and a dark takeaway bar whose last words are Lila. Headlines are in Big Shoulders Text Bold, body text in Archivo. Real posts use each brand's own photos; the stand-ins in the kit were made with Figma's image tool.

**Kinds:** cover · text · brand opener · the play · checklist ("copy it only if…") · big number · side by side · comment slide (switch: sends a resource or the YouTube video).

**Figma:** page "Template · Designed deck (space)" (`238:21`), Kit section `238:22`, example carousel `242:315`, comment slide "Sends = Resource | Video" (video: `244:444` LinkedIn, `244:464` X, `244:487` story). Optional parts are on/off switches in the right panel (cover: numeral, line 3, brands 3–4; text: paragraph 2, bottom box; opener: tabs 3–4, pill; the play: photos 2–3, takeaway bar; checklist: rows 4–5, closing line; side by side: column 4). Each kind holds the maximum and hides the extras, because Figma can't add rows to an instance. Archimoto numerals and big numbers are outlines (Figma scripting can't load the font): change them in Figma desktop. The big-number sample ("$100M+ a year in refills") is not a real figure.

## What we learned from Max

- What drives comments is the **last slide**, not the look. Ending on a specific keyword that sends something earned a median of 81 comments; a generic "DM me" earned 7.
- **The carousel often sells the YouTube video** (Juan, 2026-11-26). Max's deck ends "Comment PLAYBOOK and I'll send you a video breaking this all down in more depth", and his dark X posts end "Look up … on YouTube & watch the full breakdown" with the video's thumbnail. So both kits have two endings: the keyword sends a resource (CHECKLIST → jcgiusto.com/the-ultimate-subscription-ecommerce-checklist/) or the YouTube breakdown (keyword picked per post). Which one is case by case.
- Max's deck slides carry 60–90 words each. Juan's rule is fewer words, one idea per slide.

## Still to build

- YouTube thumbnail, Reel template (CapCut) and YouTube description + pinned comment, each shown against Max's examples first. Earlier proposals, none approved yet: https://claude.ai/artifact/CCcVbS1S7Tc3mGu354q5qX

## Changelog

- **2026-11-26:** Created. Both carousel looks picked (post look → X look-alike on #111 with blue tick, after "as close as possible to X"; deck → "space", after "make them cooler"). Templates defined as kits that fit the copy.
