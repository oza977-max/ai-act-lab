# AI Act Lab — Expert library additions 001

**Date:** 2026-10-26
**Approved by:** the owner, 2026-10-26
**Written to:** the GVM methodology's shared expert library on this Mac (`~/.claude/skills/gvm-design-system/references/`), which is outside this repository and has no remote.

*This file is the project's own record of exactly what was added to the shared library, so that this repository's history shows it, and so the entries can be restored if a methodology update overwrites the library. Scores and evidence: `scoring-reports/expert-scoring-001.md` (first ten) and `scoring-reports/expert-scoring-002.md` (second ten).*

## Where each entry went

| Library file | Entries |
|---|---|
| `industry/ai-governance.md` | European Commission (AI Office) |
| `industry/ai-evaluation.md` | Ilias Chalkidis et al.; James Pustejovsky & Amber Stubbs; Yonatan Geifman & Ran El-Yaniv; Evan Miller; Athanasios Davvetas et al. |
| `industry/llm-fine-tuning.md` | Edward J. Hu et al.; Tim Dettmers et al.; Chunting Zhou et al.; Yizhong Wang et al.; Zhenyan Lu et al.; Ricardo Dominguez-Olmedo et al.; Zorik Gekhman et al.; Dan Biderman et al.; Yu-Ang Lee et al.; Hanning Zhang et al.; Sebastian Raschka; Chip Huyen |
| `domain/ai-assisted-development.md` | METR; Addy Osmani |

The index `domain-specialists.md` gained one row for `domain/ai-assisted-development.md`.

## `industry/ai-governance.md`

### European Commission (AI Office) — AI Act Guidelines

**Source:** European Commission, *Guidelines on the definition of an artificial intelligence system established by Regulation (EU) 2024/1689*, C(2025) 924 final (6 February 2025); *Guidelines on prohibited artificial intelligence practices established by Regulation (EU) 2024/1689*, C(2025) 884 final (4 February 2025). Related, not scored: draft *Guidelines on the classification of high-risk AI systems under Article 6*, published for consultation 19 May 2026, not final as of 26 October 2026.

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 5 | 5 | 4 | 5 | 5 | **Canonical** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — the regulator; Article 96 mandates these guidelines. Publication — numbered Commission acts (C(2025) series) in the Commission's digital-strategy library. Breadth — definition, Article 5, general-purpose models (July 2025), Article 6 in draft; not 5 while Article 6 is unfinished. Adoption — national market-surveillance authorities and compliance programmes work from them. Currency — Article 6 draft May 2026.

**Work score — *Guidelines on the definition of an AI system, C(2025) 924*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 3 | 4 | 4 | **Established** |

Evidence: Specificity — seven elements of Article 3(1) with named out-of-scope examples. Currency — February 2025, unaffected by the Omnibus. Influence — the first gate in AI Act scoping; non-binding.

**Work score — *Guidelines on prohibited AI practices, C(2025) 884*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 5 | 5 | 4 | 4 | **Canonical** |

Evidence: Specificity — practice-by-practice tests with in-scope and out-of-scope examples. Depth — roughly 140 pages, including interplay with GDPR, DSA and consumer law. Currency — February 2025; predates the two Omnibus prohibitions. Influence — the operative Article 5 reference. Average 4.5 classifies upward.

**Activation signals:** EU AI Act scoping, 'is this an AI system', Article 5 prohibitions, Article 6 high-risk classification, interpreting the Act's text, official guidance status

**Key principles:**

- **Definition first** — the definition guidelines break Article 3(1) into seven elements (machine-based system, autonomy, possible adaptiveness, explicit or implicit objectives, inference, outputs, influence on environments) and name what falls outside (basic data processing, classical heuristics, simple prediction). A system that fails the test is out of scope, which is a different answer from minimal risk.
- **Prohibitions are illustrated, not just listed** — the prohibited-practices guidelines give practice-by-practice tests with in-scope and out-of-scope examples for each Article 5 item; they are the worked-example source for prohibited cases.
- **Guidance can lag the law** — both final guidelines (February 2025) predate the Digital Omnibus (Regulation (EU) 2026/1744); the two prohibitions it added apply from 2 December 2026 and are not covered. Where guidance and the amended text differ, the text wins.
- **Article 6 guidance is a draft** — the high-risk classification guidelines were published in draft for consultation on 19 May 2026; no final text as of 26 October 2026. Anything resting on them says so and records the date checked.

---

## `industry/ai-evaluation.md`

### Ilias Chalkidis et al. — Legal Text Classification Benchmarks

