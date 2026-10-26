# AI Act Lab — Expert Calibration (init-001)

**Date:** 2026-10-26
**Phase:** `/gvm-init` (Discovery, entry point for a new project)
**Status:** awaiting owner review

*A learning project: fine-tune a small open language model on a laptop to triage AI systems under the EU AI Act. This report records which published authorities will ground every later decision, and why.*

## 1. Executive Summary

**Project:** AI Act Lab.
**Business domain:** two domains at once. A regulated one, EU AI Act compliance (risk-tier triage of AI systems against Regulation (EU) 2024/1689 as amended by the Digital Omnibus on AI, Regulation (EU) 2026/1744). And a technical one, adapting a small open language model with LoRA on an Apple M2 with 8 GB of memory, with honest measurement.

**What this phase does, in plain English.** The Grounded Vibe Methodology does not let the AI assistant make design calls from instinct. Every decision in later phases must cite a named, published authority: a book, a peer-reviewed paper, a regulation or an official guideline. This phase assembles that list, called the expert roster, scores each authority on how trustworthy it is, and writes the result down so the later phases (impact map, requirements, test cases, technical specification, build) read the same list. Think of it as choosing the reference shelf before writing the first page.

**How the roster is organised.**

- *Tier 1, process experts.* How software is specified, built and tested well. Always active. Drawn from the methodology's standard shelf.
- *Tier 2b, industry experts.* The regulation, its interpretation, and the craft of evaluating AI models. Chosen for this project.
- *Tier 2a (software patterns) and Tier 3 (tools and libraries)* are not chosen yet. They are added when the requirements and the technical specification make the stack concrete. For this project that means the `mlx-lm` fine-tuning library, the conversion tools and Ollama; they will be grounded at the tech-spec phase.

**Pre-check.** No earlier initialisation of this project exists: no `init/` folder and no activation-log rows for this repository. Other projects on this machine have added industry files to the shared library; two of them turned out to fit this project and were reused.

**Application brief.** The methodology offers an optional one-page project brief at this point. It was not written separately: `docs/00-plan.md` already answers every question the brief asks (problem, solution, value, existing landscape, solution shape, stakeholders, constraints), so a second copy would drift from the first.

**How the domain question was answered.** The methodology normally asks the owner for the business domain interactively. This run was started by another session with the domain already stated in its brief, so the brief's answer was used. The owner can correct it in review.

**Scope of this phase.** No training code was written, no model downloaded, no Python package installed. The output is this report, a scoring report for the newly proposed experts, and the activation log.

## 2. Process Experts (Tier 1)

**Decision: the standard Tier 1 roster is confirmed unchanged.** The regulated nature of the domain is carried by the Tier 2b experts, not by swapping out the process experts. Nothing in the standard roster conflicts with a data-and-evaluation project; several entries fit it unusually well.

The seventeen Tier 1 experts, and the role each will actually play here:

| Expert | Work | Role on this project |
|---|---|---|
| George Fairbanks | *Just Enough Software Architecture* (2010) | Risk-driven depth: thorough on the label scheme, the gold set and the evaluation harness, where the project can fail; light on everything else |
| Mike Cohn | *Agile Estimating and Planning* (2005); *User Stories Applied* (2004) | Vertical slicing. The first slice stays tiny: label scheme, lookup table, gold set, zero-shot baseline. Training comes later |
| Kent Beck | *Test-Driven Development: By Example* (2002) | Tests first for the deterministic parts: the lookup table, the citation checker, the scorer |
| Andrew Hunt and David Thomas | *The Pragmatic Programmer* (2019 ed.) | Tracer bullets: a thin end-to-end thread (describe a system, get a scored record) before any tuning. DRY for the lookup table as the single source of dates |
| Cem Kaner | *Lessons Learned in Software Testing* (2001) | Realistic test data: the gold set must read like real system descriptions, not toy sentences |
| Boris Beizer | *Software Testing Techniques* (1990) | Bugs cluster at boundaries: the Annex III versus Article 50 boundary gets the most hand-labelling effort |
| Frederick Brooks | *The Mythical Man-Month*; *The Design of Design* | Conceptual integrity: one idea throughout, the model judges, the table knows the dates |
| Michael Keeling | *Design It!* (2017) | Decision records. The decisions log in `docs/00-plan.md` continues in this style |
| Len Bass, Paul Clements, Rick Kazman | *Software Architecture in Practice* (4th ed.); *Documenting Software Architectures* | Quality-attribute scenarios: memory ceiling, run time per training run, accuracy targets stated as measurable scenarios |
| Simon Brown | C4 model | One context diagram when the tech spec is written: owner, model, lookup table, Ollama, local page |
| Martin Fowler | *Refactoring* (2nd ed.); *Patterns of Enterprise Application Architecture* | Anti-bloat lens: keep scripts small and readable |
| Steve McConnell | *Code Complete* (2nd ed.) | Defensive construction: fail loudly on a missing table entry or a malformed model output |
| Robert C. Martin | *Clean Code* (2008) | No swallowed errors in the evaluation harness; a silent failure would fake a result |
| Sandi Metz | *Practical Object-Oriented Design* (2nd ed.) | Test the public behaviour of scripts, not their internals |

