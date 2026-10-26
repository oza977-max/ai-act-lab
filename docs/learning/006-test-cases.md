# 006. Test cases: deciding "done" before building

**Step:** `/gvm-test-cases`, slice 1. **Date:** 2026-10-26.
**Output:** `test-cases/test-cases.md` and `.html`, `test-cases/requirements-health-report.md`.

## The lesson before the step

**What we did.** Turned each requirement's check line into a concrete test:
an input, a starting situation, one action, what the result must contain and
what it must not contain. 63 tests for 43 requirements, written before any code.

**Why before building.** A test written after the code tends to check what the
code happens to do; a test written first checks what you asked for (Kent Beck).

**What usually goes wrong.** Abstract tests that always pass; only testing the
happy path; tests nobody can trace to a reason.

## What happened

- **The health check caught four gaps in our own requirements** and you fixed
  them: a crashed model could have shrunk the denominator and inflated
  accuracy; the dates table could have returned nothing for labels with no
  duties; "a method suited to small samples" was untestable; a paired
  comparison with a missing model had nothing to pair.
- **The evaluation is tested on a set you can count by hand.** Ten cases: six
  right, two wrong, two "needs human review" (one correctly). By hand: 7 of 10
  right; 8 of 10 answered; 6 of 8 right when answered. The script must produce
  exactly those numbers.
- **Every boundary is tested on both sides:** 40 and 41 words, 59 and 60, 200
  and 201, 90 and 91 days, kappa 0.79 and 0.80.
- **A pre-commit guard now actually blocks** a commit that contains anything
  that looks confidential. It was tested on a planted line and stopped it.

## Terms that came up

- **Given / When / Then.** The starting situation, the one action, the expected result.
- **Boundary value.** The value right at a limit, and the one just past it. Bugs live there.
- **Fixture.** A small, fixed set of inputs with known answers, used to test a tool.
- **Property test.** A rule that must always hold, for example "the same input
  always gives the same answer", rather than one example.
- **Traceability matrix.** The table linking every requirement to its tests.

## What you just learned

- "Done" is decided before building, as tests with concrete numbers.
- The evaluation script is the riskiest piece, because a silent bug there fakes
  every result; that is why its tests use numbers you can check by hand.
- Writing tests found real holes in requirements we had just approved.

## Check questions

1. In the 10-case set, why is accuracy on answered cases 6 of 8 and not 7 of 10?
2. Why test 90 and 91 days, rather than, say, 30 and 200?
3. If a model crashes on case 57, what must the evaluation report, and why?
