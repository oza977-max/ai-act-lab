# Reading list: fine-tuning small language models

**Compiled:** 2026-10-26, from four themed arXiv sweeps run in parallel, each verified against arxiv.org.
**Purpose:** the papers worth knowing for this project, ranked for its constraints, so the owner can pick which ones join the expert roster and which to read first.
**Status:** candidate list. Nothing here is on the roster until it has been scored and the owner has approved it.

## How to read this list

**What "good" meant.** A paper is on the list if it meets two tests. It is either peer-reviewed at a strong venue (NeurIPS, ICML, ICLR, ACL, EMNLP, TMLR and the like) or so widely cited and adopted that practitioners treat it as standard. And it is relevant to what this project actually is: a 0.8-billion-parameter model, 4-bit, adapted with LoRA on a laptop with 8 GB of memory, to classify descriptions of AI systems with a citation, a reason and an honest "needs human review". A famous paper about 70-billion-parameter models with no bearing on that is not here.

**How "relevance" was judged.** High means it changes a decision in this project (a training setting, a data rule, a measurement). Medium means it informs the decision or sets expectations. Low means useful background.

**What to trust.** Every entry was checked on arxiv.org for title, first author, year and identifier. Anything that could not be confirmed is marked "(unverified)" and should not be cited until it is. Each sweep also records what it looked at and left out, so the list shows its breadth, not only its picks.

**What this list is not.** It is not a survey of the field and not a ranking of importance in general. It is the shelf for one small, specific project. It will grow: when a later phase needs a paper that is not here, it is added with a dated line.

**Where it goes next.** The owner picks the entries to put on the expert roster. Each picked entry is then scored the same way as the ten proposed in `init/init-001.md`: two independent passes, reconciled, with evidence. The rest stay here as reading.

## Start here

Ten papers, in reading order. Each line says what you get from it. Together they take a weekend; the first five take an evening.

1. **Lu et al., Small Language Models: Survey, Measurements, and Insights** (2409.15790). The map: what sub-5B open models can do, and what they cost in memory and time on a device.
2. **Hu et al., LoRA** (2106.09685). What we are actually doing to the model, in the authors' words. Read for rank, scaling factor and the merge step.
3. **Dettmers et al., QLoRA** (2305.14314). Why a 4-bit base with adapters fits in 8 GB and loses little.
4. **Biderman et al., LoRA Learns Less and Forgets Less** (2405.09673). The honest limits of LoRA and the settings that work.
5. **Lee et al., Learning Rate Matters** (2602.04998). Tune the learning rate; do not chase LoRA variants.
6. **Zhou et al., LIMA** (2305.11206). Quality beats volume. The case for a small, careful dataset.
7. **Dominguez-Olmedo et al., Lawma** (2407.16615). Open models from 135 million parameters up, lightly fine-tuned, beat commercial models on 260 legal annotation tasks with a few hundred to a thousand examples per task. The closest evidence to this project.
8. **Gekhman et al., Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?** (2405.05904). Why dates and duties stay in a table: teaching a model facts it lacks makes it hallucinate more.
9. **Zhang et al., R-Tuning** (2311.09677). How to train a model to say "I don't know", which is what "needs human review" is.
10. **Davvetas et al., AI Act Evaluation Benchmark** (2603.09435). The nearest external yardstick: 339 scenarios labelled by AI Act tier. The baseline's weak spot was the minimal tier.

Next two when ready: **Miller, Adding Error Bars to Evals** (2411.00640), so no number is reported without an interval; and **Hsieh et al., Distilling Step-by-Step** (2305.02301), for training a small model to give a reason with its label.


## A. The fine-tuning technique: LoRA, its variants and its limits

What this theme settles: which knobs matter (rank, scaling factor, learning rate, which layers), whether a variant of LoRA is worth trying, and what LoRA cannot do that full fine-tuning can. The clearest message from the sweep is that the learning rate matters more than the choice of variant.

