"""Unit tests for the dates-and-duties table (DT-1 to DT-5)."""

import datetime
import re

import pytest
from conftest import ROOT

from lab.articles import is_valid
from lab.dates import (
    DatesError,
    NoEntryError,
    NotApprovedError,
    UnverifiedEntryError,
    load_table,
    lookup,
    main,
)

TABLE = ROOT / "data" / "dates" / "dates-table.toml"
TODAY = datetime.date(2026, 10, 27)


@pytest.fixture
def approved(tmp_path):
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
    path = tmp_path / "t.toml"
    path.write_text(text, encoding="utf-8")
    return path


def variant(approved, old, new, count=1):
    text = approved.read_text(encoding="utf-8")
    assert old in text
    approved.write_text(text.replace(old, new, count), encoding="utf-8")
    return approved


# Every (tier, route, flag) that a valid answer record can carry under the guideline.
REACHABLE = [
    ("prohibited", "none", False),
    ("high-risk", "annex-iii", False),
    ("high-risk", "annex-iii", True),
    ("high-risk", "annex-i", False),
    ("high-risk", "annex-i", True),
    ("transparency-only", "none", True),
    ("minimal", "none", False),
    ("out-of-scope", "none", False),
    ("needs-human-review", "none", False),
    ("needs-human-review", "none", True),
]


@pytest.mark.parametrize("tier, route, flag", REACHABLE)
def test_every_reachable_answer_gets_an_entry(approved, tier, route, flag):
    entries = lookup(tier, route, flag, TODAY, approved)
    assert entries
    has_50 = any(d.article.startswith("Art. 50") for e in entries for d in e.duties)
    assert has_50 == (flag and tier in ("high-risk", "transparency-only"))


def test_every_cited_article_exists_in_the_amended_act():
    _, entries = load_table(TABLE)
    for e in entries:
        for d in e.duties:
            assert is_valid(d.article), d.article


def test_duty_dates_are_the_verified_ones():
    _, entries = load_table(TABLE)
    allowed = {
        datetime.date(2025, 2, 2),  # Chapters I and II
        datetime.date(2026, 8, 2),  # general date
        datetime.date(2026, 12, 2),  # new bans; Art. 111(4)
        datetime.date(2027, 12, 2),  # Annex III, Chapter III Sections 1 to 3
        datetime.date(2028, 8, 2),  # Annex I, Chapter III Sections 1 to 3
    }
    for e in entries:
        for d in e.duties:
            assert d.applies_from in allowed, (e.tier, d.article)
    by_route = {(e.tier, e.route): e for e in entries if e.art50 == "any"}
    assert {
        d.applies_from
        for d in by_route[("high-risk", "annex-iii")].duties
        if d.article == "Art. 9"
    } == {datetime.date(2027, 12, 2)}
    assert {
        d.applies_from
        for d in by_route[("high-risk", "annex-i")].duties
        if d.article == "Art. 9"
    } == {datetime.date(2028, 8, 2)}


def test_impact_assessment_is_annex_iii_only():
    _, entries = load_table(TABLE)
    for e in entries:
        if any(d.article == "Art. 27" for d in e.duties):
            assert e.route == "annex-iii"


def test_unapproved_table_is_refused(approved):
    variant(approved, "approved_on = 2026-10-27", 'approved_on = ""')
    with pytest.raises(NotApprovedError):
        lookup("minimal", "none", False, TODAY, approved)


def test_impossible_combination_raises_no_entry(approved):
    with pytest.raises(NoEntryError):
        lookup("transparency-only", "none", False, TODAY, approved)


def test_unverified_entry_is_refused(approved):
    variant(approved, "verified = true", "verified = false")
    with pytest.raises(UnverifiedEntryError, match="prohibited"):
        lookup("prohibited", "none", False, TODAY, approved)


