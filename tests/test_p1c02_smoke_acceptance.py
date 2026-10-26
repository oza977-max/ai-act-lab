"""P1-C02 acceptance: one real answer from the smallest candidate on this Mac.

Skipped automatically when the model is not in the local cache, so the suite
still runs on a machine that has not downloaded it.
"""

import re
import subprocess
import sys

import pytest
from conftest import ROOT


def model_cached():
    try:
        from huggingface_hub import snapshot_download

        snapshot_download(
            "mlx-community/Qwen3.5-0.8B-4bit",
            revision="da28692b5f139cb0ec58a356b437486b7dac7462",
            local_files_only=True,
        )
        return True
    except Exception:  # noqa: BLE001 - any failure means "not cached"
        return False


@pytest.mark.skipif(
    not model_cached(), reason="Qwen3.5-0.8B 4-bit not in the local cache"
)
def test_smoke_loads_real_model_and_reports_time_and_memory():
    result = subprocess.run(
        [sys.executable, "-m", "lab.bakeoff", "smoke", "--model", "qwen3.5-0.8b"],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=600,
    )
    assert result.returncode == 0, result.stderr[-2000:]
    peak = float(re.search(r"Peak memory: ([0-9.]+) GB", result.stdout).group(1))
    assert 0 < peak < 6.5
    assert re.search(r"Load seconds: [0-9.]+", result.stdout)
    assert re.search(r"Answer seconds: [0-9.]+", result.stdout)
    assert re.search(r"Answer readable as a record: (yes|no)", result.stdout)
