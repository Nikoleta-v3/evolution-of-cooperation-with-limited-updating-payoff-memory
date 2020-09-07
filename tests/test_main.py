from importlib.machinery import SourceFileLoader

import sympy as sym
import numpy as np

main = SourceFileLoader("main", "src/main.py").load_module()


def test_expected_distribution_opening_round():
    assert main.expected_distribution_opening_round((1, 0, 0), (1, 0, 0)) == (
        1,
        0,
        0,
        0,
    )
    assert main.expected_distribution_opening_round((0, 0, 0), (1, 0, 0)) == (
        0,
        0,
        1,
        0,
    )
    assert main.expected_distribution_opening_round((1, 0, 0), (0, 0, 0)) == (
        0,
        1,
        0,
        0,
    )
    assert main.expected_distribution_opening_round((0, 0, 0), (0, 0, 0)) == (
        0,
        0,
        0,
        1,
    )


def test_markov_chain_for_reactive_strategies_first_row():
    y_1, p_1, q_1 = sym.symbols("y_1, p_1, q_1")
    y_2, p_2, q_2 = sym.symbols("y_2, p_2, q_2")

    markov = main.markov_chain_for_reactive_strategies(
        (y_1, p_1, q_1), (y_2, p_2, q_2)
    )

    assert markov[0, 0] == p_1 * p_2
    assert markov[0, 1] == p_1 * (1 - p_2)
    assert markov[0, 2] == (1 - p_1) * p_2
    assert markov[0, 3] == (1 - p_1) * (1 - p_2)


def test_markov_chain_for_reactive_strategies_first_column():
    y_1, p_1, q_1 = sym.symbols("y_1, p_1, q_1")
    y_2, p_2, q_2 = sym.symbols("y_2, p_2, q_2")

    markov = main.markov_chain_for_reactive_strategies(
        (y_1, p_1, q_1), (y_2, p_2, q_2)
    )

    assert markov[0, 0] == p_1 * p_2
    assert markov[1, 0] == q_1 * p_2
    assert markov[2, 0] == p_1 * q_2
    assert markov[3, 0] == q_1 * q_2


def test_probability_being_in_state_R():
    assert main.probability_being_in_state_R((1, 0, 0), (1, 0, 0), delta=0) == 1


def test_probability_being_in_state_S():
    assert main.probability_being_in_state_S((1, 0, 0), (0, 0, 0), delta=0) == 1


def test_probability_being_in_state_T():
    assert main.probability_being_in_state_T((0, 0, 0), (1, 0, 0), delta=0) == 1


def test_probability_being_in_state_P():
    assert main.probability_being_in_state_P((0, 0, 0), (0, 0, 0), delta=0) == 1


def test_imitation_probability():
    assert np.isclose(float(main.imitation_probability(0, 5, 1)), 0.993307)


def test_probability_of_receving_payoffs():
    q, d, N = sym.symbols("q, delta, N")

    ALLD = (0, 0, 0)
    GTFT = (1, 1, q)

    expr = main.probability_of_receving_payoffs(
        player=GTFT,
        opponent=ALLD,
        player_state=main.probability_being_in_state_R,
        opponent_state=main.probability_being_in_state_P,
        N=N,
        k=1,
        delta=d,
    ).factor()

    assert (expr - (((N - 2) / (N - 1)) * d * (1 - q))).simplify() == 0
