from pathlib import Path

from PIL import Image

from content.scripts.visual.piece import parse_piece
from content.scripts.visual.render import render_html, render_piece, bundle_pdf


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


def test_bundle_pdf_combines_pngs(tmp_path):
    piece = parse_piece(
        "---\ntitle: T\nmode: carousel\n---\n# slide:cover\nheadline: A\n# slide:narrative\nbody: B\n"
    )
    pngs = render_piece(piece, tmp_path)
    pdf = bundle_pdf(pngs, tmp_path)
    assert pdf.name == "bundle.pdf"
    assert pdf.exists() and pdf.stat().st_size > 0


def test_e2e_aov_renders_all_types(tmp_path):
    text = Path("tests/visual/fixtures/aov.md").read_text(encoding="utf-8")
    piece = parse_piece(text)
    assert len(piece.slides) == 12
    pngs = render_piece(piece, tmp_path)
    assert len(pngs) == 12
    for p in pngs:
        assert Image.open(p).size == (1080, 1350)
    pdf = bundle_pdf(pngs, tmp_path)
    assert pdf.exists()
