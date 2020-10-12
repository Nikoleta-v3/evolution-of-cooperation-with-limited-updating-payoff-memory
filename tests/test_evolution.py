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
    assert np.isclose(output[1], 0, 10 ** (-3))
    assert np.isclose(output[2], 0, 10 ** (-3))

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
    assert np.isclose(cooperation, 1)
    assert np.isclose(score, 2)


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
    assert np.isclose(cooperation, 1)
    assert np.isclose(score, 2)


def test_fixation_probability_for_stochastic_test_case():
    """
    This is inline with the MatLab code given to me by Dr Hilbe.
    More specifically:

    ```
    >> u = [2, -1, 3, 0]
    >> beta = 1
    >> Rho=zeros(4,4);
       for i1=1:4
           for i2=1:4
               Rho(i1,i2)=1/(1+exp(-beta*(u(i2)-u(i1))));
           end
       end

    >> CalcRho([0, 0, 0], [1 / 3, 1 / 7, 1 / 6], Rho, 10, u, 0.999, beta, 0, 1)
    0.1814
    ```
    """
    mutant = (0, 0, 0)
    resident = (1 / 3, 1 / 7, 1 / 6)

    (
        fixation_probability,
        _,
        _,
    ) = evolution.fixation_probability_for_stochastic_payoffs(
        resident=resident,
        mutant=mutant,
        N=10,
        delta=0.999,
        beta=1,
        payoffs=simulation.donation_game(1, 3),
    )
    assert np.isclose(fixation_probability, 0.1814, rtol=10 ** -3)


def test_fixation_probability_for_stochastic_test_case():
    """
    This is inline with the MatLab code given to me by Dr Hilbe.
    More specifically:

    ```
    >> u = [2, -1, 3, 0]
    >> beta = 1
    >> Rho=zeros(4,4);
       for i1=1:4
           for i2=1:4
               Rho(i1,i2)=1/(1+exp(-beta*(u(i2)-u(i1))));
           end
       end

    >> [rho,coopMM,piMM]=CalcRho([0, 0, 0, 0, 0], [1 / 7, 1 / 6, 1 / 7, 1 / 6, 1 / 3], Rho, 10, u, 0.999, beta, 1, 0)
    rho =

    0.2268

    coopMM =

        0

    piMM =

        0

    ```
    """
    mutant = (0, 0, 0)
    resident = (1 / 3, 1 / 7, 1 / 6)

    (
        fixation_probability,
        coop_rate,
        score,
    ) = evolution.fixation_probability_for_expected_payoffs(
        resident=resident,
        mutant=mutant,
        N=10,
        delta=0.999,
        beta=1,
        payoffs=simulation.donation_game(1, 3),
    )
    assert np.isclose(fixation_probability, 0.2268, rtol=10 ** -3)
    assert np.isclose(coop_rate, 0, rtol=10 ** -3)
    assert np.isclose(score, 0, rtol=10 ** -3)

    # For the opposite case where the mutant is the resident and the resident is
    # the mutant.
    expected_fixation = 0.0297
    expected_coop_rate = 0.1630
    expected_score = 0.3259

    resident = (0, 0, 0)
    mutant = (1 / 3, 1 / 7, 1 / 6)

    (
        fixation_probability,
        coop_rate,
        score,
    ) = evolution.fixation_probability_for_expected_payoffs(
        resident=resident,
        mutant=mutant,
        N=10,
        delta=0.999,
        beta=1,
        payoffs=simulation.donation_game(1, 3),
    )
    assert np.isclose(fixation_probability, expected_fixation, rtol=10 ** -3)
    assert np.isclose(coop_rate, expected_coop_rate, rtol=10 ** -3)
    assert np.isclose(score, expected_score, rtol=10 ** -3)
