"""The answer record: the one shape every tool shares (specs/cross-cutting.md).

This module owns the vocabularies, the record rules (`validate`), the only
reader of a model's raw answer (`parse_answer`, ADR-005) and the date detector
(`contains_date`, EV-8). A model's text is untrusted: it is read, never
repaired.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, fields
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
HIGH_RISK = "high-risk"
ROUTES: tuple[str, ...] = ("annex-iii", "annex-i")
REVIEW_REASONS: tuple[str, ...] = ("missing-fact", "conflicting-facts", "unsettled-law")
TAGS: tuple[str, ...] = (
    "boundary",
    "art6-3",
    "hidden-instruction",
    "annex-i",
    *(f"area-{n}" for n in range(1, 9)),
)
MAX_RAW_CHARS = 4000
MAX_REASON_WORDS = 40

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
        """Build a record from a decoded JSON object.

        Raises KeyError for a missing field, ValueError for an unknown one, and
        TypeError when `articles` is not a list. Every other type is checked by
        `validate`.
        """
        unknown = set(data) - FIELD_NAMES
        if unknown:
            raise ValueError(f"unknown fields: {', '.join(sorted(unknown))}")
        if not isinstance(data["articles"], list):
            raise TypeError("articles must be a list")
        return cls(
            **{
                **{name: data[name] for name in FIELD_NAMES},
                "articles": tuple(data["articles"]),
            }
        )

    def to_json(self) -> dict:
        return {**asdict(self), "articles": list(self.articles)}


FIELD_NAMES = frozenset(f.name for f in fields(Record))


# ---------- rules ----------

# Periods that do not end a sentence: abbreviations used in legal citations and
# decimals such as "6.5". Matched case-insensitively, as whole words.
_ABBREVIATIONS = re.compile(
    r"\b(?:Arts?|e\.g|i\.e|etc|No|Nos|Reg|para|paras|pt|pts|sec|cf|vs|pp?|Inc|Ltd|Co)\.",
    re.IGNORECASE,
)
_DECIMAL = re.compile(r"\d\.\d")
_ANNEX_III_POINT = re.compile(r"([1-8])(?:\([a-z]\))?")


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_tier(r: Record) -> list[str]:
    return (
        []
        if isinstance(r.tier, str) and r.tier in TIERS
        else [f"tier: unknown value {r.tier!r}"]
    )


def _check_route(r: Record) -> list[str]:
    if r.tier == HIGH_RISK:
        if not (isinstance(r.route, str) and r.route in ROUTES):
            return [f"route: required for high-risk, one of {', '.join(ROUTES)}"]
        return []
    return (
        [] if r.route is None else ["route: must be null unless the tier is high-risk"]
    )


def _check_annex_iii(r: Record) -> list[str]:
    if r.route != "annex-iii":
        out = []
        if r.annex_iii_area is not None:
            out.append("annex_iii_area: must be null unless the route is annex-iii")
        if r.annex_iii_point is not None:
            out.append("annex_iii_point: must be null unless the route is annex-iii")
        return out
    out = []
    area_ok = _is_int(r.annex_iii_area) and 1 <= r.annex_iii_area <= 8
    if not area_ok:
        out.append("annex_iii_area: required for annex-iii, a whole number 1 to 8")
    match = (
        _ANNEX_III_POINT.fullmatch(r.annex_iii_point)
        if isinstance(r.annex_iii_point, str)
        else None
    )
    if match is None:
        out.append("annex_iii_point: required for annex-iii, such as 4(a)")
    elif area_ok and int(match.group(1)) != r.annex_iii_area:
        out.append("annex_iii_point: must belong to the stated area")
    return out


def _check_annex_i(r: Record) -> list[str]:
    if r.route == "annex-i":
        return (
            []
            if _is_text(r.annex_i_legislation)
            else ["annex_i_legislation: required for annex-i"]
        )
    return (
        []
        if r.annex_i_legislation is None
        else ["annex_i_legislation: must be null unless the route is annex-i"]
    )


def _check_flag(r: Record) -> list[str]:
    return (
        [] if isinstance(r.art50_flag, bool) else ["art50_flag: must be true or false"]
    )


def _check_articles(r: Record) -> list[str]:
    if not all(_is_text(a) for a in r.articles):
        return ["articles: every citation must be non-empty text"]
    if not r.articles and r.tier != REVIEW_TIER:
        return ["articles required: at least one, except for needs-human-review"]
    return []


def _check_review_reason(r: Record) -> list[str]:
    if r.tier == REVIEW_TIER:
        if isinstance(r.review_reason, str) and r.review_reason in REVIEW_REASONS:
            return []
        return [
            f"review_reason: required for needs-human-review, one of {', '.join(REVIEW_REASONS)}"
        ]
    return (
        []
        if r.review_reason is None
        else ["review_reason: must be null unless the tier is needs-human-review"]
    )


def _check_reason(r: Record) -> list[str]:
    if not _is_text(r.reason):
        return ["reason: required, one sentence"]
    text = r.reason.strip()
    out = []
    words = len(text.split())
    if words > MAX_REASON_WORDS:
        out.append(f"reason: too long ({words} words; at most {MAX_REASON_WORDS})")
    body = _DECIMAL.sub("", _ABBREVIATIONS.sub("", text[:-1]))
    if text[-1] not in ".!?" or re.search(r"[.!?]", body):
        out.append("reason: must be exactly one sentence ending in . ! or ?")
    return out


_CHECKS = (
    _check_tier,
    _check_route,
    _check_annex_iii,
    _check_annex_i,
    _check_flag,
    _check_articles,
    _check_review_reason,
    _check_reason,
)


def validate(record: Record) -> list[str]:
    """Return every rule the record breaks; an empty list means valid."""
    return [problem for check in _CHECKS for problem in check(record)]


# ---------- reading a model's answer (ADR-005) ----------


class _DuplicateKey(ValueError):
    pass


def _reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
    data = dict(pairs)
    if len(data) != len(pairs):
        raise _DuplicateKey("duplicate key")
    return data


_DECODER = json.JSONDecoder(object_pairs_hook=_reject_duplicates)


def _first_json_object(raw: str) -> dict | None:
    """Return the first `{...}` that decodes as a JSON object, or None.

    An object with a duplicate key decodes but is refused: None, not the next
    object, so a model cannot be credited for a later, different answer.
    """
    start = raw.find("{")
    while start != -1:
        try:
            obj, _ = _DECODER.raw_decode(raw, start)
        except _DuplicateKey:
            return None
        except json.JSONDecodeError:
            obj = None
        if isinstance(obj, dict):
            return obj
        start = raw.find("{", start + 1)
    return None


def parse_answer(raw: str | None) -> tuple[Record | None, ParseStatus]:
    """Read a model's raw answer as a valid record (ADR-005). Never repairs or guesses."""
    if not isinstance(raw, str) or len(raw) > MAX_RAW_CHARS:
        return None, "unreadable"
    obj = _first_json_object(raw)
    if obj is None:
        return None, "unreadable"
    try:
        record = Record.from_json(obj)
    except (KeyError, TypeError, ValueError):
        return None, "unreadable"
    if validate(record):
        return None, "unreadable"
    return record, "ok"


# ---------- the date detector (EV-8) ----------

_MONTH = (
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December"
    r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\.?"
)
_DAY = r"\d{1,2}(?:st|nd|rd|th)?"
_DATE = re.compile(
    rf"\b(?:{_DAY}\s+)?{_MONTH},?\s+\d{{4}}\b"  # 2 August 2026, August 2026
    rf"|\b{_MONTH}\s+{_DAY},?\s+\d{{4}}\b"  # August 2, 2026
    rf"|\b{_DAY}\s+(?i:{_MONTH}),?\s+\d{{4}}\b"  # 2 august 2026 (a day makes case safe)
    r"|\b\d{4}-\d{2}-\d{2}\b"  # 2026-08-02
    r"|\b\d{1,2}/\d{1,2}/\d{4}\b"  # 02/08/2026
    r"|\b\d{2}\.\d{2}\.\d{4}\b"  # 02.08.2026 (two digits each, so not "6.5.2026")
)


def contains_date(text: str) -> bool:
    """True when the text states a calendar date or a month and year.

    A bare month and year needs a capital ("May 2026"), so "may 2026" in
    running prose is not a date; with a day in front, any case counts. Bare years and regulation numbers such as 2024/1689 are not dates.
    """
    return bool(_DATE.search(text))
