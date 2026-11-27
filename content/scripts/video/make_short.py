"""Raw recording in, finished ranking short out.

    python content/scripts/video/make_short.py ranking <job_dir> --step prep|render|all [--whisper-model small]

Job folder: raw/ (one recording), shots/ (1.png, 2.png, ...; optional redact.json).
prep   -> face.mp4, words.json, edl.json, review.md
render -> out/render.mp4 (Remotion), out/<job-name>.mp4 (loudness -14 LUFS, checked)

    python content/scripts/video/make_short.py transparent <job_dir> --step prep|plan|matte|render|all

prep   -> face.mp4, words.json, pictures.json (stub, never overwritten)
plan   -> edl.json, review.md (needs headline.txt and Claude's pictures.json)
matte  -> matte/*.webm (cut-out of Juan for each full-screen picture, GPU)
render -> as ranking; "all" for transparent = plan, matte, render
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

VIDEO_DIR = Path(__file__).resolve().parent
REPO = VIDEO_DIR.parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from content.scripts.video.prep.edl import PrepError, build_ranking_edl, write_review  # noqa: E402
from content.scripts.video.prep.media import FPS, HEIGHT, WIDTH, normalize, probe  # noqa: E402
from content.scripts.video.prep.pictures import write_stub  # noqa: E402
from content.scripts.video.prep.transparent import (  # noqa: E402
    build_transparent_edl,
    matte_jobs,
    write_transparent_review,
)
from content.scripts.video.prep.words import load_words, save_words  # noqa: E402

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".webm"}
PUBLIC_JOB = VIDEO_DIR / "public" / "job"
MATTE_PY = VIDEO_DIR / ".venv-matte" / "Scripts" / "python.exe"
MATTE_MODEL = VIDEO_DIR / "models" / "rvm_resnet50_fp32.onnx"
COMPOSITIONS = {"ranking": "Ranking", "transparent": "TransparentBackground"}
TARGET_LUFS = -14.0
LUFS_TOLERANCE = 1.0


class RenderError(Exception):
    """The finished file doesn't meet the output spec."""


def find_recording(job: Path) -> Path:
    raw = job / "raw"
    videos = sorted(p for p in raw.iterdir() if p.suffix.lower() in VIDEO_EXTS) if raw.is_dir() else []
    if not videos:
        raise PrepError(f"No recording found in {raw}. Put exactly one video file there.")
    if len(videos) > 1:
        names = ", ".join(p.name for p in videos)
        raise PrepError(f"Found {len(videos)} recordings in {raw} ({names}). Keep exactly one.")
    return videos[0]


def prep(job: Path, whisper_model: str = "small") -> Path:
    from content.scripts.video.prep.transcribe import transcribe  # loads whisper; keep lazy

    job = Path(job)
    recording = find_recording(job)
    face = job / "face.mp4"
    print(f"normalising {recording.name} -> face.mp4", flush=True)
    normalize(recording, face)
    print(f"transcribing (whisper {whisper_model})", flush=True)
    words = transcribe(face, model=whisper_model)
    save_words(words, job / "words.json")
    edl = build_ranking_edl(job, words)
    edl_path = job / "edl.json"
    edl_path.write_text(json.dumps(edl, indent=1, ensure_ascii=False), encoding="utf-8")
    write_review(edl, job / "review.md")
    print(f"review: {job / 'review.md'}", flush=True)
    return edl_path


def prep_transparent(job: Path, whisper_model: str = "small") -> None:
    from content.scripts.video.prep.transcribe import transcribe  # loads whisper; keep lazy

    job = Path(job)
    recording = find_recording(job)
    face = job / "face.mp4"
    print(f"normalising {recording.name} -> face.mp4", flush=True)
    normalize(recording, face)
    print(f"transcribing (whisper {whisper_model})", flush=True)
    words = transcribe(face, model=whisper_model)
    save_words(words, job / "words.json")
    if write_stub(job):
        print("pictures.json ready for words", flush=True)
    else:
        print("kept your pictures.json", flush=True)


