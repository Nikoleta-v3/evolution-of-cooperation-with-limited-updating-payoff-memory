import copy
import itertools
import sys

import axelrod as axl
import numpy as np
import tqdm

import evol_dynamics


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

    return probabilities_of_role_mode, probabilities_of_learner


if __name__ == "__main__":  # pragma: no cover
    filename = "data/soup_for_theoretical_utility.csv"
    number_of_checks = 10000
    delta = 0.999

    seed = int(sys.argv[1])
    number_of_repetitions = int(sys.argv[2])
    random_state = np.random.RandomState(seed)

    for i in tqdm.tqdm(range(number_of_checks)):
        mutant = [np.random.random() for _ in range(3)]
        resident = [np.random.random() for _ in range(3)]
        population_size = 2 * (np.random.randint(5, 100) // 2)
        number_of_mutants = np.random.randint(1, population_size)

        stochastic_scores = evol_dynamics.StochasticScores(
            resident,
            mutant,
            delta,
            population_size,
            number_of_mutants,
            number_of_repetitions,
            random_state,
        )

        population = stochastic_scores.create_population()
        simulation_scores = stochastic_scores.get_scores(population)
        theoretical_scores = evol_dynamics.theoretical_utility(
            mutant, resident, delta, number_of_mutants, population_size
        )

        data = [
            i,
            number_of_repetitions,
            *mutant,
            *resident,
            population_size,
            number_of_mutants,
            delta,
            *simulation_scores.values(),
            *theoretical_scores,
        ]

        with open(filename, "a") as textfile:
            textfile.write(",".join([str(elem) for elem in data]) + "\n")
        textfile.close()
