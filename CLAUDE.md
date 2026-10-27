# AI Act Lab: project instructions

What this is: read `README.md`, then `docs/00-plan.md` and `docs/01-glossary.md`.
Those hold every decision taken so far and the reasons.

**This repo is PUBLIC** at https://github.com/oza977-max/ai-act-lab, made public by
the owner on 2026-10-26. Every push is world-readable the moment it lands, so the
confidentiality check runs before every commit. There is no margin for a quiet fix-up.

## House rules

- **The owner is non-technical on git and new to model training.** Handle all git
  mechanics. Commit and push at every meaningful milestone. Never ask the owner to
  run git commands.
- **Learn as you build.** The owner is fine-tuning for the first time. Learning is a
  deliverable alongside the model, and a functional requirement, not tone. For
  every step:
  - Teach just in time. Introduce a concept when the work needs it, including what
    each GVM phase is for. No opening lectures.
  - Before the step, give a short plain-English lesson: what we are doing, why, and
    what usually goes wrong.
  - The owner makes the decisions that carry the learning: label scheme, gold-set
    judgements, base model, training settings. Give options, trade-offs and a
    recommendation, then let the owner choose. Routine mechanics stay with Claude.
  - After the step, give a "what you just learned" recap with two or three check
    questions.
  - Add an entry to `docs/learning/`, the owner's own textbook. It is separate from
    the training-run notebook.
  - Offer the owner the exact training and evaluation commands to run themselves.
    Never git.
  - Keep requirement slices thin so building starts early.
  Every explanation must be one the owner could repeat to a colleague.
- **The README is the public story.** The repo is meant to teach others. At every
  milestone, update `README.md`: status, what was measured, decisions and why, and
  what went wrong and how it was caught. Plain English, honest, no internal names.
- **The repo is a showcase for learners.** The owner wants it to be the best
  public example of learning fine-tuning with GVM: easy for anyone to follow, with
  live stats. Keep it that way without being asked: at every milestone run
  `.venv/bin/python scripts/repo_stats.py` (refreshes the README's "Progress at a
  glance" block from the repo; never hand-edit that block), keep the README's
  "Start here" paths, the learning index and `docs/how-this-was-built.md` current.
- **Confidentiality is a hard rule.** No employer name, no internal figures, no
  internal team or committee names, anywhere in the repo or its history. Public
  regulation text and freshly written cases only.
- **Honesty is a functional requirement.** Never claim more than the measurements
  show. Report test numbers as measured, including failures. "Needs human review"
  is a first-class output, not a failure.
- **Hardware:** Apple M2, 8 GB memory, macOS. Training must fit. Qwen3.5-0.8B
  4-bit LoRA through `mlx-lm` is the baseline, 2B the stretch.
- **Method:** GVM pipeline, one phase at a time, owner reviews between phases. No
  parallel builds, no extras the spec did not ask for. Stop and ask when the spec
  is silent.
- **Design rule:** the model learns judgement and output format. Dates, deadlines
  and obligation lists live in a maintained lookup table, never in the weights.
- **Lab notebook:** every training run gets an entry in `notebook/`: what changed,
  what was expected, what happened, next try.
- **Python:** one project virtual environment, pinned versions. Model weights and
  adapters are never committed; datasets and evaluation results are.
