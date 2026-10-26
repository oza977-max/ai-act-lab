"""Run candidate models on this Mac (specs/data-and-evaluation.md, ADR-007 to ADR-009).

Commands:
    python -m lab.bakeoff smoke --model <slug>    one sample case, prints time and memory

Each model runs in a child process, so running out of memory ends only the
child; the parent records why. The full bake-off run arrives in P4-C02.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from lab.records import parse_answer

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "data" / "models.toml"
MEMORY_LIMIT_GB = 6.5
MAX_TOKENS = 400
OVER_MEMORY_EXIT = 3
SLUG_PATTERN = re.compile(r"^[a-z0-9._-]+$")
REVISION_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_SUFFIXES = (".py", ".bin", ".pt", ".pth", ".pkl", ".pickle")
REQUIRED_KEYS = (
    "repo", "revision", "original_model", "card_url", "licence", "parameters",
    "quantisation", "developer", "jurisdiction", "training_data_disclosure",
    "converted_with", "checked_on", "template", "weights",
)  # fmt: skip
RESULT_KEYS = ("load_seconds", "answer_seconds", "peak_memory_gb")

# Interim prompt for the smoke test only; the real prompt is generated from the
# guideline in P2-C02 (ADR-006).
SMOKE_PROMPT = (
    "Classify the AI system below under the EU AI Act. Answer with one JSON object "
    "and nothing else, with the fields: tier (one of prohibited, high-risk, "
    "transparency-only, minimal, out-of-scope, needs-human-review), route, "
    "annex_iii_area, annex_iii_point, annex_i_legislation, art50_flag, articles, "
    "review_reason, reason (one sentence).\n\n"
    "<<<CASE\nA fictional retailer uses a model to sort incoming customer emails into "
    "billing, delivery and returns queues. Staff read every email.\nCASE>>>"
)


class RegistryError(Exception):
    """The model registry is malformed or does not list the requested model."""


class BuildCheckError(Exception):
    """A downloaded model build fails the supply-chain checks (ADR-008)."""


@dataclass(frozen=True)
class ModelEntry:
    slug: str
    repo: str
    revision: str
    weights: dict = field(default_factory=dict)
    template: dict = field(default_factory=dict)


class Registry(dict):
    """Model entries keyed by slug, remembering which file they came from."""

    def __init__(self, path: Path):
        super().__init__()
        self.path = path

    def get_entry(self, slug: str) -> ModelEntry:
        if slug not in self:
            raise RegistryError(
                f"{self.path}: model {slug!r} is not in the registry ({', '.join(self)})"
            )
        return self[slug]


def load_registry(path: Path = REGISTRY_PATH) -> Registry:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise RegistryError(f"{path}: cannot read ({exc})") from exc
    registry = Registry(path)
    for slug, values in data.get("models", {}).items():
        registry[slug] = _entry_from_toml(path, slug, values)
    return registry


def _entry_from_toml(path: Path, slug: str, values: dict) -> ModelEntry:
    if not SLUG_PATTERN.match(slug):
        raise RegistryError(
            f"{path}: model key {slug!r} must match {SLUG_PATTERN.pattern}"
        )
    missing = [key for key in REQUIRED_KEYS if not values.get(key)]
    if missing:
        raise RegistryError(f"{path}: model {slug} is missing {', '.join(missing)}")
    if not REVISION_PATTERN.match(str(values["revision"])):
        raise RegistryError(
            f"{path}: model {slug} revision must be a full 40-character commit hash"
        )
    bad = [
        name
        for name, h in values["weights"].items()
        if not SHA256_PATTERN.match(str(h))
    ]
    if bad:
        raise RegistryError(
            f"{path}: model {slug} weights hash for {', '.join(bad)} is not 64 hex characters"
        )
    return ModelEntry(
        slug=slug,
        repo=values["repo"],
        revision=values["revision"],
        weights=dict(values["weights"]),
        template=dict(values["template"]),
    )


def snapshot_files(root: Path) -> list[str]:
    """Every file in a downloaded build, including subfolders, as relative paths."""
    return sorted(
        p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
    )


def check_build_files(names: list[str]) -> None:
    """Safetensors weights only; no code or pickle files anywhere in the build (ADR-008)."""
    bad = [n for n in names if n.lower().endswith(FORBIDDEN_SUFFIXES)]
    if bad:
        raise BuildCheckError(f"build contains code or pickle files: {', '.join(bad)}")
    if not any(n.endswith(".safetensors") for n in names):
        raise BuildCheckError("build has no .safetensors weights")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_weights(root: Path, registered: dict[str, str]) -> None:
    """Every weights file must be registered, and every registered hash must match."""
    present = {n for n in snapshot_files(root) if n.endswith(".safetensors")}
    unregistered = sorted(present - set(registered))
    absent = sorted(set(registered) - present)
    if unregistered or absent:
        raise BuildCheckError(
            "weights files differ from the registry: "
            f"unregistered {unregistered or 'none'}, missing {absent or 'none'}"
        )
    for name in sorted(present):
        if _sha256(root / name) != registered[name]:
            raise BuildCheckError(f"{name}: hash differs from the registry")


class Generator(Protocol):
    def load(self) -> None: ...
    def generate(self, prompt: str) -> str: ...
    def peak_memory_gb(self) -> float: ...


class MlxGenerator:
    """A pinned, checked MLX model: greedy, thinking off, one user message."""

    def __init__(self, entry: ModelEntry):
        self.entry = entry
        self.template = entry.template
        self.model = None
        self.tokenizer = None

    def load(self) -> None:
        import mlx.core as mx
        from huggingface_hub import snapshot_download
        from mlx_lm import load

        mx.reset_peak_memory()
        path = Path(snapshot_download(self.entry.repo, revision=self.entry.revision))
        check_build_files(snapshot_files(path))
        verify_weights(path, self.entry.weights)
        self.model, self.tokenizer = load(str(path), trust_remote_code=False)

    def render(self, prompt: str) -> str:
        return self.tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            add_generation_prompt=True,
            tokenize=False,
            **self.template,
        )

    def generate(self, prompt: str) -> str:
        from mlx_lm import generate
        from mlx_lm.sample_utils import make_sampler

        return generate(
            self.model,
            self.tokenizer,
            self.render(prompt),
            max_tokens=MAX_TOKENS,
            sampler=make_sampler(temp=0.0),
        )

    def peak_memory_gb(self) -> float:
        import mlx.core as mx

        return mx.get_peak_memory() / 1e9


def _printable(text: str, limit: int = 600) -> str:
    """Untrusted text (model output, library errors): drop control characters before printing."""
    cleaned = "".join(c for c in text if c in "\n\t" or c.isprintable())
    return cleaned[:limit] + ("…" if len(cleaned) > limit else "")


@dataclass
class ChildOutcome:
    ok: bool
    result: dict = field(default_factory=dict)
    reason: str = ""


def run_child(command: list[str]) -> ChildOutcome:
    """Run a model in a child process; turn every ending into a recorded outcome."""
    proc = subprocess.run(
        command, check=False, capture_output=True, text=True, cwd=ROOT
    )
    last_line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    try:
        result = json.loads(last_line) if last_line else {}
    except json.JSONDecodeError:
        result = {}
    if not isinstance(result, dict):
        result = {}
    if proc.returncode == 0:
        if all(key in result for key in RESULT_KEYS):
            return ChildOutcome(ok=True, result=result)
        return ChildOutcome(
            ok=False, reason="the model process finished but printed no result"
        )
    if proc.returncode < 0:
        signal_number = -proc.returncode
        cause = " (SIGKILL, likely out of memory)" if signal_number == 9 else ""
        return ChildOutcome(ok=False, reason=f"killed by signal {signal_number}{cause}")
    if proc.returncode == OVER_MEMORY_EXIT:
        peak = result.get("peak_memory_gb", "unknown")
        return ChildOutcome(
            ok=False,
            result=result,
            reason=f"peak memory {peak} GB above the {MEMORY_LIMIT_GB} GB limit",
        )
    tail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "no message"
    return ChildOutcome(
        ok=False,
        reason=f"exited with status {proc.returncode}: {_printable(tail, 300)}",
    )


def _child_smoke(slug: str) -> int:
    """Child side: load, answer one case, print one JSON line."""
    generator = MlxGenerator(load_registry().get_entry(slug))
    start = time.perf_counter()
    generator.load()
    loaded = time.perf_counter()
    raw = generator.generate(SMOKE_PROMPT)
    done = time.perf_counter()
    peak = round(generator.peak_memory_gb(), 2)
    result = {
        "load_seconds": round(loaded - start, 2),
        "answer_seconds": round(done - loaded, 2),
        "peak_memory_gb": peak,
        "raw": raw,
    }
    print(json.dumps(result))
    return OVER_MEMORY_EXIT if peak > MEMORY_LIMIT_GB else 0


def smoke(slug: str) -> int:
    load_registry().get_entry(
        slug
    )  # fail fast on an unknown slug, before the child starts
    outcome = run_child(
        [sys.executable, "-m", "lab.bakeoff", "_child-smoke", "--model", slug]
    )
    if not outcome.ok:
        print(f"Smoke test for {slug}: EXCLUDED — {outcome.reason}")
        return 1
    result = outcome.result
    _, status = parse_answer(result.get("raw"))
    print(f"Model: {slug}")
    print(
        f"Load seconds: {result['load_seconds']} (checks, hash and loading the weights)"
    )
    print(
        f"Answer seconds: {result['answer_seconds']} (one answer, up to {MAX_TOKENS} tokens)"
    )
    print(f"Peak memory: {result['peak_memory_gb']} GB (limit {MEMORY_LIMIT_GB} GB)")
    print(f"Answer readable as a record: {'yes' if status == 'ok' else 'no'}")
    print("Answer:")
    print(_printable(result.get("raw") or ""))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run candidate models on this Mac.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("smoke", "_child-smoke"):
        sub.add_parser(name).add_argument("--model", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "_child-smoke":
            return _child_smoke(args.model)
        return smoke(args.model)
    except (RegistryError, BuildCheckError) as exc:
        print(f"bakeoff: {_printable(str(exc), 300)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
