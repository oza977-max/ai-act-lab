---
schema_version: 1
---
# Impact Map

AI Act Lab. Drafted 2026-10-26 with the owner during `/gvm-impact-map`. Every requirement in the next phase must trace to one Deliverable (D-N) below.

## Goals
| ID | Statement | Metric | Target | Deadline |
|---|---|---|---|---|
| G-1 | The triage answer is trustworthy on clean descriptions and honest about the rest | On the held-out test set: tier accuracy on answered cases; share of cases answered; gain over the untuned base model | At least 90% correct on answered cases; at least 75% of cases answered; gain larger than its 95% confidence interval | 2026-11-16 |
| G-2 | The owner runs, reads and explains a fine-tuning cycle unaided | Train-and-evaluate cycles the owner runs from the notebook commands and writes up; concepts the owner explains to a colleague | At least 3 cycles run and written up by the owner; explains rank, learning rate, overfitting, selective accuracy and coverage | 2026-11-16 |

## Actors
| ID | Goal-ID | Name | Description |
|---|---|---|---|
| A-1 | G-1 | Owner as labeller and reviewer | Writes the label scheme, checks every gold case, decides whether a model version is good enough, and reviews every needs-human-review hand-off |
| A-2 | G-1 | Future user of the triage model | Someone who describes an AI system in plain English and reads the triage record; the owner now, others using the public repository later |
| A-3 | G-2 | Owner as learner | Runs training and evaluation commands, writes the notebook entries, answers the check questions |

## Impacts
| ID | Actor-ID | Behavioural change | Direction |
|---|---|---|---|
| I-1 | A-1 | Labels each gold case against a written guideline and records doubts instead of guessing | + |
| I-2 | A-1 | Spends review time only on the cases the model hands off, not on re-checking every answer | - |
| I-3 | A-1 | Accepts or rejects a model version on measured numbers with intervals, not on impressions | + |
| I-4 | A-2 | Relies on the tier, citation and reason for clean descriptions, and takes dates and duties from the lookup table, never from the model | + |
| I-5 | A-2 | Takes a needs-human-review answer to a person instead of overriding it | + |
| I-6 | A-3 | Runs each train-and-evaluate cycle from the written commands without asking how | + |
| I-7 | A-3 | Changes one training setting per run and writes a prediction before seeing the result | + |
| I-8 | A-3 | Explains each result with its confidence interval rather than as a bare number | + |

## Deliverables
| ID | Impact-ID | Title | Type |
|---|---|---|---|
| D-1 | I-1 | Label scheme and labelling guideline: tiers, Annex III areas, out of scope, needs human review, decision rules with examples, versioned | content |
| D-2 | I-1 | Gold set of 100 hand-checked cases, weighted to the Annex III versus Article 50 boundary and to the minimal tier | content |
| D-3 | I-1 | Agreement check: the owner re-labels a blind sample after a gap, and disagreements are settled into the guideline | process |
| D-4 | I-2 | Needs human review as a trained output, measured as accuracy on answered cases and share answered | feature |
| D-5 | I-2 | Hand-off record: what the model saw, why it declined, which articles are in play | feature |
| D-6 | I-3 | Evaluation script: tier accuracy, Annex III category accuracy, citation validity, answered-case accuracy and coverage, each with a 95% interval | tool |
| D-7 | I-3 | Base-model bake-off on the gold set: at least three candidates under 2B parameters, scored on zero-shot tier accuracy, output-format compliance, speed on this Mac, and licence and provenance | process |
| D-8 | I-3 | Held-out test set touched once at the end, with a leakage check against training cases | process |
| D-9 | I-4 | Dates-and-duties lookup table from Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744, each entry with a source link and a last-checked date | content |
| D-10 | I-4 | Fine-tuned LoRA adapter on the chosen base model, returning tier, Annex III category, article and a one-sentence reason | feature |
| D-11 | I-4 | Teacher-written training set of about 2,000 cases, filtered by a judge from a different model family | content |
| D-12 | I-4 | Citation checker against a fixed table of valid articles | tool |
| D-13 | I-4 | Local triage page that attaches the lookup table to the model's answer and runs offline | tool |
| D-14 | I-4 | Model card: intended use, out-of-scope use, evaluation numbers with intervals, known limits | content |
| D-15 | I-5 | Plain-language hand-off message on the triage page saying the case needs a person and what to ask them | content |
| D-16 | I-6 | Owner-runnable training and evaluation commands, one per step, in the lab notebook | process |
| D-17 | I-7 | Lab notebook entry per run: what changed, the prediction, what happened, next try | process |
| D-18 | I-8 | Learning-log entries with recaps and check questions, one per step | content |

## Changelog
| Date | Change | Rationale |
|---|---|---|
| 2026-10-26 | Approved by the owner: G-1, G-2; A-1 to A-3; I-1 to I-8; D-1 to D-18 | Elicited with the owner in /gvm-impact-map; validator clean (no implicit parents, goals pass the ambiguity scan, no childless nodes) |
