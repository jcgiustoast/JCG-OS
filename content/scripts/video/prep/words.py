"""A spoken word with its time in the source recording."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Word:
    text: str
    start: float
    end: float


def load_words(path: Path | str) -> list[Word]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Word(d["text"], float(d["start"]), float(d["end"])) for d in data]


def save_words(words: list[Word], path: Path | str) -> None:
    Path(path).write_text(
        json.dumps([asdict(w) for w in words], indent=1, ensure_ascii=False),
        encoding="utf-8",
    )
