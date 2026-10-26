# AI Act Lab — Cross-Cutting Spec (Slice 1)

**Date:** 2026-10-26
**Status:** approved by the owner, 2026-10-26; revised after design review 001
**Scope:** conventions every slice-1 chunk follows. Requirements: all of `requirements/requirements.md` slice 1.

*The shared rules: tools, folders, file formats, the one answer record everything agrees on, how errors are handled, and how tests are run.*

## Expert Panel

| Expert | Work | Role in This Document |
|---|---|---|
| Michael Keeling | *Design It!* | Decisions recorded as ADRs |
| Andrew Hunt & David Thomas | *The Pragmatic Programmer* | One source of truth per fact; tracer bullet first |
| Steve McConnell | *Code Complete* (2nd ed.) | Fail loudly on bad input |
| Robert C. Martin | *Clean Code* | No swallowed errors |
| Luciano Ramalho | *Fluent Python* (2nd ed.) | Plain dataclasses, standard library first |
| Kent Beck | *Test-Driven Development* | Tests before code, in every chunk |
| Sebastian Raschka | *Build a Large Language Model (From Scratch)* | Deterministic generation for evaluation |

## ADR-001: Plain Python scripts and files, no service

**Context.** Slice 1 is one person on one laptop: drafting, labelling, a lookup and an evaluation. No users, no network service (constraints; BO-3 timing on this Mac).
**Options.** (1) Python scripts with files in the repository; (2) a small web app with a database; (3) notebooks.
**Decision.** Option 1. Each task is one command the owner can run and read.
**Consequences.** Everything is diffable in git; datasets and results are committed (house rule). A local page is a later slice (D-13).

## ADR-002: Python 3.13 in one project virtual environment, pinned versions

**Context.** House rule: one virtual environment, pinned versions. This Mac has Python 3.13 (Homebrew) and 3.11.
**Decision.** Python 3.13 in `.venv/` at the repository root; dependencies pinned to exact versions in `requirements.txt`. Fallback to 3.11 if the walking skeleton finds MLX unsupported on 3.13; the fallback is recorded as a decision.
**Dependencies (slice 1).** `mlx-lm` (model loading, 4-bit generation on Apple Silicon; brings `mlx`), `pytest` (tests). Nothing else: statistics, CSV, JSON and TOML use the standard library. Versions are chosen and pinned in the walking-skeleton chunk.
**Consequences.** `.venv/` is git-ignored (already). Model weights are cached outside the repository and never committed.

## ADR-003: File formats, chosen for the reader

| Data | Format | Why |
|---|---|---|
| Labelling guideline | Markdown, `docs/guideline/labelling-guideline.md`, version in its header | The owner reads and edits it |
| Gold set (source of truth) | JSON Lines, one case per line, `data/gold/gold-v{N}.jsonl` | One case per line diffs cleanly |
| Gold review sheet | CSV, `data/gold/review/batch-{NN}.csv`, opened in Numbers or Excel | Owner's choice, 2026-10-26 |
| Dates-and-duties table | TOML, `data/dates/dates-table.toml` | Readable by a person, parsed by the standard library |
| Valid-article table | JSON, `data/articles.json` | Fixed list; EV-4 |
| Prompt | Text, `prompts/zero-shot-v{N}.txt` | Recorded verbatim (BO-2) |
| Model registry | TOML, `data/models.toml` | Slug, build repository and pinned revision, file hashes, card URL, licence, parameters, developer, jurisdiction, training-data disclosure, template settings |
| Model outputs | JSON Lines, `results/bakeoff/{model-slug}/outputs.jsonl` | One raw answer per gold case |
| Run metadata | JSON, `results/bakeoff/{model-slug}/run.json` | Model, build revision, prompt version, guideline version, gold-set version, settings, peak memory, mean seconds, run date |
| Evaluation metrics | JSON, `results/bakeoff/{model-slug}/metrics.json` | Every measure with its interval; read by `compare` |
| Gold metadata | JSON, `data/gold/gold-v{N}.meta.json` | Build date, file hash, guideline version |
| Re-label records | JSON and CSV, `data/gold/relabel/` | `record.json` (seed, date, ids), `sheet.csv`, `resolutions.csv` |
| Decisions log | Markdown, `docs/00-plan.md` (Decisions log section) | Base-model choice and other owner decisions (BO-6) |
| Private name list | Text, `.private/deny-terms.txt`, git-ignored, owner-only | Real names the confidentiality guard must block |
| Reports | Markdown, `results/.../report.md` | Owner reads them; committed |

## Shared contract: the answer record

The single shape that the guideline (LS-9), the gold set (GS), the bake-off (BO) and the evaluation (EV) all use. One source of truth: `lab/records.py` defines it; the guideline quotes it.

| Field | Type | Rule |
|---|---|---|
| `tier` | one of `prohibited`, `high-risk`, `transparency-only`, `minimal`, `out-of-scope`, `needs-human-review` | Required (LS-1) |
| `route` | `annex-iii`, `annex-i` or `null` | Required when tier is high-risk, else null (LS-2) |
| `annex_iii_area` | integer 1 to 8 or `null` | Required when route is annex-iii (LS-2) |
| `annex_iii_point` | string such as `4(a)` or `null` | Required when route is annex-iii (LS-2) |
| `annex_i_legislation` | string or `null` | Required when route is annex-i (LS-2) |
| `art50_flag` | `true` or `false` | Required (LS-3) |
| `articles` | list of strings such as `"Art. 6(2)"` | At least one, except for needs-human-review (LS-4) |
| `review_reason` | `missing-fact`, `conflicting-facts`, `unsettled-law` or `null` | Required when tier is needs-human-review (LS-6) |
| `reason` | string, one sentence, at most 40 words | Required (LS-4) |

