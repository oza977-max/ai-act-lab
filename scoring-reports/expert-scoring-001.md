# AI Act Lab — Expert Scoring Report 001

**Date:** 2026-10-26
**Operation:** score on discovery, during `/gvm-init`
**Scope:** ten newly proposed experts, fifteen works, for two coverage gaps found during calibration: EU AI Act classification practice and gold-set annotation (Group A), and small-model adaptation with LoRA, data curation and abstention (Group B)
**Target reference files (on owner approval):** `industry/ai-governance.md` (1 expert), `industry/ai-evaluation.md` (3 experts), new `industry/llm-fine-tuning.md` (6 experts)
**Status:** scores reconciled across two independent passes; persistence to the shared library awaits the owner's approval of the init report

*What this report is, in plain English: before an authority is allowed to ground a decision in this project, it is scored on five questions about the author (standing, venue, range, uptake, how current) and four about the work (how concrete, how thorough, how current, how influential). Two assessments were made independently, one by the session running the phase and one by a fresh agent given only names and titles, and then reconciled: where they agreed the score stands; where they differed by one point the lower score is recorded; a difference of two or more would have been escalated to the owner. None was.*

## 1. Executive Summary

| | |
|---|---|
| Experts assessed | 10 |
| Works assessed | 15 |
| Full convergence on every dimension | 3 experts (European Commission; Chalkidis on both works; Pustejovsky & Stubbs on the expert score) |
| Largest single-dimension difference | 1 point (all cases) |
| Escalations (2+ point divergence) | 0 |
| Boundary cases recorded | 4 (Dettmers expert score; LIMA work; SelectiveNet work; *AI Engineering* work) |
| Existence verification | all 15 works verified by the independent pass, 11 by web search, 4 from established knowledge; one date clarified (*AI Engineering*, released January 2025) |

Scoring scale: integers 1 to 5. Classification by average: Canonical 4.5 and above, Established 3.5 to 4.4, Recognised 2.5 to 3.4, Emerging 1.5 to 2.4, Provisional below 1.5. An average of exactly 4.5 classifies upward.

## 2. Expert Scorecards

### 2.1 European Commission (AI Office)

**Sources:** European Commission, *Guidelines on the definition of an artificial intelligence system established by Regulation (EU) 2024/1689*, C(2025) 924 final, 6 February 2025; *Guidelines on prohibited artificial intelligence practices established by Regulation (EU) 2024/1689*, C(2025) 884 final, 4 February 2025. Also noted: *Guidelines on the classification of high-risk AI systems under Article 6*, published in draft for consultation on 19 May 2026; no final adoption found as of 26 October 2026.

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 5 | 5 | 4 | 5 | 5 | **Canonical** (avg 4.8) |

Evidence: Authority 5, the regulator itself; Article 96 of the Act mandates the Commission to issue these guidelines. Publication 5, numbered Commission acts in the C(2025) series, published through the Commission's digital-strategy library. Breadth 4, covers the definition, Article 5, general-purpose models (July 2025) and Article 6 in draft; not 5 while the Article 6 guidance is unfinished. Adoption 5, national market-surveillance authorities and compliance programmes across the EU work from them. Currency 5, Article 6 draft May 2026, general-purpose model guidelines July 2025.

Utilisation: no usage data, newly added.

**Work score — *Guidelines on the definition of an AI system*, C(2025) 924:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 4 | 3 | 4 | 4 | **Established** (avg 3.75) |

Evidence: Specificity 4, breaks Article 3(1) into seven elements with named out-of-scope examples (basic data processing, classical heuristics, simple prediction). Currency 4, February 2025, not affected by the Omnibus, described as designed to evolve (split 5/4, lower recorded). Influence 4, the first gate in AI Act scoping, cited by national-authority FAQs and law-firm briefings; non-binding (split 4/5, lower recorded).

**Work score — *Guidelines on prohibited AI practices*, C(2025) 884:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 5 | 5 | 4 | 4 | **Canonical** (avg 4.5, classifies upward) |

