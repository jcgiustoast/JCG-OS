"""Remove pauses: keep only the stretches of the recording where words are spoken."""
from __future__ import annotations

from dataclasses import dataclass

from .words import Word

MIN_PIECE = 0.05  # a spoken stretch shorter than this between two pauses is a click, not a word


@dataclass(frozen=True)
class Span:
    src_start: float  # seconds in the source recording
    src_end: float
    out_start: float  # where this stretch begins in the finished video


def keep_spans(
    words: list[Word],
    max_gap: float = 0.3,
    pad: float = 0.08,
    duration: float | None = None,
    silences: list[tuple[float, float]] | None = None,
) -> list[Span]:
    """Cut every pause longer than max_gap; pad what's left; lay it end to end.

    A pause is either a gap between two words or a stretch the audio says is
    silent (`silences`, from find_silences). The second matters because whisper
    stretches words across pauses ("create" 24.2 -> 26.1 when the sound starts
    at 25.6), so word gaps alone miss them. Silences are quiet by definition, so
    cutting them never cuts into a word's sound.
    """
    if not words:
        return []
    quiet = [(a, b) for a, b in (silences or []) if b - a > max_gap]
    gaps = [(a.end, b.start) for a, b in zip(words, words[1:]) if b.start - a.end > max_gap]
    # where the audio measured a gap, trust the audio's edges over whisper's
    # (sound can run past a word's end); gaps with no measured silence at all
    # (a breath, room noise) are still cut on the word times
    pauses = [g for g in gaps if not any(a < g[1] and b > g[0] for a, b in quiet)] + quiet
    pauses.sort()
    merged: list[list[float]] = []
    for a, b in pauses:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])

    # spoken stretches: first word start -> last word end, minus the pauses
    pieces: list[list[float]] = []
    cursor = words[0].start
    stop = max(w.end for w in words)
    for a, b in merged:
        if b <= cursor or a >= stop:
            continue
        if a > cursor:
            pieces.append([cursor, a])
        cursor = max(cursor, b)
    if cursor < stop:
        pieces.append([cursor, stop])
    pieces = [p for p in pieces if p[1] - p[0] >= MIN_PIECE]
    if not pieces:
        return []

    spans: list[Span] = []
    out = 0.0
    for i, (start, end) in enumerate(pieces):
        lo = start - pad
        hi = end + pad
        if i > 0:  # never reach back past the middle of the pause before us
            lo = max(lo, (pieces[i - 1][1] + start) / 2)
        if i + 1 < len(pieces):  # nor forward past the middle of the pause after us
            hi = min(hi, (end + pieces[i + 1][0]) / 2)
        lo = max(lo, 0.0)
        if duration is not None:
            hi = min(hi, duration)
        spans.append(Span(round(lo, 4), round(hi, 4), round(out, 4)))
        out += hi - lo
    return spans


def speech_threshold(levels_db: list[float], min_contrast: float = 15.0) -> float | None:
    """Level (dB) below which the recording counts as silent.

    Halfway between the room (10th percentile of the short-window levels) and
    the voice (90th percentile). None when the two are too close to tell apart
    (no real quiet part, or a noisy room): then only word gaps are cut.
    """
    if not levels_db:
        return None
    ordered = sorted(levels_db)
    room = ordered[int(0.10 * (len(ordered) - 1))]
    voice = ordered[int(0.90 * (len(ordered) - 1))]
    if voice - room < min_contrast:
        return None
    return (room + voice) / 2


def find_silences(
    levels_db: list[float], step: float, threshold: float, min_len: float = 0.3
) -> list[tuple[float, float]]:
    """Stretches (start, end) in seconds where every window is below threshold."""
    found: list[tuple[float, float]] = []
    run_start: int | None = None
    for i, level in enumerate(list(levels_db) + [float("inf")]):
        if level < threshold:
            if run_start is None:
                run_start = i
        elif run_start is not None:
            a, b = run_start * step, i * step
            if b - a >= min_len - 1e-9:
                found.append((round(a, 4), round(b, 4)))
            run_start = None
    return found


def total(spans: list[Span]) -> float:
    return sum(s.src_end - s.src_start for s in spans)


def to_out(t: float, spans: list[Span]) -> float:
    """Source time -> finished-video time. A time inside a removed pause maps to the next kept stretch."""
    for s in spans:
        if t < s.src_start:
            return s.out_start
        if t <= s.src_end:
            return s.out_start + (t - s.src_start)
    return total(spans)


def to_src(t_out: float, spans: list[Span]) -> float:
    """Finished-video time -> source time (inverse of to_out). Clamps to the nearest edge."""
    if not spans:
        return 0.0
    if t_out <= spans[0].out_start:
        return spans[0].src_start
    for s in spans:
        if t_out <= s.out_start + (s.src_end - s.src_start):
            return s.src_start + (t_out - s.out_start)
    return spans[-1].src_end
