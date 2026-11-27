"""Build the Transparent Background short's edit list (edl.json) and Juan's check sheet."""
from __future__ import annotations

from pathlib import Path

from .cuts import keep_spans, total
from .edl import (
    LAYOUT,
    SAFE,
    SAFE_Y1,
    PrepError,
    _load_redact,
    build_captions,
)
from .fixes import apply_fixes, load_fixes
from .media import FPS, HEIGHT, WIDTH, detect_silences, image_size, probe
from .pictures import load_choices, place
from .title import fit_title
from .words import Word

_CARD = LAYOUT["transparent"]["card"]
CAPTION_H = 170
CAPTION_BOX = {
    "x": LAYOUT["transparent"]["caption"]["x"],
    "y": SAFE_Y1 - CAPTION_H,
    "w": LAYOUT["transparent"]["caption"]["w"],
    "h": CAPTION_H,
}


def _card_box(img_w: int, img_h: int) -> dict:
    scale = min(_CARD["w"] / img_w, _CARD["h"] / img_h)
    w, h = int(img_w * scale), int(img_h * scale)
    return {
        "x": _CARD["x"] + (_CARD["w"] - w) // 2,
        "y": _CARD["y"] + (_CARD["h"] - h) // 2,
        "w": w,
        "h": h,
    }


def _full_box(img_w: int, img_h: int) -> tuple[dict, bool]:
    h = round(WIDTH * img_h / img_w)
    return {"x": 0, "y": 0, "w": WIDTH, "h": min(HEIGHT, h)}, h > HEIGHT


def _matte(shot_name: str, out_start: float, out_end: float, spans) -> dict:
    """The face spans clipped to the picture's time, so the cut-out stays in step with the face."""
    pieces = []
    for s in spans:
        o0 = s.out_start
        o1 = o0 + (s.src_end - s.src_start)
        a, b = max(o0, out_start), min(o1, out_end)
        if b - a > 1e-6:
            pieces.append((s.src_start + (a - o0), s.src_start + (b - o0), a))
    if not pieces:
        raise PrepError(f"Picture {shot_name}: no part of the recording plays while it is on screen.")
    base = pieces[0][0]
    return {
        "file": f"job/matte/{Path(shot_name).stem}.webm",
        "srcStart": round(base, 3),
        "srcEnd": round(pieces[-1][1], 3),
        "spans": [
            {"srcStart": round(s0 - base, 3), "srcEnd": round(s1 - base, 3), "outStart": round(o, 3)}
            for s0, s1, o in pieces
        ],
    }


def build_transparent_edl(
    job: Path, words: list[Word], silences: list[tuple[float, float]] | None = None
) -> dict:
    job = Path(job)
    headline_file = job / "headline.txt"
    if not headline_file.exists():
        raise PrepError("There is no headline.txt yet. Write the headline Juan wants on screen in the first 3 seconds.")
    title = fit_title(headline_file.read_text(encoding="utf-8").strip())

    choices = load_choices(job)
    face = job / "face.mp4"
    duration = probe(face)["duration"] if face.exists() else None
    if silences is None:
        if not face.exists():
            raise PrepError("There is no face.mp4 in the job folder yet, so I can't find the pauses to cut.")
        silences = detect_silences(face)
    spans = keep_spans(words, duration=duration, silences=silences)
    out_total = round(total(spans), 3)

    placed = place(words, choices, spans)
    redact = _load_redact(job / "shots")
    pictures = []
    for p in placed:
        img_w, img_h = image_size(job / "shots" / p["picture"])
        if p["show"] == "card":
            box, crop, matte = _card_box(img_w, img_h), False, None
        else:
            box, crop = _full_box(img_w, img_h)
            matte = _matte(p["picture"], p["outStart"], p["outEnd"], spans)
        pictures.append({
            "picture": p["picture"],
            "show": p["show"],
            "words": p["words"],
            "shot": f"job/shots/{p['picture']}",
            "box": box,
            "imgW": img_w,
            "imgH": img_h,
            "crop": crop,
            "outStart": p["outStart"],
            "outEnd": p["outEnd"],
            "pushed": p["pushed"],
            "redact": [dict(zip("xywh", r)) for r in redact.get(p["picture"], [])],
            "matte": matte,
        })

    fixes = load_fixes(job)
    captions = build_captions(
        words, spans, [p["wordIndex"] for p in placed], lambda t: apply_fixes(t, fixes)
    )

    return {
        "format": "transparent",
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
        "title": title,
        "pictures": pictures,
        "captions": captions,
    }


def matte_jobs(edl: dict) -> list[dict]:
    """What the cut-out tool must make: one clip per full-screen picture."""
    return [
        {"out": f"matte/{Path(p['matte']['file']).name}", "start": p["matte"]["srcStart"], "end": p["matte"]["srcEnd"]}
        for p in edl["pictures"]
        if p.get("matte")
    ]


def write_transparent_review(edl: dict, path: Path) -> None:
    """Plain sheet for Juan: the headline, then each picture with the captions shown while it is up."""
    lines = ["# Transparent Background short — check before render", ""]
    lines.append("Headline (first 3 s):")
    lines += [f"- {ln}" for ln in edl["title"]["lines"]]
    lines += ["", f"Length after removing pauses: {edl['duration']:.1f} s", ""]
    for p in edl["pictures"]:
        length = p["outEnd"] - p["outStart"]
        lines.append(f"## {p['picture']}")
        lines.append("")
        lines.append(f"- appears on: “{p['words']}” at {p['outStart']:.1f} s for {length:.1f} s")
        lines.append("- shown as: " + ("card" if p["show"] == "card" else "full-screen (you cut out in front)"))
        if p["pushed"]:
            lines.append("- moved to 3.0 s so it doesn't cover the title")
        lines.append("- captions while it is up:")
        for c in edl["captions"]:
            if p["outStart"] - 1e-6 <= c["outStart"] < p["outEnd"] - 1e-6:
                lines.append(f"  - {c['text']}")
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
