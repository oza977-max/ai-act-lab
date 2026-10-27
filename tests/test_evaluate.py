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


# ---------- P1-C04: every measure ----------

from lab.evaluate import metrics_json, render_report

BASE = {
    "tier": "minimal",
    "route": None,
    "annex_iii_area": None,
    "annex_iii_point": None,
    "annex_i_legislation": None,
    "art50_flag": False,
    "articles": ["Art. 95"],
    "review_reason": None,
    "reason": "It has no listed use.",
}


def annex_iii(area, point, **extra):
    return {
        **BASE,
        "tier": "high-risk",
        "route": "annex-iii",
        "annex_iii_area": area,
        "annex_iii_point": point,
        "articles": ["Art. 6(2)", f"Annex III {point}"],
        **extra,
    }


def hand_made(tmp_path, pairs):
    """Write a gold file and outputs from (gold record, output record or raw) pairs."""
    gold_lines, out_lines = [], []
    for i, (g, o) in enumerate(pairs, start=1):
        case_id = f"H{i:02d}"
        gold_lines.append({"id": case_id, "description": "x", "gold": g})
        if o is not None:
            raw = o if isinstance(o, str) else json.dumps(o)
            out_lines.append({"id": case_id, "raw": raw, "seconds": 1.0, "error": None})
    gold = tmp_path / "gold.jsonl"
    gold.write_text("".join(json.dumps(l) + "\n" for l in gold_lines))
    run = tmp_path / "run"
    run.mkdir()
    (run / "outputs.jsonl").write_text("".join(json.dumps(l) + "\n" for l in out_lines))
    return gold, run


def test_tc_ev_3_01_area_accuracy_only_on_annex_iii_cases(tmp_path):
    pairs = [
        (annex_iii(4, "4(a)"), annex_iii(4, "4(a)")),
        (annex_iii(5, "5(b)"), annex_iii(5, "5(b)")),
        (annex_iii(1, "1(a)"), annex_iii(1, "1(a)")),
        (annex_iii(8, "8(a)"), annex_iii(4, "4(a)")),  # wrong area
    ] + [(BASE, BASE)] * 6
    m = measures(*hand_made(tmp_path, pairs))
    assert (m.area_correct, m.gold_annex_iii) == (3, 4)


def test_tc_ev_4_01_invented_article_is_an_invalid_citation(tmp_path):
    pairs = [(BASE, {**BASE, "articles": ["Art. 147"]}), (BASE, BASE)]
    m = measures(*hand_made(tmp_path, pairs))
    assert (m.citations_valid, m.citations) == (1, 2)
    assert m.invalid_citation_ids == ["H01"]


def test_tc_ev_4_02_overlap_with_gold_citations_counted(tmp_path):
    gold = {**BASE, "articles": ["Art. 6(2)"]}
    pairs = [
        (gold, {**BASE, "articles": ["Art. 6", "Art. 50(1)"]}),
        (gold, {**BASE, "articles": ["Art. 95"]}),
    ]
    m = measures(*hand_made(tmp_path, pairs))
    assert (m.overlap, m.gold_with_citation) == (1, 2)
    assert m.overlap_ids == ["H01"]


def test_tc_ev_5_01_unreadable_output_stays_in_the_denominator(eval10):
    gold, run_dir = eval10

    def prose(lines):
        lines[4]["raw"] = "I cannot answer that"
        return lines

    rewrite_outputs(run_dir, prose)
    m = measures(gold, run_dir)
    assert (m.tier_correct, m.total, m.unreadable) == (6, 10, 1)


def test_tc_ev_5_02_missing_output_counted_as_wrong(eval10):
    gold, run_dir = eval10
    rewrite_outputs(run_dir, lambda lines: lines[:4] + lines[5:])
    m = measures(gold, run_dir)
    assert (m.tier_correct, m.total, m.missing) == (6, 10, 1)


