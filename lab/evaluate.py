"""Evaluate a model's answers against the gold set (specs/data-and-evaluation.md).

Command:
    python -m lab.evaluate --gold <gold.jsonl> --run <run folder> [--paired <other run folder>]

Reads `outputs.jsonl` and `run.json` from the run folder, prints the headline
numbers, and writes `report.md` and `metrics.json` into the run folder. Every
proportion carries a 95% Wilson interval (ADR-004). With `--paired`, it also
writes `paired-vs-<other>.md`, and refuses if either run lacks a gold case.
Nothing is written when an input is malformed or the pair is incomplete.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from lab.articles import article_number, is_valid
from lab.records import (
    REVIEW_TIER,
    TIERS,
    Record,
    contains_date,
    parse_answer,
    validate,
)
from lab.stats import (
    BOOTSTRAP_METHOD,
    SEED,
    WILSON_METHOD,
    paired_bootstrap_diff,
    wilson,
)


class EvaluationError(Exception):
    """An input file is malformed; the message names the file and the problem."""


class PairingRefused(EvaluationError):
    """The paired comparison would not cover the same gold cases on both sides."""


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
    gold_annex_iii: int = 0
    area_correct: int = 0
    flag_correct: int = 0
    gold_flag_yes: int = 0
    flag_yes_correct: int = 0
    citations: int = 0
    citations_valid: int = 0
    gold_with_citation: int = 0
    overlap: int = 0
    unreadable: int = 0
    missing: int = 0
    with_raw: int = 0
    dates_found: int = 0
    unreadable_ids: list[str] = field(default_factory=list)
    missing_ids: list[str] = field(default_factory=list)
    date_ids: list[str] = field(default_factory=list)
    invalid_citation_ids: list[str] = field(default_factory=list)
    overlap_ids: list[str] = field(default_factory=list)
    case_correct: dict[str, bool] = field(default_factory=dict)
    confusion: dict[str, dict[str, int]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(int))
    )

    @property
    def answered_case_accuracy(self) -> float | None:
        return self.answered_correct / self.answered if self.answered else None


# (metrics key, report label, numerator, denominator, case ids shown)
MEASURES: tuple[tuple[str, str, str, str, str | None], ...] = (
    ("tier_accuracy", "Tier accuracy", "tier_correct", "total", None),
    ("share_answered", "Share answered", "answered", "total", None),
    (
        "answered_case_accuracy",
        "Answered-case accuracy",
        "answered_correct",
        "answered",
        None,
    ),
    (
        "review_when_gold_review",
        "Review when gold says review",
        "review_when_gold_review",
        "gold_review",
        None,
    ),
    (
        "review_when_gold_not",
        "Review when gold does not",
        "review_when_gold_not",
        "gold_not_review",
        None,
    ),
    (
        "annex_iii_area_accuracy",
        "Annex III area accuracy",
        "area_correct",
        "gold_annex_iii",
        None,
    ),
    ("art50_flag_accuracy", "Article 50 flag accuracy", "flag_correct", "total", None),
    (
        "art50_flag_yes_accuracy",
        "Article 50 flag right when gold says yes",
        "flag_yes_correct",
        "gold_flag_yes",
        None,
    ),
    (
        "citation_validity",
        "Citation validity",
        "citations_valid",
        "citations",
        "invalid_citation_ids",
    ),
    ("citation_overlap", "Citation overlap", "overlap", "gold_with_citation", None),
    ("format_failures", "Format failures", "unreadable", "total", "unreadable_ids"),
    ("missing_answers", "Missing answers", "missing", "total", "missing_ids"),
    ("dates_found", "Dates found", "dates_found", "with_raw", "date_ids"),
)


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
            raise EvaluationError(
                f"{path}: line {number} is not valid JSON ({exc.msg})"
            ) from exc
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


def load_gold(path: Path) -> dict[str, Record]:
    """Map each gold case id to its gold record; every record must be valid."""
    gold = {}
    for case_id, row in _index_by_id(_read_jsonl(path), path).items():
        data = row.get("gold")
        if not isinstance(data, dict):
            raise EvaluationError(f"{path}: case {case_id} has no gold record")
        try:
            record = Record.from_json(data)
        except (KeyError, TypeError, ValueError) as exc:
            raise EvaluationError(f"{path}: case {case_id}: gold record {exc}") from exc
        problems = validate(record)
        if problems:
            raise EvaluationError(f"{path}: case {case_id}: {'; '.join(problems)}")
        gold[case_id] = record
    if not gold:
        raise EvaluationError(f"{path}: the gold set has no cases")
    return gold


RUN_FIELDS = (
    "model",
    "build_revision",
    "prompt_version",
    "guideline_version",
    "gold_version",
    "run_date",
)


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


def _raw_text(output: dict | None) -> str | None:
    """The model's text, or None when the answer is missing or not text."""
    if output is None or output.get("error") == "missing":
        return None
    raw = output.get("raw")
    return raw if isinstance(raw, str) else None


