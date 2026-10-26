# AI Act Lab — Requirements, Slice 1

**Date:** 2026-10-26
**Status:** approved by the owner, 2026-10-26
**Scope:** first slice only: label scheme and guideline (D-1), gold set (D-2), blind re-label check (D-3), base-model bake-off (D-7), dates-and-duties table (D-9), evaluation (D-6). Training is a later slice.

*What the first slice must do, in testable sentences. Each requirement has an ID, a priority, a trace to a deliverable in `impact-map.md`, and a way to check it. No design or technology choices: those belong to the technical specification.*

## Expert Panel

| Expert | Work | Role in This Document |
|---|---|---|
| Karl Wiegers | *Software Requirements* (3rd ed.) | Classification, MoSCoW priorities, ambiguity removal |
| Gause & Weinberg | *Exploring Requirements* | "How would we know it is met?" for every requirement |
| Jeff Patton | *User Story Mapping* | Now-versus-later slicing; the Won't boundary |
| Alan Cooper | *About Face* | The owner persona |
| James Pustejovsky & Amber Stubbs | *Natural Language Annotation for Machine Learning* | Guideline, gold set, blind re-label |
| European Commission (AI Office) | AI Act guidelines C(2025) 924 and 884 | Definition-first decision order; prohibited examples |
| Yonatan Geifman & Ran El-Yaniv | *Selective Classification* | Answered-case accuracy and coverage |
| Evan Miller | *Adding Error Bars to Evals* | Intervals and paired comparison |
| Percy Liang et al. | *HELM* | Several measures, not one headline number |
| Zhenyan Lu et al. | *Small Language Models: Survey, Measurements, and Insights* | Measure speed and memory on this Mac |
| Zorik Gekhman et al. | *Fine-Tuning on New Knowledge* | No dates in the weights or the output record |
| Athanasios Davvetas et al. | *AI Act Evaluation Benchmark* | Weighting the gold set to the minimal tier |
| OWASP | *Top 10 for LLM Applications* | Instructions hidden in descriptions as test cases |

## Purpose & Vision

**Job statement.** When I describe an AI system in plain English, I want a trustworthy first answer on its EU AI Act tier, with the article and a reason, or an honest "needs human review", so I can spend my own review time only on the hard cases, and learn to build such a model myself.

This slice builds the measuring stick before the model: the labels, the hand-checked cases, the dates table and the evaluation, then measures four untuned candidate models with it. It serves impact-map goals G-1 and G-2.

## Target User

**The owner.** An EU AI Act practitioner who is new to model training and to git. Goal: a triage assistant they trust on clean descriptions, and the skill to build and judge one. Context: an Apple M2 laptop with 8 GB, an hour or two a day, a deadline of 16 November 2026. Frustration to avoid: confident answers that recite outdated dates. Experience goal: never be surprised by a number they cannot explain.

## User Journeys

1. **Agree the labels.** Read the guideline draft, settle open points, approve version 1.
2. **Judge the gold set.** Review 100 drafted cases in batches; accept, change or mark doubt.
3. **Check yourself.** Two or more days later, re-label 20 cases blind; settle disagreements into the guideline.
4. **Approve the dates table.** Check each entry's source; approve.
5. **Run the bake-off.** Run the given commands; read one comparison table; choose the base model.

## Label Scheme and Guideline

How a case is labelled and what the model must output. The guideline is the single source of labelling rules (Pustejovsky and Stubbs, MATTER).

**LS-1 (Must) [impact-deliverable: D-1]:** **[MUST]** The label scheme shall define exactly six tier labels: prohibited, high-risk, transparency-only, minimal, out-of-scope (not an AI system, or excluded from the Act), and needs-human-review. Each label shall have a one-sentence definition that names the article it rests on.
*Check:* Read the guideline: six labels, six definitions, each citing an article.