| Rank | Title | Authors and year | arXiv id and venue | Why it matters for this project | Relevance |
|---|---|---|---|---|---|
| 1 | LoRA: Low-Rank Adaptation of Large Language Models | Hu et al., 2021 | 2106.09685; ICLR 2022 | The method `mlx-lm` implements; defines rank, scaling factor, target modules and the merge step | H |
| 2 | QLoRA: Efficient Finetuning of Quantized LLMs | Dettmers et al., 2023 | 2305.14314; NeurIPS 2023 | Establishes that LoRA on a frozen 4-bit base recovers near-16-bit quality, which is the 8 GB recipe | H |
| 3 | LoRA Learns Less and Forgets Less | Biderman et al., 2024 | 2405.09673; TMLR 2024 | Best empirical guide to rank, scaling factor of twice the rank, targeting all modules, and why LoRA preserves base-model behaviour | H |
| 4 | Learning Rate Matters: Vanilla LoRA May Suffice for LLM Fine-tuning | Lee et al., 2026 | 2602.04998; listed as a NeurIPS 2026 poster and at two ICML 2026 workshops | Once the learning rate is swept, the LoRA variants tested land within one to two points of plain LoRA, including on Qwen3-0.6B; tune the learning rate, do not chase variants | H |
| 5 | LoRA vs Full Fine-tuning: An Illusion of Equivalence | Shuttleworth et al., 2024 | 2410.21228; NeurIPS 2025 (venue from one listing; arXiv page shows none) | Explains "intruder dimensions" and why a higher rank with rank-stabilised scaling generalises better off-distribution | M |
| 6 | A Rank Stabilization Scaling Factor for Fine-Tuning with LoRA (rsLoRA) | Kalajdzievski, 2023 | 2312.03732; preprint, adopted in Hugging Face PEFT | Replaces alpha/r with alpha/sqrt(r) so raising the rank actually helps; cheap to replicate by setting the scaling factor | M |
| 7 | LoRA+: Efficient Low Rank Adaptation of Large Models | Hayou et al., 2024 | 2402.12354; ICML 2024 | Argues the B matrix should get a much larger learning rate than A; informs the learning-rate choice even with one rate | M |
| 8 | The Impact of Initialization on LoRA Finetuning Dynamics | Hayou et al., 2024 | 2406.08447; NeurIPS 2024 | The default B = 0 initialisation tolerates larger learning rates, so keep the default and sweep the rate | M |
| 9 | DoRA: Weight-Decomposed Low-Rank Adaptation | Liu et al., 2024 | 2402.09353; ICML 2024 (oral) | The one variant `mlx-lm` ships natively; worth one controlled comparison run | M |
| 10 | LoftQ: LoRA-Fine-Tuning-Aware Quantization for Large Language Models | Li et al., 2023 | 2310.08659; ICLR 2024 | Initialises adapters to cancel 4-bit quantisation error; the main lever if the 4-bit base underperforms | M |
| 11 | PiSSA: Principal Singular Values and Singular Vectors Adaptation | Meng et al., 2024 | 2404.02948; NeurIPS 2024 (spotlight) | An initialisation that converges faster and reduces quantisation error; relevant when few training steps are affordable | M |
| 12 | GaLore: Memory-Efficient LLM Training by Gradient Low-Rank Projection | Zhao et al., 2024 | 2403.03507; ICML 2024 (oral) | The reference for full-parameter training inside 8 GB if LoRA plateaus on the 0.8B model; no MLX port, so a stretch | M |
| 13 | The Expressive Power of Low-Rank Adaptation | Zeng and Lee, 2023 | 2310.17513; ICLR 2024 | Theoretical rank bounds; justifies why a small rank can represent a narrow classification task | M |
| 14 | QA-LoRA: Quantization-Aware Low-Rank Adaptation of Large Language Models | Xu et al., 2023 | 2309.14717; ICLR 2024 | How to merge adapters back into a quantised model without quality loss; relevant when shipping a 4-bit classifier | L |
| 15 | Low-Rank Adaptation for Foundation Models: A Comprehensive Review | Yang et al., 2025 | 2501.00365; preprint | A map of the variant landscape; for orientation, not decisions | M |

**Checked and excluded.** AdaLoRA (Zhang et al., 2023, 2303.10512): adaptive rank, not in `mlx-lm`. VeRA (Kopiczko et al., 2023, 2310.11454): parameter count is not the bottleneck here. LISA (2403.17919), BAdam (2404.02827), LOMO (2306.09782): full-parameter methods with no MLX implementation. "LoRA Without Regret" (Schulman et al., Thinking Machines, September 2025): a blog post, not arXiv, but still the clearest practitioner guide (LoRA learning rate about ten times the full fine-tuning rate; apply to all layers); it stays on the init report's recall list. "Post-Training Science for Supervised Fine-Tuning" (O'Neill et al., 2026, 2609.01244): one month old, unreviewed. Apple's MLX has no arXiv paper; cite the software itself (Hannun, Digani, Katharopoulos, Collobert, 2023). No arXiv paper on `mlx-lm` fine-tuning exists as of today.