def _read_answer(output: dict | None) -> tuple[Record | None, str]:
    """Return (record or None, status) where status is ok, unreadable or missing."""
    if output is None or output.get("error") == "missing":
        return None, "missing"
    return parse_answer(output.get("raw"))


def _article_numbers(citations: tuple[str, ...]) -> set[str]:
    return {n for n in map(article_number, citations) if n is not None}


def _score_case(m: Measures, case_id: str, gold: Record, output: dict | None) -> None:
    record, status = _read_answer(output)
    predicted = record.tier if record else None
    if status == "missing":
        m.missing += 1
        m.missing_ids.append(case_id)
    elif status == "unreadable":
        m.unreadable += 1
        m.unreadable_ids.append(case_id)
    raw = _raw_text(output)
    if raw is not None and raw.strip():
        # Dates are scanned in the raw text, even when the answer is unreadable.
        m.with_raw += 1
        if contains_date(raw):
            m.dates_found += 1
            m.date_ids.append(case_id)

    m.total += 1
    m.confusion[gold.tier][predicted or status] += 1
    correct = predicted == gold.tier
    m.case_correct[case_id] = correct
    m.tier_correct += correct
    if predicted is not None and predicted != REVIEW_TIER:
        m.answered += 1
        m.answered_correct += correct
    said_review = predicted == REVIEW_TIER
    if gold.tier == REVIEW_TIER:
        m.gold_review += 1
        m.review_when_gold_review += said_review
    else:
        m.gold_not_review += 1
        m.review_when_gold_not += said_review

    if gold.route == "annex-iii":
        m.gold_annex_iii += 1
        m.area_correct += bool(record and record.annex_iii_area == gold.annex_iii_area)
    flag_right = bool(record and record.art50_flag == gold.art50_flag)
    m.flag_correct += flag_right
    if gold.art50_flag:
        m.gold_flag_yes += 1
        m.flag_yes_correct += flag_right

    if record:
        valid = [is_valid(c) for c in record.articles]
        m.citations += len(valid)
        m.citations_valid += sum(valid)
        if not all(valid):
            m.invalid_citation_ids.append(case_id)
    if gold.articles:
        m.gold_with_citation += 1
        if record and _article_numbers(record.articles) & _article_numbers(
            gold.articles
        ):
            m.overlap += 1
            m.overlap_ids.append(case_id)


def evaluate(gold: dict[str, Record], outputs: dict[str, dict]) -> Measures:
    extra = sorted(set(outputs) - set(gold))
    if extra:
        raise EvaluationError(f"output ids not in the gold set: {', '.join(extra)}")
    m = Measures()
    for case_id, gold_record in gold.items():
        _score_case(m, case_id, gold_record, outputs.get(case_id))
    return m


# ---------- formatting ----------


def _percent(x: float) -> str:
    return f"{round(100 * x)}%"


def _share(k: int, n: int) -> str:
    """Rounded percentage that never claims all or none when that is not true."""
    if 0 < k < n:
        return f"{min(99, max(1, round(100 * k / n)))}%"
    return _percent(k / n)


