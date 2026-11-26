import pytest

from content.scripts.video.prep.cuts import Span, keep_spans, to_out, total
from content.scripts.video.prep.words import Word

PAD = 0.08


def test_gap_removed():
    words = [Word("a", 0.5, 1.0), Word("b", 1.0, 1.5), Word("c", 2.5, 3.0), Word("d", 3.0, 3.5)]
    spans = keep_spans(words, max_gap=0.3, pad=PAD)
    assert len(spans) == 2
    assert total(spans) == pytest.approx(2.0 + 4 * PAD)
    assert spans[1].out_start == pytest.approx(spans[0].src_end - spans[0].src_start)


def test_small_gap_kept():
    words = [Word("a", 0.5, 1.0), Word("b", 1.2, 1.6)]
    assert len(keep_spans(words, max_gap=0.3, pad=PAD)) == 1


def test_leading_trailing_silence_trimmed():
    words = [Word("a", 1.5, 2.0), Word("b", 2.0, 2.4)]
    spans = keep_spans(words, max_gap=0.3, pad=PAD, duration=10.0)
    assert spans[0].src_start == pytest.approx(1.5 - PAD)
    assert spans[-1].src_end == pytest.approx(2.4 + PAD)


def test_pad_clamped_to_recording():
    spans = keep_spans([Word("a", 0.02, 0.5)], pad=PAD, duration=0.53)
    assert spans[0].src_start == 0.0
    assert spans[0].src_end == pytest.approx(0.53)


def test_to_out():
    spans = [Span(1.0, 2.0, 0.0), Span(3.0, 4.0, 1.0)]
    assert to_out(1.5, spans) == pytest.approx(0.5)
    assert to_out(3.25, spans) == pytest.approx(1.25)
    assert to_out(2.5, spans) == pytest.approx(1.0)  # in the removed gap -> next span start
    assert to_out(0.2, spans) == 0.0
    assert to_out(9.0, spans) == pytest.approx(2.0)


def test_pad_never_overlaps():
    words = [Word("a", 0.5, 1.0), Word("b", 1.31, 1.8)]
    spans = keep_spans(words, max_gap=0.3, pad=PAD)
    assert len(spans) == 2
    assert spans[0].src_end <= spans[1].src_start


def test_tiny_gap_with_big_pad_never_overlaps():
    words = [Word("a", 0.5, 1.0), Word("b", 1.35, 1.8)]
    spans = keep_spans(words, max_gap=0.3, pad=0.3)
    assert all(a.src_end <= b.src_start for a, b in zip(spans, spans[1:]))
