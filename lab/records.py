"""The answer record: the one shape every tool shares (specs/cross-cutting.md).

This module owns the label vocabulary. In this chunk it parses a model's raw
answer and checks only that the tier is known; full rule validation arrives
in P1-C03 (`validate`).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal

TIERS: tuple[str, ...] = (
    "prohibited",
    "high-risk",
    "transparency-only",
    "minimal",
    "out-of-scope",
    "needs-human-review",
)
REVIEW_TIER = "needs-human-review"
MAX_RAW_CHARS = 4000

ParseStatus = Literal["ok", "unreadable"]


@dataclass(frozen=True)
class Record:
    tier: str
    route: str | None
    annex_iii_area: int | None
    annex_iii_point: str | None
    annex_i_legislation: str | None
    art50_flag: bool
    articles: tuple[str, ...]
    review_reason: str | None
    reason: str

    @classmethod
    def from_json(cls, data: dict) -> Record:
        """Build a record from a decoded JSON object. Raises KeyError or TypeError if malformed."""
        return cls(
            tier=data["tier"],
            route=data["route"],
            annex_iii_area=data["annex_iii_area"],
            annex_iii_point=data["annex_iii_point"],
            annex_i_legislation=data["annex_i_legislation"],
            art50_flag=data["art50_flag"],
            articles=tuple(data["articles"]),
            review_reason=data["review_reason"],
            reason=data["reason"],
        )


def _first_json_object(raw: str) -> dict | None:
    """Return the first `{...}` in the text that decodes as a JSON object, or None."""
    decoder = json.JSONDecoder()
    start = raw.find("{")
    while start != -1:
        try:
            obj, _ = decoder.raw_decode(raw, start)
        except json.JSONDecodeError:
            obj = None
        if isinstance(obj, dict):
            return obj
        start = raw.find("{", start + 1)
    return None


def parse_answer(raw: str | None) -> tuple[Record | None, ParseStatus]:
    """Read a model's raw answer as a record (ADR-005). Never repairs or guesses."""
    if not isinstance(raw, str) or len(raw) > MAX_RAW_CHARS:
        return None, "unreadable"
    obj = _first_json_object(raw)
    if obj is None:
        return None, "unreadable"
    try:
        record = Record.from_json(obj)
    except (KeyError, TypeError):
        return None, "unreadable"
    if record.tier not in TIERS:
        return None, "unreadable"
    return record, "ok"
