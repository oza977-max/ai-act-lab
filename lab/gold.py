"""The gold set (GS-1 to GS-6, LS-7): review sheets, checks and the build.

Claude drafts each batch of cases into `data/gold/drafts/batch-NN.jsonl`;
`sheet` turns a draft file into a review sheet the owner opens in Numbers;
`check` validates the filled sheet and never edits it; `build` turns all checked
sheets into `data/gold/gold-v{N}.jsonl` and its metadata.

    python -m lab.gold sheet --drafts data/gold/drafts/batch-01.jsonl --out data/gold/review/batch-01.csv
    python -m lab.gold check data/gold/review/batch-01.csv
    python -m lab.gold build
"""

from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from lab.articles import is_valid
from lab.prompt import PromptError, description_problems, guideline_version
from lab.records import HIGH_RISK, TAGS, Record, validate

ROOT = Path(__file__).resolve().parent.parent
GOLD_DIR = ROOT / "data" / "gold"
GUIDELINE_PATH = ROOT / "docs" / "guideline" / "labelling-guideline.md"

# Sheet column part -> record field.
FIELDS = {
    "tier": "tier",
    "route": "route",
    "area": "annex_iii_area",
    "point": "annex_iii_point",
    "legislation": "annex_i_legislation",
    "art50": "art50_flag",
    "articles": "articles",
    "review_reason": "review_reason",
    "reason": "reason",
}
COLUMNS = (
    "id",
    "description",
    "tags",
    *(f"proposed_{k}" for k in FIELDS),
    "decision",
    *(f"final_{k}" for k in FIELDS),
    "owner_note",
    "guideline_version",
)
DECISIONS = ("accept", "change", "doubt")
MIN_WORDS, MAX_WORDS = 60, 200
SPREAD = {  # GS-1
    "prohibited": 10,
    "high-risk annex-iii": 30,
    "high-risk annex-i": 5,
    "transparency-only": 20,
    "minimal": 20,
    "needs-human-review": 10,
    "out-of-scope": 5,
}
AREA_MIN = 3  # GS-3
TAG_QUOTAS = {"boundary": 15, "art6-3": 5, "hidden-instruction": 5}  # GS-4
DRAFT_KEYS = {"id", "description", "tags", "draft", "guideline_version"}
# Cells a spreadsheet would run as a formula (spec), plus tab and carriage return (OWASP).
FORMULA_START = ("=", "+", "-", "@", "\t", "\r")
ENUM_PARTS = ("tier", "route", "review_reason", "art50")
_AREA = re.compile(r"[0-9]{1,2}(?:\.0+)?")
_ID = re.compile(
    r"GC-[0-9]{3}"
)  # used with fullmatch: ASCII digits, no trailing newline
_GOLD_FILE = re.compile(r"^gold-v(\d+)\.jsonl$")


class GoldError(Exception):
    """A draft file, sheet or gold build cannot be used."""


# --- cells ---------------------------------------------------------------------


def _escape(cell: str) -> str:
    """Stop a spreadsheet running a cell Claude wrote as a formula."""
    if cell.startswith(FORMULA_START) or (
        cell.startswith("'") and cell[1:2] in FORMULA_START
    ):
        return "'" + cell
    return cell


def _unescape(cell: str) -> str:
    """Undo `_escape`: drop the one apostrophe it added."""
    escaped = cell[1:2] in FORMULA_START or (
        cell[1:2] == "'" and cell[2:3] in FORMULA_START
    )
    return cell[1:] if cell.startswith("'") and escaped else cell


def _split(cell: str) -> list[str]:
    return [part.strip() for part in cell.split(";") if part.strip()]


def normalise_text(text: str) -> str:
    """Text as compared with the draft: Unicode NFC, any line endings, spacing collapsed."""
    return " ".join(unicodedata.normalize("NFC", text).split())


def record_to_cells(record: dict) -> dict[str, str]:
    """A record as sheet cells: empty for none, `true`/`false`, lists joined by `; `."""
    cells = {}
    for part, field in FIELDS.items():
        value = record.get(field)
        if value is None:
            cells[part] = ""
        elif isinstance(value, bool):
            cells[part] = "true" if value else "false"
        elif isinstance(value, list):
            cells[part] = "; ".join(value)
        else:
            cells[part] = str(value)
    return cells


