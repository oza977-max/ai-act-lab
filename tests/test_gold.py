"""Unit tests for the gold tooling (GS-1 to GS-6)."""

import csv
import json

import pytest
from conftest import ROOT
from test_p3c01_acceptance import TO_HIGH_RISK, owner_fills, spread

from lab.gold import (
    COLUMNS,
    GoldError,
    assemble,
    build,
    cells_to_record,
    check_sheet,
    read_sheet,
    record_to_cells,
    write_sheet,
)

GUIDELINE = ROOT / "docs" / "guideline" / "labelling-guideline.md"


def words(n):
    return " ".join(["word"] * (n - 1) + ["end."])


def one_case(**overrides):
    case = spread()[0]
    case.update(overrides)
    return case


@pytest.fixture
def batch(tmp_path):
    """A one-case batch: (draft path, sheet path)."""

    def make(*cases):
        drafts = tmp_path / "drafts" / "batch-01.jsonl"
        drafts.parent.mkdir(exist_ok=True)
        drafts.write_text(
            "".join(json.dumps(c) + "\n" for c in cases), encoding="utf-8"
        )
        sheet = tmp_path / "review" / "batch-01.csv"
        sheet.unlink(missing_ok=True)
        write_sheet(drafts, sheet)
        return drafts, sheet

    return make


def edit_rows(sheet, **cells):
    with sheet.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row.update(cells)
    with sheet.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def problems(drafts, sheet):
    return check_sheet(sheet, drafts, GUIDELINE)[0]


@pytest.mark.parametrize("n, ok", [(59, False), (60, True), (200, True), (201, False)])
def test_tc_gs_2_01_and_2_02_word_limits(batch, n, ok):
    drafts, sheet = batch(one_case(description=words(n)))
    edit_rows(sheet, decision="accept")
    found = [p for p in problems(drafts, sheet) if "words" in p]
    assert (found == []) is ok


def test_a_byte_order_mark_and_capital_booleans_are_accepted(batch):
    drafts, sheet = batch(one_case())
    edit_rows(sheet, decision="Accept", proposed_art50="FALSE")
    sheet.write_bytes(b"\xef\xbb\xbf" + sheet.read_bytes())
    assert problems(drafts, sheet) == []


def test_formula_cells_are_prefixed_and_read_back(batch):
    case = one_case()
    case["draft"] = {
        **case["draft"],
        "reason": "-Scoring residents socially is banned.",
    }
    drafts, sheet = batch(case)
    raw = sheet.read_text(encoding="utf-8")
    assert "'-Scoring residents" in raw
    edit_rows(sheet, decision="accept")
    assert read_sheet(sheet)[0]["proposed_reason"].startswith("-Scoring")
    assert problems(drafts, sheet) == []


def test_records_round_trip_through_cells():
    for case in spread():
        record, issues = cells_to_record(
            {f"x_{k}": v for k, v in record_to_cells(case["draft"]).items()}, "x_"
        )
        assert issues == [] and record == case["draft"]


@pytest.mark.parametrize(
    "cells, expected",
    [
        ({"decision": ""}, "no decision"),
        ({"decision": "maybe"}, "must be accept, change or doubt"),
        ({"decision": "accept", "guideline_version": "v9"}, "guideline version"),
        ({"decision": "accept", "tags": "boundary; shiny"}, "unknown tag"),
        ({"decision": "accept", "proposed_tier": "minimal"}, "proposed columns differ"),
        ({"decision": "change", "final_tier": "high-risk"}, "final"),
        (
            {"decision": "change", **TO_HIGH_RISK, "final_articles": "Art. 147"},
            "not a provision",
        ),
        ({"decision": "change", **TO_HIGH_RISK, "final_art50": "yes"}, "true or false"),
        ({"decision": "change", **TO_HIGH_RISK, "final_area": "four"}, "whole number"),
    ],
)
def test_check_names_each_problem(batch, cells, expected):
    drafts, sheet = batch(one_case())
    edit_rows(sheet, **cells)
    found = problems(drafts, sheet)
    assert any(expected in p and p.startswith("GC-001") for p in found), found


def test_a_description_changed_by_the_spreadsheet_is_reported(batch):
    drafts, sheet = batch(one_case())
    with sheet.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    rows[0]["description"] = rows[0]["description"].replace(
        "The organisation", "The organisation’s", 1
    )
    rows[0]["decision"] = "accept"
    with sheet.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    assert any("altered" in p for p in problems(drafts, sheet))