@pytest.mark.parametrize(
    "old, new",
    [
        ('tier = "minimal"', 'tier = "limited-risk"'),
        ('route = "annex-iii"', 'route = "annex-3"'),
        ('art50 = "false"', 'art50 = "no"'),
        ("verified = true", 'verified = "yes"'),
        ("last_checked = 2026-10-27", 'last_checked = "2026-10-27"'),
        ("applies_from = 2027-12-02", 'applies_from = "soon"'),
        (
            'source_url = "https://eur-lex.europa.eu/',
            'source_url = "https://example.org/',
        ),
        ('checked_by = "Claude', 'extra_field = 1\nchecked_by = "Claude'),
        ('note = "No tier duties', 'note = "" #'),
    ],
)
def test_malformed_tables_are_refused(approved, old, new):
    variant(approved, old, new)
    with pytest.raises(DatesError):
        load_table(approved)


def test_duplicate_entries_are_refused(approved):
    text = approved.read_text(encoding="utf-8")
    block = text[
        text.index("# --- out-of-scope") : text.index("# --- needs-human-review")
    ]
    approved.write_text(text + "\n" + block, encoding="utf-8")
    with pytest.raises(DatesError, match="same tier"):
        load_table(approved)


def test_missing_change_log_is_refused(approved):
    text = approved.read_text(encoding="utf-8")
    start, end = text.index("[[changes]]"), text.index("# --- prohibited")
    approved.write_text(
        text[:start] + "changes = []\n\n" + text[end:], encoding="utf-8"
    )
    with pytest.raises(DatesError, match="change log"):
        load_table(approved)


def test_stale_boundary_through_the_api(approved):
    fresh = lookup(
        "minimal", "none", False, datetime.date(2027, 1, 25), approved
    )  # 90 days after
    old = lookup(
        "minimal", "none", False, datetime.date(2027, 1, 26), approved
    )  # 91 days after
    assert not fresh[0].stale and old[0].stale


def test_text_output_flags_stale_entries(approved, capsys):
    args = [
        "lookup",
        "--tier",
        "minimal",
        "--route",
        "none",
        "--art50",
        "false",
        "--table",
        str(approved),
    ]
    assert main([*args, "--today", "2027-02-01"]) == 0
    assert "STALE" in capsys.readouterr().out
    assert main([*args, "--today", "2026-10-27"]) == 0
    assert "STALE" not in capsys.readouterr().out


def test_cli_refuses_a_missing_table(tmp_path, capsys):
    args = ["lookup", "--tier", "minimal", "--route", "none", "--art50", "false"]
    assert main([*args, "--table", str(tmp_path / "none.toml")]) == 1
    assert "lookup refused" in capsys.readouterr().err


def test_exact_dates_per_duty():
    _, entries = load_table(TABLE)
    by = {
        (e.tier, e.route, e.art50): {d.article: d.applies_from for d in e.duties}
        for e in entries
    }
    prohibited = by[("prohibited", "none", "any")]
    assert prohibited["Art. 5(1)"] == datetime.date(2025, 2, 2)
    for point in ("Art. 5(1)(ba)", "Art. 5(1)(bb)", "Art. 5(1a)", "Art. 5(1b)"):
        assert prohibited[point] == datetime.date(2026, 12, 2), point
    for route, date in (
        ("annex-iii", datetime.date(2027, 12, 2)),
        ("annex-i", datetime.date(2028, 8, 2)),
    ):
        core = by[("high-risk", route, "any")]
        for n in range(8, 27):
            assert core[f"Art. {n}"] == date, (route, n)
    for key in (
        ("high-risk", "annex-iii", "true"),
        ("transparency-only", "none", "true"),
    ):
        assert by[key]["Art. 50(1)"] == datetime.date(2026, 8, 2)
        assert by[key]["Art. 111(4)"] == datetime.date(2026, 12, 2)


def test_ai_literacy_is_listed_for_every_lawful_ai_system_tier():
    _, entries = load_table(TABLE)
    for e in entries:
        has_4 = any(d.article == "Art. 4" for d in e.duties)
        # Once per answer: the core high-risk entries carry it, not their Article 50 add-ons.
        expected = (e.tier, e.art50) in {
            ("high-risk", "any"),
            ("transparency-only", "true"),
            ("minimal", "false"),
        }
        assert has_4 == expected, (e.tier, e.route, e.art50)