def plan_transparent(job: Path) -> Path:
    job = Path(job)
    words_path = job / "words.json"
    if not words_path.exists():
        raise PrepError(f"No words.json in {job}. Run --step prep first.")
    edl = build_transparent_edl(job, load_words(words_path), None)
    edl_path = job / "edl.json"
    edl_path.write_text(json.dumps(edl, indent=1, ensure_ascii=False), encoding="utf-8")
    write_transparent_review(edl, job / "review.md")
    print(f"review: {job / 'review.md'}", flush=True)
    return edl_path


def _face_key(job: Path) -> list | None:
    """Identity of the current face.mp4, so cut-outs made from another take are never reused."""
    face = Path(job) / "face.mp4"
    if not face.exists():
        return None
    st = face.stat()
    return [st.st_mtime_ns, st.st_size]


def matte_transparent(job: Path) -> None:
    job = Path(job)
    edl_path = job / "edl.json"
    if not edl_path.exists():
        raise PrepError(f"No edl.json in {job}. Run --step plan first.")
    todo = matte_jobs(json.loads(edl_path.read_text(encoding="utf-8")))
    if todo and not (MATTE_PY.exists() and MATTE_MODEL.exists()):
        raise PrepError("Cut-out tool isn't set up — run setup_matte.ps1")
    matte_dir = job / "matte"
    matte_dir.mkdir(exist_ok=True)
    index_path = matte_dir / "index.json"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        index = {}
    face_key = _face_key(job)
    wanted = {Path(m["out"]).name for m in todo}
    for f in matte_dir.iterdir():
        if f.name != "index.json" and f.name not in wanted:
            f.unlink()
            index.pop(f.name, None)
    index = {k: v for k, v in index.items() if k in wanted}
    index_path.write_text(json.dumps(index, indent=1), encoding="utf-8")
    for m in todo:
        name = Path(m["out"]).name
        rec = {"start": m["start"], "end": m["end"], "face": face_key}
        if index.get(name) == rec and (job / m["out"]).exists():
            print(f"cut-out {name}: already done", flush=True)
            continue
        # drop the record first, so a crash can't leave a half-written clip counted as done
        index.pop(name, None)
        index_path.write_text(json.dumps(index, indent=1), encoding="utf-8")
        print(f"cutting out {name} ({m['start']:.2f}-{m['end']:.2f} s)", flush=True)
        res = subprocess.run(
            [str(MATTE_PY), "-I", str(VIDEO_DIR / "matte.py"), str(job / "face.mp4"),
             str(job / m["out"]), "--start", str(m["start"]), "--end", str(m["end"]),
             "--model", str(MATTE_MODEL)],
        )
        if res.returncode != 0:
            raise PrepError(f"The cut-out tool failed on {name} (exit {res.returncode}).")
        index[name] = rec
        index_path.write_text(json.dumps(index, indent=1), encoding="utf-8")


def _stage_media(job: Path) -> None:
    if PUBLIC_JOB.exists():
        shutil.rmtree(PUBLIC_JOB)
    PUBLIC_JOB.mkdir(parents=True)
    shutil.copy2(job / "face.mp4", PUBLIC_JOB / "face.mp4")
    shutil.copytree(job / "shots", PUBLIC_JOB / "shots")
    if (job / "matte").is_dir():
        shutil.copytree(job / "matte", PUBLIC_JOB / "matte")


def _npx() -> str:
    return shutil.which("npx") or ("npx.cmd" if sys.platform == "win32" else "npx")


def _loudnorm(src: Path, dst: Path) -> None:
    """Two-pass EBU R128 loudness to -14 LUFS; video stream copied untouched."""
    target = f"I={TARGET_LUFS}:TP=-1:LRA=11"
    first = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(src),
         "-af", f"loudnorm={target}:print_format=json", "-f", "null", "-"],
        check=True, capture_output=True, text=True,
    )
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", first.stderr)
    if not m:
        raise RenderError("Couldn't measure loudness (ffmpeg loudnorm gave no stats).")
    stats = json.loads(m.group())
    second = (
        f"loudnorm={target}:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}"
        f":measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}"
        f":offset={stats['target_offset']}:linear=true"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", second,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-movflags", "+faststart", str(dst)],
        check=True,
    )


