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


def probability_of_receiving_payoffs(
    resident, mutant, resident_state, mutant_state, N, k, delta
):
    """This is defined as x in the written material and is given by Eq (6).

    We use x(u1, u2) to denote the probability that the randomly chosen resident
    was at state u1 in the last round of their respective game, and
    that the mutant was at state u2.

    Parameters
    ----------
    resident : tuple
        A reactive resident.
    mutant : tuple
        A reactive mutant.
    resident_state : function
        State of resident in the last round.
    mutant_state : function
        State of mutant in the last round.
    N : int
        Number of individuals in the population
    k : int
        Number of mutants in the population
    delta : float
        The probability that the match will go on for another round.
    """
    if (resident_state, mutant_state) in [
        (
            formulation.probability_being_in_state_R,
            formulation.probability_being_in_state_R,
        ),
        (
            formulation.probability_being_in_state_T,
            formulation.probability_being_in_state_S,
        ),
        (
            formulation.probability_being_in_state_S,
            formulation.probability_being_in_state_T,
        ),
        (
            formulation.probability_being_in_state_P,
            formulation.probability_being_in_state_P,
        ),
    ]:
        first_term = (1 / (N - 1)) * resident_state(resident, mutant, delta)
    else:
        first_term = 0

    second_term_case_one = (
        ((k - 1) / (N - 2))
        * ((k - 2) / (N - 3))
        * resident_state(resident, mutant, delta)
        * mutant_state(mutant, mutant, delta)
    )
    second_term_case_two = (
        ((k - 1) / (N - 2))
        * ((N - k - 1) / (N - 3))
        * resident_state(resident, mutant, delta)
        * mutant_state(mutant, resident, delta)
    )
    second_term_case_three = (
        ((N - k - 1) / (N - 2))
        * ((k - 1) / (N - 3))
        * resident_state(resident, resident, delta)
        * mutant_state(mutant, mutant, delta)
    )
    second_term_case_four = (
        ((N - k - 1) / (N - 2))
        * ((N - k - 2) / (N - 3))
        * resident_state(resident, resident, delta)
        * mutant_state(mutant, resident, delta)
    )

    return first_term + (1 - 1 / (N - 1)) * (
        second_term_case_one
        + second_term_case_two
        + second_term_case_three
        + second_term_case_four
    )


def probability_mutant_increases(resident, mutant, N, k, delta, beta, payoffs):
    """The probability that the mutants in the population decrease.

    Thus, the probability that mutant becomes a resident.
    """
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
            probability_of_receiving_payoffs(
                resident, mutant, state[0], state[1], N, k, delta
            )
            * imitation_probability(payoff[0], payoff[1], beta)
            for state, payoff in zip(states, payoffs_)
        ]
    )
    return ((N - k) / N) * (k / N) * sum_


def probability_mutant_descreases(resident, mutant, N, k, delta, beta, payoffs):
    """The probability that the mutants in the population decrease.

    Thus, the probability that mutant becomes a resident.
    """
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
            probability_of_receiving_payoffs(
                resident, mutant, state[0], state[1], N, k, delta
            )
            * imitation_probability(payoff[1], payoff[0], beta)
            for state, payoff in zip(states, payoffs_)
        ]
    )

    return ((N - k) / N) * (k / N) * sum_


def expected_payoffs_of_resident(resident, mutant, N, k, delta, payoffs):
    """
    The expected payoff the resident.

    There are N individuals in the population, k of them are mutants and N - k
    are residents.

    The expected payoff the resident is defined as pi_1 in the written material
    and is given by:

    pi_1 = ((N - k - 1) / (N - 1)) * u(S1, S1) + (k / (N - 1)) * u(S1, S2)

    Parameters
    ----------
    resident : tuple
        A reactive resident.
    mutant : tuple
        A reactive mutant.
    resident_state : function
        State of resident in the last round.
    mutant_state : function
        State of mutant in the last round.
    N : int
        Number of individuals in the population
    k : int
        Number of mutants in the population
    delta : float
        The probability that the match will go on for another round.
    payoffs: tuple
        The payoffs of the game the players play.

    Returns
    -------
    expected_payoff: float
        The expected payoff pi_1
    """
    against_residents = formulation.utility(resident, resident, delta, payoffs)
    against_mutants = formulation.utility(resident, mutant, delta, payoffs)

    return ((N - k - 1) / (N - 1)) * against_residents + (
        k / (N - 1)
    ) * against_mutants


def expected_payoffs_of_mutant(resident, mutant, N, k, delta, payoffs):
    """
    The expected payoff the mutant.

    There are N individuals in the population, k of them are mutants and N - k
    are residents.

    The expected payoff the mutant is defined as pi_2 in the written material
    and is given by:


    pi_2 = ((N - k) / (N - 1)) * u(S2, S1) + ((k - 1)/ (N - 1)) * u(S2, S2)

    Parameters
    ----------
    resident : tuple
        A reactive resident.
    mutant : tuple
        A reactive mutant.
    resident_state : function
        State of resident in the last round.
    mutant_state : function
        State of mutant in the last round.
    N : int
        Number of individuals in the population
    k : int
        Number of mutants in the population
    delta : float
        The probability that the match will go on for another round.
    payoffs: tuple
        The payoffs of the game the players play.

    Returns
    -------
    expected_payoff: float
        The expected payoff pi_2
    """
    against_residents = formulation.utility(mutant, resident, delta, payoffs)
    against_mutants = formulation.utility(mutant, mutant, delta, payoffs)

    return ((N - k) * against_residents + (k - 1) * against_mutants) / (N - 1)


def ratio_of_expected_payoffs(resident, mutant, N, k, delta, beta, payoffs):
    """Returns the ration of:
        pi_1 / pi_2

    The expected payoff of the resident divided by the expected payoff of
    the mutant.
    """
    return expected_payoffs_of_resident(
        resident, mutant, N, k, delta, payoffs
    ) / expected_payoffs_of_mutant(resident, mutant, N, k, delta, payoffs)