def _fraction(k: int, n: int) -> str:
    return f"{k} of {n} ({_share(k, n)})" if n else "not defined (0 cases)"


def _interval(k: int, n: int) -> str:
    bounds = wilson(k, n)
    return (
        f"{_percent(bounds[0])} to {_percent(bounds[1])}" if bounds else "not defined"
    )


def _counts(m: Measures, numerator: str, denominator: str) -> tuple[int, int]:
    return getattr(m, numerator), getattr(m, denominator)


def headline(m: Measures) -> str:
    return (
        f"Tier correct: {m.tier_correct} of {m.total}\n"
        f"Answered (not sent to human review): {m.answered} of {m.total}\n"
        f"Correct when answered: "
        f"{f'{m.answered_correct} of {m.answered}' if m.answered else 'not defined (0 cases)'}\n"
        f"Unreadable answers: {m.unreadable}; missing answers: {m.missing}"
    )


def _summary(m: Measures) -> str:
    answered = (
        f"when it answered, it was right on {_fraction(m.answered_correct, m.answered)}, "
        f"95% interval {_interval(m.answered_correct, m.answered)}"
        if m.answered
        else "it answered no case itself, so its accuracy when answering is not defined"
    )
    return (
        f"The model gave the right tier on {_fraction(m.tier_correct, m.total)} cases "
        f"(95% interval {_interval(m.tier_correct, m.total)}). "
        f"It answered {_fraction(m.answered, m.total)} cases itself and sent the rest to "
        f"human review; {answered}. "
        f"Unreadable ({m.unreadable}) and missing ({m.missing}) answers count as wrong. "
        f"What this does not show: with {m.total} cases the intervals are wide, so a "
        "difference smaller than an interval means little; a right tier does not mean "
        "the reason or the citations were sound (see the citation rows); and the "
        "numbers say nothing about cases unlike the gold set."
    )


def _header(run: dict) -> str:
    def value(key: str) -> str:
        return str(run.get(key) or "(not recorded)")

    return (
        f"Model build: {value('build_revision')} | Prompt: {value('prompt_version')} | "
        f"Guideline: {value('guideline_version')} | Gold set: {value('gold_version')} | "
        f"Run date: {value('run_date')}"
    )


def render_report(m: Measures, run: dict) -> str:
    lines = [
        f"# Evaluation report: {run.get('model') or '(not recorded)'}",
        "",
        _header(run),
        "",
        "## Summary",
        "",
        _summary(m),
        "",
        "## Measures",
        "",
        (
            f"Intervals: {WILSON_METHOD}. Unreadable and missing answers count as wrong "
            "and as not answered."
        ),
        "",
        "| Measure | Result | 95% interval | Cases |",
        "|---|---|---|---|",
    ]
    for _key, label, numerator, denominator, ids in MEASURES:
        k, n = _counts(m, numerator, denominator)
        cases = ", ".join(getattr(m, ids)) if ids else ""
        lines.append(f"| {label} | {_fraction(k, n)} | {_interval(k, n)} | {cases} |")
    lines += ["", "## Confusion table (rows: gold tier; columns: answer)", ""]
    columns = list(TIERS) + ["unreadable", "missing"]
    lines.append("| Gold \\ Answer | " + " | ".join(columns) + " |")
    lines.append("|---" * (len(columns) + 1) + "|")
    for gold_tier in TIERS:
        row = m.confusion.get(gold_tier, {})
        lines.append(
            f"| {gold_tier} | " + " | ".join(str(row.get(c, 0)) for c in columns) + " |"
        )
    return "\n".join(lines) + "\n"


def metrics_json(m: Measures, run: dict) -> dict:
    """Every measure with its interval, for the comparison step (P4)."""
    measures = {}
    for key, _label, numerator, denominator, ids in MEASURES:
        k, n = _counts(m, numerator, denominator)
        bounds = wilson(k, n)
        measures[key] = {
            "k": k,
            "n": n,
            "value": k / n if n else None,
            "low": bounds[0] if bounds else None,
            "high": bounds[1] if bounds else None,
            **({"case_ids": list(getattr(m, ids))} if ids else {}),
        }
    return {
        "run": {k: run.get(k) or "(not recorded)" for k in RUN_FIELDS},
        "interval_method": WILSON_METHOD,
        "measures": measures,
    }


