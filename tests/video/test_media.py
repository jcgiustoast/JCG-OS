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


def test_detect_silences_finds_the_quiet_stretch(tmp_path):
    from content.scripts.video.prep.media import detect_silences

    # 1 s tone, 0.8 s near-silence (faint noise, like a room), 1 s tone
    wav = tmp_path / "a.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", "sine=frequency=300:duration=1",
            "-f", "lavfi", "-i", "anoisesrc=d=0.8:a=0.002",
            "-f", "lavfi", "-i", "sine=frequency=300:duration=1",
            "-filter_complex", "[0][1][2]concat=n=3:v=0:a=1", str(wav),
        ],
        check=True,
    )
    found = detect_silences(wav, min_len=0.3)
    assert len(found) == 1
    a, b = found[0]
    assert a == pytest.approx(1.0, abs=0.05) and b == pytest.approx(1.8, abs=0.05)


def test_image_size_follows_exif_rotation(tmp_path):
    p = tmp_path / "phone.jpg"
    im = Image.new("RGB", (300, 700))
    exif = Image.Exif()
    exif[0x0112] = 6  # stored sideways; shown rotated 90 degrees
    im.save(p, exif=exif)
    assert image_size(p) == (700, 300)