**Verification note.** All fifteen entries were confirmed on arxiv.org for title, first author, year and identifier. Venues not shown on an arXiv page come from conference listings and standard citation records; the NeurIPS 2025 venue for entry 5 rests on a single listing.

## B. Small models and distillation: what a sub-2B model can be taught

What this theme settles: what the candidate base models are, as their makers describe them; what small models have been shown to do after specialisation, and at what cost; and how a strong teacher's judgement and reasons get into a small student. Two findings matter most for the bake-off: 4-bit quantisation tends to preserve a small model's reasoning, and small models often fail strict output formats, so format compliance has to be measured, not assumed.

| Rank | Title | Authors and year | arXiv id and venue | Why it matters for this project | Relevance |
|---|---|---|---|---|---|
| 1 | Small Language Models: Survey, Measurements, and Insights | Lu et al., 2024 | 2409.15790; preprint | Benchmarks 100M to 5B open models on capability, on-device latency and memory, which is the frame for an 8 GB bake-off | H |
| 2 | Qwen3 Technical Report | Yang et al., 2025 | 2505.09388; preprint; Apache 2.0 stated | Documents the 0.6B and 1.7B dense models and the post-training recipe behind the Qwen candidate; Qwen3.5 has no arXiv report yet | H |
| 3 | Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes | Hsieh et al., 2023 | 2305.02301; Findings of ACL 2023 | Trains sub-1B students on teacher labels plus rationales, the same "tier plus one-sentence reason" shape as this project's cases | H |
| 4 | Gemma 3 Technical Report | Gemma Team, 2025 | 2503.19786; preprint; weights under the Gemma Terms of Use | Primary source for the 1B candidate, including its distillation from larger models and quantisation-aware checkpoints | H |
| 5 | LFM2 Technical Report | Amini et al. (Liquid AI), 2025 | 2511.23404; preprint; LFM Open License v1.0 | Primary source for the 1.2B candidate, with explicit CPU and edge memory and latency measurements for 350M to 2.6B models | H |
| 6 | SmolLM2: When Smol Goes Big. Data-Centric Training of a Small Language Model | Ben Allal et al., 2025 | 2502.02737; preprint; Apache 2.0 | The most detailed public account of curating instruction data for a 1.7B model; useful when judging the 2,000 teacher-written cases | H |
| 7 | Towards Reasoning Ability of Small Language Models | Srivastava et al., 2025 | 2502.11569; EMNLP 2025 | Evaluates 72 small models: 4-bit quantisation preserves reasoning, but small models often fail strict output formats; two risks to measure | H |
| 8 | Punching Above Their Weight: Classification-Head Fine-Tuning of Tiny Language Models for Verifiable Multiple-Choice Tasks | Sood et al., 2026 | 2607.03801; preprint | Fine-tunes Qwen3 0.6B and 1.7B on classification-style tasks; a classification head beat label generation by two to three points, a cheap ablation for the bake-off | H |
| 9 | Specializing Smaller Language Models towards Multi-Step Reasoning | Fu et al., 2023 | 2301.12726; ICML 2023 | Concentrating a small model's capacity on one task works but costs general ability, which is the bet this project is making | M |
| 10 | MobileLLM: Optimizing Sub-billion Parameter Language Models for On-Device Use Cases | Liu et al., 2024 | 2402.14905; ICML 2024 | Why deep-and-thin sub-1B architectures beat wider ones; helps read the 0.8B candidates' design choices | M |
| 11 | Orca 2: Teaching Small Language Models How to Reason | Mitra et al., 2023 | 2311.11045; preprint | Teaches small models to pick a reasoning strategy per input, including answering cautiously; a template for an honest "needs human review" class | M |
| 12 | On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes | Agarwal et al., 2023 | 2306.13649; ICLR 2024 | The reference for on-policy distillation; relevant only if a later phase moves from offline teacher cases to a live teacher | M |
| 13 | Textbooks Are All You Need | Gunasekar et al., 2023 | 2306.11644; preprint | Origin of the Phi line: a 1.3B model trained on small, high-quality synthetic data; the argument for quality over volume | M |
| 14 | Small Language Models are the Future of Agentic AI | Belcak et al. (NVIDIA), 2025 | 2506.02153; preprint, position paper | Argues specialised small models with LoRA adapters should replace general models for narrow tasks, and sketches a conversion pipeline | M |
| 15 | Sub-Billion, Super-Frontier: Small Language Models Rival Zero-Shot Frontier LLMs on General and Literary Relation Extraction | Christou et al., 2026 | 2606.22606; preprint | A fine-tuned Qwen2.5-0.5B beat zero-shot frontier models on structured extraction while still failing complex reasoning; a realistic ceiling | M |

