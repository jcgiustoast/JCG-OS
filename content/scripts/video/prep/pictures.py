"""The picture list for the Transparent Background short.

Claude proposes it (pictures.json): per picture, the exact few words Juan says
where it should appear. Juan can edit the words. Code finds them in the
transcript and works out the timings.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .cuts import Span, to_out, total
from .edl import LAYOUT, PrepError, list_shots
from .media import image_size
from .scores import normalize
from .words import Word

_T = LAYOUT["transparent"]
FULL_RATIO = _T["fullRatio"]
TITLE_SECONDS = _T["title"]["seconds"]
MIN_ON = _T["minOn"]
MAX_ON = _T["maxOn"]
FILE = "pictures.json"


@dataclass(frozen=True)
class PictureChoice:
    picture: str
    words: str
    show: Literal["card", "full"]


def suggest_show(img_w: int, img_h: int) -> str:
    """Very tall pictures (long page screenshots) fill the frame; everything else is a card."""
    return "full" if img_h / img_w >= FULL_RATIO else "card"


def write_stub(job: Path) -> bool:
    """Write the empty picture list for Claude to fill in. Never overwrites."""
    path = Path(job) / FILE
    if path.exists():
        return False
    rows = []
    for shot in list_shots(Path(job) / "shots"):
        w, h = image_size(shot)
        rows.append({"picture": shot.name, "words": "", "show": suggest_show(w, h)})
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def load_choices(job: Path) -> list[PictureChoice]:
    path = Path(job) / FILE
    if not path.exists():
        raise PrepError(f"There is no {FILE} yet. It lists which words Juan says when each picture appears.")
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise PrepError(f"{FILE} is not valid JSON ({e}). Check commas and quotes.") from e
    on_disk = {p.name for p in list_shots(Path(job) / "shots")}
    choices: list[PictureChoice] = []
    for row in rows:
        name = str(row.get("picture", "")).strip()
        words = str(row.get("words", "")).strip()
        show = row.get("show")
        if name not in on_disk:
            raise PrepError(f"{FILE} lists the picture {name!r}, but there is no such file in the shots folder.")
        if not words:
            raise PrepError(f"Picture {name} has no words yet. Write the few words Juan says when it should appear.")
        if show not in ("card", "full"):
            raise PrepError(f'Picture {name} has show={show!r}. It must be "card" or "full".')
        choices.append(PictureChoice(name, words, show))
    listed = {c.picture for c in choices}
    for missing in sorted(on_disk - listed):
        raise PrepError(f"The picture {missing} is in the shots folder but not in {FILE}. Add it or remove the file.")
    return choices


def _key(text: str) -> str:
    return normalize(text).replace("'", "").replace("’", "")


def find_phrase(words: list[Word], phrase: str, after: int = 0) -> int:
    """Index of the first word of the phrase (case, punctuation and apostrophes ignored); -1 if absent."""
    want = [k for k in (_key(t) for t in phrase.split()) if k]
    if not want:
        return -1
    heard = [(i, _key(w.text)) for i, w in enumerate(words)]
    heard = [(i, k) for i, k in heard if k]
    for pos in range(len(heard) - len(want) + 1):
        if heard[pos][0] < after:
            continue
        if [k for _, k in heard[pos : pos + len(want)]] == want:
            return heard[pos][0]
    return -1


def place(words: list[Word], choices: list[PictureChoice], spans: list[Span]) -> list[dict]:
    """Turn each picture's words into when it appears and disappears (seconds in the finished video)."""
    found: list[tuple[PictureChoice, int, float, bool]] = []
    cursor = 0
    for n, c in enumerate(choices):
        idx = find_phrase(words, c.words, after=cursor)
        if idx < 0:
            if n > 0 and find_phrase(words, c.words, after=0) >= 0:
                raise PrepError(
                    f'Picture {c.picture}: "{c.words}" comes before the previous picture '
                    f"({choices[n - 1].picture}) in the recording. Pictures must follow the order he speaks."
                )
            raise PrepError(f'Picture {c.picture}: I never hear "{c.words}" in the recording. Check the words.')
        start = to_out(words[idx].start, spans)
        pushed = start < TITLE_SECONDS
        if pushed:
            start = TITLE_SECONDS
        found.append((c, idx, round(start, 3), pushed))
        cursor = idx + 1

    end_of_video = total(spans)
    out: list[dict] = []
    for n, (c, idx, start, pushed) in enumerate(found):
        has_next = n + 1 < len(found)
        nxt = found[n + 1][2] if has_next else end_of_video
        if has_next and nxt - start < MIN_ON[c.show]:
            raise PrepError(
                f"Pictures {c.picture} and {found[n + 1][0].picture} are only {nxt - start:.1f}s apart. "
                f"A {c.show} picture needs at least {MIN_ON[c.show]}s on screen. "
                f"Change the words of one of them."
            )
        out.append(
            {
                "picture": c.picture,
                "show": c.show,
                "words": c.words,
                "wordIndex": idx,
                "outStart": start,
                "outEnd": round(min(nxt, start + MAX_ON[c.show]), 3),
                "pushed": pushed,
            }
        )
    return out
