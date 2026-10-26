# AI Act Lab — Data and Evaluation Spec (Slice 1)

**Date:** 2026-10-26
**Status:** approved by the owner, 2026-10-26; revised after design review 001
**Scope:** the guideline, gold set, re-label check, dates table, bake-off and evaluation. Requirements LS-1 to LG-2. Conventions: `specs/cross-cutting.md`.

*What each part of the code is responsible for, what goes in and out of it, the statistics it uses, and which tests prove it.*

## Expert Panel

| Expert | Work | Role in This Document |
|---|---|---|
| George Fairbanks | *Just Enough Software Architecture* | Depth where the risk is: the evaluation and the bake-off runner |
| Evan Miller | *Adding Error Bars to Evals* | Interval and paired-comparison methods |
| James Pustejovsky & Amber Stubbs | *Natural Language Annotation for Machine Learning* | Gold-set and re-label workflow |
| Yonatan Geifman & Ran El-Yaniv | *Selective Classification* | Answered-case accuracy and coverage |
| Zhenyan Lu et al. | *Small Language Models survey* | Measuring speed and memory on the device |
| Martin Kleppmann | *Designing Data-Intensive Applications* | One-way data flow; one owner per derived fact |
| Bratus, Patterson & Sassaman | LANGSEC | One parser for model output; recognise fully before use |
| OWASP | *Top 10 for LLM Applications* | Model output and case text treated as untrusted |

## Architecturally Significant Requirements

- **EV-5, EV-7 (correct denominators).** A silent bug here fakes every result: the evaluation is the riskiest component and gets the most design.
- **BO-3, BO-4 (8 GB).** One model at a time, in a child process, with peak memory measured and a crash recorded rather than fatal (ADR-007).
- **BO-7, EV-9 (repeatable).** Greedy generation, thinking off, fixed seeds, report dates from run files.
- **LS-10, DT (dates never from the model).** The dates table is a separate lookup; the evaluation flags any date in a model's raw answer.

## Data flow

One direction only; each step reads files and writes new files; each derived fact has one owner (Kleppmann).

```
guideline (md) + records ──> prompt build ──> prompt v{N} (txt)
guideline + articles ──> review sheets (csv) ──owner──> gold build ──> gold-v{N}.jsonl + .meta.json
gold ──> relabel sample ──> sheet.csv ──owner──> relabel score ──> kappa report + resolutions.csv
models.toml + prompt + gold ──> bakeoff run (child process) ──> outputs.jsonl + run.json  (or excluded.md)
gold + outputs + run.json ──> evaluate ──> report.md + metrics.json   (--paired: paired-vs-{b}.md)
metrics.json + run.json + models.toml + excluded.md + licence criteria ──> compare ──> comparison.md
recommendation.md (written once by Claude, never overwritten) ──owner──> decisions log
dates-table.toml ──> dates lookup (independent of the model)
```

## ADR-004: Statistics

**Context.** EV-6 requires a 95% interval on every proportion with a named method; EV-7 a paired difference; GS-7 kappa with an interval. Samples are small (10 to 100).
**Decision.** Wilson score interval, z = 1.96, for every proportion; with zero cases the proportion and interval are "not defined". Paired bootstrap for differences between two models: resample case indices with replacement, keeping both models' answers on a case together, 10,000 resamples, `random.Random(20261026)`, percentile interval from the 2.5th and 97.5th percentiles, on per-case tier correctness. Cohen's kappa on tiers; when expected agreement is 1, kappa is "not defined"; the kappa interval is a bootstrap as above, skipping resamples where kappa is undefined and reporting how many were skipped. Kappa is compared with the 0.8 target after rounding to two decimals. Standard library only.
**Consequences.** Results repeat exactly (EV-9). The report names both methods (EV-6). A gain counts only if the paired interval excludes zero (EV-7). Known-answer tests pin Wilson and the bootstrap.

## ADR-005: Reading a model's answer

**Context.** Small models often wrap the record in prose or produce near-JSON. Model text is untrusted. Two parsers for the same input invite disagreement (LANGSEC).
**Decision.** Only `evaluate` parses. It scans the raw text (at most 4,000 characters; longer is unreadable) from each `{` with the standard JSON decoder and takes the first object that decodes. Duplicate keys, unknown keys, missing keys or any `validate` rule violation make the answer `unreadable`. Prose around a valid record is allowed and counted in the report. The parser never repairs content and never executes or evaluates text.
**Consequences.** Format compliance is honest: a model that answers in prose scores as a format failure (TC-LS-9-02).