def check_output(path: Path) -> dict:
    """Size, frame rate and integrated loudness (LUFS) of a finished file."""
    info = probe(path)
    meter = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-filter_complex", "ebur128", "-f", "null", "-"],
        check=True, capture_output=True, text=True,
    ).stderr
    summary = meter[meter.rfind("Summary:"):]
    m = re.search(r"I:\s*(-?[\d.]+|-inf)\s*LUFS", summary)
    if not m:
        raise RenderError(f"Couldn't read loudness of {path}.")
    lufs = float(m.group(1)) if m.group(1) != "-inf" else float("-inf")
    return {"width": info["width"], "height": info["height"], "fps": info["fps"], "lufs": lufs}


def render(job: Path) -> Path:
    job = Path(job).resolve()
    edl_path = job / "edl.json"
    if not edl_path.exists():
        raise PrepError(f"No edl.json in {job}. Run --step prep first.")
    edl = json.loads(edl_path.read_text(encoding="utf-8"))
    try:
        index = json.loads((job / "matte" / "index.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        index = {}
    for p in edl.get("pictures", []):
        m = p.get("matte")
        if not m:
            continue
        name = Path(m["file"]).name
        rec = index.get(name)
        fresh = (job / "matte" / name).exists() and rec and (rec["start"], rec["end"]) == (m["srcStart"], m["srcEnd"]) and rec.get("face") == _face_key(job)
        if not fresh:
            raise PrepError(f"Picture {p['picture']} needs its cut-out but the matte file is missing or out of date. Run --step matte.")
    _stage_media(job)
    out_dir = job / "out"
    out_dir.mkdir(exist_ok=True)
    raw_render = out_dir / "render.mp4"

    started = time.monotonic()
    subprocess.run(
        [_npx(), "remotion", "render", "src/index.ts", COMPOSITIONS[edl.get("format", "ranking")], str(raw_render),
         f"--props={edl_path}"],
        cwd=VIDEO_DIR, check=True,
    )
    print(f"remotion render took {time.monotonic() - started:.1f} s", flush=True)

    final = out_dir / f"{job.name}.mp4"
    _loudnorm(raw_render, final)

    info = check_output(final)
    problems = []
    if (info["width"], info["height"]) != (WIDTH, HEIGHT):
        problems.append(f"size {info['width']}x{info['height']}, want {WIDTH}x{HEIGHT}")
    if abs(info["fps"] - FPS) > 0.01:
        problems.append(f"{info['fps']} fps, want {FPS}")
    if abs(info["lufs"] - TARGET_LUFS) > LUFS_TOLERANCE:
        problems.append(f"loudness {info['lufs']} LUFS, want {TARGET_LUFS} +/- {LUFS_TOLERANCE}")
    if problems:
        raise RenderError(f"{final} is off: " + "; ".join(problems))
    print(f"done: {final} ({info['width']}x{info['height']}, {info['fps']:g} fps, "
          f"{info['lufs']} LUFS)", flush=True)
    return final


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("format", choices=["ranking", "transparent"])
    ap.add_argument("job", type=Path)
    ap.add_argument("--step", choices=["prep", "plan", "matte", "render", "all"], default="all")
    ap.add_argument("--whisper-model", default="small")
    args = ap.parse_args(argv)

    try:
        if args.format == "ranking":
            if args.step in ("plan", "matte"):
                raise PrepError(f"The ranking short has no {args.step} step. Use prep or render.")
            if args.step in ("prep", "all"):
                prep(args.job, args.whisper_model)
        else:
            if args.step == "prep":
                prep_transparent(args.job, args.whisper_model)
            if args.step in ("plan", "all"):
                plan_transparent(args.job)
            if args.step in ("matte", "all"):
                matte_transparent(args.job)
        if args.step in ("render", "all"):
            render(args.job)
    except PrepError as e:
        print(f"stopped: {e}", file=sys.stderr)
        return 2
    except RenderError as e:
        print(f"render check failed: {e}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
