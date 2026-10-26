"""P1-C01 acceptance test: the evaluation runs end to end on the 10-case fixture.

TC-EV-1-01 and TC-EV-2-01, from the owner's command line.
"""
import subprocess
import sys

from conftest import ROOT


def run_cli(gold, run_dir):
    return subprocess.run(
        [sys.executable, "-m", "lab.evaluate", "--gold", str(gold), "--run", str(run_dir)],
        capture_output=True, text=True, cwd=ROOT,
    )


def test_tc_ev_1_01_and_2_01_cli_prints_hand_counts_and_writes_report(eval10):
    gold, run_dir = eval10
    result = run_cli(gold, run_dir)
    assert result.returncode == 0, result.stderr
    assert "7 of 10" in result.stdout
    assert "6 of 8" in result.stdout
    report = (run_dir / "report.md").read_text(encoding="utf-8")
    first_section = report.split("\n## ", 2)[1]
    assert first_section.startswith("Summary")
    assert "fixture-model" in report and "zero-shot-v0" in report and "2026-10-26" in report


def test_report_and_stdout_never_contain_raw_model_text(eval10):
    import json
    gold, run_dir = eval10
    path = run_dir / "outputs.jsonl"
    lines = [json.loads(l) for l in path.read_text().splitlines()]
    lines[4]["raw"] = "CANARY-7f3a unreadable prose answer"
    path.write_text("".join(json.dumps(l) + "\n" for l in lines))
    result = run_cli(gold, run_dir)
    assert result.returncode == 0
    assert "CANARY-7f3a" not in result.stdout
    assert "CANARY-7f3a" not in (run_dir / "report.md").read_text()


def test_zero_answered_renders_not_defined(eval10):
    import json
    gold, run_dir = eval10
    path = run_dir / "outputs.jsonl"
    lines = [json.loads(l) for l in path.read_text().splitlines()]
    for l in lines:
        r = json.loads(l["raw"]); r["tier"] = "needs-human-review"; l["raw"] = json.dumps(r)
    path.write_text("".join(json.dumps(l) + "\n" for l in lines))
    result = run_cli(gold, run_dir)
    assert "Correct when answered: not defined" in result.stdout
    assert "not defined" in (run_dir / "report.md").read_text()


def test_malformed_run_json_exits_1_naming_the_file(eval10):
    gold, run_dir = eval10
    (run_dir / "run.json").write_text("{not json")
    result = run_cli(gold, run_dir)
    assert result.returncode == 1
    assert "run.json" in result.stderr


def test_missing_run_fields_show_not_recorded(eval10):
    gold, run_dir = eval10
    (run_dir / "run.json").write_text('{"model": "m"}')
    result = run_cli(gold, run_dir)
    assert result.returncode == 0
    report = (run_dir / "report.md").read_text()
    assert "None" not in report.split("## Summary")[0]
    assert "(not recorded)" in report
