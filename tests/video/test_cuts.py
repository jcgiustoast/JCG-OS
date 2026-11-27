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


# --- real silence from the audio (whisper stretches words across pauses) ---

from content.scripts.video.prep.cuts import find_silences, speech_threshold  # noqa: E402


def test_silence_inside_stretched_word_is_cut():
    # whisper says "create" runs 24.18-26.08, but the audio is silent 23.3-25.6
    words = [Word("10,", 22.7, 23.2), Word("create", 24.18, 26.08), Word("gummies", 26.08, 27.44)]
    spans = keep_spans(words, pad=PAD, silences=[(23.3, 25.6)])
    assert len(spans) == 2
    assert spans[0].src_end == pytest.approx(23.3 + PAD)
    assert spans[1].src_start == pytest.approx(25.6 - PAD)
    # the stretched word's start maps to where its sound really begins
    assert to_out(24.18, spans) == pytest.approx(spans[1].out_start)


def test_short_silence_not_cut():
    words = [Word("a", 1.0, 2.0), Word("b", 2.0, 3.0)]
    assert len(keep_spans(words, pad=PAD, silences=[(1.5, 1.75)])) == 1


def test_leading_silence_past_first_word_start_trimmed():
    words = [Word("grooms", 2.1, 2.66), Word("3", 3.08, 3.64)]
    spans = keep_spans(words, pad=PAD, silences=[(0.0, 2.27)], duration=31.0)
    assert spans[0].src_start == pytest.approx(2.27 - PAD)


def test_trailing_silence_inside_last_word_trimmed():
    words = [Word("out", 29.88, 30.42), Word("there.", 30.42, 31.2)]
    spans = keep_spans(words, pad=PAD, silences=[(30.7, 31.25)], duration=31.25)
    assert spans[-1].src_end == pytest.approx(30.7 + PAD)


def test_silences_and_word_gaps_both_cut():
    words = [Word("a", 0.5, 1.0), Word("b", 2.0, 4.0), Word("c", 4.0, 5.0)]
    spans = keep_spans(words, pad=PAD, silences=[(2.5, 3.5)])
    assert len(spans) == 3
    assert all(a.src_end <= b.src_start for a, b in zip(spans, spans[1:]))
    assert total(spans) == pytest.approx(0.5 + 0.5 + 1.5 + 6 * PAD)


def test_find_silences():
    loud, quiet = -20.0, -50.0
    levels = [loud] * 10 + [quiet] * 20 + [loud] * 5 + [quiet] * 10 + [loud] * 5
    # 20 ms steps: a 0.4 s quiet stretch at 0.2 s, a 0.2 s one at 0.7 s
    found = find_silences(levels, step=0.02, threshold=-35.0, min_len=0.3)
    assert found == [pytest.approx((0.2, 0.6))]


def test_find_silences_at_end():
    levels = [-20.0] * 10 + [-50.0] * 20
    assert find_silences(levels, step=0.02, threshold=-35.0, min_len=0.3) == [pytest.approx((0.2, 0.6))]


def test_speech_threshold_halfway_between_room_and_voice():
    levels = [-52.0] * 50 + [-20.0] * 50
    assert speech_threshold(levels) == pytest.approx(-36.0)


def test_speech_threshold_none_when_no_quiet_part():
    # wall-to-wall talking: no level is far enough below the voice to call silence
    levels = [-22.0, -20.0, -18.0, -24.0] * 30
    assert speech_threshold(levels) is None


def test_to_src_inverts_to_out():
    from content.scripts.video.prep.cuts import to_src

    words = [Word("a", 0.5, 1.0), Word("b", 1.0, 1.5), Word("c", 2.5, 3.0), Word("d", 3.0, 3.5)]
    spans = keep_spans(words, max_gap=0.3, pad=PAD)
    for t in (0.6, 1.2, 2.7, 3.2):
        assert to_src(to_out(t, spans), spans) == pytest.approx(t)
