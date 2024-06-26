import numpy as np
import sympy as sym

import evol_dynamics


def test_expected_distribution_opening_round():
    assert evol_dynamics.expected_distribution_opening_round(
        (1, 0, 0), (1, 0, 0)
    ) == (
        1,
        0,
        0,
        0,
    )
    assert evol_dynamics.expected_distribution_opening_round(
        (0, 0, 0), (1, 0, 0)
    ) == (
        0,
        0,
        1,
        0,
    )
    assert evol_dynamics.expected_distribution_opening_round(
        (1, 0, 0), (0, 0, 0)
    ) == (
        0,
        1,
        0,
        0,
    )
    assert evol_dynamics.expected_distribution_opening_round(
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

    markov = evol_dynamics.markov_chain_for_reactive_strategies(
        (y_1, p_1, q_1), (y_2, p_2, q_2)
    )

    assert markov[0, 0] == p_1 * p_2
    assert markov[0, 1] == p_1 * (1 - p_2)
    assert markov[0, 2] == (1 - p_1) * p_2
    assert markov[0, 3] == (1 - p_1) * (1 - p_2)


def test_markov_chain_for_reactive_strategies_first_column():
    y_1, p_1, q_1 = sym.symbols("y_1, p_1, q_1")
    y_2, p_2, q_2 = sym.symbols("y_2, p_2, q_2")

    markov = evol_dynamics.markov_chain_for_reactive_strategies(
        (y_1, p_1, q_1), (y_2, p_2, q_2)
    )

    assert markov[0, 0] == p_1 * p_2
    assert markov[1, 0] == q_1 * p_2
    assert markov[2, 0] == p_1 * q_2
    assert markov[3, 0] == q_1 * q_2


def test_probability_being_in_state_R():
    assert (
        evol_dynamics.formulation.probability_being_in_state_R(
            (1, 0, 0), (1, 0, 0), delta=0
        )
        == 1
    )


def test_probability_being_in_state_S():
    assert (
        evol_dynamics.formulation.probability_being_in_state_S(
            (1, 0, 0), (0, 0, 0), delta=0
        )
        == 1
    )


def test_probability_being_in_state_T():
    assert (
        evol_dynamics.formulation.probability_being_in_state_T(
            (0, 0, 0), (1, 0, 0), delta=0
        )
        == 1
    )


def test_probability_being_in_state_P():
    assert (
        evol_dynamics.formulation.probability_being_in_state_P(
            (0, 0, 0), (0, 0, 0), delta=0
        )
        == 1
    )


def test_expected_distribution_last_round_defectors():
    d = sym.symbols("delta")
    assert evol_dynamics.expected_distribution_last_round(
        (0, 0, 0), (0, 0, 0), d
    ) == (0, 0, 0, 1)


def test_expected_distribution_last_round_cooperators():
    d = sym.symbols("delta")
    assert evol_dynamics.expected_distribution_last_round(
        (1, 1, 1), (1, 1, 1), d
    ) == (1, 0, 0, 0)


def test_expected_distribution_last_round_opening_with_c():
    d = sym.symbols("delta")
    assert evol_dynamics.expected_distribution_last_round(
        (0, 1, 1), (0, 0, 0), d
    ) == (0, d, 0, 1 - d)


def test_steady_state_inline_with_matlab_code():
    """
    Tests that the results are the same as the ones given by the MatLab code
    produced by CH.
    """
    player = (0, 0, 0)
    opponent = (1 / 3, 1 / 7, 1 / 6)
    delta = 0.999

    steady_states = evol_dynamics.steady_state(player, opponent, delta)
    expected_steady_states = [0, 0, 0.1668, 0.8332]

    for state, expected_state in zip(steady_states, expected_steady_states):
        assert np.isclose(state, expected_state, 10 ** (-3))
