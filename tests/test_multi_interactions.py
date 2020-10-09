from importlib.machinery import SourceFileLoader

import axelrod as axl

import numpy as np

mutli = SourceFileLoader("mutli", "src/multi_interactions.py").load_module()


def test_introduce_mutant():
    N = 10
    resident = (1, 1, 1)
    population = {resident: N}
    random_ = np.random.RandomState(0)

    mutant, population = mutli.introduce_mutant(population, resident, random_)
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

    player = mutli.ReactivePlayer((0, 0, 0))
    assert player.name == 'Reactive Player'
    assert player.initial == axl.Action.D
    assert player.four_vector == (0, 0, 0, 0)

    opponent = mutli.ReactivePlayer((1, 1, 0))
    assert opponent.name == 'Reactive Player'
    assert opponent.initial == axl.Action.C
    assert opponent.four_vector == (1, 0, 1, 0)

    match = axl.Match([player, opponent], turns=5)
    results = match.play()

    assert results[0] == (axl.Action.D, axl.Action.C)
    assert results[-1] == (axl.Action.D, axl.Action.D)