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


class StochasticScores:
    def __init__(
        self,
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
        scoring_turns=1,
        number_of_opponents=1,
    ):
        self.resident = resident
        self.mutant = mutant
        self.delta = delta
        self.population_size = population_size
        self.number_of_mutants = number_of_mutants
        self.repetitions = repetitions
        self.random = random_state
        self.scoring_turns = scoring_turns

    def create_population(self):
        population = [
            ReactivePlayer(self.resident, role="resident"),
            ReactivePlayer(self.mutant, role="mutant"),
        ]

        population += [
            ReactivePlayer(self.resident, role="generic")
            for _ in range(self.population_size - self.number_of_mutants - 1)
        ]
        population += [
            ReactivePlayer(self.mutant, role="generic")
            for _ in range(self.number_of_mutants - 1)
        ]

        self.random.shuffle(population)
        return population

    def match_pairs(self, population):
        pairs = {}
        while len(population) > 0:
            player = population.pop()
            index = self.random.randint(low=0, high=len(population))
            opponent = population.pop(index)

            if player.name in ["resident", "mutant"] and opponent.name in [
                "resident",
                "mutant",
            ]:
                pairs[player.name] = (player, opponent)
                return pairs

            if player.name in ["resident", "mutant"]:
                pairs[player.name] = (player, opponent)

            if opponent.name in ["resident", "mutant"]:
                pairs[opponent.name] = (opponent, player)

        return pairs

    def get_scores(self, population):
        scores = {"mutant": 0, "resident": 0}

        for _ in range(self.repetitions):
            population_copy = copy.deepcopy(population)
            pairs = self.match_pairs(population_copy)

            if len(pairs) == 1:
                match = axl.Match(*pairs.values(), prob_end=(1 - self.delta))
                _ = match.play()

                for i, player in enumerate(*pairs.values()):
                    scores[player.name] += (
                        sum(
                            [
                                s[i]
                                for s in match.scores()[-self.scoring_turns :]
                            ]
                        )
                        / self.scoring_turns
                    )
            else:
                for pair in pairs:
                    match = axl.Match(pairs[pair], prob_end=(1 - self.delta))
                    _ = match.play()

                    scores[pair] += (
                        sum(
                            [
                                s[0]
                                for s in match.scores()[-self.scoring_turns :]
                            ]
                        )
                        / self.scoring_turns
                    )

        return {k: v / self.repetitions for k, v in scores.items()}


def theoretical_utility(
    mutant, resident, delta, number_of_mutants, population_size
):
    combinations = itertools.product([mutant, resident], repeat=2)
    vMM, vMR, vRM, vRR = [
        evol_dynamics.expected_distribution_last_round(p1, p2, delta)
        for p1, p2 in combinations
    ]

    x = evol_dynamics.evolution.probability_of_receiving_payoffs(
        vMM, vMR, vRM, vRR, number_of_mutants, population_size
    )

    payoff_vector = np.array([3, 0, 5, 1])

    rhos = np.array([[payoff_vector[i] for i in range(4)] for j in range(4)])

    return round(sum(sum(x * rhos)), 3), round(sum(sum(x * rhos.T)), 3)


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
