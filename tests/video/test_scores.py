from content.scripts.video.prep.scores import ScoreHit, find_scores
from content.scripts.video.prep.words import Word, load_words, save_words
from tests.video.helpers import words_from


def test_digits():
    hits = find_scores(words_from("this is a 0 out of 10 email"))
    assert [(h.score, h.word_index) for h in hits] == [(0, 3)]
    assert hits[0].start == 0.9


def test_number_words():
    hits = find_scores(words_from("this one is a three out of ten"))
    assert [(h.score, h.word_index) for h in hits] == [(3, 4)]


def test_slash():
    assert [h.score for h in find_scores(words_from("honestly 7/10"))] == [7]
    assert [h.score for h in find_scores(words_from("honestly 7/10."))] == [7]


def test_ten_out_of_ten():
    hits = find_scores(words_from("a 10 out of 10"))
    assert [(h.score, h.word_index) for h in hits] == [(10, 1)]


def test_punctuation_case():
    assert [h.score for h in find_scores(words_from("Zero out of ten."))] == [0]


def test_order():
    text = "first is a two out of ten then a 5 out of 10 and finally 9/10"
    hits = find_scores(words_from(text))
    assert [h.score for h in hits] == [2, 5, 9]
    assert hits == sorted(hits, key=lambda h: h.start)


def test_out_of_other_number_is_not_a_score():
    assert find_scores(words_from("three out of five people")) == []


def test_save_load_roundtrip(tmp_path):
    words = [Word("hi", 0.0, 0.25), Word("there", 0.3, 0.6)]
    path = tmp_path / "words.json"
    save_words(words, path)
    assert load_words(path) == words
    assert isinstance(ScoreHit(1, 0, 0.0), ScoreHit)
