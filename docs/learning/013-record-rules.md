# 013. The rules for a proper answer (P1-C03)

**Step:** build chunk P1-C03, record rules. **Date:** 2026-10-27.

## The lesson before the step

Words first:

- **Record.** A filled-in form with nine boxes (**fields**): `tier`, `route`,
  `annex_iii_area`, `annex_iii_point`, `annex_i_legislation`, `art50_flag`,
  `articles`, `review_reason`, `reason`.
- **JSON.** How the form is written as text: `{"tier": "minimal", "art50_flag": false, ...}`.
- **Parse.** Pulling the form out of the model's text.
- **Validate.** Checking the form against the rules.

Before this step, the marker only checked that the tier was one of the six
allowed words. A model could write a sloppy form and still score.

**What usually goes wrong:** markers that quietly fix broken answers (so a bad
model looks good), yes/no or numbers written as text slipping through, and date
detectors that flag the law's own name ("Regulation (EU) 2024/1689").

## What we did

Tests first, then code. The rules now enforced:

| Rule | Plain English |
|---|---|
| Route | High-risk must say *why*: Annex III (a listed use) or Annex I (a product). Every other tier leaves it empty. |
| Annex III details | Area is a whole number 1 to 8; the point (such as `4(a)`) must belong to that area. |
| Annex I details | Must name the product law (for example the lifts directive). |
| Article 50 flag | A real yes/no, never the text `"false"` or the number 0. |
| Articles | At least one citation, except for "needs human review". |
| Review reason | Required for "needs human review" (missing fact, conflicting facts, unsettled law); empty otherwise. |
| Reason | One sentence, at most 40 words. "Art." and "e.g." don't count as sentence ends. |
| Form itself | No missing boxes, no extra boxes, no box written twice. |

Break any rule and the answer is **unreadable**, which counts as wrong.

The **date detector** scans the model's whole text, even unreadable answers, and
the evaluation report now has a "Dates found" row. Dates must come from the
lookup table, never from the model.

## What went wrong and how it was caught

An independent reviewer threw about 60 hostile inputs at the code (lists where
words should be, deeply nested brackets, odd numbers). Nothing crashed. It found
three small issues, all fixed:

- "2 august 2026" (lowercase month) was missed. It now counts when a day comes
  first. "may 2026" in a sentence still doesn't count, because "may" is usually a verb.
- "Section 6.5.2026" was wrongly flagged as a date. Dotted dates now need two
  digits each ("02.08.2026").
- "Example Ltd." ended the sentence early, so a good one-sentence reason was
  rejected. Common abbreviations like "Ltd." and "Inc." are now allowed.

## Terms that came up

- **Validate / validation rule.** A check that returns a list of problems; an empty list means valid.
- **Unreadable (format failure).** An answer that isn't a valid form. It scores as wrong.
- **Duplicate key.** The same box filled in twice, such as two `tier` values. We refuse it rather than pick one.
- **False positive / false negative.** Flagging something that isn't a date / missing one that is.
- **Regular expression.** A pattern for matching text, such as "a number, a month name, a four-digit year".

## What you just learned

1. Strict marking keeps scores honest: the model must fill in the whole form correctly.
2. Untrusted text is read, never repaired.
3. Every detector makes two kinds of mistake, and tests pin down both.

## Check questions

1. The model answers `{"tier": "minimal", ..., "art50_flag": "false", ...}`. Readable or not, and why?
2. Why do we flag a date even when the rest of the answer is unreadable?
3. Why must the date detector *not* flag "Regulation (EU) 2024/1689"?