**Source:** Chalkidis, Jana, Hartung, Bommarito, Androutsopoulos, Katz, Aletras, *"LexGLUE: A Benchmark Dataset for Legal Language Understanding in English"*, ACL 2022; Chalkidis, Fergadiotis, Androutsopoulos, *"MultiEURLEX: A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer"*, EMNLP 2021

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 5 | 3 | 4 | 3 | **Established** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — lead author of LEGAL-BERT, LexGLUE and MultiEURLEX; co-organiser of the Natural Legal Language Processing workshops. Publication — ACL, EMNLP, NAACL and ICAIL main tracks. Adoption — LEGAL-BERT cited in the thousands; LexGLUE and MultiEURLEX are standard Hugging Face legal datasets.

**Work score — *LexGLUE*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 4 | 3 | 4 | **Established** |

Evidence: Specificity — seven defined tasks, fixed splits, public leaderboard. Depth — a dozen encoders benchmarked with per-task analysis. Influence — several hundred citations; the default legal-NLP benchmark before LegalBench.

**Work score — *MultiEURLEX*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 3 | 3 | 3 | **Recognised** |

Evidence: Specificity — 65,000 EU laws in 23 languages with hierarchical EUROVOC labels and a zero-shot transfer protocol.

**Activation signals:** Legal-text classification, legal NLP benchmarks, hierarchical legal labels, EU law datasets, expectation-setting for legal model performance

**Key principles:**

- **Legal labels come in hierarchies** — MultiEURLEX classifies EU law against EUROVOC concept levels and performance differs by level; score both the coarse and the fine label.
- **Fine-tuned small models have a track record on legal classification** — LexGLUE showed fine-tuned small encoders competitive on legal tasks; expect weak zero-shot numbers and a visible fine-tuning gain.
- **Benchmarks age** — both predate instruction-tuned decoder models; use them to set expectations, not as targets.

---

### James Pustejovsky & Amber Stubbs — Annotation for Machine Learning

**Source:** James Pustejovsky and Amber Stubbs, *Natural Language Annotation for Machine Learning*, O'Reilly (2012)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 4 | 3 | 4 | 2 | **Recognised** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — Pustejovsky is TJX Feldberg Professor at Brandeis, author of the Generative Lexicon, lead designer of TimeML. Publication — O'Reilly, with MIT Press and ACL/LREC for the underlying research. Adoption — the MATTER cycle is standard teaching material for corpus annotation. Currency 2 reflects the 2012 date.

**Work score — *Natural Language Annotation for Machine Learning*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 4 | 2 | 4 | **Established** |

Evidence: Specificity — specification writing, guideline drafting, agreement computation, worked TimeML case. Depth — the whole annotate-train-evaluate-revise loop. Influence — cited in the thousands; the standard annotation-method reference.

**Activation signals:** Annotation guidelines, gold-standard datasets, inter-annotator agreement, adjudication, label scheme design, MATTER cycle

**Key principles:**

- **MATTER: Model, Annotate, Train and Test, Evaluate, Revise** — the label scheme (the model of the phenomenon) is written before any case is labelled, with decision rules and examples, and revised when labelling exposes gaps.
- **A gold standard is adjudicated, not single-pass** — measure agreement on a sample (a second rater, or the same rater blind after a gap), adjudicate disagreements, feed resolutions back into the guideline.
- **Version the guideline with the data** — every gold item records which guideline version labelled it, so a later revision does not silently invalidate earlier labels.

---

### Yonatan Geifman & Ran El-Yaniv — Selective Classification

**Source:** Geifman and El-Yaniv, *"Selective Classification for Deep Neural Networks"*, NeurIPS 2017; *"SelectiveNet: A Deep Neural Network with an Integrated Reject Option"*, ICML 2019. Lineage, not scored: C. K. Chow, *"On optimum recognition error and reject tradeoff"*, IEEE Transactions on Information Theory (1970)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 5 | 3 | 3 | 3 | **Established** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — El-Yaniv, Technion professor who established selective prediction for deep networks; Geifman co-founded Deci AI. Publication — NeurIPS, ICML, ICLR.

**Work score — *Selective Classification for Deep Neural Networks*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 3 | 3 | 4 | **Established** |

Evidence: Specificity — an explicit algorithm choosing a confidence threshold that meets a target risk with a stated guarantee. Influence — cited in the thousands; defines the framework later abstention work uses.

**Work score — *SelectiveNet*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 3 | 3 | 3 | **Recognised** |

Evidence: Specificity — a concrete architecture with a selection head and a coverage-constrained loss. Boundary case: the independent pass placed the work at 3.5 (Established).

**Activation signals:** Abstention, reject option, 'needs human review', selective prediction, coverage versus risk, operating point

**Key principles:**

