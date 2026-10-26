import re
import subprocess
import sys
from pathlib import Path

import pytest
from archimoto_svg import text_to_svg


def test_returns_svg_with_path_and_colour():
    svg, w, h = text_to_svg("1.", size=150, color="#B084D3")
    assert svg.startswith("<svg") and "<path" in svg and "#B084D3" in svg
    assert w > 0 and h > 0


def test_width_scales_with_size():
    _, w1, _ = text_to_svg("PARA OPTIMIZAR", weight="bold", size=60)
    _, w2, _ = text_to_svg("PARA OPTIMIZAR", weight="bold", size=120)
    assert abs(w2 / w1 - 2) < 0.01


def test_bold_differs_from_regular():
    assert text_to_svg("10", weight="bold")[0] != text_to_svg("10")[0]


def test_spanish_characters():
    svg, w, _ = text_to_svg("¿AÑO ÚNICO?", weight="bold", size=100)
    assert svg.count("<path") >= 1 and w > text_to_svg("ANO UNICO", weight="bold", size=100)[1]


def test_missing_glyph_raises():
    with pytest.raises(ValueError, match="漢"):
        text_to_svg("A漢")


def test_unknown_weight_raises():
    with pytest.raises(ValueError, match="heavy"):
        text_to_svg("A", weight="heavy")


def test_empty_or_blank_text_raises():
    for blank in ("", "   "):
        with pytest.raises(ValueError, match="empty"):
            text_to_svg(blank)


def test_tracking_adds_width():
    text = "PARA OPTIMIZAR"
    _, w0, _ = text_to_svg(text, weight="bold", size=80)
    _, w5, _ = text_to_svg(text, weight="bold", size=80, tracking=5)
    assert abs(w5 - (w0 + 5 * len(text))) < 0.01


def _path_points(svg):
    """Yield every (x, y) coordinate pair, or (x, None) / (None, y) for H / V, in each path's d."""
    for d in re.findall(r' d="([^"]+)"', svg):
        for command, args in re.findall(r"([A-Za-z])([^A-Za-z]*)", d):
            nums = [float(n) for n in re.findall(r"-?\d+\.?\d*", args)]
            if command == "H":
                yield from ((n, None) for n in nums)
            elif command == "V":
                yield from ((None, n) for n in nums)
            elif command != "Z":
                yield from zip(nums[0::2], nums[1::2])


def test_all_ink_inside_box():
    svg, w, h = text_to_svg("¿ÚÑ?", weight="bold", size=100)
    points = list(_path_points(svg))
    assert points
    for x, y in points:
        assert x is None or 0 <= x <= w
        assert y is None or 0 <= y <= h
    assert h > 100  # accents rise above the font ascender, so the box grows


def test_cli_error_is_one_line_and_exits_1():
    script = Path(__file__).with_name("archimoto_svg.py")
    result = subprocess.run(
        [sys.executable, str(script), "A\u6f22"], capture_output=True, text=True, encoding="utf-8"
    )
    assert result.returncode == 1
    assert result.stdout == ""
    assert len(result.stderr.strip().splitlines()) == 1
    assert result.stderr.startswith("error:")
