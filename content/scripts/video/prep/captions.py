"""Group spoken words into short lowercase caption phrases."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .scores import find_scores, normalize
from .words import Word

MIN_WORDS = 5
MAX_WORDS = 13
MAX_SECONDS = 3.0
PHRASE_GAP = 0.25
MERGE_MAX_SECONDS = 4.0


@dataclass(frozen=True)
class Caption:
    text: str
    src_start: float
    src_end: float


def _clean(token: str) -> str:
    """lowercase, no punctuation except inner apostrophes."""
    t = token.lower().replace("’", "'")
    t = re.sub(r"[^\w'/]", "", t)
    return t.strip("'")


def _display_tokens(words: list[Word]) -> list[str]:
    tokens = [_clean(w.text) for w in words]
    for hit in find_scores(words):
        i = hit.word_index
        if "/" in normalize(words[i].text):
            tokens[i] = f"{hit.score} out of 10"
        else:
            tokens[i] = str(hit.score)
            tokens[i + 3] = "10"
    return [t.replace("/", " ") if "out of" not in t else t for t in tokens]


def _ends_sentence(token: str) -> bool:
    return token.rstrip("\"')").endswith((".", "?", "!"))


def make_captions(words: list[Word], breaks: list[int]) -> list[Caption]:
    if not words:
        return []
    tokens = _display_tokens(words)
    break_set = set(breaks)
    groups: list[list[int]] = []  # word indices per phrase
    starts_item: list[bool] = []  # phrase begins at a break
    current: list[int] = []

    def close() -> None:
        nonlocal current
        if current:
            groups.append(current)
            starts_item.append(current[0] in break_set)
            current = []

    for i, w in enumerate(words):
        if i in break_set:
            close()
        current.append(i)
        nxt = words[i + 1] if i + 1 < len(words) else None
        n = len(current)
        if n >= MAX_WORDS:
            close()
            continue
        if n >= MIN_WORDS and nxt is not None:
            first = words[current[0]]
            if (
                nxt.start - w.end > PHRASE_GAP
                or _ends_sentence(w.text)
                or w.end - first.start >= MAX_SECONDS
                or nxt.end - first.start > MAX_SECONDS
            ):
                close()
    close()

    # a short tail (end of recording, or just before a new item) joins the
    # phrase before it, if that phrase belongs to the same item
    k = len(groups) - 1
    while k >= 1:
        if len(groups[k]) < MIN_WORDS and not starts_item[k]:
            merged = groups[k - 1] + groups[k]
            span = words[merged[-1]].end - words[merged[0]].start
            if len(merged) <= MAX_WORDS and span <= MERGE_MAX_SECONDS:
                groups[k - 1 : k + 1] = [merged]
                del starts_item[k]
        k -= 1

    return [
        Caption(
            " ".join(t for t in (tokens[i] for i in g) if t),
            words[g[0]].start,
            words[g[-1]].end,
        )
        for g in groups
    ]
