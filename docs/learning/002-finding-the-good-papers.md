# 002. Finding the good papers: an arXiv sweep

**Step:** a side step inside `/gvm-init`, at the owner's request. **Date:** 2026-10-26.
**Output:** `docs/02-reading-list-slm-fine-tuning.md`.

## The lesson before the step

**What we are doing.** Searching arXiv, the open archive where nearly every
machine-learning paper appears first, for the papers worth knowing about
fine-tuning small language models, and sorting them for this project.

**Why.** Three reasons. The expert roster should rest on the field's actual
evidence, not on the first names that come to mind. Several decisions ahead (how
many cases, which settings, how to score "needs human review") have been studied,
and reading the study beats guessing. And a reading list is part of the textbook.

**What usually goes wrong.**

- Invented references. Language models produce plausible titles that do not
  exist. The cure is to check every entry against the arXiv page itself: title,
  first author, year, identifier.
- Reading titles, not findings. A paper's title says what it is about; its
  finding may cut the other way. Each entry here carries one sentence on what it
  found and why that matters to us.
- Famous is not the same as relevant. A landmark paper about 70-billion-parameter
  models may say nothing about a 0.8-billion one on a laptop.
- Recency bias in both directions. The newest paper is not yet checked by the
  field; the oldest may be superseded. Young papers are kept when they are the
  only evidence on our exact question, and marked as preprints.

## What we did

Four searches ran in parallel, one per theme: the fine-tuning technique; small
models and distillation; training data and synthetic data; classification,
abstention, evaluation and the legal domain. Each returned up to fifteen or so
verified papers, ranked, plus a list of what it checked and left out. The results
were merged into one document with a ten-paper "start here" list and a
recommendation of eight to add to the roster.

## Terms that came up

- **arXiv identifier.** A number like 2305.14314: year, month, and a serial. It
  is the stable way to cite a paper; titles change, identifiers do not.
- **Preprint.** A paper on arXiv that has not been accepted at a peer-reviewed
  venue. It may still be excellent, or widely used; it has not been checked by
  reviewers.
- **Venue.** The conference or journal that accepted the paper. NeurIPS, ICML,
  ICLR, ACL and EMNLP are the strong ones in this field.
- **Relevance.** High means it changes a decision in this project; medium, it
  informs one; low, background.

## The decision that is yours

Which of the recommended eight to score and add to the roster. Options: all
eight (recommended; each changes a decision ahead); only the five that enter at
requirements, leaving the three tech-spec ones for later; or a different pick
from the sixty-one listed.

## What you just learned

- A reference is only a reference once it has been checked at the source.
- The two findings that most change this project: small open models, lightly
  fine-tuned, beat GPT-4 on legal classification with few examples per task; and
  teaching a model facts it does not already know makes it hallucinate more.
- A benchmark of AI Act risk-tier scenarios already exists, and its baseline was
  weakest on the minimal tier. That is where our cases should be hardest.

## Check questions

1. Why is "verified on arXiv" a different claim from "peer-reviewed"?
2. Lawma found that tens to a few hundred examples per task were enough. What
   does that suggest about a 2,000-case set spread over five tiers and the Annex
   III categories?
3. If the judge that filters our teacher-written cases is from the same model
   family as the teacher, what goes wrong, and what is the fix?
