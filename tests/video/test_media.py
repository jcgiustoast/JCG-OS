import subprocess

import pytest
from PIL import Image

from content.scripts.video.prep.media import image_size, normalize, probe


def _make_clip(path, w, h, fps, seconds=3):
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", f"testsrc2=size={w}x{h}:rate={fps}:duration={seconds}",
            "-f", "lavfi", "-i", f"sine=frequency=440:duration={seconds}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(path),
        ],
        check=True,
    )


def test_normalize_landscape_60fps(tmp_path):
    src = tmp_path / "in.mp4"
    dst = tmp_path / "face.mp4"
    _make_clip(src, 1920, 1080, 60)
    normalize(src, dst)
    info = probe(dst)
    assert (info["width"], info["height"]) == (1080, 1920)
    assert info["fps"] == pytest.approx(30, abs=0.01)
    assert info["has_audio"]
    assert info["duration"] == pytest.approx(3, abs=0.2)


def test_image_size(tmp_path):
    p = tmp_path / "a.png"
    Image.new("RGB", (300, 700)).save(p)
    assert image_size(p) == (300, 700)