def record_problems(data: dict) -> list[str]:
    """Why a record dict is not a valid answer record citing real provisions."""
    try:
        record = Record.from_json(data)
    except (KeyError, TypeError, ValueError) as exc:
        return [str(exc)]
    problems = validate(record)
    problems += [
        f"{a!r} is not a provision of the Act"
        for a in record.articles
        if not is_valid(a)
    ]
    return problems


def cells_to_record(row: dict[str, str], prefix: str) -> tuple[dict | None, list[str]]:
    """(record, problems) from the `proposed_` or `final_` columns of one row."""
    data: dict = {}
    problems = []
    for part, field in FIELDS.items():
        cell = row[f"{prefix}{part}"].strip()
        if field == "articles":
            data[field] = _split(cell)
        elif field == "art50_flag":
            if cell not in ("true", "false"):
                problems.append(f"{prefix}art50 must be true or false")
            data[field] = cell == "true"
        elif field == "annex_iii_area":
            if cell and not _AREA.fullmatch(cell):
                problems.append(f"{prefix}area must be a whole number from 1 to 8")
            data[field] = int(float(cell)) if _AREA.fullmatch(cell) else None
        else:
            data[field] = cell or None
    if problems:
        return None, problems
    issues = record_problems(data)
    return (None, [f"{prefix} columns: {p}" for p in issues]) if issues else (data, [])


# --- files ---------------------------------------------------------------------


def _draft_problems(case: dict) -> list[str]:
    problems = []
    if not isinstance(case["description"], str):
        return ["the description is not text"]
    words = len(case["description"].split())
    if not MIN_WORDS <= words <= MAX_WORDS:
        problems.append(
            f"the description has {words} words; it needs {MIN_WORDS} to {MAX_WORDS}"
        )
    problems += [
        f"the description {p}" for p in description_problems(case["description"])
    ]
    tags = case["tags"]
    if not isinstance(tags, list) or not all(
        isinstance(t, str) and t in TAGS for t in tags
    ):
        problems.append(f"tags must be a list drawn from {list(TAGS)}")
    draft = case["draft"]
    if not isinstance(draft, dict):
        return [*problems, "the draft record is not an object"]
    problems += [f"draft record: {p}" for p in record_problems(draft)]
    if any(";" in a for a in draft.get("articles") or [] if isinstance(a, str)):
        problems.append(
            "draft record: an article contains ';', which the sheet uses between articles"
        )
    if not isinstance(case["guideline_version"], str):
        problems.append("guideline_version is not text")
    if not problems:
        # What the owner will see must read back as exactly this draft, or they could never pass check.
        cells = {
            "description": case["description"],
            **{f"proposed_{k}": v for k, v in record_to_cells(draft).items()},
        }
        if any(_unescape(_escape(v)) != v for v in cells.values()):
            problems.append("a cell would not survive the formula-escape round trip")
        elif (
            cells_to_record({k: v.strip() for k, v in cells.items()}, "proposed_")[0]
            != draft
        ):
            problems.append(
                "the draft record does not read back from the sheet unchanged (stray spaces or ';' in a field?)"
            )
    return problems


def read_drafts(path: Path) -> dict[str, dict]:
    """Claude's draft file: id -> draft case, every case checked before the owner sees it."""
    if not path.is_file():
        raise GoldError(
            f"no draft file {path}; a sheet must be named batch-NN.csv to match batch-NN.jsonl"
        )
    drafts: dict[str, dict] = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            raise GoldError(f"{path} line {n}: not JSON ({exc.msg})") from exc
        if not isinstance(case, dict) or set(case) != DRAFT_KEYS:
            raise GoldError(
                f"{path} line {n}: a draft needs exactly {sorted(DRAFT_KEYS)}"
            )
        if not _ID.fullmatch(str(case["id"])) or case["id"] in drafts:
            raise GoldError(f"{path} line {n}: bad or repeated id {case['id']!r}")
        if problems := _draft_problems(case):
            raise GoldError(f"{path} line {n} ({case['id']}): " + "; ".join(problems))
        drafts[case["id"]] = case
    return drafts


