"""Transparent Background: Juan's hand-written caption fixes (fixes.json), applied on every prep run."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .edl import PrepError

FILE = "fixes.json"


def load_fixes(job: Path) -> dict[str, str]:
    p = Path(job) / FILE
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        raise PrepError(f"{FILE} is not valid JSON ({e}). Check commas and quotes.") from e
    if not isinstance(data, dict):
        raise PrepError(f'{FILE} must look like {{"what whisper heard": "what Juan means"}}.')
    return {str(k): str(v) for k, v in data.items()}


def apply_fixes(text: str, fixes: dict[str, str]) -> str:
    for key in sorted(fixes, key=len, reverse=True):
        if not key.strip():
            continue
        pattern = r"(?<!\w)" + re.escape(key) + r"(?!\w)"
        text = re.sub(pattern, lambda _m, v=fixes[key]: v, text, flags=re.IGNORECASE)
    return text
