import axelrod as axl
import numpy as np
import pytest

import evol_dynamics


resident = [np.random.random() for _ in range(3)]
mutant = [np.random.random() for _ in range(3)]
delta = 0.999
population_size = 10
number_of_mutants = 3
repetitions = 100
seed = 5
random_state = np.random.RandomState(seed)


def test_reactive_player():

    player = evol_dynamics.ReactivePlayer((0, 0, 0), role="resident")
    assert player.initial == axl.Action.D
    assert player.four_vector == (0, 0, 0, 0)
    assert player.name == "resident"

    opponent = evol_dynamics.ReactivePlayer((1, 1, 0), role="generic")
    assert opponent.initial == axl.Action.C
    assert opponent.four_vector == (1, 0, 1, 0)
    assert opponent.name == "generic"

    match = axl.Match([player, opponent], turns=5)
    results = match.play()

    assert results[0] == (axl.Action.D, axl.Action.C)
    assert results[-1] == (axl.Action.D, axl.Action.D)


def test_create_population():

    population = evol_dynamics.create_population(
        population_size, number_of_mutants, random_state
    )

    assert len(population) == population_size
    assert len([member for member in population if member == "role-model"]) == 1
    assert len([member for member in population if member == "learner"]) == 1
    assert len([member for member in population if member == "resident"]) == (
        population_size - 1 - number_of_mutants
    )
    assert len([member for member in population if member == "mutant"]) == (
        number_of_mutants - 1
    )


def test_match_pairs():
    population_size = 100
    seed = 2
    random_state = np.random.RandomState(seed)

    pairs = evol_dynamics.match_pairs(
        population_size, number_of_mutants, random_state
    )

    assert isinstance(pairs, dict)
    assert isinstance(pairs["role-model"], list)
    assert len(pairs["role-model"]) == 2
    assert len(pairs) == 4


def get_probabilities_for_opponents():
    num_of_repetitions = 100
    seed = 2
    random_state = np.random.RandomState(seed)
    num_of_opponents = 2

    probabilities_of_opponents = evol_dynamics.get_probabilities_for_opponents(
        num_of_repetitions,
        population_size,
        number_of_mutants,
        random_state,
        num_of_opponents,
    )

    assert isinstance(probabilities_of_opponents, dict)
    assert len(probabilities_of_opponents) == 29

    one_opponent_combinations = [
        "learner-role-model" "learner-resident-role-model-resident",
        "learner-resident-role-model-mutant",
        "learner-mutant-role-model-resident",
        "learner-mutant-role-model-mutant",
    ]

    assert (
        sum([probabilities_of_opponents[p] for p in one_opponent_combinations])
        == 1
    )


def test_stationary_for_16_states():
    player = [1, 1, 1]
    opponent = [0, 1, 1]
    delta = 0.999

    ss = evol_dynamics.stationary_for_16_states(player, opponent, delta)

    assert len(ss) == 16
    assert np.isclose(sum(ss), 1, atol=10 ** -2)


def test_simulated_states():
    player = [1, 1, 1]
    opponent = [0, 1, 1]
    delta = 0.999

    number_of_repetitions = 100
    rounds_of_history = 2

    ss = evol_dynamics.simulated_states(
        player, opponent, delta, number_of_repetitions, rounds_of_history
    )

    assert len(ss) == 20


def test_opponents_probabilities():
    number_of_repetitions = 1
    number_of_mutants = 10
    population_size = 100
    random_state = np.random.RandomState(0)
    num_of_opponents = 2

    simulated_opponents = evol_dynamics.get_probabilities_for_opponents(
        number_of_repetitions,
        population_size,
        number_of_mutants,
        random_state,
        num_of_opponents,
    )

    theoretical_opponents = (
        evol_dynamics.theoretical_probabilities_for_opponents(
            population_size, number_of_mutants
        )
    )

    assert simulated_opponents.keys() == theoretical_opponents.keys()


def test_theoretical_opponents_probabilities():
    N = 10
    k = 2

    probabilities = evol_dynamics.theoretical_probabilities_for_opponents(N, k)

    assert np.isclose(probabilities["learner-role-model"], 0.11111)
    assert np.isclose(
        probabilities["learner-resident-role-model-resident"], 0.66666
    )
    assert np.isclose(
        probabilities["learner-resident-role-model-mutant"], 0.11111
    )
    assert np.isclose(
        probabilities["learner-mutant-role-model-resident"], 0.11111
    )
    assert np.isclose(probabilities["learner-mutant-role-model-mutant"], 0.0)

    assert np.isclose(
        probabilities["learner-resident-resident-role-model-resident-resident"],
        0.416666,
    )
    assert np.isclose(
        probabilities["learner-resident-mutant-role-model-resident-resident"],
        0.083333,
    )
    assert np.isclose(
        probabilities["learner-resident-resident-role-model-mutant-resident"],
        0.083333,
    )
    assert np.isclose(
        probabilities[
            "learner-resident-role-model-role-model-resident-learner"
        ],
        0.095238,
    )
