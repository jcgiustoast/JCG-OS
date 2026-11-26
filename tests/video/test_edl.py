import json

import pytest
from PIL import Image

from content.scripts.video.prep.edl import (
    SAFE,
    PrepError,
    build_ranking_edl,
    item_cut,
    list_shots,
    write_review,
)
from content.scripts.video.prep.scores import find_scores
from content.scripts.video.prep.words import Word, save_words
from tests.video.helpers import words_from

H = 1920
# safe area (what Reels/TikTok buttons and text don't cover): x 60-940, y 260-1480
SAFE_X0, SAFE_Y0, SAFE_X1, SAFE_Y1 = 60, 260, 940, 1480
BAND_TOP = SAFE_Y0 + 53  # half a badge above the shot's top edge stays inside too


def _spoken(*sentences, pause=0.8):
    """Sentences separated by pauses, like a real recording."""
    words, t = [], 0.5
    for s in sentences:
        ws = words_from(s, start=t)
        words += ws
        t = ws[-1].end + pause
    return words


THREE = _spoken(
    "this is a zero out of ten email.",
    "this one is a seven out of ten because the subject line works.",
    "and this one is a ten out of ten.",
)


def _job(tmp_path, sizes, words=THREE, redact=None):
    job = tmp_path / "job"
    (job / "shots").mkdir(parents=True)
    for i, size in enumerate(sizes, start=1):
        Image.new("RGB", size, "white").save(job / "shots" / f"{i}.png")
    if redact is not None:
        (job / "shots" / "redact.json").write_text(json.dumps(redact))
    save_words(words, job / "words.json")
    return job


def test_list_shots_numeric(tmp_path):
    for name in ["1.png", "2.png", "10.png", "9.png", "notes.txt"]:
        (tmp_path / name).write_bytes(b"x")
    assert [p.name for p in list_shots(tmp_path)] == ["1.png", "2.png", "9.png", "10.png"]


def test_mismatch_raises(tmp_path):
    job = _job(tmp_path, [(400, 900), (400, 900)])
    with pytest.raises(PrepError) as e:
        build_ranking_edl(job, THREE)
    msg = str(e.value)
    assert "3 scores" in msg and "2 screenshots" in msg
    assert "0, 7, 10" in msg


def test_no_scores_raises(tmp_path):
    job = _job(tmp_path, [(400, 900)], words=words_from("hello there nothing to rank"))
    with pytest.raises(PrepError):
        build_ranking_edl(job, words_from("hello there nothing to rank"))


def test_tall_layout(tmp_path):
    edl = build_ranking_edl(_job(tmp_path, [(400, 900)] * 3), THREE)
    item = edl["items"][0]
    assert item["layout"] == "tall" and item["crop"] is False
    box = item["box"]
    assert box["x"] == 65 and box["w"] == 421
    assert box["h"] == round(421 * 900 / 400)
    assert box["y"] >= BAND_TOP and box["y"] + box["h"] <= SAFE_Y1
    assert abs((box["y"] + box["h"] / 2) - 0.47 * H) <= 1


def test_very_tall_is_cropped(tmp_path):
    edl = build_ranking_edl(_job(tmp_path, [(1080, 8000)] * 3), THREE)
    item = edl["items"][0]
    assert item["crop"] is True
    assert item["box"] == {"x": 65, "y": BAND_TOP, "w": 421, "h": SAFE_Y1 - BAND_TOP}


def test_wide_layout(tmp_path):
    edl = build_ranking_edl(_job(tmp_path, [(1600, 900)] * 3), THREE)
    item = edl["items"][0]
    assert item["layout"] == "wide"
    assert item["box"]["x"] == 65 and item["box"]["w"] == 508 and item["box"]["y"] == BAND_TOP


def test_item_times(tmp_path):
    edl = build_ranking_edl(_job(tmp_path, [(400, 900)] * 3), THREE)
    items = edl["items"]
    assert [i["score"] for i in items] == [0, 7, 10]
    assert [i["shot"] for i in items] == ["job/shots/1.png", "job/shots/2.png", "job/shots/3.png"]
    for a, b in zip(items, items[1:]):
        assert a["outEnd"] == b["outStart"]
        assert a["outStart"] < b["outStart"]
    assert items[-1]["outEnd"] == pytest.approx(edl["duration"])
    assert edl["duration"] < THREE[-1].end  # pauses removed


def test_item_cut_finds_sentence_start():
    hits = find_scores(THREE)
    cut = item_cut(THREE, hits[1])
    assert THREE[cut].text == "this" and THREE[cut - 1].text == "email."


def test_redact_boxes(tmp_path):
    edl = build_ranking_edl(
        _job(tmp_path, [(400, 900)] * 3, redact={"2.png": [[10, 20, 200, 40]]}), THREE
    )
    assert edl["items"][0]["redact"] == []
    assert edl["items"][1]["redact"] == [{"x": 10, "y": 20, "w": 200, "h": 40}]
    assert (edl["items"][1]["imgW"], edl["items"][1]["imgH"]) == (400, 900)