def test_tc_ev_6_01_every_proportion_has_an_interval_and_the_method_is_named(eval10):
    gold, run_dir = eval10
    report = render_report(measures(gold, run_dir), {})
    assert "Wilson score interval, 95%" in report
    table = report.split("## Measures", 1)[1].split("## Confusion", 1)[0]
    rows = [r for r in table.splitlines() if r.startswith("| ") and " of " in r]
    assert len(rows) >= 12
    for row in rows:
        result, interval = row.split(" | ")[1:3]
        assert "not defined" in result or "%" in interval, row


def test_tc_ev_8_02_article_50_flag_accuracy_reported(tmp_path):
    yes = {
        **BASE,
        "tier": "transparency-only",
        "art50_flag": True,
        "articles": ["Art. 50(1)"],
    }
    pairs = (
        [(yes, yes)] * 4 + [(yes, {**yes, "art50_flag": False})] + [(BASE, BASE)] * 5
    )
    m = measures(*hand_made(tmp_path, pairs))
    assert (m.flag_yes_correct, m.gold_flag_yes) == (4, 5)
    assert (m.flag_correct, m.total) == (9, 10)
    assert "| Article 50 flag accuracy | 9 of 10 (90%) |" in render_report(m, {})


def test_tc_ev_9_01_same_inputs_give_the_same_report_and_metrics(eval10):
    import random

    gold, run_dir = eval10
    rng = random.Random(20261027)
    run = {
        "model": "m",
        "prompt_version": "p",
        "guideline_version": "g",
        "gold_version": "v",
        "run_date": "2026-10-27",
        "build_revision": "b",
    }
    for _ in range(20):  # property: any variant of the answers repeats exactly

        def shuffle_answers(lines):
            raws = [l["raw"] for l in lines]
            rng.shuffle(raws)
            for l, r in zip(lines, raws):
                l["raw"] = r
            return lines

        rewrite_outputs(run_dir, shuffle_answers)
        first = (
            render_report(measures(gold, run_dir), run),
            metrics_json(measures(gold, run_dir), run),
        )
        second = (
            render_report(measures(gold, run_dir), run),
            metrics_json(measures(gold, run_dir), run),
        )
        assert first == second
        assert all(v in first[0] for v in ("m", "p", "g", "v", "2026-10-27"))


def test_tc_ev_10_01_report_opens_with_a_plain_english_summary(eval10):
    gold, run_dir = eval10
    report = render_report(measures(gold, run_dir), {})
    first = report.split("\n## ", 2)[1]
    assert first.startswith("Summary")
    assert "when it answered" in first and "does not show" in first
    assert "|" not in first


def test_realistic_unreadable_answers_cite_nothing_and_overlap_nothing(tmp_path):
    gold = {**BASE, "articles": ["Art. 95"]}
    pairs = [(gold, "Minimal risk under Art. 95."), (gold, None)]
    m = measures(*hand_made(tmp_path, pairs))
    assert (m.citations, m.overlap, m.gold_with_citation) == (0, 0, 2)


def test_realistic_invalid_gold_record_is_an_error(eval10):
    gold, _run_dir = eval10
    gold.write_text(
        gold.read_text().replace('"articles": ["Art. 95"]', '"articles": []', 1)
    )
    with pytest.raises(EvaluationError, match="articles required"):
        load_gold(gold)


def test_realistic_empty_raw_text_is_not_counted_as_text(tmp_path):
    pairs = [(BASE, "   "), (BASE, BASE)]
    m = measures(*hand_made(tmp_path, pairs))
    assert (m.with_raw, m.unreadable) == (1, 1)


def test_realistic_rounding_never_shows_all_or_none_falsely():
    from lab.evaluate import _fraction

    assert _fraction(199, 200) == "199 of 200 (99%)"
    assert _fraction(1, 200) == "1 of 200 (1%)"
    assert _fraction(200, 200) == "200 of 200 (100%)"
