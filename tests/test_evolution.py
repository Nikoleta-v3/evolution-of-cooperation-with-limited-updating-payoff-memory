import itertools
from importlib.machinery import SourceFileLoader

import numpy as np
import sympy as sym

evolution = SourceFileLoader("evolution", "src/evolution.py").load_module()
simulation = SourceFileLoader("simulation", "src/simulation.py").load_module()
formulation = SourceFileLoader(
    "formulation", "src/formulation.py"
).load_module()


def test_imitation_probability():
    assert np.isclose(float(evolution.imitation_probability(0, 5, 1)), 0.993307)


def test_probability_of_receiving_payoffs():
    q, d, N = sym.symbols("q, delta, N")

    ALLD = (0, 0, 0)
    GTFT = (1, 1, q)

    all_pairs = itertools.product([ALLD, GTFT], repeat=2)
    states = [
        formulation.expected_distribution_last_round(*pair, d)
        for pair in all_pairs
    ]
    assert len(states) == 4

    xs = evolution.probability_of_receiving_payoffs(*states, 1, N)
    assert isinstance(xs, (np.ndarray, np.generic))
    assert xs.shape == (4, 4)


def test_fixation_probability_for_expected_payoffs():
    ALLD = (0, 0, 0)
    GTFT = (1, 1, 3 / 8)

    output = evolution.fixation_probability_for_expected_payoffs(
        GTFT,
        ALLD,
        10,
        delta=0.999,
        beta=1,
        payoffs=simulation.donation_game(1, 3),
    )

    assert len(output) == 3
    assert output[1] == 0
    assert output[2] == 0

    (
        fixation_probability,
        cooperation,
        score,
    ) = evolution.fixation_probability_for_expected_payoffs(
        ALLD,
        GTFT,
        10,
        delta=0.999,
        beta=1,
        payoffs=simulation.donation_game(1, 3),
    )

    assert isinstance(fixation_probability, float)
    assert fixation_probability <= 1
    assert cooperation == 1
    assert score == 2


def test_fixation_probability_for_stochastic_payoffs():
    ALLD = (0, 0, 0)
    GTFT = (1, 1, 3 / 8)

    (
        fixation_probability,
        cooperation,
        score,
    ) = evolution.fixation_probability_for_stochastic_payoffs(
        ALLD,
        GTFT,
        10,
        delta=0.999,
        beta=1,
        payoffs=simulation.donation_game(1, 3),
    )
    assert fixation_probability <= 1
    assert cooperation == 1
    assert score == 2