- **Coverage and selective risk are reported together** — a classifier with a reject option trades the share of cases it answers against its error rate on those it answers; accuracy alone can be bought by refusing everything.
- **Pick the operating point from the target** — choose the threshold that meets a stated risk (for example, at most one error in ten on answered cases) and measure the coverage that costs.
- **Risk-coverage curves, not single numbers** — the curve shows the whole trade-off; report it when abstention is a designed output.

---

### Evan Miller — Error Bars for Evals

**Source:** Evan Miller (Anthropic), *"Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations"*, arXiv 2411.00640 (November 2024), preprint

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 3 | 2 | 3 | 4 | 4 | **Recognised** |

Evidence (scoring-reports/expert-scoring-002.md in the AI Act Lab project, dual-pass verified, splits resolved down): Adoption — his A/B-test sample-size calculators and 'How Not To Run an A/B Test' are common industry references (split 4/5). Currency — 2024 paper (split 5/4). Authority 3 (split 3/4). Boundary case: the independent pass averaged 3.6 (Established).

**Work score — *Adding Error Bars to Evals*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 5 | 3 | 4 | 4 | **Established** |

Evidence: Specificity — ready-to-use formulas for standard errors, clustered errors, paired comparisons, power and sample size. Currency — methods not tied to a model generation (split 5/4). Influence — companion Anthropic research post; implemented in an open package. Depth 3 (split 3/4).

**Activation signals:** Confidence intervals for evaluations, small test sets, paired model comparison, statistical power, error bars

**Key principles:**

- **Every eval score is an estimate with a standard error** — treat the test set as a sample and report a confidence interval, not a bare number.
- **Compare models on the same questions with paired differences** — pairing removes question difficulty from the comparison and narrows the interval.
- **Cluster when questions come in groups** — related items are not independent; clustered standard errors are wider and honest.
- **Decide the sample size before running** — a power calculation says what difference the test set can detect; a 100-item set at 80% accuracy has a 95% interval of roughly plus or minus 8 points.

---

### Athanasios Davvetas et al. — AI Act Evaluation Benchmark

**Source:** Athanasios Davvetas, Michael Papademas, Xenia Ziouvelou, Vangelis Karkaletsis (NCSR "Demokritos" and Panteion University), *"AI Act Evaluation Benchmark: An Open, Transparent, and Reproducible Evaluation Dataset for NLP and RAG Systems"*, arXiv 2603.09435 (March 2026), preprint; data on GitHub (davidath/ai-act-evaluation-benchmark)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 2 | 2 | 2 | 1 | 5 | **Emerging** |

Evidence (scoring-reports/expert-scoring-002.md in the AI Act Lab project, dual-pass verified, splits resolved down): Currency — March 2026. Boundary case: the independent pass averaged 3.2 (Recognised); recorded Emerging on the lower-integer rule.

**Work score — *AI Act Evaluation Benchmark*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 3 | 5 | 1 | **Recognised** |

Evidence: Specificity — 339 scenarios (70 prohibited, 86 high-risk, 84 limited, 99 minimal), 3,350 linked articles, 3,572 obligation points, machine-readable (split 4/5). Currency — March 2026. Caveats stated by the paper: generated with gpt-oss-120b, only qualitative human checks on some entries, legal-expert validation still needed; no dataset licence stated. Boundary case: the independent pass averaged 3.5 (Established).

**Activation signals:** EU AI Act risk-tier classification benchmark, external yardstick, AI Act scenario datasets, retrieval baselines

**Key principles:**

- **An external yardstick exists for AI Act tier classification** — 339 generated scenarios labelled prohibited, high-risk, limited or minimal, with article retrieval.
- **The task is hard and uneven** — the retrieval baseline reached weighted F1 0.69 and was weakest on the minimal tier; that is where cases should be hardest.
- **Generated benchmarks carry the generator's caveats** — the scenarios were written by gpt-oss-120b with only partial, qualitative human checks, and the authors say legal-expert validation is still needed; no licence is stated. Treat it as a comparison point, not ground truth, and check the licence before reusing the data.

---

## `industry/llm-fine-tuning.md`

### Edward J. Hu et al. — LoRA

**Source:** Hu, Shen, Wallis, Allen-Zhu, Li, Wang, Wang, Chen, *"LoRA: Low-Rank Adaptation of Large Language Models"*, ICLR 2022 (arXiv 2106.09685)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 5 | 3 | 5 | 4 | **Established** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — Microsoft Research team that defined the dominant parameter-efficient method. Publication — ICLR 2022. Adoption — implemented in Hugging Face PEFT, mlx-lm, llama.cpp and every major fine-tuning stack. Currency — still the default adapter method in 2026.

