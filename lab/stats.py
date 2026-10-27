"""Statistics for small samples (specs/data-and-evaluation.md, ADR-004).

Standard library only. An undefined value is None, shown as "not defined".
"""

from __future__ import annotations

import math
import random
import statistics
from collections import Counter
from collections.abc import Callable, Sequence

Z_95 = 1.96
RESAMPLES = 10_000
SEED = 20261026
WILSON_METHOD = "Wilson score interval, 95%"
BOOTSTRAP_METHOD = (
    "paired bootstrap, 10,000 resamples of cases, 2.5th to 97.5th percentile"
)


def wilson(k: int, n: int) -> tuple[float, float] | None:
    """95% Wilson score interval for k successes out of n; None when n is 0."""
    if n < 0 or not 0 <= k <= max(n, 0):
        raise ValueError(f"impossible counts: {k} of {n}")
    if n == 0:
        return None
    p = k / n
    z2 = Z_95 * Z_95
    centre = p + z2 / (2 * n)
    half = Z_95 * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))
    denominator = 1 + z2 / n
    return max(0.0, (centre - half) / denominator), min(1.0, (centre + half) / denominator)


def _percentile_interval(values: list[float]) -> tuple[float, float]:
    cuts = statistics.quantiles(values, n=40, method="inclusive")
    return cuts[0], cuts[-1]


def _bootstrap(
    n: int, statistic: Callable[[list[int]], float | None], seed: int
) -> tuple[list[float], int]:
    """Resample n case indices with replacement; return defined values and skips."""
    rng = random.Random(seed)
    values, skipped = [], 0
    for _ in range(RESAMPLES):
        value = statistic([rng.randrange(n) for _ in range(n)])
        if value is None:
            skipped += 1
        else:
            values.append(value)
    return values, skipped


def paired_bootstrap_diff(
    a_correct: Sequence[bool], b_correct: Sequence[bool], seed: int = SEED
) -> tuple[float, float, float]:
    """Difference in accuracy (A minus B) and its 95% paired bootstrap interval.

    Both models' answers on a case stay together in every resample.
    """
    n = len(a_correct)
    if n == 0 or n != len(b_correct):
        raise ValueError("paired lists must be non-empty and the same length")
    diffs = [int(a) - int(b) for a, b in zip(a_correct, b_correct, strict=True)]
    values, _ = _bootstrap(n, lambda idx: sum(diffs[i] for i in idx) / n, seed)
    low, high = _percentile_interval(values)
    return sum(diffs) / n, low, high


def cohen_kappa(a: Sequence[str], b: Sequence[str]) -> float | None:
    """Cohen's kappa between two raters; None when undefined (no cases, or pe = 1)."""
    n = len(a)
    if n != len(b):
        raise ValueError("raters must label the same cases")
    if n == 0:
        return None
    observed = sum(x == y for x, y in zip(a, b, strict=True)) / n
    count_a, count_b = Counter(a), Counter(b)
    expected = sum(count_a[c] * count_b[c] for c in count_a) / (n * n)
    if expected == 1:
        return None
    return (observed - expected) / (1 - expected)


def kappa_bootstrap(
    a: Sequence[str], b: Sequence[str], seed: int = SEED
) -> tuple[float, float, int] | None:
    """95% bootstrap interval for kappa and the number of skipped resamples.

    Resamples where kappa is undefined are skipped and counted; None if all are.
    """
    if len(a) != len(b) or not a:
        raise ValueError("raters must label the same, non-empty set of cases")
    values, skipped = _bootstrap(
        len(a), lambda idx: cohen_kappa([a[i] for i in idx], [b[i] for i in idx]), seed
    )
    if not values:
        return None
    low, high = _percentile_interval(values) if len(values) > 1 else (values[0], values[0])
    return low, high, skipped
