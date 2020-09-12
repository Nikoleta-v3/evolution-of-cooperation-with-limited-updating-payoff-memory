from importlib.machinery import SourceFileLoader

import numpy as np
import sympy as sym

formulation = SourceFileLoader(
    "formulation", "src/formulation.py"
).load_module()


def test_expected_distribution_opening_round():
    assert formulation.expected_distribution_opening_round(
        (1, 0, 0), (1, 0, 0)
    ) == (
        1,
        0,
        0,
        0,
    )
    assert formulation.expected_distribution_opening_round(
        (0, 0, 0), (1, 0, 0)
    ) == (
        0,
        0,
        1,
        0,
    )
    assert formulation.expected_distribution_opening_round(
        (1, 0, 0), (0, 0, 0)
    ) == (
        0,
        1,
        0,
        0,
    )
    assert formulation.expected_distribution_opening_round(
        (0, 0, 0), (0, 0, 0)
    ) == (
        0,
        0,
        0,
        1,
    )


def test_markov_chain_for_reactive_strategies_first_row():
    y_1, p_1, q_1 = sym.symbols("y_1, p_1, q_1")
    y_2, p_2, q_2 = sym.symbols("y_2, p_2, q_2")

    markov = formulation.markov_chain_for_reactive_strategies(
        (y_1, p_1, q_1), (y_2, p_2, q_2)
    )

    assert markov[0, 0] == p_1 * p_2
    assert markov[0, 1] == p_1 * (1 - p_2)
    assert markov[0, 2] == (1 - p_1) * p_2
    assert markov[0, 3] == (1 - p_1) * (1 - p_2)


def test_markov_chain_for_reactive_strategies_first_column():
    y_1, p_1, q_1 = sym.symbols("y_1, p_1, q_1")
    y_2, p_2, q_2 = sym.symbols("y_2, p_2, q_2")

    markov = formulation.markov_chain_for_reactive_strategies(
        (y_1, p_1, q_1), (y_2, p_2, q_2)
    )

    assert markov[0, 0] == p_1 * p_2
    assert markov[1, 0] == q_1 * p_2
    assert markov[2, 0] == p_1 * q_2
    assert markov[3, 0] == q_1 * q_2


def test_probability_being_in_state_R():
    assert (
        formulation.probability_being_in_state_R((1, 0, 0), (1, 0, 0), delta=0)
        == 1
    )


def test_probability_being_in_state_S():
    assert (
        formulation.probability_being_in_state_S((1, 0, 0), (0, 0, 0), delta=0)
        == 1
    )


def test_probability_being_in_state_T():
    assert (
        formulation.probability_being_in_state_T((0, 0, 0), (1, 0, 0), delta=0)
        == 1
    )


def test_probability_being_in_state_P():
    assert (
        formulation.probability_being_in_state_P((0, 0, 0), (0, 0, 0), delta=0)
        == 1
    )


def test_expected_distribution_last_round_defectors():
    d = sym.symbols("delta")
    assert formulation.expected_distribution_last_round(
        (0, 0, 0), (0, 0, 0), d
    ) == (0, 0, 0, 1)


def test_expected_distribution_last_round_cooperators():
    d = sym.symbols("delta")
    assert formulation.expected_distribution_last_round(
        (1, 1, 1), (1, 1, 1), d
    ) == (1, 0, 0, 0)


def test_expected_distribution_last_round_opening_with_c():
    d = sym.symbols("delta")
    assert formulation.expected_distribution_last_round(
        (0, 1, 1), (0, 0, 0), d
    ) == (0, d, 0, 1 - d)


def test_utility_defectors():
    assert (
        formulation.utility(
            (0, 0, 0), (1, 1, 3 / 8), delta=0, payoffs=(3, 0, 5, 1)
        )
        == 5
    )
    assert (
        formulation.utility(
            (0, 0, 0), (1, 1, 1), delta=1 / 2, payoffs=(3, 0, 5, 1)
        )
        == 5
    )


def test_utility_gtft_vs_defector():
    assert (
        formulation.utility(
            (1, 1, 3 / 8), (0, 0, 0), delta=0, payoffs=(3, 0, 5, 1)
        )
        == 0
    )
    assert (
        formulation.utility(
            (0, 0, 0), (1, 1, 3 / 8), delta=1 / 2, payoffs=(3, 0, 5, 1)
        )
        == 3.75
    )


def test_utility_cooperator():
    assert (
        formulation.utility(
            (1, 1, 1), (1, 1, 1), delta=1 / 2, payoffs=(3, 0, 5, 1)
        )
        == 3
    )
