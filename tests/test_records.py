"""The answer record: parsing (ADR-005), rules (validate) and the date detector."""

import dataclasses
import json

import pytest

from lab.records import TIERS, Record, contains_date, parse_answer, validate

GOOD = {
    "tier": "minimal",
    "route": None,
    "annex_iii_area": None,
    "annex_iii_point": None,
    "annex_i_legislation": None,
    "art50_flag": False,
    "articles": ["Art. 95"],
    "review_reason": None,
    "reason": "It filters spam.",
}


def test_six_tiers():
    assert TIERS == (
        "prohibited",
        "high-risk",
        "transparency-only",
        "minimal",
        "out-of-scope",
        "needs-human-review",
    )


def test_plain_record_is_readable():
    record, status = parse_answer(json.dumps(GOOD))
    assert status == "ok" and record.tier == "minimal"


def test_realistic_prose_around_record_is_readable():
    raw = "Here is my answer:\n" + json.dumps(GOOD) + "\nHope that helps."
    record, status = parse_answer(raw)
    assert status == "ok" and record.tier == "minimal"


def test_realistic_fenced_code_block_is_readable():
    raw = "```json\n" + json.dumps(GOOD) + "\n```"
    assert parse_answer(raw)[1] == "ok"


def test_realistic_broken_first_brace_then_valid_record():
    raw = "Tier {not json} then " + json.dumps(GOOD)
    record, status = parse_answer(raw)
    assert status == "ok" and record.tier == "minimal"


def test_tc_ls_9_02_prose_only_is_unreadable():
    assert parse_answer("This looks high risk to me.") == (None, "unreadable")


def test_unknown_tier_is_unreadable():
    assert parse_answer(json.dumps({**GOOD, "tier": "limited-risk"})) == (
        None,
        "unreadable",
    )


def test_overlong_answer_is_unreadable():
    assert parse_answer(" " * 4001 + json.dumps(GOOD)) == (None, "unreadable")


def test_none_is_unreadable():
    assert parse_answer(None) == (None, "unreadable")


def test_non_string_raw_is_unreadable():
    assert parse_answer(5) == (None, "unreadable")
    assert parse_answer({"tier": "minimal"}) == (None, "unreadable")


def test_raw_of_exactly_4000_characters_is_read_but_4001_is_not():
    body = json.dumps(GOOD)
    assert parse_answer(body + " " * (4000 - len(body)))[1] == "ok"
    assert parse_answer(body + " " * (4001 - len(body)))[1] == "unreadable"


# ---------- P1-C03: record rules ----------

HIGH_RISK_ANNEX_III = {
    "tier": "high-risk",
    "route": "annex-iii",
    "annex_iii_area": 4,
    "annex_iii_point": "4(a)",
    "annex_i_legislation": None,
    "art50_flag": True,
    "articles": ["Art. 6(2)", "Annex III 4(a)", "Art. 50(1)"],
    "review_reason": None,
    "reason": "The system screens job applicants, an Annex III employment use, and it talks to them directly.",
}

HIGH_RISK_ANNEX_I = {
    **HIGH_RISK_ANNEX_III,
    "route": "annex-i",
    "annex_iii_area": None,
    "annex_iii_point": None,
    "annex_i_legislation": "Directive 2014/33/EU (lifts)",
    "art50_flag": False,
    "articles": ["Art. 6(1)", "Annex I"],
    "reason": "It is a safety component of a lift covered by Annex I legislation.",
}

REVIEW = {
    **GOOD,
    "tier": "needs-human-review",
    "articles": [],
    "review_reason": "missing-fact",
    "reason": "The description does not say whether the system decides on hiring.",
}


def rec(data):
    return Record.from_json(data)


def problems(data):
    return validate(rec(data))


def test_valid_examples_have_no_problems():
    for data in (GOOD, HIGH_RISK_ANNEX_III, HIGH_RISK_ANNEX_I, REVIEW):
        assert problems(data) == [], data


