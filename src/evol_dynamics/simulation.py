import copy
import itertools
import sys

import axelrod as axl
import numpy as np
import tqdm

import evol_dynamics

from collections import Counter


class ReactivePlayer(axl.MemoryOnePlayer):
    """
    A generic reactive player. Defined by 2 probabilities conditional on the
    opponent's last move (P(C|C), P(C|D)) and the opening probability.
    """

    def __init__(self, probabilities, role):

        self.initial = np.random.choice(
            [axl.Action.C, axl.Action.D],
            p=(probabilities[0], 1 - probabilities[0]),
        )
        self.four_vector = (*probabilities[1:], *probabilities[1:])
        self.name = role

        super().__init__(self.four_vector, self.initial)


def create_population(population_size, number_of_mutants, random_state):

    population = ["role-model", "learner"]

    population += [
        "resident" for _ in range(population_size - number_of_mutants - 1)
    ]

    population += ["mutant" for _ in range(number_of_mutants - 1)]

    random_state.shuffle(population)
    assert len(population) == population_size
    return population


def match_pairs(
    population_size,
    number_of_mutants,
    random_state,
    num_of_opponents,
):
    population = create_population(
        population_size, number_of_mutants, random_state
    )

    pairs = {i: [] for i in range(population_size)}

    for _ in range(num_of_opponents):

        population_numbers = list(range(population_size))
        random_state.shuffle(population_numbers)

        while len(population_numbers) > 0:
            player = population_numbers.pop()
            opponent = random_state.choice(
                [i for i in population_numbers if i not in pairs[player]]
            )
            population_numbers.remove(opponent)

            pairs[player] += [opponent]
            pairs[opponent] += [player]

    pairs_to_types = {
        population[i]: [population[j] for j in pairs[i]] for i in pairs.keys()
    }

    return pairs_to_types


def get_probabilities_for_opponents(
    num_of_repetitions,
    population_size,
    number_of_mutants,
    random_state,
    num_of_opponents,
):
    role_model_pairs = []
    learner_pairs = []

    for _ in range(num_of_repetitions):

        pairs = match_pairs(
            population_size, number_of_mutants, random_state, num_of_opponents
        )
        role_model_pairs.append(pairs["role-model"])
        learner_pairs.append(pairs["learner"])

    # ToDo change this to depend on `num_of_opponents`
    probabilities_of_role_mode = {
        "learner": 0,
        "resident": 0,
        "mutant": 0,
        "role-model": 0,
        "resident-resident": 0,
        "mutant-resident": 0,
        "learner-resident": 0,
        "role-model-resident": 0,
        "resident-mutant": 0,
        "mutant-mutant": 0,
        "learner-mutant": 0,
        "role-model-mutant": 0,
        "resident-learner": 0,
        "mutant-learner": 0,
        "learner-learner": 0,
        "role-model-learner": 0,
        "resident-role-model": 0,
        "mutant-role-model": 0,
        "learner-role-model": 0,
        "role-model-role-model": 0,
    }

    probabilities_of_learner = {
        "learner": 0,
        "resident": 0,
        "mutant": 0,
        "role-model": 0,
        "resident-resident": 0,
        "mutant-resident": 0,
        "learner-resident": 0,
        "role-model-resident": 0,
        "resident-mutant": 0,
        "mutant-mutant": 0,
        "learner-mutant": 0,
        "role-model-mutant": 0,
        "resident-learner": 0,
        "mutant-learner": 0,
        "learner-learner": 0,
        "role-model-learner": 0,
        "resident-role-model": 0,
        "mutant-role-model": 0,
        "learner-role-model": 0,
        "role-model-role-model": 0,
    }

    for pair in role_model_pairs:
        probabilities_of_role_mode[pair[0]] += 1 / num_of_repetitions
        probabilities_of_role_mode["-".join(pair)] += 1 / num_of_repetitions

    for pair in learner_pairs:
        probabilities_of_learner[pair[0]] += 1 / num_of_repetitions
        probabilities_of_learner["-".join(pair)] += 1 / num_of_repetitions

    return probabilities_of_learner, probabilities_of_role_mode


def stationary_for_16_states(player, opponent, delta):
    """
    The probability of being at each state in steady state.
    """
    v_zero = np.array(
        evol_dynamics.expected_distribution_opening_round(player, opponent)
    )
    M = evol_dynamics.markov_chain_for_reactive_strategies(player, opponent)
    rhs = np.dot(v_zero, np.linalg.pinv((np.eye(4) - delta * M)))

    ss = []
    for i, row in enumerate(M):
        for m in row:
            ss.append((1 - delta) * m * (delta ** 2) * rhs[i])

    return np.array(ss)


def simulated_states(
    player, opponent, delta, number_of_repetitions, rounds_of_history
):

    history_two_to_state = {
        "CCCC": "RR",
        "CCCD": "RS",
        "CCDC": "RT",
        "CCDD": "RP",
        "CDCC": "SR",
        "CDCD": "SS",
        "CDDC": "ST",
        "CDDD": "SP",
        "DCCC": "TR",
        "DCCD": "TS",
        "DCDC": "TT",
        "DCDD": "TP",
        "DDCC": "PR",
        "DDCD": "PS",
        "DDDC": "PT",
        "DDDD": "PP",
    }

    history_one_to_state = {
        "CC": "R",
        "CD": "S",
        "DC": "T",
        "DD": "P",
    }
    ss = []
    for _ in range(number_of_repetitions):

        match = axl.Match(
            [
                evol_dynamics.ReactivePlayer(player, role="mutant"),
                evol_dynamics.ReactivePlayer(opponent, role="resident"),
            ],
            prob_end=(1 - delta),
        )
        _ = match.play()

        histories = match.result[-rounds_of_history:]
        histories_in_characters = "".join(
            [str(v) for history in histories for v in history]
        )
        try:
            ss.append(history_two_to_state[histories_in_characters])
        except KeyError:
            pass

        last_round = [match.result[-1]]
        last_round_in_characters = "".join(
            [str(v) for history in last_round for v in history]
        )
        try:
            ss.append(history_one_to_state[last_round_in_characters])
        except KeyError:
            pass

    states = {
        name: 0
        for name in list(history_two_to_state.values())
        + list(history_one_to_state.values())
    }
    for key, value in zip(Counter(ss).keys(), Counter(ss).values()):
        states[key] = value / number_of_repetitions

    return states
