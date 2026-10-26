# AI Act Lab — Implementation Guide (Slice 1)

**Date:** 2026-10-26
**Status:** approved by the owner, 2026-10-26
**Inputs:** `specs/cross-cutting.md`, `specs/data-and-evaluation.md`, `test-cases/test-cases.md`

*The build order: four phases, thirteen chunks, each small enough to finish and test in one sitting. Phase numbering starts at P1: no earlier build exists in this repository.*

## Expert Panel

| Expert | Work | Role in This Document |
|---|---|---|
| Mike Cohn | *Agile Estimating and Planning*; *User Stories Applied* | Small, vertical, testable chunks; spikes for uncertainty |
| Andrew Hunt & David Thomas | *The Pragmatic Programmer* | A tracer bullet first: something runs end to end on day one |
| Kent Beck | *Test-Driven Development* | Tests inside every chunk, never a separate test chunk |
| Michael Feathers | *Working Effectively with Legacy Code* | Every module has a consumer that demanded it (wiring matrix) |

## Dependency Network

| Chunk | Depends on | Enables | Parallel with |
|---|---|---|---|
| P1-C01 Skeleton and first evaluation | none | P1-C02, P1-C03 | none |
| P1-C02 Full evaluation | P1-C01 | P4-C03 | P1-C03, P2-C01 |
| P1-C03 Record rules | P1-C01 | P3-C01, P4-C02 | P1-C02 |
| P2-C01 Guideline v1 | P1-C01 | P3-C02, P4-C02 | P1-C02, P1-C03 |
| P2-C02 Dates table | P2-C01 | none in slice 1 | P3 chunks |
| P3-C01 Gold tooling | P1-C03 | P3-C02 | P2-C02 |
| P3-C02 Gold drafting and review | P2-C01, P3-C01 | P3-C03, P4-C03 | P4-C00, P4-C01 |
| P3-C03 Blind re-label | P3-C02 plus 2 days | none | P4 chunks |
| P4-C00 Spike: candidate builds | P1-C01 | P4-C02 | P2, P3 chunks |
| P4-C01 Licence criteria | none | P4-C04 | anything before P4-C03 |
| P4-C02 Bake-off runner and prompt | P1-C03, P2-C01, P4-C00 | P4-C03 | P3-C02 |
| P4-C03 Owner runs the bake-off | P1-C02, P3-C02, P4-C02 | P4-C04 | P3-C03 |
| P4-C04 Comparison, choice, end-to-end check | P4-C01, P4-C03 | slice 2 | none |

```
Track A (code):   P1-C01 ─> P1-C03 ─> P3-C01 ─────────────┐      P4-C02 ─┐
                     │  └─> P1-C02 ──────────────────────────┼──────────────┼─> P4-C03 ─> P4-C04
Track B (owner):     └─> P2-C01 ─> P3-C02 (100 cases) ──────┘              │      ↑
                              └─> P2-C02 (dates)    P3-C02 + 2 days ─> P3-C03   P4-C01
Track C (models):    P4-C00 (spike) ─────────────────────────────────────────┘
```

**Critical path:** P1-C01 → P1-C03 → P3-C01 → P3-C02 → P4-C03 → P4-C04. The gold-set review (P3-C02, 3 to 6 hours of owner time) is the longest step; the blind re-label waits 2 days and runs alongside the bake-off.

## Wiring matrix

