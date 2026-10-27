"""Known-answer tests for the statistics (ADR-004)."""

import pytest

from lab.stats import (
    cohen_kappa,
    kappa_bootstrap,
    paired_bootstrap_diff,
    wilson,
)


def test_wilson_known_answer_7_of_10():
    low, high = wilson(7, 10)
    assert low == pytest.approx(0.3968, abs=1e-4)
    assert high == pytest.approx(0.8922, abs=1e-4)


def test_wilson_known_answer_6_of_8():
    low, high = wilson(6, 8)
    assert (round(low, 4), round(high, 4)) == (0.4093, 0.9285)


def test_wilson_edges_stay_within_zero_and_one():
    assert wilson(0, 10) == (0.0, pytest.approx(0.2775, abs=1e-4))
    assert wilson(10, 10) == (pytest.approx(0.7225, abs=1e-4), 1.0)


def test_wilson_with_no_cases_is_not_defined():
    assert wilson(0, 0) is None


@pytest.mark.parametrize("k, n", [(-1, 10), (11, 10), (1, -1)])
def test_wilson_rejects_impossible_counts(k, n):
    with pytest.raises(ValueError):
        wilson(k, n)


def test_tc_ev_7_01_identical_answers_give_zero_difference():
    a = [True, False, True, True, False, True, True, False, True, True]
    diff, low, high = paired_bootstrap_diff(a, list(a), seed=20261026)
    assert (diff, low, high) == (0.0, 0.0, 0.0)


def test_paired_bootstrap_is_repeatable_and_brackets_the_difference():
    a = [True] * 8 + [False] * 2
    b = [True] * 5 + [False] * 5
    first = paired_bootstrap_diff(a, b, seed=20261026)
    assert first == paired_bootstrap_diff(a, b, seed=20261026)
    diff, low, high = first
    assert diff == pytest.approx(0.3)
    assert low <= diff <= high
    assert 0.0 <= low and high <= 0.6


def test_paired_bootstrap_known_answer_one_model_always_better():
    # B is right only where A is: every resample gives a difference >= 0.
    a = [True] * 10
    b = [True] * 5 + [False] * 5
    diff, low, high = paired_bootstrap_diff(a, b, seed=20261026)
    assert diff == 0.5 and low > 0


def test_paired_bootstrap_needs_equal_non_empty_lists():
    with pytest.raises(ValueError):
        paired_bootstrap_diff([True], [True, False], seed=1)
    with pytest.raises(ValueError):
        paired_bootstrap_diff([], [], seed=1)


def test_cohen_kappa_known_answer():
    # Classic 2x2: po = 0.7, pe = 0.5, kappa = 0.4.
    a = ["y"] * 5 + ["n"] * 5
    b = ["y"] * 4 + ["n"] + ["y"] * 2 + ["n"] * 3
    assert cohen_kappa(a, b) == pytest.approx(0.4)


def test_cohen_kappa_perfect_and_undefined():
    assert cohen_kappa(["a", "b"], ["a", "b"]) == 1.0
    # Both raters always say the same single label: expected agreement 1.
    assert cohen_kappa(["a", "a"], ["a", "a"]) is None
    assert cohen_kappa([], []) is None


def test_kappa_bootstrap_counts_skipped_resamples():
    a = ["a", "a", "a", "b"]
    b = ["a", "a", "a", "b"]
    low, high, skipped = kappa_bootstrap(a, b, seed=20261026)
    assert low == high == 1.0
    assert skipped > 0  # resamples that drew only "a" cases
