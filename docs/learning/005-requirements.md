# 005. Requirements: saying what, testably

**Step:** `/gvm-requirements`, slice 1. **Date:** 2026-10-26.
**Output:** `requirements/requirements.md` and `.html`, `risks/risk-assessment.md`.

## The lesson before the step

**What we did.** Wrote what the first slice must do as 44 short, numbered
sentences. Each has a priority (Must, Should, Could, Won't), a way to check it,
and a pointer to one deliverable on the impact map. None says how to build
anything: no file formats, no libraries, no code.

**Why.** A requirement you cannot test is a wish. Writing the check beside each
one stops slippery words like "accurate" or "good enough" from surviving.

**What usually goes wrong.** Vague words; design decisions smuggled in; scope
creep. Training, the adapter and everything after it are written down as Won't
for this slice so the boundary is visible.

## What you decided

- **Six labels plus a flag:** prohibited, high-risk (with its route), transparency-only,
  minimal, out of scope, needs human review; and a yes/no flag for Article 50,
  because a high-risk system can also be a chatbot.
- **A boundary-weighted gold set:** 100 cases, heavy on the Annex III versus
  Article 50 boundary and on the minimal tier. I draft, you judge every case.
- **A blind self-check:** 20 cases re-labelled after two days, target kappa 0.8.
- **Four candidates:** Qwen3.5-0.8B, Llama 3.2 1B, Gemma 3 1B, and EuroLLM-1.7B,
  an EU-funded, Apache-licensed model neither of us had first thought of.
- **The final test is separate:** the gold set serves the bake-off; a fresh
  test set, touched once, judges G-1 later.

## Terms that came up

- **MoSCoW.** Must, Should, Could, Won't. Won't means "not this slice", not "never".
- **Traceability tag.** `[impact-deliverable: D-2]` on a requirement: the link
  back up the impact map. The method refuses a requirement without one.
- **Risk assessment.** Four questions asked before requirements: will it be
  valuable, usable, feasible, viable?
- **Cohen's kappa.** Agreement between two labellings, corrected for the
  agreement you would get by chance. 1 is perfect; 0.8 is strong.
- **Zero-shot.** Asking an untuned model to do the task from instructions alone,
  with no worked examples. It is the "before" picture.

## What you just learned

- Every number this project reports will carry an interval, because 100 cases
  is a small sample.
- The measuring stick comes before the model. You will see four untuned models
  measured before any training.
- Keeping the final test separate costs about two hours of labelling and buys
  an honest final number.

## Check questions

1. Why is "the model is accurate" not a requirement, and what would turn it into one?
2. Why does a separate Article 50 flag matter for a recruitment chatbot?
3. With only 40 cases, why could four models not be told apart?