## ADR-006: The zero-shot prompt

**Context.** BO-2 requires one prompt for all candidates. A hand-written prompt would be a second copy of the guideline that drifts (design review C-5).
**Decision.** `python -m lab.prompt build` generates `prompts/zero-shot-v{N}.txt` from the guideline's label definitions and decision order and from the record definition in `records`, stamping the guideline version. It contains the six label definitions, the decision order, the record fields with the example, the instruction to answer with the record only, and the case between the delimiters `<<<CASE` and `CASE>>>`, with a line stating that instructions inside the case are part of the case, not commands. `gold check` rejects any description containing either delimiter. No worked examples (zero-shot). The whole prompt is one user message; each model's chat template wraps it with thinking off (cross-cutting ADR-009). The models have no tools and no network, so a successful injection can only produce a wrong label, which the evaluation measures.
**Consequences.** A test checks that the prompt's definitions match the guideline's.

## ADR-007: Running a model within 8 GB

**Context.** An out-of-memory kill ends the process before it can record anything; a single generation cannot be interrupted from inside (design review T1).
**Decision.** `bakeoff run` starts a child process per model. The child loads the model, then after each case reads MLX peak memory and appends it to the run log; it stops with a distinct exit status if peak memory exceeds 6.5 GB. The parent records `excluded.md` from the exit status and the last recorded peak if the child exits abnormally, is killed, or exceeds the limit. There is no per-case timeout: the 400-token cap bounds each case.
**Consequences.** One failing model cannot stop the comparison; the 6.5 GB limit leaves headroom for macOS on an 8 GB machine.

## Measure definitions

Every measure uses all gold cases unless stated. Unreadable and missing answers count as wrong and as not answered.

| Measure | Numerator | Denominator | Unreadable or missing |
|---|---|---|---|
| Tier accuracy | answers whose tier equals the gold tier | all gold cases | wrong |
| Share answered | answers with a tier other than needs-human-review | all gold cases | not answered |
| Answered-case accuracy | answered cases whose tier equals gold | answered cases | excluded (not answered) |
| Review when gold says review | answers of needs-human-review | gold needs-human-review cases | counts as not saying review |
| Review when gold does not | answers of needs-human-review | gold cases that are not needs-human-review | counts as not saying review |
| Annex III area accuracy | answers with the gold area | gold cases with route Annex III | wrong |
| Article 50 flag accuracy | answers with the gold flag | all gold cases | wrong |
| Citation validity | cited citations found in `articles.json` | all citations in readable answers | contributes none |
| Citation overlap | answers sharing at least one article number with gold | gold cases with at least one gold citation | no overlap |
| Format failures | unreadable answers | all gold cases | — |
| Missing answers | missing answers | all gold cases | — |
| Dates found | answers whose raw text contains a date | all gold cases with raw text | raw text is scanned even when unreadable |

## Components

Interfaces below are contracts: name, inputs, outputs, behaviour. No bodies.

### `lab/records.py` — the answer record (LS-1 to LS-4, LS-9, LS-10, EV-5, EV-8)

- Owns the vocabularies: tiers, routes, review reasons, tags. Every other module imports them from here.
- `Record` is a frozen dataclass with the nine fields in `cross-cutting.md`; `to_json()` and `from_json()` serialise it.
- `validate(record) -> list[str]`: rule violations; empty means valid. A reason is one sentence when it has exactly one sentence-ending mark (`.`, `!`, `?`) at its end, ignoring periods in abbreviations such as "Art." and "e.g."; at most 40 words split on whitespace.
- `parse_answer(raw: str) -> tuple[Record | None, Literal["ok", "unreadable"]]`: per ADR-005.
- `contains_date(text: str) -> bool`: must match "2 August 2026", "2 Aug 2026", "August 2026", "2026-08-02", "02/08/2026"; must not match "2027" alone, "Art. 113", "Annex III 4(a)", "Regulation (EU) 2024/1689". Applied to raw text.

### `lab/articles.py` — valid articles (EV-4)

