# AI Act Lab — Architecture Overview (Slice 1)

**Date:** 2026-10-26
**Status:** approved by the owner, 2026-10-26

*One page: what slice 1 is, its parts, and why it hangs together.*

## System context

One person (the owner) on one Apple M2 laptop with 8 GB. Inputs: the public text of the EU AI Act as amended, and small open models downloaded once. Outputs: a labelling guideline, a hand-checked gold set, a dates-and-duties table, and a measured comparison of four untuned models. No network service, no other users, no data leaves the laptop except commits to the public repository.

## Containers

- **Documents the owner reads and approves:** the guideline, the dates table, the licence criteria, every report.
- **Data files:** review sheets, the gold set, model outputs. All committed; model weights never.
- **The `lab` command-line tools:** `gold`, `relabel`, `dates`, `bakeoff`, `evaluate`, `compare`. Each reads files and writes new files; none calls another over a network.
- **Local model runtime:** `mlx-lm`, loading one 4-bit model at a time.

## Key decisions

| ADR | Decision | Where |
|---|---|---|
| ADR-001 | Plain scripts and files, no service | cross-cutting |
| ADR-002 | Python 3.13, one pinned environment, two dependencies | cross-cutting |
| ADR-003 | Readable formats: CSV for review, TOML for dates, JSON Lines for cases | cross-cutting |
| ADR-004 | Wilson intervals; paired bootstrap for differences and kappa | data-and-evaluation |
| ADR-005 | An answer is a valid record or a format failure, never guessed | data-and-evaluation |
| ADR-006 | One zero-shot prompt; instructions inside a case are case content | data-and-evaluation |

## Quality attributes

| Requirement | How it is met |
|---|---|
| Fits in 8 GB (BO-3, BO-4) | One model at a time; peak memory recorded; exclusion recorded on failure |
| Honest numbers (EV-5 to EV-7) | Missing and unreadable answers stay in the denominator; intervals on every number; paired test for gains |
| Repeatable (BO-7, EV-9) | Greedy generation, fixed seeds, versions in every report |
| Dates never from the model (LS-10, DT) | No date field in the record; a separate, sourced, approved table; dates in answers flagged |
| Confidentiality (GS-2) | Fictional cases; the pre-commit guard blocks risky text |

## Spec index

- `specs/cross-cutting.md` — conventions: tools, folders, formats, the answer record, errors, determinism, tests.
- `specs/data-and-evaluation.md` — the nine modules, the statistics, the parser, the prompt, and which tests prove each part.
- `specs/implementation-guide.md` — the build order in small chunks.

## Conceptual integrity

One idea runs through everything: the model judges, the table knows the dates, and every judgement is measured against cases a human checked. The single answer record, defined once and used by every tool, is what keeps the parts consistent.

---

*Developed using the Grounded Vibe Methodology*