**Work score — *LoRA: Low-Rank Adaptation of Large Language Models*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 5 | 4 | 4 | 5 | **Canonical** |

Evidence: Specificity — exact parameterisation, initialisation, scaling, rank and target-module ablations, reference code. Depth — RoBERTa through GPT-3 175B with subspace analysis. Currency — base of QLoRA, DoRA, rsLoRA. Influence — cited in the tens of thousands. Average 4.5 classifies upward.

**Activation signals:** LoRA, adapters, rank, alpha, target modules, parameter-efficient fine-tuning, adapter merging

**Key principles:**

- **Freeze the base, train a low-rank update** — trainable rank-decomposition matrices sit alongside frozen weights; ranks of 4 to 16 were enough in the paper, so the adapter is megabytes against hundreds of megabytes for the base.
- **The knobs are rank, target matrices and the scaling factor** — record all three for every run; they are the first things a reader needs to reproduce it.
- **Adapters merge at no inference cost** — the update can be folded back into the base weights, which is what makes export to a single model file possible.

---

### Tim Dettmers et al. — QLoRA

**Source:** Dettmers, Pagnoni, Holtzman, Zettlemoyer, *"QLoRA: Efficient Finetuning of Quantized LLMs"*, NeurIPS 2023, oral (arXiv 2305.14314)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 5 | 3 | 5 | 4 | **Established** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — author of bitsandbytes and LLM.int8(); faculty at CMU and Ai2. Publication — NeurIPS oral, ICLR, ICML. Adoption — bitsandbytes is the default quantisation backend in Hugging Face Transformers. Currency — continued quantisation work through 2025. Boundary case: the independent pass averaged 4.6 (Canonical); recorded Established.

**Work score — *QLoRA: Efficient Finetuning of Quantized LLMs*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 5 | 4 | 4 | 5 | **Canonical** |

Evidence: Specificity — NF4, double quantisation, paged optimisers, full hyperparameters and memory tables. Depth — over a thousand fine-tuning runs. Currency — still the standard 4-bit LoRA recipe. Influence — several thousand citations. Average 4.5 classifies upward.

**Activation signals:** QLoRA, 4-bit base, NF4, quantised fine-tuning, memory budget, consumer hardware

**Key principles:**

- **A 4-bit base with LoRA matched 16-bit fine-tuning** — in the paper's benchmarks, at a fraction of the memory; this is the recipe for small-memory machines.
- **Compare at the same precision** — quantisation error is small but not zero; compare the fine-tuned 4-bit model with the untuned model at the same precision so the gain is attributed correctly.
- **Small curated data beat large data** — the best results came from a small, high-quality dataset, not the largest.

---

### Chunting Zhou et al. — LIMA

**Source:** Zhou, Liu, Xu, Iyer, Sun, Mao, Ma, Efrat, Yu, Yu, Zhang, Ghosh, Lewis, Zettlemoyer, Levy, *"LIMA: Less Is More for Alignment"*, NeurIPS 2023 (arXiv 2305.11206)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 5 | 2 | 4 | 3 | **Established** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — Meta AI team including Omer Levy and Luke Zettlemoyer. Publication — NeurIPS 2023. Adoption — the superficial alignment hypothesis drove the shift to small curated fine-tuning sets.

**Work score — *LIMA: Less Is More for Alignment*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 3 | 3 | 3 | 4 | **Recognised** |

Evidence: Influence — cited in the thousands; the standard reference for data quality over quantity. Boundary case: the primary pass placed the work at 3.5 (Established).

**Activation signals:** Data quality versus quantity, small curated fine-tuning sets, superficial alignment hypothesis, what fine-tuning teaches

**Key principles:**

- **Fine-tuning teaches format and behaviour; knowledge comes from pretraining** — 1,000 curated examples sufficed on a 65B base (the superficial alignment hypothesis).
- **The caveat travels with the claim** — a much smaller model holds less, so expect to need more examples and measure rather than assume.
- **Diversity beats volume** — prompt diversity in the curated set mattered more than its size.

---

### Yizhong Wang et al. — Self-Instruct

**Source:** Wang, Kordi, Mishra, Liu, Smith, Khashabi, Hajishirzi, *"Self-Instruct: Aligning Language Models with Self-Generated Instructions"*, ACL 2023 (arXiv 2212.10560)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 5 | 3 | 5 | 3 | **Established** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — University of Washington and Ai2 team; Wang led Super-NaturalInstructions and Tülu. Publication — ACL, EMNLP, NeurIPS. Adoption — Stanford Alpaca was built on it; 'self-instruct' is generic vocabulary.

**Work score — *Self-Instruct*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 4 | 3 | 5 | **Established** |