# ---------- paired comparison (EV-7) ----------


def check_pair(
    gold: dict, outputs_a: dict, outputs_b: dict, name_a: str, name_b: str
) -> None:
    """Refuse unless both runs have an answer line for every gold case."""
    gaps = []
    for name, outputs in ((name_a, outputs_a), (name_b, outputs_b)):
        lacking = [i for i in gold if _read_answer(outputs.get(i))[1] == "missing"]
        if lacking:
            gaps.append(f"{name} lacks {', '.join(lacking)}")
    if gaps:
        raise PairingRefused(
            "paired comparison refused: both runs must answer every gold case; "
            + "; ".join(gaps)
        )


def _points(x: float) -> str:
    return f"{round(100 * x) + 0}"


def render_paired(a: Measures, b: Measures, run_a: dict, run_b: dict) -> str:
    ids = list(a.case_correct)
    diff, low, high = paired_bootstrap_diff(
        [a.case_correct[i] for i in ids], [b.case_correct[i] for i in ids], seed=SEED
    )
    if low > 0:
        verdict = "Gain counted: the whole interval is above zero, so model A is better on tier accuracy."
    elif high < 0:
        verdict = "No gain counted for model A: the whole interval is below zero, so model B is better."
    else:
        verdict = "No gain counted: the interval includes zero, so these cases cannot tell the models apart."
    name_a = run_a.get("model") or "(not recorded)"
    name_b = run_b.get("model") or "(not recorded)"
    return "\n".join(
        [
            f"# Paired comparison: {name_a} (A) vs {name_b} (B)",
            "",
            (
                f"Gold set: {run_a.get('gold_version') or '(not recorded)'} | "
                f"A run date: {run_a.get('run_date') or '(not recorded)'} | "
                f"B run date: {run_b.get('run_date') or '(not recorded)'}"
            ),
            "",
            f"Both models answered the same {len(ids)} gold cases.",
            (
                f"Tier accuracy: A {_fraction(a.tier_correct, a.total)}, "
                f"B {_fraction(b.tier_correct, b.total)}."
            ),
            (
                f"Difference: {_points(diff)} percentage points (A minus B); 95% interval "
                f"{_points(low)} to {_points(high)} percentage points ({BOOTSTRAP_METHOD}, seed {SEED})."
            ),
            "",
            verdict,
            "",
        ]
    )


# ---------- command ----------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate a model run against the gold set."
    )
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument(
        "--run",
        type=Path,
        required=True,
        help="run folder with outputs.jsonl and run.json",
    )
    parser.add_argument(
        "--paired", type=Path, help="a second run folder to compare with, case by case"
    )
    args = parser.parse_args(argv)
    try:
        gold = load_gold(args.gold)
        run = load_run(args.run / "run.json")
        outputs = load_outputs(args.run / "outputs.jsonl")
        measures = evaluate(gold, outputs)
        paired_text = paired_path = None
        if args.paired:
            other_run = load_run(args.paired / "run.json")
            other_outputs = load_outputs(args.paired / "outputs.jsonl")
            check_pair(gold, outputs, other_outputs, str(args.run), str(args.paired))
            paired_text = render_paired(
                measures, evaluate(gold, other_outputs), run, other_run
            )
            paired_path = args.run / f"paired-vs-{args.paired.resolve().name}.md"
        (args.run / "report.md").write_text(
            render_report(measures, run), encoding="utf-8"
        )
        (args.run / "metrics.json").write_text(
            json.dumps(metrics_json(measures, run), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if paired_path:
            paired_path.write_text(paired_text, encoding="utf-8")
    except (EvaluationError, OSError) as exc:
        print(f"evaluate: {exc}", file=sys.stderr)
        return 1
    print(headline(measures))
    print(f"Report written to {args.run / 'report.md'}")
    if paired_path:
        print(f"Paired comparison written to {paired_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
