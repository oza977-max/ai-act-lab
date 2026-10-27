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
        {
            "id": m[1],
            "label": m[2],
            "boundary": bool(m[3]),
            "description": m[4],
            "record": json.loads(m[5]),
        }
        for m in _EXAMPLE.finditer(section(text, "Worked examples"))
    ]


def test_every_example_heading_has_its_own_record(text):
    headings = re.findall(
        r"^### Example ", section(text, "Worked examples"), re.MULTILINE
    )
    found = examples(text)
    assert len(found) == len(headings)
    assert all("### Example" not in e["description"] for e in found)


def test_tc_ls_1_01_six_labels_each_resting_on_an_article(text):
    rows = re.findall(
        r"^\| `([a-z-]+)` \| (.+?) \| (.+?) \|$",
        section(text, "The six labels"),
        re.MULTILINE,
    )
    assert [r[0] for r in rows] == list(LABELS)
    for label, definition, rests_on in rows:
        assert len(definition.split()) >= 8 and definition.endswith("."), label
        if label == REVIEW_TIER:
            assert "project label" in rests_on  # the Act has no such label
            continue
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
    ranking = [e for e in review if "ranks people" in e["description"]]
    assert ranking
    assert all(e["record"]["review_reason"] == "missing-fact" for e in ranking)
    assert all(e["record"]["art50_flag"] is False for e in ranking)


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
    assert "eur-lex.europa.eu" in rule and re.search(
        r"checked on\s+2026-\d\d-\d\d", rule
    )
    assert not re.search(
        r"(final|adopted) (Commission )?(Article 6|classification) guidelines",
        rule,
        re.IGNORECASE,
    )


def test_ls_8_sources_link_the_amended_act(text):
    sources = section(text, "Sources")
    assert "2024/1689" in sources and "2026/1744" in sources
    assert "eur-lex.europa.eu" in sources and "checked on" in sources


@pytest.mark.parametrize(
    "heading",
    [
        "The six labels",
        "Decision order",
        "Article 50 in short",
        "When the description is silent",
        "The Article 6(3) exception",
        "When to say needs-human-review",
        "The answer record",
    ],
)
def test_ls_8_every_rule_section_names_its_source(text, heading):
    rule = section(text, heading)
    assert "Source:" in rule
    assert "eur-lex.europa.eu" in rule and re.search(
        r"checked on\s+2026-\d\d-\d\d", rule
    )


def test_tc_ls_9_01_complete_example_is_a_valid_record(text):
    block = re.search(
        r"Complete example:\n\n```json\n(.*?)\n```",
        section(text, "The answer record"),
        re.DOTALL,
    )
    record = Record.from_json(json.loads(block.group(1)))
    assert validate(record) == []
    assert set(json.loads(block.group(1))) == set(FIELD_NAMES)


def test_flag_is_false_when_article_50_is_never_reached(text):
    for e in examples(text):
        if e["label"] in ("prohibited", "out-of-scope"):
            assert e["record"]["art50_flag"] is False, e["id"]
    assert "always `false`" in section(text, "Decision order")


def test_examples_follow_the_articles_rule(text):
    for e in examples(text):
        r = e["record"]
        cites_50 = any(c.startswith("Art. 50") for c in r["articles"])
        assert cites_50 == r["art50_flag"], e[
            "id"
        ]  # Article 50 cited if and only if flagged
        if r["route"] == "annex-iii":
            assert "Art. 6(2)" in r["articles"], e["id"]
            assert f"Annex III {r['annex_iii_point']}" in r["articles"], e["id"]
        if r["route"] == "annex-i":
            assert "Art. 6(1)" in r["articles"], e["id"]


def test_tc_ls_3_01_and_3_02_flag_independent_of_tier(text):
    found = examples(text)
    assert any(e["label"] == "high-risk" and e["record"]["art50_flag"] for e in found)
    assert any(e["label"] == "minimal" and not e["record"]["art50_flag"] for e in found)


def test_amended_prohibitions_and_safety_components_are_covered(text):
    order = section(text, "Decision order")
    for phrase in (
        "(ba)",
        "(bb)",
        "5(1a)",
        "5(1b)",
        "Art. 6(1a)",
        "Art. 6(1b)",
        "Art. 6(1c)",
        "Art. 2(2)",
    ):
        assert phrase in order, phrase


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
    rule = section(text, "The Article 6(3) exception")
    assert "Not clearly stated means high-risk" in rule
    assert "always high-risk" in rule and "Art. 3(52)" in rule
    assert "never on the Annex I route" in rule


def test_d_ls_2_minimal_examples_cite_consistently(text):
    for e in examples(text):
        r = e["record"]
        if r["tier"] != "minimal":
            continue
        if "Art. 6(3)" in r["articles"]:  # an Article 6(3) result
            assert any(c.startswith("Annex III ") for c in r["articles"]), e["id"]
            assert "Art. 95(1)" not in r["articles"] and len(r["articles"]) == 2, e[
                "id"
            ]
        else:
            assert r["articles"] == ["Art. 95(1)"], e["id"]
