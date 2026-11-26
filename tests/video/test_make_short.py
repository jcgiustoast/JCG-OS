"""Fast checks on the runner (the full pipeline is in test_e2e.py)."""
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
MAKE_SHORT = REPO / "content" / "scripts" / "video" / "make_short.py"


def _run(*args):
    return subprocess.run(
        [sys.executable, str(MAKE_SHORT), *args], cwd=REPO, capture_output=True, text=True
    )


def test_prep_without_recording_exits_2(tmp_path):
    job = tmp_path / "job"
    (job / "raw").mkdir(parents=True)
    (job / "shots").mkdir()
    result = _run("ranking", str(job), "--step", "prep")
    assert result.returncode == 2
    assert "raw" in (result.stdout + result.stderr)


def test_prep_with_two_recordings_exits_2(tmp_path):
    job = tmp_path / "job"
    (job / "raw").mkdir(parents=True)
    (job / "raw" / "a.mp4").write_bytes(b"")
    (job / "raw" / "b.MOV").write_bytes(b"")
    result = _run("ranking", str(job), "--step", "prep")
    assert result.returncode == 2
    assert "a.mp4" in result.stdout + result.stderr


def test_check_output_reads_size_fps_loudness(tmp_path):
    from content.scripts.video.make_short import check_output

    clip = tmp_path / "c.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", "color=c=gray:s=1080x1920:r=30:d=3",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(clip),
        ],
        check=True,
    )
    info = check_output(clip)
    assert (info["width"], info["height"]) == (1080, 1920)
    assert info["fps"] == pytest.approx(30, abs=0.01)
    assert -40 < info["lufs"] < 0  # ffmpeg's sine is ~-21 LUFS
