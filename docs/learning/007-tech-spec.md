# 007. The technical specification: from what to how

**Step:** `/gvm-tech-spec`, slice 1. **Date:** 2026-10-26.
**Output:** `specs/cross-cutting.md`, `specs/data-and-evaluation.md`, `specs/architecture-overview.md`, `specs/implementation-guide.md`, each with an HTML version.

## The lesson before the step

**What we did.** Decided *how*: tools, folders, file formats, one shared answer
record, what each piece of code does, the statistics, and the order to build in.

**Why.** Without shared contracts, pieces built one at a time do not fit. The
answer record is the example: the bake-off writes it, the evaluation reads it,
and if they disagree every number is wrong.

**What usually goes wrong.** Over-engineering; modules nobody calls; building
all the plumbing before anything runs.

## What you decided

- **Four short documents**, not the usual six to eight.
- **You judge the gold cases in a spreadsheet**, five batches of 20, with a
  checker that catches typos and missing decisions.
- **You run all four bake-off commands yourself**, one per model.

## What I decided, and why

- **Plain Python scripts and files, two dependencies** (`mlx-lm`, `pytest`).
- **Wilson intervals** for single proportions: they stay between 0 and 1 and
  behave on small samples. **A paired bootstrap** for model-versus-model
  differences: resample cases 10,000 times, keeping both models' answers on the
  same case together, with a fixed seed so it repeats exactly.
- **A model's answer is either a valid record or a format failure.** No guessing
  a tier from prose; that would flatter weak models.
- **One prompt for all four models**, telling them that instructions inside a
  case description are part of the case, not commands.

## Terms that came up

- **ADR (architecture decision record).** A short note: the context, the options,
  the choice, the consequences. So the next person knows why.
- **Contract.** A shape two pieces of code agree on, written down once.
- **Walking skeleton.** The thinnest thing that runs end to end. Ours: the
  evaluation on the 10-case set.
- **Wiring matrix.** A table proving every module is actually used by a command.
- **Spike.** A short, time-boxed investigation whose output is knowledge, not
  code: here, which model builds load on this Mac.
- **Critical path.** The longest chain of steps that must happen in order. Ours
  runs through your 100-case review.

## What you just learned

- "How" comes after "what" and "done", not before.
- Every number in this project will be repeatable exactly: fixed seeds, greedy
  generation, versions in every report.
- Your own review time, not the computer, is the critical path.

## Check questions

1. Why should a model that answers in prose score as a format failure rather
   than have its tier guessed?
2. Why does the bootstrap keep both models' answers on the same case together?
3. Why is the evaluation built first, before there is any real data to evaluate?
