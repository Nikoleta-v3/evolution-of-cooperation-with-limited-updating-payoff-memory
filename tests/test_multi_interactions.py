import os
from importlib.machinery import SourceFileLoader

import axelrod as axl
import numpy as np
import pandas as pd
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


def test_get_opponents_of_resident_one_mutant_interaction_true():

    resident = (0, 0, 0)
    N = 6
    population = {resident: N}
    random_ = np.random.RandomState(0)
    play_against_role_model = True

    mutant, population = multi.introduce_mutant(population, resident, random_)

    opponents = multi.get_opponents_of_resident(
        resident, mutant, play_against_role_model, 4, N, population
    )

    assert sum([mutant == opponent for opponent in opponents]) == 1


def test_get_opponents_of_resident_two_mutants_interaction_true():

    resident = (0, 0, 0)
    N = 6
    population = {resident: N}
    random_ = np.random.RandomState(0)
    play_against_role_model = True

    mutant, population = multi.introduce_mutant(population, resident, random_)
    population = {
        resident: population[resident] - 1,
        mutant: population[mutant] + 1,
    }

    opponents = multi.get_opponents_of_resident(
        resident, mutant, play_against_role_model, 5, N, population
    )

    assert sum([mutant == opponent for opponent in opponents]) == 2


def test_get_opponents_of_resident_three_mutants_interaction_true():

    resident = (0, 0, 0)
    N = 6
    population = {resident: N}
    random_ = np.random.RandomState(0)
    play_against_role_model = True

    mutant, population = multi.introduce_mutant(population, resident, random_)
    population = {
        resident: population[resident] - 2,
        mutant: population[mutant] + 2,
    }

    opponents = multi.get_opponents_of_resident(
        resident, mutant, play_against_role_model, 5, N, population
    )

    assert sum([mutant == opponent for opponent in opponents]) == 3


def test_resident_opponents_error_when_interactions_exceed_population_size():

    resident = (0, 0, 0)
    N = 6
    population = {resident: N}
    interactions = N
    play_against_role_model = False

    # get different mutant each time tests run
    seed = np.random.randint(100)
    random_ = np.random.RandomState(seed)

    mutant, population = multi.introduce_mutant(population, resident, random_)

    with pytest.raises(ZeroDivisionError):
        multi.get_opponents_of_resident(
            resident,
            mutant,
            play_against_role_model,
            interactions,
            N,
            population,
        )


def test_simulation_for_one_run():
    resident = (1, 1, 1)
    N = 6
    delta = 0.999
    strength_of_selection = 1
    num_of_steps = 1
    num_of_opponents = 2
    num_of_interactions = 2
    seed = 0
    filename = "test_multi_interactions_simulation.csv"

    assert os.path.exists(filename) == False

    population = multi.simulation(
        resident,
        N,
        delta,
        strength_of_selection,
        num_of_steps,
        num_of_opponents,
        num_of_interactions,
        seed,
        filename,
    )

    assert isinstance(population, dict)
    assert len(population.keys()) == 2
    assert list(population.values()) == [5, 1]

    assert os.path.exists(filename) == False


def test_simulation_for_multiple_runs():
    resident = (1, 1, 1)
    N = 6
    delta = 0.999
    strength_of_selection = 1
    num_of_steps = 10
    num_of_opponents = 2
    num_of_interactions = 2
    seed = 0
    filename = "test_multi_interactions_simulation.csv"

    assert os.path.exists(filename) == False

    population = multi.simulation(
        resident,
        N,
        delta,
        strength_of_selection,
        num_of_steps,
        num_of_opponents,
        num_of_interactions,
        seed,
        filename,
    )

    assert isinstance(population, dict)

    assert os.path.exists(filename) == True
    df = pd.read_csv(filename)
    df.columns = [
        "timestep",
        "$y_1$",
        "$p_1$",
        "$q_1$",
        "$y_2$",
        "$p_2$",
        "$q_2$",
        "resident count",
        "mutant count",
        "num of interactions",
        "num of opponents",
    ]

    assert len(df.columns) == 11
    assert df.iloc[-1]["num of interactions"] == num_of_interactions

    os.remove(filename)


def test_simulation_previous_experiment_file_is_delete():
    """
    This ensures that the results on new experiment are not appended to a file
    of previous results.
    """
    filename = "tests/example_multi_simulation.csv"
    resident = (1, 1, 1)
    N = 6
    delta = 0.999
    strength_of_selection = 1
    num_of_steps = 10
    num_of_opponents = 2
    num_of_interactions = 2
    seed = 0

    _ = multi.simulation(
        resident,
        N,
        delta,
        strength_of_selection,
        num_of_steps,
        num_of_opponents,
        num_of_interactions,
        seed,
        filename,
    )

    df = pd.read_csv(filename, header=None)

    assert len(df.columns) == 11
    assert len(df.values) <= num_of_steps


def test_mutant_becomes_the_resident():

    resident = (1, 1, 1)
    N = 6
    delta = 0.999
    strength_of_selection = 1
    num_of_steps = 10
    num_of_opponents = 2
    num_of_interactions = 1
    seed = 2
    filename = "test_multi_interactions_simulation.csv"

    population = multi.simulation(
        resident,
        N,
        delta,
        strength_of_selection,
        num_of_steps,
        num_of_opponents,
        num_of_interactions,
        seed,
        filename,
    )

    expected_resident = (
        0.43599490214200376,
        0.025926231827891333,
        0.5496624778787091,
    )

    assert (resident in population) == False
    assert expected_resident in population

    os.remove(filename)
