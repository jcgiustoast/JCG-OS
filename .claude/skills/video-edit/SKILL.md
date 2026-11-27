---
name: video-edit
description: Use when Juan hands over a selfie recording and wants a finished short ("edit my video", "make the ranking short", "rank these", a phone video plus screenshots) — turns the raw recording and one screenshot per item into a ready-to-post 1080×1920 MP4 in Max Wellcopy's ranking layout, or in the Transparent Background look (title box, pictures as cards or full-screen with Juan cut out on top), in Juan's brand. Triggers for Transparent Background: "transparent background", "cut-out short", a recording plus pictures plus a headline. The edited-clip look is not built yet.
---

# Video edit — the ranking short and the Transparent Background short

Two formats. The ranking short is below. For Transparent Background, jump to its own section further down.

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

# Transparent Background short

Recording + pictures + a headline in, finished vertical video out. The headline shows in a black box for the first 3 seconds. After that each picture shows when Juan says its words: either a card in the top half (his room behind him) or full screen, with Juan cut out of his room and standing on top of the picture. Same captions, pause cuts, loudness (−14 LUFS) and safe zones as the ranking short. Always call it Transparent Background, nothing else.

Code format name is `transparent`. Design: same spec as above.

## What Juan hands over

- **The original recording** from the phone, not a WhatsApp copy (same reason as ranking).
- **Pictures named 1, 2, 3…** in the order he speaks them.
- **The headline in his words.** Shown exactly as he writes it.
- Full-screen moments cut him out best against a plain, evenly lit wall. A busy wall (paintings) gives rough edges. A plain white wall cut him out cleanly on 2026-11-27 (hair, hands, shirt edges).
- **Framing for cards:** cards sit in the top half (y 300–920). If he's framed in the middle, his face is under the cards. Before filling `pictures.json`, grab one frame of `face.mp4` and check where his face is. If it's in the top half, tell him and recommend making every picture full-screen for this video, and framing lower next time (chest at the bottom edge, head below the middle).

## Steps

1. **Job folder:** `content/video/<YYYY-MM-DD>-<slug>/`. Recording into `raw/` (exactly one video), pictures into `shots/`, his headline into `headline.txt`.
2. **Prep:** `python content/scripts/video/make_short.py transparent <job> --step prep`. Normalises and transcribes, and writes a `pictures.json` stub. It never overwrites a `pictures.json` that exists.
3. **Fill `pictures.json`.** One row per picture: `{"picture": "1.png", "words": "...", "show": "card"}`. `words` = the exact 2–6 words Juan says where the picture should appear, copied from `words.json`. `show` is `"card"` or `"full"`; the stub guesses full for very tall page screenshots, card otherwise. To switch a picture, change `show` in its row. Pictures must follow the order he speaks.
4. **Look at every picture** (Read tool). Black out names, emails, addresses, order numbers or anything personal in `shots/redact.json` → `{"2.png": [[x, y, w, h]]}` in image pixels. Screen the hard limits: no Mars Men numbers, no ASTEROI client names, no men's-health brands, no Meta ads advice, no paid tool deals. Check each picture matches what he says there.
5. **Plan:** `python content/scripts/video/make_short.py transparent <job> --step plan`. Writes `edl.json` and `review.md`. If it stops (exit 2) it names the picture and the words that don't work: words not heard, out of order, too close together, too near the end. Fix `pictures.json` and re-run. Never force it.
6. **Show Juan the check list in chat.** The headline, then each picture by what it shows, the words where it appears, card or full screen, and the captions under it. Wait for his answers.
7. **Apply his changes:** switch card/full or change words in `pictures.json`; fix caption slips in `fixes.json` → `{"what whisper heard": "what Juan means"}` (brand names especially). Re-run `--step plan` until it comes out clean. Never hand-edit `edl.json`; plan rewrites it every time, and caption fixes in `fixes.json` survive re-runs.
8. **Cut-out:** `python content/scripts/video/make_short.py transparent <job> --step matte`. Only runs over the full-screen moments, on the GPU. Needs the cut-out tool set up once: `powershell content/scripts/video/setup_matte.ps1` (downloads about 2 GB plus a 107 MB model). Ask Juan before installing. If he records again, run matte again: the render refuses a cut-out made from an older recording.
9. **Render:** `python content/scripts/video/make_short.py transparent <job> --step render`. Checks size, fps and loudness itself (exit 3 if off). `--step all` runs plan, matte and render in one go.
10. **Watch it before sending:** one frame per picture plus the title (`ffmpeg -ss <t> -i <job>/out/<name>.mp4 -frames:v 1 frame.png`). Title inside the safe area, right picture at the right words, cut-out edges clean (hair, hands), captions on top and readable.
11. **Send** `<job>/out/<job-name>.mp4` with SendUserFile.

For a first video on a new wall, run the matte step on the first full-screen moment before showing Juan the list and look at three frames (hair, hands, edge). If rough, say so in one line and recommend a plain wall next time. Render only if he accepts the look.

Talking to Juan: same plain-speech rules as above.
