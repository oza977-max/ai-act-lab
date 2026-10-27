"""Refresh the "Progress at a glance" block in README.md from the repository itself.

Every number is counted from files in the repo (the build guide, the handovers,
the learning log, the notebook) or measured (the test run), never typed by hand.
Run at every milestone:

    .venv/bin/python scripts/repo_stats.py

`--no-tests` skips the test run and reports the test count as not measured.
"""

from __future__ import annotations

import argparse
import datetime
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = "<!-- stats:start -->"
END = "<!-- stats:end -->"

_GUIDE_ROW = re.compile(r"^\| (P\d-C\w+)(?: to (P\d-C\w+))? (.+?) \|", re.MULTILINE)
_PASSES = re.compile(r"\*\*Review passes:\*\* \[(.*?)\]")
_PAIR = re.compile(r"\((\d+), (\d+)\)")


@dataclass(frozen=True)
class Chunk:
    id: str
    title: str
    done: bool
    passes: tuple[int, ...]  # serious (Critical or Important) findings per review pass


def _expand(first: str, last: str | None) -> list[str]:
    """ "P3-C02" to "P3-C06" becomes the five ids in between."""
    if last is None:
        return [first]
    prefix, low = first.rsplit("C", 1)
    high = last.rsplit("C", 1)[1]
    return [f"{prefix}C{n:02d}" for n in range(int(low), int(high) + 1)]


def planned_chunks(guide_text: str) -> list[tuple[str, str]]:
    """(id, title) for every chunk in the build guide's dependency table."""
    chunks = []
    for m in _GUIDE_ROW.finditer(guide_text):
        ids = _expand(m.group(1), m.group(2))
        for chunk_id in ids:
            title = m.group(3)
            if len(ids) > 1:
                title = re.sub(
                    r"(?:es)? \d+ to \d+$", f" {ids.index(chunk_id) + 1}", title
                )
            chunks.append((chunk_id, title))
    return chunks


def read_handover(text: str) -> tuple[bool, tuple[int, ...]]:
    """(complete?, serious findings per review pass) from one handover file."""
    done = "## Status: Complete" in text
    m = _PASSES.search(text)
    passes = tuple(int(n) for _, n in _PAIR.findall(m.group(1))) if m else ()
    return done, passes


def collect(root: Path) -> list[Chunk]:
    guide = (root / "specs" / "implementation-guide.md").read_text(encoding="utf-8")
    chunks = []
    for chunk_id, title in planned_chunks(guide):
        path = root / "build" / "handovers" / f"{chunk_id}.md"
        done, passes = (
            read_handover(path.read_text(encoding="utf-8"))
            if path.exists()
            else (False, ())
        )
        chunks.append(Chunk(chunk_id, title, done, passes))
    return chunks


def run_tests(root: Path) -> str:
    """The test result as measured, such as "201 passing" or "199 passing, 2 failing"."""
    out = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-o",
            "addopts=",
            "-p",
            "no:cacheprovider",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    counts = {
        word: int(n) for n, word in re.findall(r"(\d+) (passed|failed|error)", out)
    }
    if not counts:
        return "not measured (the test run produced no summary)"
    text = f"{counts.get('passed', 0)} passing"
    bad = counts.get("failed", 0) + counts.get("error", 0)
    return text + (f", {bad} failing" if bad else "")


def _phases(chunks: list[Chunk]) -> str:
    phases: dict[str, list[bool]] = {}
    for c in chunks:
        phases.setdefault(c.id[:2], []).append(c.done)
    complete = [p for p, flags in phases.items() if all(flags)]
    return f"{len(complete)} of {len(phases)} phases complete"


def render(chunks: list[Chunk], tests: str, root: Path, today: datetime.date) -> str:
    done = [c for c in chunks if c.done]
    passes = sum(len(c.passes) for c in done)
    serious = sum(sum(c.passes) for c in done)
    learning = sorted(
        p for p in (root / "docs" / "learning").glob("[0-9][0-9][0-9]-*.md")
    )
    films = list((root / "docs" / "learning").glob("*.html"))
    runs = [p for p in (root / "notebook").glob("*.md") if p.name != "README.md"]
    commits = (
        subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        or "not counted"
    )

    lines = [
        START,
        "## Progress at a glance",
        "",
        (
            f"*Counted from the repository by `scripts/repo_stats.py` on {today.isoformat()};"
            " nothing in this block is typed by hand.*"
        ),
        "",
        "| Measure | Now |",
        "|---|---|",
        f"| Build chunks done | {len(done)} of {len(chunks)} ({_phases(chunks)}) |",
        f"| Automated tests | {tests} |",
        (
            f"| Independent review passes | {passes} passes over {len(done)} chunks;"
            f" {serious} serious findings caught and fixed before commit |"
        ),
        f"| Learning entries | {len(learning)}"
        + (f", plus {len(films)} film" if films else "")
        + " |",
        f"| Training runs logged | {len(runs)} |",
        f"| Commits | {commits} |",
        "",
        (
            "**Build log.** Each chunk is reviewed by an independent reviewer until a pass finds"
            " nothing serious; the numbers show the serious findings each pass found."
        ),
        "",
        "| Chunk | What it builds | Review passes | Record |",
        "|---|---|---|---|",
    ]
    for c in chunks:
        if c.done:
            trail = " → ".join(str(n) for n in c.passes) or "not recorded"
            record = f"[handover](build/handovers/{c.id}.md)"
        else:
            trail, record = "not started", ""
        lines.append(f"| {c.id} | {c.title} | {trail} | {record} |")
    lines.append(END)
    return "\n".join(lines)


def replace_block(readme: str, block: str) -> str:
    if START not in readme or END not in readme:
        raise ValueError(f"README.md needs the markers {START} and {END}")
    head, rest = readme.split(START, 1)
    tail = rest.split(END, 1)[1]
    return head + block + tail


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-tests", action="store_true", help="skip the test run")
    args = parser.parse_args(argv)
    tests = "not measured (skipped)" if args.no_tests else run_tests(ROOT)
    readme_path = ROOT / "README.md"
    block = render(collect(ROOT), tests, ROOT, datetime.date.today())
    readme_path.write_text(
        replace_block(readme_path.read_text(encoding="utf-8"), block), encoding="utf-8"
    )
    print(block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
