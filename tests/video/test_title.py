import pytest
from PIL import ImageFont

from content.scripts.video.prep.edl import LAYOUT, PrepError
from content.scripts.video.prep.title import FONT, fit_title

T = LAYOUT["transparent"]["title"]


def test_short_headline_one_line_biggest_size():
    r = fit_title("Steal This Page")
    assert len(r["lines"]) == 1
    assert r["fontSize"] == 104
    assert r["outEnd"] == 3.0


def test_long_headline_wraps_to_three_lines_max():
    r = fit_title("How I rebuilt a product page in one afternoon and doubled sales")
    assert 1 <= len(r["lines"]) <= 3
    font = ImageFont.truetype(str(FONT), r["fontSize"])
    for line in r["lines"]:
        assert font.getlength(line) + 2 * T["padX"] <= T["maxWidth"]


def test_box_inside_safe_area_and_top_300():
    b = fit_title("Steal This Page")["box"]
    assert b["y"] == 300
    assert b["x"] >= 60
    assert b["x"] + b["w"] <= 940
    assert b["y"] + b["h"] < 960


def test_box_centred_on_500():
    b = fit_title("Steal This Page")["box"]
    assert abs(b["x"] + b["w"] / 2 - 500) <= 1


def test_headline_keeps_juans_casing():
    assert " ".join(fit_title("the $10M PDP")["lines"]) == "the $10M PDP"


def test_too_long_headline_stops():
    with pytest.raises(PrepError, match="3 lines"):
        fit_title(" ".join(["supercalifragilistic"] * 20))


def test_empty_headline_stops():
    with pytest.raises(PrepError):
        fit_title("   ")