**Checked and excluded.** The Llama 3 Herd of Models (2407.21783): does not cover the Llama 3.2 1B model. Phi-3 (2404.14219) and Phi-4-mini (2503.01743): 3.8B, above the size limit. MiniLLM (2306.08543, ICLR 2024): needs teacher logits; on-policy distillation suffices as the reference. A Survey of Small Language Models (2410.20011): overlaps entry 1 without the measurements. "Fine-Tuned 'Small' LLMs (Still) Outperform Zero-Shot" (2406.08660): encoder models, not decoders. Granite 4.0 and Qwen3.5 technical reports: no arXiv paper found as of today.

**Verification note.** All titles, first authors, years and identifiers were checked on arxiv.org abstract pages. Licences come from the Hugging Face model cards, not the papers, except where the abstract states one.

## C. Training data: curation, teacher-written cases and their failure modes

What this theme settles: how many cases are enough, what makes a case good, how a judge filter should work and how it can fail, and what fine-tuning does to a base model that nobody asked for. The two findings that change this project most are that lightly fine-tuned small open models, down to 135 million parameters, beat commercial models on legal classification with a few hundred to a thousand examples per task (entry 3), and that a judge from the same model family as the teacher waves the teacher's flaws through (entry 10).

| Rank | Title | Authors and year | arXiv id and venue | Why it matters for this project | Relevance |
|---|---|---|---|---|---|
| 1 | LIMA: Less Is More for Alignment | Zhou et al., 2023 | 2305.11206; NeurIPS 2023 | 1,000 carefully curated examples taught format and judgement; effort belongs in case quality, not volume | H |
| 2 | Self-Instruct: Aligning Language Models with Self-Generated Instructions | Wang et al., 2022 | 2212.10560; ACL 2023 | The template for teacher-written cases with automatic filtering; its finding that about half of raw generations have flaws is why the judge filter exists | H |
| 3 | Lawma: The Power of Specialization for Legal Annotation | Dominguez-Olmedo et al., 2024 | 2407.16615; ICLR 2025 | On 260 legal annotation tasks, fine-tuned open models from 135M to 70B parameters (including Llama 3.2 1B) beat commercial models such as GPT-4.5 and Claude 3.7 Sonnet; a few hundred to a thousand labelled examples per task were usually enough. The closest evidence for this project's data budget (figures from v2, April 2025) | H |
| 4 | AlpaGasus: Training A Better Alpaca with Fewer Data | Chen et al., 2023 | 2307.08701; ICLR 2024 | A judge scored teacher-written data and keeping 9,000 of 52,000 beat training on all of it; the project's judge filter, measured | H |
| 5 | Synthetic Data Generation with Large Language Models for Text Classification: Potential and Limitations | Li et al., 2023 | 2310.07849; EMNLP 2023 | Synthetic training data works for objective classification and degrades as the task gets subjective; borderline tier cases are where "needs human review" must fire | H |
| 6 | The False Promise of Imitating Proprietary LLMs | Gudibande et al., 2023 | 2305.15717; ICLR 2024 (spotlight) | Imitation data teaches a small student the teacher's style but not its knowledge, and the student fabricates confidently; supports the lookup table and targeted gold cases | H |
| 7 | Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations? | Gekhman et al., 2024 | 2405.05904; EMNLP 2024 | Listed in section D; the data-side reading is that cases must not try to teach facts the base model lacks | H |
| 8 | Best Practices and Lessons Learned on Synthetic Data | Liu et al., 2024 | 2404.07503; COLM 2024 | A checklist of synthetic-data failure modes (factuality, diversity loss, bias amplification, contamination of the test set) to audit the teacher pipeline against | M |
| 9 | What Makes Good Data for Alignment? A Comprehensive Study of Automatic Data Selection in Instruction Tuning (DEITA) | Liu et al., 2023 | 2312.15685; ICLR 2024 | Scores cases on complexity, quality and diversity; 6,000 selected examples matched far larger sets; concrete signals for the judge stage | M |
| 10 | LLM Evaluators Recognize and Favor Their Own Generations | Panickssery et al., 2024 | 2404.13076; NeurIPS 2024 (oral) | A judge favours text in its own style, so a judge from the teacher's family will pass flawed cases; argues for a different-family judge and for the gold cases as the real check | M |
| 11 | Scaling Instruction-Finetuned Language Models | Chung et al., 2022 | 2210.11416; JMLR 2024 | Instruction tuning helps at every model size, and small models stood in for much larger ones on narrow tasks; the foundation for expecting a 0.8B model to learn this job | M |
| 12 | How Abilities in Large Language Models are Affected by Supervised Fine-tuning Data Composition | Dong et al., 2023 | 2310.05492; ACL 2024 | How mixing general and task data changes small models' abilities; informs whether to add some general data so the model keeps its language skills | M |
| 13 | Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To! | Qi et al., 2023 | 2310.03693; ICLR 2024 (oral) | Even benign fine-tuning data erodes the base model's refusal behaviour, so "needs human review" must be trained in explicitly, not assumed to survive | M |
| 14 | AI models collapse when trained on recursively generated data | Shumailov et al., 2024 | 2305.17493 (preprint titled "The Curse of Recursion"); Nature 631, 2024 | Model-generated data loses the tails; one teacher generation is low risk, but a judge filter that strips rare edge cases is not | M |
| 15 | A Survey on Data Selection for Language Models | Albalak et al., 2024 | 2402.16827; TMLR 2024 | The map of filtering, de-duplication and quality-scoring methods; useful when deciding what the judge filter should measure | M |

