import random

import numpy as np

# import tqdm
import copy

import evol_dynamics

import time


def payoffs_expected(resident, mutant, population, payoffs, delta, N):

    resident_payoff = sum(
        [
            evol_dynamics.expected_distribution_last_round(
                resident, opponent, delta
            )
            @ payoffs
            * (population[opponent] - int(resident == opponent))
            for opponent in population.keys()
        ]
    ) / (N - 1)

    mutant_payoff = sum(
        [
            evol_dynamics.expected_distribution_last_round(
                mutant, opponent, delta
            )
            @ payoffs
            * (population[opponent] - int(mutant == opponent))
            for opponent in population.keys()
        ]
    ) / (N - 1)

    return resident_payoff, mutant_payoff


def payoffs_last_round(resident, mutant, population, payoffs, delta):

    population_cp = copy.deepcopy(population)

    opponent = random.sample(
        [key for key in population.keys() for _ in range(population[key])], 1
    )[0]
    population_cp[opponent] -= 1

    resident_payoff = (
        evol_dynamics.expected_distribution_last_round(
            resident, opponent, delta
        )
        @ payoffs
    )

    opponent = random.sample(
        [key for key in population.keys() for _ in range(population[key])], 1
    )[0]
    mutant_payoff = (
        evol_dynamics.expected_distribution_last_round(mutant, opponent, delta)
        @ payoffs
    )

    return resident_payoff, mutant_payoff


def simulation(
    N,
    delta,
    beta,
    mutation,
    number_of_steps,
    payoffs,
    mode,
    filename,
    seed=10,
    starting_resident=(0, 0, 0),
):

    data = [0, *payoffs, N, delta, beta, mutation, mode, *starting_resident, 0]

    with open(filename, "w") as textfile:
        textfile.write(",".join([str(elem) for elem in data]) + "\n")
    textfile.close()

    population = {starting_resident: N}
    random.seed(seed)

    for i in range(1, number_of_steps + 1):

        if random.random() < mutation:
            to_mutate = random.sample(
                [
                    key
                    for key in population.keys()
                    for _ in range(population[key])
                ],
                1,
            )
            population[to_mutate[0]] -= 1
            population[tuple(random.random() for _ in range(3))] = 1

        else:

            resident, mutant = random.sample(
                [
                    key
                    for key in population.keys()
                    for _ in range(population[key])
                ],
                2,
            )

            if mode == "expected":

                resident_payoff, mutant_payoff = payoffs_expected(
                    resident, mutant, population, payoffs, delta, N
                )

            if mode == "last_round":

                resident_payoff, mutant_payoff = payoffs_last_round(
                    resident, mutant, population, payoffs, delta
                )

            fermi = 1 / (
                1 + np.exp(float(-beta * (mutant_payoff - resident_payoff)))
            )

            if random.random() < fermi:
                population[resident] -= 1
                population[mutant] += 1

            for member in population.items():

                data = [
                    i,
                    *payoffs,
                    N,
                    delta,
                    beta,
                    mutation,
                    mode,
                    *member[0],
                    member[1],
                ]

                with open(filename, "a") as textfile:
                    textfile.write(
                        ",".join([str(elem) for elem in data]) + "\n"
                    )
                textfile.close()

        population = {key: val for key, val in population.items() if val != 0}
    return population


if __name__ == "__main__":  # pragma: no cover
    start_time = time.time()
    N = 100
    delta = 0.999
    beta = 1
    mutation = 0.01
    number_of_steps = 10 ** 4
    payoffs = np.array([2, -1, 3, 0])
    mode = "expected"
    filename = "mutation_expected.csv"
    seed = 10
    starting_resident = (0, 0, 0)

    _ = simulation(
        N,
        delta,
        beta,
        mutation,
        number_of_steps,
        payoffs,
        mode,
        filename,
        seed,
        starting_resident,
    )

    print("--- %s seconds ---" % (time.time() - start_time))
