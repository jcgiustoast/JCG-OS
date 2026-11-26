"""Speech to words with timings (faster-whisper, runs on the CPU)."""
from __future__ import annotations

import subprocess
from pathlib import Path

from .words import Word

SAMPLE_RATE = 16000


def load_audio(path: Path):
    """16 kHz mono float32 via ffmpeg.

    faster-whisper's own decoder (PyAV) breaks on some installed PyAV versions,
    so we decode with ffmpeg and hand it the samples directly.
    """
    import numpy as np

    raw = subprocess.run(
        [
            "ffmpeg", "-loglevel", "error", "-i", str(path),
            "-vn", "-ac", "1", "-ar", str(SAMPLE_RATE), "-f", "s16le", "-",
        ],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def transcribe(path: Path, model: str = "small", language: str = "en") -> list[Word]:
    from faster_whisper import WhisperModel  # slow import, keep it local

    whisper = WhisperModel(model, device="cpu", compute_type="int8")
    segments, _info = whisper.transcribe(
        load_audio(path), language=language, word_timestamps=True, vad_filter=False
    )
    words: list[Word] = []
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if text:
                words.append(Word(text, round(float(w.start), 3), round(float(w.end), 3)))
    return words
