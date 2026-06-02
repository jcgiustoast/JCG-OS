from content.scripts.visual.piece import parse_frontmatter


def test_parse_frontmatter_reads_keys_and_returns_body():
    text = "---\ntitle: El secreto del AOV\nmode: carousel\naspect: 4:5\n---\n# slide:cover\ntitle: Hola\n"
    meta, body = parse_frontmatter(text)
    assert meta == {"title": "El secreto del AOV", "mode": "carousel", "aspect": "4:5"}
    assert body.startswith("# slide:cover")


def test_parse_frontmatter_requires_block():
    import pytest
    with pytest.raises(ValueError):
        parse_frontmatter("no frontmatter here")


from content.scripts.visual.piece import parse_piece, Slide, Piece


def test_parse_piece_builds_typed_slides_with_repeated_keys():
    text = (
        "---\ntitle: T\nmode: carousel\n---\n"
        "# slide:cover\n"
        "headline: El Secreto del AOV\n"
        "subtitle: Que no conocías\n"
        "# slide:infographic-framework\n"
        "title: Las 3 Herramientas\n"
        "card: 01 | Media | tres lentes\n"
        "card: 02 | Histogramas | agrupa\n"
    )
    piece = parse_piece(text)
    assert isinstance(piece, Piece)
    assert piece.meta["mode"] == "carousel"
    assert [s.type for s in piece.slides] == ["cover", "infographic-framework"]
    assert piece.slides[0].fields["subtitle"] == "Que no conocías"
    assert piece.slides[1].fields["card"] == ["01 | Media | tres lentes", "02 | Histogramas | agrupa"]


from content.scripts.visual.piece import parse_bars, parse_pipes


def test_parse_bars_marks_highlight_with_star():
    bars = parse_bars("€10:34, €30:100*, €70:9")
    assert bars == [
        {"label": "€10", "height": 34, "hi": False},
        {"label": "€30", "height": 100, "hi": True},
        {"label": "€70", "height": 9, "hi": False},
    ]


def test_parse_pipes_splits_and_strips():
    assert parse_pipes("01 | Media | tres lentes") == ["01", "Media", "tres lentes"]
