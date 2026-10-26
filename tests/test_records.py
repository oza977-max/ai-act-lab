"""Parsing a model's raw answer (ADR-005; this chunk checks the tier only)."""
import json

from lab.records import TIERS, parse_answer

GOOD = {"tier": "minimal", "route": None, "annex_iii_area": None, "annex_iii_point": None,
        "annex_i_legislation": None, "art50_flag": False, "articles": ["Art. 95"],
        "review_reason": None, "reason": "It filters spam."}


def test_six_tiers():
    assert TIERS == ("prohibited", "high-risk", "transparency-only", "minimal",
                     "out-of-scope", "needs-human-review")


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
    assert parse_answer(json.dumps({**GOOD, "tier": "limited-risk"})) == (None, "unreadable")


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