Evidence: Specificity 5, practice-by-practice tests with concrete in-scope and out-of-scope examples for each Article 5 prohibition. Depth 5, roughly 140 pages, including interplay with the GDPR, the DSA and consumer law. Currency 4, February 2025; Article 5 applied from 2 February 2025; the two prohibitions added by the Omnibus (applying from 2 December 2026) post-date it. Influence 4, the operative reference for Article 5 across the member states (split 4/5, lower recorded).

### 2.2 Ilias Chalkidis et al.

**Sources:** Chalkidis, Jana, Hartung, Bommarito, Androutsopoulos, Katz, Aletras, *"LexGLUE: A Benchmark Dataset for Legal Language Understanding in English"*, ACL 2022; Chalkidis, Fergadiotis, Androutsopoulos, *"MultiEURLEX: A multi-lingual and multi-label legal document classification dataset for zero-shot cross-lingual transfer"*, EMNLP 2021.

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 4 | 5 | 3 | 4 | 3 | **Established** (avg 3.8) |

Evidence: Authority 4, lead author of LEGAL-BERT, LexGLUE and MultiEURLEX; co-organiser of the Natural Legal Language Processing workshop series. Publication 5, ACL, EMNLP, NAACL and ICAIL main tracks. Adoption 4, LEGAL-BERT has citations in the thousands; LexGLUE and MultiEURLEX are standard Hugging Face-hosted legal datasets. Currency 3 (split 4/3, lower recorded).

Utilisation: no usage data, newly added.

**Work score — *LexGLUE*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 4 | 4 | 3 | 4 | **Established** (avg 3.75) |

Evidence: Specificity 4, seven defined tasks, released code, fixed splits, public leaderboard. Depth 4, benchmarks a dozen encoder models including legal-domain variants with per-task analysis. Influence 4, several hundred citations; the default legal-NLP benchmark before LegalBench. Both passes matched on every dimension.

**Work score — *MultiEURLEX*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 4 | 3 | 3 | 3 | **Recognised** (avg 3.25) |

Evidence: Specificity 4, 65,000 EU laws in 23 languages with hierarchical EUROVOC labels and a defined zero-shot transfer protocol. Both passes matched on every dimension.

### 2.3 James Pustejovsky and Amber Stubbs

**Source:** James Pustejovsky and Amber Stubbs, *Natural Language Annotation for Machine Learning*, O'Reilly (2012).

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 4 | 4 | 3 | 4 | 2 | **Recognised** (avg 3.4) |

Evidence: Authority 4, Pustejovsky is TJX Feldberg Professor at Brandeis, author of the Generative Lexicon and lead designer of TimeML. Publication 4, O'Reilly, with MIT Press and ACL/LREC venues for the underlying research. Adoption 4, the MATTER annotation cycle is standard teaching material for corpus annotation. Currency 2 reflects the 2012 date; the method is unchanged in practice. Both passes matched on every dimension.

Utilisation: no usage data, newly added.

**Work score — *Natural Language Annotation for Machine Learning*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 4 | 4 | 2 | 4 | **Established** (avg 3.5) |

Evidence: Specificity 4, step-by-step specification writing, guideline drafting, inter-annotator agreement computation, worked TimeML case study (split 5/4, lower recorded). Depth 4, a full-length book covering the whole model-annotate-train-test-evaluate-revise loop. Influence 4, citations in the thousands; the standard reference on corpus annotation method.

### 2.4 Edward J. Hu et al.

**Source:** Hu, Shen, Wallis, Allen-Zhu, Li, Wang, Wang, Chen, *"LoRA: Low-Rank Adaptation of Large Language Models"*, ICLR 2022.

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 4 | 5 | 3 | 5 | 4 | **Established** (avg 4.2) |

Evidence: Authority 4, Microsoft Research team that defined the dominant parameter-efficient method (split 4/5, lower recorded). Publication 5, ICLR 2022. Adoption 5, implemented in Hugging Face PEFT, `mlx-lm`, llama.cpp and every major fine-tuning stack. Currency 4, still the default adapter method in 2026.

