from content.scripts.video.prep.captions import Caption, make_captions
from content.scripts.video.prep.words import Word
from tests.video.helpers import words_from


def test_lowercase_no_punct():
    caps = make_captions(words_from("This is GREAT. I don't know, really"), breaks=[])
    assert " ".join(c.text for c in caps) == "this is great i don't know really"


def test_score_digits():
    caps = make_captions(words_from("a three out of ten email and this one is fine"), breaks=[])
    text = " ".join(c.text for c in caps)
    assert "a 3 out of 10 email" in text
    assert "this one is" in text


def test_slash_score_spelled_out():
    caps = make_captions(words_from("honestly this is a 7/10 for me"), breaks=[])
    assert "a 7 out of 10 for me" in " ".join(c.text for c in caps)


def test_max_13_words():
    caps = make_captions(words_from(" ".join(f"w{i}" for i in range(30)), step=0.15), breaks=[])
    assert all(len(c.text.split()) <= 13 for c in caps)
    assert sum(len(c.text.split()) for c in caps) == 30


def test_min_5_words():
    words = words_from("one two three four five six seven eight nine ten eleven twelve")
    # pauses after every 2nd word tempt short phrases
    spaced = [Word(w.text, w.start + (i // 2) * 0.5, w.end + (i // 2) * 0.5) for i, w in enumerate(words)]
    caps = make_captions(spaced, breaks=[])
    assert all(len(c.text.split()) >= 5 for c in caps)


def test_short_recording_single_caption():
    caps = make_captions(words_from("hi there"), breaks=[])
    assert [c.text for c in caps] == ["hi there"]


def test_break_starts_new_caption():
    words = words_from(" ".join(f"w{i}" for i in range(20)))
    caps = make_captions(words, breaks=[7])
    assert any(c.src_start == words[7].start for c in caps)
    assert all(not (c.src_start < words[7].start < c.src_end) for c in caps)


def test_max_3_seconds():
    caps = make_captions(words_from(" ".join(f"w{i}" for i in range(20)), step=0.6), breaks=[])
    assert all(c.src_end - c.src_start <= 3.0 + 1e-6 for c in caps)


def test_caption_times_follow_words():
    words = words_from("this is a short little caption here")
    caps = make_captions(words, breaks=[])
    assert caps[0] == Caption("this is a short little caption here", words[0].start, words[-1].end)