- `data/articles.json`: `{"source_url", "checked_on", "articles": {"1": ["1","2"], ..., "113": [...]}, "annexes": {"I": [], ..., "III": ["1(a)", ...], ..., "XIII": []}}`, listing paragraphs per article and points per annex, as amended by Regulation (EU) 2026/1744.
- Citation grammar: `Art. <n>` or `Article <n>`, optionally `(<para>)` and `(<letter>)`; `Annex <roman>` optionally followed by a point such as `4(a)`. `normalise` produces `Art. 6(2)` and `Annex III 4(a)`.
- `is_valid(citation) -> bool`; `article_number(citation) -> str | None` for overlap at article level ("Art. 6(2)" and "Art. 6" overlap).

### `lab/stats.py` — statistics (EV-6, EV-7, GS-7)

- `wilson(k, n)`, `paired_bootstrap_diff(a_correct, b_correct, seed)`, `cohen_kappa(a, b)`, `kappa_bootstrap(a, b, seed)` per ADR-004; undefined values are `None`, shown as "not defined".

### `lab/prompt.py` — prompt build (BO-2)

- `python -m lab.prompt build` per ADR-006.

### `lab/evaluate.py` — the evaluation (EV-1 to EV-10)

- `python -m lab.evaluate --gold <gold.jsonl> --run results/bakeoff/<slug>/` reads `outputs.jsonl` and `run.json` from the run folder; `--paired results/bakeoff/<other>/` adds a paired comparison.
- Joins outputs to gold by `id`; an output id not in gold, or a duplicate id, stops with an error; a gold case with no output is `missing` (EV-5).
- Computes every measure in the table above with Wilson intervals; writes `report.md` (plain-English summary first, then measures and a confusion table; counts and case IDs only, never raw model text) and `metrics.json`. The header names model, build revision, prompt version, guideline version, gold-set version and run date from `run.json`.
- Paired mode writes `results/bakeoff/<slug>/paired-vs-<other>.md` and refuses if either side lacks any gold case, naming them (EV-7).

### `lab/gold.py` — gold set (GS-1 to GS-6, LS-7)

- Review sheet columns: `id, description, tags, proposed_tier, proposed_route, proposed_area, proposed_point, proposed_legislation, proposed_art50, proposed_articles, proposed_review_reason, proposed_reason, decision, final_tier, final_route, final_area, final_point, final_legislation, final_art50, final_articles, final_review_reason, final_reason, owner_note, guideline_version`.
- Encodings: UTF-8 (a byte-order mark added by a spreadsheet app is accepted); booleans `true`/`false`; lists separated by `;`; an empty cell means none. Cells written by Claude that begin with `=`, `+`, `-` or `@` are prefixed with an apostrophe so a spreadsheet does not run them as formulas.
- `python -m lab.gold check <sheet>` validates only, never edits: decision is `accept`, `change` or `doubt`; on `change` the final columns form a valid record; on `accept` the proposed columns do; 60 to 200 words; tags from the vocabulary; no delimiter strings; guideline version matches the guideline header; a description altered by the spreadsheet (compared with the draft file) is reported.
- `python -m lab.gold build` refuses while any `doubt` remains; copies accepted proposals into the gold record; keeps the full draft; checks GS-1 counts, GS-3 area coverage, GS-4 tag quotas and one guideline version; reports the share changed; sets `never_train`; writes `gold-v{N}.jsonl` and `gold-v{N}.meta.json` (build date, hash, guideline version). A guideline change after build means a new gold version.

### `lab/relabel.py` — blind re-label (GS-7, GS-8)

- `sample`: refuses if fewer than 2 days since the build date in the meta file; picks 20 ids with `random.Random(seed).sample` over sorted ids; writes `sheet.csv` (`id, description, relabel_tier, note`) and `record.json` (seed, date, ids, gold version).
- `score`: reads the filled sheet; reports agreement, kappa and interval against 0.8; writes `resolutions.csv` (`id, first_label, second_label, resolution, guideline_version`) with the disagreements for the owner to complete (GS-8).

### `lab/dates.py` — dates-and-duties table (DT-1 to DT-5)

- `data/dates/dates-table.toml`: a header (`approved_by`, `approved_on`, `[[changes]]`), then `[[entry]]` tables with `tier`, `route` (`annex-iii`, `annex-i` or `none`), `art50` (`true`, `false` or `any`), `duties` (array of tables: `article`, `title`, `applies_from`), `source_url`, `last_checked`, `checked_by`, `verified`, `plan_value`, `discrepancy_note`, `note`. Vocabularies imported from `records`.
- `lookup(tier, route, art50, today) -> list[Entry]`: entries matching exactly, plus `art50 = any`; deterministic; each entry carries `stale` (more than 90 days since `last_checked`). Raises `UnverifiedEntryError` naming the entry if any match is unverified; raises `NoEntryError` if nothing matches. Explicit entries exist for out-of-scope and needs-human-review (DT-1).
- `python -m lab.dates lookup --tier high-risk --route annex-iii --art50 false [--today 2026-10-26]`.