Utilisation: no usage data, newly added.

**Work score — *LoRA*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 5 | 4 | 4 | 5 | **Canonical** (avg 4.5, classifies upward) |

Evidence: Specificity 5, exact parameterisation, initialisation, scaling, rank and target-module ablations, reference code. Depth 4, experiments across RoBERTa, DeBERTa, GPT-2 and GPT-3 175B with subspace analysis. Currency 4, the base for later variants (QLoRA, DoRA, rsLoRA); unchanged in practice. Influence 5, citations in the tens of thousands. Both passes matched on every dimension.

### 2.5 Tim Dettmers et al.

**Source:** Dettmers, Pagnoni, Holtzman, Zettlemoyer, *"QLoRA: Efficient Finetuning of Quantized LLMs"*, NeurIPS 2023 (oral).

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 4 | 5 | 3 | 5 | 4 | **Established** (avg 4.2) |

Evidence: Authority 4, author of bitsandbytes, LLM.int8() and 8-bit optimisers; now faculty at CMU and at Ai2 (split 4/5, lower recorded). Publication 5, NeurIPS oral, ICLR, ICML. Breadth 3 (split 3/4, lower recorded). Adoption 5, bitsandbytes is the default quantisation backend in Hugging Face Transformers. Currency 4, continued quantisation and inference work through 2025.

*Boundary case: the primary pass averaged 4.2 (Established), the independent pass 4.6 (Canonical). Recorded as Established per the lower-integer rule; flagged for the owner.*

Utilisation: no usage data, newly added.

**Work score — *QLoRA*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 5 | 4 | 4 | 5 | **Canonical** (avg 4.5, classifies upward) |

Evidence: Specificity 5, the NF4 data type, double quantisation, paged optimisers, full hyperparameters and memory tables. Depth 4, over a thousand fine-tuning runs across datasets and scales plus a human and GPT-4 evaluation of Guanaco (split 4/5, lower recorded). Currency 4, still the standard recipe for 4-bit LoRA on consumer hardware. Influence 5, several thousand citations; 4-bit LoRA is the default low-memory path.

### 2.6 Chunting Zhou et al.

**Source:** Zhou, Liu, Xu, Iyer, Sun, Mao, Ma, Efrat, Yu, Yu, Zhang, Ghosh, Lewis, Zettlemoyer, Levy, *"LIMA: Less Is More for Alignment"*, NeurIPS 2023.

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 4 | 5 | 2 | 4 | 3 | **Established** (avg 3.6) |

Evidence: Authority 4, Meta AI team including Omer Levy and Luke Zettlemoyer. Publication 5, NeurIPS 2023. Breadth 2, a single-result team for scoring purposes (split 2/3, lower recorded). Adoption 4, the "superficial alignment hypothesis" drove the shift to small curated fine-tuning sets in open-model practice.

Utilisation: no usage data, newly added.

**Work score — *LIMA*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 3 | 3 | 3 | 4 | **Recognised** (avg 3.25) |

Evidence: Specificity 3 (split 4/3, lower recorded). Influence 4, citations in the thousands; the standard reference for data quality over quantity.

*Boundary case: the primary pass averaged 3.5 (Established), the independent pass 3.25 (Recognised). Recorded as Recognised; flagged for the owner.*

### 2.7 Yizhong Wang et al.

**Source:** Wang, Kordi, Mishra, Liu, Smith, Khashabi, Hajishirzi, *"Self-Instruct: Aligning Language Models with Self-Generated Instructions"*, ACL 2023.

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 4 | 5 | 3 | 5 | 3 | **Established** (avg 4.0) |

Evidence: Authority 4, University of Washington and Ai2 team with Hajishirzi, Smith and Khashabi; Wang led Super-NaturalInstructions and the Tülu recipes. Publication 5, ACL, EMNLP, NeurIPS. Breadth 3 (split 3/4, lower recorded). Adoption 5, Stanford Alpaca was built directly on it; "self-instruct" is now generic vocabulary for synthetic instruction data. Currency 3 (split 3/4, lower recorded).

