import json

import pytest
from PIL import Image

from content.scripts.video.prep.edl import PrepError
from content.scripts.video.prep.transparent import (
    build_transparent_edl,
    matte_jobs,
    write_transparent_review,
)
from content.scripts.video.prep.words import Word
from tests.video.helpers import words_from

SENT = "so here is the first page and then we look at a long page that scrolls and finally the end of it all today"


def _job(tmp_path, sizes, words_text=SENT, show=None, phrases=None, fixes=None, headline="Seven emails that sell", words=None):
    job = tmp_path / "job"
    (job / "shots").mkdir(parents=True)
    for i, size in enumerate(sizes, start=1):
        Image.new("RGB", size, "white").save(job / "shots" / f"{i}.png")
    phrases = phrases or ["first page", "long page", "the end"][: len(sizes)]
    rows = []
    for i, size in enumerate(sizes, start=1):
        rows.append({
            "picture": f"{i}.png",
            "words": phrases[i - 1],
            "show": (show or {}).get(i, "full" if size[1] / size[0] >= 2.5 else "card"),
        })
    (job / "pictures.json").write_text(json.dumps(rows))
    if headline is not None:
        (job / "headline.txt").write_text(headline)
    if fixes is not None:
        (job / "fixes.json").write_text(json.dumps(fixes))
    return job, (words or words_from(words_text, start=0.0, step=0.5))


def _build(tmp_path, sizes, **kw):
    job, words = _job(tmp_path, sizes, **kw)
    return build_transparent_edl(job, words, silences=[])


def test_edl_has_title_pictures_captions(tmp_path):
    edl = _build(tmp_path, [(1200, 675), (1080, 4000), (600, 600)])
    assert edl["format"] == "transparent"
    assert edl["title"]["outEnd"] == 3.0
    assert len(edl["pictures"]) == 3
    assert edl["captions"]
    assert edl["video"] == "job/face.mp4"


@pytest.mark.parametrize("size", [(1200, 675), (1080, 1350), (600, 600)])
def test_card_box_inside_card_region_and_safe_area(tmp_path, size):
    edl = _build(tmp_path, [size], phrases=["first page"], show={1: "card"})
    b = edl["pictures"][0]["box"]
    assert b["x"] >= 100 and b["x"] + b["w"] <= 900
    assert b["y"] >= 300 and b["y"] + b["h"] <= 920


def test_full_box_covers_width_top_anchored(tmp_path):
    edl = _build(tmp_path, [(1200, 675), (1080, 4000)], phrases=["first page", "long page"])
    p = edl["pictures"][1]
    assert p["box"] == {"x": 0, "y": 0, "w": 1080, "h": 1920}
    assert p["crop"] is True
    assert p["matte"]["file"] == "job/matte/2.webm"
    assert p["shot"] == "job/shots/2.png"


def test_cards_have_no_matte(tmp_path):
    edl = _build(tmp_path, [(1200, 675)], phrases=["first page"], show={1: "card"})
    assert edl["pictures"][0]["matte"] is None


def test_matte_spans_mirror_face_spans_across_a_cut(tmp_path):
    words = words_from("one two three four five six seven eight nine ten", start=0.0, step=0.5)
    words += words_from("eleven twelve thirteen fourteen fifteen sixteen seventeen", start=6.0, step=0.5)
    job, _ = _job(tmp_path, [(1080, 4000)], phrases=["three four"], show={1: "full"}, words=words)
    edl = build_transparent_edl(job, words, silences=[])
    p = edl["pictures"][0]
    assert p["outStart"] == 3.0  # pushed? words start 1.0 -> out 1.0, pushed to 3.0
    spans = edl["spans"]
    assert len(spans) == 2
    m = p["matte"]
    assert len(m["spans"]) == 2
    face_out = {round(s["outStart"], 3): s for s in spans}
    for ms in m["spans"]:
        if abs(ms["outStart"] - p["outStart"]) < 1e-6:
            face = max((s for s in spans if s["outStart"] <= ms["outStart"] + 1e-6), key=lambda s: s["outStart"])
            expect = face["srcStart"] + (ms["outStart"] - face["outStart"])
        else:
            face = face_out[round(ms["outStart"], 3)]
            expect = face["srcStart"]
        assert m["srcStart"] + ms["srcStart"] == pytest.approx(expect, abs=0.001)
        assert ms["srcEnd"] > ms["srcStart"]
        piece_end = min(face["srcEnd"], face["srcStart"] + (p["outEnd"] - face["outStart"]))
        assert ms["srcEnd"] - ms["srcStart"] == pytest.approx(piece_end - expect, abs=0.002)


def test_captions_get_fixes(tmp_path):
    edl = _build(tmp_path, [(1200, 675)], phrases=["first page"], show={1: "card"}, fixes={"first": "FIRST"})
    assert any("FIRST" in c["text"] for c in edl["captions"])


def test_missing_headline_stops(tmp_path):
    with pytest.raises(PrepError, match="headline"):
        _build(tmp_path, [(1200, 675)], phrases=["first page"], headline=None)


def test_matte_jobs_lists_full_pictures_only(tmp_path):
    edl = _build(tmp_path, [(1200, 675), (1080, 4000)], phrases=["first page", "long page"])
    jobs = matte_jobs(edl)
    p = edl["pictures"][1]
    assert jobs == [{"out": "matte/2.webm", "start": p["matte"]["srcStart"], "end": p["matte"]["srcEnd"]}]


def test_review_lists_picture_words_show_and_captions(tmp_path):
    edl = _build(tmp_path, [(1200, 675), (1080, 4000)], phrases=["first page", "long page"])
    out = tmp_path / "review.md"
    write_transparent_review(edl, out)
    text = out.read_text(encoding="utf-8")
    assert "- Seven emails that" in text and "- sell" in text
    assert "1.png" in text and "2.png" in text
    assert "“first page”" in text
    assert "card" in text
    assert "full-screen (you cut out in front)" in text
    assert "long page" in text


def test_review_flags_pushed_picture(tmp_path):
    edl = _build(tmp_path, [(1200, 675)], phrases=["so here"], show={1: "card"})
    out = tmp_path / "review.md"
    write_transparent_review(edl, out)
    assert "moved to 3.0 s so it doesn't cover the title" in out.read_text(encoding="utf-8")


def test_missing_face_video_stops_when_silences_not_given(tmp_path):
    job, words = _job(tmp_path, [(1200, 675)], phrases=["first page"], show={1: "card"})
    with pytest.raises(PrepError, match="face.mp4"):
        build_transparent_edl(job, words)
