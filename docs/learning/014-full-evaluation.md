# 014. The full scoring report (P1-C04)

**Step:** build chunk P1-C04, full evaluation. **Date:** 2026-10-27.

## The lesson before the step

Words first:

- **Proportion.** A share: "7 of 10 right".
- **Denominator.** The "of 10". Picking the wrong one is the quietest way to fake a
  result. Annex III area accuracy, for example, counts only Annex III cases.
- **95% interval (confidence interval).** An honest range around a share. With 10
  cases, "7 of 10" is compatible with anything from 40% to 89%. More cases, narrower
  range. We use the **Wilson** formula, made for small samples.
- **Paired comparison.** Two models judged on the same cases, case by case.
- **Bootstrap.** Re-draw the cases at random 10,000 times, recompute the difference
  each time, and see how much it wobbles. A "gain" counts only if the whole range is
  above zero.
- **Citation validity / overlap.** Does a cited article exist? Does the answer share
  at least one article with the right answer?
- **metrics.json.** The same numbers in a file a program can read, for the later comparison.

**What usually goes wrong:** wrong denominators; quietly dropping unreadable
answers (which flatters a model); and shares shown without a range.

## What we did

1. **Read the law itself.** With your permission, Claude read the official texts on
   EUR-Lex: the AI Act and its July 2026 amendment. From them it built
   `data/articles.json`: every article's numbered paragraphs and every annex's points.
   The amendment added Articles 4a, 60a and 75a to 75d, new paragraphs (such as
   Article 6(1a) to 6(1c)), a new Annex XIV, and deleted Article 10(5) and Annex I
   point 1. So "Art. 147" (invented) and "Art. 10(5)" (deleted) both count as invalid.
2. **Statistics.** Wilson intervals, the paired bootstrap, and Cohen's kappa (needed
   later, when a second reader re-labels a sample of cases), each pinned by a
   known-answer test.
3. **The report.** It opens with a plain-English summary, including what the
   numbers *don't* show. Then 13 measures, each with its 95% interval, then the
   confusion table. It also writes `metrics.json`.
4. **Paired mode.** `--paired <other run>` compares two models. It refuses if either
   one lacks any case, names the missing cases, and writes nothing.

## What went wrong and how it was caught

The independent reviewer noticed that Article 3, the definitions, had an empty list
in the table. Article 3 has no numbered *paragraphs*; it has numbered *definitions*
(point 1 is "AI system"), and lawyers cite them as "Art. 3(1)". So a model citing
the definition of an AI system correctly would have been marked as inventing law.
Fixed: Article 3 now lists points 1 to 68, plus 14a and 14b, which the 2026
amendment inserted. Smaller fixes: "Art. 6(1A)" with a capital letter is now
accepted, and an empty answer no longer counts as "text scanned for dates".

## What the practice exam now says

On the 10-case fixture: tier right 7 of 10 (70%), **95% interval 40% to 89%**. That
range is the honest message. Ten cases cannot tell a 50% model from an 85% one.
That is why the real exam needs about 100 cases.

## Terms that came up

- **Wilson interval.** The formula for the range around a share; works even at 0 of 10 or 10 of 10.
- **Percentile.** The 2.5th percentile is the value 2.5% of results fall below.
- **Cohen's kappa.** Agreement between two people labelling the same cases, corrected for agreement by luck.
- **Consolidated text.** The law with all amendments merged in. We built ours from the original plus the amendment.

## What you just learned

1. A number without its range overstates what you know.
2. The denominator decides what a number means; it must match the definition.
3. Comparisons are fair only on the same cases, so incomplete pairs are refused.

## Check questions

1. Model A scores 8 of 10, model B 7 of 10. Can you say A is better? What would you look at?
2. Why does an unreadable answer stay in the "of 10"?
3. Why is "Art. 10(5)" invalid today but would have been valid in 2025?
