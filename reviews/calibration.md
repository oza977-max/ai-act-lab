# Review Calibration

Carried between review rounds so later reviews can tighten their criteria and spot recurring problems.

## Score History

| Round | Date | Type | Coverage | Contracts | Structure | Implementability | Security | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-26 | design | 7 → 9 | 5 → 9 | 7 → 9 | 5 → 8 | 6 → 8 | Before → after fixes; quick scan; liberal criterion |

## Round 1 metrics

- Raw findings 59; consolidated themes 14 (Critical 2, Important 9, Minor 3).
- Capture-recapture estimate about 15 themes; coverage about 93%. Round 2 optional.
- Borderline filter: kept 6 of 6.
- Quote spot-check: 6 of 6 verbatim.

## Dimension benchmarks

| Dimension | Baseline | Current | Trend |
|---|---|---|---|
| Interface contracts | 5 | 9 | first round |
| Implementability | 5 | 8 | first round |

## Anchor examples

- **Contracts, worst:** a review sheet with no columns for two required record fields (B-1); **best:** the single answer record defined once and imported everywhere.
- **Implementability, worst:** "memory exceeds the limit" with no limit or mechanism (D-1); **best:** the 10-case fixture with hand counts.

## Recurring findings

None yet (first round).

## Resolved findings

All 14 round-1 themes resolved on 2026-10-26 (see `design-review/design-review-001.html`).
