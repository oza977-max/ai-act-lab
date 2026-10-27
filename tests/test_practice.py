"""Practice data preparation (LG-3, P1-C02b)."""

import json

from lab.practice import (
    TIER_MAP,
    build_description,
    build_target,
    parse_practice_answer,
    practice_prompt,
    split_items,
)

ITEM = {
    "role": "Deployer",
    "intended_use": "Score job applicants' CVs to shortlist candidates",
    "system_type": "CV ranking model",
    "input_data": "CVs, cover letters",
    "domain": "Employment",
    "related_articles": [6, 26],
    "obligations": ["Keep logs for six months under Article 26(6)."],
    "risk_level": "high-risk",
}


def items(n_per_tier=30):
    out = []
    for tier in TIER_MAP:
        for i in range(n_per_tier):
            out.append({**ITEM, "risk_level": tier, "intended_use": f"{tier} use {i}"})
    return out


def test_description_uses_the_case_fields():
    text = build_description(ITEM)
    for part in ("Deployer", "Score job applicants", "CV ranking model", "CVs, cover letters", "Employment"):
        assert part in text


def test_target_has_tier_articles_reason_and_never_obligations():
    target = build_target(ITEM)
    assert set(target) == {"tier", "articles", "reason"}
    assert target["tier"] == "high-risk"
    assert target["articles"] == ["Art. 6", "Art. 26"]
    assert "six months" not in json.dumps(target)
    assert "logs" not in json.dumps(target).lower()


def test_limited_maps_to_transparency_only():
    assert build_target({**ITEM, "risk_level": "limited"})["tier"] == "transparency-only"


def test_split_is_stratified_disjoint_and_repeatable():
    data = items()
    a = split_items(data, seed=20261027)
    b = split_items(data, seed=20261027)
    assert a == b
    train, valid, heldout = a
    assert len(heldout) == 20 and len(valid) == 32
    for part, per_tier in ((heldout, 5), (valid, 8)):
        tiers = [x["risk_level"] for x in part]
        assert all(tiers.count(t) == per_tier for t in TIER_MAP)
    keys = lambda part: {x["intended_use"] for x in part}  # noqa: E731
    assert not keys(train) & keys(heldout)
    assert not keys(train) & keys(valid)
    assert not keys(valid) & keys(heldout)
    assert len(train) + len(valid) + len(heldout) == len(data)


def test_prompt_wraps_description_in_case_delimiters():
    prompt = practice_prompt("A system.")
    assert "<<<CASE\nA system.\nCASE>>>" in prompt
    assert "transparency-only" in prompt


def test_parse_practice_answer_reads_tier():
    raw = 'Sure: {"tier": "minimal", "articles": ["Art. 95"], "reason": "x"}'
    assert parse_practice_answer(raw) == "minimal"


def test_realistic_answer_with_unknown_or_missing_tier_is_unreadable():
    assert parse_practice_answer('{"tier": "limited-risk"}') is None
    assert parse_practice_answer("It is high risk.") is None
    assert parse_practice_answer(None) is None
