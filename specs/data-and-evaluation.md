# AI Act Lab — Data and Evaluation Spec (Slice 1)

**Date:** 2026-10-26
**Status:** approved by the owner, 2026-10-26
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
| Martin Kleppmann | *Designing Data-Intensive Applications* | One-way data flow between files |
| OWASP | *Top 10 for LLM Applications* | Model output treated as untrusted text |

## Architecturally Significant Requirements

- **EV-5, EV-7 (correct denominators).** A silent bug here fakes every result: the evaluation is the riskiest component and gets the most design.
- **BO-3, BO-4 (8 GB).** The runner must load one model at a time, measure peak memory, and record failure instead of crashing the comparison.
- **BO-7, EV-9 (repeatable).** Greedy generation and fixed seeds.
- **LS-10, DT (dates never from the model).** The dates table is a separate lookup; the evaluation flags any date in a model's answer.

## Data flow

One direction only; each step reads files and writes new files (Kleppmann).

```
guideline (md) ─┐
                ├─> review sheets (csv) ──owner──> gold set (jsonl) ──┬──> relabel sample (csv) ──owner──> kappa report
articles (json) ┘                                                     │
prompt (txt) ─────────────────────────────────────────────────────────┼──> bakeoff runner ──> outputs (jsonl) per model
                                                                      └──> evaluate ──> report (md) per model
outputs of two models ──> evaluate --paired ──> difference report
all reports ──> compare ──> comparison table (md) ──owner──> decisions log
dates table (toml) ──> dates lookup (independent of the model)
```

## ADR-004: Statistics

**Context.** EV-6 requires a 95% interval on every proportion with a named method; EV-7 a paired difference; GS-7 kappa with an interval. Samples are small (10 to 100), so normal-approximation intervals misbehave near 0 and 1.
**Options.** (1) Normal approximation everywhere; (2) Wilson score interval for proportions, paired bootstrap for differences and kappa; (3) exact (Clopper–Pearson) intervals.
**Decision.** Option 2. Wilson intervals stay inside 0 to 1 and are accurate at small n. The paired bootstrap resamples cases, keeping both models' answers on the same case together, 10,000 resamples with seed 20261026, percentile interval; the same for kappa. All standard library.
**Consequences.** Results repeat exactly (EV-9). The report names both methods (EV-6). A gain counts only if the paired interval excludes zero (EV-7).

## ADR-005: Reading a model's answer

**Context.** Small models often wrap the record in prose or produce near-JSON (format compliance is a bake-off measure, BO-3). Model text is untrusted (OWASP).
**Decision.** The parser takes the first complete JSON object in the text and validates it against the record rules. Anything else is `unreadable`. The parser never repairs content (no guessing a tier from prose); never executes or evaluates text.
**Consequences.** Format compliance is honest: a model that answers in prose scores as a format failure (TC-LS-9-02).

## ADR-006: The zero-shot prompt

**Context.** BO-2 requires one prompt for all candidates.
**Decision.** Prompt v1 contains: the six label definitions from the guideline, the decision order, the record fields with the example, the instruction to answer with the record only, and the case description inside clearly marked delimiters with a line stating that any instructions inside the description are part of the case, not commands (GS-4). No worked examples (zero-shot). Each model's own chat template wraps it.
**Consequences.** The prompt is versioned and committed before any run.

## Components

Interfaces below are contracts: name, inputs, outputs, behaviour. No bodies.

### `lab/records.py` — the answer record (LS-1 to LS-4, LS-9, LS-10, EV-5, EV-8)

- `Record` dataclass with the nine fields in `cross-cutting.md`.
- `validate(record) -> list[str]`: returns rule violations (empty means valid): label set, route/area/point consistency, article presence, review reason, reason of one sentence and at most 40 words.
- `parse_answer(raw: str) -> (Record | None, error)`: per ADR-005.
- `contains_date(text: str) -> bool`: detects day-month-year dates, month-year and ISO dates (EV-8).

### `lab/articles.py` — valid articles (EV-4)

- Loads `data/articles.json`: Articles 1 to 113, their paragraph numbers where cited, and Annexes I to XIII with Annex III points; as amended by Regulation (EU) 2026/1744, with source link and checked date.
- `is_valid(citation: str) -> bool`; `normalise(citation) -> str` so "Article 6(2)" and "Art. 6(2)" match.

### `lab/stats.py` — statistics (EV-6, EV-7, GS-7)

- `wilson(k, n) -> (low, high)`; `paired_bootstrap_diff(a_correct, b_correct, seed, n=10000) -> (diff, low, high)`; `cohen_kappa(labels_a, labels_b) -> float`; `kappa_bootstrap(labels_a, labels_b, seed) -> (low, high)`.

### `lab/evaluate.py` — the evaluation (EV-1 to EV-10)

