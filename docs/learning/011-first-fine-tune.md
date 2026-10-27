# 011. Your first fine-tune

**Step:** P1-C02b, practice run 001. **Date:** 2026-10-27. **Notebook:** `notebook/2026-10-27-01.md`.

## The lesson before the step

LoRA clips small "sticky notes" onto a frozen model and trains only those.
Training shows the model an example, measures how wrong it was (the loss), and
nudges the sticky notes. Two losses matter: training loss on the practice cards,
and validation loss on cards it never trains on. When validation stops falling
while training keeps falling, the model is memorising.

## What you did

You chose the settings (rank 8, learning rate 0.0001; then 8 layers after the
memory test), typed the command, and watched 300 steps over 12 minutes.

## What happened

- **Before:** the untrained model said "high-risk" for all 20 held-out cases: 5 right
  by luck.
- **After:** 16 of 20 right, across all four labels.
- **The surprise:** halfway through (step 200), the loss looked good, but every
  answer got stuck repeating "Art. 99, Art. 99…" and never finished. By step 300,
  19 of 20 answers finished properly.

## Terms that came up

- **Snapshot (checkpoint).** The sticky notes saved at a given step; 7.2 MB each.
- **Gradient checkpointing.** Recomputing some values instead of storing them:
  slower, but it fits in memory.
- **Batch size.** How many examples per nudge. Ours had to be 1.
- **Degenerate repetition.** A model stuck repeating itself until the length limit.
- **Token cap.** The maximum length of an answer (400 word-pieces here).

## What you just learned

- A falling loss is necessary, not sufficient: always read real answers.
- The data teaches habits as well as answers. Messy article lists taught looping.
- On 8 GB, memory sets the rules: batch size 1, gradient checkpointing, fewer layers.

## Check questions

1. Step 200 had a lower validation loss than step 150, yet zero usable answers. How?
2. Why did the untrained model's 5 out of 20 mean nothing?
3. What would you change in the training data before the next run, and why?
