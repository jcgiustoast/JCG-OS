"""Transparent Background: fit Juan's headline into the black title box.

Biggest font size whose greedy word wrap fits in 3 lines; text keeps Juan's casing.
"""
from __future__ import annotations

from pathlib import Path

from PIL import ImageFont

from .edl import LAYOUT, PrepError

FONT = Path(__file__).resolve().parents[2] / "visual" / "assets" / "fonts" / "bigshoulders-extrabold.ttf"
_T = LAYOUT["transparent"]["title"]


def _wrap(words: list[str], font: ImageFont.FreeTypeFont, limit: float) -> list[str] | None:
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}" if cur else w
        if font.getlength(trial) * _T["slack"] <= limit:
            cur = trial
        elif cur:
            lines.append(cur)
            cur = w
            if font.getlength(cur) * _T["slack"] > limit:
                return None
        else:
            return None
    lines.append(cur)
    return lines if len(lines) <= _T["maxLines"] else None


def fit_title(text: str) -> dict:
    words = text.split()
    if not words:
        raise PrepError("headline.txt is empty. Write the headline Juan wants on screen.")
    limit = _T["maxWidth"] - 2 * _T["padX"]
    for size in _T["sizes"]:
        font = ImageFont.truetype(str(FONT), size)
        lines = _wrap(words, font, limit)
        if lines is None:
            continue
        text_w = max(font.getlength(ln) for ln in lines) * _T["slack"]
        w = min(_T["maxWidth"], round(text_w + 2 * _T["padX"]))
        h = round(len(lines) * size * _T["lineHeight"] + 2 * _T["padY"])
        return {
            "lines": lines,
            "fontSize": size,
            "lineHeight": _T["lineHeight"],
            "box": {"x": round(_T["centreX"] - w / 2), "y": _T["top"], "w": w, "h": h},
            "outEnd": _T["seconds"],
        }
    raise PrepError("The headline doesn't fit in 3 lines — shorten it")