**LS-2 (Must) [impact-deliverable: D-1]:** **[MUST]** Every high-risk label shall state its route: Annex III, with the area (1 to 8) and point, or Annex I, with the product legislation concerned.
*Check:* Every high-risk gold case carries a route; every Annex III case carries an area and point.

**LS-3 (Must) [impact-deliverable: D-1]:** **[MUST]** Every record shall carry a yes/no flag stating whether Article 50 transparency duties also apply, independently of the tier.
*Check:* A high-risk chatbot case can be labelled high-risk with the flag set to yes.

**LS-4 (Must) [impact-deliverable: D-1]:** **[MUST]** Every record shall carry the article or articles relied on and a reason of one sentence, at most 40 words.
*Check:* Count words; check the article field is never empty for the first five labels.

**LS-5 (Must) [impact-deliverable: D-1]:** **[MUST]** The guideline shall set a fixed order of questions (is it an AI system and in scope; is it prohibited; is it high-risk through Annex I or Annex III, including the Article 6(3) exception; do Article 50 duties apply; otherwise minimal) and give at least two worked examples per label, at least one of them a boundary case.
*Check:* Count the worked examples per label in the guideline.

**LS-6 (Must) [impact-deliverable: D-1]:** **[MUST]** The guideline shall define needs-human-review narrowly: the description lacks a fact that decides the tier, the facts conflict, or the legal text needed is unsettled (for example, a point that depends on the draft Article 6 guidelines). A case that is hard but decidable shall not be labelled needs-human-review.
*Check:* Each needs-human-review gold case names which of the three reasons applies.

**LS-7 (Must) [impact-deliverable: D-1]:** **[MUST]** The guideline shall carry a version number and a change log; every gold label shall record the guideline version it was given under.
*Check:* Every gold case has a guideline-version field that matches a version in the change log.

**LS-8 (Must) [impact-deliverable: D-1]:** **[MUST]** Every rule in the guideline shall cite Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744, with a link to the official text and the date it was checked. Where a rule rests on Commission guidance that is only a draft, the guideline shall say so.
*Check:* Spot-check five rules: each has an article, a link and a checked date.
> The Article 6 classification guidelines were in draft (consultation from 19 May 2026) with no final text found on 26 October 2026.

**LS-9 (Must) [impact-deliverable: D-1]:** **[MUST]** The guideline shall specify one fixed output record with named fields (tier, route, Annex III area and point, Article 50 flag, articles, reason) and one complete example. Any model output that cannot be read as this record counts as a format failure.
*Check:* The example record in the guideline contains every named field.

**LS-10 (Must) [impact-deliverable: D-1]:** **[MUST]** The output record shall contain no application dates, deadlines or lists of obligations. These come only from the dates-and-duties table.
*Check:* The record definition has no date or obligations field.

## Gold Set and Re-label Check

The 100 hand-checked cases everything is measured against, and the owner's blind check on their own consistency.

**GS-1 (Must) [impact-deliverable: D-2]:** **[MUST]** The gold set shall contain 100 cases distributed as: prohibited 10, high-risk through Annex III 30, high-risk through Annex I 5, transparency-only 20, minimal 20, needs-human-review 10, out-of-scope 5.
*Check:* Count gold cases by final label.
> The owner chose this distribution on 2026-10-26: heavy on the Annex III versus Article 50 boundary and on the minimal tier, where the 2026 AI Act benchmark's baseline was weakest.

**GS-2 (Must) [impact-deliverable: D-2]:** **[MUST]** Every case shall be a plain-English description of 60 to 200 words, freshly written, about a fictional organisation, built from public regulation text only. No real employer, client, product or person shall appear.
*Check:* Word-count check; the confidentiality scan finds no real organisation names.

**GS-3 (Must) [impact-deliverable: D-2]:** **[MUST]** The 30 Annex III cases shall cover all eight Annex III areas with at least three cases each.
*Check:* Count Annex III cases by area.

