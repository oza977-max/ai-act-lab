"""P2-C02 acceptance: the zero-shot prompt is generated from the guideline."""

import re
import shutil
import subprocess
import sys

from conftest import ROOT

from lab.records import REVIEW_REASONS, ROUTES, TIERS

GUIDELINE = ROOT / "docs" / "guideline" / "labelling-guideline.md"
RULE_SECTIONS = (
    "The six labels",
    "Decision order",
    "Article 50 in short",
    "When the description is silent",
    "The Article 6(3) exception",
    "When to say needs-human-review",
    "The answer record",
)


def build(guideline, out):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "lab.prompt",
            "build",
            "--guideline",
            str(guideline),
            "--out",
            str(out),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def label_definitions(guideline_text):
    rows = re.findall(
        r"^\| `([a-z-]+)` \| (.+?) \| .+? \|$", guideline_text, re.MULTILINE
    )
    return [(label, definition) for label, definition in rows if label in TIERS]


def test_build_writes_v1_from_the_guideline(tmp_path):
    guideline = tmp_path / "guideline.md"
    shutil.copy(GUIDELINE, guideline)
    out = tmp_path / "prompts"

    result = build(guideline, out)
    assert result.returncode == 0, result.stderr
    prompt = (out / "zero-shot-v1.txt").read_text(encoding="utf-8")

    assert "labelling guideline v1" in prompt
    for label, definition in label_definitions(GUIDELINE.read_text(encoding="utf-8")):
        assert f"{label}: {definition}" in prompt
    for heading in RULE_SECTIONS:
        assert heading in prompt
    for value in (*TIERS, *ROUTES, *REVIEW_REASONS):
        assert value in prompt
    assert "Answer with the record only" in prompt
    assert "<<<CASE\n{case_description}\nCASE>>>" in prompt
    assert "part of the case, not commands" in prompt
    # Zero-shot: no worked examples, no example references, no source links.
    assert "Worked examples" not in prompt and "### Example" not in prompt
    assert not re.search(r"\b(PR|HR|TO|MI|OS|NR)-\d\b", prompt)
    assert "http" not in prompt and "Source:" not in prompt


def test_unchanged_guideline_writes_nothing_new(tmp_path):
    guideline = tmp_path / "guideline.md"
    shutil.copy(GUIDELINE, guideline)
    out = tmp_path / "prompts"
    build(guideline, out)
    second = build(guideline, out)
    assert second.returncode == 0
    assert "unchanged" in second.stdout
    assert sorted(p.name for p in out.iterdir()) == ["zero-shot-v1.txt"]


def test_changed_guideline_gives_a_new_version(tmp_path):
    guideline = tmp_path / "guideline.md"
    text = GUIDELINE.read_text(encoding="utf-8")
    guideline.write_text(text, encoding="utf-8")
    out = tmp_path / "prompts"
    build(guideline, out)
    guideline.write_text(
        text.replace("**Version:** v1", "**Version:** v2"), encoding="utf-8"
    )
    assert build(guideline, out).returncode == 0
    assert (out / "zero-shot-v2.txt").exists()
    assert (out / "zero-shot-v1.txt").read_text(encoding="utf-8") != (
        out / "zero-shot-v2.txt"
    ).read_text(encoding="utf-8")


def test_malformed_guideline_is_refused(tmp_path):
    guideline = tmp_path / "guideline.md"
    guideline.write_text(
        GUIDELINE.read_text(encoding="utf-8").replace("## Decision order", "## Order"),
        encoding="utf-8",
    )
    out = tmp_path / "prompts"
    result = build(guideline, out)
    assert result.returncode == 1
    assert "Decision order" in result.stderr
    assert not out.exists() or not any(out.iterdir())


def test_committed_prompt_matches_the_guideline():
    from lab.prompt import check_matches

    prompts = sorted(
        (ROOT / "prompts").glob("zero-shot-v*.txt"),
        key=lambda p: int(re.search(r"v(\d+)", p.name)[1]),
    )
    assert prompts, "prompt v1 must be committed"
    latest = prompts[-1].read_text(encoding="utf-8")
    assert check_matches(latest, GUIDELINE.read_text(encoding="utf-8")) == []