**Checked and excluded.** "Finetuned Language Models Are Zero-Shot Learners" (2109.01652, ICLR 2022): superseded by entry 11. Alpaca (Taori et al., 2023): no arXiv paper. WizardLM (2304.12244, ICLR 2024): complexity evolution, not classification. Instruction backtranslation (2308.06259, ICLR 2024): needs an unlabelled web corpus. "An Empirical Study of Catastrophic Forgetting in LLMs During Continual Fine-tuning" (2308.08747): no venue. "Fine-Tuning on Noisy Instructions" (2510.03528, AACL 2025): input noise, not label noise.

**A gap the sweep could not fill.** No strong-venue 2024 to 2026 paper isolates label-noise effects in language-model fine-tuning or compares judge-filtered against unfiltered synthetic data head to head. Lawma is the best evidence on example counts; AlpaGasus and Panickssery are the best on judge filtering. This project's own measurements will have to stand in.

**Verification note.** All titles, first authors, years and identifiers were checked on arxiv.org abstract pages; venues on the arXiv comments field or the venue's own proceedings page. The Nature title was confirmed through institutional listings, as the Nature page is paywalled.

## D. Classification, abstention, honest evaluation, and the legal domain

What this theme settles: that a small decoder model with LoRA is a credible classifier; how to train and score a "needs human review" answer; what a small test set can and cannot prove; and what already exists for the EU AI Act specifically. The single most useful find of the whole sweep is entry 10: a 2026 benchmark of 339 generated scenarios labelled by AI Act risk tier, with article retrieval, on which a retrieval baseline reached a weighted F1 of 0.69 and was weakest on the minimal tier. It is the closest thing to an external yardstick this project has, and it says the task is hard.