def write_sheet(drafts_path: Path, out_path: Path) -> int:
    """Write the review sheet for one batch; refuse to overwrite the owner's work."""
    if out_path.exists():
        raise GoldError(f"{out_path} already exists; it may hold the owner's decisions")
    drafts = read_drafts(drafts_path)
    rows = []
    for case in drafts.values():
        row = dict.fromkeys(COLUMNS, "")
        row.update(
            id=case["id"], description=case["description"], tags="; ".join(case["tags"])
        )
        row.update(
            {f"proposed_{k}": v for k, v in record_to_cells(case["draft"]).items()}
        )
        row["guideline_version"] = case["guideline_version"]
        rows.append({k: _escape(v) for k, v in row.items()})
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def _normalise_row(row: dict[str, str]) -> dict[str, str]:
    """One sheet row as the checks read it: formula prefixes removed, ids and choices tidied."""
    row = {k: _unescape(v) for k, v in row.items()}
    row["id"] = row["id"].strip()
    row["decision"] = row["decision"].strip().lower()
    for prefix in ("proposed_", "final_"):
        for part in ENUM_PARTS:
            row[f"{prefix}{part}"] = row[f"{prefix}{part}"].strip().lower()
    return row


def read_sheet(path: Path) -> list[dict[str, str]]:
    """The owner's sheet as rows; the columns must be exactly the review columns."""
    if not path.is_file():
        raise GoldError(f"no sheet {path}")
    try:
        with path.open(encoding="utf-8-sig", newline="") as f:  # a BOM is accepted
            reader = csv.reader(f)
            header = next(reader, [])
            raw_rows = list(reader)
    except UnicodeDecodeError as exc:
        raise GoldError(
            f"{path} is not UTF-8 text: export it again as 'CSV UTF-8'"
        ) from exc
    except csv.Error as exc:
        raise GoldError(f"{path} cannot be read as CSV: {exc}") from exc
    # Spreadsheets may add empty columns on the right and empty rows at the bottom.
    while (
        header
        and header[-1] == ""
        and all(len(r) < len(header) or r[len(header) - 1] == "" for r in raw_rows)
    ):
        header = header[:-1]
    if tuple(header) != COLUMNS:
        missing = [c for c in COLUMNS if c not in header]
        extra = [c for c in header if c not in COLUMNS]
        raise GoldError(
            f"{path}: the columns are not the review-sheet columns"
            + (f"; missing {missing}" if missing else "")
            + (f"; unexpected {extra}" if extra else "")
            + ("" if missing or extra else "; they are in a different order")
        )
    rows = []
    for n, cells in enumerate(raw_rows, start=2):
        if not any(c.strip() for c in cells):
            continue
        cells = (
            cells[: len(COLUMNS)]
            if all(c == "" for c in cells[len(COLUMNS) :])
            else cells
        )
        if len(cells) < len(COLUMNS):  # some exports drop empty cells at the end
            cells = cells + [""] * (len(COLUMNS) - len(cells))
        if len(cells) != len(COLUMNS):
            raise GoldError(
                f"{path} row {n}: {len(cells)} cells; expected {len(COLUMNS)}"
            )
        rows.append(_normalise_row(dict(zip(COLUMNS, cells, strict=True))))
    return rows


# --- check -----------------------------------------------------------------------


def check_rows(
    rows: list[dict[str, str]], drafts: dict[str, dict], version: str
) -> list[str]:
    """Every problem in a filled sheet, as 'GC-001: message' lines."""
    problems = []
    seen = set()
    for row in rows:
        case_id = row["id"]

        def flag(message, case_id=case_id):
            problems.append(f"{case_id or '(no id)'}: {message}")

        if not _ID.fullmatch(case_id):
            flag("the id must look like GC-001")
        if case_id in seen:
            flag("the id appears twice")
        seen.add(case_id)
        description = row["description"]
        words = len(description.split())
        if not MIN_WORDS <= words <= MAX_WORDS:
            flag(
                f"the description has {words} words; it needs {MIN_WORDS} to {MAX_WORDS}"
            )
        for p in description_problems(description):
            flag(f"the description {p}")
        for tag in _split(row["tags"]):
            if tag not in TAGS:
                flag(f"unknown tag {tag!r}")
        if row["guideline_version"].strip() != version:
            flag(
                f"guideline version {row['guideline_version']!r} is not the guideline's {version}"
            )
        draft = drafts.get(case_id)
        proposed = None
        if draft is None:
            flag("no draft has this id")
        else:
            if normalise_text(description) != normalise_text(draft["description"]):
                flag(
                    "the description differs from the draft; the spreadsheet may have altered it"
                )
            if _split(row["tags"]) != draft["tags"]:
                flag("the tags differ from the draft")
            proposed, issues = cells_to_record(row, "proposed_")
            if issues or proposed != draft["draft"]:
                flag(
                    "the proposed columns differ from the draft; leave them as they are and write changes in the final columns"
                )
        decision = row["decision"]
        finals_filled = any(row[f"final_{k}"].strip() for k in FIELDS)
        if not decision:
            flag("no decision: write accept, change or doubt")
        elif decision not in DECISIONS:
            flag(f"decision {decision!r} must be accept, change or doubt")
        elif decision == "change":
            final, issues = cells_to_record(row, "final_")
            for p in issues:
                flag(p)
            if final is not None and draft is not None and final == draft["draft"]:
                flag(
                    "the final columns equal the draft; write accept instead of change"
                )
        elif finals_filled:
            flag(
                f"the final columns are filled but the decision is {decision}; write change, or clear them"
            )
    for case_id in sorted(set(drafts) - seen):
        problems.append(f"{case_id}: in the draft file but missing from the sheet")
    return problems


