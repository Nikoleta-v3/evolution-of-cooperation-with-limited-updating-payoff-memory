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


def probability_mutant_increases(resident, mutant, N, k, delta, beta, payoffs):

    states = itertools.product(
        [
            formulation.probability_being_in_state_R,
            formulation.probability_being_in_state_S,
            formulation.probability_being_in_state_T,
            formulation.probability_being_in_state_P,
        ],
        repeat=2,
    )

    payoffs_ = itertools.product(
        payoffs,
        repeat=2,
    )

    sum_ = sum(
        [
            formulation.probability_of_receiving_payoffs(
                resident, mutant, state[0], state[1], N, k, delta
            )
            * imitation_probability(payoff[0], payoff[1], beta)
            for state, payoff in zip(states, payoffs_)
        ]
    )
    return ((N - k) / N) * (k / N) * sum_


def probability_mutant_descreases(resident, mutant, N, k, delta, beta, payoffs):

    states = itertools.product(
        [
            formulation.probability_being_in_state_R,
            formulation.probability_being_in_state_S,
            formulation.probability_being_in_state_T,
            formulation.probability_being_in_state_P,
        ],
        repeat=2,
    )

    payoffs_ = itertools.product(
        payoffs,
        repeat=2,
    )

    sum_ = sum(
        [
            formulation.probability_of_receiving_payoffs(
                resident, mutant, state[0], state[1], N, k, delta
            )
            * imitation_probability(payoff[1], payoff[0], beta)
            for state, payoff in zip(states, payoffs_)
        ]
    )

    return ((N - k) / N) * (k / N) * sum_


def expected_payoffs_of_resident(resident, mutant, N, k, delta, payoffs):

    payoff_vector = np.array(payoffs)

    against_residents = (
        np.array(
            formulation.expected_distribution_last_round(
                resident, resident, delta
            )
        )
        @ payoff_vector
    )
    against_mutants = (
        np.array(
            formulation.expected_distribution_last_round(
                resident, mutant, delta
            )
        )
        @ payoff_vector
    )

    return ((N - k - 1) * against_residents + k * against_mutants) / (N - 1)


def expected_payoffs_of_mutant(resident, mutant, N, k, delta, payoffs):

    payoff_vector = np.array(payoffs)

    against_residents = (
        np.array(
            formulation.expected_distribution_last_round(
                mutant, resident, delta
            )
        )
        @ payoff_vector
    )
    against_mutants = (
        np.array(
            formulation.expected_distribution_last_round(mutant, mutant, delta)
        )
        @ payoff_vector
    )

    return ((N - k) * against_residents + (k - 1) * against_mutants) / (N - 1)


def ratio_of_expected_payoffs(resident, mutant, N, k, delta, beta, payoffs):

    return expected_payoffs_of_resident(
        resident, mutant, N, k, delta, payoffs
    ) / expected_payoffs_of_mutant(resident, mutant, N, k, delta, payoffs)