| Rank | Sub-theme | Title | Authors and year | arXiv id and venue | Why it matters for this project | Relevance |
|---|---|---|---|---|---|---|
| 1 | Abstention | R-Tuning: Instructing Large Language Models to Say "I Don't Know" | Zhang et al., 2023 | 2311.09677; NAACL 2024 | Fine-tunes the model to answer "I don't know" on cases outside its competence: the recipe for a trained "needs human review" label | H |
| 2 | Classification | Label Supervised LLaMA Finetuning | Li et al., 2023 | 2310.01208; preprint, widely cited | A decoder model with LoRA, trained with label supervision, beats encoder baselines on classification; this project's setup | H |
| 3 | Abstention | Know Your Limits: A Survey of Abstention in Large Language Models | Wen et al., 2024 | 2407.18418; TACL | Organises abstention methods and metrics; the vocabulary for designing and scoring the review option | H |
| 4 | Abstention | Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations? | Gekhman et al., 2024 | 2405.05904; EMNLP 2024 | Fine-tuning on facts the base model lacks raises hallucination; the published support for keeping dates and duties in a table, not the weights | H |
| 5 | Evaluation | Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations | Miller, 2024 | 2411.00640; preprint, widely adopted | Confidence-interval and paired-comparison formulas for small test sets, so the notebook reports intervals, not bare scores | H |
| 6 | Evaluation | With Little Power Comes Great Responsibility | Card et al., 2020 | 2010.06595; EMNLP 2020 | Typical test sets are underpowered to detect small gains; sets honest expectations for a small, once-touched test set | H |
| 7 | Classification | Fine-Tuned "Small" LLMs (Still) Significantly Outperform Zero-Shot Generative AI Models in Text Classification | Bucher and Martini, 2024 | 2406.08660; preprint, widely cited | Fine-tuned small models beat zero-shot large models on text classification across datasets; the models are encoders, so the evidence transfers in spirit, not detail | H |
| 8 | Evaluation | Lessons from the Trenches on Reproducible Evaluation of Language Models | Biderman et al., 2024 | 2405.14782; preprint | The evaluation-harness authors' checklist on prompt and format sensitivity, scoring choices and reporting | H |
| 9 | Legal | AI Act Evaluation Benchmark: An Open, Transparent, and Reproducible Evaluation Dataset for NLP and RAG Systems | Davvetas et al., 2026 | 2603.09435; preprint | 339 scenarios labelled prohibited, high-risk, limited or minimal, plus article retrieval; a retrieval baseline scored weighted F1 0.69, weakest on minimal. Caveats: written by gpt-oss-120b, only partial human checks, no licence stated | H |
| 10 | Legal | COMPL-AI Framework: A Technical Interpretation and LLM Benchmarking Suite for the EU Artificial Intelligence Act | Guldimann et al., 2024 | 2410.07959; preprint, widely cited | Maps Act articles to concrete technical checks; grounds article citations and what a classifier can honestly claim | M |
| 11 | Abstention | Alignment for Honesty | Yang et al., 2023 | 2312.07000; NeurIPS 2024 | Defines honesty as declining what the model does not know, with data recipes and metrics (prudence, over-conservativeness) that fit the review option | M |
| 12 | Legal | LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models | Guha et al., 2023 | 2308.11462; NeurIPS 2023 Datasets and Benchmarks | 162 legal tasks including rule application and issue spotting; a template for case-style evaluation and a check on a base model's legal ability | M |
| 13 | Abstention | Language Models (Mostly) Know What They Know | Kadavath et al., 2022 | 2207.05221; preprint, widely cited | Models can predict whether they know an answer, but calibration improves with scale: a caution before trusting a 0.8B model's confidence | M |
| 14 | Abstention | Selective Question Answering under Domain Shift | Kamath et al., 2020 | 2006.09462; ACL 2020 | Selective prediction with a trained calibrator and coverage-risk curves; the standard way to report accuracy at a given coverage | M |
| 15 | Classification | Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models | Tam et al., 2024 | 2408.02442; EMNLP 2024 Industry Track | Strict JSON constraints can hurt reasoning while looser format instructions hurt less; informs the tier, citation and reason output schema | M |
| 16 | Legal | LawInstruct: A Resource for Studying Language Model Adaptation to the Legal Domain | Niklaus et al., 2024 | 2404.02127; Findings of NAACL 2025 | Legal instruction tuning of small models lifts LegalBench scores; small models gain from domain-specific instruction data | M |

Two further entries from this sweep are placed elsewhere: *LIMA* in section C, and *Judging LLM-as-a-Judge* (Zheng et al., 2023), already on the roster through the evaluation file.

