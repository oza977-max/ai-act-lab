# AI Act Lab — Requirements Health Report (Slice 1)

**Date:** 2026-10-26
**Scope:** `requirements/requirements.md`, 44 requirements (43 in scope, WN-1 Won't)

*Before writing tests, every requirement is checked for four defects: untestable wording, contradictions, design decisions in disguise, and gaps. Four issues were found; none blocks test writing.*

## Summary

| Check | Result |
|---|---|
| Untestable requirements | 1 (H-3) |
| Inconsistencies | 1 (H-2) |
| Weak requirements (design in disguise, duplicates) | 0 |
| Missing coverage | 2 (H-1, H-4) |
| Gold-set arithmetic (GS-1 totals 100) | passes |
| Every in-scope requirement traces to a deliverable | passes |

## Issues

### H-1. Missing outputs are not covered (EV-5, gap)

EV-5 says unreadable outputs count as wrong. It does not say what happens when a gold case has no output at all, for example when a model crashes partway through the bake-off. Recommendation: treat a missing output exactly like an unreadable one, counted as wrong and reported separately, and add one sentence to EV-5.

### H-2. Dates for labels that have no dates (DT-1, inconsistency)

DT-1 asks for dates and duties for every tier label, but out-of-scope and needs-human-review have none, and minimal has only general duties such as AI literacy. Recommendation: for those labels the table returns an explicit entry saying so (for example, "no AI Act tier duties; refer to a person"), never an empty result.

### H-3. "A method suited to small samples" (EV-6, untestable as worded)

A tester cannot check "suited". Recommendation: keep the requirement implementation-agnostic but testable by requiring the report to name the method, and leave the choice of method to the technical specification.

### H-4. Excluded candidates in the paired comparison (BO-4 with EV-7, gap)

If a candidate is excluded under BO-4, there is no output file to pair. Recommendation: the evaluation refuses a paired comparison when either side is missing cases, and says which.

---

*Developed using the Grounded Vibe Methodology*
