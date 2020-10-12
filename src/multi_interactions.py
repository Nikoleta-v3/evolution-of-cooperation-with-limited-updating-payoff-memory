import itertools
import multiprocessing
import os
import random
import time

import axelrod as axl
import numpy as np
import tqdm


def introduce_mutant(population, resident, random_state):
    """Introduces a mutant in a population of residents.

    Parameters
    ----------
    population : list
        A list of dictionaries. Each dictionary described the population at a
        given time step.
    resident : tuple
        A reactive tuple for the strategy which is currently the resident in the
        population.

    Returns
    -------
    tuple, list
        The mutant as a tuple but also the updated list of the population
    """
    mutant = tuple(random_state.random() for _ in range(3))
    population = {resident: population[resident] - 1, mutant: 1}

    return mutant, population


class ReactivePlayer(axl.MemoryOnePlayer):
    """
    A generic reactive player. Defined by 2 probabilities conditional on the
    opponent's last move (P(C|C), P(C|D)) and the opening probability.
    """

    name = "Reactive Player"

    def __init__(self, probabilities):
        self.initial = np.random.choice(
            [axl.Action.C, axl.Action.D],
            p=(probabilities[0], 1 - probabilities[0]),
        )
        self.four_vector = (*probabilities[1:], *probabilities[1:])
        super().__init__(self.four_vector, self.initial)


def get_score_for_last_n_turns(
    player, opponents, num_of_interactions, delta, seed=None
):
    """Score an individual against their opponents. The score is based on the
    last number of interactions.

    The individual is being scored on a probabilistic ending against each
    opponent. The match lengths can vary at this point.

    Parameters
    ----------
    player : tuple
        A reactive player tuple
    opponents : list of tuples
        A list of reactive opponents
    num_of_interactions : int
        The number of scores the player remembers
    delta : float
        The probability of the match continuing.

    Returns
    -------
    float
        The sum of the scores per turns the player achieved against the opponents.
    """
    score_per_turn = []
    for opponent in opponents:

        match = axl.Match(
            [ReactivePlayer(player), ReactivePlayer(opponent)],
            prob_end=(1 - delta),
            seed=seed,
        )
        _ = match.play()

        scores, _ = zip(*match.scores()[-num_of_interactions:])
        score_per_turn.append(sum(scores) / len(scores))

    return sum(score_per_turn) / len(opponents)


def get_opponents_of_mutant(
    resident, mutant, num_of_opponents, N, population, random_state
):
    """Returns the list of opponents for the mutant."""
    play_against_role_model = False
    opponents_of_mutant = []

    for interactions in range(num_of_opponents):
        probability_interacting_with_role_model = (
            1 / (N - 1 - interactions)
        ) * (1 - int(play_against_role_model))

        if probability_interacting_with_role_model > random_state.random():

            play_against_role_model = True
            opponents_of_mutant.append(resident)

        else:

            p = (
                N - population[mutant] - opponents_of_mutant.count(resident)
            ) / (N - 1 - len(opponents_of_mutant))
            choice = np.random.choice([1, 0], p=(p, 1 - p))

            if choice == 1:
                opponents_of_mutant.append(resident)
            else:
                opponents_of_mutant.append(mutant)

    return opponents_of_mutant, play_against_role_model


def get_opponents_of_resident(
    resident, mutant, play_against_role_model, num_of_opponents, N, population
):
    opponents_of_resident = []
    if play_against_role_model:
        opponents_of_resident.append(mutant)

    while len(opponents_of_resident) < num_of_opponents:

        p = (population[mutant] - opponents_of_resident.count(mutant)) / (
            N - 1 - len(opponents_of_resident)
        )

        choice = np.random.choice([1, 0], p=(1 - p, p))
        if choice == 1:
            opponents_of_resident.append(resident)
        else:
            opponents_of_resident.append(mutant)

    return opponents_of_resident


def simulation(
    resident,
    N,
    delta,
    strength_of_selection,
    num_of_steps,
    num_of_opponents,
    num_of_interactions,
    seed,
    filename,
):

    population = {resident: N}
    random_ = np.random.RandomState(seed)

    if os.path.exists(filename):
        os.remove(filename)

    for t in tqdm.tqdm(range(num_of_steps)):

        # A mutation occurs when the population consists
        # only by residents.
        if N in population.values():
            mutant, population = introduce_mutant(population, resident, random_)

        else:
            # The invasion phase
            (
                opponents_of_mutant,
                play_again_role_model,
            ) = get_opponents_of_mutant(
                resident, mutant, num_of_opponents, N, population, random_
            )

            opponents_of_resident = get_opponents_of_resident(
                resident,
                mutant,
                play_again_role_model,
                num_of_opponents,
                N,
                population,
            )
            seeds = [random_.randint(10000) for _ in range(2)]
            mutant_score = get_score_for_last_n_turns(
                mutant,
                opponents_of_mutant,
                num_of_interactions,
                delta,
                seeds[0],
            )
            resident_score = get_score_for_last_n_turns(
                resident,
                opponents_of_resident,
                num_of_interactions,
                delta,
                seeds[1],
            )
            imitation_probability = 1 / (
                1
                + np.exp(
                    -strength_of_selection * (mutant_score - resident_score)
                )
            )

            if random_.random() < imitation_probability:
                population = {
                    resident: population[resident] - 1,
                    mutant: population[mutant] + 1,
                }

            else:
                population = {
                    resident: population[resident] + 1,
                    mutant: population[mutant] - 1,
                }

            # A mutant that takes over the population,
            # becomes the resident.
            if population[mutant] == N:
                resident = mutant

            data = (
                [t]
                + list(population.keys())
                + list(population.values())
                + [num_of_interactions]
                + [num_of_opponents]
            )
            with open(filename, "a") as textfile:
                textfile.write(
                    ",".join(
                        [
                            str(elem).replace("(", "").replace(")", "")
                            for elem in data
                        ]
                    )
                    + "\n"
                )
            textfile.close()
    return population


if __name__ == "__main__":  # pragma: no cover

    number_of_process = multiprocessing.cpu_count()
    p = multiprocessing.Pool(int(number_of_process))

    residents = {"ALLD": (0, 0, 0), "GTFT": (1, 1, 1 / 3)}
    residents_names = ["ALLD", "GTFT"]

    N = 100
    delta = 0.999
    strength_of_selection = 1
    number_of_steps = 10 ** 10

    opponents = range(2, 6)
    interactions = range(2, 6)
    parameters = itertools.product(opponents, interactions, residents_names)

    _ = p.starmap(
        simulation,
        [
            (
                residents[name],
                N,
                delta,
                strength_of_selection,
                number_of_steps,
                num_of_opponents,
                num_of_interactions,
                0,
                f"data/simulations_up_to_five/opponents_{num_of_opponents}_interactions_{num_of_interactions}.csv",
            )
            for num_of_opponents, num_of_interactions, name in parameters
        ],
    )
