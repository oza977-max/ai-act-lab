# 008. The design review: five narrow readers before building

**Step:** `/gvm-design-review`, slice 1. **Date:** 2026-10-26.
**Output:** `design-review/design-review-001.html`, revised specs, `reviews/calibration.md`, an upgraded confidentiality guard.

## The lesson before the step

**What we did.** Five independent reviewers each read every spec looking for one
kind of defect only: missing requirements, mismatched contracts, incoherent
structure, places a builder would have to guess, and security gaps.

**Why narrow.** A reviewer who finds one problem in a section tends to stop
looking there. One defect class per reviewer finds more distinct problems.

**What usually goes wrong.** Rubber-stamping, or burying real issues in style
comments. Every finding had to quote the exact spec line; a sample of six quotes
was checked and all were verbatim.

## What happened

- 59 raw findings, consolidated into 14 themes. No requirement was missing; the
  design was vague in ways that would have forced the builder to guess.
- **Two would have broken the build:** "fits in 8 GB" had no limit and no way to
  survive running out of memory; your review spreadsheet had no columns for two
  required answer fields, so 15 of 100 cases could never pass the checker.
- **The first build chunk never touched a real model**, so the riskiest seam
  would have been tested last. It now comes second.
- **The confidentiality guard was a word list run by hand.** It now runs
  automatically before every commit and blocks any name on your private list.
- You chose: fix everything now; thinking modes off for all models; a private
  name list. Verdict after fixes: **build from this**.

## Terms that came up

- **Defect class.** One kind of mistake, such as a contract mismatch.
- **Capture-recapture.** Estimating how many defects exist from how often
  independent reviewers find the same ones. Here: about 15, we found 14.
- **Tracer bullet.** The first thin thing that runs end to end through the
  riskiest part. Ours now loads a real model in the first phase.
- **Child process.** A separate program the main one starts, so if it crashes
  from running out of memory, the main one survives to record why.
- **Pre-commit hook.** A script git runs before every commit; if it fails, the
  commit does not happen.

## Your one task from this step

Open `.private/deny-terms.txt` in this repository folder and add, one per line,
any real names that must never appear: the organisation you work for, its clients, teams and
products. The file never leaves this Mac and is never committed.

## What you just learned

- Specs that read well can still be unbuildable; independent narrow reviews find that.
- The order of building matters as much as what is built: test the riskiest seam first.
- A safety check you have to remember to run is not a safety check.

## Check questions

1. Why can't a process that runs out of memory write down that it ran out of memory?
2. Two reviewers independently flagged the same memory problem. What does that tell you?
3. Why is a private, never-committed list stronger than any word pattern for confidentiality?
