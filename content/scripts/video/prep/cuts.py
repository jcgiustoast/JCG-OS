"""Remove pauses: keep only the stretches of the recording where words are spoken."""
from __future__ import annotations

from dataclasses import dataclass

from .words import Word


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
) -> list[Span]:
    """Group words separated by gaps <= max_gap; pad each group; drop the rest."""
    if not words:
        return []
    groups: list[list[float]] = [[words[0].start, words[0].end]]
    for w in words[1:]:
        if w.start - groups[-1][1] > max_gap:
            groups.append([w.start, w.end])
        else:
            groups[-1][1] = max(groups[-1][1], w.end)

    spans: list[Span] = []
    out = 0.0
    for i, (start, end) in enumerate(groups):
        lo = start - pad
        hi = end + pad
        if i > 0:  # never reach back past the middle of the gap before us
            lo = max(lo, (groups[i - 1][1] + start) / 2)
        if i + 1 < len(groups):  # nor forward past the middle of the gap after us
            hi = min(hi, (end + groups[i + 1][0]) / 2)
        lo = max(lo, 0.0)
        if duration is not None:
            hi = min(hi, duration)
        spans.append(Span(round(lo, 4), round(hi, 4), round(out, 4)))
        out += hi - lo
    return spans


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