**GS-4 (Must) [impact-deliverable: D-2]:** **[MUST]** The gold set shall include at least 15 cases on the Annex III versus Article 50 boundary, at least 5 cases that turn on the Article 6(3) exception, and at least 5 cases whose description contains instructions aimed at the model (to be ignored).
*Check:* Each case carries tags; count the tags.

**GS-5 (Must) [impact-deliverable: D-2]:** **[MUST]** Claude shall draft each case with a proposed label, articles and reason. The owner shall judge every case: accept, change, or mark as doubtful. The owner's judgement is the gold label, and every change from the draft shall be recorded.
*Check:* Every case has an owner decision field; the share of changed drafts is reported.

**GS-6 (Must) [impact-deliverable: D-2]:** **[MUST]** Gold cases shall be marked never-train and kept apart from any training data; no later training case may paraphrase a gold case.
*Check:* The gold set's location and marker are named in the guideline; the later leakage check reads them.

**GS-7 (Must) [impact-deliverable: D-3]:** **[MUST]** At least two days after finishing the gold set, the owner shall re-label 20 randomly chosen cases without seeing the first labels. Agreement on the tier shall be reported as Cohen's kappa with a 95% interval; the target is 0.8 or more.
*Check:* The re-label record shows the sample, the date gap, the two labels per case and kappa with its interval.
> Pustejovsky and Stubbs: a gold standard is adjudicated, not single-pass.

**GS-8 (Must) [impact-deliverable: D-3]:** **[MUST]** Every disagreement in the re-label check shall be settled by the owner and, where it reveals a gap, recorded as a guideline change with a new version.
*Check:* Each disagreement links to a resolution and, where applicable, a guideline version.

## Dates-and-Duties Table

The maintained table that supplies dates and duties. The model never learns them (Gekhman et al.; Huyen).

**DT-1 (Must) [impact-deliverable: D-9]:** **[MUST]** The table shall give, for each tier label and route (including the Article 50 flag), the dates from which duties apply and the duties themselves as article references with short plain-English titles. For labels that carry no tier duties (out-of-scope, needs-human-review), the table shall return an explicit entry saying so and what to do next, never an empty result.
*Check:* Every label and route in LS-1 to LS-3 has at least one entry.

**DT-2 (Must) [impact-deliverable: D-9]:** **[MUST]** Every entry shall carry a link to the official text, the article, the date it was last checked, and who checked it. The initial values from the project plan shall be verified against the Official Journal before use, and any discrepancy recorded.
*Check:* No entry lacks a source, article or checked date.
> Plan values to verify: prohibitions in force; two new Article 5 prohibitions from 2 December 2026; Annex III high-risk from 2 December 2027; Annex I from 2 August 2028; Article 50(2) grace period to 2 December 2026.

**DT-3 (Must) [impact-deliverable: D-9]:** **[MUST]** Looking up the same label, route and flag shall always return the same dates and duties.
*Check:* Run the same lookup twice; outputs match exactly.

**DT-4 (Should) [impact-deliverable: D-9]:** **[SHOULD]** An entry not checked for more than 90 days shall be flagged as stale wherever it is shown.
*Check:* Set a checked date 91 days back; the entry shows as stale.

**DT-5 (Must) [impact-deliverable: D-9]:** **[MUST]** The owner shall review and approve the table before it is used, and every later change shall be recorded with its reason.
*Check:* The table carries an approval record and a change log.

## Base-Model Bake-off

Zero-shot comparison of candidate base models on the gold set; the owner chooses.

**BO-1 (Must) [impact-deliverable: D-7]:** **[MUST]** The bake-off shall compare four instruction-tuned models under 2B parameters, quantised to 4 bits: Qwen3.5-0.8B, Llama 3.2 1B Instruct, Gemma 3 1B, and EuroLLM-1.7B-Instruct.
*Check:* The results table has four rows, or a recorded exclusion for each missing one (BO-4).
> The owner picked the first three and asked Claude for one neither had considered; Claude proposed EuroLLM (EU-funded, Apache 2.0, all 24 official EU languages).

