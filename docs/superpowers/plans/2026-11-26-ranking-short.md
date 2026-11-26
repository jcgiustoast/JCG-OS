# Ranking Short Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** One command turns Juan's raw selfie recording + one screenshot per item into a finished 1080×1920 ranking short in Max's layout and Juan's brand.

**Architecture:** Python "prep" reads the recording (normalise with ffmpeg, transcribe with faster-whisper word timings), finds each spoken score, removes pauses, groups captions, and writes one JSON edit list (`edl.json`) plus a `review.md` for Juan's text check. A Remotion project renders `edl.json` into video. A final ffmpeg pass sets loudness to −14 LUFS. `make_short.py` runs the three in order.

**Tech Stack:** Python 3.13 (faster-whisper 1.2.1, Pillow, pytest — already installed globally), ffmpeg 8, Node 22, Remotion 4 (exact version pinned at install), TypeScript, React.

**Spec:** `docs/superpowers/specs/2026-11-26-short-video-skills-design.md` (layout numbers from `docs/superpowers/specs/2026-11-26-max-video-edits-research.md`, "Ranking Reel").

## Global Constraints

- Output: 1080×1920, 30 fps, H.264 + AAC, integrated loudness −14 LUFS (±1), no music, no sound effects.
- Pauses longer than 0.3 s removed.
- Screenshot appears 0.2 s after each item's cut. No border, shadow, rounding or animation.
- Tall screenshot column: x 6–45% of width, y 5–96% of height. Wide screenshot (width ≥ height): 47% of width, upper half.
- Badge: black (#000) rounded box, score white, "/10" purple #B084D3, Archimoto V00 Medium; left 68%, top 26%, width 16%, height 5.5% of frame; appears on the cut, no animation.
- Captions: Archivo Medium, white, soft shadow, no box, 41 px, block max-width 45% of width, centred at x 65%, vertical band 82–88%; lowercase; 5–13 words per phrase; ≤3 s each; no word highlight, no emoji; score phrases written as digits ("3 out of 10").
- Fonts come from `content/scripts/visual/assets/fonts/` (already committed: `archimoto-medium.otf`, `archivo-medium.ttf`). Don't duplicate them.
- Job folders `content/video/<date>-<slug>/` are gitignored (large files). Layout: `raw/` (recording), `shots/` (1.png, 2.png…), `face.mp4`, `words.json`, `edl.json`, `review.md`, `out/`.
- Hard limits (checked by Claude in review, not code): no Mars Men numbers, no ASTEROI client names, no men's-health brands, no Meta ads advice, no paid tool deals.

## Review Focus

- Phone footage is HEVC `.MOV`, 60 fps, 4K, or rotated → normalised to 1080×1920 30 fps H.264 before anything else (Task 4 test).
- Number of spoken scores ≠ number of screenshots → prep stops and says which scores it heard and which files it found; never renders a misaligned video (Task 4 test).
- Scores said several ways ("zero out of ten", "0 out of 10", "a 10 out of 10", "3/10") → all found (Task 1 test).
- Screenshots named 1…10 → ordered numerically, so 10 comes after 9 (Task 4 test).
- A very long full-page screenshot (e.g. 1080×8000) → shows its top part inside the column, not squashed (Task 4 test).

---

### Task 1: Score finder

**Files:**
- Create: `content/scripts/video/prep/__init__.py`, `content/scripts/video/prep/words.py`, `content/scripts/video/prep/scores.py`
- Create: `tests/video/__init__.py`, `tests/video/test_scores.py`

**Interfaces:**
- Produces: `@dataclass(frozen=True) Word(text: str, start: float, end: float)` in `words.py`; `load_words(path) -> list[Word]`, `save_words(words, path)` (JSON list of `{text,start,end}`).
- Produces: `@dataclass(frozen=True) ScoreHit(score: int, word_index: int, start: float)` and `find_scores(words: list[Word]) -> list[ScoreHit]` in `scores.py`. `word_index` = index of the number word.

- [ ] **Step 1: Write failing tests** — build `Word` lists with helper `w("text", t)` (0.3 s per word):
  - `test_digits`: "this is a 0 out of 10 email" → `[ScoreHit(0, 3, …)]`
  - `test_number_words`: "this one is a three out of ten" → score 3 (and "one" is NOT a hit)
  - `test_slash`: "honestly 7/10" → score 7; also whisper splitting "7/10." with punctuation
  - `test_ten_out_of_ten`: "a 10 out of 10" → score 10
  - `test_punctuation_case`: "Zero out of ten." → score 0
  - `test_order`: three mentions → three hits in time order
- [ ] **Step 2:** `python -m pytest tests/video/test_scores.py -v` → FAIL (import error)
- [ ] **Step 3: Implement** — normalise each token (lowercase, strip punctuation except `/`), map zero…ten to ints, match `<n> out of <10|ten>` across tokens or `<n>/10` in one token.
- [ ] **Step 4:** same command → PASS
- [ ] **Step 5: Commit** `add video prep score finder — finds spoken N out of 10`

### Task 2: Pause remover

**Files:**
- Create: `content/scripts/video/prep/cuts.py`, `tests/video/test_cuts.py`

**Interfaces:**
- Consumes: `Word`.
- Produces: `@dataclass(frozen=True) Span(src_start: float, src_end: float, out_start: float)`; `keep_spans(words, max_gap=0.3, pad=0.08) -> list[Span]`; `to_out(t: float, spans) -> float` (source time → output time; a time inside a removed gap maps to the next span's `out_start`); `total(spans) -> float`.

- [ ] **Step 1: Write failing tests**
  - `test_gap_removed`: words at 0–1 s and 2–3 s → two spans; `total` ≈ 2 + 4×pad
  - `test_small_gap_kept`: gap 0.2 s → one span
  - `test_leading_trailing_silence_trimmed`: first word at 1.5 s, recording 10 s → first span starts at 1.5−pad, last ends at last word end + pad
  - `test_to_out`: time in 2nd span maps to `out_start + offset`; time in a gap maps to next span start
  - `test_pad_never_overlaps`: gap 0.31 s with pad 0.08 → spans don't overlap
- [ ] **Step 2:** run → FAIL
- [ ] **Step 3: Implement** in `cuts.py`.
- [ ] **Step 4:** run → PASS
- [ ] **Step 5: Commit** `add video prep pause remover`

### Task 3: Captions

**Files:**
- Create: `content/scripts/video/prep/captions.py`, `tests/video/test_captions.py`

**Interfaces:**
- Consumes: `Word`, `ScoreHit`.
- Produces: `@dataclass(frozen=True) Caption(text: str, src_start: float, src_end: float)`; `make_captions(words, breaks: list[int]) -> list[Caption]` where `breaks` = word indices where a new item starts (always start a new caption there).

Rule (not determined by tests alone): add words to the current phrase; close it when it has ≥5 words and (the next gap > 0.25 s, or the word ends with `.?!`, or the phrase lasts ≥3 s), or when it hits 13 words, or the next word is a break. A final phrase under 5 words merges into the previous one if that stays ≤13 words.

- [ ] **Step 1: Write failing tests**
  - `test_lowercase_no_punct`: "This is GREAT." → "this is great" (apostrophes kept: "don't")
  - `test_score_digits`: "a three out of ten email" → "a 3 out of 10 email"; "this one is" stays "this one is"
  - `test_max_13_words`: 30 evenly spaced words → every caption ≤13 words
  - `test_min_5_words`: no caption under 5 words except when the whole recording is shorter
  - `test_break_starts_new_caption`: break at index 7 → a caption starts exactly at word 7
  - `test_max_3_seconds`: slow words (0.6 s each) → each caption ≤3 s
- [ ] **Step 2:** run → FAIL
- [ ] **Step 3: Implement** `captions.py`.
- [ ] **Step 4:** run → PASS
- [ ] **Step 5: Commit** `add video prep captions`

### Task 4: Media + edit list

**Files:**
- Create: `content/scripts/video/prep/media.py`, `content/scripts/video/prep/transcribe.py`, `content/scripts/video/prep/edl.py`, `content/scripts/video/requirements.txt`
- Create: `tests/video/test_media.py`, `tests/video/test_edl.py`
- Modify: `.gitignore` — add `content/video/`, `content/scripts/video/node_modules/`, `content/scripts/video/public/job/`

**Interfaces:**
- `media.py`: `normalize(src: Path, dst: Path) -> None` (ffmpeg: autorotate, scale to cover + centre-crop 1080×1920, fps 30, libx264 crf 18, aac 192k 48 kHz); `probe(path) -> dict` with `width, height, fps, duration`; `image_size(path) -> tuple[int,int]`.
- `transcribe.py`: `transcribe(path, model="small", language="en") -> list[Word]` (faster-whisper, `word_timestamps=True`, CPU int8; model name overridable).
- `edl.py`: `list_shots(shots_dir) -> list[Path]` (png/jpg/webp, numeric order by leading number); `item_cut(words, hit, lookback=2.5) -> int` (index of the first word of the item's sentence: the word after the largest gap ≥0.15 s within `lookback` s before the hit, else the score word itself); `build_ranking_edl(job: Path, words: list[Word]) -> dict`; `write_review(edl, path)`; `class PrepError(Exception)`.

`edl.json` shape (Remotion props; times in seconds, paths relative to the Remotion public dir):

```json
{
  "format": "ranking", "fps": 30, "width": 1080, "height": 1920,
  "video": "job/face.mp4", "duration": 31.4,
  "spans": [{"srcStart": 0.4, "srcEnd": 6.1, "outStart": 0.0}],
  "items": [{"score": 0, "shot": "job/shots/1.png", "layout": "tall",
             "box": {"x": 65, "y": 96, "w": 421, "h": 1100}, "crop": false,
             "outStart": 0.0, "outEnd": 7.2, "redact": [{"x": 10, "y": 20, "w": 200, "h": 40}]}],
  "captions": [{"text": "this is a 0 out of 10 email", "outStart": 0.0, "outEnd": 2.4}]
}
```

Layout: `tall` (h > w) → width 421 px (x 65 = 6%), height scaled, vertically centred on 47% of frame height and clamped inside y 96–1843 (5–96%); if taller than the band, `crop: true` and box = full band (renderer shows the image's top, `object-fit: cover; object-position: top`). `wide` → width 508 px (47%), x 65, y 230. Item `outStart` = `to_out(words[item_cut].start)`; its shot shows from `outStart + 0.2`; `outEnd` = next item's `outStart` (last item → end). `redact` boxes come from `shots/redact.json` (`{"1.png": [[x,y,w,h]]}` in image pixels; optional file) — Claude fills it after looking at each screenshot.

- [ ] **Step 1: Write failing tests**
  - `test_normalize_landscape_60fps` (`test_media.py`): make a 3 s 1920×1080 60 fps test clip with `ffmpeg -f lavfi testsrc2 + sine`, normalise → probe says 1080×1920, 30 fps, has audio
  - `test_list_shots_numeric`: files `1.png 2.png 10.png 9.png` → order 1, 2, 9, 10
  - `test_mismatch_raises`: 3 scores in words, 2 shots → `PrepError` whose message contains "3 scores" and "2 screenshots" and lists the scores heard
  - `test_tall_layout`, `test_very_tall_is_cropped` (1080×8000 → `crop: true`, box within band), `test_wide_layout`
  - `test_item_times`: shots appear in score order, `outEnd` of item n == `outStart` of item n+1, last `outEnd` == `duration`
  - `test_review_md`: contains each score, shot file name and every caption text
- [ ] **Step 2:** `python -m pytest tests/video -v` → new tests FAIL
- [ ] **Step 3: Implement** `media.py`, `transcribe.py`, `edl.py`; write `requirements.txt` (`faster-whisper>=1.2`, `pillow>=10`, `pytest>=8`); update `.gitignore`.
- [ ] **Step 4:** run → PASS
- [ ] **Step 5: Commit** `add video prep media + edit list for the ranking short`

### Task 5: Remotion ranking look

**Files:**
- Create: `content/scripts/video/package.json`, `tsconfig.json`, `remotion.config.ts`, `src/index.ts`, `src/Root.tsx`, `src/edl.ts`, `src/fonts.ts`, `src/parts/FaceTrack.tsx`, `src/parts/Shot.tsx`, `src/parts/Badge.tsx`, `src/parts/Captions.tsx`, `src/Ranking.tsx`, `content/scripts/video/sample/edl.sample.json`, `content/scripts/video/public/.gitkeep`

**Interfaces:**
- Consumes: `edl.json` shape from Task 4.
- Produces: Remotion composition id `Ranking`, props = edl; `calculateMetadata` sets `durationInFrames = ceil(duration*fps)`, width/height/fps from props.
- `FaceTrack`: one `<Sequence>` per span (`from = outStart*fps`), `<OffthreadVideo src={staticFile(video)}>` trimmed to `srcStart…srcEnd` (use the trim prop names of the installed Remotion version).
- `Shot`: `<Img>` absolutely placed at `box`; `crop` → cover/top; black `<div>`s for `redact`, scaled from image pixels to box. `Badge`: per item, from `outStart` (no 0.2 s delay). `Captions`: per caption `<Sequence>`.
- `fonts.ts`: load Archimoto Medium and Archivo Medium by importing the files from `../../visual/assets/fonts/` and `@remotion/fonts` `loadFont` (or `FontFace` + `delayRender`).

- [ ] **Step 1:** `npm init` in `content/scripts/video`, then `npm i --save-exact remotion @remotion/cli @remotion/fonts react react-dom` and `npm i -D --save-exact typescript @types/react`. Scripts: `"typecheck": "tsc --noEmit"`, `"still": "remotion still src/index.ts Ranking"`.
- [ ] **Step 2:** write `sample/edl.sample.json` (one span over a lavfi test clip copied to `public/job/face.mp4`, two items, two captions, one redact box) — this is the visual test fixture.
- [ ] **Step 3: Implement** the components with the Global Constraints numbers.
- [ ] **Step 4: Verify:** `npm run typecheck` → 0 errors; `npx remotion still src/index.ts Ranking out/still.png --props=sample/edl.sample.json --frame=45` → PNG exists; open it and compare against `docs/superpowers/specs/assets/short-video/ranking-badge-options.png` (middle): badge position/colours, caption position/size, screenshot column.
- [ ] **Step 5: Commit** `add Remotion ranking look for the short-video editor`

### Task 6: One-command runner + end-to-end test

**Files:**
- Create: `content/scripts/video/make_short.py`, `tests/video/test_e2e.py`

**Interfaces:**
- CLI: `python content/scripts/video/make_short.py ranking <job_dir> --step prep|render|all [--whisper-model small]`
  - `prep`: find the single video in `raw/` → `normalize` → `face.mp4` → `transcribe` → `words.json` → `build_ranking_edl` → `edl.json` + `review.md`; prints review path. `PrepError` → exit code 2 with its message.
  - `render`: wipe + copy `face.mp4` and `shots/` into `content/scripts/video/public/job/`; `npx remotion render src/index.ts Ranking <job>/out/render.mp4 --props=<job>/edl.json` (cwd = video project); ffmpeg `loudnorm=I=-14:TP=-1:LRA=11` (video stream copied) → `<job>/out/<job-name>.mp4`; then check with ffprobe + `ebur128`: 1080×1920, 30 fps, integrated −14 ±1 LUFS; print the final path.
  - `all`: prep then render.
- Python functions: `prep(job: Path, whisper_model: str) -> Path` (edl path), `render(job: Path) -> Path` (final mp4), `check_output(path) -> dict` (`width,height,fps,lufs`).

- [ ] **Step 1: Write the failing test** `test_e2e_ranking` (mark `@pytest.mark.slow`; register the marker in `pytest.ini` or `pyproject` under `tests/video/conftest.py`): build a job in `tmp_path` — speech via Windows SAPI (`powershell` `System.Speech.Synthesis.SpeechSynthesizer.SetOutputToWaveFile`) saying "this is a zero out of ten email. … this one is a seven out of ten. … and this is a ten out of ten." with ~0.8 s pauses, muxed with a 1080×1920 lavfi colour video; three PNG shots made with Pillow. Run `make_short.py ranking <job> --step all`. Assert: exit 0; `edl.json` has scores `[0, 7, 10]`; output `check_output` → 1080, 1920, 30, LUFS within −15…−13; output duration < input duration (pauses removed).
- [ ] **Step 2:** `python -m pytest tests/video/test_e2e.py -v -m slow` → FAIL
- [ ] **Step 3: Implement** `make_short.py`.
- [ ] **Step 4:** run → PASS; also `python -m pytest tests/video -v` → all PASS
- [ ] **Step 5: Commit** `add make_short.py — raw recording in, finished ranking short out`

### Task 7: Skill + real recording

**Files:**
- Create: `.claude/skills/video-edit/SKILL.md`

- [ ] **Step 1:** Write the skill: when to use ("edit my video", "make the ranking short"); what Juan hands over (recording against a plain wall, score said out loud per item, one screenshot per item named 1, 2, 3…); the steps — make job folder → `--step prep` → look at every screenshot and fill `shots/redact.json` for names/emails/addresses → show Juan the review (items, scores, caption words) in plain words and screen the hard limits → fix caption typos in `edl.json` if he asks → `--step render` → watch frames from the output (`ffmpeg -ss … -frames:v 1`) before sending → `SendUserFile` the MP4. Plain-speech rules apply to every message.
- [ ] **Step 2:** Juan's recording: copy it into `content/video/2026-11-26-<slug>/raw/`, his screenshots into `shots/`; run the skill end to end.
- [ ] **Step 3:** Check 5 frames (one per item + one caption change) against the mock; fix and re-render if off.
- [ ] **Step 4:** Send Juan the finished file. Don't start the hack or edited-clip looks until he's seen it.
- [ ] **Step 5: Commit** `add video-edit skill — ranking short`