| Entry point | Consumed modules | Wiring chunk | Demanded by |
|---|---|---|---|
| `python -m lab.evaluate` | `lab.records.parse_answer`, `lab.records.validate`, `lab.records.contains_date`, `lab.articles.is_valid`, `lab.stats.wilson`, `lab.stats.paired_bootstrap_diff` | P1-C01, P1-C02 | P1-C01 (TC-EV-1-01, TC-EV-2-01 on the 10-case fixture); P1-C02 (TC-EV-4 to TC-EV-9) |
| `python -m lab.gold check` / `build` | `lab.records.validate` | P3-C01 | P3-C02 (the owner's first review batch must be checkable) |
| `python -m lab.relabel sample` / `score` | `lab.stats.cohen_kappa`, `lab.stats.kappa_bootstrap` | P3-C03 | P3-C03 (TC-GS-7-01, TC-GS-7-02) |
| `python -m lab.dates lookup` | `lab.dates.lookup` | P2-C02 | P2-C02 (TC-DT-1-01 to TC-DT-5-01) |
| `python -m lab.bakeoff run` | `lab.records.parse_answer`, model registry `data/models.toml`, prompt v1 | P4-C02 | P4-C03 (the owner's first real run) |
| `python -m lab.compare` | each model's `report.md`, `docs/bakeoff/licence-criteria.md` | P4-C04 | P4-C04 (TC-BO-3-01, TC-BO-6-01) |
| `lab.records` | (shared module, consumed by evaluate, gold, bakeoff) | P1-C01 | P1-C01 (TC-EV-5-01 needs unreadable answers detected) |
| `lab.articles` | (consumed by evaluate) | P1-C02 | P1-C02 (TC-EV-4-01) |
| `lab.stats` | (consumed by evaluate, relabel) | P1-C02 | P1-C02 (TC-EV-6-01, TC-EV-7-01) |

## Build Phases

### Phase 1 — Walking skeleton and the evaluation

The evaluation comes first because every later number depends on it, and because it can be finished and proved on the 10-case set before any real data exists.

**P1-C01 Skeleton and first evaluation (about 1 hour).** Create `.venv` with Python 3.13; pin `mlx-lm` and `pytest` in `requirements.txt` (fallback to 3.11 recorded if MLX does not install); package layout per `cross-cutting.md`; the 10-case fixture; a minimal `records` (parse, tier field) and `evaluate` producing tier accuracy and answered-case accuracy with a report. Runnable result: `python -m lab.evaluate --gold tests/fixtures/eval-10/gold.jsonl --outputs tests/fixtures/eval-10/outputs.jsonl` prints 7 of 10 and 6 of 8. Tests: TC-EV-1-01, TC-EV-2-01, TC-EV-2-02. *Needs owner permission to install packages.*

**P1-C02 Full evaluation (about 2 hours).** `stats` (Wilson, paired bootstrap), `articles.json` and `articles`, the remaining measures, paired mode with refusal, report header and plain-English summary. Tests: TC-EV-3-01 to TC-EV-10-01.

**P1-C03 Record rules (about 1 hour).** Full `validate`, date detection. Tests: TC-LS-2-01 to TC-LS-4-03, TC-LS-9-01, TC-LS-9-02, TC-LS-10-01.

### Phase 2 — Labels and dates

**P2-C01 Guideline v1 (Claude about 2 hours; owner about 1 hour).** Claude drafts `docs/guideline/labelling-guideline.md`: six labels, decision order, two worked examples per label, narrow review rule, record specification quoted from `records`, sources with checked dates, draft-guidance warnings. Owner reviews and approves v1. Checks: TC-LS-1-01, TC-LS-5-01, TC-LS-5-02, TC-LS-6-01, TC-LS-6-02, TC-LS-7-01, TC-LS-8-01.

**P2-C02 Dates table (Claude about 1 hour; owner about 30 minutes).** Claude verifies every plan date against the Official Journal and EUR-Lex, writes `data/dates/dates-table.toml` with sources, and builds `dates`. Owner checks and approves. Tests: TC-DT-1-01 to TC-DT-5-01.

### Phase 3 — Gold set

**P3-C01 Gold tooling (about 1.5 hours).** `gold check` and `gold build`. Tests: TC-GS-1-01, TC-GS-2-01 to TC-GS-2-03, TC-GS-3-01, TC-GS-4-01, TC-GS-4-02, TC-GS-5-01, TC-GS-5-02, TC-GS-6-01, on small fixture sheets.

**P3-C02 Gold drafting and review (owner 3 to 6 hours over several days).** Claude drafts five batches of 20 cases to the GS-1 spread; owner judges each batch in Numbers; `gold check` after each; `gold build` at the end. Commit after every batch.

**P3-C03 Blind re-label (owner about 45 minutes, at least 2 days after P3-C02).** `relabel sample`, owner labels 20 blind, `relabel score`, owner settles disagreements into guideline v2 if needed. Tests: TC-GS-7-01, TC-GS-7-02, TC-GS-8-01.

### Phase 4 — Bake-off

**P4-C00 Spike: candidate builds (about 1 hour; knowledge, not code).** For each of the four candidates, find the 4-bit MLX build, check it against the original model card (size, licence: BO-4), record it in `data/models.toml`, and test that it loads within 8 GB. *Each download needs the owner's permission, with file name, source and size stated first.*

**P4-C01 Licence criteria (about 30 minutes).** Claude drafts `docs/bakeoff/licence-criteria.md` (acceptable licences, use restrictions, training-data disclosure, developer jurisdiction); owner approves; committed before any result exists (BO-5, TC-BO-5-01).

**P4-C02 Bake-off runner and prompt (about 2 hours).** Prompt v1; `bakeoff run` with a stub model for tests and one real-model smoke run on 3 gold cases. Tests: TC-BO-2-01, TC-BO-4-01, TC-BO-4-02, TC-BO-7-01.

**P4-C03 Owner runs the bake-off (owner about 1 hour).** For each candidate: one `bakeoff run` command, then one `evaluate` command, each given exactly with expected output and time (LG-1). Tests: TC-BO-1-01, TC-BO-3-01, TC-LG-1-01.

**P4-C04 Comparison, choice and end-to-end check (about 1 hour).** `compare`; Claude's recommendation; owner chooses; decisions log updated. Then the integration check: from a clean checkout, run gold build, one bake-off model on the gold set, evaluate and compare, and confirm every wiring-matrix row is exercised. Tests: TC-BO-6-01, TC-BO-8-01, TC-LG-2-01.

## Claude-specific chunking

- Each chunk loads only this guide, `cross-cutting.md`, and its section of `data-and-evaluation.md`.
- A chunk over about 3 hours of work is split by data, not by operation (Cohn).

## Test co-location

Tests are written inside each chunk, first, and named by TC ID. No chunk ends red.

## Parallel work

Code and owner work overlap naturally: while the owner reviews gold batches (P3-C02), Claude can run the spike and build the runner (P4-C00, P4-C02). Only one writer touches any file at a time.

## Integration closure

P4-C04 runs the whole slice end to end from a clean checkout and checks every wiring-matrix row. Nothing is left "to be wired later".

## Next step

The method requires a design review (`/gvm-design-review`) before building; then `/gvm-build` starts at P1-C01.

---

*Developed using the Grounded Vibe Methodology*
