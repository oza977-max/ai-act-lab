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
FORBIDDEN_SUFFIXES = (".py", ".bin", ".pt", ".pth", ".pkl", ".pickle")
REQUIRED_KEYS = (
    "repo", "revision", "weights_sha256", "original_model", "card_url", "licence",
    "parameters", "quantisation", "developer", "jurisdiction", "training_data_disclosure",
    "converted_with", "checked_on",
)  # fmt: skip

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
    weights_sha256: str
    template: dict = field(default_factory=dict)


class Registry(dict):
    def get_entry(self, slug: str) -> ModelEntry:
        if slug not in self:
            raise RegistryError(
                f"model {slug!r} is not in the registry ({', '.join(self)})"
            )
        return self[slug]


def load_registry(path: Path = REGISTRY_PATH) -> Registry:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise RegistryError(f"{path}: cannot read ({exc})") from exc
    registry = Registry()
    for slug, values in data.get("models", {}).items():
        if not SLUG_PATTERN.match(slug):
            raise RegistryError(
                f"{path}: model key {slug!r} must match {SLUG_PATTERN.pattern}"
            )
        missing = [k for k in REQUIRED_KEYS if not values.get(k)]
        if missing:
            raise RegistryError(f"{path}: model {slug} is missing {', '.join(missing)}")
        registry[slug] = ModelEntry(
            slug=slug,
            repo=values["repo"],
            revision=values["revision"],
            weights_sha256=values["weights_sha256"],
            template=dict(values.get("template", {})),
        )
    return registry


def check_build_files(names: list[str]) -> None:
    """Safetensors weights only; no code or pickle files (ADR-008)."""
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
        check_build_files([p.name for p in path.iterdir()])
        weights = path / "model.safetensors"
        if weights.exists() and _sha256(weights) != self.entry.weights_sha256:
            raise BuildCheckError(
                f"{self.entry.slug}: weights hash differs from the registry"
            )
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
    if proc.returncode == 0:
        return ChildOutcome(ok=True, result=result)
    if proc.returncode < 0:
        return ChildOutcome(
            ok=False,
            reason=f"killed by signal {-proc.returncode} (likely out of memory)",
        )
    if proc.returncode == OVER_MEMORY_EXIT:
        peak = result.get("peak_memory_gb", "unknown")
        return ChildOutcome(
            ok=False,
            result=result,
            reason=f"peak memory {peak} GB above the {MEMORY_LIMIT_GB} GB limit",
        )
    tail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "no message"
    return ChildOutcome(
        ok=False, reason=f"exited with status {proc.returncode}: {tail}"
    )


def _child_smoke(slug: str) -> int:
    """Child side: load, answer one case, print one JSON line."""
    generator = MlxGenerator(load_registry().get_entry(slug))
    start = time.perf_counter()
    generator.load()
    raw = generator.generate(SMOKE_PROMPT)
    seconds = round(time.perf_counter() - start, 2)
    peak = round(generator.peak_memory_gb(), 2)
    print(json.dumps({"seconds": seconds, "peak_memory_gb": peak, "raw": raw}))
    return OVER_MEMORY_EXIT if peak > MEMORY_LIMIT_GB else 0


def _printable(text: str, limit: int = 600) -> str:
    """Model text is untrusted: drop control characters before printing it."""
    cleaned = "".join(c for c in text if c in "\n\t" or c.isprintable())
    return cleaned[:limit] + ("…" if len(cleaned) > limit else "")


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
    print(f"Seconds: {result['seconds']} (load plus one answer)")
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
        print(f"bakeoff: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
