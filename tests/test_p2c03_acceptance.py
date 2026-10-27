"""P2-C03 acceptance: the dates-and-duties table and its lookup."""

import json
import re
import subprocess
import sys
import tomllib

import pytest
from conftest import ROOT

TABLE = ROOT / "data" / "dates" / "dates-table.toml"


def lookup(*args, table=TABLE):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "lab.dates",
            "lookup",
            "--table",
            str(table),
            "--json",
            *args,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def approved(tmp_path):
    """A copy of the table marked approved, for lookups before the owner signs."""
    text = TABLE.read_text(encoding="utf-8")
    text = re.sub(
        r'^approved_by = ".*"$',
        'approved_by = "test owner"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r'^approved_on = ".*"$',
        "approved_on = 2026-10-27",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    path = tmp_path / "dates-table.toml"
    path.write_text(text, encoding="utf-8")
    return path


def test_tc_dt_1_01_high_risk_annex_iii_dates_and_duties(approved):
    result = lookup(
        "--tier",
        "high-risk",
        "--route",
        "annex-iii",
        "--art50",
        "false",
        "--today",
        "2026-10-27",
        table=approved,
    )
    assert result.returncode == 0, result.stderr
    entries = json.loads(result.stdout)
    duties = [d for e in entries for d in e["duties"]]
    risk = [d for d in duties if d["article"] == "Art. 9"]
    assert risk and risk[0]["title"] == "Risk management system"
    assert risk[0]["applies_from"] == "2027-12-02"
    assert all(
        e["source_url"].startswith("https://eur-lex.europa.eu/") for e in entries
    )
    assert all(
        len(d["title"].split()) <= 12 for d in duties
    )  # titles, not obligation text
    assert not any(d["article"].startswith("Art. 50") for d in duties)  # flag is false


def test_tc_dt_1_02_needs_human_review_is_explicit(approved):
    result = lookup(
        "--tier",
        "needs-human-review",
        "--route",
        "none",
        "--art50",
        "false",
        table=approved,
    )
    assert result.returncode == 0, result.stderr
    entries = json.loads(result.stdout)
    assert entries and entries[0]["duties"] == []
    assert (
        "No AI Act tier duties" in entries[0]["note"] and "person" in entries[0]["note"]
    )


def test_tc_dt_3_01_same_lookup_twice_is_identical(approved):
    args = (
        "--tier",
        "high-risk",
        "--route",
        "annex-i",
        "--art50",
        "true",
        "--today",
        "2026-10-27",
    )
    first, second = lookup(*args, table=approved), lookup(*args, table=approved)
    assert first.returncode == 0 and first.stdout == second.stdout
    duties = [d["article"] for e in json.loads(first.stdout) for d in e["duties"]]
    assert "Art. 9" in duties and "Art. 50(1)" in duties


def test_tc_dt_2_01_every_entry_is_sourced_and_dated():
    table = tomllib.loads(TABLE.read_text(encoding="utf-8"))
    assert len(table["entry"]) >= 9
    for entry in table["entry"]:
        assert entry["source_url"].startswith("https://eur-lex.europa.eu/eli/reg/")
        assert entry["last_checked"] and entry["checked_by"]
        assert entry["verified"] is True
        for duty in entry["duties"]:
            assert duty["article"] and duty["title"] and duty["applies_from"]


def test_tc_dt_2_02_plan_values_are_verified_or_flagged():
    table = tomllib.loads(TABLE.read_text(encoding="utf-8"))
    annex_iii = [
        e
        for e in table["entry"]
        if e["tier"] == "high-risk" and e["route"] == "annex-iii"
    ]
    assert any(e["plan_value"] == "2027-12-02" for e in annex_iii)
    for entry in table["entry"]:
        if entry["plan_value"]:
            dates = {str(d["applies_from"]) for d in entry["duties"]}
            assert entry["plan_value"] in dates or entry["discrepancy_note"], entry[
                "tier"
            ]


def test_tc_dt_4_01_ninety_days_current_ninety_one_stale(tmp_path, approved):
    # TC-DT-4-01 views the table on 2026-10-26, so date the copy's change and approval earlier.
    text = approved.read_text(encoding="utf-8").replace(
        "date = 2026-10-27", "date = 2026-07-01"
    )
    text = text.replace("approved_on = 2026-10-27", "approved_on = 2026-07-01")
    for checked, expected in (("2026-07-28", False), ("2026-07-27", True)):
        path = tmp_path / f"t-{checked}.toml"
        path.write_text(
            re.sub(
                r"last_checked = \d{4}-\d{2}-\d{2}", f"last_checked = {checked}", text
            ),
            encoding="utf-8",
        )
        result = lookup(
            "--tier",
            "minimal",
            "--route",
            "none",
            "--art50",
            "false",
            "--today",
            "2026-10-26",
            table=path,
        )
        assert result.returncode == 0, result.stderr
        assert all(e["stale"] is expected for e in json.loads(result.stdout))


def test_tc_dt_5_01_approval_and_change_log(approved):
    table = tomllib.loads(TABLE.read_text(encoding="utf-8"))
    assert table["changes"] and all(c["reason"] for c in table["changes"])
    if table["approved_on"]:  # the real table, once approved, covers its last change
        assert (
            table["approved_by"]
            and table["approved_on"] >= table["changes"][-1]["date"]
        )
    # Use before approval is refused, whatever the real table's state.
    unapproved = approved.read_text(encoding="utf-8").replace(
        "approved_on = 2026-10-27", 'approved_on = ""'
    )
    approved.write_text(unapproved, encoding="utf-8")
    result = lookup(
        "--tier", "minimal", "--route", "none", "--art50", "false", table=approved
    )
    assert result.returncode == 1 and "not approved" in result.stderr
