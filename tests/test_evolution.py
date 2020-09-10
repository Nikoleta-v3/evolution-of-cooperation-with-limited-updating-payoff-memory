from importlib.machinery import SourceFileLoader

import numpy as np
import sympy as sym

evolution = SourceFileLoader("evolution", "src/evolution.py").load_module()


def test_imitation_probability():
    assert np.isclose(float(evolution.imitation_probability(0, 5, 1)), 0.993307)


def test_fixation_ratio_for_ALLD_invading_GTFT():
    R, S, T, P = sym.symbols("R, S, T, P")
    q, d, N, b = sym.symbols("q, delta, N, beta")

    ALLD = (0, 0, 0)
    GTFT = (1, 1, q)

    expr = evolution.probability_mutant_increases(
        GTFT, ALLD, N, k=1, delta=d, beta=b, payoffs=[R, S, T, P]
    ) / evolution.probability_mutant_descreases(
        GTFT, ALLD, N, k=1, delta=d, beta=b, payoffs=[R, S, T, P]
    )

    numerator_first_term = (1 - d + d * q) / (1 + sym.exp(-b * (T - R))) + (
        (d * (1 - q)) / (1 + sym.exp(-b * (P - R)))
    )
    numerator_second_term = (1 - d + d * q) / (1 + sym.exp(-b * (T - S))) + (
        (d * (1 - q)) / 2
    )
    denominator_first_term = (1 - d + d * q) / (1 + sym.exp(-b * (R - T))) + (
        (d * (1 - q)) / (1 + sym.exp(-b * (R - P)))
    )
    denominator_second_term = (1 - d + d * q) / (1 + sym.exp(-b * (S - T))) + (
        (d * (1 - q)) / 2
    )
    written_expr = (
        ((N - 2) / (N - 1)) * numerator_first_term
        + (1 / (N - 1)) * numerator_second_term
    ) / (
        ((N - 2) / (N - 1)) * denominator_first_term
        + (1 / (N - 1)) * denominator_second_term
    )

    assert (expr - written_expr).simplify() == 0


def test_expected_payoffs_of_resident():
    q, d = sym.symbols("q, delta")
    GTFT = (1, 1, q)

    assert (
        evolution.expected_payoffs_of_resident(
            GTFT, (1, 1, 1), N=2, k=1, delta=d, payoffs=[3, 0, 5, 1]
        )
        == 3
    )


def test_expected_payoffs_of_mutant():
    q, d = sym.symbols("q, delta")
    GTFT = (1, 1, q)

    assert (
        evolution.expected_payoffs_of_mutant(
            GTFT, (1, 1, 1), N=2, k=1, delta=d, payoffs=[3, 0, 5, 1]
        )
        == 3
    )


def test_ratio_of_expected_payoffs():
    q, d, b = sym.symbols("q, delta, beta")
    GTFT = (1, 1, q)

    assert (
        evolution.ratio_of_expected_payoffs(
            GTFT, (1, 1, 1), N=2, k=1, delta=d, beta=b, payoffs=[3, 0, 5, 1]
        )
        == 1
    )
