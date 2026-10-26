"""TC-GS-2-03: the pre-commit guard blocks a planted private name (cross-cutting ADR-007)."""
import shutil
import subprocess

from conftest import ROOT

GUARD = ROOT / "scripts" / "confidentiality-check.sh"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def make_repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    git(repo, "init", "-q")
    shutil.copy(GUARD, repo / "scripts" / "confidentiality-check.sh")
    (repo / ".private").mkdir()
    (repo / ".private" / "deny-terms.txt").write_text("Zebrafoo Holdings\n")
    return repo


def run_guard(repo):
    return subprocess.run(["sh", "scripts/confidentiality-check.sh"], cwd=repo,
                          capture_output=True, text=True)


def test_tc_gs_2_03_planted_private_name_is_blocked(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "case.md").write_text("A recruitment tool built by Zebrafoo Holdings.\n")
    git(repo, "add", "case.md")
    result = run_guard(repo)
    assert result.returncode == 1
    assert "BLOCKED" in result.stdout
    assert "Zebrafoo" not in result.stdout, "the private term must not be echoed"


def test_clean_change_passes(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "case.md").write_text("A recruitment tool built by a fictional company.\n")
    git(repo, "add", "case.md")
    assert run_guard(repo).returncode == 0


def test_file_name_with_space_is_scanned(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "my case.md").write_text("Built by Zebrafoo Holdings.\n")
    git(repo, "add", "my case.md")
    assert run_guard(repo).returncode == 1


def test_added_line_starting_with_plus_plus_is_scanned(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "case.md").write_text("++ Zebrafoo Holdings\n")
    git(repo, "add", "case.md")
    assert run_guard(repo).returncode == 1


def test_blank_line_in_private_list_does_not_block_everything(tmp_path):
    repo = make_repo(tmp_path)
    (repo / ".private" / "deny-terms.txt").write_text("Zebrafoo Holdings\n\n   \n")
    (repo / "case.md").write_text("A clean line.\n")
    git(repo, "add", "case.md")
    assert run_guard(repo).returncode == 0


def test_private_list_with_windows_line_endings_still_blocks(tmp_path):
    repo = make_repo(tmp_path)
    (repo / ".private" / "deny-terms.txt").write_bytes(b"Zebrafoo Holdings\r\n")
    (repo / "case.md").write_text("Built by Zebrafoo Holdings.\n")
    git(repo, "add", "case.md")
    assert run_guard(repo).returncode == 1


def test_private_name_in_file_name_is_blocked_without_echo(tmp_path):
    repo = make_repo(tmp_path)
    (repo / ".private" / "deny-terms.txt").write_text("Zebrafoo\n")
    (repo / "d").mkdir()
    (repo / "d" / "Zebrafoo.md").write_text("clean text\n")
    git(repo, "add", "d/Zebrafoo.md")
    result = run_guard(repo)
    assert result.returncode == 1
    assert "Zebrafoo" not in result.stdout
