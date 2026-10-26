"""Turn Archimoto text into a self-contained SVG of filled outlines.

Figma's scripting runtime cannot load the Archimoto font, so the text is
converted to vector paths here and inserted later with figma.createNodeFromSvg.

Usage:
    python archimoto_svg.py --weight bold --size 120 --color "#D3FF4E" [--tracking 0] -- "TEXT"
Options go first; `--` goes last, right before the text.
Prints only the SVG to stdout.
"""
import argparse
import sys
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import quoteattr

from fontTools.pens.boundsPen import ControlBoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).resolve().parents[4] / "content" / "scripts" / "visual" / "assets" / "fonts"
WEIGHTS = ("regular", "bold")


def _num(value: float) -> str:
    return f"{round(value, 2) + 0.0:.2f}".rstrip("0").rstrip(".") or "0"


@lru_cache(maxsize=None)
def _load_font(weight: str) -> TTFont:
    return TTFont(FONT_DIR / f"archimoto-{weight}.otf")


def text_to_svg(
    text: str,
    weight: str = "regular",
    size: float = 150,
    color: str = "#B084D3",
    tracking: float = 0.0,
) -> tuple[str, float, float]:
    """Return (svg_markup, width_px, height_px) for `text` set in Archimoto."""
    if weight not in WEIGHTS:
        raise ValueError(f"unknown weight {weight!r}; expected one of {', '.join(WEIGHTS)}")
    if not text.strip():
        raise ValueError("text is empty")

    font = _load_font(weight)
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    advances = font["hmtx"].metrics
    scale = size / font["head"].unitsPerEm

    glyph_names = []
    for char in text:
        glyph_name = cmap.get(ord(char))
        if glyph_name is None:
            raise ValueError(f"glyph {char!r} (U+{ord(char):04X}) is missing from archimoto-{weight}")
        glyph_names.append(glyph_name)

    # The box covers the font's ascender/descender and any ink that pokes past them
    # (accented capitals, symbols), so nothing is clipped when Figma imports the SVG.
    top, bottom = font["hhea"].ascent, font["hhea"].descent
    for glyph_name in set(glyph_names):
        bounds_pen = ControlBoundsPen(glyph_set)
        glyph_set[glyph_name].draw(bounds_pen)
        if bounds_pen.bounds:  # spaces have no ink
            top = max(top, bounds_pen.bounds[3])
            bottom = min(bottom, bounds_pen.bounds[1])
    baseline = top * scale
    height = (top - bottom) * scale

    paths = []
    x = 0.0
    for glyph_name in glyph_names:
        pen = SVGPathPen(glyph_set, ntos=_num)
        # Font units are y-up; SVG is y-down, so flip y and drop the baseline below the box top.
        glyph_set[glyph_name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        commands = pen.getCommands()
        if commands:  # spaces advance without drawing
            paths.append(f'<path fill={quoteattr(color)} d="{commands}"/>')
        x += advances[glyph_name][0] * scale + tracking

    width = x
    w, h = _num(width), _num(height)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">{"".join(paths)}</svg>'
    )
    return svg, width, height


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Archimoto text as an SVG of outlines.")
    parser.add_argument("text")
    parser.add_argument("--weight", default="regular", choices=WEIGHTS)
    parser.add_argument("--size", type=float, default=150)
    parser.add_argument("--color", default="#B084D3")
    parser.add_argument("--tracking", type=float, default=0.0)
    args = parser.parse_args()
    try:
        svg, _, _ = text_to_svg(args.text, args.weight, args.size, args.color, args.tracking)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
    print(svg)


if __name__ == "__main__":
    main()
