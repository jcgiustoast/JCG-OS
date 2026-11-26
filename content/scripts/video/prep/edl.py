"""Build the ranking short's edit list (edl.json) and Juan's review sheet."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .captions import make_captions
from .cuts import keep_spans, to_out, total
from .media import FPS, HEIGHT, WIDTH, detect_silences, image_size, probe
from .scores import ScoreHit, find_scores
from .words import Word

SHOT_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

# Layout numbers live in ONE file, shared with the Remotion look (src/layout.ts).
LAYOUT = json.loads((Path(__file__).resolve().parents[1] / "layout.json").read_text(encoding="utf-8"))
_safe, _col, _badge, _cap = LAYOUT["safe"], LAYOUT["column"], LAYOUT["badge"], LAYOUT["caption"]

# safe area: what Reels/TikTok buttons, username, description and top bar leave clear
SAFE_X0 = _safe["left"]  # 60
SAFE_X1 = WIDTH - _safe["right"]  # 940
SAFE_Y0 = _safe["top"]  # 260
SAFE_Y1 = HEIGHT - _safe["bottom"]  # 1480
SAFE = {"x": SAFE_X0, "y": SAFE_Y0, "w": SAFE_X1 - SAFE_X0, "h": SAFE_Y1 - SAFE_Y0}

BADGE_H = _badge["height"]  # 106
BADGE_OVERHANG = _badge["overhang"]  # badge's right edge sits this far past the shot's

COL_X = _col["x"]  # 65
TALL_W = _col["width"]  # 421
WIDE_W = _col["wideWidth"]  # 508
BAND_TOP = SAFE_Y0 + BADGE_H // 2  # 313: the badge straddles the shot's top edge
BAND_BOTTOM = SAFE_Y1  # 1480
TALL_CENTRE = _col["tallCentre"] * HEIGHT
FIT_MIN = _col["fitMin"]  # shrink a too-tall shot to fit if that keeps >= 75% width; else crop

CAPTION_BOX = {
    "x": COL_X + TALL_W + _cap["gapToShot"],
    "y": SAFE_Y1 - _cap["height"],
    "w": min(_cap["maxWidth"], SAFE_X1 - (COL_X + TALL_W + _cap["gapToShot"])),
    "h": _cap["height"],
}
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
    band = BAND_BOTTOM - BAND_TOP
    if img_h > img_w:
        h = round(TALL_W * img_h / img_w)
        if h <= band:
            y = round(TALL_CENTRE - h / 2)
            y = min(max(y, BAND_TOP), BAND_BOTTOM - h)
            box = {"x": COL_X, "y": y, "w": TALL_W, "h": h}
            return {"layout": "tall", "crop": False, "box": box, "badge": _badge_for(box)}
        if band / h >= FIT_MIN:  # a little too tall: shrink it to fit, show all of it
            box = {"x": COL_X, "y": BAND_TOP, "w": round(band * img_w / img_h), "h": band}
            return {"layout": "tall", "crop": False, "box": box, "badge": _badge_for(box)}
        box = {"x": COL_X, "y": BAND_TOP, "w": TALL_W, "h": band}  # very long page: its top part
        return {"layout": "tall", "crop": True, "box": box, "badge": _badge_for(box)}
    h = min(round(WIDE_W * img_h / img_w), band)
    box = {"x": COL_X, "y": BAND_TOP, "w": WIDE_W, "h": h}
    return {"layout": "wide", "crop": False, "box": box, "badge": _badge_for(box)}


def _badge_for(box: dict) -> dict:
    """Score badge on the screenshot's top-right corner: straddles its top edge,
    right edge a little past the shot's, so it follows the shot and stays off the face.
    The box grows leftwards for "10/10"."""
    return {
        "right": box["x"] + box["w"] + BADGE_OVERHANG,
        "top": box["y"] - BADGE_H // 2,
        "h": BADGE_H,
    }


def _load_redact(shots_dir: Path) -> dict:
    path = shots_dir / "redact.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_ranking_edl(
    job: Path, words: list[Word], silences: list[tuple[float, float]] | None = None
) -> dict:
    """`silences`: quiet stretches of face.mp4 (seconds); measured from its audio when None."""
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
    if silences is None:
        silences = detect_silences(face) if face.exists() else []
    spans = keep_spans(words, duration=duration, silences=silences)
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
        "safe": SAFE,
        "caption": CAPTION_BOX,
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
