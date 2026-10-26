# AI Act Lab — Implementation Guide (Slice 1)

**Date:** 2026-10-26
**Status:** approved by the owner, 2026-10-26; revised after design review 001
**Inputs:** `specs/cross-cutting.md`, `specs/data-and-evaluation.md`, `test-cases/test-cases.md`

*The build order: four phases, seventeen chunks, each small enough to finish and test in one sitting. Phase numbering starts at P1: no earlier build exists in this repository.*

## Expert Panel

| Expert | Work | Role in This Document |
|---|---|---|
| Mike Cohn | *Agile Estimating and Planning*; *User Stories Applied* | Small, vertical, testable chunks; spikes for uncertainty |
| Andrew Hunt & David Thomas | *The Pragmatic Programmer* | A tracer bullet through the riskiest seam first |
| Kent Beck | *Test-Driven Development* | Tests inside every chunk, never a separate test chunk |
| Michael Feathers | *Working Effectively with Legacy Code* | Every module has a consumer that demanded it (wiring matrix) |

## Dependency Network

| Chunk | Depends on | Enables | Parallel with |
|---|---|---|---|
| P1-C01 Skeleton, guard hook, first evaluation | none | all | none |
| P1-C02 Model smoke test (tracer) | P1-C01 | P4-C00, P4-C02 | P1-C03 |
| P1-C03 Record rules | P1-C01 | P1-C04, P3-C01, P4-C02 | P1-C02 |
| P1-C04 Full evaluation | P1-C03 | P4-C03 | P2-C01 |
| P2-C01 Guideline v1 | P1-C03 | P2-C02, P2-C03, P3-C02 | P1-C04 |
| P2-C02 Prompt build | P2-C01 | P4-C02 | P2-C03 |
| P2-C03 Dates table | P2-C01 | none in slice 1 | P3 chunks |
| P3-C01 Gold tooling | P1-C03 | P3-C02 | P2-C02, P2-C03 |
| P3-C02 to P3-C06 Gold batches 1 to 5 | P2-C01, P3-C01, then each previous batch | P3-C07, P4-C03 | P4-C00 to P4-C02 |
| P3-C07 Blind re-label | P3-C06 plus 2 days | none | P4 chunks |
| P4-C00 Spike: candidate builds | P1-C02 | P4-C02 | P2, P3 chunks |
| P4-C01 Licence criteria | none | P4-C04 | anything before P4-C03 |
| P4-C02 Bake-off runner | P1-C03, P2-C02, P4-C00 | P4-C03 | P3 batches |
| P4-C03 Owner runs the bake-off | P1-C04, P3-C06, P4-C02 | P4-C04 | P3-C07 |
| P4-C04 Comparison and choice | P4-C01, P4-C03 | P4-C05 | none |
| P4-C05 End-to-end closure | P4-C04 | slice 2 | none |

```
Track A (code):   P1-C01 ─> P1-C03 ─> P1-C04 ───────────────────────────────┐
                     ├─> P1-C02 (model smoke) ─> P4-C00 ─> P4-C02 ───────────┤
                     │        P1-C03 ─> P3-C01 ─┐                            ├─> P4-C03 ─> P4-C04 ─> P4-C05
Track B (owner):     └─> P2-C01 ─> P2-C02       └─> P3-C02..C06 (5 batches) ─┘        ↑
                            └─> P2-C03 (dates)        └─ +2 days ─> P3-C07         P4-C01
```

**Critical path:** P1-C01 → P1-C03 → P2-C01 → P3-C02 to P3-C06 → P4-C03 → P4-C04 → P4-C05. The five gold batches (3 to 6 hours of owner time) are the longest stretch; the re-label waits 2 days and runs alongside the bake-off.

## Wiring matrix