- Command: `python -m lab.evaluate --gold data/gold/gold-v1.jsonl --outputs results/bakeoff/<model>/outputs.jsonl`, and `--paired <other outputs>`.
- Joins outputs to gold by `id`; a gold case with no output line is `missing` (EV-5). Computes: tier accuracy and confusion table; answered share and answered-case accuracy (needs-human-review is not answered); review said when gold says review, and when it does not; Annex III area accuracy on gold Annex III cases; citation validity and overlap; Article 50 flag accuracy; format failures and missing outputs; dates found. Every proportion with a Wilson interval.
- Paired mode refuses if either side lacks any gold case, naming them (EV-7).
- Writes `report.md` next to the outputs, opening with a plain-English summary (EV-10) and a header naming model, prompt, guideline and gold-set versions (EV-9).

### `lab/gold.py` — gold set (GS-1 to GS-6, LS-7)

- `python -m lab.gold check data/gold/review/batch-01.csv`: validates a review sheet: decision present, final tier in the label set, record rules, 60 to 200 words, guideline version known.
- `python -m lab.gold build`: merges all reviewed sheets into `gold-v{N}.jsonl`; checks the GS-1 counts, GS-3 area coverage, GS-4 tag quotas; reports the share of drafts the owner changed (GS-5); sets `never_train` on every case (GS-6).
- Review sheet columns: `id, description, proposed_tier, proposed_route, proposed_area, proposed_point, proposed_art50, proposed_articles, proposed_reason, tags, decision, final_tier, final_route, final_area, final_point, final_art50, final_articles, final_reason, owner_note`. The owner fills `decision`; on `accept`, the final columns are copied from the proposals by `check`; on `change`, the owner fills them.

### `lab/relabel.py` — blind re-label (GS-7, GS-8)

- `python -m lab.relabel sample`: picks 20 cases with the fixed seed, writes `data/gold/relabel/sheet.csv` with descriptions only (no labels), records the date. Refuses if fewer than 2 days have passed since the gold set's build date.
- `python -m lab.relabel score`: compares tiers, reports agreement, kappa and its interval against the 0.8 target, and lists each disagreement for the owner to settle into the guideline (GS-8).

### `lab/dates.py` — dates-and-duties table (DT-1 to DT-5)

- Table entries keyed by `tier`, `route` and `art50`: `applies_from` (date), `duties` (list of article references with short titles), `source_url`, `article`, `last_checked`, `checked_by`, `verified` (true only after the Official Journal check), `note`. Explicit entries for out-of-scope and needs-human-review (DT-1). Header block: `approved_by`, `approved_on`, change log (DT-5).
- `lookup(tier, route, art50, today) -> list[Entry]`: deterministic (DT-3); marks entries stale when more than 90 days since `last_checked` (DT-4); refuses unverified entries (DT-2).
- Command: `python -m lab.dates lookup --tier high-risk --route annex-iii`.

### `lab/bakeoff.py` — runner (BO-1 to BO-4, BO-7)

- Command: `python -m lab.bakeoff run --model <model-slug>`, one model at a time.
- Loads the model's 4-bit MLX build through `mlx-lm`, applies its chat template to prompt v1, generates greedily with a 400-token limit per case, writes one output line per gold case as it goes, records seconds per case and peak memory.
- If loading fails or memory exceeds the limit, writes an `excluded.md` with the reason and the memory observed instead of outputs (BO-4).
- Model registry `data/models.toml`: slug, the build to download, the original model card URL, licence, parameter count; filled and checked in the spike chunk (BO-4 community-build check).

### `lab/compare.py` — comparison (BO-3, BO-5, BO-6)

- `python -m lab.compare`: reads each model's report and the licence criteria (`docs/bakeoff/licence-criteria.md`, committed before any run, BO-5) and writes `results/bakeoff/comparison.md`: one row per candidate with the five measures, and a recommendation section that Claude writes and the owner reads before choosing (BO-6).

## Integration points

- `records.py` is used by `evaluate`, `gold`, `bakeoff`: one definition of the record.
- `stats.py` is used by `evaluate` and `relabel`.
- `dates.py` stands alone in slice 1; the local page (later slice) will call `lookup`.

## Error handling and edge cases

- A gold id appearing twice, an unknown tier in a sheet, or a missing column stops the command with file, line and rule.
- A model that times out on one case: the case is recorded as `missing` and the run continues; the count is in the report.
- An answer citing an article that does not exist is valid as a record but counts as an invalid citation (EV-4).
- Answered-case accuracy with zero answered is reported as "not defined", never 100% (TC-EV-2-02).

## Testing strategy

| Component | Test cases |
|---|---|
| `records` | TC-LS-1-01 to TC-LS-10-01 |
| `gold` | TC-GS-1-01 to TC-GS-6-01 |
| `relabel`, `stats` | TC-GS-7-01, TC-GS-7-02, TC-GS-8-01 |
| `dates` | TC-DT-1-01 to TC-DT-5-01 |
| `bakeoff`, `compare` | TC-BO-1-01 to TC-BO-8-01 (runner tests use a stub model; one real-model smoke test) |
| `evaluate`, `stats` | TC-EV-1-01 to TC-EV-10-01 on the 10-case fixture |
| owner steps | TC-LG-1-01, TC-LG-2-01 (checked at the end of each step) |

---

*Developed using the Grounded Vibe Methodology*
