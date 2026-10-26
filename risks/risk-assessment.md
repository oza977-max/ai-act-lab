---
schema_version: 1
---
# Risk Assessment — AI Act Lab

Drafted 2026-10-26 by Claude from `docs/00-plan.md` and `impact-map.md`, for the owner to review and correct. Cagan's four product risks, as required before `/gvm-requirements`.

## Value Risk

Will the result be worth having? The value is twofold (impact map G-1 and G-2). For the model, the risk is that a 0.8B model cannot reach 90% correct tiers on answered cases with 75% coverage, so the triage answer is not trustworthy enough to save the owner's time; the untuned baseline and the bake-off on the gold set will show early whether the gap is closable, and Lawma's results on legal labelling suggest it is. A second value risk is that the gold set is too easy, so a high score means little; weighting it to the Annex III versus Article 50 boundary and to the minimal tier addresses this. For learning, the risk is that the owner watches rather than does; the owner running three cycles is the guard.

questioner: Claude (draft), to be confirmed by the owner

## Usability Risk

Can the people on the map use it? The owner as labeller must label 100 cases against a guideline without legal training in every Annex III area; the risk is fatigue and inconsistent labels, mitigated by a short versioned guideline, worked examples, a "needs human review" option for genuine doubt, and a blind re-label check. A future user may read a tier as legal advice; the hand-off wording and model card must say plainly what the answer is and is not. The owner as learner may find terminal commands intimidating; every command is given exactly, one per step, with what to expect on screen.

questioner: Claude (draft), to be confirmed by the owner

## Feasibility Risk

Can it be built on an Apple M2 with 8 GB? Reference figures from a comparable project put a 0.8B 4-bit LoRA run at 3.9 GB and about fifteen minutes, so training should fit, but they are not yet measured here. The bake-off needs three to five candidate models to run on this Mac; some may lack MLX builds or exceed memory, which shrinks the field. Legal feasibility risk: the Commission's Article 6 classification guidelines are only a draft, and dates moved once already under Regulation (EU) 2026/1744, so labels and the dates table must cite their sources and a last-checked date. Teacher-written data may inherit the teacher's blind spots; the gold set is the check.

questioner: Claude (draft), to be confirmed by the owner

## Viability Risk

Does it make sense to do at all, and under what constraints? The project is a personal learning project with a public repository; confidentiality is the hard constraint, so no employer names, internal figures or internal team names may appear anywhere, and every case is freshly written from public regulation text. The deadline is 16 November 2026, with roughly 15 to 20 hours of owner time; scope beyond the first slice must wait. Honesty is a constraint too: a 0.8B model is not a lawyer, and results are reported with confidence intervals, including failures. Licences of candidate base models must be acceptable for a European compliance audience.

questioner: Claude (draft), to be confirmed by the owner
