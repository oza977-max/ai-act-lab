"""P1-C03 acceptance test: the record rules reach the owner's evaluation command.

An answer with the right tier but a broken rule is unreadable (ADR-005), and a
date anywhere in an answer is flagged (TC-EV-8-01).
"""

import json

from test_p1c01_acceptance import run_cli


def _edit_outputs(run_dir, edits):
    path = run_dir / "outputs.jsonl"
    lines = [json.loads(line) for line in path.read_text().splitlines()]
    for line in lines:
        if line["id"] in edits:
            record = json.loads(line["raw"])
            record.update(edits[line["id"]])
            line["raw"] = json.dumps(record)
    path.write_text("".join(json.dumps(line) + "\n" for line in lines))


def test_rule_breaking_answer_is_unreadable_and_dates_are_flagged(eval10):
    gold, run_dir = eval10
    _edit_outputs(
        run_dir,
        {
            # Right tier, but a 41-word reason: no longer counts as correct.
            "E01": {"reason": " ".join(["word"] * 40) + " end."},
            # Still a valid record, but it states a date.
            "E02": {"reason": "It filters job applicants and applies from 2 August 2026."},
        },
    )
    result = run_cli(gold, run_dir)
    assert result.returncode == 0, result.stderr
    assert "Tier correct: 6 of 10" in result.stdout
    report = (run_dir / "report.md").read_text(encoding="utf-8")
    assert "| Unreadable answers | 1 (E01) |" in report
    assert "| Dates found | 1 of 10 (E02) |" in report