| Entry point | Consumed modules | Wiring chunk | Demanded by |
|---|---|---|---|
| `python -m lab.evaluate` | `lab.records.parse_answer`, `lab.records.validate`, `lab.records.contains_date`, `lab.articles.is_valid`, `lab.articles.article_number`, `lab.stats.wilson`, `lab.stats.paired_bootstrap_diff` | P1-C01, P1-C04 | P1-C01 (TC-EV-1-01, TC-EV-2-01); P1-C04 (TC-EV-3 to TC-EV-10) |
| `python -m lab.bakeoff smoke` | `lab.bakeoff` child-process runner, `data/models.toml` | P1-C02 | P1-C02 (one-case smoke acceptance) |
| `python -m lab.prompt build` | `lab.records` vocabularies and example, guideline file | P2-C02 | P2-C02 (prompt-matches-guideline test) |
| `python -m lab.dates lookup` | `lab.dates.lookup`, `lab.records` vocabularies | P2-C03 | P2-C03 (TC-DT-1-01 to TC-DT-5-01) |
| `python -m lab.gold check` / `build` | `lab.records.validate`, `lab.articles.is_valid` | P3-C01 | P3-C02 (the owner's first batch must be checkable) |
| `python -m lab.relabel sample` / `score` | `lab.stats.cohen_kappa`, `lab.stats.kappa_bootstrap` | P3-C07 | P3-C07 (TC-GS-7-01, TC-GS-7-02, TC-GS-8-01) |
| `python -m lab.bakeoff run` | child-process runner, `data/models.toml`, prompt file, gold file | P4-C02 | P4-C03 (the owner's first real run) |
| `python -m lab.compare` | `metrics.json`, `run.json`, `excluded.md`, `models.toml`, licence criteria | P4-C04 | P4-C04 (TC-BO-1-01, TC-BO-3-01, TC-BO-6-01) |
| git pre-commit hook | `scripts/confidentiality-check.sh`, `.private/deny-terms.txt` | P1-C01 | P1-C01 (TC-GS-2-03: a planted name is blocked) |
| `lab.records` | (shared: evaluate, gold, prompt, dates) | P1-C01, P1-C03 | P1-C01 (TC-EV-5-01 needs unreadable answers detected) |
| `lab.articles` | (shared: evaluate, gold) | P1-C04 | P1-C04 (TC-EV-4-01) |
| `lab.stats` | (shared: evaluate, relabel) | P1-C04 | P1-C04 (TC-EV-6-01, TC-EV-7-01) |

## Build Phases

Every chunk's done-criteria: tests green, a learning-log entry (lesson, recap, check questions; LG-2), and a commit through the guard.

### Phase 1 — Walking skeleton, the evaluation, and a real model

**P1-C01 Skeleton, guard hook, first evaluation (about 1.5 hours).** `.venv` on Python 3.13 (3.11 if MLX will not install, recorded); `requirements.txt` with every dependency pinned; package layout; `.gitignore` additions (`.private/`, weights); the guard upgraded per cross-cutting ADR-007 and installed as a pre-commit hook; the 10-case fixture; minimal `records` and `evaluate` giving tier accuracy and answered-case accuracy. Runnable: `python -m lab.evaluate --gold tests/fixtures/eval-10/gold.jsonl --run tests/fixtures/eval-10/run/` prints 7 of 10 and 6 of 8. Tests: TC-EV-1-01, TC-EV-2-01, TC-EV-2-02, TC-GS-2-03. *Needs owner permission to install packages.*

**P1-C02 Model smoke test (about 1 hour).** The riskiest seam, first: download the smallest candidate (owner permission first, with name, source and size), load it in a child process, apply its chat template with thinking off, generate one answer for one sample case, print seconds and peak memory. Records the pinned generation calls for this `mlx-lm` version.

**P1-C03 Record rules (about 1 hour).** Full `validate`, `parse_answer` per ADR-005, `contains_date`. Tests: TC-LS-2-01 to TC-LS-4-03, TC-LS-9-01, TC-LS-9-02, TC-LS-10-01, TC-EV-8-01.

**P1-C04 Full evaluation (about 2 hours).** `stats`, `articles.json` and `articles`, every measure in the definitions table, `metrics.json`, paired mode with refusal, report header from `run.json`, plain-English summary. Tests: TC-EV-3-01 to TC-EV-10-01 except TC-EV-8-01; known-answer tests for `stats`.

### Phase 2 — Labels, prompt and dates

**P2-C01 Guideline v1 (Claude about 2 hours; owner about 1 hour).** Claude drafts `docs/guideline/labelling-guideline.md`: version and change log in the header; six labels; decision order; two worked examples per label, at least one marked as a boundary case; the narrow review rule with its three reasons; the record specification quoted from `records`; sources with checked dates; draft-guidance warnings; where the gold set lives and that it is never used for training. Owner reviews and approves v1. Checks: TC-LS-1-01, TC-LS-5-01, TC-LS-5-02, TC-LS-6-01, TC-LS-6-02, TC-LS-7-01, TC-LS-8-01, TC-GS-6-01.

**P2-C02 Prompt build (about 45 minutes).** `lab.prompt build`, prompt v1 committed, the prompt-matches-guideline test.

**P2-C03 Dates table (Claude about 1 hour; owner about 30 minutes).** Claude verifies every plan date against the Official Journal and EUR-Lex, records discrepancies, writes the TOML table, builds `dates`. Owner checks and approves. Tests: TC-DT-1-01 to TC-DT-5-01.

### Phase 3 — Gold set

**P3-C01 Gold tooling (about 1.5 hours).** `gold check` and `gold build` per the spec. Tests: TC-GS-1-01, TC-GS-2-01, TC-GS-2-02, TC-GS-3-01, TC-GS-4-01, TC-GS-4-02, TC-GS-5-01, TC-GS-5-02, on small fixture sheets.

**P3-C02 to P3-C06 Gold batches 1 to 5 (owner 40 to 70 minutes each).** For each batch: Claude drafts 20 cases to the GS-1 spread; the owner judges them in Numbers; `gold check` must pass; commit by path. P3-C06 ends with `gold build`.

**P3-C07 Blind re-label (owner about 45 minutes, at least 2 days after P3-C06).** `relabel sample`, the owner labels 20 blind, `relabel score`, disagreements settled into `resolutions.csv` and, if needed, guideline v2 (with a new gold version). Tests: TC-GS-7-01, TC-GS-7-02, TC-GS-8-01.

### Phase 4 — Bake-off

**P4-C00 Spike: candidate builds (about 1 hour; knowledge, not code).** For each candidate: find the 4-bit MLX build, check it against the original model card (size, licence) and against ADR-008 (safetensors only, no code files); record repository, revision, hashes, developer, jurisdiction, training-data disclosure and template settings in `models.toml`; smoke-test that it loads under 6.5 GB. *Each download needs the owner's permission, with name, source and size stated first.*

**P4-C01 Licence criteria (about 30 minutes).** Claude drafts `docs/bakeoff/licence-criteria.md`; owner approves; committed before any result exists (TC-BO-5-01).

**P4-C02 Bake-off runner (about 2 hours).** `bakeoff run` per ADR-007 with the stub model for tests and one real three-case run. Tests: TC-BO-2-01, TC-BO-4-01, TC-BO-4-02, TC-BO-7-01.

**P4-C03 Owner runs the bake-off (owner about 1 hour).** For each candidate: one `bakeoff run`, then one `evaluate`, each given exactly with expected output and time (LG-1). Tests: TC-BO-3-01, TC-LG-1-01.

**P4-C04 Comparison and choice (about 45 minutes).** `compare`; Claude writes `recommendation.md`; the owner chooses; the decisions log is updated; BO-8 is run or declined on record. Tests: TC-BO-1-01, TC-BO-6-01, TC-BO-8-01.

**P4-C05 End-to-end closure (about 45 minutes).** From a clean checkout: gold build, one bake-off model, evaluate, compare; confirm every wiring-matrix row is exercised and one learning-log entry exists per chunk. Tests: TC-LG-2-01.

## Claude-specific chunking

- Each chunk loads only this guide, `cross-cutting.md`, and its section of `data-and-evaluation.md`.
- A chunk over about 3 hours is split by data, not by operation (Cohn).

## Test co-location

Tests are written inside each chunk, first, and named by TC ID. No chunk ends red.

## Parallel work

While the owner reviews gold batches, Claude runs the spike and builds the runner. Only one writer touches any file at a time; P1-C03 and P1-C04 are sequential because both touch `records`.

## Integration closure

P4-C05 runs the whole slice end to end from a clean checkout and checks every wiring-matrix row. Nothing is left to be wired later.

## Next step

Design review 001 findings are applied; `/gvm-build` starts at P1-C01.

## Changelog

| Date | Change | Reason | Author |
|---|---|---|---|
| 2026-10-26 | Model smoke test moved into Phase 1 (P1-C02); record rules before full evaluation (P1-C03, P1-C04, no longer parallel); prompt build chunk added (P2-C02); gold review split into five batch chunks (P3-C02 to P3-C06); comparison split from end-to-end closure (P4-C04, P4-C05); guard hook in P1-C01; learning entry in every chunk's done-criteria; wiring matrix extended | Design review 001, themes T1, T9, T10, T12, T14 | owner/AI |

---

*Developed using the Grounded Vibe Methodology*
