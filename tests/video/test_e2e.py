"""Whole pipeline: a spoken recording + three screenshots in, a finished short out."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
MAKE_SHORT = REPO / "content" / "scripts" / "video" / "make_short.py"
KEEP_COPY = REPO / "content" / "scripts" / "video" / "out" / "e2e.mp4"

SENTENCES = [
    "this is a zero out of ten email.",
    "this one is a seven out of ten.",
    "and this is a ten out of ten.",
]


def _speak(wav: Path) -> None:
    """Windows SAPI voice reading the three sentences with 0.8 s pauses."""
    parts = ["$p = New-Object System.Speech.Synthesis.PromptBuilder",
             "$p.AppendBreak([TimeSpan]::FromMilliseconds(600))"]
    for s in SENTENCES:
        parts.append(f"$p.AppendText('{s}')")
        parts.append("$p.AppendBreak([TimeSpan]::FromMilliseconds(800))")
    script = "; ".join([
        "Add-Type -AssemblyName System.Speech",
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer",
        "$s.Rate = -1",
        *parts,
        f"$s.SetOutputToWaveFile('{wav}')",
        "$s.Speak($p)",
        "$s.Dispose()",
    ])
    subprocess.run(["powershell", "-NoProfile", "-Command", script], check=True)


def _shot(path: Path, w: int, h: int, colour) -> None:
    im = Image.new("RGB", (w, h), (253, 246, 236))
    d = ImageDraw.Draw(im)
    d.rectangle([w * 0.1, 40, w * 0.9, 140], fill=colour)
    for y in range(200, h - 100, 120):
        d.rectangle([60, y, w * 0.8, y + 50], fill=(140, 140, 140))
    im.save(path)


def _make_job(root: Path) -> Path:
    job = root / "2026-11-26-e2e"
    (job / "raw").mkdir(parents=True)
    (job / "shots").mkdir()
    wav = root / "speech.wav"
    _speak(wav)
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", "color=c=0x8a7f74:s=1080x1920:r=30",
            "-i", str(wav),
            "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
            str(job / "raw" / "recording.mp4"),
        ],
        check=True,
    )
    _shot(job / "shots" / "1.png", 1080, 1800, (200, 40, 40))   # tall
    _shot(job / "shots" / "2.png", 1600, 1000, (40, 120, 200))  # wide
    _shot(job / "shots" / "3.png", 1080, 6000, (40, 160, 80))   # very tall -> cropped
    return job


@pytest.mark.slow
@pytest.mark.skipif(sys.platform != "win32", reason="uses Windows SAPI speech")
def test_e2e_ranking(tmp_path):
    from content.scripts.video.make_short import check_output
    from content.scripts.video.prep.media import probe

    job = _make_job(tmp_path)
    result = subprocess.run(
        [sys.executable, str(MAKE_SHORT), "ranking", str(job), "--step", "all",
         "--whisper-model", "base"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout[-3000:] + result.stderr[-3000:]

    edl = json.loads((job / "edl.json").read_text(encoding="utf-8"))
    assert [i["score"] for i in edl["items"]] == [0, 7, 10]
    assert (job / "review.md").exists()

    final = job / "out" / f"{job.name}.mp4"
    assert final.exists()
    info = check_output(final)
    assert (info["width"], info["height"]) == (1080, 1920)
    assert info["fps"] == pytest.approx(30, abs=0.01)
    assert -15 <= info["lufs"] <= -13

    assert probe(final)["duration"] < probe(job / "raw" / "recording.mp4")["duration"]

    KEEP_COPY.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final, KEEP_COPY)
    shutil.copy2(job / "edl.json", KEEP_COPY.with_suffix(".edl.json"))