def _version(guideline: Path) -> str:
    try:
        return guideline_version(guideline.read_text(encoding="utf-8"))
    except PromptError as exc:
        raise GoldError(f"{guideline}: {exc}") from exc


def check_sheet(
    sheet: Path, drafts_path: Path, guideline: Path = GUIDELINE_PATH
) -> tuple[list[str], Counter]:
    rows = read_sheet(sheet)
    problems = check_rows(rows, read_drafts(drafts_path), _version(guideline))
    return problems, Counter(r["decision"] or "none" for r in rows)


# --- build -----------------------------------------------------------------------


def _label(record: dict) -> str:
    return (
        f"{record['tier']} {record['route']}"
        if record["tier"] == HIGH_RISK
        else record["tier"]
    )


def _quota_problems(cases: list[dict]) -> list[str]:
    problems = []
    counts = Counter(_label(c["gold"]) for c in cases)
    for label, want in SPREAD.items():
        if counts[label] != want:
            problems.append(f"GS-1: {label} has {counts[label]} cases; it needs {want}")
    areas = Counter(
        c["gold"]["annex_iii_area"] for c in cases if c["gold"]["route"] == "annex-iii"
    )
    for area in range(1, 9):
        if areas[area] < AREA_MIN:
            problems.append(
                f"GS-3: Annex III area {area} has {areas[area]} cases; it needs {AREA_MIN}"
            )
    tags = Counter(t for c in cases for t in c["tags"])
    for tag, want in TAG_QUOTAS.items():
        if tags[tag] < want:
            problems.append(f"GS-4: {tags[tag]} cases tagged {tag}; it needs {want}")
    return problems


def assemble(
    review_dir: Path, drafts_dir: Path, guideline: Path
) -> tuple[list[dict], str]:
    """All checked sheets as gold cases, or GoldError listing every reason not to build.

    Sheet-level problems are reported first; the quotas are checked once the sheets are clean.
    """
    sheets = sorted(review_dir.glob("batch-*.csv"))
    if not sheets:
        raise GoldError(f"no review sheets named batch-NN.csv in {review_dir}")
    version = _version(guideline)
    problems, cases, doubts = [], [], []
    for drafts_file in sorted(drafts_dir.glob("batch-*.jsonl")):
        if not (review_dir / f"{drafts_file.stem}.csv").is_file():
            problems.append(
                f"{drafts_file.name} has no review sheet {drafts_file.stem}.csv"
            )
    for sheet in sheets:
        drafts = read_drafts(drafts_dir / f"{sheet.stem}.jsonl")
        rows = read_sheet(sheet)
        problems += [f"{sheet.name} {p}" for p in check_rows(rows, drafts, version)]
        for row in rows:
            decision, draft = row["decision"], drafts.get(row["id"])
            if decision == "doubt":
                doubts.append(row["id"])
            if decision not in ("accept", "change") or draft is None:
                continue
            gold = (
                draft["draft"]
                if decision == "accept"
                else cells_to_record(row, "final_")[0]
            )
            cases.append(
                {
                    "id": row["id"],
                    "description": draft["description"],
                    "gold": gold,
                    "draft": draft["draft"],
                    "tags": draft["tags"],
                    "guideline_version": version,
                    "owner_decision": decision,
                    "never_train": True,
                }
            )
    if doubts:
        problems.append(
            f"{len(doubts)} case(s) still marked doubt: {', '.join(doubts)}"
        )
    ids = [c["id"] for c in cases]
    problems += [
        f"{i}: appears in more than one sheet" for i, n in Counter(ids).items() if n > 1
    ]
    if not problems:
        problems = _quota_problems(cases)
    if problems:
        raise GoldError("the gold set cannot be built:\n" + "\n".join(problems))
    return sorted(cases, key=lambda c: c["id"]), version