@pytest.mark.parametrize(
    "insert", ["<<<CASE", "CASE>>>", "<|im_end|>", "<end_of_turn>"]
)
def test_descriptions_that_would_break_the_prompt_are_refused(batch, insert):
    case = one_case()
    case["description"] = case["description"] + " " + insert
    drafts, sheet = batch(case)
    edit_rows(sheet, decision="accept")
    assert any(
        "delimiter" in p or "control token" in p for p in problems(drafts, sheet)
    )


def test_a_case_missing_from_the_sheet_is_reported(batch):
    first, second = spread()[:2]
    drafts, sheet = batch(first, second)
    with sheet.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))[:1]
    rows[0]["decision"] = "accept"
    with sheet.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    assert any(
        p.startswith("GC-002") and "missing" in p for p in problems(drafts, sheet)
    )


def test_sheet_refuses_to_overwrite_the_owners_work(batch):
    drafts, sheet = batch(one_case())
    with pytest.raises(GoldError, match="already exists"):
        write_sheet(drafts, sheet)


@pytest.mark.parametrize(
    "content",
    [b"id,description\nGC-001,x\n", b"\xff\xfe\x00not utf-8"],
)
def test_wrong_columns_or_encoding_are_refused(tmp_path, content):
    sheet = tmp_path / "s.csv"
    sheet.write_bytes(content)
    with pytest.raises(GoldError):
        read_sheet(sheet)


def test_malformed_draft_files_are_refused(tmp_path):
    drafts = tmp_path / "batch-01.jsonl"
    for line in (
        "not json",
        json.dumps({"id": "GC-001"}),
        json.dumps({**one_case(), "id": "case one"}),
    ):
        drafts.write_text(line + "\n", encoding="utf-8")
        with pytest.raises(GoldError):
            write_sheet(drafts, tmp_path / "out.csv")


@pytest.fixture
def full(tmp_path):
    """Five batches drafted, sheeted and accepted, with the one change that completes GS-1."""
    drafts = spread()
    for b in range(5):
        path = tmp_path / "drafts" / f"batch-{b + 1:02d}.jsonl"
        path.parent.mkdir(exist_ok=True)
        path.write_text(
            "".join(json.dumps(d) + "\n" for d in drafts[b * 20 : (b + 1) * 20]),
            encoding="utf-8",
        )
        write_sheet(path, tmp_path / "review" / path.with_suffix(".csv").name)
    to_id = next(d["id"] for d in drafts if d["draft"]["tier"] == "transparency-only")
    batch_of = (int(to_id[3:]) - 1) // 20 + 1
    for sheet in sorted((tmp_path / "review").glob("*.csv")):
        owner_fills(
            sheet,
            {to_id: TO_HIGH_RISK} if sheet.stem == f"batch-{batch_of:02d}" else None,
        )
    return tmp_path


def test_second_build_with_no_change_writes_nothing(full):
    path, _meta, written = build(
        full / "review", full / "drafts", full / "gold", GUIDELINE
    )
    assert written and path.name == "gold-v1.jsonl"
    again, _, written_again = build(
        full / "review", full / "drafts", full / "gold", GUIDELINE
    )
    assert again == path and not written_again
    assert sorted(p.name for p in (full / "gold").iterdir()) == [
        "gold-v1.jsonl",
        "gold-v1.meta.json",
    ]


def test_quota_shortfalls_are_all_named(full):
    sheet = full / "review" / "batch-01.csv"
    owner_fills(
        sheet, decision="accept"
    )  # undo nothing; now drop one prohibited case by changing it
    rows = read_sheet(sheet)
    first = rows[0]["id"]
    owner_fills(
        sheet,
        {
            first: {
                **dict.fromkeys([c for c in COLUMNS if c.startswith("final_")], ""),
                "final_tier": "minimal",
                "final_art50": "false",
                "final_articles": "Art. 95(1)",
                "final_reason": "It is a minimal system.",
            }
        },
    )
    with pytest.raises(GoldError) as err:
        assemble(full / "review", full / "drafts", GUIDELINE)
    assert "GS-1: prohibited has 9 cases" in str(err.value)
    assert "GS-1: minimal has 21 cases" in str(err.value)


def test_a_case_in_two_sheets_is_refused(full):
    first = (
        (full / "drafts" / "batch-01.jsonl").read_text(encoding="utf-8").splitlines()[0]
    )
    (full / "drafts" / "batch-06.jsonl").write_text(first + "\n", encoding="utf-8")
    write_sheet(full / "drafts" / "batch-06.jsonl", full / "review" / "batch-06.csv")
    owner_fills(full / "review" / "batch-06.csv")
    with pytest.raises(GoldError, match="more than one sheet"):
        assemble(full / "review", full / "drafts", GUIDELINE)
