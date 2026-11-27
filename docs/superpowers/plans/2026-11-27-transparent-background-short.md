# Transparent Background Short Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A second look in the existing short-video maker: Juan's selfie recording + his pictures + his headline in, a finished 1080×1920 Transparent Background short out — 3 s black title box, picture cards in the top half while he talks in his real room, and a few full-screen pages with him cut out in front.

**Architecture:** Reuses the ranking short's prep (normalise, whisper words, pause removal, captions, loudness, safe zones) and its Remotion project. New: a hand-editable picture list `pictures.json` (picture, the words where it appears, card or full) that prep creates once and **never overwrites**; a `plan` step that turns that list + `headline.txt` + `fixes.json` into a throwaway `edl.json` and `review.md`; a `matte` step that runs Robust Video Matting (resnet50, GPU) in its own venv only over the full-screen moments and writes transparent WebM clips; a `TransparentBackground` Remotion composition that layers page → cut-out → cards → title → captions.

**Tech Stack:** Python 3.13 (faster-whisper, Pillow, pytest — global, as today); separate venv `.venv-matte` with onnxruntime-gpu 1.32.0 + NVIDIA CUDA 13 runtime wheels + numpy (RTX 5070 Ti laptop GPU); ffmpeg 8 (libvpx-vp9 for alpha WebM); Remotion 4.0.547 (pinned, unchanged), React 19, TypeScript.

**Spec:** `docs/superpowers/specs/2026-11-26-short-video-skills-design.md` — "### Transparent Background (approved 2026-11-27)", "Background removal test", "Constraints". Measurements: `docs/superpowers/specs/2026-11-26-max-video-edits-research.md` ("Transparent Background short"). Builds on `docs/superpowers/plans/2026-11-26-ranking-short.md`.

## Global Constraints

