"""ffmpeg helpers: make any phone recording a clean 1080x1920 30 fps file."""
from __future__ import annotations

import json
import math
import subprocess
from array import array
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageOps

from .cuts import find_silences, speech_threshold

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
        return ImageOps.exif_transpose(im).size  # as a browser shows it (phone photos carry a rotation)


LEVEL_STEP = 0.02  # seconds per loudness window
LEVEL_RATE = 16000


def audio_levels(path: Path, step: float = LEVEL_STEP) -> list[float]:
    """Loudness (dB, RMS) of each `step`-second window of the file's audio."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
         "-ar", str(LEVEL_RATE), "-f", "s16le", "-"],
        check=True, capture_output=True,
    ).stdout
    samples = array("h")
    samples.frombytes(raw[: len(raw) // 2 * 2])
    n = max(1, round(step * LEVEL_RATE))
    levels = []
    for i in range(0, len(samples) - n + 1, n):
        chunk = samples[i : i + n]
        rms = math.sqrt(sum(x * x for x in chunk) / n) / 32768
        levels.append(20 * math.log10(rms + 1e-9))
    return levels


def detect_silences(path: Path, min_len: float = 0.3) -> list[tuple[float, float]]:
    """Quiet stretches of at least `min_len` s, judged against this recording's
    own room noise and voice level (see cuts.speech_threshold)."""
    levels = audio_levels(path)
    threshold = speech_threshold(levels)
    if threshold is None:
        return []
    return find_silences(levels, step=LEVEL_STEP, threshold=threshold, min_len=min_len)
