# 000. The whole picture, in plain English

Read this first. Everything else in this folder is a detail of one of these steps.

## What we are building

A small AI model that makes a first pass at triaging AI systems under the EU AI Act,
running on a laptop. Someone describes a system in plain English ("a tool that
screens job applicants"). The model says which risk category it falls in, which
article applies, and why in one sentence; or, when unsure, "needs a human". A
separate, hand-maintained table adds the deadlines and duties for that category.
The model never guesses dates, because the law keeps changing them.

## The analogy: training a new junior colleague

| Step | Junior-colleague version | What we actually do |
|---|---|---|
| 1. Write the rulebook | A short guide to how you classify, with worked examples | The labelling guideline |
| 2. Make an answer key | 100 example cases checked by an expert | The gold set: the ruler everything is measured against |
| 3. Test candidates before hiring | Four applicants take the same 100 cases, untrained | The bake-off: four small models, scored, one chosen |
| 4. Train the chosen one | Lots of practice cases with model answers | Fine-tuning with LoRA: small "sticky notes" clipped onto the model, and only those are trained |
| 5. Final exam | Fresh cases never seen before | The held-out test: right 9 times in 10 when it answers? |
| 6. Put it to work | A desk of its own | A small app that answers and attaches the dates table |

## Why in this order

You cannot tell whether training helped without an answer key, so the ruler (steps 1
and 2) comes before the training (step 4). A practice training run on public data
happens early anyway, like a driving lesson in a car park: nothing counts, but the
controls become familiar.

## Who does what

The owner makes the judgement calls (the rules, checking the 100 cases, choosing the
model), runs the training, and reviews each step. Claude handles the code, the
checks, and the paperwork.

## Check questions

1. Why does the model never output dates?
2. Why build the answer key before training?
3. What does "needs a human" protect against?