def test_tc_ls_2_01_annex_iii_needs_area_and_point():
    record = rec(HIGH_RISK_ANNEX_III)
    assert (record.route, record.annex_iii_area, record.annex_iii_point) == (
        "annex-iii",
        4,
        "4(a)",
    )
    assert any("route" in p for p in problems({**HIGH_RISK_ANNEX_III, "route": None}))
    assert any(
        "annex_iii_area" in p
        for p in problems({**HIGH_RISK_ANNEX_III, "annex_iii_area": 9})
    )
    assert any(
        "annex_iii_area" in p
        for p in problems({**HIGH_RISK_ANNEX_III, "annex_iii_area": None})
    )
    assert any(
        "annex_iii_point" in p
        for p in problems({**HIGH_RISK_ANNEX_III, "annex_iii_point": None})
    )


def test_annex_iii_point_must_belong_to_its_area():
    assert any(
        "annex_iii_point" in p
        for p in problems({**HIGH_RISK_ANNEX_III, "annex_iii_point": "5(b)"})
    )
    assert any(
        "annex_iii_point" in p
        for p in problems({**HIGH_RISK_ANNEX_III, "annex_iii_point": "four"})
    )
    assert (
        problems({**HIGH_RISK_ANNEX_III, "annex_iii_area": 2, "annex_iii_point": "2"})
        == []
    )


def test_tc_ls_2_02_annex_i_names_legislation_and_has_no_area():
    assert rec(HIGH_RISK_ANNEX_I).annex_i_legislation.endswith("(lifts)")
    assert any(
        "annex_iii_area" in p
        for p in problems({**HIGH_RISK_ANNEX_I, "annex_iii_area": 4})
    )
    assert any(
        "annex_i_legislation" in p
        for p in problems({**HIGH_RISK_ANNEX_I, "annex_i_legislation": None})
    )
    assert any(
        "annex_i_legislation" in p
        for p in problems({**HIGH_RISK_ANNEX_I, "annex_i_legislation": "  "})
    )


def test_route_and_route_details_must_be_empty_unless_high_risk():
    assert any("route" in p for p in problems({**GOOD, "route": "annex-iii"}))
    assert any("annex_iii_area" in p for p in problems({**GOOD, "annex_iii_area": 4}))
    assert any(
        "annex_i_legislation" in p
        for p in problems({**GOOD, "annex_i_legislation": "lifts"})
    )
    assert any(
        "route" in p for p in problems({**HIGH_RISK_ANNEX_III, "route": "annex-ii"})
    )


def test_tc_ls_3_01_high_risk_chatbot_keeps_tier_and_flag():
    record = rec(HIGH_RISK_ANNEX_III)
    assert record.tier == "high-risk" and record.art50_flag is True
    assert validate(record) == []


def test_tc_ls_3_02_minimal_case_flag_is_false_not_empty():
    assert rec(GOOD).art50_flag is False
    assert any("art50_flag" in p for p in problems({**GOOD, "art50_flag": None}))


def test_tc_ls_4_01_reason_of_exactly_40_words_is_accepted():
    reason = " ".join(["word"] * 39) + " end."
    assert len(reason.split()) == 40
    assert problems({**GOOD, "reason": reason}) == []


def test_tc_ls_4_02_reason_of_41_words_is_rejected_for_length():
    reason = " ".join(["word"] * 40) + " end."
    assert any("too long" in p for p in problems({**GOOD, "reason": reason}))


def test_tc_ls_4_03_empty_article_list_rejected_for_a_decided_tier():
    assert any("articles required" in p for p in problems({**GOOD, "articles": []}))


def test_needs_human_review_may_have_no_articles_but_needs_a_review_reason():
    assert problems(REVIEW) == []
    assert any(
        "review_reason" in p for p in problems({**REVIEW, "review_reason": None})
    )
    assert any(
        "review_reason" in p for p in problems({**REVIEW, "review_reason": "too-hard"})
    )
    assert any(
        "review_reason" in p
        for p in problems({**GOOD, "review_reason": "missing-fact"})
    )


@pytest.mark.parametrize(
    "reason",
    [
        "",
        "It filters spam",  # no sentence-ending mark
        "It filters spam. It is minimal.",  # two sentences
        "It filters spam!?",
        "It filters spam...",
    ],
)
def test_reason_must_be_one_sentence(reason):
    assert any("reason" in p for p in problems({**GOOD, "reason": reason}))


