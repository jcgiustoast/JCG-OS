"""Find spoken scores like "three out of ten", "3 out of 10" or "3/10"."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .words import Word

NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}
_SLASH = re.compile(r"^(\d{1,2})/10$")


@dataclass(frozen=True)
class ScoreHit:
    score: int
    word_index: int  # index of the number word
    start: float


def normalize(token: str) -> str:
    """Lowercase, strip surrounding punctuation (keeps '/' and inner apostrophes)."""
    return re.sub(r"^[^\w/]+|[^\w/]+$", "", token.lower())


def as_number(token: str) -> int | None:
    if token.isdigit():
        return int(token)
    return NUMBER_WORDS.get(token)


def find_scores(words: list[Word]) -> list[ScoreHit]:
    tokens = [normalize(w.text) for w in words]
    hits: list[ScoreHit] = []
    i = 0
    while i < len(tokens):
        slash = _SLASH.match(tokens[i])
        if slash and int(slash.group(1)) <= 10:
            hits.append(ScoreHit(int(slash.group(1)), i, words[i].start))
            i += 1
            continue
        n = as_number(tokens[i])
        if (
            n is not None
            and 0 <= n <= 10
            and tokens[i + 1 : i + 3] == ["out", "of"]
            and i + 3 < len(tokens)
            and as_number(tokens[i + 3]) == 10
        ):
            hits.append(ScoreHit(n, i, words[i].start))
            i += 4
            continue
        i += 1
    return hits
