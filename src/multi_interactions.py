import numpy as np
import random

import axelrod as axl


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
    population.append({resident: population[-1][resident] - 1, mutant: 1})

    return mutant, population


def get_score_for_last_n_turns(player, opponents, num_of_interactions, delta):
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
            [axl.ReactivePlayer(player), axl.ReactivePlayer(opponent)],
            prob_end=(1 - delta),
        )
        _ = match.play()

        scores, _ = zip(*match.scores()[-num_of_interactions:])
        score_per_turn.append(sum(scores) / num_of_interactions)

    return sum(score_per_turn) / len(opponents)
