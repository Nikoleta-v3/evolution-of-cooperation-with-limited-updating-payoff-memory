import concurrent.futures
import time
from importlib.machinery import SourceFileLoader

import numpy as np
import sympy as sym

formulation = SourceFileLoader(
    "formulation", "src/formulation.py"
).load_module()

import itertools


def imitation_probability(
    utility_of_resident, utility_of_mutant, strength_of_selection
):
    return 1 / (
        1
        + sym.exp(
            -strength_of_selection * (utility_of_mutant - utility_of_resident)
        )
    )


def fixation_probability_for_expected_payoffs(
    resident, mutant, N, delta, beta, payoffs
):
    """Returns the fixation probability of a mutant based on the expected
    payoffs.

    The function also returns two other measures which are calculated during
    the calculation of the fixation probability:

    - cooperation rate of a mutant against another mutant (which is the
    probability of CC and CD).
    - the payoff of a mutant against another mutant.

    Parameters
    ----------
    resident : tuple
        A reactive resident.
    mutant : tuple
        A reactive mutant.
    N : int
        Number of individuals in the population
    delta : float
        The probability that the match will go on for another round
    beta : float
        The strength of selection
    payoffs: tuple
        The payoffs of the game the players play.
    """
    payoff_vector = np.array(payoffs)
    combinations = itertools.product([mutant, resident], repeat=2)

    steady_states = [
        formulation.steady_state(p1, p2, delta)
        for p1, p2 in combinations
    ]
    payoff_MM, payoff_MR, payoff_RM, payoff_RR = [
        state @ payoff_vector for state in steady_states
    ]
    lminus, lplus = [], []
    for k in range(1, N):
        expected_payoff_mutant = ((k - 1) / (N - 1) * payoff_MM) + (
            (N - k) / (N - 1)
        ) * payoff_MR
        expected_payoff_resident = (k / (N - 1) * payoff_RM) + (
            (N - k - 1) / (N - 1)
        ) * payoff_RR

        lplus.append(
            1
            / (
                1
                + np.exp(
                    float(
                        -beta
                        * (expected_payoff_mutant - expected_payoff_resident)
                    )
                )
            )
        )
        lminus.append(
            1
            / (
                1
                + np.exp(
                    float(
                        -beta
                        * (expected_payoff_resident - expected_payoff_mutant)
                    )
                )
            )
        )
    gammas = np.array(lminus) / np.array(lplus)
    cooperation_rate = steady_states[0][0] + steady_states[0][1]
    return (
        1 / (1 + np.sum(np.cumprod(gammas))),
        cooperation_rate,
        payoff_MM,
    )


def fixation_probability_for_stochastic_payoffs(
    resident,
    mutant,
    N,
    delta,
    beta,
    payoffs,
):
    """Returns the fixation probability of a mutant based on the stochastic
    payoffs.

    The function also returns two other measures which are calculated during
    the calculation of the fixation probability:

    - cooperation rate of a mutant against another mutant (which is the
    probability of CC and CD).
    - the payoff of a mutant against another mutant.


    Parameters
    ----------
    resident : tuple
        A reactive resident.
    mutant : tuple
        A reactive mutant.
    N : int
        Number of individuals in the population
    delta : float
        The probability that the match will go on for another round
    beta : float
        The strength of selection
    payoffs: tuple
        The payoffs of the game the players play.
    """
    payoff_vector = np.array(payoffs)

    rhos = np.array(
        [
            [
                float(
                    imitation_probability(
                        payoff_vector[i], payoff_vector[j], beta
                    )
                )
                for i in range(4)
            ]
            for j in range(4)
        ]
    )
    combinations = itertools.product([mutant, resident], repeat=2)
    vMM, vMR, vRM, vRR = [
        formulation.expected_distribution_last_round(p1, p2, delta)
        for p1, p2 in combinations
    ]

    lminus, lplus = [], []
    for k in range(1, N):
        x = probability_of_receiving_payoffs(vMM, vMR, vRM, vRR, k, N)
        lplus.append(sum(sum(x * rhos.T)))
        lminus.append(sum(sum(x * rhos)))

    gammas = np.array(lminus) / np.array(lplus)
    cooperation_rate = vMM[0] + vMM[1]
    return (
        float(1 / (1 + np.sum(np.cumprod(gammas)))),
        cooperation_rate,
        vMM @ payoff_vector,
    )


def probability_of_receiving_payoffs(
    vector_mutant_mutant,
    vector_mutant_resident,
    vector_resident_mutant,
    vector_resident_resident,
    k,
    N,
):
    """This is defined as x in the written material and is given by Eq (6).
    We use x(u1, u2) to denote the probability that the randomly chosen resident
    was at state u1 in the last round of their respective game, and
    that the mutant was at state u2.
    """
    feasible_states = [(0, 0), (1, 2), (2, 1), (3, 3)]
    x = []
    for i in range(4):
        for j in range(4):
            expr = 0

            if (i, j) in feasible_states:
                expr += (1 / (N - 1)) * vector_resident_mutant[i]

            expr += (1 - 1 / (N - 1)) * (
                ((k - 1) / (N - 2))
                * ((k - 2) / (N - 3))
                * vector_resident_mutant[i]
                * vector_mutant_mutant[j]
                + ((k - 1) / (N - 2))
                * ((N - k - 1) / (N - 3))
                * vector_resident_mutant[i]
                * vector_mutant_resident[j]
                + ((N - k - 1) / (N - 2))
                * ((k - 1) / (N - 3))
                * vector_resident_resident[i]
                * vector_mutant_mutant[j]
                + ((N - k - 1) / (N - 2))
                * ((N - k - 2) / (N - 3))
                * vector_resident_resident[i]
                * vector_mutant_resident[j]
            )
            x.append(expr)
    return np.array(x).reshape(4, 4)
