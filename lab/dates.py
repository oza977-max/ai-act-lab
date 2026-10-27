"""The dates-and-duties table (DT-1 to DT-5): dates live here, never in the model.

`lookup(tier, route, art50, today)` returns the entries for one answer record:
those matching tier, route and flag exactly, plus those whose flag is `any`.
The table is checked strictly when loaded, every match must be verified, and the
table is refused until the owner has approved it.

    python -m lab.dates lookup --tier high-risk --route annex-iii --art50 false
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path

from lab.records import HIGH_RISK, ROUTES, TIERS

ROOT = Path(__file__).resolve().parent.parent
TABLE_PATH = ROOT / "data" / "dates" / "dates-table.toml"
STALE_AFTER_DAYS = 90
ROUTE_VALUES = (*ROUTES, "none")
FLAG_VALUES = ("true", "false", "any")

_HEADER_KEYS = {"version", "approved_by", "approved_on", "changes", "entry"}
_ENTRY_KEYS = {
    "tier", "route", "art50", "duties", "source_url", "last_checked", "checked_by",
    "verified", "plan_value", "discrepancy_note", "note",
}  # fmt: skip
_DUTY_KEYS = {"article", "title", "applies_from"}
_CHANGE_KEYS = {"version", "date", "change", "reason"}


class DatesError(Exception):
    """The table file is malformed."""


class NotApprovedError(DatesError):
    """The owner has not approved the table yet (DT-5)."""


class NoEntryError(DatesError):
    """No entry matches the requested tier, route and flag."""


class UnverifiedEntryError(DatesError):
    """A matching entry has not been verified against the Official Journal (DT-2)."""


@dataclass(frozen=True)
class Duty:
    article: str
    title: str
    applies_from: datetime.date


@dataclass(frozen=True)
class Entry:
    tier: str
    route: str
    art50: str
    duties: tuple[Duty, ...]
    source_url: str
    last_checked: datetime.date
    checked_by: str
    verified: bool
    plan_value: str
    discrepancy_note: str
    note: str
    stale: bool = False

    def to_json(self) -> dict:
        data = asdict(self)
        data["last_checked"] = self.last_checked.isoformat()
        data["duties"] = [
            {**asdict(d), "applies_from": d.applies_from.isoformat()}
            for d in self.duties
        ]
        return data


def _need(cond: bool, message: str) -> None:
    if not cond:
        raise DatesError(message)


def _entry(raw: dict, index: int) -> Entry:
    where = f"entry {index + 1}"
    _need(isinstance(raw, dict), f"{where} is not a table")
    _need(
        set(raw) == _ENTRY_KEYS,
        f"{where} has fields {sorted(set(raw) ^ _ENTRY_KEYS)} wrong",
    )
    _need(raw["tier"] in TIERS, f"{where}: unknown tier {raw['tier']!r}")
    _need(raw["route"] in ROUTE_VALUES, f"{where}: unknown route {raw['route']!r}")
    _need(raw["art50"] in FLAG_VALUES, f"{where}: art50 must be one of {FLAG_VALUES}")
    _need(isinstance(raw["verified"], bool), f"{where}: verified must be true or false")
    _need(
        type(raw["last_checked"]) is datetime.date,
        f"{where}: last_checked must be a date",
    )
    _need(
        isinstance(raw["source_url"], str)
        and raw["source_url"].startswith("https://eur-lex.europa.eu/"),
        f"{where}: source_url must be a EUR-Lex link",
    )
    _need(
        (raw["tier"] == HIGH_RISK) == (raw["route"] != "none"),
        f"{where}: only high-risk entries have an Annex route",
    )
    for key in ("checked_by", "note"):
        _need(
            isinstance(raw[key], str) and raw[key].strip() != "",
            f"{where}: {key} is empty",
        )
    for key in ("plan_value", "discrepancy_note"):
        _need(isinstance(raw[key], str), f"{where}: {key} must be text")
    _need(isinstance(raw["duties"], list), f"{where}: duties must be a list")
    duties = []
    for d in raw["duties"]:
        _need(
            isinstance(d, dict) and set(d) == _DUTY_KEYS,
            f"{where}: a duty needs exactly {sorted(_DUTY_KEYS)}",
        )
        _need(
            all(isinstance(d[k], str) and d[k].strip() for k in ("article", "title")),
            f"{where}: a duty's article and title must be non-empty text",
        )
        _need(
            type(d["applies_from"]) is datetime.date,
            f"{where}: {d['article']} applies_from must be a date",
        )
        duties.append(Duty(d["article"], d["title"], d["applies_from"]))
    # DT-2: a plan value either matches one of the verified dates or the gap is recorded.
    if raw["plan_value"]:
        listed = {d.applies_from.isoformat() for d in duties}
        _need(
            raw["plan_value"] in listed or raw["discrepancy_note"].strip() != "",
            f"{where}: plan value {raw['plan_value']} matches no date and has no discrepancy note",
        )
    return Entry(
        tier=raw["tier"],
        route=raw["route"],
        art50=raw["art50"],
        duties=tuple(duties),
        source_url=raw["source_url"],
        last_checked=raw["last_checked"],
        checked_by=raw["checked_by"],
        verified=raw["verified"],
        plan_value=raw["plan_value"],
        discrepancy_note=raw["discrepancy_note"],
        note=raw["note"],
    )


def load_table(path: Path = TABLE_PATH) -> tuple[dict, list[Entry]]:
    """(header, entries) from the table file, checked strictly."""
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise DatesError(f"the table is not valid UTF-8 TOML: {exc}") from exc
    _need(
        set(raw) == _HEADER_KEYS,
        f"the table header has fields {sorted(set(raw) ^ _HEADER_KEYS)} wrong",
    )
    _need(
        isinstance(raw["changes"], list) and raw["changes"] != [],
        "the table needs a change log",
    )
    for change in raw["changes"]:
        _need(
            isinstance(change, dict) and set(change) == _CHANGE_KEYS,
            f"each change needs exactly {sorted(_CHANGE_KEYS)}",
        )
        _need(type(change["date"]) is datetime.date, "each change needs a date")
    _need(
        raw["version"] == raw["changes"][-1]["version"],
        "the table version must match the last change-log entry",
    )
    _need(
        raw["approved_on"] == "" or type(raw["approved_on"]) is datetime.date,
        "approved_on must be empty or a date",
    )
    dates = [c["date"] for c in raw["changes"]]
    _need(dates == sorted(dates), "the change log must be in date order")
    _need(isinstance(raw["entry"], list), "entries must be a list of [[entry]] tables")
    entries = [_entry(e, i) for i, e in enumerate(raw["entry"])]
    keys = [(e.tier, e.route, e.art50) for e in entries]
    _need(
        len(keys) == len(set(keys)), "two entries share the same tier, route and flag"
    )
    header = {k: raw[k] for k in ("version", "approved_by", "approved_on", "changes")}
    return header, entries


def lookup(
    tier: str,
    route: str,
    art50: bool,
    today: datetime.date | None = None,
    path: Path = TABLE_PATH,
) -> list[Entry]:
    """Entries for one answer: exact matches plus `art50 = any`, in table order."""
    header, entries = load_table(path)
    today = today or datetime.date.today()
    if not (header["approved_by"] and header["approved_on"]):
        raise NotApprovedError("the dates table is not approved by the owner yet")
    if header["approved_on"] < header["changes"][-1]["date"]:
        # Approval covers the table as it stood; a later change needs a new approval.
        raise NotApprovedError(
            "the table changed after it was approved; it needs approval again"
        )
    if header["approved_on"] > today:
        raise DatesError(f"the approval is dated after {today}")
    flag = "true" if art50 else "false"
    found = [
        e
        for e in entries
        if e.tier == tier and e.route == route and e.art50 in (flag, "any")
    ]
    if not found:
        raise NoEntryError(f"no entry for tier {tier!r}, route {route!r}, art50 {flag}")
    for e in found:
        if not e.verified:
            raise UnverifiedEntryError(
                f"entry {e.tier}/{e.route}/{e.art50} is not verified"
            )
    articles = [d.article for e in found for d in e.duties]
    if len(articles) != len(set(articles)):
        raise DatesError("matching entries list the same article twice")
    for e in found:
        if e.last_checked > today:
            raise DatesError(
                f"entry {e.tier}/{e.route}/{e.art50} is dated after {today}"
            )
    stale_before = today - datetime.timedelta(days=STALE_AFTER_DAYS)
    return [
        Entry(**{**e.__dict__, "stale": e.last_checked < stale_before}) for e in found
    ]


def _render(entries: list[Entry]) -> str:
    lines = []
    for e in entries:
        lines.append(f"{e.tier} / {e.route} / Article 50 flag: {e.art50}")
        lines.extend(f"  {d.applies_from}  {d.article}  {d.title}" for d in e.duties)
        lines.append(f"  Note: {e.note}")
        flag = "  STALE: check again" if e.stale else ""
        lines.append(
            f"  Source: {e.source_url} (checked {e.last_checked} by {e.checked_by}){flag}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m lab.dates", description="Look up AI Act dates and duties."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    q = sub.add_parser("lookup", help="dates and duties for one answer record")
    q.add_argument("--tier", required=True, choices=TIERS)
    q.add_argument("--route", required=True, choices=ROUTE_VALUES)
    q.add_argument("--art50", required=True, choices=("true", "false"))
    q.add_argument("--today", type=datetime.date.fromisoformat, default=None)
    q.add_argument("--table", type=Path, default=TABLE_PATH)
    q.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = parser.parse_args(argv)
    try:
        entries = lookup(
            args.tier, args.route, args.art50 == "true", args.today, args.table
        )
    except (DatesError, OSError) as exc:
        print(f"lookup refused: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps([e.to_json() for e in entries], indent=2)
        if args.json
        else _render(entries)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
