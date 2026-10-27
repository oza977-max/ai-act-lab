# 015. The labelling guideline (P2-C01)

**Step:** build chunk P2-C01, guideline v1. **Date:** 2026-10-27.

## The lesson before the step

Words first:

- **Label.** The correct answer attached to a case, such as "high-risk, Annex III
  area 4".
- **Gold case.** A case whose label you have checked by hand. The 100 gold cases
  are the real exam.
- **Labelling guideline.** The rulebook you follow when you label, so that case 12
  on Monday and a similar case on Thursday get the same answer.
- **Boundary case.** A case right on the line between two labels. Most of the
  guideline's work is deciding these.
- **Default rule.** What to do when the description does not say something.

**Why it matters:** a model cannot be more consistent than its marking key. Later,
a second reading of a sample of your cases measures agreement (kappa). Low
agreement points at a vague guideline, not at the model.

**What usually goes wrong:** vague rules ("use judgement"), and using "needs human
review" to avoid hard but decidable cases, which makes accuracy look better than
it is.

## Your four decisions

1. **D-LS-1, missing facts: assume the ordinary case.** Assume use in the EU and
   that the system works as described. Send a case to review only when the
   missing fact would change the tier.
2. **D-LS-2, Article 6(3): the exception must be stated clearly.** A system in an
   Annex III area stays high-risk unless the description plainly names a narrow
   or preparatory task and nothing suggests it assesses, ranks, scores or filters
   people.
3. **D-LS-3, silence passes.** A plainly narrow task, such as transcribing
   interviews, qualifies even if the description never says "it does not score
   anyone", as long as nothing suggests it does.
4. **D-LS-4, the fraud score stays with review.** Whether the fraud-detection
   exclusion in Annex III 5(b) is judged by purpose or by effect is open, so a
   fraud score that alone decides who gets a loan is labelled "needs human
   review" until guidance settles it.

## What we did

1. Wrote the test first: six labels, each resting on an article; a decision order
   that starts with scope; two worked examples per label, one a boundary case;
   every example a valid record citing real provisions; a source line on every
   rule.
2. Drafted `docs/guideline/labelling-guideline.md`: the six labels, the five-step
   decision order, Article 50 in short, your two decisions, the narrow review
   rule, the answer record, 18 worked examples and the change log.
3. Sent it to independent reviewers, round after round, until a round found
   nothing serious. It took seven rounds; the serious findings per round were
   10, 8, 3, 4, 3, 1 and 0. Two of the round-4 findings were judgement calls, so
   they came to you (decisions 3 and 4).

## What went wrong and how it was caught

- **The first draft missed parts of the 2026 amendment.** The reviewer noticed
  that our article table listed new paragraphs that the guideline never
  mentioned. Re-reading the official text showed two new bans (AI that generates
  non-consensual intimate images, and child sexual abuse material) and a narrower
  meaning of "safety component". Both are now in the rules.
- **Our own examples broke our own rules.** One example sent a case to review that
  your Article 6(3) decision already decided. Another summarised CVs and should,
  by our own text-generation rule, have set the Article 50 flag. The fix was to
  make each rule precise enough to test, then add tests that every example obeys
  it.
- **Twice, "unsettled law" was not really unsettled.** A reviewer showed that the
  first two candidate examples could be decided from the text. "Needs human
  review" has to be earned. The final example is a fraud score that alone decides
  who gets a loan, which sits between "credit scoring" (high-risk) and "fraud
  detection" (excluded).
- **One reviewer claim was wrong.** It said "Annex I 4" could mean two different
  things. Annex I is numbered straight through both sections, so it cannot.
  Reviewers are checked too.

## Terms that came up

- **Decision order.** The fixed sequence of questions; stop at the first that
  decides.
- **Article 50 flag.** A separate yes/no for transparency duties, independent of
  the tier.
- **Safety component.** A part whose failure would endanger health and safety;
  since 2026, not a part used only for convenience or efficiency.
- **Profiling.** Automated evaluation of a person's work, finances, health,
  behaviour and so on (the GDPR definition, which the Act points to).
- **Convention.** A rule this guideline sets where the law leaves a choice, stated
  openly so that everyone applies it the same way.

## What you just learned

1. A labelling rulebook is code for people: each rule must be precise enough that
   two careful readers reach the same answer.
2. Examples teach more than rules. A wrong example teaches the wrong habit, so
   every example is tested against the rules.
3. "Needs human review" is a real answer, but only for missing facts, conflicting
   facts or genuinely unsettled law.

## Check questions

1. A chatbot helps employees book holidays and decides nothing about them. Which
   label, and what is the Article 50 flag?
2. A recruitment tool "summarises each CV in five bullets". Under your Article 6(3)
   decision, high-risk or minimal? Why?
3. Why is a case that is hard, but decidable from the text, not "needs human
   review"?
