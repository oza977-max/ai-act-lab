# How this was built: the method, in plain English

This project is built with the **Grounded Vibe Methodology (GVM)**: a way of
working with an AI coding assistant (here, Claude Code) so that what gets built
is backed by evidence, not by how confident the assistant sounds. This page
explains the method for someone who has never seen it, using this repo as the
worked example. Every file it mentions is in the repo, so you can check each claim.

## The one idea behind it

An AI assistant writes plausible code and plausible prose very fast. Plausible is
not the same as right. GVM puts a check of some kind between every step and the
next: a written decision, a test that fails first, an independent reviewer, or a
person signing off. "Grounded" means each decision names its source: a paper, a
book, the law's own text, or a measurement.

## The phases, and what each is for

Each phase produces one file you can read, and the owner reviews it before the
next phase starts.

| Phase | The question it answers | This repo's file | Plain-English lesson |
|---|---|---|---|
| Expert calibration | Whose published advice should guide this work? | `init/init-001.md` | [001](learning/001-expert-calibration.md) |
| Impact map | Why build this, for whom, and what would change? | `impact-map.md` | [004](learning/004-impact-map.md) |
| Requirements | What exactly must it do, in testable sentences? | `requirements/requirements.md` | [005](learning/005-requirements.md) |
| Test cases | How will we know each requirement is met, decided before any code? | `test-cases/test-cases.md` | [006](learning/006-test-cases.md) |
| Technical spec | How will it be built, in what order of small chunks? | `specs/` | [007](learning/007-tech-spec.md) |
| Design review | Before building, could independent readers break the design? | `design-review/design-review-001.html` | [008](learning/008-design-review.md) |
| Build | Code, one small chunk at a time | `build/` | [009](learning/009-first-build-chunk.md) onward |

## How one build chunk is made

The build guide (`specs/implementation-guide.md`) splits the work into small
chunks, each finishable in one sitting. Every chunk goes through the same steps:

1. **Prompt file** (`build/prompts/`). The chunk's task is written down first:
   what to build, which requirements and tests it covers, and which experts'
   advice the review will check it against.
2. **Acceptance test, red.** A test that describes what the user will see is
   written and committed *before* the code. It fails ("red"), proving the test
   can fail.
3. **Code, green.** The code is written until that test and the smaller tests
   pass ("green"), and the passing state is committed. Both commits are recorded.
4. **Self-review**, then an **independent review loop**. A separate AI reviewer,
   which did not write the code, reads it and reports findings. Serious ones are
   fixed and the reviewer looks again. The loop stops only when a pass finds
   nothing serious. The handover records each pass, for example
   `[(1, 4), (2, 2), (3, 0)]`: 4 serious findings, then 2, then none.
5. **Smoke run.** The chunk's real command is run end to end, and its output is
   checked for structure.
6. **Handover** (`build/handovers/`). What was built, the test results, every
   review finding and how it was handled, any departure from the spec and why,
   and notes for later chunks. A new session can pick up from this file alone.

The build log in the README's "Progress at a glance" block is counted from these
handovers by `scripts/repo_stats.py`, so the numbers there cannot drift from the
records.

## Why bother: what the checks actually caught here

From the handovers and the README's "what went wrong" list:

- The independent reviewer found that the table of valid AI Act articles gave
  Article 3 no entries. Every correct citation of a definition would have been
  scored as invented law. (P1-C04)
- About 60 unusual inputs from the reviewer showed that the date detector missed
  "2 august 2026" and that the one-sentence check rejected "Ltd.". (P1-C03)
- The design review found that "fits in 8 GB" had no actual limit written down,
  before any code depended on it.

None of these would have failed an ordinary test written by the same author,
because the author's blind spots are in the tests too. That is the case for
independent review.

## The other half: learning as a deliverable

The owner is fine-tuning a model for the first time, so every step also produces
a lesson in `docs/learning/`: a short lesson before the step, what happened, the
new terms, and check questions. The owner makes the decisions that carry the
learning (the label scheme, judging the gold cases, choosing the base model,
training settings), and Claude handles the mechanics. Training runs are recorded
separately in `notebook/`.

## If you want to work this way

You need three habits more than any tool:

1. Write down what "done" means before building.
2. Never let the author of something be its only reviewer.
3. Report what was measured, including the failures, with its margin of error.