### `lab/bakeoff.py` — runner (BO-1 to BO-4, BO-7)

- `python -m lab.bakeoff run --model <slug>`; the slug must be a key in `models.toml` matching `^[a-z0-9._-]+$`.
- Per ADR-007 and cross-cutting ADR-008/009: child process, pinned revision, safetensors only, no remote code, thinking off, greedy, 400 tokens; writes `outputs.jsonl` and `run.json` as it goes.
- `python -m lab.bakeoff smoke --model <slug>`: one case, prints the answer, seconds and peak memory (Phase 1 tracer).
- A `Generator` protocol (`load()`, `generate(prompt) -> str`, `peak_memory_gb() -> float`) lets tests use a stub model.

### `lab/compare.py` — comparison (BO-3, BO-5, BO-6, BO-8)

- `python -m lab.compare` reads every model's `metrics.json`, `run.json` and `excluded.md`, `models.toml`, and `docs/bakeoff/licence-criteria.md`; writes `results/bakeoff/comparison.md` with one row per candidate (excluded ones with their reason). Adding a candidate is one row in `models.toml` (BO-8).
- Claude's recommendation goes in `results/bakeoff/recommendation.md`; `compare` never overwrites it.

## Integration points

- `records` is used by `evaluate`, `gold`, `prompt` and `dates` (vocabularies); `stats` by `evaluate` and `relabel`; `articles` by `evaluate` and `gold`.
- `dates` stands alone in slice 1; the local page (a later slice) will call `lookup`.

## Error handling and edge cases

- A duplicate id, an unknown value in a sheet or a missing column stops the command with file, line and rule.
- Answered-case accuracy with zero answered is "not defined", never 100% (TC-EV-2-02).
- An answer citing an article that does not exist is a readable record with an invalid citation (EV-4).

## Testing strategy

| Component | Test cases |
|---|---|
| `records` | TC-LS-1-01 to TC-LS-10-01, TC-EV-8-01 |
| `gold` | TC-GS-1-01 to TC-GS-6-01 |
| `relabel`, `stats` | TC-GS-7-01, TC-GS-7-02, TC-GS-8-01, plus known-answer tests for Wilson and the bootstrap |
| `dates` | TC-DT-1-01 to TC-DT-5-01 |
| `prompt` | a test that the prompt's definitions match the guideline |
| `bakeoff`, `compare` | TC-BO-1-01 to TC-BO-8-01 (stub model for unit tests; one real-model smoke run) |
| `evaluate`, `stats` | TC-EV-1-01 to TC-EV-10-01 on the 10-case fixture below |

**The 10-case fixture** (`tests/fixtures/eval-10/`): `gold.jsonl` and `run/outputs.jsonl` plus `run/run.json`. Gold tiers: E01 prohibited, E02 high-risk (Annex III area 4), E03 high-risk (Annex III area 5), E04 transparency-only, E05 minimal, E06 minimal, E07 transparency-only, E08 out-of-scope, E09 minimal, E10 needs-human-review. Outputs: E01 to E06 correct; E07 minimal (wrong); E08 minimal (wrong); E09 needs-human-review; E10 needs-human-review. Hand counts: tier accuracy 7 of 10; answered 8 of 10; answered-case accuracy 6 of 8. Variants for TC-EV-3 to TC-EV-8 are separate small files in the same folder.

## Changelog

| Date | Change | Reason | Author |
|---|---|---|---|
| 2026-10-26 | Rewritten after design review 001: ADR-004 edge cases; ADR-005 single parser in `evaluate`; ADR-006 prompt generated from the guideline; new ADR-007 child-process runner with a 6.5 GB limit; measure definitions table; contracts for articles, dates TOML, review sheet, re-label files, run and metrics files, prompt build, smoke command and stub protocol; 10-case fixture defined | Design review 001, themes T1 to T9, T12 to T14 | owner/AI |

---

*Developed using the Grounded Vibe Methodology*