- Name: always "Transparent Background" in copy, `transparent` in code (CLI format, `edl.format`), composition id `TransparentBackground`. Never "hack" anywhere.
- Output: 1080×1920, 30 fps, H.264 + AAC, −14 LUFS (±1), no music, no sound effects — via the existing `_loudnorm` + `check_output` in `make_short.py`.
- Reused as is: pause removal (`keep_spans`, >0.3 s, audio silences), cut blending (cuts removing ≤0.5 s blend over 2 frames — `FaceTrack`), captions (`make_captions`, Archivo Medium 41 px white, lowercase, 5–13 words, ≤3 s, `CAPTION_BRIDGE`), safe zone 260 top / 440 bottom / 60 left / 140 right (x 60–940, y 260–1480) from `layout.json`.
- Inputs in job folder `content/video/<date>-<slug>/` (gitignored): `raw/` (one recording), `shots/` (pictures named 1, 2, 3… in spoken order; optional `redact.json` as in ranking), `headline.txt` (Juan's words, shown exactly as he typed them — no case change).
- Hand-edited files, never written by any step once they exist: `pictures.json`, `fixes.json`, `headline.txt`, `shots/redact.json`. Derived files, rewritten every run, never hand-edited: `words.json`, `edl.json`, `review.md`, `matte/`.
- Title: first 3.0 s, black (#000) box, white text, Big Shoulders ExtraBold (`content/scripts/visual/assets/fonts/bigshoulders-extrabold.ttf`, no copy), ≤3 lines, top edge y 300, centred on the safe area's centre x 500, max box width 880 (safe width). No animation.
- Cards: inside the region x 100–900, y 300–920 (top half, inside safe zone), contain-fit and centred in it; 20 px rounded corners, soft shadow (pending Juan's OK — the ranking short has neither); hard cut in, no animation. No card before 3.0 s (title time).
- Full-screen page: picture scaled to 1080 wide, top-anchored, covers the frame (very tall page shows its top 1920 px); Juan's cut-out on top at camera position; captions on top of both.
- Default show: picture height/width ≥ 1.6 → `full`, else `card`. Juan can switch any.
- On-screen time: card 1.5–6.0 s, full 2.0–8.0 s. Each picture starts at the first word of its phrase; ends at the next picture's start, capped at its max (face alone after). Below its min → plan stops.
- Matting: RVM `rvm_resnet50_fp32.onnx` (GitHub release `PeterL1n/RobustVideoMatting` v1.0.0), CUDA provider, `downsample_ratio` 0.25, full 1080×1920, only over each full moment's source range plus 0.5 s warm-up before it (warm-up frames discarded). Output VP9 WebM, `yuva420p`, 30 fps.
- Venv `content/scripts/video/.venv-matte/` and model folder `content/scripts/video/models/` are gitignored. Downloading wheels or the model needs Juan's yes first.
- Hard limits (Claude checks in review, not code): no Mars Men numbers, no ASTEROI client names, no men's-health brands, no Meta ads advice, no paid tool deals; personal data blacked out.

## Review Focus

- Prep re-run after Juan's changes (new transcription, new picture) → `pictures.json`, `fixes.json`, `headline.txt` untouched; caption fixes still applied (Task 5 test).
- A phrase whisper heard differently, or one that comes before the previous picture's → plan stops naming that picture and the words; no render (Task 2 test).
- A picture whose words fall inside the first 3 s → starts at 3.0 s, flagged in review, never under the title (Task 2 test).
- Two pictures' words too close together (card < 1.5 s) → plan stops with both pictures named (Task 2 test).
- A full-screen moment that spans a removed pause → cut-out stays in sync with the face/voice underneath (matte spans mirror the face spans) (Task 4 test).

---

### Task 1: Cut-out tool (matte script + setup)

**Files:**
- Create: `content/scripts/video/matte.py` (runs inside `.venv-matte`; imports only numpy, onnxruntime, stdlib — no repo imports)
- Create: `content/scripts/video/requirements-matte.txt`, `content/scripts/video/setup_matte.ps1`
- Modify: `.gitignore` (add `content/scripts/video/.venv-matte/`, `content/scripts/video/models/`)
- Modify: `tests/video/conftest.py` (add marker `gpu`)
- Test: `tests/video/test_matte.py`

**Interfaces:**
- Produces CLI: `.venv-matte/Scripts/python.exe -I matte.py <src.mp4> <out.webm> --start S --end E [--warmup 0.5] [--model models/rvm_resnet50_fp32.onnx] [--dr 0.25] [--cpu]` → writes VP9 alpha WebM of source seconds [S, E], prints `frames=N seconds=T provider=CUDAExecutionProvider`. Exit 1 with a plain message if CUDA isn't available and `--cpu` wasn't passed.
- Paths (the test computes them itself; Task 5 defines the same in `make_short.py`): `VIDEO_DIR/".venv-matte"/"Scripts"/"python.exe"`, `VIDEO_DIR/"models"/"rvm_resnet50_fp32.onnx"`.

- [ ] **Step 1: Write requirements + setup.** `requirements-matte.txt` pins the set that worked on 2026-11-26: `onnxruntime-gpu==1.32.0`, `numpy==2.5.5`, `nvidia-cuda-runtime==13.5.37`, `nvidia-cudnn-cu13==9.28.1.4`, `nvidia-cublas==13.10.0.20`, `nvidia-cufft==12.5.0.14`, `nvidia-curand==10.4.5.25`, `nvidia-nvjitlink==13.5.37`. `setup_matte.ps1`: `py -3.13 -m venv .venv-matte`; `pip install -r requirements-matte.txt`; model: copy from `$env:LOCALAPPDATA\Temp\claude\6d266a6eef6d0ce4\c1a0c63e-a9a3-4537-9022-72ed6f716258\scratchpad\bgtest\models\rvm_resnet50_fp32.onnx` if present (it still was on 2026-11-27), else `Invoke-WebRequest https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_resnet50_fp32.onnx`; then `python -I -c "import onnxruntime as o; o.preload_dlls(); print(o.get_available_providers())"` must list `CUDAExecutionProvider`. **Ask Juan before running it** (≈2 GB of wheels + 107 MB model).
- [ ] **Step 2: Run setup** — `powershell -File content/scripts/video/setup_matte.ps1` → prints a provider list containing `CUDAExecutionProvider`.
- [ ] **Step 3: Write failing test** `tests/video/test_matte.py`, module-level `pytest.mark.gpu` + `skipif` when the venv python or model is missing. Fixture: ffmpeg `testsrc2` 1080×1920 30 fps 3 s (mechanics only).
  - `test_matte_writes_alpha_webm`: `--start 1.0 --end 2.0` → out exists; `ffprobe` codec `vp9`, tag `alpha_mode` == `"1"`, 1080×1920, `r_frame_rate` 30/1, decoded frame count 30 ± 1 (warm-up frames not written).
  - `test_matte_start_zero_has_no_warmup_before_file_start`: `--start 0 --end 1` → 30 ± 1 frames, exit 0.
- [ ] **Step 4:** `python -m pytest tests/video/test_matte.py -v` → FAIL (no `matte.py`).
- [ ] **Step 5: Implement `matte.py`.** Port the `RVM` class from the 2026-11-26 test harness (same scratchpad folder, `scripts/matte.py`; recurrent state `r1i..r4i`, `preload_dlls()`, CUDA then CPU providers). Read with ffmpeg `-ss max(0, S - warmup) -to E` as rgb24 frames; run every frame (warm-up primes the recurrent state); write only frames at t ≥ S as RGBA (`fgr` × 255, alpha = `pha` × 255) to `ffmpeg -f rawvideo -pix_fmt rgba -r 30 -i - -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 -row-mt 1 -an`. Refuse to run on CPU unless `--cpu`.
- [ ] **Step 6:** same pytest command → PASS (or SKIP with reason if the venv isn't set up).
- [ ] **Step 7: Commit** `add video cut-out tool — Robust Video Matting on the GPU, own venv, alpha WebM`

### Task 2: Picture list (proposal file, phrase matching, timings)

**Files:**
- Create: `content/scripts/video/prep/pictures.py`
- Modify: `content/scripts/video/prep/cuts.py` (add `to_src`)
- Test: `tests/video/test_pictures.py`, `tests/video/test_cuts.py` (add one test)

**Interfaces:**
- Consumes: `Word`, `Span`, `to_out(t, spans)`, `total(spans)`, `list_shots(dir)`, `PrepError`, `image_size(path)`, `scores.normalize(token)`.
- Produces in `cuts.py`: `to_src(t_out: float, spans: list[Span]) -> float` (inverse of `to_out`; clamps to the nearest span edge).
- Produces in `pictures.py`:
  - `@dataclass(frozen=True) PictureChoice(picture: str, words: str, show: Literal["card","full"])`
  - `suggest_show(img_w: int, img_h: int) -> str` — `"full"` if `img_h / img_w >= 1.6`.
  - `write_stub(job: Path) -> bool` — writes `pictures.json` (`[{"picture": "1.png", "words": "", "show": <suggested>}, …]` from `shots/`) **only if it doesn't exist**; returns whether it wrote.
  - `load_choices(job: Path) -> list[PictureChoice]` — PrepError if missing, any `words` empty, a `show` not card/full, a picture name not in `shots/`, or a file in `shots/` not listed.
  - `find_phrase(words: list[Word], phrase: str, after: int = 0) -> int` — index of the phrase's first word: first contiguous match of the normalised tokens at index ≥ `after`; -1 if none.
  - `place(words, choices, spans) -> list[dict]` — each `{"picture","show","words","wordIndex","outStart","outEnd","pushed": bool}`; constants from `layout.json` `transparent` block (Task 3 adds it; if Task 2 runs first, add that block here).

Decision (how pictures get matched to words): Claude reads `words.json` and writes, per picture, the **exact 2–6 words Juan says** where it should land. Code finds them in order and does all the timing. Words, not word numbers or seconds, so the list stays readable for Juan and still works after a re-transcription.

- [ ] **Step 1: Write failing tests** (use `helpers.words_from`, 0.3 s/word, `keep_spans` with no gaps so out = source time):
  - `test_to_src_inverts_to_out`: spans with a removed gap → `to_src(to_out(t)) == t` for spoken t.
  - `test_suggest_show`: 1080×3000 → `"full"`; 1080×1200 → `"card"`; 1200×800 → `"card"`.
  - `test_write_stub_never_overwrites`: write stub, edit `words`, call again → returns False, edit still there.
  - `test_load_choices_rejects_empty_words`, `test_load_choices_rejects_unlisted_picture` → PrepError mentioning the picture name.
  - `test_find_phrase_ignores_case_and_punctuation`: "So, Bloom's page IS great." / phrase `"blooms page is"` → index 1.
  - `test_find_phrase_after`: repeated phrase → second hit when `after` past the first.
  - `test_place_starts_at_phrase_and_ends_at_next`: two cards → `outStart` = first-word start, first `outEnd` == second `outStart`.
  - `test_place_caps_card_at_six_seconds`: next picture 9 s later → `outEnd - outStart == 6.0`.
  - `test_place_last_picture_ends_at_video_end_or_cap`.
  - `test_phrase_not_heard_stops`: PrepError text contains the picture name and the phrase.
  - `test_phrase_before_previous_picture_stops`: PrepError says it comes before the previous picture.
  - `test_picture_inside_title_is_pushed_to_three_seconds`: phrase at 1.2 s → `outStart == 3.0`, `pushed is True`.
  - `test_too_close_stops`: two cards 1.0 s apart → PrepError naming both pictures.
- [ ] **Step 2:** `python -m pytest tests/video/test_pictures.py tests/video/test_cuts.py -v` → new tests FAIL.
- [ ] **Step 3: Implement** `to_src` and `pictures.py`. `place` searches each phrase from the previous match + 1; if not found there but found earlier, raise the "comes before" error.
- [ ] **Step 4:** same command → PASS.
- [ ] **Step 5: Commit** `add video picture list — Claude's proposal Juan can edit, words to timings`

### Task 3: Title box fit + caption fixes

**Files:**
- Create: `content/scripts/video/prep/title.py`, `content/scripts/video/prep/fixes.py`
- Modify: `content/scripts/video/layout.json` (add `"transparent"` block)
- Test: `tests/video/test_title.py`, `tests/video/test_fixes.py`

**Interfaces:**
- `layout.json` adds: `"transparent": {"title": {"top": 300, "centreX": 500, "maxWidth": 880, "padX": 36, "padY": 24, "sizes": [104, 96, 88, 80, 72], "lineHeight": 1.05, "maxLines": 3, "seconds": 3.0, "slack": 1.04}, "card": {"x": 100, "y": 300, "w": 800, "h": 620, "radius": 20}, "caption": {"x": 150, "w": 700}, "fullRatio": 1.6, "minOn": {"card": 1.5, "full": 2.0}, "maxOn": {"card": 6.0, "full": 8.0}}`.
- `title.py`: `fit_title(text: str) -> dict` → `{"lines": list[str], "fontSize": int, "lineHeight": float, "box": {"x","y","w","h"}, "outEnd": 3.0}`. Greedy word wrap measured with Pillow `ImageFont.truetype(bigshoulders-extrabold.ttf, size).getlength(line) * slack`; sizes largest first; PrepError("The headline doesn't fit in 3 lines — shorten it") if none fits; PrepError if empty.
- `fixes.py`: `load_fixes(job: Path) -> dict[str, str]` (`{}` if absent); `apply_fixes(text: str, fixes: dict[str, str]) -> str` (whole-word, case-insensitive, longest key first).

- [ ] **Step 1: Write failing tests:**
  - `test_short_headline_one_line_biggest_size`: "Steal This Page" → 1 line, `fontSize == 104`.
  - `test_long_headline_wraps_to_three_lines_max`: ~12-word headline → `1 <= len(lines) <= 3`, each line width + 2·padX ≤ 880.
  - `test_box_inside_safe_area_and_top_300`: `box.y == 300`, `60 <= box.x`, `box.x + box.w <= 940`, `box.y + box.h < 960`.
  - `test_box_centred_on_500`: `abs(box.x + box.w/2 - 500) <= 1`.
  - `test_headline_keeps_juans_casing`: "the $10M PDP" → lines joined == "the $10M PDP".
  - `test_too_long_headline_stops`, `test_empty_headline_stops` → PrepError.
  - `test_apply_fixes_whole_word_case_insensitive`: "I am 8 is great" + `{"i am 8": "im8"}` → "im8 is great"; "diam 8" unchanged.
  - `test_load_fixes_missing_is_empty`.
- [ ] **Step 2:** `python -m pytest tests/video/test_title.py tests/video/test_fixes.py -v` → FAIL.
- [ ] **Step 3: Implement** both modules + `layout.json` block.
- [ ] **Step 4:** same command → PASS; `python -m pytest tests/video -q` → all old tests still pass.
- [ ] **Step 5: Commit** `add video title box fit and caption fixes that survive re-prep`

### Task 4: Transparent Background edit list + review sheet

**Files:**
- Create: `content/scripts/video/prep/transparent.py`
- Test: `tests/video/test_transparent.py`

**Interfaces:**
- Consumes: `load_choices`, `place` (Task 2); `fit_title`, `load_fixes`, `apply_fixes` (Task 3); `keep_spans`, `to_out`, `to_src`, `total`, `make_captions`, `detect_silences`, `probe`, `image_size`, `list_shots`, `_load_redact`, `SAFE`, `SAFE_Y1`, `CAPTION_BRIDGE`, `PrepError` from existing prep.
- Produces:
  - `build_transparent_edl(job: Path, words: list[Word], silences: list[tuple[float,float]] | None = None) -> dict`:
    `{"format": "transparent", "fps", "width", "height", "video": "job/face.mp4", "duration", "safe", "caption": {"x":150,"y":SAFE_Y1-170,"w":700,"h":170}, "spans": [...], "title": <fit_title of headline.txt>, "pictures": [{"picture","show","words","shot": "job/shots/<name>","box","imgW","imgH","crop","outStart","outEnd","pushed","redact", "matte": null | {"file": "job/matte/<stem>.webm", "srcStart", "srcEnd", "spans": [{"srcStart","srcEnd","outStart"}]}}], "captions": [...]}`
    — card `box` = contain-fit in the card region, centred; full `box` = `{x:0, y:0, w:1080, h:min(1920, scaled height)}`, `crop` true when scaled height > 1920. `matte.spans` = the face spans clipped to [outStart, outEnd], `srcStart/srcEnd` relative to `matte.srcStart`. Captions use `make_captions(words, breaks=[p["wordIndex"] …])`, text through `apply_fixes`.
  - `matte_jobs(edl: dict) -> list[dict]` → `[{"out": "matte/<stem>.webm", "start": srcStart, "end": srcEnd}]` for full pictures.
  - `write_transparent_review(edl: dict, path: Path) -> None` — plain sheet for Juan: headline lines, length; per picture: name, "appears on: “<words>”" at N.N s for N.N s, "card" or "full-screen (you cut out in front)", "moved to 3.0 s so it doesn't cover the title" when pushed, then the captions shown while it's up.

- [ ] **Step 1: Write failing tests** (tmp job with Pillow pictures, `headline.txt`, `pictures.json`, words from `helpers.words_from`, `silences=[]`):
  - `test_edl_has_title_pictures_captions`: `format == "transparent"`, `title.outEnd == 3.0`, picture count == files.
  - `test_card_box_inside_card_region_and_safe_area`: parametrize 1200×675, 1080×1350, 600×600 → box within x 100–900, y 300–920.
  - `test_full_box_covers_width_top_anchored`: 1080×4000 → `box == {x:0,y:0,w:1080,h:1920}`, `crop is True`, `matte.file == "job/matte/2.webm"`.
  - `test_cards_have_no_matte`.
  - `test_matte_spans_mirror_face_spans_across_a_cut`: 1.0 s gap inside the full picture's time → 2 matte spans; each `outStart` equals a face span's `outStart` (or the picture's `outStart` for a clipped first piece); `matte.srcStart + span.srcStart` equals the face span's source start (±0.001).
  - `test_captions_get_fixes`.
  - `test_missing_headline_stops` → PrepError mentioning `headline`.
  - `test_matte_jobs_lists_full_pictures_only`.
  - `test_review_lists_picture_words_show_and_captions`.
  - `test_review_flags_pushed_picture`.
- [ ] **Step 2:** `python -m pytest tests/video/test_transparent.py -v` → FAIL.
- [ ] **Step 3: Implement** `transparent.py`.
- [ ] **Step 4:** same command → PASS.
- [ ] **Step 5: Commit** `add Transparent Background edit list and Juan's check sheet`

### Task 5: Runner — prep / plan / matte / render

**Files:**
- Modify: `content/scripts/video/make_short.py`
- Test: `tests/video/test_make_short.py`

**Interfaces:**
- Consumes: Task 2 `write_stub`; Task 4 `build_transparent_edl`, `matte_jobs`, `write_transparent_review`; Task 1 CLI.
- Constants `MATTE_PY = VIDEO_DIR / ".venv-matte" / "Scripts" / "python.exe"`, `MATTE_MODEL = VIDEO_DIR / "models" / "rvm_resnet50_fp32.onnx"`.
- CLI: `python content/scripts/video/make_short.py transparent <job> --step prep|plan|matte|render|all [--whisper-model small]`. Ranking unchanged (`plan`/`matte` with `ranking` → exit 2).
  - `prep_transparent(job, whisper_model)`: `find_recording` → `normalize` → `transcribe` → `save_words` → `write_stub` → prints "pictures.json ready for words" or "kept your pictures.json". Never writes `edl.json`.
  - `plan_transparent(job) -> Path`: `load_words` → `build_transparent_edl` → writes `edl.json` + `review.md`.
  - `matte_transparent(job)`: per `matte_jobs` entry, skip if `matte/index.json` records same start/end and file exists; else run `[MATTE_PY, "-I", VIDEO_DIR/"matte.py", job/"face.mp4", job/out, "--start", s, "--end", e, "--model", MATTE_MODEL]`. PrepError("Cut-out tool isn't set up — run setup_matte.ps1") if missing. Delete matte files no longer listed; rewrite `index.json`.
  - `render(job)`: composition `{"ranking": "Ranking", "transparent": "TransparentBackground"}[edl["format"]]`; `_stage_media` also copies `job/matte/`; PrepError if a full picture's matte file is missing ("run --step matte").
  - `all` for transparent = plan → matte → render.

- [ ] **Step 1: Write failing tests** (monkeypatch `transcribe`/`normalize`):
  - `test_transparent_prep_writes_stub_once`: prep twice with edited `pictures.json` between → edit kept; `fixes.json`, `headline.txt` byte-identical.
  - `test_transparent_prep_does_not_write_edl`.
  - `test_transparent_plan_with_empty_words_exits_2` (stderr names the picture).
  - `test_transparent_render_without_matte_exits_2`.
  - `test_matte_without_venv_exits_2`.
  - `test_ranking_rejects_plan_step` → 2.
- [ ] **Step 2:** `python -m pytest tests/video/test_make_short.py -v` → new tests FAIL.
- [ ] **Step 3: Implement**; keep exit codes 2 (PrepError) / 3 (RenderError).
- [ ] **Step 4:** same command → PASS; `python -m pytest tests/video -q -m "not slow and not gpu"` → all pass.
- [ ] **Step 5: Commit** `add Transparent Background steps to the video maker — picture list kept across re-prep`

### Task 6: Remotion look — TransparentBackground

**Files:**
- Create: `content/scripts/video/src/TransparentBackground.tsx`, `src/parts/TitleBox.tsx`, `src/parts/Card.tsx`, `src/parts/FullPage.tsx`
- Modify: `src/edl.ts`, `src/Root.tsx`, `src/fonts.ts`, `src/parts/FaceTrack.tsx`, `src/parts/Shot.tsx` (extract shared `Redactions`), `package.json` (`still:tb`)
- Create: `sample/edl.transparent.sample.json`; Modify: `sample/make_sample.py` (`transparent` argument: sample face, one card picture, one tall page, sample alpha WebM via ffmpeg `color=c=black@0.0` + white circle, `yuva420p`)

**Interfaces:**
- `edl.ts`: `TitleLayout = {lines: string[]; fontSize: number; lineHeight: number; box: Box; outEnd: number}`, `Matte = {file: string; srcStart: number; srcEnd: number; spans: Span[]}`, `Picture = {picture; show: "card" | "full"; shot; box: Box; imgW; imgH; crop: boolean; outStart; outEnd; pushed: boolean; redact: Box[]; matte: Matte | null}`, `TransparentEdl = {format: "transparent"; fps; width; height; video; duration; safe: Box; caption: Box; spans: Span[]; title: TitleLayout; pictures: Picture[]; captions: Caption[]}`, `TransparentProps = TransparentEdl & Record<string, unknown>`.
- `FaceTrack` gains `transparent?: boolean` (to `OffthreadVideo transparent`) and `muted?: boolean`. Defaults keep ranking identical.
- `fonts.ts`: `TITLE_FONT = "Big Shoulders"`, `loadFont` of `../../visual/assets/fonts/bigshoulders-extrabold.ttf` weight `"800"`.
- Layers (bottom → top): `FaceTrack` (audio) → per full picture: `FullPage` (Sequence from `outStart`) then cut-out `FaceTrack video={matte.file} spans={matte.spans} transparent muted` (matte `outStart`s are absolute — place outside the Sequence or offset) → `Card`s → `TitleBox` (0 → `toFrame(title.outEnd)`) → `Captions` (`box={edl.caption}`).
- `Card`: absolute at `box`, radius from layout, `boxShadow: "0 8px 28px rgba(0,0,0,0.35)"`, `overflow: hidden`, `Redactions` on top.
- `TitleBox`: absolute at `title.box`, `#000`, one `<div>` per line, `whiteSpace: "nowrap"`, centred, weight 800, white.

- [ ] **Step 1:** `python content/scripts/video/sample/make_sample.py transparent` → `public/job/` has `face.mp4`, `shots/1.png`, `shots/2.png`, `matte/2.webm`.
- [ ] **Step 2:** `cd content/scripts/video; npx tsc --noEmit` → fails first.
- [ ] **Step 3: Implement.**
- [ ] **Step 4:** typecheck → clean.
- [ ] **Step 5: Stills, look at each:** `npx remotion still src/index.ts TransparentBackground out/tb-title.png --props=sample/edl.transparent.sample.json --frame=30` → title box near top; a card frame → rounded card in top half, no title; a full frame → page fills frame, white circle on top, captions over both. If the WebM doesn't show see-through, check the Remotion 4.0.547 docs for `OffthreadVideo transparent` before changing approach.
- [ ] **Step 6: Ranking unchanged** — `python sample/make_sample.py`; `npx remotion still src/index.ts Ranking out/still-check.png --props=sample/edl.sample.json --frame=45` → matches `out/still.png` (ffmpeg `psnr` > 40 dB).
- [ ] **Step 7: Commit** `add Transparent Background look to the Remotion project — title box, cards, full page with cut-out`

### Task 7: End-to-end test

**Files:** Modify `tests/video/test_e2e.py` (reuse `_speak` and the synthetic video builder).

- [ ] **Step 1:** `test_e2e_transparent` (`@pytest.mark.slow`): SAPI speaks three sentences; `headline.txt` "Steal These Three Pages", two wide pictures + one 1080×4000 page; `prep`; fill `pictures.json`; tall one `full` only if the matte venv exists; `--step all`. Asserts: exit 0; 1080×1920, 30 fps, LUFS −14 ± 1; frame at 1.5 s title box mean luma < 40; a card frame differs from plain face in the card region; `outStart`s strictly increase, first ≥ 3.0.
- [ ] **Step 2:** `python -m pytest tests/video/test_e2e.py -v -m slow` → PASS. Copy to `content/scripts/video/out/e2e-transparent.mp4`, look at one frame per part.
- [ ] **Step 3:** `python -m pytest tests/video -q` → all pass (gpu tests pass or skip).
- [ ] **Step 4: Commit** `add end-to-end test for the Transparent Background short`

### Task 8: Skill + Juan's first real video

**Files:**
- Modify: `.claude/skills/video-edit/SKILL.md`
- Modify: `docs/superpowers/specs/2026-11-26-short-video-skills-design.md` (`updated:` date; "Test script kept at …scratchpad…" → "Cut-out tool: `content/scripts/video/matte.py`, set up with `setup_matte.ps1`")

- [ ] **Step 1: Update the skill.** Description covers ranking **and** Transparent Background (triggers: "transparent background", "cut-out short", recording + pictures + headline). Remove "Ranking format only for now". Add a Transparent Background section:
  - Juan hands over: original recording (not WhatsApp), pictures named 1, 2, 3… in spoken order, the headline in his words. Plain, evenly lit wall works best for full-screen moments.
  - Steps: job folder + `headline.txt` → `--step prep` → Claude fills `pictures.json` (exact 2–6 words per picture, card or full) → look at every picture, black out personal data, screen hard limits → `--step plan` → show Juan the check list in chat (headline; each picture by what it shows, its words, card or full-screen, captions under it) → apply changes, re-run `--step plan` until OK → `--step matte` → `--step render` → watch frames → send.
  - Rules: caption fixes in `fixes.json`, never hand-edit `edl.json`. Never call this format anything but Transparent Background.
- [ ] **Step 2: First real video (with Juan).** Before showing the check list, run `--step matte` on the first full-screen moment and look at three frames (hair, hands, edge against the painting wall). If rough, tell Juan in one line and recommend a plain wall next time; render only if he accepts the look.
- [ ] **Step 3:** `python -m pytest tests/video -q` → all pass.
- [ ] **Step 4: Commit** `update video-edit skill, short-video-skills-design.md — Transparent Background short built`

---

## Self-review

- **Spec coverage:** inputs → Tasks 2, 4, 5; title box → 3, 6; room + cards on his words → 2, 4, 6; full-screen cut-out moments, Juan can switch → 1, 2, 4, 6; Claude proposes, Juan checks one list → 2, 4, 8; reused captions/cuts/loudness/safe zones → 4, 5, 6; RVM setup moved into repo → 1; cut-out test on first recording → 8; skill + Remotion 4.0.547 → 5–8; hard limits + redaction → 8.
- **Known gotcha avoided:** prep never rewrites hand-edited files; `edl.json` derived (Task 5 test).
- **Type consistency:** `place` keys → Task 4; Task 4 edl keys → Task 6 types; `matte_jobs` → Task 5; venv/model paths identical in Tasks 1 and 5.