@pytest.mark.parametrize(
    "reason",
    [
        "It falls under Art. 50(1) because it talks to people.",
        "It handles personal data, e.g. names, but has no listed use.",
        "It meets the 6.5 threshold in no listed use?",
        "It lists inputs such as text, images etc.",
        "It runs on tools from Example Ltd. for screening.",
    ],
)
def test_realistic_abbreviations_and_decimals_do_not_end_the_sentence(reason):
    assert problems({**GOOD, "reason": reason}) == []


def test_articles_must_be_non_empty_strings():
    assert any("articles" in p for p in problems({**GOOD, "articles": [""]}))
    assert any("articles" in p for p in problems({**GOOD, "articles": [95]}))


def test_tc_ls_9_01_spec_example_record_has_every_field_and_is_valid():
    names = {f.name for f in dataclasses.fields(Record)}
    assert names == set(HIGH_RISK_ANNEX_III)
    record, status = parse_answer(json.dumps(HIGH_RISK_ANNEX_III))
    assert status == "ok" and record.to_json() == HIGH_RISK_ANNEX_III


def test_tc_ls_10_01_record_has_no_date_or_duties_field():
    names = {f.name for f in dataclasses.fields(Record)}
    for banned in ("date", "deadline", "applies_from", "duties", "obligations"):
        assert not any(banned in name for name in names)


# ---------- ADR-005: what parse_answer refuses ----------


def test_rule_breaking_record_is_unreadable():
    assert parse_answer(json.dumps({**GOOD, "articles": []})) == (None, "unreadable")


def test_missing_key_is_unreadable():
    data = dict(GOOD)
    del data["review_reason"]
    assert parse_answer(json.dumps(data)) == (None, "unreadable")


def test_unknown_key_is_unreadable():
    assert parse_answer(json.dumps({**GOOD, "deadline": "2026-08-02"})) == (
        None,
        "unreadable",
    )


def test_realistic_duplicate_key_is_unreadable_not_last_wins():
    raw = json.dumps(GOOD)[:-1] + ', "tier": "high-risk"}'
    assert parse_answer(raw) == (None, "unreadable")


@pytest.mark.parametrize(
    "field, value",
    [
        ("art50_flag", "false"),  # text, not a yes/no value
        ("art50_flag", 0),
        ("articles", "Art. 95"),  # one string, not a list
        ("reason", 5),
        ("tier", ["minimal"]),
    ],
)
def test_realistic_wrong_types_are_unreadable(field, value):
    assert parse_answer(json.dumps({**GOOD, field: value})) == (None, "unreadable")


@pytest.mark.parametrize("area", ["4", True, 4.0])
def test_realistic_area_must_be_a_whole_number_not_text_or_yes(area):
    raw = json.dumps({**HIGH_RISK_ANNEX_III, "annex_iii_area": area})
    assert parse_answer(raw) == (None, "unreadable")


def test_first_decodable_object_decides_even_if_a_later_one_is_valid():
    raw = '{"note": "thinking"} ' + json.dumps(GOOD)
    assert parse_answer(raw) == (None, "unreadable")


# ---------- the date detector (EV-8, LS-10) ----------


@pytest.mark.parametrize(
    "text",
    [
        "2 August 2026",
        "2 Aug 2026",
        "August 2026",
        "2026-08-02",
        "02/08/2026",
        "It applies from 2 August 2026.",
        "2\u00a0August\u00a02026",  # no-break spaces, as copied from web pages
        "2nd August 2026",
        "August 2, 2026",
        "02.08.2026",
        "Sept 2026",
        "The deadline is 2 august 2026.",
    ],
)
def test_contains_date_matches(text):
    assert contains_date(text)


@pytest.mark.parametrize(
    "text",
    [
        "2027",
        "Art. 113",
        "Annex III 4(a)",
        "Regulation (EU) 2024/1689",
        "Regulation (EU) 2026/1744",
        "It may 2026 be reviewed",
        "Section 6.5.2026",
        "",
    ],
)
def test_contains_date_does_not_match(text):
    assert not contains_date(text)
