import itertools
from importlib.machinery import SourceFileLoader

import numpy as np
import pandas as pd
import sympy as sym

simulation = SourceFileLoader("simulation", "src/simulation.py").load_module()
formulation = SourceFileLoader(
    "formulation", "src/formulation.py"
).load_module()


def test_donation_game():
    c, b = sym.symbols("c, b")
    assert (b - c, -c, b, 0) == simulation.donation_game(c, b)
    assert (2, -1, 3, 0) == simulation.donation_game(1, 3)


def test_reshape_data():
    df = pd.DataFrame(np.random.random(size=(10, 3)), columns=list("ypq"))

    ps, qs = simulation._reshape_data(df)

    assert type(ps) == tuple
    assert type(qs) == tuple
    assert len(qs) <= 10
    assert len(ps) <= 10


def test_simulate_probability_of_receiving_payoffs():
    q, delta, N = sym.symbols("q, delta, N")
    resident = (1, 1, q)
    mutant = (0, 0, 0)

    feasible_states = [("R", "R"), ("S", "T"), ("T", "S"), ("P", "P")]

    state_labels = [
        (state, label[0], label[1])
        for label in itertools.product(["resident", "mutant"], repeat=2)
        for state in ["R", "S", "T", "P"]
    ]
    states = itertools.product(
        [
            formulation.probability_being_in_state_R(resident, resident, delta),
            formulation.probability_being_in_state_S(resident, resident, delta),
            formulation.probability_being_in_state_T(resident, resident, delta),
            formulation.probability_being_in_state_P(resident, resident, delta),
            formulation.probability_being_in_state_R(resident, mutant, delta),
            formulation.probability_being_in_state_S(resident, mutant, delta),
            formulation.probability_being_in_state_T(resident, mutant, delta),
            formulation.probability_being_in_state_P(resident, mutant, delta),
            formulation.probability_being_in_state_R(mutant, resident, delta),
            formulation.probability_being_in_state_S(mutant, resident, delta),
            formulation.probability_being_in_state_T(mutant, resident, delta),
            formulation.probability_being_in_state_P(mutant, resident, delta),
            formulation.probability_being_in_state_R(mutant, mutant, delta),
            formulation.probability_being_in_state_S(mutant, mutant, delta),
            formulation.probability_being_in_state_T(mutant, mutant, delta),
            formulation.probability_being_in_state_P(mutant, mutant, delta),
        ],
        repeat=1,
    )

    states_dict = {
        label: state[0] for label, state in zip(state_labels, states)
    }

    label = ("S", "R")
    assert (
        simulation.simulate_probability_of_receiving_payoffs(
            label, feasible_states, states_dict, N, k=1
        )
        == 0
    )

    label = ("R", "P")
    expr = simulation.simulate_probability_of_receiving_payoffs(
        label, feasible_states, states_dict, N, k=1
    ).factor()
    assert (expr - (((N - 2) / (N - 1)) * delta * (1 - q))).simplify() == 0

    label = ("R", "T")
    expr = simulation.simulate_probability_of_receiving_payoffs(
        label, feasible_states, states_dict, N, k=1
    ).factor()
    assert (
        expr - (((N - 2) / (N - 1)) * (1 - delta + delta * q))
    ).simplify() == 0

    label = ("S", "T")
    expr = simulation.simulate_probability_of_receiving_payoffs(
        label, feasible_states, states_dict, N, k=1
    )
    assert (expr - ((1 / (N - 1)) * (1 - delta + delta * q))).simplify() == 0

    label = ("P", "P")
    expr = simulation.simulate_probability_of_receiving_payoffs(
        label, feasible_states, states_dict, N, k=1
    )
    assert (expr - ((1 / (N - 1)) * (delta * (1 - q)))).simplify() == 0

    label = ("R", "R")
    assert (
        simulation.simulate_probability_of_receiving_payoffs(
            label, feasible_states, states_dict, N, k=1
        )
        == 0
    )