**BO-2 (Must) [impact-deliverable: D-7]:** **[MUST]** Every candidate shall be run zero-shot on all 100 gold cases with the same prompt (containing the label definitions and the output record) and the same settings. The prompt shall be recorded verbatim with a version.
*Check:* Each result row names the same prompt version and case count.

**BO-3 (Must) [impact-deliverable: D-7]:** **[MUST]** Each candidate shall be scored on: tier accuracy with a 95% interval; format compliance (share of outputs readable as the record); accuracy on answered cases and share answered; mean seconds per case and peak memory on this Mac; and licence and provenance (licence name and restrictions, training-data disclosure, developer and jurisdiction).
*Check:* The results table has all five measures for every candidate.

**BO-4 (Must) [impact-deliverable: D-7]:** **[MUST]** A candidate that cannot run within 8 GB, or has no usable 4-bit build, shall be recorded as excluded with the reason. A community-made build shall be checked against the original model card (size, licence) before use.
*Check:* Every excluded candidate has a reason in the results.

**BO-5 (Must) [impact-deliverable: D-7]:** **[MUST]** The licence and provenance criteria for acceptability to a European compliance audience shall be written down before any candidate's results are seen.
*Check:* The criteria's commit precedes the results' commit.

**BO-6 (Must) [impact-deliverable: D-7]:** **[MUST]** The results shall be presented to the owner as one comparison table with a recommendation and its reasons. The owner chooses the base model; the choice and reason are added to the decisions log.
*Check:* The decisions log has a dated base-model entry.

**BO-7 (Should) [impact-deliverable: D-7]:** **[SHOULD]** Running the same candidate twice on the same cases shall produce the same labels.
*Check:* Repeat one candidate's run; compare labels case by case.

**BO-8 (Could) [impact-deliverable: D-7]:** **[COULD]** If time allows, OLMo 2 1B Instruct (fully open training data, Apache 2.0) shall be added as a fifth candidate under the same conditions.
*Check:* A fifth row exists, or a recorded decision not to run it.

## Evaluation

How results are measured and reported: two numbers for review behaviour (Geifman and El-Yaniv), intervals on everything (Miller), several measures rather than one (Liang et al.).

**EV-1 (Must) [impact-deliverable: D-6]:** **[MUST]** The evaluation shall report overall tier accuracy and a table of gold label against predicted label.
*Check:* On a hand-made set of 10 outputs with known answers, the reported numbers match a hand count.

**EV-2 (Must) [impact-deliverable: D-6]:** **[MUST]** The evaluation shall report accuracy on answered cases and the share of cases answered, counting needs-human-review as not answered; and how often the model says needs-human-review when the gold label says so, and when it does not.
*Check:* On the hand-made set, the four numbers match a hand count.

**EV-3 (Must) [impact-deliverable: D-6]:** **[MUST]** The evaluation shall report Annex III area accuracy on gold cases labelled high-risk through Annex III.
*Check:* Matches a hand count on the hand-made set.

**EV-4 (Must) [impact-deliverable: D-6]:** **[MUST]** The evaluation shall report the share of cited articles that exist in a fixed table of valid articles, and the share of records whose citations overlap the gold citations.
*Check:* An invented article number is counted as invalid.

**EV-5 (Must) [impact-deliverable: D-6]:** **[MUST]** Outputs that cannot be read as the record, and gold cases with no output at all, shall be counted as wrong on every measure and reported separately; they are never excluded from the denominator.
*Check:* Insert one unreadable output; every accuracy falls accordingly.

**EV-6 (Must) [impact-deliverable: D-6]:** **[MUST]** Every proportion shall carry a 95% confidence interval, and the report shall name the interval method used.
*Check:* No reported proportion lacks an interval.
> Miller, Adding Error Bars to Evals.