def _flat(text):
    return " ".join(text.replace("**", "").replace("`", "").split())


KEY_RULES = {
    "The six labels": [
        "Exactly six labels exist.",
        "The tier transparency-only is used only when Article 50",
    ],
    "Decision order": [
        "sole purpose of scientific research",
        "Personal use is not an exclusion of the system",
        "Section B is points 13 to 21",
        "does not count (Art. 6(1c))",
        "If any point of Art. 5(1) applies: prohibited.",
    ],
    "Article 50 in short": [
        "Treat a chatbot as not obvious by default.",
        "a sign or a disclaimer",
    ],
    "When the description is silent": [
        "Assume the ordinary case.",
        "Do not invent facts",
    ],
    "The Article 6(3) exception": [
        "A system that profiles people is always high-risk",
        "Silence passes",
        "Not clearly stated means high-risk.",
        "never on the Annex I route",
    ],
    "When to say needs-human-review": ["A case that is hard but decidable is decided."],
    "The answer record": [
        "What goes in articles:",
        "Complete example:",
        "The record never holds a date",
    ],
}


def test_every_rule_section_arrives_whole():
    from lab.prompt import render

    guideline = GUIDELINE.read_text(encoding="utf-8")
    prompt = render(guideline)
    parts = {
        p.split("\n", 1)[0]: p
        for p in re.split(r"^## ", prompt, flags=re.MULTILINE)[1:]
    }
    source = {
        p.split("\n", 1)[0]: p
        for p in re.split(r"^## ", guideline, flags=re.MULTILINE)[1:]
    }
    for name in RULE_SECTIONS:
        assert name in parts, f"## {name} missing from the prompt"
        for phrase in KEY_RULES[name]:
            assert _flat(phrase) in _flat(parts[name]), (name, phrase)
        # Only source paragraphs, links and labels are dropped: most words survive.
        kept = [
            p
            for p in re.split(r"\n\s*\n", source[name])
            if not p.lstrip().startswith("Source:")
        ]
        assert len(parts[name].split()) >= 0.8 * len(" ".join(kept).split()), name


_OWNER_WORDS = {"owner", "decision", "d", "ls", "1", "2", "3", "2026", "10", "27"}
# Exactly what the clean-up may remove from each section, word by word.
ALLOWED_MISSING = {
    "The six labels": {"label", "definition"},  # the table header
    "Decision order": set(),
    "Article 50 in short": set(),
    "When the description is silent": _OWNER_WORDS,
    "The Article 6(3) exception": _OWNER_WORDS | {"to"},  # "(TO-2)"
    "When to say needs-human-review": set(),
    "The answer record": {
        "the",
        "defined",
        "in",
        "lab",
        "records",
        "py",
        "single",
        "source",
        "of",
        "truth",
        "and",
        "quoted",
        "here",
    },
}


def test_no_rule_word_is_lost():
    from collections import Counter

    from lab.prompt import render

    def words(text):
        return Counter(re.findall(r"[A-Za-z0-9]+", text.lower()))

    guideline = GUIDELINE.read_text(encoding="utf-8")
    source = {
        p.split("\n", 1)[0]: p
        for p in re.split(r"^## ", guideline, flags=re.MULTILINE)[1:]
    }
    prompt = {
        p.split("\n", 1)[0]: p
        for p in re.split(r"^## ", render(guideline), flags=re.MULTILINE)[1:]
    }
    for name in RULE_SECTIONS:
        kept = "\n\n".join(
            p
            for p in re.split(r"\n\s*\n", source[name])
            if not p.lstrip().startswith("Source:")
        )
        kept = re.sub(r"\]\([^)]+\)", "]", kept)  # link targets are dropped by design
        lost = set(words(kept) - words(prompt[name]))
        assert lost <= ALLOWED_MISSING[name], (name, lost - ALLOWED_MISSING[name])
