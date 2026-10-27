# 018. The gold set and its tools (P3-C01)

**Step:** build chunk P3-C01, gold tooling. **Date:** 2026-10-27.

## The lesson before the step

Words first:

- **Gold set.** The 100 hand-checked cases that become the real exam for every
  model. "Gold" means its labels are treated as correct.
- **Draft.** Claude writes each case with a proposed answer (label, articles,
  reason). Your judgement turns it into the gold label.
- **Review sheet.** A spreadsheet (CSV file) you open in Numbers: one row per case.
  In `decision` you write **accept**, **change** (and fill the `final_` columns)
  or **doubt** (unsure; it must be settled before the set is built).
- **CSV.** Comma-separated values: a plain-text table any spreadsheet app opens.
- **Formula injection.** A spreadsheet runs a cell starting with `=` as a formula,
  so the tool puts an apostrophe before any cell starting with `=`, `+`, `-` or `@`.
- **Quota.** A minimum the set must meet: every Annex III area at least 3 times,
  at least 15 boundary cases, 5 that turn on Article 6(3), 5 with a hidden
  instruction.
- **Hash (SHA-256).** A fingerprint of a file. Change one character and the
  fingerprint changes, so a result can prove which gold set it was scored on.
- **Never-train.** Every gold case carries this mark. Exam questions must never
  become study material, or the exam measures memory, not judgement.

**What usually goes wrong:** spreadsheet apps quietly change text (curly quotes,
trimmed spaces), so the tool compares each description with the original draft.
And "doubt" cases get forgotten, so the build refuses while any remain.

## What we did

1. Wrote the test first: a whole simulated run, from 100 drafts to five sheets,
   your decisions (one of them a change), the check, and the build, ending with
   a gold file the evaluation can read.
2. Built `python -m lab.gold`:
   - `sheet` turns a draft file into a review sheet, and never overwrites one
     that may already hold your decisions;
   - `check` reads your filled sheet, never edits it, and names every problem by
     case id ("GC-007: no decision");
   - `build` refuses while any doubt remains or any quota is missed, records which
     cases you changed and the share changed, marks every case never-train, and
     writes `gold-v1.jsonl` with its fingerprint.

## What went wrong and how it was caught

- The first full test run failed with "Annex III area 8 has 1 case; it needs 3".
  The tool was right: the test's own made-up spread was wrong. A quota check that
  catches its author's mistake on the first day is doing its job.

- Independent reviewers needed three rounds (5, 1, 0 serious findings). The worst
  find: if you typed a new label but left the decision as "accept", your label
  would have been ignored without a word. Now the check stops and says so. The
  rest were everyday spreadsheet habits (a trailing space, "4.0" instead of "4",
  a capital letter, blank rows) that could have locked you out; all are handled.

## How you will review a batch (from the next step)

1. Open `data/gold/review/batch-01.csv` in Numbers.
2. Read each description. Check it names no real organisation, product or person.
3. Read the proposed label, articles and reason against the guideline.
4. In `decision`, write `accept`, `change` or `doubt`. On `change`, fill in the
   `final_` columns with the correct answer. Use `owner_note` for any thought.
5. Export as CSV (File > Export To > CSV), saving over the same file name.
6. Tell Claude; Claude runs `python -m lab.gold check` and reports any problem.

## Terms that came up

- **Batch.** 20 cases reviewed in one sitting; five batches make the set.
- **Share changed.** How many drafts you changed. A high share says the drafts (or
  the guideline) need work; it is reported, not hidden.

## What you just learned

1. A gold label is a person's judgement, recorded with what the draft said.
2. Tools that check, refuse and name the problem make a non-technical reviewer
   safe: nothing wrong slips through silently.
3. Exam cases must never be used for training.

## Check questions

1. You are unsure about a case. What do you write, and what happens at build time?
2. Why does the tool compare your sheet's descriptions with the draft file?
3. Why must gold cases never be used to train the model?