def test_high_risk_notes_say_what_is_not_listed():
    _, entries = load_table(TABLE)
    for e in entries:
        if e.tier == "high-risk" and e.art50 == "any":
            assert "Not listed" in e.note and "Articles 43 to 49" in e.note


def test_unknown_header_field_is_refused(approved):
    variant(approved, 'version = "v1"', 'version = "v1"\nowner = "x"')
    with pytest.raises(DatesError, match="header"):
        load_table(approved)


def test_version_must_match_the_change_log(approved):
    variant(approved, 'version = "v1"', 'version = "v2"')
    with pytest.raises(DatesError, match="change-log"):
        load_table(approved)


def test_a_change_after_approval_needs_new_approval(approved):
    variant(approved, "date = 2026-10-27", "date = 2026-11-03")
    with pytest.raises(NotApprovedError, match="again"):
        lookup("minimal", "none", False, datetime.date(2026, 11, 4), approved)


def test_high_risk_needs_an_annex_route(approved):
    variant(
        approved,
        'tier = "minimal"\nroute = "none"',
        'tier = "minimal"\nroute = "annex-iii"',
    )
    with pytest.raises(DatesError, match="Annex route"):
        load_table(approved)


def test_unverified_entry_elsewhere_does_not_block_a_lookup(approved):
    text = approved.read_text(encoding="utf-8")
    i = text.index('tier = "out-of-scope"')
    approved.write_text(
        text[:i] + text[i:].replace("verified = true", "verified = false", 1),
        encoding="utf-8",
    )
    assert lookup("minimal", "none", False, TODAY, approved)


def test_the_same_article_twice_in_one_answer_is_refused(approved):
    variant(approved, 'article = "Art. 50(4)"', 'article = "Art. 9"', count=2)
    with pytest.raises(DatesError, match="twice"):
        lookup("high-risk", "annex-iii", True, TODAY, approved)


def test_a_check_dated_in_the_future_is_refused(approved):
    with pytest.raises(DatesError, match="after"):
        lookup("minimal", "none", False, datetime.date(2026, 10, 1), approved)


def test_json_output_carries_stale(approved, capsys):
    import json

    args = [
        "lookup",
        "--tier",
        "minimal",
        "--route",
        "none",
        "--art50",
        "false",
        "--json",
    ]
    assert main([*args, "--table", str(approved), "--today", "2027-02-01"]) == 0
    assert json.loads(capsys.readouterr().out)[0]["stale"] is True


def test_invalid_toml_and_bad_encoding_exit_1(tmp_path, capsys):
    args = [
        "lookup",
        "--tier",
        "minimal",
        "--route",
        "none",
        "--art50",
        "false",
        "--table",
    ]
    bad = tmp_path / "bad.toml"
    bad.write_text("this is = = not toml", encoding="utf-8")
    assert main([*args, str(bad)]) == 1
    bad.write_bytes(b"\xff\xfe")
    assert main([*args, str(bad)]) == 1


@pytest.mark.parametrize(
    "old, new, match",
    [
        (
            '[[entry]]\ntier = "prohibited"',
            'entry = 5\n[[x]]\ntier = "prohibited"',
            "TOML|header|list",
        ),
        ("duties = []", "duties = 3", "duties must be a list"),
    ],
)
def test_wrong_shapes_raise_dates_error_not_a_crash(approved, old, new, match):
    variant(approved, old, new)
    with pytest.raises(DatesError, match=match):
        load_table(approved)


def test_change_log_must_be_in_date_order(approved):
    text = approved.read_text(encoding="utf-8")
    extra = (
        '[[changes]]\nversion = "v1"\ndate = 2026-10-01\nchange = "x"\nreason = "y"\n\n'
    )
    i = text.index("# --- prohibited")
    approved.write_text(text[:i] + extra + text[i:], encoding="utf-8")
    with pytest.raises(DatesError, match="date order"):
        load_table(approved)


def test_an_approval_dated_in_the_future_is_refused(approved):
    with pytest.raises(DatesError, match="approval"):
        lookup("minimal", "none", False, datetime.date(2026, 10, 26), approved)
