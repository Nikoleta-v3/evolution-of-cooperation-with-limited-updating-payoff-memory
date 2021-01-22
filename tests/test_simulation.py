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


def test_stochastic_scores_initialization():
    stochastic_scores = evol_dynamics.StochasticScores(
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
    )

    assert isinstance(stochastic_scores.resident, list)
    assert isinstance(stochastic_scores.mutant, list)
    assert stochastic_scores.delta == delta
    assert stochastic_scores.population_size == population_size
    assert stochastic_scores.number_of_mutants == number_of_mutants
    assert stochastic_scores.repetitions == repetitions
    assert isinstance(stochastic_scores.random, np.random.RandomState)
    assert stochastic_scores.scoring_turns == 1


def test_stochastic_scores_initialization_with_scoring_turns():
    scoring_turns = 5
    stochastic_scores = evol_dynamics.StochasticScores(
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
        scoring_turns,
    )

    assert isinstance(stochastic_scores.resident, list)
    assert isinstance(stochastic_scores.mutant, list)
    assert stochastic_scores.delta == delta
    assert stochastic_scores.population_size == population_size
    assert stochastic_scores.number_of_mutants == number_of_mutants
    assert stochastic_scores.repetitions == repetitions
    assert isinstance(stochastic_scores.random, np.random.RandomState)
    assert stochastic_scores.scoring_turns == 5


def test_create_population():
    stochastic_scores = evol_dynamics.StochasticScores(
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
    )

    population = stochastic_scores.create_population()
    assert len(population) == population_size
    assert (
        len([member for member in population if member.name == "mutant"]) == 1
    )
    assert (
        len([member for member in population if member.name == "resident"]) == 1
    )
    assert len(
        [member for member in population if member.name == "generic"]
    ) == (population_size - 2)


def test_match_pairs():
    population_size = 100
    seed = 2
    random_state = np.random.RandomState(seed)

    stochastic_scores = evol_dynamics.StochasticScores(
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
    )

    population = stochastic_scores.create_population()
    pairs = stochastic_scores.match_pairs(population)

    assert isinstance(pairs, dict)
    assert isinstance(pairs["resident"], tuple)
    assert isinstance(pairs["mutant"], tuple)


def test_match_pairs_resident_plays_mutant():
    population_size = 10
    seed = 2
    random_state = np.random.RandomState(seed)

    stochastic_scores = evol_dynamics.StochasticScores(
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
    )

    population = stochastic_scores.create_population()
    pairs = stochastic_scores.match_pairs(population)

    assert isinstance(pairs, dict)
    assert isinstance(pairs["resident"], tuple)
    with pytest.raises(KeyError):
        assert pairs["mutant"]


def test_match_pairs_mutant_plays_role_model():
    population_size = 10
    seed = 1
    random_state = np.random.RandomState(seed)

    stochastic_scores = evol_dynamics.StochasticScores(
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
    )

    population = stochastic_scores.create_population()
    pairs = stochastic_scores.match_pairs(population)

    assert isinstance(pairs, dict)
    assert isinstance(pairs["mutant"], tuple)
    with pytest.raises(KeyError):
        assert pairs["resident"]


def test_score():
    population_size = 10
    repetitions = 1
    seed = 1
    random_state = np.random.RandomState(seed)
    mutant = [0, 0, 0]
    resident = [1, 1, 1]

    stochastic_scores = evol_dynamics.StochasticScores(
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
    )

    population = stochastic_scores.create_population()
    scores = stochastic_scores.get_scores(population)
    assert isinstance(scores, dict)
    assert scores["mutant"] == 5.0
    assert scores["resident"] == 0.0


def test_theoretical_utility_example_one():
    mutant = (0, 0, 0)
    resident = (1, 1, 1)
    delta = 0.999
    number_of_mutants = 1
    population_size = 5
    scores = evol_dynamics.theoretical_utility(
        mutant, resident, delta, number_of_mutants, population_size
    )

    assert scores[0] == 5.0
    assert scores[1] == 2.25


def test_scoring_turns_five():
    population_size = 2
    number_of_mutants = 1
    repetitions = 1
    seed = 5
    random_state = np.random.RandomState(seed)
    scoring_turns = 5

    resident = [1, 1, 0]
    mutant = [0, 1, 0]

    stochastic_scores = evol_dynamics.StochasticScores(
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
        scoring_turns,
    )

    population = stochastic_scores.create_population()
    scores = stochastic_scores.get_scores(population)

    assert set(scores.values()) == {2.0, 3.0}


def test_scoring_turns():
    population_size = 10
    repetitions = 1
    number_of_mutants = 3
    seed = 6
    random_state = np.random.RandomState(seed)
    scoring_turns = 5
    delta = 0.7

    resident = [0, 1, 1]
    mutant = [1, 0, 1]

    stochastic_scores = evol_dynamics.StochasticScores(
        resident,
        mutant,
        delta,
        population_size,
        number_of_mutants,
        repetitions,
        random_state,
        scoring_turns,
    )

    population = stochastic_scores.create_population()
    scores = stochastic_scores.get_scores(population)

    assert isinstance(scores, dict)