Utilisation: no usage data, newly added.

**Work score — *Self-Instruct*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 4 | 4 | 3 | 5 | **Established** (avg 4.0) |

Evidence: Specificity 4, full pipeline with 175 seed tasks, generation prompts, a ROUGE-L de-duplication threshold, released code and data (split 5/4, lower recorded). Depth 4, 52,000 instructions, evaluation on Super-NaturalInstructions and a 252-prompt user-oriented set with human ratings. Influence 5, several thousand citations; the basis of Alpaca and most later synthetic-instruction pipelines.

### 2.8 Yonatan Geifman and Ran El-Yaniv

**Sources:** Geifman and El-Yaniv, *"Selective Classification for Deep Neural Networks"*, NeurIPS 2017; Geifman and El-Yaniv, *"SelectiveNet: A Deep Neural Network with an Integrated Reject Option"*, ICML 2019. Lineage: C. K. Chow, *"On optimum recognition error and reject tradeoff"*, IEEE Transactions on Information Theory (1970), not scored.

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 4 | 5 | 3 | 3 | 3 | **Established** (avg 3.6) |

Evidence: Authority 4, El-Yaniv is a Technion professor who established selective prediction for deep networks; Geifman co-founded Deci AI. Publication 5, NeurIPS, ICML, ICLR. Adoption 3 (split 3/4, lower recorded).

Utilisation: no usage data, newly added.

**Work score — *Selective Classification for Deep Neural Networks*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 4 | 3 | 3 | 4 | **Established** (avg 3.5) |

Evidence: Specificity 4, an explicit algorithm to choose a confidence threshold that meets a target risk with a stated guarantee, using softmax response or MC-dropout (split 5/4, lower recorded). Depth 3 (split 4/3, lower recorded). Influence 4, citations in the thousands; defines the framework later abstention work uses.

**Work score — *SelectiveNet*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 4 | 3 | 3 | 3 | **Recognised** (avg 3.25) |

Evidence: Specificity 4, a concrete architecture with prediction, selection and auxiliary heads and a coverage-constrained loss. Influence 3 (split 3/4, lower recorded).

*Boundary case: the primary pass averaged 3.25 (Recognised), the independent pass 3.5 (Established). Recorded as Recognised; flagged for the owner.*

### 2.9 Sebastian Raschka

**Sources:** Sebastian Raschka, *Build a Large Language Model (From Scratch)*, Manning (2024); Sebastian Raschka, *"Practical Tips for Finetuning LLMs Using LoRA (Low-Rank Adaptation)"*, Ahead of AI newsletter, 19 November 2023.

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 4 | 3 | 4 | 4 | 5 | **Established** (avg 4.0) |

Evidence: Authority 4, PhD, former assistant professor at UW-Madison, former staff research engineer at Lightning AI, LitGPT maintainer. Publication 3 (split 4/3, lower recorded; the recent work is Manning and a newsletter rather than peer-reviewed venues). Breadth 4, classical machine learning through LLM pretraining, fine-tuning and reasoning-model work. Adoption 4, *Python Machine Learning* translated into a dozen languages; the companion repository has tens of thousands of stars (split 4/5, lower recorded). Currency 5, 2024 book, 2025 follow-up, newsletter active in 2026.

Utilisation: no usage data, newly added.

**Work score — *Build a Large Language Model (From Scratch)*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 5 | 4 | 4 | 3 | **Established** (avg 4.0) |

Evidence: Specificity 5, every component implemented line by line in runnable PyTorch with a public repository. Depth 4, tokenisation through pretraining, classification fine-tuning and instruction fine-tuning, LoRA appendix. Currency 4, GPT-2 base architecture, with Llama 3 and Qwen3 conversions added in the repository (split 5/4, lower recorded). Influence 3 (split 3/4, lower recorded).

**Work score — *Practical Tips for Finetuning LLMs Using LoRA*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 5 | 3 | 3 | 3 | **Established** (avg 3.5) |

