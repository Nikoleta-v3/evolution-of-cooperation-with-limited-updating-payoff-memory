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


def test_probability_of_receiving_payoffs():
    q, d, N = sym.symbols("q, delta, N")

    ALLD = (0, 0, 0)
    GTFT = (1, 1, q)

    expr = formulation.probability_of_receiving_payoffs(
        player=GTFT,
        opponent=ALLD,
        player_state=formulation.probability_being_in_state_R,
        opponent_state=formulation.probability_being_in_state_P,
        N=N,
        k=1,
        delta=d,
    ).factor()

    assert (expr - (((N - 2) / (N - 1)) * d * (1 - q))).simplify() == 0


def test_probability_of_receiving_payoffs_for_non_feasible_payoffs():
    """
    For this test case the first_term in `probability_of_receiving_payoffs`
    falls to zero because an GTFT can not interact with an ALLD player and
    receive an S payoff while ALLD receives R.
    """
    q, d, N = sym.symbols("q, delta, N")

    ALLD = (0, 0, 0)
    GTFT = (1, 1, q)

    expr = formulation.probability_of_receiving_payoffs(
        player=GTFT,
        opponent=ALLD,
        player_state=formulation.probability_being_in_state_S,
        opponent_state=formulation.probability_being_in_state_R,
        N=N,
        k=1,
        delta=d,
    ).simplify()

    assert expr == 0


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