Metz and Martin are object-oriented authors and this project is mostly short Python scripts and data files. Their principles still apply, proportionately. No replacement was needed.

## 3. Industry Domain (Tier 2b)

### 3.1 Files activated from the shared library

Two existing industry files match this project and are activated.

**`industry/ai-governance.md`.** Holds the EU AI Act itself (scored Canonical), the NIST AI Risk Management Framework, several financial-sector model-risk standards, and five practitioners. The entries that matter most here:

- *EU AI Act, Regulation (EU) 2024/1689.* The primary source for the label scheme, the Annex III categories and the article citations.
- *NIST AI RMF.* Its Measure function is the reminder that a claim is tested, not asserted. The project's measurement plan follows that.
- *Margaret Mitchell et al., Model Cards.* The shipped model gets a model card: intended use, out-of-scope use, evaluation data, disaggregated results, caveats. The README's honesty paragraph becomes that card.
- *Michael Power, The Audit Society.* Guards against verification theatre. A citation that looks right is not a citation that is right; the citation checker tests against a fixed table.
- *Cathy O'Neil and Virginia Eubanks.* The harm lens for writing cases: who is affected when a system is misclassified as minimal risk.
- *OWASP Top 10 for LLM Applications.* A system description typed by a user is untrusted text. Prompt injection inside a description is a test case, not an afterthought.

The entries on US, UK, Singaporean and Canadian banking supervision (SR 26-2, SS1/23, FEAT, E-23) are loaded with the file but are not expected to be cited; the project is not sector-specific.

**`industry/ai-evaluation.md`.** The craft of measuring models honestly. The entries that matter most here:

- *Sayash Kapoor and Arvind Narayanan, Leakage and the Reproducibility Crisis.* The test set is touched once. Teacher-written training cases must not paraphrase gold cases. Leakage checks are a requirement, not a hope.
- *Percy Liang et al., HELM.* One headline number hides trade-offs. The project reports tier accuracy, category accuracy, citation validity and review behaviour separately, and names what was not evaluated.
- *Lianmin Zheng et al., Judging LLM-as-a-Judge.* The judge pass that filters synthetic cases is itself a model with biases. Its agreement with the owner's gold labels is measured before it is trusted.
- *Deborah Raji et al., Closing the AI Accountability Gap.* Write the evaluation scope before running it, so coverage cannot be claimed after the fact.
- *Mitchell, Model Cards* (also here) and *NIST AI RMF* (also here).
- *UK AI Security Institute, Inspect* and *METR* describe evaluation infrastructure at a scale this project does not need; loaded, unlikely to be cited.

**Files considered and not activated.** `model-risk.md` (bank model-validation standards; useful vocabulary but sector-specific, and the project deliberately carries no sector), `forecast-verification.md`, `world-models.md`, `predictive-neuroscience.md` (unrelated).

**Two housekeeping notes on the shared library, flagged, not changed.** The EU AI Act entry describes the Digital Omnibus as a "provisional agreement, May 2026"; it has since been adopted as Regulation (EU) 2026/1744, in force 27 July 2026. This is exactly why the project keeps dates in a lookup table and not in prose or weights; the project's table, not the library entry, is the source of truth for dates. Second, Margaret Mitchell and the NIST AI RMF each carry a full score block in both files, which the methodology's single-canonical-source rule says should be a cross-reference. Noted for `/gvm-experts`.

### 3.2 Coverage gaps and the experts proposed to fill them

