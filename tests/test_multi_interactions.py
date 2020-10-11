from importlib.machinery import SourceFileLoader

import axelrod as axl

import numpy as np
import pytest

multi = SourceFileLoader("mutli", "src/multi_interactions.py").load_module()


def test_introduce_mutant():
    N = 10
    resident = (1, 1, 1)
    population = {resident: N}
    random_ = np.random.RandomState(0)

    mutant, population = multi.introduce_mutant(population, resident, random_)
    expected_mutant = [
        0.5488135039273248,
        0.7151893663724195,
        0.6027633760716439,
    ]

    assert len(population) == 2
    assert population[resident] == 9
    assert set(expected_mutant) == set(mutant)
    assert population[mutant] == 1


def test_reactive_player():

    player = multi.ReactivePlayer((0, 0, 0))
    assert player.name == "Reactive Player"
    assert player.initial == axl.Action.D
    assert player.four_vector == (0, 0, 0, 0)

    opponent = multi.ReactivePlayer((1, 1, 0))
    assert opponent.name == "Reactive Player"
    assert opponent.initial == axl.Action.C
    assert opponent.four_vector == (1, 0, 1, 0)

    match = axl.Match([player, opponent], turns=5)
    results = match.play()

    assert results[0] == (axl.Action.D, axl.Action.C)
    assert results[-1] == (axl.Action.D, axl.Action.D)


def test_get_score_for_last_n_turns_last_two_interactions():
    player = (1, 1, 0)
    opponents = [(1, 1, 1), (0, 1, 1), (0, 0, 0), (0, 1, 0)]

    score = multi.get_score_for_last_n_turns(
        player, opponents, num_of_interactions=2, delta=0.90, seed=1
    )

    assert score == (sum([3.0, 3.0, 1.0, 2.5]) / 4)


def test_get_score_for_last_n_turns_last_hundred_interactions():
    player = (1, 1, 0)
    opponents = [(1, 1, 1), (0, 1, 1), (0, 0, 0), (0, 1, 0)]

    score = multi.get_score_for_last_n_turns(
        player, opponents, num_of_interactions=100, delta=0.90, seed=1
    )

    assert np.isclose(score, (sum([3.0, 2.83333, 0.83333, 2.5]) / 4))


def test_mutant_opponents_single_mutant():
    """
    The mutant never interacts with another mutant when there is a single mutant in the population.
    """
    resident = (0, 0, 0)
    N = 6
    population = {resident: N}
    interactions = 5

    # get different mutant each time tests run
    seed = np.random.randint(100)
    random_ = np.random.RandomState(seed)

    mutant, population = multi.introduce_mutant(population, resident, random_)

    opponents, _ = multi.get_opponents_of_mutant(
        resident, mutant, interactions, N, population, random_
    )

    assert mutant not in opponents


def test_mutant_opponents_error_when_interactions_exceed_population_size():

    resident = (0, 0, 0)
    N = 6
    population = {resident: N}
    interactions = N

    # get different mutant each time tests run
    seed = np.random.randint(100)
    random_ = np.random.RandomState(seed)

    mutant, population = multi.introduce_mutant(population, resident, random_)

    with pytest.raises(ZeroDivisionError):
        multi.get_opponents_of_mutant(
            resident, mutant, interactions, N, population, random_
        )


def test_mutant_opponents_interacts_with_all_residents():

    resident = (0, 0, 0)
    N = 6
    population = {resident: N}
    interactions = 5

    # get different mutant each time tests run
    seed = np.random.randint(100)
    random_ = np.random.RandomState(seed)

    mutant, population = multi.introduce_mutant(population, resident, random_)

    opponents, play_again_role_model = multi.get_opponents_of_mutant(
        resident, mutant, interactions, N, population, random_
    )

    for opponent in opponents:
        assert opponent == resident
    assert play_again_role_model


def test_that_mutant_interacts_with_other_mutant_and_role_model():
    resident = (0, 0, 0)
    N = 6
    population = {resident: N}
    random_ = np.random.RandomState(0)

    mutant, population = multi.introduce_mutant(population, resident, random_)

    population = {
        resident: population[resident] - 1,
        mutant: population[mutant] + 1,
    }

    opponents, interacts = multi.get_opponents_of_mutant(
        resident, mutant, 5, N, population, random_
    )

    assert interacts
    assert sum([mutant == opponent for opponent in opponents]) == 1
    assert sum([resident == opponent for opponent in opponents]) == 4