def _write(target: Path, content: str) -> None:
    partial = target.with_suffix(target.suffix + ".partial")
    try:
        partial.write_text(content, encoding="utf-8")
        os.replace(partial, target)
    finally:
        partial.unlink(missing_ok=True)


def build(
    review_dir: Path = GOLD_DIR / "review",
    drafts_dir: Path = GOLD_DIR / "drafts",
    out_dir: Path = GOLD_DIR,
    guideline: Path = GUIDELINE_PATH,
    today: datetime.date | None = None,
) -> tuple[Path, dict, bool]:
    """Write the next gold version if the cases changed; return (path, meta, written)."""
    cases, version = assemble(review_dir, drafts_dir, guideline)
    text = "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cases)
    existing = {}
    if out_dir.exists():
        existing = {
            int(m.group(1)): p
            for p in out_dir.iterdir()
            if (m := _GOLD_FILE.match(p.name))
        }
    if existing:
        latest = existing[max(existing)]
        meta_path = latest.with_name(latest.stem + ".meta.json")
        if latest.read_text(encoding="utf-8") == text and meta_path.is_file():
            return latest, json.loads(meta_path.read_text(encoding="utf-8")), False
    n = max(existing, default=0) + 1
    changed = [c["id"] for c in cases if c["owner_decision"] == "change"]
    counts = Counter(_label(c["gold"]) for c in cases)
    meta = {
        "gold_version": f"v{n}",
        "build_date": (today or datetime.date.today()).isoformat(),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "guideline_version": version,
        "cases": len(cases),
        "counts": {label: counts[label] for label in SPREAD},
        "share_changed": round(len(changed) / len(cases), 4),
        "changed_ids": changed,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"gold-v{n}.jsonl"
    # Metadata first: a gold file never exists without its fingerprint.
    _write(out_dir / f"gold-v{n}.meta.json", json.dumps(meta, indent=2) + "\n")
    _write(path, text)
    return path, meta, True


# --- command line ----------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m lab.gold", description="Review sheets and the gold set."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("sheet", help="write a review sheet from a draft file")
    s.add_argument("--drafts", type=Path, required=True)
    s.add_argument("--out", type=Path, required=True)
    c = sub.add_parser("check", help="check a filled review sheet (never edits it)")
    c.add_argument("sheet", type=Path)
    c.add_argument(
        "--drafts", type=Path, help="default: data/gold/drafts/<sheet name>.jsonl"
    )
    c.add_argument("--guideline", type=Path, default=GUIDELINE_PATH)
    b = sub.add_parser("build", help="build the gold set from all checked sheets")
    b.add_argument("--review-dir", type=Path, default=GOLD_DIR / "review")
    b.add_argument("--drafts-dir", type=Path, default=GOLD_DIR / "drafts")
    b.add_argument("--out", type=Path, default=GOLD_DIR)
    b.add_argument("--guideline", type=Path, default=GUIDELINE_PATH)
    b.add_argument("--today", type=datetime.date.fromisoformat, default=None)
    args = parser.parse_args(argv)
    try:
        if args.command == "sheet":
            n = write_sheet(args.drafts, args.out)
            print(f"wrote {args.out}: {n} cases to review")
            return 0
        if args.command == "check":
            drafts = args.drafts or GOLD_DIR / "drafts" / f"{args.sheet.stem}.jsonl"
            problems, decisions = check_sheet(args.sheet, drafts, args.guideline)
            for p in problems:
                print(p)
            total = sum(decisions.values())
            print(
                f"{args.sheet.name}: {total} cases; accept {decisions['accept']}, change "
                f"{decisions['change']}, doubt {decisions['doubt']}; {len(problems)} problem(s)"
            )
            return 1 if problems else 0
        path, meta, written = build(
            args.review_dir, args.drafts_dir, args.out, args.guideline, args.today
        )
        changed = len(meta["changed_ids"])
        verb = "wrote" if written else "unchanged:"
        print(
            f"{verb} {path.name}: {meta['cases']} cases, guideline {meta['guideline_version']}; "
            f"the owner changed {changed} of {meta['cases']} drafts ({meta['share_changed']:.0%})"
        )
        return 0
    except (GoldError, OSError, ValueError) as exc:
        print(f"gold {args.command} refused: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
