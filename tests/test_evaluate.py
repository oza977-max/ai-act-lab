"""Measures on the 10-case fixture and its variants (measure definitions table)."""

import json

import pytest

from lab.evaluate import EvaluationError, evaluate, load_gold, load_outputs


def measures(gold, run_dir):
    return evaluate(load_gold(gold), load_outputs(run_dir / "outputs.jsonl"))


def rewrite_outputs(run_dir, change):
    path = run_dir / "outputs.jsonl"
    lines = [json.loads(l) for l in path.read_text().splitlines()]
    lines = change(lines)
    path.write_text("".join(json.dumps(l) + "\n" for l in lines))


def test_tc_ev_1_01_tier_accuracy_and_confusion(eval10):
    m = measures(*eval10)
    assert (m.tier_correct, m.total) == (7, 10)
    assert sum(sum(row.values()) for row in m.confusion.values()) == 10
    assert m.confusion["transparency-only"]["minimal"] == 1


def test_tc_ev_2_01_answered_measures(eval10):
    m = measures(*eval10)
    assert (m.answered, m.answered_correct) == (8, 6)
    assert (m.review_when_gold_review, m.gold_review) == (1, 1)
    assert (m.review_when_gold_not, m.gold_not_review) == (1, 9)


def test_tc_ev_2_02_all_review_has_zero_coverage_and_undefined_accuracy(eval10):
    gold, run_dir = eval10

    def all_review(lines):
        for l in lines:
            r = json.loads(l["raw"])
            r["tier"] = "needs-human-review"
            l["raw"] = json.dumps(r)
        return lines

    rewrite_outputs(run_dir, all_review)
    m = measures(gold, run_dir)
    assert m.answered == 0
    assert m.answered_case_accuracy is None


def test_realistic_missing_line_counts_as_wrong(eval10):
    gold, run_dir = eval10
    rewrite_outputs(run_dir, lambda lines: [l for l in lines if l["id"] != "E05"])
    m = measures(gold, run_dir)
    assert (m.tier_correct, m.total, m.missing) == (6, 10, 1)


def test_realistic_missing_marker_equals_absent_line(eval10):
    gold, run_dir = eval10

    def mark(lines):
        for l in lines:
            if l["id"] == "E05":
                l.update(raw=None, seconds=None, error="missing")
        return lines

    rewrite_outputs(run_dir, mark)
    m = measures(gold, run_dir)
    assert (m.tier_correct, m.missing, m.unreadable) == (6, 1, 0)


def test_realistic_unreadable_counts_as_wrong_and_not_answered(eval10):
    gold, run_dir = eval10

    def garble(lines):
        for l in lines:
            if l["id"] == "E05":
                l["raw"] = "I cannot answer that"
        return lines

    rewrite_outputs(run_dir, garble)
    m = measures(gold, run_dir)
    assert (m.tier_correct, m.unreadable, m.answered) == (6, 1, 7)


def test_output_id_not_in_gold_is_an_error(eval10):
    gold, run_dir = eval10
    rewrite_outputs(run_dir, lambda lines: lines + [{**lines[0], "id": "E99"}])
    with pytest.raises(EvaluationError, match="E99"):
        measures(gold, run_dir)


def test_duplicate_output_id_is_an_error(eval10):
    gold, run_dir = eval10
    rewrite_outputs(run_dir, lambda lines: lines + [lines[0]])
    with pytest.raises(EvaluationError, match="E01"):
        measures(gold, run_dir)


def test_malformed_gold_line_names_file_and_line(eval10):
    gold, _run_dir = eval10
    gold.write_text(gold.read_text() + "{not json\n")
    with pytest.raises(EvaluationError, match=r"gold.jsonl.*line 11"):
        load_gold(gold)


def test_duplicate_id_error_names_the_line(eval10):
    gold, run_dir = eval10
    rewrite_outputs(run_dir, lambda lines: lines + [lines[0]])
    with pytest.raises(
        EvaluationError, match=r"outputs.jsonl: line 11: duplicate id E01"
    ):
        measures(gold, run_dir)


def test_non_object_line_is_an_error_with_line(eval10):
    gold, run_dir = eval10
    path = run_dir / "outputs.jsonl"
    path.write_text(path.read_text() + "[1]\n")
    with pytest.raises(EvaluationError, match=r"line 11: not a JSON object"):
        measures(gold, run_dir)


def test_non_string_raw_counts_as_unreadable(eval10):
    gold, run_dir = eval10

    def numeric(lines):
        for l in lines:
            if l["id"] == "E05":
                l["raw"] = 5
        return lines

    rewrite_outputs(run_dir, numeric)
    assert measures(gold, run_dir).unreadable == 1


def test_unknown_gold_tier_is_an_error(eval10):
    gold, _run_dir = eval10
    gold.write_text(
        gold.read_text().replace('"tier": "prohibited"', '"tier": "limited-risk"', 1)
    )
    with pytest.raises(EvaluationError, match="limited-risk"):
        load_gold(gold)


def test_empty_gold_set_is_an_error(eval10):
    gold, _run_dir = eval10
    gold.write_text("")
    with pytest.raises(EvaluationError, match="no cases"):
        load_gold(gold)


def test_realistic_unicode_line_separator_inside_raw_answer(eval10):
    gold, run_dir = eval10
    path = run_dir / "outputs.jsonl"
    lines = [json.loads(l) for l in path.read_text().splitlines() if l]
    lines[4]["raw"] = lines[4]["raw"].replace("spam", "spam filter")
    path.write_text(
        "".join(json.dumps(l, ensure_ascii=False) + "\n" for l in lines),
        encoding="utf-8",
    )
    assert measures(gold, run_dir).tier_correct == 7


def test_tc_ev_8_01_date_in_output_is_flagged(eval10):
    gold, run_dir = eval10

    def dated(lines):
        for l in lines:
            if l["id"] == "E03":
                record = json.loads(l["raw"])
                record["reason"] = "It scores credit and applies from 2 August 2026."
                l["raw"] = json.dumps(record)
        return lines

    rewrite_outputs(run_dir, dated)
    m = measures(gold, run_dir)
    assert m.date_ids == ["E03"]
    assert (m.dates_found, m.with_raw) == (1, 10)


def test_realistic_date_is_flagged_even_in_an_unreadable_answer(eval10):
    gold, run_dir = eval10

    def prose(lines):
        for l in lines:
            if l["id"] == "E05":
                l["raw"] = "Minimal risk; obligations start 2026-08-02."
            if l["id"] == "E06":
                l["raw"] = None
        return lines

    rewrite_outputs(run_dir, prose)
    m = measures(gold, run_dir)
    assert "E05" in m.unreadable_ids and m.date_ids == ["E05"]
    assert m.with_raw == 9
