"""Build the media that sample/edl.sample.json points at, inside public/job/.

    python content/scripts/video/sample/make_sample.py              (ranking)
    python content/scripts/video/sample/make_sample.py transparent  (Transparent Background)
    cd content/scripts/video
    npx remotion still src/index.ts Ranking out/still.png --props=sample/edl.sample.json --frame=45
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

VIDEO_DIR = Path(__file__).resolve().parents[1]
JOB = VIDEO_DIR / "public" / "job"


def fake_email(path: Path, w: int, h: int) -> None:
    """A cream 'order email': header bar, text lines, a card, an address block."""
    im = Image.new("RGB", (w, h), (253, 246, 236))
    d = ImageDraw.Draw(im)
    d.rectangle([w * 0.3, 40, w * 0.7, 90], fill=(40, 40, 40))
    d.rectangle([w * 0.1, 150, w * 0.9, 230], fill=(20, 20, 20))
    y = 300
    while y < h - 120:
        d.rounded_rectangle([60, y, w - 60, y + 300], radius=20, outline=(60, 60, 60), width=4)
        for k in range(4):
            d.rectangle([100, y + 40 + k * 60, w * (0.85 - 0.1 * k), y + 70 + k * 60], fill=(120, 120, 120))
        y += 380
    d.rectangle([60, 1200, 460, 1310], fill=(150, 150, 150))  # 'address' (redacted in sample)
    im.save(path)


def alpha_webm(path: Path, src_start: float, seconds: float) -> None:
    """See-through clip standing in for the cut-out: a white circle whose x follows
    the SOURCE time (src_start + t) plus that time as text, so a still shows whether
    it is in step with the timestamp burned into face.mp4."""
    path.parent.mkdir(parents=True, exist_ok=True)
    src_t = f"({src_start}+T)"
    font = r"C\:/Windows/Fonts/arial.ttf"
    vf = (
        f"color=c=black@0.0:s=1080x1920:r=30:d={seconds},format=rgba,"
        f"geq=r='255':g='255':b='255':a='if(lt(hypot(X-(100+120*{src_t}),Y-1300),200),255,0)',"
        rf"drawtext=fontfile='{font}':text='src %{{eif\:{src_start}+t\:d}}.%{{eif\:mod(({src_start}+t)*10\,10)\:d}}':"
        "fontsize=90:fontcolor=red:box=1:boxcolor=black:x=300:y=1000,"
        "format=yuva420p"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", vf,
         "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-auto-alt-ref", "0", str(path)],
        check=True,
    )


def main() -> None:
    transparent = "transparent" in sys.argv[1:]
    if JOB.exists():
        shutil.rmtree(JOB)
    (JOB / "shots").mkdir(parents=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30:duration=8",
            "-f", "lavfi", "-i", "sine=frequency=330:duration=8",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
            str(JOB / "face.mp4"),
        ],
        check=True,
    )
    fake_email(JOB / "shots" / "1.png", 1080, 1800)
    fake_email(JOB / "shots" / "2.png", 1080, 6000)
    if transparent:
        alpha_webm(JOB / "matte" / "2.webm", src_start=5.0, seconds=2.5)
    print(f"sample media written to {JOB}")


if __name__ == "__main__":
    main()
