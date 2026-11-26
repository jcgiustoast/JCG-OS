---
name: video-edit
description: Use when Juan hands over a selfie recording and wants a finished short ("edit my video", "make the ranking short", "rank these", a phone video plus screenshots) — turns the raw recording and one screenshot per item into a ready-to-post 1080×1920 MP4 in Max Wellcopy's ranking layout and Juan's brand. Ranking format only for now; the Transparent Background and edited-clip looks are not built yet.
---

# Video edit — the ranking short

Raw selfie recording + one screenshot per item in, finished vertical video out. Juan gets the finished file, not a CapCut project.

The look: his face full screen with his **real room behind him** (no cut-out, no blur), each screenshot in a column on the left, a black badge with the white score and a purple "/10" sitting on that screenshot's top-right corner (never on his face), small white lowercase captions right of the screenshot, low on his chest. Everything stays inside the area Instagram and TikTok leave clear of their buttons and text (260 px from the top, 440 from the bottom, 60 left, 140 right; numbers in `content/scripts/video/layout.json`). Pauses over 0.3 s removed, including silences whisper hides inside stretched words; small cuts blend over 2 frames so they don't stutter. Loudness −14 LUFS. No music, no sound effects.

Design: `docs/superpowers/specs/2026-11-26-short-video-skills-design.md`. Code: `content/scripts/video/` (Python prep + Remotion look + `make_short.py`). Tests: `python -m pytest tests/video -q`.

## What Juan hands over

- **One phone recording, ~30 s.** Tidy, well-lit spot, phone at eye level. No plain wall needed. He says a score out loud for every item: "Bloom's product page, seven out of ten."
- **The original file from the phone** (cable, Google Drive, email as a file). WhatsApp shrinks video to about 480×850 and it looks soft at 1080×1920. If WhatsApp is all there is, render it, but say once that the original would be sharper.
- **One screenshot per item**, named 1, 2, 3… in the order he speaks. Phone-size page screenshots work best; very long full-page ones are fine (the top part shows).

## Steps

1. **Job folder:** `content/video/<YYYY-MM-DD>-<slug>/` (gitignored). Copy the recording into `raw/` (exactly one video there) and screenshots into `shots/`.
2. **Prep:** `python content/scripts/video/make_short.py ranking <job> --step prep`. It normalises the video, transcribes it, finds each spoken score and writes `edl.json` + `review.md`.
   - If it stops (exit 2), it says which scores it heard and which screenshots it found. Tell Juan in plain words what doesn't line up. Never force a render.
   - If he spoke items but no scores ("number one, number two"), it can't place anything: ask him to re-record with a score per item.
3. **Look at every screenshot** (Read tool). Black out names, emails, addresses, order numbers or anything personal by writing `shots/redact.json` → `{"2.png": [[x, y, w, h]]}` in image pixels, then re-run prep.
4. **Screen the hard limits** — no Mars Men numbers, no ASTEROI client names, no men's-health brands, no Meta ads advice, no paid tool deals. Also check each screenshot actually matches what he says about that item.
5. **Show Juan the review** in chat: each item with its brand, score and the caption words under it. Fix transcription slips in `edl.json` captions (brand names especially: "I am 8" → "im8"). Wait for his OK.
6. **Render:** `python content/scripts/video/make_short.py ranking <job> --step render` (~1 min per 10 s of video). It checks size, fps and loudness itself (exit 3 if off).
7. **Watch it before sending:** pull one frame per item plus one caption change (`ffmpeg -ss <t> -i <job>/out/<name>.mp4 -frames:v 1 frame.png`) and look at each. Badge right score, right screenshot, on the screenshot's corner not his face, captions readable and not over the screenshot, nothing outside the safe area. Prep overwrites `edl.json`, so caption fixes have to be redone after any re-prep.
8. **Send** `<job>/out/<job-name>.mp4` with SendUserFile.

## Talking to Juan

Plain-speech rules from his global CLAUDE.md apply to every message: say the brand, not "item 2"; no file names, IDs or numbered lists of findings; a question is one bold sentence plus one sentence recommending an answer. Report what he'll see, not the machinery.
