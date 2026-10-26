# AI Act Lab: why, what, and the plan

Started 2026-10-26. Written from the research session that started the project.

## Why this project

The skill worth learning is not pretraining a model from scratch. That is a cluster
job and will stay one. The skill is shaping an existing small open model with your
own data, proving it got better, and shipping it to run locally. That craft is mostly
data and evaluation. It suits an owner who works by specifying, reviewing and
measuring.

The domain is the EU AI Act, because it is the most pressing AI regulation today and
it is the owner's own field.

## What we are building

An **EU AI Act triage model**.

Input: a plain-English description of an AI system and how it is used.

Output: a structured record with

- risk tier: prohibited, high-risk, transparency-only (Article 50), minimal, or
  needs human review
- the Annex III category when high-risk
- the article relied on
- a one-sentence reason

A small, maintained lookup table then attaches the current dates and duties for that
tier. The table is deterministic and reviewed by a human.

## The design decision that matters most

**The model learns judgement and output format. It must not learn dates, deadlines
or obligation lists.**

Reason: the Digital Omnibus on AI changed the dates in July 2026 and they will change
again. A model trained on the 2024 text would recite wrong dates with full
confidence. Every source read on legal and regulatory models agreed: facts through
lookup, behaviour through fine-tuning.

## The Act as of 2026-10-26

- Regulation (EU) 2024/1689, amended by Regulation (EU) 2026/1744, the Digital
  Omnibus on AI, in force since 27 July 2026.
- Annex III high-risk duties apply from 2 December 2027.
- Annex I high-risk duties apply from 2 August 2028.
- Two new Article 5 prohibitions, on non-consensual intimate imagery and on child
  sexual abuse material, apply from 2 December 2026.
- Prohibitions, AI literacy, general-purpose model rules and Article 50 transparency
  already apply.
- Article 50(2) grace period for generative systems already on the market: until
  2 December 2026.

These belong in the lookup table, each with a source link and a "last checked" date.

## Hardware and model

Apple M2, 8 GB memory. Figures below are from a comparable Mac MLX LoRA project, not
measured here yet.

| Model | Peak memory while training | Time per run |
|---|---|---|
| Qwen3.5-0.8B, 4-bit | 3.9 GB | about 15 min |
| Qwen3.5-2B, 4-bit | 5.9 GB | about 8 min |
| Qwen3.5-4B, 4-bit | 11.1 GB | does not fit |

Baseline: Qwen3.5-0.8B, 4-bit, LoRA through `mlx-lm`. Stretch: 2B with batch size 1
and gradient checkpointing. The Qwen3.5 small models are Apache 2.0 licensed.

## Data

- About 2,000 case descriptions written by a teacher model from the Act's text, each
  with tier, Annex category, article and reason.
- 100 cases hand-checked by the owner as the gold set. Hand-labelling effort goes to
  the hard boundary: Annex III high-risk versus Article 50 transparency-only.
- A judge pass filters the rest. Train, validation and test split. The test set is
  touched once, at the end.
- "Needs human review" is a first-class label.
- Precedent: a community classifier on Hugging Face reached 92% accuracy on about
  1,500 examples with five labels including "review". We aim to match it and add
  citations and reasons.
- Nothing from any employer. Public regulation text and freshly written cases only.

## Measurement

- Tier accuracy on the test set.
- Annex III category accuracy on high-risk cases.
- Citation validity: the cited article exists and is the right one, checked against
  a fixed citation table.
- Review behaviour: how often the model says "review" when the gold set says it
  should, and how often it does not.
- Baselines: untuned Qwen3.5-0.8B, 2B and 4B given the same prompt, so the gain
  from fine-tuning is visible.
- Validation loss alone is not trusted. The comparable project found it misleading.

## Shipping

Merge the adapters into the base model, convert to GGUF with the llama.cpp converter
(MLX's own GGUF export does not cover Qwen), load into Ollama with a short Modelfile,
wrap in a small local page that attaches the lookup table to the model's output. To
be verified when reached.

## How we work

- GVM pipeline, one phase at a time: init, impact map, requirements, test cases,
  tech spec, build. The owner reviews between phases.
- Every training run gets a lab-notebook entry in `notebook/`.
- Honesty: a 0.8B model is not a lawyer. The win is a triage assistant that is right
  about nine times in ten on clean descriptions, hands the rest to a human, and runs
  with no data leaving the laptop.

## Decisions log

- 2026-10-26: no toy-GPT warm-up; start with the real task.
- 2026-10-26: LoRA fine-tune, not retrieval-only and not full fine-tune.
- 2026-10-26: dates and duties in a lookup table, never in the weights.
- 2026-10-26: repo private until the owner decides otherwise.

## Sources

- [mlx-lm LoRA guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- [Mac MLX LoRA benchmark project](https://github.com/sciences44/mlx-lora-finetune)
- [Small-model tunability benchmark](https://www.distillabs.ai/blog/we-benchmarked-12-small-language-models-across-8-tasks-to-find-the-best-base-model-for-fine-tuning/)
- [Qwen3.5 small models](https://artificialanalysis.ai/articles/qwen3-5-small-models)
- [EU AI Act risk classifier on Hugging Face](https://huggingface.co/Samika16/ferendis-risk-classifier)
- [Digital Omnibus on AI, AI Act Explorer](https://artificialintelligenceact.eu/ai-act-explorer/digital-omnibus/)
- [Gibson Dunn on the Omnibus](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)
- [Ollama import docs](https://docs.ollama.com/import)
- [Fine-tuning versus retrieval](https://www.thenile.dev/blog/fine-tuning-or-rag)
- [Synthetic training data guide](https://blog.premai.io/how-to-generate-synthetic-training-data-for-llm-fine-tuning-2026-guide)
