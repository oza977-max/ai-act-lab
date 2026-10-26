# AI Act Lab: project instructions

What this is: read `README.md`, then `docs/00-plan.md` and `docs/01-glossary.md`.
Those hold every decision taken so far and the reasons.

## House rules

- **The owner is non-technical on git and new to model training.** Handle all git
  mechanics. Commit and push at every meaningful milestone. Never ask the owner to
  run git commands.
- **Teach as you go.** Every step gets a plain-English explanation the owner could
  repeat to a colleague. This is a functional requirement, not tone.
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
