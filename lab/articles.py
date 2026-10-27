"""Valid citations of the AI Act (EV-4), checked against `data/articles.json`.

Grammar: `Art. <n>` or `Article <n>`, optionally `(<paragraph>)`, then up to two
point groups such as `(a)` and `(iii)`; or `Annex <roman>` optionally followed
by a point such as `4(a)` or `(a)`. Paragraph and annex points are checked
against the table; letter points inside a paragraph are not listed there and
are accepted as written.
"""

from __future__ import annotations

import json
import re
from functools import cache
from pathlib import Path

TABLE_PATH = Path(__file__).resolve().parent.parent / "data" / "articles.json"

_ARTICLE = re.compile(
    r"(?:art\.|article)\s*(\d+[a-z]?)\s*(?:\(\s*(\d+[a-z]?)\s*\))?"
    r"((?:\s*\(\s*[a-z]{1,4}\s*\)){0,2})",
    re.IGNORECASE,
)
_ANNEX = re.compile(
    r"annex\s+([ivxl]+)(?:\s+(\d+(?:\([a-z]\))?|\([a-z]\)))?", re.IGNORECASE
)


@cache
def _table() -> dict:
    return json.loads(TABLE_PATH.read_text(encoding="utf-8"))


def _parse(citation: str) -> tuple[str, str, str | None, str] | None:
    """Return (kind, number, paragraph or point, points suffix), or None."""
    if not isinstance(citation, str):
        return None
    text = citation.strip()
    if m := _ARTICLE.fullmatch(text):
        points = re.sub(r"\s+", "", m.group(3)).lower()
        return "article", m.group(1).lower(), m.group(2), points
    if m := _ANNEX.fullmatch(text):
        return "annex", m.group(1).upper(), m.group(2), ""
    return None


def normalise(citation: str) -> str | None:
    """Canonical form, such as "Art. 6(2)" or "Annex III 4(a)"; None outside the grammar."""
    parsed = _parse(citation)
    if parsed is None:
        return None
    kind, number, part, points = parsed
    if kind == "article":
        return f"Art. {number}" + (f"({part})" if part else "") + points
    return f"Annex {number}" + (f" {part}" if part else "")


def is_valid(citation: str) -> bool:
    """True when the citation follows the grammar and names a real provision."""
    parsed = _parse(citation)
    if parsed is None:
        return False
    kind, number, part, _ = parsed
    listing = _table()["articles" if kind == "article" else "annexes"].get(number)
    if listing is None:
        return False
    return part is None or part in listing


def article_number(citation: str) -> str | None:
    """The article number, for overlap at article level ("Art. 6(2)" -> "6")."""
    parsed = _parse(citation)
    return parsed[1] if parsed and parsed[0] == "article" else None
