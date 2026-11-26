"""ffmpeg helpers: make any phone recording a clean 1080x1920 30 fps file."""
from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path

from PIL import Image

WIDTH, HEIGHT, FPS = 1080, 1920, 30


def normalize(src: Path, dst: Path) -> None:
    """Rotate per phone metadata, fill + centre-crop to 1080x1920, 30 fps, H.264/AAC."""
    vf = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT},fps={FPS},format=yuv420p,setsar=1"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart",
            str(dst),
        ],
        check=True,
    )


def probe(path: Path) -> dict:
    out = subprocess.run(
        [
            "ffprobe", "-v", "error", "-print_format", "json",
            "-show_streams", "-show_format", str(path),
        ],
        check=True, capture_output=True, text=True,
    ).stdout
    data = json.loads(out)
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    return {
        "width": int(video["width"]),
        "height": int(video["height"]),
        "fps": float(Fraction(video["r_frame_rate"])),
        "duration": float(data["format"]["duration"]),
        "has_audio": any(s["codec_type"] == "audio" for s in data["streams"]),
    }


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size