**Checked and excluded.** SaulLM-7B (2403.03883): 7B exceeds the memory budget. LexGLUE (2110.00976): encoder-era and no AI Act tiers; it stays on the roster as expectation-setting, not as a target. "Language Models for Text Classification: Is In-Context Learning Enough?" (2403.17661): duplicates entry 7's finding. AIR-Bench 2024 (2407.17436): tests refusals, not risk tiers. "NLP Evaluation in Trouble" on data contamination (2310.18018): this project's test cases are freshly written. "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge" (2410.02736, ICLR 2025): judging is not central.

**Verification note.** All titles, first authors, years and identifiers were verified on arxiv.org abstract pages; venues as stated on arXiv or confirmed in the ACL Anthology, ICLR proceedings or TMLR listings. "Preprint" means no venue was found.

## Recommended for the expert roster

The reading list is for reading. The roster is for citing in decisions, and every entry on it is scored with evidence. Of the sixty papers above, these change a decision in this project and are not already proposed in `init/init-001.md`. Recommendation: score and add these eight in one pass, alongside the ten already proposed and the two AI-assisted-development authorities.

| Paper | What it decides | Phase it enters |
|---|---|---|
| Lu et al., Small Language Models survey | The bake-off's frame: which measurements to take on this Mac | Requirements |
| Dominguez-Olmedo et al., Lawma | The data budget: a few hundred to a thousand examples per task, and evidence that even sub-1B models can beat commercial ones on narrow legal labelling | Requirements |
| Gekhman et al., fine-tuning on new knowledge | The design rule's published evidence: facts in a table, judgement in weights | Requirements |
| Davvetas et al., AI Act Evaluation Benchmark | An external yardstick for the evaluation, and a warning about the minimal tier | Requirements |
| Miller, Adding Error Bars to Evals | How every result is reported: with an interval | Requirements |
| Biderman et al., LoRA Learns Less and Forgets Less | The adapter settings and their limits | Tech spec |
| Lee et al., Learning Rate Matters | What to sweep first, and what not to bother with | Tech spec |
| Zhang et al., R-Tuning | How the "needs human review" label is trained | Tech spec |

Held for the tech spec, when the data pipeline is designed: Hsieh et al. (rationales), Chen et al. AlpaGasus and Panickssery et al. (judge filter design), Srivastava et al. (format compliance of small models), Tam et al. (output schema). Already proposed or on the roster: Hu, Dettmers, Zhou, Wang, Zheng, Chalkidis.

## Totals and what was not found

| | |
|---|---|
| Sweeps | 4, run in parallel, each verified on arxiv.org |
| Papers listed | 61 table rows, 60 distinct papers; Gekhman et al. appears under both the data theme and the abstention theme because it bears on both |
| Papers checked and excluded | 25, each with a reason; one of them (Bucher and Martini) was excluded by one sweep as encoder-based and kept by another with that caveat stated |
| Marked "(unverified)" | 0 |
| Gaps the sweeps could not fill | No arXiv paper on `mlx-lm` fine-tuning or on Apple's MLX framework itself; no Qwen3.5 or Granite 4.0 technical report on arXiv; no strong-venue head-to-head of judge-filtered against unfiltered synthetic data; no paper isolating label-noise effects in language-model fine-tuning |

Two entries are younger than six months (2606.22606, 2607.03801), and one (2602.04998) is from February 2026 and listed as a NeurIPS 2026 poster. Young papers are kept because they are the only ones that test sub-1B Qwen models on classification-style tasks, and they are marked as preprints where no venue exists. They are evidence to weigh, not settled results.

## Changelog

| Date | Change | Reason | Author |
|---|---|---|---|
| 2026-10-26 | Corrected the venue for Lee et al. (2602.04998): not an ICML 2026 main-conference paper; listed as a NeurIPS 2026 poster and at two ICML 2026 workshops. Added the AI Act benchmark's stated caveats (generated by gpt-oss-120b, partial human checks, no licence) | Found by the independent scoring pass before these papers joined the roster | AI |
| 2026-10-26 | Corrected the Lawma entry (section C, rank 3), the start-here line and the roster table: example count is "a few hundred to a thousand" per task, not "tens to a few hundred"; the comparison is with GPT-4.5 and Claude 3.7 Sonnet, not GPT-4; the tested models run from 135M to 70B parameters | Re-checked against the paper's current version (v2, April 2025) before scoring it for the roster; the sweep had reported figures from an earlier version | AI |
