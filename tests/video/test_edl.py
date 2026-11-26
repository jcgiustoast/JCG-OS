import json

import pytest
from PIL import Image

from content.scripts.video.prep.edl import (
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
    assert box["y"] >= 96 and box["y"] + box["h"] <= 1843
    assert abs((box["y"] + box["h"] / 2) - 0.47 * H) <= 1


def test_very_tall_is_cropped(tmp_path):
    edl = build_ranking_edl(_job(tmp_path, [(1080, 8000)] * 3), THREE)
    item = edl["items"][0]
    assert item["crop"] is True
    assert item["box"] == {"x": 65, "y": 96, "w": 421, "h": 1747}


def test_wide_layout(tmp_path):
    edl = build_ranking_edl(_job(tmp_path, [(1600, 900)] * 3), THREE)
    item = edl["items"][0]
    assert item["layout"] == "wide"
    assert item["box"]["x"] == 65 and item["box"]["w"] == 508 and item["box"]["y"] == 230


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
