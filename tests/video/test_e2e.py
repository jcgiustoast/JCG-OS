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


T_SENTENCES = [
    "so today i will show you three pages that are worth stealing right now.",
    "first, look at this pricing page with the big bold headline and the clear button.",
    "second, this landing page puts the proof right under the offer.",
    "third, this long sales page walks you through every single objection.",
    "and that is why it keeps selling for them day after day.",
]
T_PHRASES = ["pricing page", "landing page", "sales page"]
MATTE_PY = REPO / "content" / "scripts" / "video" / ".venv-matte" / "Scripts" / "python.exe"
MATTE_MODEL = REPO / "content" / "scripts" / "video" / "models" / "rvm_resnet50_fp32.onnx"
T_KEEP_COPY = REPO / "content" / "scripts" / "video" / "out" / "e2e-transparent.mp4"


def _speak_transparent(wav: Path) -> None:
    parts = ["$p = New-Object System.Speech.Synthesis.PromptBuilder"]
    for s in T_SENTENCES:
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


def _page(path: Path, w: int, h: int, colour) -> None:
    im = Image.new("RGB", (w, h), (253, 246, 236))
    d = ImageDraw.Draw(im)
    d.rectangle([w * 0.1, 40, w * 0.9, 140], fill=colour)
    for y in range(200, h - 100, 120):
        d.rectangle([60, y, w * 0.8, y + 50], fill=(140, 140, 140))
    im.save(path)


def _frame_luma(video: Path, t: float, crop: str | None = None) -> float:
    vf = (crop + "," if crop else "") + "scale=1:1:flags=area,format=gray"
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(video), "-frames:v", "1",
         "-vf", vf, "-f", "rawvideo", "-"],
        capture_output=True, check=True,
    ).stdout
    return out[0]


@pytest.mark.slow
@pytest.mark.skipif(sys.platform != "win32", reason="uses Windows SAPI speech")
def test_e2e_transparent(tmp_path):
    from content.scripts.video.make_short import check_output

    job = tmp_path / "2026-11-27-e2e-transparent"
    (job / "raw").mkdir(parents=True)
    (job / "shots").mkdir()
    wav = tmp_path / "speech.wav"
    _speak_transparent(wav)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "lavfi", "-i", "color=c=0x8a7f74:s=1080x1920:r=30",
         "-i", str(wav), "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
         str(job / "raw" / "recording.mp4")],
        check=True)
    _page(job / "shots" / "1.png", 1600, 1000, (40, 120, 200))
    _page(job / "shots" / "2.png", 1500, 1000, (200, 40, 40))
    _page(job / "shots" / "3.png", 1080, 4000, (40, 160, 80))
    (job / "headline.txt").write_text("Steal These Three Pages", encoding="utf-8")

    def run(step):
        return subprocess.run(
            [sys.executable, str(MAKE_SHORT), "transparent", str(job), "--step", step,
             "--whisper-model", "base"],
            cwd=REPO, capture_output=True, text=True)

    r = run("prep")
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
    heard = " ".join(w["text"] for w in json.loads((job / "words.json").read_text(encoding="utf-8")))
    stub = json.loads((job / "pictures.json").read_text(encoding="utf-8"))
    assert [p["show"] for p in stub] == ["card", "card", "full"]

    can_matte = MATTE_PY.exists() and MATTE_MODEL.exists()
    rows = [{"picture": p["picture"], "words": T_PHRASES[i],
             "show": p["show"] if (p["show"] == "card" or can_matte) else "card"}
            for i, p in enumerate(stub)]
    for row in rows:
        assert row["words"].split()[0] in heard.lower(), heard
    (job / "pictures.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    result = run("all")
    if result.returncode != 0 and "No frame found at position" in result.stdout:
        # Remotion's frame reader intermittently fails on face.mp4 (same file, passes on retry);
        # the cut-out is cached by now, so the retry only re-renders.
        result = run("all")
    noise = ("Rendered ", "Encoded ", "Bundling ")
    shown = chr(10).join(ln for ln in result.stdout.splitlines() if not ln.startswith(noise))
    assert result.returncode == 0, shown[-4000:] + result.stderr[:3000]

    final = job / "out" / f"{job.name}.mp4"
    assert final.exists()
    info = check_output(final)
    assert (info["width"], info["height"]) == (1080, 1920)
    assert info["fps"] == pytest.approx(30, abs=0.01)
    assert -15 <= info["lufs"] <= -13

    # title box: empty corner of the box (right of the short last line) is black at 1.5 s
    assert _frame_luma(final, 1.5, "crop=180:80:700:470") < 40

    edl = json.loads((job / "edl.json").read_text(encoding="utf-8"))
    starts = [p["outStart"] for p in edl["pictures"]]
    assert starts == sorted(set(starts)) and len(starts) == 3
    assert starts[0] >= 3.0

    # a card frame differs from the plain face in the card region
    card_t = starts[0] + 0.5
    card = _frame_luma(final, card_t, "crop=800:620:100:300")
    face = _frame_luma(final, 2.9, "crop=800:620:100:300")
    assert abs(card - face) > 5

    T_KEEP_COPY.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final, T_KEEP_COPY)
    shutil.copy2(job / "edl.json", T_KEEP_COPY.with_suffix(".edl.json"))
    shutil.copy2(job / "words.json", T_KEEP_COPY.with_suffix(".words.json"))
