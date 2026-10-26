"""Evaluate a model's answers against the gold set (specs/data-and-evaluation.md).

Command:
    python -m lab.evaluate --gold <gold.jsonl> --run <run folder>

Reads `outputs.jsonl` and `run.json` from the run folder, prints the headline
numbers, and writes `report.md` into the run folder. This chunk covers tier
accuracy, share answered, answered-case accuracy and the review rates; the
remaining measures and intervals arrive in P1-C04.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from lab.records import REVIEW_TIER, TIERS, parse_answer


class EvaluationError(Exception):
    """An input file is malformed; the message names the file and the problem."""


@dataclass
class Measures:
    total: int = 0
    tier_correct: int = 0
    answered: int = 0
    answered_correct: int = 0
    gold_review: int = 0
    review_when_gold_review: int = 0
    gold_not_review: int = 0
    review_when_gold_not: int = 0
    unreadable: int = 0
    missing: int = 0
    unreadable_ids: list[str] = field(default_factory=list)
    missing_ids: list[str] = field(default_factory=list)
    confusion: dict[str, dict[str, int]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(int))
    )

    @property
    def answered_case_accuracy(self) -> float | None:
        return self.answered_correct / self.answered if self.answered else None


def _read_jsonl(path: Path) -> list[tuple[int, dict]]:
    """Return (line number, object) pairs; every non-blank line must be a JSON object."""
    rows = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise EvaluationError(f"{path}: not valid UTF-8 text") from exc
    # Split on real line breaks only: str.splitlines() would also split inside
    # answers containing Unicode separators such as U+2028.
    for number, line in enumerate(text.split("\n"), start=1):
        line = line.rstrip("\r")
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EvaluationError(f"{path}: line {number} is not valid JSON ({exc.msg})") from exc
        if not isinstance(row, dict):
            raise EvaluationError(f"{path}: line {number}: not a JSON object")
        rows.append((number, row))
    return rows


def _index_by_id(rows: list[tuple[int, dict]], path: Path) -> dict[str, dict]:
    indexed: dict[str, dict] = {}
    for number, row in rows:
        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id:
            raise EvaluationError(f"{path}: line {number}: missing or non-text id")
        if row_id in indexed:
            raise EvaluationError(f"{path}: line {number}: duplicate id {row_id}")
        indexed[row_id] = row
    return indexed


def load_gold(path: Path) -> dict[str, str]:
    """Map each gold case id to its gold tier."""
    gold = {}
    for case_id, row in _index_by_id(_read_jsonl(path), path).items():
        record = row.get("gold")
        tier = record.get("tier") if isinstance(record, dict) else None
        if tier not in TIERS:
            raise EvaluationError(f"{path}: case {case_id} has unknown gold tier {tier!r}")
        gold[case_id] = tier
    if not gold:
        raise EvaluationError(f"{path}: the gold set has no cases")
    return gold


RUN_FIELDS = ("model", "build_revision", "prompt_version", "guideline_version", "gold_version", "run_date")


def load_run(path: Path) -> dict:
    """Read run.json; missing header fields are shown as '(not recorded)'."""
    try:
        run = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise EvaluationError(f"{path}: not valid JSON") from exc
    if not isinstance(run, dict):
        raise EvaluationError(f"{path}: not a JSON object")
    return {**run, **{k: run.get(k) or "(not recorded)" for k in RUN_FIELDS}}


def load_outputs(path: Path) -> dict[str, dict]:
    return _index_by_id(_read_jsonl(path), path)


def _predicted_tier(output: dict | None) -> tuple[str | None, str]:
    """Return (tier or None, status) where status is ok, unreadable or missing."""
    if output is None or output.get("error") == "missing":
        return None, "missing"
    record, status = parse_answer(output.get("raw"))
    return (record.tier if record else None), status


def evaluate(gold: dict[str, str], outputs: dict[str, dict]) -> Measures:
    extra = sorted(set(outputs) - set(gold))
    if extra:
        raise EvaluationError(f"output ids not in the gold set: {', '.join(extra)}")
    m = Measures()
    for case_id, gold_tier in gold.items():
        predicted, status = _predicted_tier(outputs.get(case_id))
        m.total += 1
        if status == "missing":
            m.missing += 1
            m.missing_ids.append(case_id)
        elif status == "unreadable":
            m.unreadable += 1
            m.unreadable_ids.append(case_id)
        m.confusion[gold_tier][predicted or status] += 1
        correct = predicted == gold_tier
        m.tier_correct += correct
        if predicted is not None and predicted != REVIEW_TIER:
            m.answered += 1
            m.answered_correct += correct
        said_review = predicted == REVIEW_TIER
        if gold_tier == REVIEW_TIER:
            m.gold_review += 1
            m.review_when_gold_review += said_review
        else:
            m.gold_not_review += 1
            m.review_when_gold_not += said_review
    return m


def _fraction(k: int, n: int) -> str:
    return f"{k} of {n}" if n else "not defined (0 cases)"


def headline(m: Measures) -> str:
    return (
        f"Tier correct: {_fraction(m.tier_correct, m.total)}\n"
        f"Answered (not sent to human review): {_fraction(m.answered, m.total)}\n"
        f"Correct when answered: {_fraction(m.answered_correct, m.answered)}\n"
        f"Unreadable answers: {m.unreadable}; missing answers: {m.missing}"
    )


def render_report(m: Measures, run: dict) -> str:
    lines = [
        f"# Evaluation report: {run['model']}",
        "",
        f"Model build: {run['build_revision']} | Prompt: {run['prompt_version']} | "
        f"Guideline: {run['guideline_version']} | Gold set: {run['gold_version']} | "
        f"Run date: {run['run_date']}",
        "",
        "## Summary",
        "",
        f"The model gave the right tier on {_fraction(m.tier_correct, m.total)} cases. "
        f"It answered {_fraction(m.answered, m.total)} cases itself and sent the rest to human "
        f"review; when it answered, it was right on {_fraction(m.answered_correct, m.answered)}. "
        f"Unreadable ({m.unreadable}) and missing ({m.missing}) answers count as wrong. "
        "These numbers have no confidence intervals yet, so small differences mean little.",
        "",
        "## Measures",
        "",
        "| Measure | Result |",
        "|---|---|",
        f"| Tier accuracy | {_fraction(m.tier_correct, m.total)} |",
        f"| Share answered | {_fraction(m.answered, m.total)} |",
        f"| Answered-case accuracy | {_fraction(m.answered_correct, m.answered)} |",
        f"| Review when gold says review | {_fraction(m.review_when_gold_review, m.gold_review)} |",
        f"| Review when gold does not | {_fraction(m.review_when_gold_not, m.gold_not_review)} |",
        f"| Unreadable answers | {m.unreadable} ({', '.join(m.unreadable_ids) or 'none'}) |",
        f"| Missing answers | {m.missing} ({', '.join(m.missing_ids) or 'none'}) |",
        "",
        "## Confusion table (rows: gold tier; columns: answer)",
        "",
    ]
    columns = list(TIERS) + ["unreadable", "missing"]
    lines.append("| Gold \\ Answer | " + " | ".join(columns) + " |")
    lines.append("|---" * (len(columns) + 1) + "|")
    for gold_tier in TIERS:
        row = m.confusion.get(gold_tier, {})
        lines.append(f"| {gold_tier} | " + " | ".join(str(row.get(c, 0)) for c in columns) + " |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate a model run against the gold set.")
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True, help="run folder with outputs.jsonl and run.json")
    args = parser.parse_args(argv)
    try:
        run = load_run(args.run / "run.json")
        measures = evaluate(load_gold(args.gold), load_outputs(args.run / "outputs.jsonl"))
        (args.run / "report.md").write_text(render_report(measures, run), encoding="utf-8")
    except (EvaluationError, OSError) as exc:
        print(f"evaluate: {exc}", file=sys.stderr)
        return 1
    print(headline(measures))
    print(f"Report written to {args.run / 'report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
