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
