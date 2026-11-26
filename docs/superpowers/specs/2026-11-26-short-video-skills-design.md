---
title: Short-video skills — design
description: Four skills that take Juan from idea to a finished, ready-to-post short video in Max Wellcopy's edit style and Juan's brand. Ranking short built first.
type: project
author: claude
sources: [docs/superpowers/specs/2026-11-26-max-video-edits-research.md]
related: [max-wellcopy-playbook, templates, content-strategy]
created: 2026-11-26
updated: 2026-11-26
confidence: medium (approved pieces marked; the rest is Claude's proposal)
---

# Short-video skills — design

## Why

Juan posts on five platforms, modelled on Max Wellcopy. Short videos are the piece he can't make today without an editor. He wants to film himself, hand over the raw file, and get back a video that is ready to post: Max's edit style, Juan's colours, Juan's words. **"Raw recording in, finished file out."** No CapCut step.

## Scope

- **In:** short vertical videos only, three formats (below).
- **Out for now:** long YouTube videos. They come later.
- **Anti-goals:** a video that looks like a template engine made it; anything that needs Juan to open an editor; copying Max's face, voice or exact words.

## The four skills

| Skill | Juan gives | Juan gets back |
|---|---|---|
| Ideas | nothing, or a topic | short ideas for each format, grounded in Max's 320 transcripts and what performs |
| Script | the idea he picked | what to say, in his voice, timed for 20–45 s |
| Edit | the raw recording + screenshots | the finished MP4 |
| Clip | a long video (podcast or his YouTube) | the best 30–60 s moments, ready for the Edit skill |

Build order (agreed): the Edit skill with the ranking look first → Juan sees a real finished file → the hack and edited-clip looks → the Clip skill → Ideas and Script.

## Approaches (decided)

- **Remotion (picked).** Videos written as code, rendered on his PC. Proven for talking head + captions + overlays; free for a solo creator.
- HyperFrames: newer, less proven for this mix. Dropped.
- Claude prepares, Juan finishes in CapCut: Juan rejected — he wants the finished file.

One Remotion project, one look per format, sharing captions, badges, cuts and audio.

## The three formats

### Ranking (build first)

Max's real example: Instagram reel Db3PqznPy6B — his face full screen, the email pasted on the left, "0/10" badge top right, small white captions under his face.

**Juan hands over:**
1. A vertical selfie recording, phone or webcam, ~30 s. He says the score out loud for each item ("this one is a three out of ten").
2. One screenshot per item, in the order he talks about them (file names 1, 2, 3…).

**Claude does, in order:**
1. Transcribes with word timings (faster-whisper, already installed).
2. Finds each item by the spoken score. Shows Juan the list — item, score, caption text — before rendering. **This is the text check.**
3. Removes every pause longer than ~0.3 s. Cuts at each new item.
4. Places each screenshot ~0.2 s after its cut: tall pages in the left column (x 6–45%, y 5–96%), wide ones in the upper half. No border, shadow or animation.
5. Adds the score badge, top right of the screenshot.
6. Adds captions: white, lowercase, 5–13 words per line, 2–3 s each, under his face (82–88% down).
7. Sets loudness to −14 LUFS. No music, no sound effects.
8. Renders 1080×1920, 30 fps MP4.

**Look:** Max's measured layout, Juan's brand on the badge and captions. Badge = Archimoto numbers on a rounded box, either black box with white score and purple "/10", or purple box with black text — **Juan picks** (mock: two options next to Max's frame). Captions = Archivo Medium, white, soft shadow.

### Hack ("changing backgrounds")

Max's example: YouTube short Wi7TmhMsiAA. 3 s title box over his face, then screenshot cards in the top half changing every ~3 s, sometimes a full-screen page with him cut out in front.

Juan's version: title box black with Big Shoulders headline; cards as in ranking. The cut-out works on his PC (see the test below), as long as he films against a plain wall.

### Edited clip ("steal this")

Max's example: Instagram reel DdOyjXIRDrf. Black frame, wide podcast clip in the middle, words pop below one at a time, key words big and bold, cut to the screenshot, red underlines, "BAD" sticker.

**Source (Juan, 2026-11-26):** his Andrew Faris podcast episode now; his own YouTube videos once they start in week four. The Clip skill picks moments by the rule in the research doc: bold claim → one concrete example with a number → a rule, 30–60 s, no "as I said earlier". Key-word colour: purple or the site-button green — **Juan picks** when this format is built.

Note: Max doesn't cut his long videos into shorts. Clipping is Juan's own addition.

## Background removal test

Tested on Juan's PC 2026-11-26 (an earlier message said it had been tested; it hadn't — this is the first real test). Footage: 10 s clips of Max's home selfies (no footage of Juan on the PC yet).

- **Works: Robust Video Matting (resnet50 model) on the laptop's GPU.** Hair kept strand by strand, no leftover wall or door, fingers cut cleanly. About 1.5 min of processing per 30 s of 1080×1920 video with a lean script.
- **Weak spot:** a very fast, blurred hand wave loses part of the hand for 1–3 frames. Slower gestures are fine.
- **Best case only:** plain, evenly lit wall. A cluttered room or a window behind him will look worse. Film against a plain wall.
- MediaPipe: fast but blocky edges, leaves bits of the room. rembg: halo around hair, or 20+ min per clip for the good model. Both dropped.
- Setup that worked: onnxruntime-gpu plus NVIDIA's CUDA 13 runtime packages in a Python venv; model file from the project's GitHub release. Test script kept at `scratchpad/bgtest/scripts/matte.py` (session scratch — copy into `content/scripts/video/` when the hack look is built).

## Constraints

- No Mars Men numbers, no ASTEROI client names, no men's-health brands in rankings, no Meta ads advice, no paid tool deals.
- Personal data on screenshots hidden with plain black boxes (Max's way).
- Scripts in Juan's voice (writing-voice memory, humanize skill), not AI voice.
- Credit Andrew Faris when clipping his podcast.
- Max's downloaded videos stay local (gitignored).

## Where things live (Claude's call)

- Remotion project: `content/scripts/video/` (committed).
- Each video's inputs and output: `content/video/<date>-<slug>/` with `raw/`, `shots/`, `out/` — gitignored (large files).
- Skills: `.claude/skills/` like figma-post.

## Left to the builder

Remotion version and setup, how captions break into lines, how pauses are found (word gaps vs audio level), how a score is matched when Juan says it oddly, test approach.
