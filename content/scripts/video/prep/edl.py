"""Build the ranking short's edit list (edl.json) and Juan's review sheet."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .captions import make_captions
from .cuts import keep_spans, to_out, total
from .media import FPS, HEIGHT, WIDTH, image_size, probe
from .scores import ScoreHit, find_scores
from .words import Word

SHOT_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

# layout, in px of the 1080x1920 frame (see the plan's Global Constraints)
COL_X = round(0.06 * WIDTH)  # 65
TALL_W = round(0.39 * WIDTH)  # 421 (6% -> 45%)
WIDE_W = round(0.47 * WIDTH)  # 508
WIDE_Y = 230
BAND_TOP = round(0.05 * HEIGHT)  # 96
BAND_BOTTOM = int(0.96 * HEIGHT)  # 1843
TALL_CENTRE = 0.47 * HEIGHT
CAPTION_BRIDGE = 0.4  # hold a caption over short silences so it doesn't flicker


class PrepError(Exception):
    """The recording and the screenshots don't line up; never render."""


def list_shots(shots_dir: Path) -> list[Path]:
    def key(p: Path):
        m = re.match(r"\d+", p.stem)
        return (int(m.group()) if m else 10**9, p.name)

    return sorted(
        (p for p in Path(shots_dir).iterdir() if p.suffix.lower() in SHOT_EXTS), key=key
    )


def item_cut(words: list[Word], hit: ScoreHit, lookback: float = 2.5, min_index: int = 0) -> int:
    """First word of the sentence that gives this score.

    Picks the word after the biggest pause (>= 0.15 s, or a sentence end) within
    `lookback` seconds before the score; falls back to the score word itself.
    """
    best, best_weight = hit.word_index, 0.0
    for j in range(hit.word_index, min_index - 1, -1):
        if words[hit.word_index].start - words[j].start > lookback:
            break
        if j == 0:
            gap, sentence_end = words[0].start + 1.0, True
        else:
            gap = words[j].start - words[j - 1].end
            sentence_end = words[j - 1].text.rstrip("\"')").endswith((".", "?", "!"))
        if gap < 0.15 and not sentence_end:
            continue
        weight = gap + (1.0 if sentence_end else 0.0)
        if weight > best_weight:
            best, best_weight = j, weight
    return best


def _layout(img_w: int, img_h: int) -> dict:
    if img_h > img_w:
        h = round(TALL_W * img_h / img_w)
        band = BAND_BOTTOM - BAND_TOP
        if h > band:
            return {"layout": "tall", "crop": True,
                    "box": {"x": COL_X, "y": BAND_TOP, "w": TALL_W, "h": band}}
        y = round(TALL_CENTRE - h / 2)
        y = min(max(y, BAND_TOP), BAND_BOTTOM - h)
        return {"layout": "tall", "crop": False, "box": {"x": COL_X, "y": y, "w": TALL_W, "h": h}}
    h = round(WIDE_W * img_h / img_w)
    return {"layout": "wide", "crop": False, "box": {"x": COL_X, "y": WIDE_Y, "w": WIDE_W, "h": h}}


def _load_redact(shots_dir: Path) -> dict:
    path = shots_dir / "redact.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_ranking_edl(job: Path, words: list[Word]) -> dict:
    job = Path(job)
    shots = list_shots(job / "shots")
    hits = find_scores(words)
    heard = ", ".join(str(h.score) for h in hits) or "none"
    if not hits:
        raise PrepError(
            "I didn't hear any score like 'three out of ten' in the recording. "
            f"Found {len(shots)} screenshots."
        )
    if len(hits) != len(shots):
        raise PrepError(
            f"Heard {len(hits)} scores ({heard}) but found {len(shots)} screenshots "
            f"({', '.join(p.name for p in shots) or 'none'}). They must match one to one."
        )

    face = job / "face.mp4"
    duration = probe(face)["duration"] if face.exists() else None
    spans = keep_spans(words, duration=duration)
    out_total = round(total(spans), 3)

    cuts: list[int] = []
    for k, hit in enumerate(hits):
        floor = hits[k - 1].word_index + 1 if k else 0
        cuts.append(max(item_cut(words, hit, min_index=floor), floor))

    redact = _load_redact(job / "shots")
    items = []
    for k, (hit, shot, cut) in enumerate(zip(hits, shots, cuts)):
        img_w, img_h = image_size(shot)
        out_start = round(to_out(words[cut].start, spans), 3)
        items.append({
            "score": hit.score,
            "shot": f"job/shots/{shot.name}",
            **_layout(img_w, img_h),
            "imgW": img_w,
            "imgH": img_h,
            "outStart": out_start,
            "outEnd": None,
            "redact": [dict(zip("xywh", r)) for r in redact.get(shot.name, [])],
        })
    for a, b in zip(items, items[1:]):
        a["outEnd"] = b["outStart"]
    items[-1]["outEnd"] = out_total

    captions = []
    for c in make_captions(words, breaks=cuts):
        captions.append({
            "text": c.text,
            "outStart": round(to_out(c.src_start, spans), 3),
            "outEnd": round(to_out(c.src_end, spans), 3),
        })
    for a, b in zip(captions, captions[1:]):
        if b["outStart"] - a["outEnd"] <= CAPTION_BRIDGE:
            a["outEnd"] = b["outStart"]

    return {
        "format": "ranking",
        "fps": FPS,
        "width": WIDTH,
        "height": HEIGHT,
        "video": "job/face.mp4",
        "duration": out_total,
        "spans": [
            {"srcStart": s.src_start, "srcEnd": s.src_end, "outStart": s.out_start} for s in spans
        ],
        "items": items,
        "captions": captions,
    }


def write_review(edl: dict, path: Path) -> None:
    """Plain list for Juan: each item, its score, and the caption words under it."""
    lines = [f"# Ranking short — check before render", "",
             f"Length after removing pauses: {edl['duration']:.1f} s", ""]
    items = edl["items"]
    for n, item in enumerate(items):
        shot = item["shot"].split("/")[-1]
        lines.append(f"## {item['score']}/10 — screenshot {shot}")
        lines.append("")
        for c in edl["captions"]:
            inside = item["outStart"] - 1e-6 <= c["outStart"] < item["outEnd"] - 1e-6
            before_first = n == 0 and c["outStart"] < item["outStart"]
            if inside or before_first:
                lines.append(f"- {c['text']}")
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
