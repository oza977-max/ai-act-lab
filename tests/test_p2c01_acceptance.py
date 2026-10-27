"""P2-C01 acceptance: the labelling guideline v1 is complete, consistent and checkable."""

import json
import re

import pytest
from conftest import ROOT

from lab.articles import is_valid
from lab.records import FIELD_NAMES, REVIEW_TIER, TIERS, Record, contains_date, validate

GUIDELINE = ROOT / "docs" / "guideline" / "labelling-guideline.md"
LABELS = (*TIERS, REVIEW_TIER) if REVIEW_TIER not in TIERS else TIERS

_EXAMPLE = re.compile(
    r"^### Example (\S+) \(([a-z-]+)\)( · boundary)?\n(.*?)```json\n(.*?)\n```",
    re.MULTILINE | re.DOTALL,
)


@pytest.fixture(scope="module")
def text():
    return GUIDELINE.read_text(encoding="utf-8")


def section(text, heading):
    m = re.search(
        rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL
    )
    assert m, f"section '{heading}' missing"
    return m.group(1)


def examples(text):
    return [
        {"id": m[1], "label": m[2], "boundary": bool(m[3]), "record": json.loads(m[5])}
        for m in _EXAMPLE.finditer(section(text, "Worked examples"))
    ]


def test_tc_ls_1_01_six_labels_each_resting_on_an_article(text):
    rows = re.findall(
        r"^\| `([a-z-]+)` \| (.+?) \| (.+?) \|$",
        section(text, "The six labels"),
        re.MULTILINE,
    )
    assert [r[0] for r in rows] == list(LABELS)
    for label, definition, rests_on in rows:
        assert definition.count(".") >= 1 and rests_on.strip(), label
        assert all(is_valid(c.strip()) for c in rests_on.split(";")), rests_on
    assert len(rows) == 6  # no seventh label such as limited-risk


def test_tc_ls_5_01_decision_order_starts_with_scope(text):
    steps = re.findall(
        r"^\d+\. \*\*(.+?)\*\*", section(text, "Decision order"), re.MULTILINE
    )
    assert len(steps) == 5
    assert "AI system" in steps[0] and "scope" in steps[0]
    assert "prohibited" in steps[1].lower() and "prohibited" not in steps[0].lower()
    assert "high-risk" in steps[2].lower() and "6(3)" in steps[2]
    assert "Article 50" in steps[3] and "minimal" in steps[4].lower()


def test_tc_ls_5_02_two_examples_per_label_one_boundary(text):
    found = examples(text)
    for label in LABELS:
        mine = [e for e in found if e["label"] == label]
        assert len(mine) >= 2, label
        assert any(e["boundary"] for e in mine), label


def test_every_example_is_a_valid_record_with_real_citations(text):
    found = examples(text)
    assert found
    for e in found:
        record = Record.from_json(e["record"])
        assert validate(record) == [], e["id"]
        assert record.tier == e["label"], e["id"]
        assert all(is_valid(c) for c in record.articles), (e["id"], record.articles)
        assert not contains_date(json.dumps(e["record"])), e["id"]  # LS-10


def test_tc_ls_6_01_decidable_credit_case_is_high_risk(text):
    credit = [e for e in examples(text) if e["record"].get("annex_iii_point") == "5(b)"]
    assert credit and all(e["label"] == "high-risk" for e in credit)


def test_tc_ls_6_02_ranking_tool_without_purpose_goes_to_review(text):
    review = [e for e in examples(text) if e["label"] == REVIEW_TIER]
    assert {e["record"]["review_reason"] for e in review} >= {"missing-fact"}
    ranking = [e for e in review if "ranks people" in section(text, "Worked examples")]
    assert ranking


def test_review_rule_is_narrow_and_names_three_reasons(text):
    rule = section(text, "When to say needs-human-review")
    for reason in ("missing-fact", "conflicting-facts", "unsettled-law"):
        assert f"`{reason}`" in rule
    assert "hard but decidable" in rule.lower()


def test_tc_ls_7_01_version_and_change_log(text):
    assert re.search(r"^\*\*Version:\*\* v1\b", text, re.MULTILINE)
    log = section(text, "Change log")
    assert re.search(r"^\| v1 \|", log, re.MULTILINE)


def test_tc_ls_8_01_article_6_3_rule_names_draft_guidance(text):
    rule = section(text, "The Article 6(3) exception")
    assert "Art. 6(3)" in rule
    assert "draft Commission guidelines" in rule
    assert "eur-lex.europa.eu" in rule and re.search(r"checked on 2026-\d\d-\d\d", rule)
    assert not re.search(
        r"final (Commission )?(Article 6|classification) guidelines",
        rule,
        re.IGNORECASE,
    )


def test_ls_8_sources_link_the_amended_act(text):
    sources = section(text, "Sources")
    assert "2024/1689" in sources and "2026/1744" in sources
    assert "eur-lex.europa.eu" in sources and "checked on" in sources


def test_ls_9_record_fields_quoted_from_records(text):
    quoted = re.findall(
        r"^\| `([a-z_0-9]+)` \|", section(text, "The answer record"), re.MULTILINE
    )
    assert len(quoted) == len(set(quoted)) and set(quoted) == set(FIELD_NAMES)


def test_tc_gs_6_01_gold_set_is_never_train(text):
    gold = section(text, "The gold set")
    assert "never_train" in gold and "never used for training" in gold
    assert "data/gold/" in gold


def test_owner_decisions_are_written_down(text):
    assumptions = section(text, "When the description is silent")
    assert "used in the EU" in assumptions
    assert "profiling" in section(text, "The Article 6(3) exception")
