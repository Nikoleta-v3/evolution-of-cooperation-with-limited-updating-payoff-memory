import itertools
import os.path
import sys
from collections import Counter

import numpy as np
import pandas as pd
from tqdm import tqdm

import evol_dynamics


def donation_game(c, b):
    """The donation game

    In the donation game the payoffs follow the constrain:

    T > R > P > S.

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


def is_donation(payoffs, dis=False):
    c = -payoffs[1]
    b = payoffs[2]

    if dis:
        return (payoffs[0] == b - c, "c:{c} and b:{b}")

    return payoffs[0] == b - c


def snowdrift_game(c, b):
    """The snowdrift game

    In the snowdrift game the payoffs follow the constrain:

    T > R > S > P.

    Parameters
    ----------
    c : int
        The resident's personal cost.
    b : int
        The mutant's benefit.

    Returns
    -------
    tuple
        The payoff vector for the snowdrift game.
    """
    return (b - (c / 2), b - c, b, 0)


def is_snowdrift(payoffs):
    b = payoffs[2]
    c = b - payoffs[1]

    return payoffs[0] == b - (c / 2)


def stag_hunt_game():
    """The stag hunt game

    In the stag hunt game the payoffs follow the constrain:

    R > T > P > S.

    Returns
    -------
    tuple
        The payoff vector for the stag hunt game.
    """
    return (3, 0, 2, 1)


def harmony_game():
    """The harmony game

    In the harmony game the payoffs follow the constrain:

    R > T, S > P.

    Returns
    -------
    tuple
        The payoff vector for the harmony game.
    """
    return (3, 2, 1, 0)


def main(
    N,
    delta,
    beta,
    number_of_steps,
    payoffs,
    mode,
    filename,
    seed=10,
    starting_resident=(0, 0, 0),
):
    data = [*payoffs, N, delta, beta, mode, 0, 0, *starting_resident]
    resident = starting_resident
    history = [resident]
    random_ = np.random.RandomState(seed)

    with open(filename, "w") as textfile:
        textfile.write(",".join([str(elem) for elem in data]) + "\n")
    textfile.close()

    for _ in tqdm(range(number_of_steps)):
        mutant = [random_.random() for _ in range(3)]

        if mode == "expected":
            (
                fixation_probability,
                cooperation,
                score,
            ) = evol_dynamics.fixation_probability_for_expected_payoffs(
                resident, mutant, N, delta, beta, payoffs
            )
        if mode == "stochastic":
            (
                fixation_probability,
                cooperation,
                score,
            ) = evol_dynamics.fixation_probability_for_stochastic_payoffs(
                resident, mutant, N, delta, beta, payoffs
            )

        if random_.random() < fixation_probability:
            resident = mutant
            data[-3:] = resident
            data[-4] = score
            data[-5] = cooperation

        with open(filename, "a") as textfile:
            textfile.write(",".join([str(elem) for elem in data]) + "\n")
        textfile.close()
        history.append(resident)
    return history


def _reshape_data(df):
    """Returns the points p and q that occurred at each time step of the 4."""
    history = df[["y", "p", "q"]].values
    points = [(p, q) for _, p, q in history]
    ps, qs = zip(*points)
    return ps, qs


if __name__ == "__main__":  # pragma: no cover

    number_of_steps = 10 ** 7
    mode = sys.argv[1]
    game = sys.argv[2]

    list_of_games = {
        "donation": donation_game(1, 3),
        "snowdrift": snowdrift_game(1, 3),
        "stag": stag_hunt_game(),
        "harmony": harmony_game(),
    }
    payoffs = list_of_games[game]
    seed = 0
    filename = f"data/{mode}_{game}_{seed}_payoffs.csv"
    starting_resident = (0, 0, 0)

    _ = main(
        N=100,
        delta=1 - (10 ** -3),
        beta=1,
        number_of_steps=number_of_steps,
        payoffs=payoffs,
        mode=mode,
        filename=filename,
        seed=seed,
        starting_resident=starting_resident,
    )
