from content.scripts.video.prep.words import Word


def words_from(text: str, start: float = 0.0, step: float = 0.3) -> list[Word]:
    """Evenly spaced words, `step` seconds each, no gaps."""
    out = []
    t = start
    for token in text.split():
        out.append(Word(token, round(t, 3), round(t + step, 3)))
        t += step
    return out
