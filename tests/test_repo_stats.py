"""The README progress block is counted from the repo, not typed by hand."""

import datetime
import importlib.util
import sys

import pytest
from conftest import ROOT

_spec = importlib.util.spec_from_file_location(
    "repo_stats", ROOT / "scripts" / "repo_stats.py"
)
repo_stats = importlib.util.module_from_spec(_spec)
sys.modules["repo_stats"] = repo_stats
_spec.loader.exec_module(repo_stats)


def test_guide_ranges_expand_to_one_row_per_chunk():
    guide = (
        "| P1-C02b Practice fine-tune (owner-run) | P1-C02 | x | y |\n"
        "| P3-C02 to P3-C06 Gold batches 1 to 5 | P2-C01 | x | y |\n"
        "| Chunk | Depends on | Enables | Parallel with |\n"
    )
    assert repo_stats.planned_chunks(guide) == [
        ("P1-C02b", "Practice fine-tune (owner-run)"),
        ("P3-C02", "Gold batch 1"),
        ("P3-C03", "Gold batch 2"),
        ("P3-C04", "Gold batch 3"),
        ("P3-C05", "Gold batch 4"),
        ("P3-C06", "Gold batch 5"),
    ]


def test_handover_reading():
    text = "## Status: Complete\n**Review passes:** [(1, 4), (2, 2), (3, 0)]\n"
    assert repo_stats.read_handover(text) == (True, (4, 2, 0))
    assert repo_stats.read_handover("## Status: In progress\n") == (False, ())


def test_real_repo_counts_match_the_files():
    chunks = repo_stats.collect(ROOT)
    handovers = {p.stem for p in (ROOT / "build" / "handovers").glob("*.md")}
    assert {c.id for c in chunks if c.done} == handovers
    assert all(
        c.passes[-1] == 0 for c in chunks if c.done
    )  # every review loop converged


def test_block_replaces_only_between_markers():
    block = repo_stats.render(
        repo_stats.collect(ROOT), "1 passing", ROOT, datetime.date(2026, 10, 27)
    )
    readme = f"intro\n{repo_stats.START}\nSTALE-BLOCK\n{repo_stats.END}\noutro\n"
    out = repo_stats.replace_block(readme, block)
    assert out.startswith("intro\n") and out.endswith("\noutro\n")
    assert "STALE-BLOCK" not in out and "| Automated tests | 1 passing |" in out
    with pytest.raises(ValueError):
        repo_stats.replace_block("no markers", block)