No date, deadline or duties field exists (LS-10). Example:

```json
{"tier": "high-risk", "route": "annex-iii", "annex_iii_area": 4, "annex_iii_point": "4(a)",
 "annex_i_legislation": null, "art50_flag": true, "articles": ["Art. 6(2)", "Annex III 4(a)", "Art. 50(1)"],
 "review_reason": null,
 "reason": "The system screens job applicants, an Annex III employment use, and it talks to them directly."}
```

A gold case wraps a record: `id` (`GC-001`…), `description`, `gold` (the record), `draft` (the full proposed record, kept for GS-5), `tags` (from a fixed vocabulary: `boundary`, `art6-3`, `hidden-instruction`, `annex-i`, `area-1` to `area-8`), `guideline_version` (one version per gold set), `owner_decision` (`accept` or `change`; `doubt` must be resolved before build), `never_train` (always `true`).

A model output line, written by the runner: `id`, `raw` (the model's text, verbatim, or `null`), `seconds` (number or `null`), `error` (`null` or `missing`). The runner never parses. A gold case with no output line and a line with `error: "missing"` are treated identically. Only the evaluation parses `raw`, deriving `unreadable` when no valid record can be read (`data-and-evaluation.md`, ADR-005).

## ADR-007: Confidentiality guard

**Context.** The repository is public; history is permanent. No word list can contain the real names that matter (design review T10).
**Decision.** `scripts/confidentiality-check.sh` runs automatically as a git pre-commit hook, installed by `scripts/install-hooks.sh`. It scans added lines and the names of staged files; blocks spreadsheet files (`.xlsx`, `.numbers`); blocks local paths, email addresses and employer-style wording; and blocks every term in the owner's private, git-ignored `.private/deny-terms.txt`. Lines stating the confidentiality rule are exempt only in `CLAUDE.md`, `README.md`, `docs/` and `specs/`, never in `data/`, `results/` or `notebook/`. Data files are staged by path.
**Consequences.** A safety net, not a guarantee: the owner still reads every gold batch for real names (GS-2).

## ADR-008: Model supply chain

**Context.** Candidate builds are third-party downloads (design review T11).
**Decision.** Weights only in safetensors format; never load remote code; `data/models.toml` records the repository, the exact revision and file hashes, and the runner loads that revision only. All Python dependencies, including transitive ones, are pinned in `requirements.txt`.
**Consequences.** A build that ships code files or pickle weights is excluded with the reason recorded (BO-4).

## ADR-009: Thinking modes off

**Context.** Some candidates (Qwen3.5) may reason at length before answering and exhaust the 400-token budget, scoring as format failures for a reason unrelated to the task.
**Decision.** Owner's choice, 2026-10-26: thinking modes off for every model, through each model's chat-template setting, recorded per model in `models.toml` and per run in `run.json`. The whole prompt is one user message.
**Consequences.** Same conditions for all candidates (BO-2).

## Errors: fail loudly, never quietly drop

- Invalid input files stop the command with a message naming the file, line and rule broken (McConnell). No partial results written.
- An unreadable or missing model answer is data, not an error: it is counted as wrong on every measure and reported separately (EV-5).
- No bare `except` that hides a failure (Martin).

## Determinism

- Model generation is greedy (temperature 0) with a 400-token cap and thinking modes off for every model (ADR-009). Repeatability is measured, not assumed: BO-7 compares two runs label by label.
- Random sampling (the re-label sample, bootstrap intervals) uses a fixed, recorded seed (EV-9, GS-7).
- Reports carry model, prompt version, guideline version, gold-set version and the run date from `run.json`, never the clock at report time, so a re-run on the same inputs gives an identical report (EV-9). Timing appears only in `run.json` and the comparison.

## Repository layout

```
lab/            Python package: records, articles, stats, prompt, gold, relabel, dates, bakeoff, compare, evaluate
tests/          pytest; fixtures/ holds the 10-case hand-counted set (EV tests)
data/           gold/, dates/, articles.json
docs/guideline/ labelling guideline
prompts/        zero-shot prompt versions
results/        bake-off outputs and reports
scripts/        confidentiality check and git hook installer
docs/learning/  owner's learning log, one entry per chunk
notebook/       one entry per model run
.private/       git-ignored; the owner's private name list
```

## Testing conventions

- Tests come before code in every chunk; test names follow the TC IDs (for example `test_tc_ev_2_01_answered_case_accuracy`).
- Every chunk's done-criteria include a learning-log entry (LG-2).
- Run with `.venv/bin/python -m pytest`. Every chunk ends green.
- The 10-case fixture in `tests/fixtures/eval-10/` is the evaluation's ground truth (TC-EV-1-01 to TC-EV-10-01).

## Owner-facing conventions

- Every command the owner runs is a single line, given exactly, with expected output and time (LG-1).
- Commands are `python -m lab.<tool>` from the repository root with the virtual environment active.


## Changelog

| Date | Change | Reason | Author |
|---|---|---|---|
| 2026-10-26 | Output line no longer carries a parsed record; new run, metrics, gold-meta, re-label and model-registry files; full draft record and tag vocabulary in the gold case; report date from the run; ADR-007 confidentiality guard, ADR-008 model supply chain, ADR-009 thinking off; layout adds learning log, notebook and private folder | Design review 001, themes T2, T3, T4, T9, T10, T11, T14; owner decisions on thinking modes and the private name list | owner/AI |

---

*Developed using the Grounded Vibe Methodology*
