# 003. When two scorers disagree

**Step:** approving the expert roster, end of `/gvm-init`. **Date:** 2026-10-26.
**Output:** twenty entries in the shared expert library, `scoring-reports/expert-scoring-002.md`, and `init/expert-library-additions-001.md`.

## The lesson before the step

**What we did.** Every authority on the roster is scored twice: once by the
session doing the work, once by a fresh agent that sees only names and titles.
Where they agree, the score stands. Where they differ by one point, the lower
score is kept. Where they differ by two or more, neither scorer decides; the
owner does.

**Why a human decides the big gaps.** Two passes from the same family of model
can share the same blind spot and agree confidently on a wrong answer. A large
disagreement is the moment the method can see that one pass knows something the
other does not. That is exactly when a person with judgement should look.

**What usually goes wrong.** Splitting the difference. Averaging a 2 and a 4 into
a 3 hides the reason they differed. The right move is to read both reasons and
pick the one that is better evidenced.

## What happened

Five scores differed by two or more points. You settled all five:

- **Lee et al.** My pass scored the authors low because I did not recognise
  them. The independent pass looked them up and found a senior IBM researcher.
  You took the independent score. The lesson: not knowing someone is not
  evidence that they are weak.
- **Lu et al.** We disagreed on what "Publication" measures: this one preprint,
  or where the team usually publishes. You took the method's reading, the
  team's venues.
- **Osmani's essay, the METR trial.** Both are about AI coding tools, which
  change fast. You took the lower "currency" score for both: the arguments
  hold, the examples have aged.
- **Biderman et al.** You took the lower score, the cautious choice, since the
  band did not change either way.

The independent pass also caught three factual errors before anything was
saved: a paper's conference was wrong, a book's subtitle was wrong, and a
benchmark we were about to rely on turned out to be written by a model with only
partial human checks and no stated licence.

And one error was caught by checking the source before scoring: the reading list
had said the Lawma paper needed "tens to a few hundred" examples per task. Its
current version says "a few hundred to a thousand", and it tests models as small
as 135 million parameters. The list now says so.

## Terms that came up

- **Divergence.** Two scores for the same thing that differ by two or more points.
- **Boundary case.** One pass put the entry in a different band from the final
  one. Eight entries were boundary cases this round; all are flagged in the
  scoring report.
- **Mirror.** A copy of what was written to the shared library, kept in this
  repository so its history records the change.

## What you just learned

- A second opinion is only useful if disagreements are read, not averaged.
- Ignorance looks like low scores. Check before you score.
- Verification pays for itself early. Three errors were caught before they
  could reach a requirement.

## Check questions

1. Why does the method keep the lower score on a one-point split, but hand a
   two-point split to you?
2. The AI Act benchmark has no stated licence. What does that change about how
   we may use it?
3. Which of today's five decisions would you make differently if the band had
   changed, and why?
