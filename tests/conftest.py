import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "eval-10"
sys.path.insert(0, str(ROOT))


@pytest.fixture
def eval10(tmp_path):
    """A writable copy of the 10-case fixture: (gold path, run folder)."""
    dest = tmp_path / "eval-10"
    shutil.copytree(FIXTURE, dest)
    return dest / "gold.jsonl", dest / "run"