def test_captions_break_at_items(tmp_path):
    edl = build_ranking_edl(_job(tmp_path, [(400, 900)] * 3), THREE)
    starts = {round(c["outStart"], 3) for c in edl["captions"]}
    for item in edl["items"]:
        assert round(item["outStart"], 3) in starts
    assert any("a 7 out of 10" in c["text"] for c in edl["captions"])


def test_review_md(tmp_path):
    job = _job(tmp_path, [(400, 900)] * 3)
    edl = build_ranking_edl(job, THREE)
    path = job / "review.md"
    write_review(edl, path)
    text = path.read_text(encoding="utf-8")
    for item in edl["items"]:
        assert f"{item['score']}/10" in text
        assert item["shot"].split("/")[-1] in text
    for cap in edl["captions"]:
        assert cap["text"] in text


def test_safe_area_numbers():
    assert SAFE == {"x": SAFE_X0, "y": SAFE_Y0, "w": SAFE_X1 - SAFE_X0, "h": SAFE_Y1 - SAFE_Y0}


def test_a_bit_too_tall_shot_is_shrunk_to_fit_not_cropped(tmp_path):
    # the real recording's screenshots: 780x2400 is 1295 px tall at full column width
    edl = build_ranking_edl(_job(tmp_path, [(780, 2400)] * 3), THREE)
    box = edl["items"][0]["box"]
    assert edl["items"][0]["crop"] is False
    assert box["h"] == SAFE_Y1 - BAND_TOP
    assert box["w"] == round(box["h"] * 780 / 2400)
    assert box["x"] == 65 and box["y"] == BAND_TOP


@pytest.mark.parametrize("size", [(400, 900), (780, 2400), (1080, 8000), (1600, 900), (400, 500)])
def test_everything_inside_the_safe_area(tmp_path, size):
    edl = build_ranking_edl(_job(tmp_path, [size] * 3), THREE)
    assert edl["safe"] == SAFE

    def inside(x0, y0, x1, y1):
        assert SAFE_X0 <= x0 and x1 <= SAFE_X1 and SAFE_Y0 <= y0 and y1 <= SAFE_Y1

    cap = edl["caption"]
    inside(cap["x"], cap["y"], cap["x"] + cap["w"], cap["y"] + cap["h"])
    for item in edl["items"]:
        b, badge = item["box"], item["badge"]
        inside(b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"])
        # badge grows left from its right edge; the widest one ("10/10") is ~240 px
        inside(badge["right"] - 240, badge["top"], badge["right"], badge["top"] + badge["h"])
        # captions never sit on a screenshot
        clear = cap["x"] >= b["x"] + b["w"] or cap["y"] >= b["y"] + b["h"]
        assert clear, (cap, b)


def test_badge_sits_on_the_shot_top_right_corner(tmp_path):
    edl = build_ranking_edl(_job(tmp_path, [(400, 900), (780, 2400), (1600, 900)]), THREE)
    for item in edl["items"]:
        b, badge = item["box"], item["badge"]
        assert badge["h"] == 106
        assert badge["top"] == b["y"] - 53  # straddles the shot's top edge
        assert badge["right"] == b["x"] + b["w"] + 24  # a little past its right edge
    # it follows each screenshot rather than a fixed spot
    assert len({i["badge"]["right"] for i in edl["items"]}) > 1


def test_caption_box_right_of_column_at_bottom_of_safe_area(tmp_path):
    edl = build_ranking_edl(_job(tmp_path, [(400, 900)] * 3), THREE)
    cap = edl["caption"]
    assert cap["x"] == 65 + 421 + 28
    assert cap["x"] + cap["w"] == SAFE_X1
    assert cap["y"] + cap["h"] == SAFE_Y1


def test_audio_silences_cut_and_times_still_map(tmp_path):
    words = _spoken(
        "this is a zero out of ten email.",
        "this one is a seven out of ten.",
        "and this one is a ten out of ten.",
        pause=0.2,  # whisper saw no pauses...
    )
    plain = build_ranking_edl(_job(tmp_path, [(400, 900)] * 3), words, silences=[])
    # ...but the audio is silent for 0.9 s inside "email." (whisper stretched it)
    email = next(w for w in words if w.text == "email.")
    quiet = (email.start + 0.05, email.start + 0.95)
    cut = build_ranking_edl(_job(tmp_path / "b", [(400, 900)] * 3), words, silences=[quiet])
    assert len(cut["spans"]) == len(plain["spans"]) + 1
    assert cut["duration"] == pytest.approx(plain["duration"] - (0.9 - 2 * 0.08), abs=1e-3)
    for a, b in zip(cut["items"], cut["items"][1:]):
        assert a["outEnd"] == b["outStart"] and a["outStart"] < b["outStart"]
    assert cut["items"][-1]["outEnd"] == pytest.approx(cut["duration"])
    for c in cut["captions"]:
        assert 0 <= c["outStart"] < c["outEnd"] <= cut["duration"] + 1e-6
