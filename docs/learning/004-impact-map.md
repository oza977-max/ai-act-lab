# 004. The impact map: why, who, how, what

**Step:** `/gvm-impact-map`, the second phase of the GVM pipeline. **Date:** 2026-10-26.
**Output:** `impact-map.md` and `impact-map.html`.

## The lesson before the step

**What we did.** Drew four linked tables: a goal you can measure; the people
whose behaviour must change for it; how it changes; and what we build to cause
that change. The idea is Gojko Adzic's *Impact Mapping*. Marty Cagan's *Inspired*
supplies the rule behind the first table: a goal is an outcome, not a feature.

**Why before requirements.** It is the cheapest place to stop scope creep. In the
next phase, every requirement must point at one deliverable on the map, and the
method refuses any that cannot.

**What usually goes wrong.** Goals written as things to build ("launch", "build",
"deliver"); too many people on the map; deliverables that serve no impact; and,
here, forgetting that this project has two goals, the model and your learning.

## What we decided

- **Two goals, both measured.** G-1: the triage answer is trustworthy on clean
  descriptions and honest about the rest: at least 90% right on answered
  cases, at least 75% answered, and a gain over the untuned model larger than
  its margin of error. G-2: you run, read and explain a fine-tuning cycle
  unaided: at least three cycles run and written up by you.
- **Deadline 16 November 2026.** Three weeks. The computer's part is small; the
  pace is set by your time on labelling, reviews and your own training runs,
  roughly 15 to 20 hours in total.
- **Three people.** You as labeller and reviewer; a future user of the public
  repository; you as learner. You handle every "needs human review" case for now.
- **Eighteen deliverables**, none new to the plan, each now linked to a reason.

## Terms that came up

- **Outcome versus output.** An outcome is a change in the world you can
  measure; an output is a thing you make. Goals are outcomes.
- **Actor.** A person whose behaviour must change for the goal to be met.
- **Impact.** That change in behaviour, with a direction: more of something (+)
  or less of something (−).
- **Deliverable.** What we build to cause an impact.
- **Answered-case accuracy and coverage.** The two numbers for "needs human
  review": how often the model is right when it answers, and how often it
  answers at all. Each is meaningless without the other.
- **Traceability.** Every requirement points at a deliverable, every deliverable
  at an impact, every impact at a person, every person at a goal.

## What you just learned

- A goal is only a goal if a number can say whether it was met.
- The map is short on purpose: three people, eight impacts. Detail belongs in
  requirements.
- Your learning is on the map as a goal in its own right, so the requirements
  must serve it, not just the model.

## Check questions

1. Why does G-1 need both numbers, accuracy on answered cases and the share
   answered? What could a model do to pass on one alone?
2. "Build the local triage page" is a deliverable. What is the impact it serves,
   and which person makes that impact?
3. If a requirement next week cannot be traced to any of D-1 to D-18, what are
   the two honest responses?
