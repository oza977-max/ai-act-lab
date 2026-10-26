# 001. Choosing the reference shelf: expert calibration

**Step:** `/gvm-init`, the first phase of the GVM pipeline. **Date:** 2026-10-26.
**Output:** `init/init-001.md` (the report) and `scoring-reports/expert-scoring-001.md` (the evidence).

## The lesson before the step

**What we are doing.** Before anyone writes a requirement or a line of code, the
methodology picks the published authorities that every later decision must cite: a
regulation, an official guideline, a peer-reviewed paper, a well-regarded book. The
list is called the expert roster. It is the reference shelf for the whole project.

**Why.** Left to itself, an AI assistant makes design choices from instinct and
states them with full confidence. Requiring a named source for each choice does
two things. It makes the choice checkable: you can open the source and see whether
it says what was claimed. And it forces honesty where no source exists: a gap in
the shelf is reported as a gap, not papered over.

**What usually goes wrong.**

- The shelf gets padded with famous names that never get used. The cure is a log
  of which experts are actually loaded and cited, so the roster can be pruned later.
- Scores get invented. "Canonical" is a claim about the world and needs evidence.
  The cure is two independent scorings, reconciled, with evidence for every high
  mark.
- The wrong shelf gets loaded. A banking model-risk file would drag in obligations
  this project does not have. The cure is to activate only the files that match the
  work, and to say which were considered and left out.
- Nobody checks for who is missing. Scoring only tests the names someone thought
  of. The cure is a blind recall check: ask, without showing the list, who the most
  cited authorities are, and compare.

## What we did

1. Loaded the methodology's standard shelf of process experts (how to specify, build
   and test software) and confirmed it unchanged. Seventeen names.
2. Found two files in the shared library that fit: one on AI governance, which
   holds the EU AI Act itself, and one on evaluating AI models honestly. Loaded both.
   Considered and left out four others.
3. Compared the shelf with what this project has to do and found eight gaps, from
   "how to interpret the Act's classification rules" to "how to measure a model
   that says *needs human review*".
4. Proposed ten authorities to fill them, scored each twice independently, and
   reconciled. Every score landed within one point between the two passes; four
   entries sit on a band boundary and are flagged.
5. Ran the blind recall check. The core names were already on the shelf. Twelve
   further authorities are recommended for later phases, when they become relevant.
6. Wrote the report, the scoring evidence, and this entry. Nothing has been written
   into the shared library yet; that waits for your approval.

## Terms that came up

- **Expert roster.** The list of authorities the project may cite.
- **Tier.** Where an authority sits: Tier 1 is process (always on), Tier 2b is the
  industry or field, Tier 2a is software patterns, Tier 3 is specific tools. Only
  Tiers 1 and 2b are chosen now; the rest wait until the stack is known.
- **Classification.** A band from the average of five scores: Canonical (4.5 and
  up), Established (3.5 to 4.4), Recognised (2.5 to 3.4), Emerging, Provisional.
  Established is a good score. Canonical means "the field's defining source".
- **Two-pass scoring.** One assessment by the session, one by a fresh agent that saw
  only names and titles. Agreement shows the scores are stable, not that they are
  right. Your approval is the correctness check.
- **Boundary case.** The two passes put an entry in different bands. The lower
  score is kept and the entry is flagged for you.
- **Recall check.** The reverse question: who did we forget?
- **Activation log.** A file outside the repository that records every time an
  expert is loaded or cited, so unused ones can be pruned.

## The decision that is yours

**Approve, amend or trim the ten proposed experts.** Three ways to go:

- **Approve all ten** (recommended). Each fills a gap the first slice needs: the
  Commission guidelines and the annotation method feed the label scheme and gold
  set; the fine-tuning papers and practitioner guides feed the later training
  slice; the selective-classification paper is what makes "needs human review"
  measurable. They are references, not commitments; nothing is installed or run.
- **Approve the regulation and annotation ones now, defer the fine-tuning ones.**
  Fewer names to hold in mind this week. The cost is that the tech-spec phase
  would have to rediscover and rescore them in a few weeks.
- **Amend.** Name an authority you trust that is not on the list, or strike one. It
  is scored the same way and added or removed before the next phase.

Also confirm, or correct, the one-paragraph statement of the project's domain at
the top of the report.

## What you just learned

- A project under this method starts by choosing and scoring its sources, and the
  scoring is itself checked two ways: a second independent pass, and a blind
  search for who was left out.
- "Needs human review" is not a soft option. There is a published framework,
  selective classification, in which it is a designed output with its own two
  numbers: how often the model answers, and how often it is right when it does.
- The official guidance for classifying high-risk systems under Article 6 is still
  a draft. The label scheme will say so, and the lookup table will carry a
  "last checked" date for every fact.

## Check questions

1. Why is it not enough that two scoring passes agreed with each other?
2. If a model marks every case as "needs human review", what happens to its
   accuracy on answered cases, and why is that a problem?
3. Which of the ten proposed authorities would you open first when writing the
   labelling guideline, and why?

## Next step

`/gvm-impact-map`. Before running it you will get the same shape of lesson: what an
impact map is (a four-column trace from a goal, through the people whose behaviour
must change, to the things we build), why it comes before requirements (so that
every requirement can be traced back to a goal, which is how scope creep is caught
early), and what usually goes wrong (goals stated as deliverables instead of
outcomes).