The two activated files cover the regulation and the general craft of evaluation. Checked against what this project actually has to do, eight gaps remained. Ten experts are proposed to fill them. Each was scored twice, independently, and the scores reconciled; the full record with evidence is in `scoring-reports/expert-scoring-001.md`. **None has been written into the shared library yet. That happens when the owner approves this report.**

| Gap | What the project needs | Proposed expert | Classification |
|---|---|---|---|
| Interpreting the Act's classification rules | Official tests for "is this an AI system" and "is this prohibited", with worked examples | European Commission (AI Office), AI Act guidelines | Canonical |
| Evidence on legal-text classification by language models | What small models have achieved on EU legal classification, and how labels behave in hierarchies | Ilias Chalkidis et al., LexGLUE and MultiEURLEX | Established |
| Building the hand-checked gold set | A method for writing the labelling guideline, measuring agreement and adjudicating | James Pustejovsky and Amber Stubbs, *Natural Language Annotation for Machine Learning* | Recognised |
| The fine-tuning technique | What LoRA does, which knobs matter, why the adapter is small | Edward J. Hu et al., *LoRA* | Established (work: Canonical) |
| Fitting training in 8 GB | Why a 4-bit base with adapters matches full-precision quality, and what to compare against | Tim Dettmers et al., *QLoRA* | Established (work: Canonical) |
| Writing training cases with a teacher model | How teacher-written data is generated, de-duplicated and filtered; how few good cases can be enough | Yizhong Wang et al., *Self-Instruct*; Chunting Zhou et al., *LIMA* | Established; Established |
| Measuring "needs human review" honestly | The reject option: coverage against error on answered cases | Yonatan Geifman and Ran El-Yaniv, selective classification | Established |
| Teaching the craft as we go | Practical, current guides that explain the mechanism in plain terms | Sebastian Raschka, *Build a Large Language Model (From Scratch)*; Chip Huyen, *AI Engineering* | Established; Established |

**Where each would be filed.** The Commission guidelines join the EU AI Act entry in `industry/ai-governance.md`. Chalkidis, Pustejovsky and Stubbs, and Geifman and El-Yaniv join `industry/ai-evaluation.md`, because benchmarks, gold sets and abstention are evaluation concerns. Hu, Dettmers, Zhou, Wang, Raschka and Huyen go into a new file, `industry/llm-fine-tuning.md`, for the craft of adapting small language models. The new file follows the same append-only convention as the others.

**Four boundary cases.** Where the two scoring passes disagreed on the band, the lower integer was recorded and the entry flagged: Dettmers (expert score, Established versus Canonical), *LIMA* (Recognised versus Established), *SelectiveNet* (Recognised versus Established), *AI Engineering* (Established versus Canonical). None changes how the expert is used.

**One finding from verification worth knowing now.** The Commission's guidelines on classifying high-risk systems under Article 6 exist only as a draft, published for consultation on 19 May 2026, with no final text found as of today. The definition guidelines and the prohibited-practices guidelines are final (February 2025). The label scheme in the requirements phase will therefore rest on the Act's text and the draft, and say so.

**What each proposed expert will govern on this project.**

*European Commission (AI Office), AI Act guidelines.* Definition first: a described system that fails the seven-element test for "AI system" is out of scope, which is a different answer from "minimal risk", and the label scheme must handle it. Prohibitions are illustrated, not just listed: the prohibited-practices guidelines supply the worked examples for prohibited cases in the gold set. The two prohibitions the Omnibus added apply from 2 December 2026 and post-date the guidelines; cases for them come from the amended Act text. Where guidance and the amended text differ, the text wins and the lookup table records the date checked.

*Ilias Chalkidis et al.* Legal labels come in hierarchies, and performance differs by level; Annex III has areas and sub-points, so score both. Fine-tuned small models have a track record on legal classification, so expect weak zero-shot numbers from small instruct models and a large gain from fine-tuning, which the baseline makes visible. The benchmarks predate instruction-tuned models; use them to set expectations, not as the target.

*James Pustejovsky and Amber Stubbs.* The MATTER cycle: Model, Annotate, Train and Test, Evaluate, Revise. The labelling guideline is written before any case is labelled, with decision rules and examples, and revised when labelling exposes gaps. A gold standard is adjudicated, not single-pass: measure agreement on a sample (a second rater, or the owner re-labelling blind after a gap) and feed the disagreements back into the guideline. Every gold case records which guideline version labelled it.