Evidence: Specificity 5, concrete settings (scaling factor twice the rank, adapters on all linear layers, single epoch, the QLoRA memory-versus-time trade-off) drawn from hundreds of runs. Both passes matched on every dimension.

### 2.10 Chip Huyen

**Source:** Chip Huyen, *AI Engineering: Building Applications with Foundation Models*, O'Reilly (January 2025).

**Expert score:**
| Authority | Publication | Breadth | Adoption | Currency | Classification |
|---|---|---|---|---|---|
| 4 | 4 | 4 | 4 | 5 | **Established** (avg 4.2) |

Evidence: Authority 4, formerly at NVIDIA and Snorkel AI, co-founder of Claypot AI, taught Stanford CS 329S on machine-learning systems design. Publication 4, O'Reilly; *Designing Machine Learning Systems* was a category bestseller. Breadth 4, machine-learning systems, LLM evaluation, retrieval, agents, fine-tuning, inference. Adoption 4, her two O'Reilly books are default practitioner references (split 4/5, lower recorded). Currency 5, January 2025 book, active writing in 2025 and 2026.

Utilisation: no usage data, newly added.

**Work score — *AI Engineering*:**
| Specificity | Depth | Currency | Influence | Classification |
|---|---|---|---|---|
| 4 | 4 | 5 | 4 | **Established** (avg 4.25) |

Evidence: Specificity 4, decision frameworks for fine-tune versus prompt versus retrieve, evaluation design, dataset engineering; survey-style rather than code-led. Depth 4, roughly 530 pages spanning evaluation through inference optimisation (split 4/5, lower recorded). Currency 5, January 2025. Influence 4, O'Reilly's top-selling 2025 title in its category.

*Boundary case: the primary pass averaged 4.25 (Established), the independent pass 4.5 (Canonical). Recorded as Established; flagged for the owner.*

## 3. Independent Verification

Primary pass (P) by the session running `/gvm-init`, recorded before the independent pass was read. Independent pass (I) by a fresh agent given names and titles only. Expert dimensions in the order Authority, Publication, Breadth, Adoption, Currency; work dimensions in the order Specificity, Depth, Currency, Influence.

| Expert / work | P | I | Final | Differences |
|---|---|---|---|---|
| European Commission | 5 5 4 5 5 | 5 5 4 5 5 | 5 5 4 5 5 | none |
| — Definition guidelines | 4 3 5 4 | 4 3 4 5 | 4 3 4 4 | Currency, Influence (1 each) |
| — Prohibited practices guidelines | 5 5 4 4 | 5 5 4 5 | 5 5 4 4 | Influence (1) |
| Chalkidis et al. | 4 5 3 4 4 | 4 5 3 4 3 | 4 5 3 4 3 | Currency (1) |
| — LexGLUE | 4 4 3 4 | 4 4 3 4 | 4 4 3 4 | none |
| — MultiEURLEX | 4 3 3 3 | 4 3 3 3 | 4 3 3 3 | none |
| Pustejovsky & Stubbs | 4 4 3 4 2 | 4 4 3 4 2 | 4 4 3 4 2 | none |
| — *Natural Language Annotation* | 5 4 2 4 | 4 4 2 4 | 4 4 2 4 | Specificity (1) |
| Hu et al. | 4 5 3 5 4 | 5 5 3 5 4 | 4 5 3 5 4 | Authority (1) |
| — LoRA | 5 4 4 5 | 5 4 4 5 | 5 4 4 5 | none |
| Dettmers et al. | 4 5 3 5 4 | 5 5 4 5 4 | 4 5 3 5 4 | Authority, Breadth (1 each); boundary |
| — QLoRA | 5 4 4 5 | 5 5 4 5 | 5 4 4 5 | Depth (1) |
| Zhou et al. | 4 5 2 4 3 | 4 5 3 4 3 | 4 5 2 4 3 | Breadth (1) |
| — LIMA | 4 3 3 4 | 3 3 3 4 | 3 3 3 4 | Specificity (1); boundary |
| Wang et al. | 4 5 3 5 3 | 4 5 4 5 4 | 4 5 3 5 3 | Breadth, Currency (1 each) |
| — Self-Instruct | 5 4 3 5 | 4 4 3 5 | 4 4 3 5 | Specificity (1) |
| Geifman & El-Yaniv | 4 5 3 3 3 | 4 5 3 4 3 | 4 5 3 3 3 | Adoption (1) |
| — Selective Classification | 5 4 3 4 | 4 3 3 4 | 4 3 3 4 | Specificity, Depth (1 each) |
| — SelectiveNet | 4 3 3 3 | 4 3 3 4 | 4 3 3 3 | Influence (1); boundary |
| Raschka | 4 4 4 4 5 | 4 3 4 5 5 | 4 3 4 4 5 | Publication, Adoption (1 each) |
| — *Build a Large Language Model* | 5 4 5 3 | 5 4 4 4 | 5 4 4 3 | Currency, Influence (1 each) |
| — LoRA practical tips | 5 3 3 3 | 5 3 3 3 | 5 3 3 3 | none |
| Huyen | 4 4 4 4 5 | 4 4 4 5 5 | 4 4 4 4 5 | Adoption (1) |
| — *AI Engineering* | 4 4 5 4 | 4 5 5 4 | 4 4 5 4 | Depth (1); boundary |

