"""Speech to words with timings (faster-whisper, runs on the CPU)."""
from __future__ import annotations

from pathlib import Path

from .words import Word


def transcribe(path: Path, model: str = "small", language: str = "en") -> list[Word]:
    from faster_whisper import WhisperModel  # slow import, keep it local

    whisper = WhisperModel(model, device="cpu", compute_type="int8")
    segments, _info = whisper.transcribe(
        str(path), language=language, word_timestamps=True, vad_filter=False
    )
    words: list[Word] = []
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if text:
                words.append(Word(text, round(w.start, 3), round(w.end, 3)))
    return words