*Edward J. Hu et al., LoRA.* Freeze the base, train small low-rank update matrices alongside selected weights. Rank 4 to 16 was enough in the paper, which is why the adapter is a few megabytes against hundreds for the base. The knobs are rank, which matrices get adapters, and the scaling factor; every notebook entry records them. Adapters merge back into the base at no inference cost, which is what makes the later export step possible.

*Tim Dettmers et al., QLoRA.* A 4-bit base with LoRA adapters matched 16-bit fine-tuning quality in the paper's benchmarks at a fraction of the memory; this is the design that fits 8 GB. Quantisation error is small but not zero, so the fine-tuned 4-bit model is compared against the untuned model at the same precision. Their best results came from a small curated dataset, not the largest one.

*Chunting Zhou et al., LIMA.* One thousand carefully curated examples produced strong results on a 65-billion-parameter base: the model already holds the knowledge, and fine-tuning teaches format and behaviour. This is the published support for "the model learns judgement and format, not dates". The caveat travels with the claim: a 0.8-billion-parameter model holds less, so the project expects to need more examples and measures rather than assumes. Diversity in the set mattered more than volume.

*Yizhong Wang et al., Self-Instruct.* A model can write its own training data if the pipeline filters for diversity and quality; the paper dropped near-duplicates and malformed outputs before training. Keep the rejection statistics: the share of teacher-written cases the judge removes is a measurement, and a rising share is a warning about the teacher prompt. Teacher-written data inherits the teacher's blind spots; the gold set, not the teacher, is the ground truth.

*Yonatan Geifman and Ran El-Yaniv, selective classification.* A classifier with a reject option trades coverage (the share of cases it answers) against selective risk (its error rate on those it answers). "Needs human review" is a reject option. Report the two numbers together, because accuracy alone can be bought by refusing everything. Set the operating point from the target, nine in ten right on answered cases, and measure how much review that costs.

*Sebastian Raschka.* Settings that work in practice: a scaling factor about twice the rank, adapters on all linear layers rather than attention only, few epochs on small sets, and scoring the task rather than trusting the loss. These become the notebook's starting defaults, changed one at a time. His book supplies the plain-English explanations of tokens, attention and fine-tuning stages that the teaching rule needs.

*Chip Huyen.* Fine-tune for behaviour and format, retrieve for facts: the book's framing of when to fine-tune, prompt or retrieve is the published version of the project's main design rule. Evaluation-driven development: define the measurement before building the thing measured. Synthetic data is engineered, with generation, verification and filtering as separate steps.

### 3.3 Recall check: what a blind enumeration found

Scoring only tests the names put forward. To test the names left out, a separate agent was asked, without sight of the roster, to list the most-cited authorities in four fields: EU AI Act classification; parameter-efficient fine-tuning and synthetic data; honest evaluation including abstention; and gold-set annotation. It returned 48 entries. Compared with the roster:

