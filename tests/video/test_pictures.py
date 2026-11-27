import json

import pytest
from PIL import Image

from content.scripts.video.prep.cuts import keep_spans
from content.scripts.video.prep.edl import PrepError
from content.scripts.video.prep.pictures import (
    PictureChoice,
    find_phrase,
    load_choices,
    place,
    suggest_show,
    write_stub,
)
from tests.video.helpers import words_from


def _job(tmp_path, names=("1.png", "2.png")):
    shots = tmp_path / "shots"
    shots.mkdir()
    for n in names:
        Image.new("RGB", (100, 100)).save(shots / n)
    return tmp_path


def _spans(words):
    return keep_spans(words, pad=0.0)


def _write(job, rows):
    (job / "pictures.json").write_text(json.dumps(rows))


def test_suggest_show():
    assert suggest_show(1080, 3000) == "full"
    assert suggest_show(1170, 2532) == "card"
    assert suggest_show(1080, 1200) == "card"
    assert suggest_show(1200, 800) == "card"


def test_write_stub_never_overwrites(tmp_path):
    job = _job(tmp_path)
    assert write_stub(job) is True
    path = job / "pictures.json"
    rows = json.loads(path.read_text())
    assert [r["picture"] for r in rows] == ["1.png", "2.png"]
    rows[0]["words"] = "my edit"
    path.write_text(json.dumps(rows))
    assert write_stub(job) is False
    assert json.loads(path.read_text())[0]["words"] == "my edit"


def test_load_choices_ok(tmp_path):
    job = _job(tmp_path)
    _write(job, [{"picture": "1.png", "words": "a b", "show": "card"}, {"picture": "2.png", "words": "c d", "show": "full"}])
    assert load_choices(job)[1] == PictureChoice("2.png", "c d", "full")


def test_load_choices_rejects_empty_words(tmp_path):
    job = _job(tmp_path)
    _write(job, [{"picture": "1.png", "words": "", "show": "card"}, {"picture": "2.png", "words": "x", "show": "card"}])
    with pytest.raises(PrepError, match="1.png"):
        load_choices(job)


def test_load_choices_rejects_unlisted_picture(tmp_path):
    job = _job(tmp_path)
    _write(job, [{"picture": "1.png", "words": "a", "show": "card"}])
    with pytest.raises(PrepError, match="2.png"):
        load_choices(job)


def test_load_choices_rejects_bad_show_and_missing_file(tmp_path):
    job = _job(tmp_path, ("1.png",))
    _write(job, [{"picture": "1.png", "words": "a", "show": "big"}])
    with pytest.raises(PrepError, match="1.png"):
        load_choices(job)
    _write(job, [{"picture": "9.png", "words": "a", "show": "card"}])
    with pytest.raises(PrepError, match="9.png"):
        load_choices(job)
    (job / "pictures.json").unlink()
    with pytest.raises(PrepError):
        load_choices(job)


def test_find_phrase_ignores_case_and_punctuation():
    words = words_from("So, Bloom's page IS great.")
    assert find_phrase(words, "blooms page is") == 1


def test_find_phrase_after():
    words = words_from("big win here and big win again")
    assert find_phrase(words, "big win") == 0
    assert find_phrase(words, "big win", after=1) == 4
    assert find_phrase(words, "nothing") == -1


def _talk(n):
    return words_from(" ".join(f"w{i}" for i in range(n)))


def test_place_starts_at_phrase_and_ends_at_next():
    words = _talk(60)  # 18 s
    choices = [PictureChoice("1.png", "w15 w16", "card"), PictureChoice("2.png", "w30 w31", "card")]
    placed = place(words, choices, _spans(words))
    assert placed[0]["outStart"] == pytest.approx(4.5)
    assert placed[0]["wordIndex"] == 15
    assert placed[0]["outEnd"] == placed[1]["outStart"] == pytest.approx(9.0)
    assert placed[0]["pushed"] is False


def test_place_caps_card_at_six_seconds():
    words = _talk(90)
    choices = [PictureChoice("1.png", "w15 w16", "card"), PictureChoice("2.png", "w45 w46", "card")]
    p = place(words, choices, _spans(words))
    assert p[0]["outEnd"] - p[0]["outStart"] == pytest.approx(6.0)


def test_place_last_picture_ends_at_video_end_or_cap():
    words = _talk(60)  # ends 18 s
    p = place(words, [PictureChoice("1.png", "w50 w51", "card")], _spans(words))
    assert p[0]["outEnd"] == pytest.approx(18.0)
    p = place(words, [PictureChoice("1.png", "w15 w16", "card")], _spans(words))
    assert p[0]["outEnd"] - p[0]["outStart"] == pytest.approx(6.0)


def test_phrase_not_heard_stops():
    words = _talk(30)
    with pytest.raises(PrepError) as e:
        place(words, [PictureChoice("7.png", "never said", "card")], _spans(words))
    assert "7.png" in str(e.value) and "never said" in str(e.value)


def test_phrase_before_previous_picture_stops():
    words = _talk(60)
    choices = [PictureChoice("1.png", "w30 w31", "card"), PictureChoice("2.png", "w10 w11", "card")]
    with pytest.raises(PrepError, match="before the previous picture"):
        place(words, choices, _spans(words))


def test_picture_inside_title_is_pushed_to_three_seconds():
    words = _talk(60)
    p = place(words, [PictureChoice("1.png", "w4 w5", "card")], _spans(words))
    assert p[0]["outStart"] == 3.0 and p[0]["pushed"] is True


def test_too_close_stops():
    words = _talk(60)
    choices = [PictureChoice("1.png", "w15 w16", "card"), PictureChoice("2.png", "w18 w19", "card")]
    with pytest.raises(PrepError) as e:
        place(words, choices, _spans(words))
    assert "1.png" in str(e.value) and "2.png" in str(e.value)
