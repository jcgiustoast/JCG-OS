from PIL import Image

from content.scripts.visual.piece import parse_piece
from content.scripts.visual.render import render_html, render_piece


def test_render_html_includes_slide_markup_and_inline_css():
    piece = parse_piece(
        "---\ntitle: T\nmode: single\n---\n# slide:cover\nheadline: El Secreto\nsubtitle: Que no conocías\n"
    )
    html = render_html(piece)
    assert '<div class="slide cover">' in html
    assert "El Secreto" in html
    assert "Que no conocías" in html
    assert "@font-face" in html          # theme.css inlined
    assert "GIUSTO" in html              # footer macro rendered


def test_render_piece_writes_1080x1350_png(tmp_path):
    piece = parse_piece(
        "---\ntitle: T\nmode: single\n---\n# slide:cover\nheadline: El Secreto del AOV\nsubtitle: Que no conocías\n"
    )
    out = render_piece(piece, tmp_path)
    assert [p.name for p in out] == ["image-01.png"]
    assert Image.open(out[0]).size == (1080, 1350)
