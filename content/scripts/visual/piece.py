import re
from dataclasses import dataclass, field

_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text):
    """Return (meta_dict, body_after_frontmatter). Raises ValueError if absent."""
    m = _FRONTMATTER.match(text)
    if not m:
        raise ValueError("piece.md must start with a YAML frontmatter block (--- ... ---)")
    meta = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip()
    return meta, text[m.end():]


@dataclass
class Slide:
    type: str
    fields: dict = field(default_factory=dict)


@dataclass
class Piece:
    meta: dict
    slides: list


_SLIDE_HEADER = re.compile(r"^#\s*slide:([a-z0-9-]+)\s*$", re.IGNORECASE)


def _add(fields, key, val):
    if key in fields:
        if not isinstance(fields[key], list):
            fields[key] = [fields[key]]
        fields[key].append(val)
    else:
        fields[key] = val


def parse_piece(text):
    meta, body = parse_frontmatter(text)
    slides, current = [], None
    for raw in body.splitlines():
        header = _SLIDE_HEADER.match(raw.strip())
        if header:
            current = Slide(type=header.group(1).lower())
            slides.append(current)
            continue
        if current is None:
            continue
        line = raw.strip()
        if not line:
            continue
        key, sep, val = line.partition(":")
        if not sep:
            continue
        _add(current.fields, key.strip(), val.strip())
    return Piece(meta=meta, slides=slides)


def parse_pipes(value):
    """'a | b | c' -> ['a','b','c'] (stripped)."""
    return [p.strip() for p in value.split("|")]


def parse_bars(value):
    """'€10:34, €30:100*' -> [{label,height,hi}]. Trailing '*' marks the highlighted bar."""
    out = []
    for chunk in value.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        label, _, h = chunk.rpartition(":")
        hi = h.endswith("*")
        try:
            height = int(h.rstrip("*"))
        except ValueError:
            raise ValueError(f"parse_bars: height must be an integer in chunk {chunk!r}")
        out.append({"label": label.strip(), "height": height, "hi": hi})
    return out
