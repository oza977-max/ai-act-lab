"""P1-C04 acceptance test: the full evaluation from the owner's command line.

Every measure with a 95% interval, metrics.json for the comparison, and the
paired mode that refuses an incomplete pair (EV-3 to EV-7, EV-9, EV-10).
"""

import json
import shutil
import subprocess
import sys

from conftest import ROOT


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "lab.evaluate", *map(str, args)],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_full_report_metrics_and_paired_comparison(eval10):
    gold, run_dir = eval10
    result = run_cli("--gold", gold, "--run", run_dir)
    assert result.returncode == 0, result.stderr

    report = (run_dir / "report.md").read_text(encoding="utf-8")
    summary = report.split("\n## ", 2)[1]
    assert summary.startswith("Summary")
    assert "6 of 8" in summary and "does not show" in summary
    assert "Wilson score interval, 95%" in report
    for row in (
        "| Tier accuracy | 7 of 10 (70%) | 40% to 89% |",
        "| Annex III area accuracy | 2 of 2 (100%) |",
        "| Article 50 flag accuracy |",
        "| Citation validity |",
        "| Citation overlap |",
        "| Format failures | 0 of 10 (0%) | 0% to 28% |",
    ):
        assert row in report, row

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["run"]["model"] == "fixture-model"
    tier = metrics["measures"]["tier_accuracy"]
    assert (tier["k"], tier["n"]) == (7, 10)
    assert round(tier["low"], 4) == 0.3968

    # A second model with the same answers: paired comparison, no gain.
    other = run_dir.parent / "other-model"
    shutil.copytree(run_dir, other)
    result = run_cli("--gold", gold, "--run", run_dir, "--paired", other)
    assert result.returncode == 0, result.stderr
    paired = (run_dir / "paired-vs-other-model.md").read_text(encoding="utf-8")
    assert "Difference: 0 percentage points" in paired
    assert "No gain counted" in paired

    # Remove case E07 from the second model: the comparison refuses.
    lines = (other / "outputs.jsonl").read_text().splitlines()
    (other / "outputs.jsonl").write_text(
        "".join(line + "\n" for line in lines if '"E07"' not in line)
    )
    (run_dir / "paired-vs-other-model.md").unlink()
    result = run_cli("--gold", gold, "--run", run_dir, "--paired", other)
    assert result.returncode == 1
    assert "refused" in result.stderr and "E07" in result.stderr
    assert not (run_dir / "paired-vs-other-model.md").exists()
