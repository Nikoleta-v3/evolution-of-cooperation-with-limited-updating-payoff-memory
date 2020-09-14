import itertools
import os.path
from collections import Counter
from importlib.machinery import SourceFileLoader

import numpy as np
import pandas as pd
from tqdm import tqdm

evolution = SourceFileLoader("evolution", "src/evolution.py").load_module()
formulation = SourceFileLoader(
    "formulation", "src/formulation.py"
).load_module()


def donation_game(c, b):
    """The donation game

    Parameters
    ----------
    c : int
        The resident's personal cost.
    b : int
        The mutant's benefit.

    Returns
    -------
    tuple
        The payoff vector for the donation game.
    """
    return (b - c, -c, b, 0)


def simulate_probability_of_receiving_payoffs(
    label, feasible_states, states_dict, N, k
):
    if (label[1], label[-1]) in feasible_states:
        first_term = (1 / (N - 1)) * states_dict[
            (label[1], "resident", "mutant")
        ]
    else:
        first_term = 0

    second_term_case_one = (
        ((k - 1) / (N - 2))
        * ((k - 2) / (N - 3))
        * states_dict[(label[1], "resident", "mutant")]
        * states_dict[(label[-1], "mutant", "mutant")]
    )

    second_term_case_two = (
        ((k - 1) / (N - 2))
        * ((N - k - 1) / (N - 3))
        * states_dict[(label[1], "resident", "mutant")]
        * states_dict[(label[-1], "mutant", "resident")]
    )

    second_term_case_three = (
        ((N - k - 1) / (N - 2))
        * ((k - 1) / (N - 3))
        * states_dict[(label[1], "resident", "resident")]
        * states_dict[(label[-1], "mutant", "mutant")]
    )

    second_term_case_four = (
        ((N - k - 1) / (N - 2))
        * ((N - k - 2) / (N - 3))
        * states_dict[(label[1], "resident", "resident")]
        * states_dict[(label[-1], "mutant", "mutant")]
    )

    return first_term + (1 - 1 / (N - 1)) * (
        second_term_case_one
        + second_term_case_two
        + second_term_case_three
        + second_term_case_four
    )


def gammas_for_stochastic_payoffs(resident, mutant, delta, N, beta, payoffs):
    feasible_states = list(itertools.product(["R", "S", "T", "P"], repeat=2))

    payoffs_dict = {
        label: payoff for label, payoff in zip(["R", "S", "T", "P"], payoffs)
    }

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
            formulation.probability_being_in_state_P(mutant, resident, delta),
            formulation.probability_being_in_state_R(mutant, resident, delta),
            formulation.probability_being_in_state_S(mutant, resident, delta),
            formulation.probability_being_in_state_T(mutant, resident, delta),
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

    combinations = list(
        itertools.product(
            ["resident", "mutant"], ["R", "S", "T", "P"], repeat=2
        )
    )

    gammas = []
    for k in range(1, N):
        payoffs_for_increase = []
        payoffs_for_decrease = []
        for label in combinations:
            utility_of_resident = payoffs_dict[label[1]]
            utility_of_mutant = payoffs_dict[label[-1]]

            payoffs_for_increase.append(
                simulate_probability_of_receiving_payoffs(
                    label, feasible_states, states_dict, N, k
                )
                * float(
                    evolution.imitation_probability(
                        utility_of_resident, utility_of_mutant, beta
                    )
                )
            )

            payoffs_for_decrease.append(
                simulate_probability_of_receiving_payoffs(
                    label, feasible_states, states_dict, N, k
                )
                * float(
                    evolution.imitation_probability(
                        utility_of_mutant, utility_of_resident, beta
                    )
                )
            )

        gammas.append(
            (((N - k) / N) * (k / N) * sum(payoffs_for_decrease))
            / (((N - k) / N) * (k / N) * sum(payoffs_for_increase))
        )

    return gammas


def fixation_probability(resident, mutant, N, delta, beta, payoffs, mode):
    if mode == "s":
        gammas = gammas_for_stochastic_payoffs(
            resident, mutant, delta, N, beta, payoffs
        )
    if mode == "e":
        gammas = [
            evolution.ratio_of_expected_payoffs(
                resident, mutant, N, k, delta, beta, payoffs
            )
            for k in range(1, N)
        ]
    if mode not in ["s", "e"]:
        print("Chose a feasible mode.")
        exit()

    return 1 / (1 + np.sum(np.cumprod(gammas)))


def main(
    N,
    d,
    b,
    number_of_steps,
    payoffs,
    mode,
    filename,
    seed=10,
    starting_resident=(0, 0, 0),
):
    resident = starting_resident
    history = [resident]
    random_ = np.random.RandomState(seed)

    for _ in tqdm(range(number_of_steps)):
        mutant = [random_.random() for _ in range(3)]

        phi = fixation_probability(resident, mutant, N, d, b, payoffs, mode)

        if random_.random() < abs(phi):
            resident = mutant

        with open(filename, "a") as textfile:
            textfile.write(",".join([str(elem) for elem in resident]) + "\n")
        textfile.close()
        history.append(resident)
    return history


def _reshape_data(df):
    """Returns the points p and q that occurred at each time step of the simulation."""
    history = df.values
    points = [(p, q) for _, p, q in history]
    ps, qs = zip(*points)
    return ps, qs


if __name__ == "__main__":  # pragma: no cover

    number_of_steps = 10 ** 3
    mode = "s"
    filename = "stochastic_payoff_data.csv"

    _ = main(
        N=100,
        d=1 - (10 ** -3),
        b=1,
        number_of_steps=number_of_steps,
        payoffs=donation_game(1, 3),
        mode=mode,
        filename=filename,
        seed=1,
    )
