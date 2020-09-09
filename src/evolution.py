from importlib.machinery import SourceFileLoader

import numpy as np
import sympy as sym

formulation = SourceFileLoader(
    "formulation", "src/formulation.py"
).load_module()

import itertools


def imitation_probability(
    utility_of_learner, utility_of_role_model, strength_of_selection
):
    return 1 / (
        1
        + sym.exp(
            -strength_of_selection
            * (utility_of_role_model - utility_of_learner)
        )
    )


def probability_mutant_increases(player, opponent, N, k, delta, beta, payoffs):

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
                player, opponent, state[0], state[1], N, k, delta
            )
            * imitation_probability(payoff[0], payoff[1], beta)
            for state, payoff in zip(states, payoffs_)
        ]
    )
    return ((N - k) / N) * (k / N) * sum_


def probability_mutant_descreases(player, opponent, N, k, delta, beta, payoffs):

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
                player, opponent, state[0], state[1], N, k, delta
            )
            * imitation_probability(payoff[1], payoff[0], beta)
            for state, payoff in zip(states, payoffs_)
        ]
    )

    return ((N - k) / N) * (k / N) * sum_
