import argparse
from pathlib import Path

from content.scripts.visual.piece import parse_piece
from content.scripts.visual.render import render_piece, bundle_pdf

# anchor to the repo's content/ dir (cli.py lives in content/scripts/visual/) so the
# command works regardless of the caller's current working directory
ROOT = Path(__file__).resolve().parents[2] / "raw" / "visuals"

_SCAFFOLD = """---
title: {slug}
mode: carousel
aspect: 4:5
---
# slide:cover
headline: Tu titular
subtitle: Subtítulo corto
"""


def _piece_dir(slug):
    return ROOT / slug


def cmd_new(args):
    d = _piece_dir(args.slug)
    d.mkdir(parents=True, exist_ok=True)
    pm = d / "piece.md"
    if not pm.exists():
        pm.write_text(_SCAFFOLD.format(slug=args.slug), encoding="utf-8")
    print(f"scaffolded {pm}")


def cmd_render(args):
    d = _piece_dir(args.slug)
    piece = parse_piece((d / "piece.md").read_text(encoding="utf-8"))
    pngs = render_piece(piece, d / "out")
    print(f"rendered {len(pngs)} slide(s) -> {d / 'out'}")
    if piece.meta.get("mode") == "carousel":
        print(f"pdf -> {bundle_pdf(pngs, d / 'out')}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="visual")
    sub = p.add_subparsers(required=True)
    n = sub.add_parser("new"); n.add_argument("slug"); n.set_defaults(func=cmd_new)
    r = sub.add_parser("render"); r.add_argument("slug"); r.set_defaults(func=cmd_render)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
