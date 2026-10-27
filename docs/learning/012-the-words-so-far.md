# 012. The words so far, slowly

**Step:** catch-up after practice run 001. **Date:** 2026-10-27.

## Why this entry exists

After the first fine-tune, the owner said: "so many concepts here I don't
understand… I feel I ain't learning." That was fair. Earlier entries used words
before explaining them, and some settings (the token limit, the maximum sequence
length) were chosen by Claude as "routine mechanics" and mentioned only in
passing. This entry goes back over every term met so far, in the order they
matter, each with a picture, what it was in our own run, and one check question.

The running picture from entry 000 stays: the model is a **junior colleague**
who has read a huge amount but has never done our job.

**Prefer watching?** Open `012-video.html` (in this folder) in a browser: a
narrated film of this entry, about seven minutes, with chapters.

---

## Part 0. Which kind of training did we do?

There are three common ways to train a language model:

| Kind | What the model sees | What it learns |
|---|---|---|
| **Pretraining** (or *continued* pretraining, on one field's text) | Piles of plain text, no questions | Language, facts, the style of a field |
| **Instruction fine-tuning** (also called supervised fine-tuning) | A question plus the right answer | To answer a task in a set format |
| **RLHF** (reinforcement learning from human feedback) | Its own answers, ranked by people | Which answers people prefer |

**We did instruction fine-tuning, with LoRA.** Each of the 287 practice cards was a
description of an AI system (the question) and the right answer (tier, articles,
reason). The setting `mask_prompt: true` means only the answer part counted towards
the loss: the model was marked on what it wrote, not on re-reading the question.

The model's makers had already done the expensive first stage, and general
instruction training, before we downloaded it. We did not do continued
pretraining (we never fed it raw regulation text) and we did not do RLHF (nobody
ranked its answers).

**Check:** If you fed the model the whole text of the AI Act with no questions,
which of the three would that be, and would it learn our answer format?

---

## Part 1. What the model is

### Weights and parameters

**Picture.** The colleague's brain is a giant panel of dials. Each dial is a number.
When a question comes in, it flows through the dials and an answer comes out.
Which answer depends entirely on where the dials are set.

- A **parameter** is one dial. **Weights** is the usual name for all the dials together.
- **0.8B** means about 0.8 billion dials. Our model, Qwen3.5-0.8B, reported
  752 million. Big chat models have hundreds of billions.
- **Training** means turning dials so the answers get better. Nothing else changes:
  no rules are written, no facts are stored in a table. Only dials move.

**Why it matters for us.** Because knowledge lives in dials, it cannot be edited
like a spreadsheet. That is why dates and deadlines live in a lookup table, never
in the model (the design rule in `CLAUDE.md`).

**Check:** If the AI Act moved a deadline tomorrow, why would we not retrain the model?

### Tokens and the token limit

**Picture.** The colleague does not read letters or whole words. It reads
**tokens**: word-pieces. "classification" might be two tokens, "the" one. It also
*writes* one token at a time, each time asking "what is the most likely next piece?"
and then repeating.

- A typical answer from our model is 100 to 200 tokens.
- The **token limit** (`MAX_TOKENS = 400` in `lab/bakeoff.py`) is the most an
  answer may be before we cut it off.

**When was it set?** In build chunk P1-C02 (entry 010), the day we first ran the
real model on this Mac. Claude chose it as a routine setting and should have
explained it then.

**Why was it set?** Because the colleague writes one piece at a time, it never
"knows" it is finished until it writes a special stop token. If it never writes
one, it would keep going forever. The limit is a safety stop: it bounds how long
each answer can take, and 400 is roughly twice a normal answer, so honest answers
are never cut.

**Where you saw it bite.** At step 200 of the practice run, answers got stuck
writing "Art. 99, Art. 99, …". They never wrote the stop token, hit 400, got cut
off mid-sentence, and so could not be read. Unreadable counts as wrong. The limit
did its job: it turned an endless loop into a visible failure.

A second, related limit: **max sequence length** (`max_seq_length: 1024` in the
training settings). That is the longest *question plus answer* used during
training. Our examples are well under it; it exists so one giant example cannot
blow up memory.

**Check:** Would raising the limit to 4,000 have rescued the step-200 answers?

### 4-bit and quantisation

**Picture.** Each dial's setting is stored as a number. Stored precisely (16 bits),
the dial can sit at about 65,000 positions. Stored in **4 bits**, it can sit at 16.
That is like rounding every price to the nearest pound: you lose a little detail,
but the price list gets four times smaller.

- **Quantisation** is that rounding.
- Our 752 million dials at 16 bits would take about 1.5 GB; at 4 bits, under 0.5 GB.
  On an 8 GB Mac that is the difference between fitting and not.
- The cost: a slightly less precise colleague. For a small model on a narrow task,
  usually acceptable; we measure rather than assume.

**Check:** What do we give up by using 4-bit, and why did we accept it?

---

## Part 2. How training works

### Loss

**Picture.** You show the colleague a practice card: a description of an AI system
and the correct answer. The colleague guesses, one token at a time. For each token,
we ask: "how surprised were you by the right answer?" Very surprised means a high
number; expected it means near zero. Average those surprises: that is the **loss**.

- Lower loss means the colleague's guesses are closer to the right answers.
- Loss is a *score of surprise*, not a percentage right. A loss of 0.15 does not
  mean 85% correct.

### Training loss vs validation loss

**Picture.** Two piles of cards.

- **Training cards** (287 in our run): the colleague studies these and the dials
  are turned after each one. **Training loss** is the surprise on these.
- **Validation cards** (32): never used to turn dials. Every 25 steps we pause and
  check the surprise on them. That is **validation loss**.

Training loss always falls eventually: the colleague is studying those exact cards.
Validation loss tells you whether it learned something that carries over to cards
it has not seen. In our run validation loss fell from 1.003 to 0.149.

**What usually goes wrong:** the training loss keeps falling while the validation
loss stops falling or climbs. That is the sign of memorising (Part 4).

**Check:** Why can the training loss alone not tell you the model is getting better?

### Steps, batch size, learning rate

**Picture.** One **step** = show some cards, measure the loss, turn the dials a bit.

- **Batch size** = how many cards per step. Ours was 1, because 4 did not fit in
  memory. A bigger batch gives a steadier nudge; a batch of 1 gives a jumpier one,
  which is why the training loss bounced around (you saw 2.06 then 2.09 early on:
  that is normal noise, not a problem).
- **Steps (iterations)** = how many nudges in total. We did 300. With 287 cards and
  batch 1, that is roughly one pass through the pile.
- **Learning rate** = how big each nudge is. Ours was 0.0001. Too big and the dials
  overshoot and the model gets worse or erratic; too small and nothing changes in
  300 steps.

The progress line you asked about, "65% 201/300", meant: step 201 of 300 done, 65%
of the way through.

**Check:** If the loss jumped up and down wildly and never settled, which setting
would you lower first?

---

## Part 3. LoRA: training cheaply

### LoRA, adapter, rank, layers

**Picture.** Turning all 752 million dials needs far more memory than this Mac has,
and risks breaking what the colleague already knows. So we **freeze** the original
dials and clip small **sticky notes** onto some of them. The sticky notes say
"when you see this, shift your answer a little this way." Only the sticky notes are
trained.

- **LoRA** is that technique.
- **Adapter** is the file holding the sticky notes. Ours is 7.2 MB, beside a model
  of nearly 0.5 GB. We trained 1.8 million numbers: 0.24% of the model.
- **Layers.** The model is a stack of 24 processing stages, like floors in a
  building; each floor refines the answer a bit more. We put sticky notes on the
  top 8 floors only (16 used 7.1 GB, too close to the edge; 8 used 6.4 GB).
- **Rank** = how much each sticky note can say. Rank 8 is a small note; rank 64 a
  big one. Bigger notes can learn more, but cost more memory and memorise more easily.
  For a narrow task like ours, 8 is the usual starting point.

**Common mistake (the quiz question you missed):** LoRA does not delete or replace
layers. The original model is untouched; switch off the adapter and you have the
original colleague back.

**Check:** What is inside the 7.2 MB adapter file, and what is not?

---

## Part 4. Memory and saving

### GPU memory and gradient checkpointing

**Picture.** While learning from a card, the colleague keeps scratch notes of every
intermediate thought, because turning the dials needs to look back at them. Those
scratch notes fill the desk (GPU memory). On an 8 GB Mac, the desk is small, and
macOS and the apps share it.

- Batch 4 meant four cards' worth of scratch notes: the desk overflowed (out of memory).
- Even batch 1 overflowed.
- **Gradient checkpointing** = throw most scratch notes away and rewrite them when
  needed. Slower (we did not measure by how much); much less desk space. That is what made it fit.
- The laptop got hot because the graphics chip ran flat out for 12 minutes. Normal.

**Check:** What did gradient checkpointing trade away to fit in memory?

### Snapshots (checkpoints)

Every 25 steps the adapter was saved to disk: a **snapshot**. That let us test the
step-200 sticky notes and the step-300 ones separately, and that is how we found
the looping problem at step 200.

---

## Part 5. Judging the result

### Held-out cases, before and after

**Picture.** An exam the colleague has never seen.

- **Held-out cases** (20 in our run, 5 per tier) are kept out of training *and*
  validation entirely. They are only used to mark the final exam.
- **Before** = the exam taken by the untrained colleague: 5 of 20, because it said
  "high-risk" every time and a quarter of the answers happened to be high-risk.
- **After** = the same exam with the sticky notes on: 16 of 20.

Why separate from validation? Because we *looked at* validation loss to decide
things during training. Anything you use to make decisions stops being a fair exam.

### Overfitting and memorising

**Overfitting** = the colleague learns the practice cards so exactly that it does
worse on new ones; like a student who memorised last year's answers instead of the
method. Signs: training loss keeps falling, validation loss stalls or rises, and the
held-out score is poor. We did not see that clearly in run 001, but with only 287
cards and rank 8 it is the main thing to watch next.

**The step-200 lesson.** Loss looked good at step 200, yet zero answers were usable.
Loss measures surprise token by token; it does not check that an answer *finishes*.
That is why we always read real answers, not just the numbers.

**Check:** Why can we not use the validation cards as the final exam?

---

## What you just learned

1. The model is dials; training turns dials; LoRA trains small sticky notes instead.
2. Loss is surprise, not accuracy; validation loss is the honest one; held-out
   cases are the real exam.
3. On 8 GB, memory decides: 4-bit, batch 1, gradient checkpointing, 8 layers.
4. The token limit is a safety stop that turned a loop into a visible failure.