**Already covered.** The Act, the two final Commission guidelines, the draft Article 6 guidelines, LoRA, QLoRA, Self-Instruct, LIMA, LLM-as-judge bias (Zheng), leakage (Kapoor and Narayanan), selective classification (Geifman and El-Yaniv, with Chow's 1970 reject option as lineage), Pustejovsky and Stubbs, and LexGLUE. The blind list's top entries in every field are on the roster.

**Absent, and recommended for addition at the phase where they become concrete.** Each would be scored and approved then, not now.

| Authority | Why it matters here | Phase |
|---|---|---|
| Ron Artstein and Massimo Poesio, *Inter-Coder Agreement for Computational Linguistics* (2008) | The definitive guide to agreement measures for the gold-set check | Requirements |
| Paul Röttger et al., *Two Contrasting Data Annotation Paradigms* (2022) | A legal triage guideline is prescriptive; this names the choice and its consequences | Requirements |
| Evan Miller, *Adding Error Bars to Evals* (2024), with Dietterich (1998) | A 100-case test set gives wide confidence intervals; honesty requires reporting them | Requirements |
| Amita Kamath, Robin Jia and Percy Liang, *Selective Question Answering under Domain Shift* (2020) | Abstention metrics as used in NLP: coverage at a fixed accuracy | Requirements |
| Hanning Zhang et al., *R-Tuning* (2024); Bingbing Wen et al., abstention survey (2025) | How to train a model to say "I don't know" as a label, which is what "needs human review" is | Tech spec |
| Dan Biderman et al., *LoRA Learns Less and Forgets Less* (2024); John Schulman et al., *LoRA Without Regret* (2025) | Honest limits of LoRA and current hyperparameter guidance | Tech spec |
| Lichang Chen et al., *AlpaGasus* (2024); Wei Liu et al., *DEITA* (2024) | Judge-based filtering of teacher-written data, which is the planned judge pass | Tech spec |
| Cheng-Yu Hsieh et al., *Distilling Step-by-Step* (2023) | Distilling a rationale into a small model; the output includes a one-sentence reason | Tech spec |
| Neel Guha et al., *LegalBench* (2023) | The current legal-reasoning benchmark, more recent than LexGLUE | Requirements (bake-off design) |
| Pehlivan, Forgó and Valcke (eds.), *The EU Artificial Intelligence (AI) Act: A Commentary* (2024); Veale and Zuiderveen Borgesius (2021) | Per-article interpretation when writing the labelling guideline, if the owner has access | Requirements |
| AI Office, *Code of Practice on Transparency of AI-Generated Content* (reported final June 2026) | Source for Article 50 transparency cases; status to be verified first | Requirements |
| Arnav Gudibande et al., *The False Promise of Imitating Proprietary LLMs* (2024); Ilia Shumailov et al., model collapse (2024) | The cautions an honest write-up of teacher-generated data should acknowledge | Documentation |

**Noted, not needed for a triage model.** Harmonised standards and management-system standards (CEN-CENELEC JTC 21, ISO/IEC 42001, ISO/IEC 23894) concern obligations after classification, not the classification itself. The academic risk-assessment literature on the Act (Novelli et al., Almada and Petit, Schuett, Laux and colleagues) is about Article 9, not triage. LoRA's successors and the adapter lineage (DoRA, LoRA+, PiSSA; Houlsby, Li and Liang, Lester) and the PEFT library belong to the tech spec if the chosen library supports them. Calibration and verbalised-confidence work (Guo et al., Kadavath et al., Xiong et al.) becomes relevant only if review is triggered by a confidence threshold rather than a learned label. The kappa originals (Cohen, Fleiss, Krippendorff), annotation-campaign texts (Fort; Hovy and Lavid), model-based adjudication (Dawid and Skene; Paun et al.), the annotation-quality audit by Klie et al. (2024), and the legal corpora (CUAD, CLAUDETTE, OPP-115) are useful background that Artstein and Poesio, and Pustejovsky and Stubbs, already summarise for a project of this size. Work on LLM annotators needing human validation (Gilardi et al.; Pangakis et al.) restates a rule the project already has.

**Authority scored 3 or lower.** The recall rule also asks for present experts with a low Authority score. Only METR (Authority 3) qualifies; it is peripheral here.

**One discrepancy to carry forward.** The recall agent's sources disagreed on the Digital Omnibus's final adoption and application dates, and it did not check the consolidated text. The project plan records Regulation (EU) 2026/1744 as in force from 27 July 2026, from the research session that started the project. That stands, and the lookup-table requirement will include re-verifying every date against the Official Journal, with the date checked recorded in the table.

### 3.4 Deferred to later phases

Not chosen now, by design:

- *Tier 2a, software patterns.* Activated during requirements and tech spec as patterns emerge. Likely candidates: `domain/data-intensive.md` (Kleppmann) for the dataset files and splits, `domain/security.md` for the untrusted-input surface, `domain/user-documentation.md` for the owner-facing explanations.
- *Tier 3, tools and libraries.* Activated at tech spec when the stack is fixed. The shared library has a Python file (Ramalho, Percival and Gregory). It has nothing yet for `mlx-lm` and Apple's MLX framework, Hugging Face PEFT, the llama.cpp GGUF converter or Ollama; those will be discovered and scored then, from their official documentation and maintainers.
- *Base-model choice.* Deliberately not an expert question. The owner asked why Qwen is always the default. The answer will be a measured bake-off on the gold set between at least three candidates under two billion parameters, scored on zero-shot tier accuracy, output-format compliance, speed on this Mac, and licence and provenance acceptability for a European compliance audience. That is written into the requirements, not decided here.

## 4. Expert Roster Summary

Every expert active for this project. Downstream phases read this table.

| Expert Name | Work | Tier | Classification | Reference File | Status |
|---|---|---|---|---|---|
| Paul Clements | *Documenting Software Architectures* (2nd ed.) | tier1 | Established | architecture-specialists.md | existing |
| Simon Brown | *Software Architecture for Developers*; C4 model | tier1 | Established | architecture-specialists.md | existing |
| George Fairbanks | *Just Enough Software Architecture* | tier1 | Recognised | architecture-specialists.md | existing |
| Michael Keeling | *Design It!* | tier1 | Recognised | architecture-specialists.md | existing |
| Len Bass | *Software Architecture in Practice* (4th ed.) | tier1 | Canonical | architecture-specialists.md | existing |
| Rick Kazman | *Software Architecture in Practice* (4th ed.) | tier1 | Canonical | architecture-specialists.md | existing |
| Frederick Brooks | *The Mythical Man-Month*; *The Design of Design* | tier1 | Canonical | architecture-specialists.md | existing |
| Martin Fowler | *Refactoring* (2nd ed.); *Patterns of Enterprise Application Architecture* | tier1 | Canonical | architecture-specialists.md | existing |
| Steve McConnell | *Code Complete* (2nd ed.) | tier1 | Established | architecture-specialists.md | existing |
| Robert C. Martin | *Clean Code* | tier1 | Established | architecture-specialists.md | existing |
| Andrew Hunt | *The Pragmatic Programmer* (20th anniversary ed.) | tier1 | Established | architecture-specialists.md | existing |
| David Thomas | *The Pragmatic Programmer* (20th anniversary ed.) | tier1 | Established | architecture-specialists.md | existing |
| Kent Beck | *Test-Driven Development: By Example* | tier1 | Canonical | architecture-specialists.md | existing |
| Sandi Metz | *Practical Object-Oriented Design* (2nd ed.) | tier1 | Established | architecture-specialists.md | existing |
| Boris Beizer | *Software Testing Techniques* (2nd ed.) | tier1 | Recognised | architecture-specialists.md | existing |
| Cem Kaner | *Lessons Learned in Software Testing* | tier1 | Recognised | architecture-specialists.md | existing |
| Mike Cohn | *Agile Estimating and Planning*; *User Stories Applied* | tier1 | Established | architecture-specialists.md | existing |
| EU AI Act | Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744 | tier2b | Canonical | industry/ai-governance.md | existing |
| NIST | *AI Risk Management Framework 1.0* | tier2b | Canonical | industry/ai-governance.md (also scored in ai-evaluation.md) | existing |
| Federal Reserve / OCC / FDIC | SR 26-2 | tier2b | Canonical | industry/ai-governance.md | existing |
| PRA | SS1/23 | tier2b | Canonical | industry/ai-governance.md (scored in model-risk.md) | existing |
| MAS | FEAT Principles | tier2b | Established | industry/ai-governance.md | existing |
| OSFI | Guideline E-23 | tier2b | Canonical | industry/ai-governance.md | existing |
| OWASP | *Top 10 for LLM Applications* | tier2b | Established | industry/ai-governance.md | existing |
| Michael Power | *The Audit Society* | tier2b | Established | industry/ai-governance.md | existing |
| Margaret Mitchell et al. | *Model Cards for Model Reporting* | tier2b | Established | industry/ai-governance.md (also scored in ai-evaluation.md) | existing |
| Cathy O'Neil | *Weapons of Math Destruction* | tier2b | Established | industry/ai-governance.md | existing |
| Stuart Russell | *Human Compatible* | tier2b | Established | industry/ai-governance.md | existing |
| Virginia Eubanks | *Automating Inequality* | tier2b | Established | industry/ai-governance.md | existing |
| Deborah Raji et al. | *Closing the AI Accountability Gap* | tier2b | Established | industry/ai-evaluation.md | existing |
| Percy Liang et al. | *Holistic Evaluation of Language Models* | tier2b | Established | industry/ai-evaluation.md | existing |
| Sayash Kapoor and Arvind Narayanan | *Leakage and the Reproducibility Crisis*; *AI Snake Oil* | tier2b | Established | industry/ai-evaluation.md | existing |
| Lianmin Zheng et al. | *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* | tier2b | Established | industry/ai-evaluation.md | existing |
| Anthropic | *Responsible Scaling Policy* (as representative of frontier-lab risk policies) | tier2b | Recognised | industry/ai-evaluation.md | existing |
| METR | Autonomous-capability evaluation methodology | tier2b | Recognised | industry/ai-evaluation.md | existing |
| UK AI Security Institute | Inspect | tier2b | Established | industry/ai-evaluation.md | existing |
| European Commission (AI Office) | AI Act guidelines: definition of an AI system, C(2025) 924; prohibited practices, C(2025) 884 | tier2b | Canonical | industry/ai-governance.md (proposed) | newly scored (pending owner approval) |
| Ilias Chalkidis et al. | *LexGLUE*; *MultiEURLEX* | tier2b | Established | industry/ai-evaluation.md (proposed) | newly scored (pending owner approval) |
| James Pustejovsky and Amber Stubbs | *Natural Language Annotation for Machine Learning* | tier2b | Recognised | industry/ai-evaluation.md (proposed) | newly scored (pending owner approval) |
| Yonatan Geifman and Ran El-Yaniv | *Selective Classification for Deep Neural Networks*; *SelectiveNet* | tier2b | Established | industry/ai-evaluation.md (proposed) | newly scored (pending owner approval) |
| Edward J. Hu et al. | *LoRA: Low-Rank Adaptation of Large Language Models* | tier2b | Established | industry/llm-fine-tuning.md (proposed, new file) | newly scored (pending owner approval) |
| Tim Dettmers et al. | *QLoRA: Efficient Finetuning of Quantized LLMs* | tier2b | Established | industry/llm-fine-tuning.md (proposed, new file) | newly scored (pending owner approval) |
| Chunting Zhou et al. | *LIMA: Less Is More for Alignment* | tier2b | Established | industry/llm-fine-tuning.md (proposed, new file) | newly scored (pending owner approval) |
| Yizhong Wang et al. | *Self-Instruct* | tier2b | Established | industry/llm-fine-tuning.md (proposed, new file) | newly scored (pending owner approval) |
| Sebastian Raschka | *Build a Large Language Model (From Scratch)*; *Practical Tips for Finetuning LLMs Using LoRA* | tier2b | Established | industry/llm-fine-tuning.md (proposed, new file) | newly scored (pending owner approval) |
| Chip Huyen | *AI Engineering* | tier2b | Established | industry/llm-fine-tuning.md (proposed, new file) | newly scored (pending owner approval) |

Reference files live in the methodology's shared library on this machine, outside the repository; the paths are relative to its `references/` folder.

## 5. Activation Log

The activation log already existed on this machine, created on 2026-05-31 by an earlier project, so it was not initialised anew. This calibration appended one `loaded` row for each of the thirty-six experts in the three reference files read, and one `cited` row for each expert named in this report, all tagged with this repository's path. The log lives at `~/.claude/gvm/expert-activations.csv`, outside the repository, and records nothing confidential: timestamps, this project's folder path, expert names and works.

## 6. Next Steps

**Next command: `/gvm-impact-map`.** The methodology's order is init, impact map, requirements. The impact map comes before requirements so that every requirement can later be traced to a goal and an actor, which is how scope creep is caught early.

**What the impact map will ask of the owner, in plain English.** Four questions, each answered in a table:

1. *Why.* The goal, in measurable terms. For a learning project there are two goals in tension: the owner learns the craft of training and evaluating a small model, and the model reaches a stated accuracy on clean descriptions while handing the rest to a human. The owner will be asked how "learned the craft" will be judged.
2. *Who.* The actors whose behaviour has to change for the goal to be met: the owner as learner and labeller; a reader of a triage result; whoever handles a "needs human review" output; and, indirectly, anyone affected by a misclassified system. The owner will be asked whether anyone other than the owner will ever use the model.
3. *How.* The impacts: what each actor does differently once the deliverables exist.
4. *What.* The deliverables that cause those impacts, which the requirements phase then details: the label scheme, the dates-and-duties lookup table, the gold set, the baseline measurement, and only later the trained adapter.

**Before the impact map, two decisions from the owner on this report.** First, approve or amend the ten proposed experts; on approval they are written into the shared library and this table's "proposed" markers are removed with a changelog entry. Second, confirm the business-domain statement in section 1.

**Learning log.** The lesson for this step, the terms it introduced, the decision that is the owner's, and three check questions are in `docs/learning/001-expert-calibration.md`, the first entry of the owner's own textbook.

**Configured later.** Stack specialists (Tier 3) at `/gvm-tech-spec`; software-pattern specialists (Tier 2a) as requirements expose them.

---

*Developed using the Grounded Vibe Methodology*