**EV-7 (Must) [impact-deliverable: D-6]:** **[MUST]** Given two models' outputs on the same cases, the evaluation shall report the difference in accuracy with a 95% interval from a paired method; a gain counts only if the interval excludes zero. If either side lacks outputs for some cases, the comparison shall refuse to run and name the missing cases.
*Check:* Two identical output files give a difference of zero with an interval that contains zero.

**EV-8 (Must) [impact-deliverable: D-6]:** **[MUST]** The evaluation shall report Article 50 flag accuracy, and shall flag any model output that contains a date.
*Check:* An output containing '2 August 2026' is flagged.

**EV-9 (Must) [impact-deliverable: D-6]:** **[MUST]** Each report shall name the model, prompt version, guideline version, gold-set version and date, be saved in the repository, and be identical when re-run on the same inputs.
*Check:* Re-run on the same inputs; the two reports match apart from the run timestamp.

**EV-10 (Should) [impact-deliverable: D-6]:** **[SHOULD]** Each report shall open with a short plain-English summary saying what each number means and what it does not show.
*Check:* The owner can answer, from the summary alone, how often the model was right when it answered.

## Owner-Run Steps

What makes this slice a learning step as well as a build step.

**LG-1 (Should) [impact-deliverable: D-16]:** **[SHOULD]** For the bake-off and the evaluation, the owner shall be given the exact commands to run, one per step, with what to expect on screen and how long it takes.
*Check:* The owner runs the evaluation on one candidate without asking how.

**LG-2 (Must) [impact-deliverable: D-18]:** **[MUST]** Each step in this slice shall produce a learning-log entry with a lesson, a recap and check questions.
*Check:* docs/learning has an entry for each step.

## Deferred to Later Slices

Recorded so the boundary of this slice is explicit (Patton, now versus later).