**Overall confidence: High.** Every dimension converged within one point. Convergence shows the scores are stable between two passes of the same model family; it does not prove them correct. The owner's approval remains the correctness check.

**Existence checks by the independent pass.** Both Commission guidelines confirmed on the Commission's digital-strategy library with their C-numbers and February 2025 approval dates. The Article 6 high-risk classification guidelines exist only as a draft published for consultation on 19 May 2026; no final text was found as of 26 October 2026. Raschka's newsletter article confirmed with its date and subtitle. Huyen's book confirmed as released January 2025. The remaining papers confirmed against their stated venues and years.

## 4. Utilisation Analysis

No activation data exists for any of the ten experts; all are newly added. The activation log holds rows for the existing experts loaded during this calibration (Tier 1 and the two industry files), but those experts were not scored in this operation and their utilisation is outside its scope.

## 5. Summary Table

Sorted by expert classification, then average.

| Expert | Classification (avg) | Works | Highest-classified work | Verification | Cite rate | Sample | Flag |
|---|---|---|---|---|---|---|---|
| European Commission (AI Office) | Canonical (4.8) | 2 | Prohibited practices guidelines, Canonical | High | n/a | newly added | none |
| Edward J. Hu et al. | Established (4.2) | 1 | *LoRA*, Canonical | High | n/a | newly added | none |
| Tim Dettmers et al. | Established (4.2) | 1 | *QLoRA*, Canonical | High | n/a | newly added | boundary (expert) |
| Chip Huyen | Established (4.2) | 1 | *AI Engineering*, Established | High | n/a | newly added | boundary (work) |
| Yizhong Wang et al. | Established (4.0) | 1 | *Self-Instruct*, Established | High | n/a | newly added | none |
| Sebastian Raschka | Established (4.0) | 2 | *Build a Large Language Model*, Established | High | n/a | newly added | none |
| Ilias Chalkidis et al. | Established (3.8) | 2 | *LexGLUE*, Established | High | n/a | newly added | none |
| Chunting Zhou et al. | Established (3.6) | 1 | *LIMA*, Recognised | High | n/a | newly added | boundary (work) |
| Geifman & El-Yaniv | Established (3.6) | 2 | *Selective Classification*, Established | High | n/a | newly added | boundary (work) |
| Pustejovsky & Stubbs | Recognised (3.4) | 1 | *Natural Language Annotation*, Established | High | n/a | newly added | none |

## 6. Recall Check

The scoring method requires a check in the other direction: not only whether the proposed names deserve their scores, but whether any widely cited authority was missed. A separate blind agent enumerated each field's most-cited authorities without seeing the roster; the comparison is recorded in `init/init-001.md`, section 3.3.

## 7. Changes

Not applicable: this is a first scoring, not a rescore.

---

*Developed using the Grounded Vibe Methodology*