Evidence: Specificity — 175 seed tasks, generation prompts, ROUGE-L de-duplication threshold, released code and data. Depth — 52,000 instructions with human-rated evaluation. Influence — several thousand citations; basis of most synthetic-instruction pipelines.

**Activation signals:** Teacher-generated data, synthetic instruction data, generation and filtering pipeline, de-duplication

**Key principles:**

- **A model can write training data if the pipeline filters** — Self-Instruct drops near-duplicates (ROUGE-L overlap) and malformed outputs before training.
- **Keep the rejection statistics** — the share of generated cases a filter removes is itself a measurement; a rising share signals a drifting generation prompt.
- **Generated data inherits the generator's blind spots** — a hand-checked set, not the generator, is ground truth.

---

### Zhenyan Lu et al. — Small Language Models: Survey and Measurements

**Source:** Zhenyan Lu, Xiang Li, Dongqi Cai, Rongjie Yi, Fangming Liu, Xiwen Zhang, Nicholas D. Lane, Mengwei Xu, *"Small Language Models: Survey, Measurements, and Insights"*, arXiv 2409.15790 (v3 February 2025), preprint

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 4 | 3 | 3 | 4 | **Established** |

Evidence (scoring-reports/expert-scoring-002.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — senior authors Nicholas Lane (Cambridge professor) and Mengwei Xu (BUPT, on-device LLM systems). Owner decision on a 2-point divergence, 2026-10-26: Publication 4 (primary 2, independent 4): the dimension rates the team's usual venues (MobiCom, MobiSys), not this preprint. Currency 4 (split 5/4). Adoption 3 (split 3/4). Boundary case: the primary pass averaged 3.4 (Recognised).

**Work score — *Small Language Models: Survey, Measurements, and Insights*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 4 | 3 | 3 | **Established** |

Evidence: Specificity — measured runtime cost of 20 models on a Jetson Orin NX and three phones. Depth — surveys 70 open small models (the introduction says 57; the paper does not reconcile the two). Currency 3 (split 4/3).

**Activation signals:** Small language model bake-off, on-device latency and memory, sub-5B model capability, choosing a base model

**Key principles:**

- **Measure on the device you will use** — latency and memory on edge hardware depend on architecture and runtime, not only on parameter count.
- **Report capability, latency and memory together** — a bake-off that ranks on accuracy alone hides the cost that decides whether the model is usable.
- **Training data quality drives small-model capability** — differences between families of the same size trace mostly to their data, so read the technical report, not only the parameter count.

---

### Ricardo Dominguez-Olmedo et al. — Lawma

**Source:** Dominguez-Olmedo, Nanda, Abebe, Bechtold, Engel, Frankenreiter, Gummadi, Hardt, Livermore, *"Lawma: The Power of Specialization for Legal Annotation"*, ICLR 2025 (arXiv 2407.16615, v2 April 2025)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 5 | 3 | 2 | 4 | **Established** |

Evidence (scoring-reports/expert-scoring-002.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — Moritz Hardt (Director, Max Planck Institute for Intelligent Systems) with Gummadi (MPI-SWS) and legal scholars Engel, Bechtold, Livermore (split 4/5, lower recorded). Publication — ICLR 2025. Currency — v2 April 2025 (split 5/4).

**Work score — *Lawma: The Power of Specialization for Legal Annotation*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 5 | 4 | 4 | 3 | **Established** |

Evidence: Specificity — a concrete label budget (a few hundred to a thousand examples per task) to beat commercial models on 260 tasks; models from 135M (SmolLM2) through Llama 3.2 1B to 70B. Depth — 260 tasks with a sample-efficiency analysis. Currency — v2 re-ran comparisons against GPT-4.5 and Claude 3.7 Sonnet (split 5/4).

**Activation signals:** Legal annotation, specialisation versus scale, data budget per label, fine-tuned small models versus commercial models

**Key principles:**

- **Specialisation beats scale on narrow legal labelling** — on 260 legal annotation tasks, lightly fine-tuned open models from 135M to 70B parameters beat commercial models such as GPT-4.5 and Claude 3.7 Sonnet (v2, April 2025).
- **A few hundred to a thousand labelled examples per task are usually enough** — budget data per label, not as one total.
- **Commercial models are variable on concrete legal tasks** — non-trivial but uneven accuracy, generally short of what legal work needs; a prompted large model is a baseline, not a ceiling.

---

### Zorik Gekhman et al. — Fine-Tuning on New Knowledge

**Source:** Gekhman, Yona, Aharoni, Eyal, Feder, Reichart, Herzig, *"Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?"*, EMNLP 2024 long paper (arXiv 2405.05904)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 4 | 3 | 3 | 4 | **Established** |

Evidence (scoring-reports/expert-scoring-002.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — Google Research factuality researchers with Technion's Roi Reichart. Publication — EMNLP 2024 main conference (split 5/4). Currency — continued 2025–2026 work (split 4/5).

**Work score — *Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 4 | 3 | 4 | **Established** |

Evidence: Specificity — known/unknown example categories with actionable advice: stop early, filter unknown examples. Depth — controlled study varying the share of unknown examples; hallucination rises linearly once they are learned. Influence — EMNLP version alone cited at least 86 times (a lower bound). Currency 3 (split 4/3).

**Activation signals:** Fine-tuning on new facts, hallucination, what to keep out of training data, facts in a lookup table, early stopping

**Key principles:**

- **New knowledge is learned slowly through fine-tuning, and raises hallucination once learned** — examples that teach facts the base model does not know make it more likely to hallucinate on facts it did know.
- **Sort training examples by whether the base model already knows them** — the paper's categories separate known from unknown; keep unknown-fact examples out, or expect the cost.
- **Early stopping limits the damage** — the harm grows as the model fits the unknown examples; stop before it does.

---

### Dan Biderman et al. — LoRA Learns Less and Forgets Less

**Source:** Biderman, Portes, Gonzalez Ortiz, Paul, Greengard, Jennings, King, Havens, Chiley, Frankle, Blakeney, Cunningham (Columbia, Databricks Mosaic), *"LoRA Learns Less and Forgets Less"*, TMLR 2024 with Featured Certification; ICLR 2025 poster (arXiv 2405.09673)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 4 | 3 | 3 | 4 | **Established** |

Evidence (scoring-reports/expert-scoring-002.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — Jonathan Frankle (Databricks chief AI scientist; Lottery Ticket Hypothesis) and John Cunningham (Columbia) (split 4/5). Publication — TMLR Featured Certification and ICLR 2025 (split 4/5). Currency — ICLR 2025 presentation (split 5/4). Owner decision on a 2-point divergence, 2026-10-26: Adoption 3 (primary 3, independent 5): settled at the lower score; band unchanged. Boundary case: the independent pass averaged 4.6 (Canonical).

**Work score — *LoRA Learns Less and Forgets Less*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 4 | 3 | 4 | **Established** |

Evidence: Specificity — LoRA trails full fine-tuning on code and maths while full fine-tuning learns updates of 10 to 100 times higher rank; configuration guidance (split 5/4). Depth — continued pretraining and instruction tuning in two domains with forgetting measured (split 4/5). Influence — TMLR Featured Certification; later practitioner guidance responds to it (split 4/5).

**Activation signals:** LoRA versus full fine-tuning, LoRA hyperparameters, forgetting, rank choice, learning-rate sensitivity

**Key principles:**

- **LoRA learns less and forgets less** — it underperforms full fine-tuning on the target domain, especially in continued pretraining, but preserves more of the base model's other abilities.
- **Full fine-tuning learns high-rank changes** — 10 to 100 times the rank of typical LoRA settings; a narrow task needs less, a broad one more.
- **Practical settings** — target all modules, scaling factor about twice the rank, and treat the learning rate as the most sensitive knob.

---

### Yu-Ang Lee et al. — Learning Rate Matters

**Source:** Yu-Ang Lee (National Taiwan University), Ching-Yun Ko (IBM Research), Pin-Yu Chen (IBM Research), Mi-Yen Yeh (National Taiwan University, Academia Sinica), *"Learning Rate Matters: Vanilla LoRA May Suffice for LLM Fine-tuning"*, arXiv 2602.04998 (v2 May 2026). Venue: listed as a NeurIPS 2026 poster and at two ICML 2026 workshops; ICML 2026 main-conference acceptance not confirmed.

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 4 | 4 | 3 | 5 | **Established** |

Evidence (scoring-reports/expert-scoring-002.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — Pin-Yu Chen, IBM Research principal scientist, highly prolific. Publication — NeurIPS 2026 listing; the senior author publishes routinely at NeurIPS, ICML, ICLR. Breadth — robustness, safety, parameter-efficient fine-tuning, model reprogramming. Currency — 2026. Owner decision on a 2-point divergence, 2026-10-26: Authority 4, Breadth 4, Adoption 3 taken from the independent pass (primary 2, 2, 1): the primary pass had not identified the authors. Boundary case: the primary pass averaged 2.8 (Recognised).

**Work score — *Learning Rate Matters: Vanilla LoRA May Suffice for LLM Fine-tuning*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 3 | 5 | 2 | **Established** |

Evidence: Specificity — tune plain LoRA's learning rate first; once tuned, variants land within one to two points; tested on Qwen3-0.6B, close to this project's baseline (split 5/4). Currency — 2026. Depth 3 (split 3/4).

**Activation signals:** LoRA variants versus vanilla LoRA, learning-rate sweep, what to tune first

**Key principles:**

- **Tune the learning rate before changing the method** — once the learning rate is swept, the LoRA variants tested land within one to two points of plain LoRA; one of the four models was Qwen3-0.6B.
- **Comparisons at one learning rate mislead** — a variant that wins at a fixed rate may only have a better default for that rate.

---

### Hanning Zhang et al. — R-Tuning

**Source:** Zhang, Diao, Lin, Fung, Lian, Wang, Chen, Ji, Zhang (HKUST, UIUC), *"R-Tuning: Instructing Large Language Models to Say 'I Don't Know'"*, NAACL 2024, Outstanding Paper (arXiv 2311.09677)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 5 | 3 | 3 | 4 | **Established** |

Evidence (scoring-reports/expert-scoring-002.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — Tong Zhang and Heng Ji, senior UIUC professors (split 4/5). Publication — NAACL 2024 Outstanding Paper. Currency — continued 2025 work (split 4/5). Boundary case: the independent pass averaged 4.6 (Canonical).

**Work score — *R-Tuning: Instructing Large Language Models to Say 'I Don't Know'*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 3 | 3 | 4 | **Established** |

Evidence: Specificity — split training data by whether the model already answers correctly, and train it to state certainty or uncertainty. Influence — NAACL 2024 Outstanding Paper; a standard baseline for refusal-aware tuning (split 4/5). Depth 3 and Currency 3 (splits 3/4 and 4/3).

**Activation signals:** Training a model to abstain, 'I don't know' as a label, refusal-aware data, needs human review, calibration

**Key principles:**

- **Abstention is trained with refusal-aware data** — find where the model's knowledge and the training labels part ways, and teach an explicit 'unsure' answer there.
- **Refusal generalises** — the ability to decline transfers across tasks as a meta-skill, not only to the training questions.
- **Train it in; do not assume it survives** — fine-tuning on answer-only data erodes a model's willingness to decline.

---

### Sebastian Raschka — Practical LLM Fine-Tuning

**Source:** Sebastian Raschka, *Build a Large Language Model (From Scratch)*, Manning (2024); *"Practical Tips for Finetuning LLMs Using LoRA (Low-Rank Adaptation)"*, Ahead of AI newsletter (19 November 2023)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 3 | 4 | 4 | 5 | **Established** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — PhD, former UW-Madison assistant professor, former Lightning AI staff research engineer, LitGPT maintainer. Breadth — classical ML through LLM pretraining, fine-tuning and reasoning models. Adoption — companion repository with tens of thousands of stars. Currency — 2024 book, 2025 follow-up, newsletter active in 2026.

**Work score — *Build a Large Language Model (From Scratch)*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 5 | 4 | 4 | 3 | **Established** |

Evidence: Specificity — every component in runnable PyTorch. Depth — tokenisation through instruction fine-tuning, LoRA appendix. Currency — repository adds Llama 3 and Qwen3 conversions.

**Work score — *Practical Tips for Finetuning LLMs Using LoRA*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 5 | 3 | 3 | 3 | **Established** |

Evidence: Specificity — concrete settings from hundreds of runs (alpha about 2r, all linear layers, few epochs).

**Activation signals:** Practical LoRA settings, teaching how language models work, from-scratch explanations, fine-tuning defaults

**Key principles:**

- **Practical LoRA defaults** — scaling factor about twice the rank, adapters on all linear layers rather than attention only, few epochs on small datasets; change one setting at a time.
- **Score the task, not the loss** — validation loss is a training signal, not a result.
- **Teach from the mechanism** — explain tokens, attention and fine-tuning stages in runnable terms; understanding precedes tuning.

---

### Chip Huyen — AI Engineering

**Source:** Chip Huyen, *AI Engineering: Building Applications with Foundation Models*, O'Reilly (January 2025)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 4 | 4 | 4 | 5 | **Established** |

Evidence (scoring-reports/expert-scoring-001.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — formerly NVIDIA and Snorkel AI, co-founder of Claypot AI, taught Stanford CS 329S. Publication — O'Reilly. Breadth — ML systems, evaluation, retrieval, agents, fine-tuning, inference. Adoption — her two O'Reilly books are default practitioner references. Currency — 2025 book, active writing in 2026.

**Work score — *AI Engineering*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 4 | 5 | 4 | **Established** |

Evidence: Specificity — decision frameworks for fine-tune versus prompt versus retrieve, evaluation design, dataset engineering. Depth — roughly 530 pages. Currency — January 2025. Influence — a top-selling 2025 title in its category. Boundary case: the independent pass averaged 4.5 (Canonical); recorded Established.

**Activation signals:** Fine-tune versus prompt versus retrieve, evaluation-driven development, dataset engineering, AI engineering practice

**Key principles:**

- **Fine-tune for behaviour and format; retrieve for facts** — facts that change belong in a lookup the model reads, not in its weights.
- **Evaluation-driven development** — define how a result will be measured before building the thing measured; exact match, similarity and AI-as-judge each have known failure modes.
- **Synthetic data is engineered** — generation, verification and filtering are separate steps with their own checks.

---

## `domain/ai-assisted-development.md`

### METR — Randomised Trial of AI-Assisted Development

**Source:** Joel Becker, Nate Rush, Elizabeth Barnes, David Rein (METR), *"Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity"*, arXiv 2507.09089 (July 2025), preprint. METR posted a redesigned follow-up on 6 March 2026.

*Expert scored in `industry/ai-evaluation.md`. Classification: Recognised (avg 3.0).*

**Work score — *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 4 | 3 | 4 | **Established** |

Evidence: Specificity — each of 246 real tasks from 16 developers' own mature repositories randomised to AI-allowed or not, with a measured effect and the forecast-versus-actual gap. Depth — full randomised design and an analysis of factors behind the slowdown (split 4/5, lower recorded). Influence — the reference point in the AI-productivity debate (split 4/5, lower recorded). Owner decision on a 2-point divergence, 2026-10-26: Currency 3 (primary 5, independent 3): the title fixes the result to early-2025 tools, and METR's 2026 follow-up says the effect has probably moved.

**Activation signals:** AI-assisted development productivity, perceived versus measured speed-up, measuring the effect of AI tools

**Key principles:**

- **Felt speed is not measured speed** — experienced open-source developers forecast a 24% speed-up and believed afterwards they had gained about 20%, but were measured 19% slower on their own mature repositories.
- **Randomise and time the work** — tasks were randomly assigned to AI-allowed or AI-disallowed; self-report would have reversed the sign of the result.
- **Context bounds the claim** — the setting was large, mature codebases with high standards and developers with deep familiarity; the authors do not generalise beyond it, and neither should a reader.
- **Results age with the tools** — the trial measured early-2025 tools; METR's own 2026 follow-up says the effect has probably moved. Re-measure rather than quote.

---

### Addy Osmani — AI-Assisted Coding in Practice

**Source:** Addy Osmani, *"The 70% problem: Hard truths about AI-assisted coding"*, Elevate (Substack), 4 December 2024; *Beyond Vibe Coding: From Coder to AI-Era Developer*, O'Reilly (August 2025; print September 2025)

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|-----------|-------------|---------|----------|----------|----------------|
| 4 | 4 | 4 | 4 | 5 | **Established** |

Evidence (scoring-reports/expert-scoring-002.md in the AI Act Lab project, dual-pass verified, splits resolved down): Authority — Director at Google Cloud AI after about 14 years on Chrome developer experience. Publication — several O'Reilly books including *Learning JavaScript Design Patterns*. Breadth — web performance, JavaScript architecture, engineering leadership, AI-assisted coding. Adoption — *Learning JavaScript Design Patterns* is a standard reference (split 4/5, lower recorded). Currency — 2025 book, current AI role.

**Work score — *The 70% problem: Hard truths about AI-assisted coding*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 3 | 2 | 3 | 4 | **Recognised** |

Evidence: Influence — widely covered; '70% problem' became common shorthand. Owner decision on a 2-point divergence, 2026-10-26: Currency 3 (primary 5, independent 3): the argument holds but its late-2024 examples have aged. Boundary case: the primary pass averaged 3.75 (Established).

**Work score — *Beyond Vibe Coding: From Coder to AI-Era Developer*:**
| Specificity | Depth | Currency | Influence | Classification |
|-------------|-------|----------|-----------|----------------|
| 4 | 4 | 4 | 3 | **Established** |

Evidence: Specificity — book-length workflows for prompting, reviewing and testing AI-written code. Depth — about 254 pages. Currency — 2025 (split 5/4, lower recorded).

**Activation signals:** Vibe coding, AI-generated code quality, the last 30 percent, reviewing AI output, human as architect

**Key principles:**

- **The 70% problem** — AI tools get a project most of the way quickly; the last 30% (edge cases, integration, security, maintainability) needs engineering judgement, and non-experts are least able to see what is missing.
- **Two steps back** — fixing one bug with AI help introduces others when the person cannot read the code; understanding is the brake.
- **Accelerate what you understand** — use AI on work you can review; the human stays the architect and reads every change.

---

*Developed using the Grounded Vibe Methodology*