**WN-1 (Won't):** **[WONT]** Teacher-written training data, the judge filter, training runs and the adapter, the held-out test-set procedure, the standalone citation checker, the local page, the model card and export to Ollama are not in this slice (D-4, D-5, D-8, D-10 to D-15, D-17).
*Check:* Not applicable.

## Non-Functional Requirements

Covered inside the domains: fits in 8 GB and is timed on this Mac (BO-3, BO-4); repeatable (BO-7, DT-3, EV-9); confidentiality (GS-2); honesty about uncertainty (EV-5, EV-6).

## Assumptions

- Claude drafting the gold cases does not leak into training, provided the later teacher model and judge are checked against the gold set (GS-6) and the teacher is not instructed with gold cases.
- The four candidates have usable 4-bit builds for this Mac; if not, BO-4 records it.
- The owner can spend 3 to 6 hours judging the gold set within the deadline.

## Constraints

- Apple M2, 8 GB memory; nothing may require a cloud GPU.
- Public repository: no employer names, internal figures or internal team names, ever; cases are fictional and built from public regulation text.
- Deadline 16 November 2026 for the whole project.
- Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744 is the legal basis; draft Commission guidance is marked as draft.

## Out of Scope

- Legal advice. Outputs are triage, not legal opinions.
- General-purpose AI model obligations (Chapter V) as a tier: the scheme classifies AI systems, not models.
- Languages other than English for case descriptions in this slice.

## Open Questions

- **OQ-1 (decided 2026-10-26 by the owner):** the 100-case gold set is used in full for the bake-off and development. A separate final test set, written later under the same guideline and touched once, measures G-1 (deliverable D-8, a later slice). Reason: 40 cases would give intervals of about plus or minus 15 points, too wide to separate four candidates.
- **OQ-2:** Which areas of Annex III does the owner know least, so the guideline gives them more worked examples?

## Requirements Index

| ID | Domain | Summary | Priority |
|---|---|---|---|
| LS-1 | Label Scheme and Guideline | Six labels, each defined against an article | Must |
| LS-2 | Label Scheme and Guideline | High-risk records its route and Annex III area | Must |
| LS-3 | Label Scheme and Guideline | Separate Article 50 flag | Must |
| LS-4 | Label Scheme and Guideline | Citation and one-sentence reason | Must |
| LS-5 | Label Scheme and Guideline | Fixed decision order with worked examples | Must |
| LS-6 | Label Scheme and Guideline | When to say needs-human-review | Must |
| LS-7 | Label Scheme and Guideline | Versioned guideline | Must |
| LS-8 | Label Scheme and Guideline | Sources for every rule | Must |
| LS-9 | Label Scheme and Guideline | One fixed output record | Must |
| LS-10 | Label Scheme and Guideline | No dates or duty lists in the label record | Must |
| GS-1 | Gold Set and Re-label Check | 100 cases, boundary-weighted | Must |
| GS-2 | Gold Set and Re-label Check | Freshly written, fictional, public sources only | Must |
| GS-3 | Gold Set and Re-label Check | All eight Annex III areas covered | Must |
| GS-4 | Gold Set and Re-label Check | Hard cases are present | Must |
| GS-5 | Gold Set and Re-label Check | Claude drafts, the owner judges every case | Must |
| GS-6 | Gold Set and Re-label Check | Gold set never used for training | Must |
| GS-7 | Gold Set and Re-label Check | Blind re-label of 20 cases | Must |
| GS-8 | Gold Set and Re-label Check | Disagreements settle into the guideline | Must |
| DT-1 | Dates-and-Duties Table | Dates and duties per label | Must |
| DT-2 | Dates-and-Duties Table | Every entry sourced and dated | Must |
| DT-3 | Dates-and-Duties Table | Deterministic lookup | Must |
| DT-4 | Dates-and-Duties Table | Stale entries flagged | Should |
| DT-5 | Dates-and-Duties Table | Reviewed by a human | Must |
| BO-1 | Base-Model Bake-off | Four candidates | Must |
| BO-2 | Base-Model Bake-off | Same conditions for every model | Must |
| BO-3 | Base-Model Bake-off | Five measures per candidate | Must |
| BO-4 | Base-Model Bake-off | Failures recorded, not dropped | Must |
| BO-5 | Base-Model Bake-off | Licence criteria fixed before results | Must |
| BO-6 | Base-Model Bake-off | The owner chooses the base model | Must |
| BO-7 | Base-Model Bake-off | Repeatable runs | Should |
| BO-8 | Base-Model Bake-off | Optional fifth candidate | Could |
| EV-1 | Evaluation | Tier accuracy and confusion table | Must |
| EV-2 | Evaluation | Answered-case accuracy and coverage | Must |
| EV-3 | Evaluation | Annex III area accuracy | Must |
| EV-4 | Evaluation | Citation validity | Must |
| EV-5 | Evaluation | Format failures counted, not dropped | Must |
| EV-6 | Evaluation | Intervals on every number | Must |
| EV-7 | Evaluation | Paired comparison of two models | Must |
| EV-8 | Evaluation | Article 50 flag and dates check | Must |
| EV-9 | Evaluation | Reproducible, identified reports | Must |
| EV-10 | Evaluation | Plain-English summary for the owner | Should |
| LG-1 | Owner-Run Steps | Commands the owner can run | Should |
| LG-2 | Owner-Run Steps | Learning-log entry per step | Must |
| WN-1 | Deferred to Later Slices | Training and everything after it | Won't |

## Priority Model

| Level | Meaning |
|---|---|
| Must | The slice fails its purpose without this. |
| Should | Expected; omit only with a stated reason. |
| Could | Include if time allows. |
| Won't | Deliberately not in this slice. |


## Changelog

| Date | Change | Reason | Author |
|---|---|---|---|
| 2026-10-26 | EV-5: missing outputs count as wrong. DT-1: explicit entry for labels with no tier duties. EV-6: report names its interval method. EV-7: paired comparison refuses incomplete pairs | Requirements health report H-1 to H-4, fixes approved by the owner | owner/AI |

---

*Developed using the Grounded Vibe Methodology*
