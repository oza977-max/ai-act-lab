# 009. The first build chunk: red, green, and an honest reviewer

**Step:** `/gvm-build` P1-C01. **Date:** 2026-10-26.
**Output:** `lab/records.py`, `lab/evaluate.py`, 38 tests, a hardened confidentiality guard.

## The lesson before the step

**Red, then green.** Write the test first and watch it fail; then write just
enough code to make it pass; then tidy. A test you have never seen fail might be
testing nothing.

## What happened

1. **Red** (commit e1d03b5): the tests existed, the code did not; the acceptance
   test failed with "No module named lab.evaluate".
2. **Green** (commit d147710): the evaluation printed exactly the hand counts:
   7 of 10 right, 8 of 10 answered, 6 of 8 right when answered.
3. **Independent review, three passes:** 4 serious findings, then 2, then 0.
   - The reviewer found two real ways to slip a private name past the guard:
     a file name with a space, and a line starting with "++". Both fixed.
   - It found that a blank line in your private list would have blocked every
     commit, and a list saved with Windows line endings would have blocked
     nothing. Both fixed.
   - Its final point was wrong, and I proved it by putting the old bug back:
     the test failed, as it should.

## Terms that came up

- **Acceptance test.** A test of what the user sees: here, the command's output.
- **Unit test.** A test of one small piece, such as the answer parser.
- **Fixture.** Fixed test data with known answers: our 10 hand-counted cases.
- **Mutation check.** Deliberately breaking the code to prove a test notices.
- **Convergence.** Reviewing again and again until a pass finds nothing serious.

## What you just learned

- A first review pass with findings is normal; stopping there is the mistake.
- Reviewers can be wrong too; check their claim with an experiment.
- The tool now behaves on bad input: a missing answer, an unreadable one, a
  corrupt file, all stop or count clearly instead of crashing or flattering.

## Try it yourself (optional, 1 minute)

From the project folder in a terminal:

```bash
.venv/bin/python -m pytest
```

You should see "38 passed".

## Check questions

1. Why commit the red state before writing the code?
2. A model's answer is missing for one case. Why must it still count in the
   denominator?
3. How did we decide the reviewer's last finding was wrong, and why is that
   better than arguing?
