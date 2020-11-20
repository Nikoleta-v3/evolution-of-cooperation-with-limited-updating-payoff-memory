import itertools
import os
from importlib.machinery import SourceFileLoader

import numpy as np
import pandas as pd
import sympy as sym

numerical = SourceFileLoader("numerical", "src/numerical.py").load_module()
formulation = SourceFileLoader(
    "formulation", "src/formulation.py"
).load_module()


def test_donation_game():
    c, b = sym.symbols("c, b")
    assert (b - c, -c, b, 0) == numerical.donation_game(c, b)
    assert (2, -1, 3, 0) == numerical.donation_game(1, 3)


def test_snowdrift_game():
    c, b = sym.symbols("c, b")
    assert ((b - c) / 2, (b / 2) - c, b / 2, 0) == numerical.snowdrift_game(
        c, b
    )
    assert (1, 0, 2, 0) == numerical.snowdrift_game(2, 4)


def test_stag_hunt():
    assert numerical.stag_hunt_game() == (3, 0, 2, 1)


def test_harmony_game():
    assert numerical.harmony_game() == (3, 2, 1, 0)


def test_reshape_data():
    df = pd.DataFrame(
        np.random.random(size=(10, 13)), columns=list("RSTPNdbmcsypq")
    )

    ps, qs = numerical._reshape_data(df)

    assert type(ps) == tuple
    assert type(qs) == tuple
    assert len(qs) <= 10
    assert len(ps) <= 10


def test_simulation():

    filename = "test_simulation.csv"
    assert os.path.exists(filename) == False

    _ = numerical.main(
        10,
        delta=0.999,
        beta=1,
        number_of_steps=1,
        payoffs=numerical.donation_game(1, 3),
        mode="expected",
        filename=filename,
        seed=0,
        starting_resident=(0, 0, 0),
    )
    assert os.path.exists(filename) == True

    df = pd.read_csv(filename, header=None)

    assert len(df.columns) == 13
    assert len(df.values) == 2
    assert df.values[0][7] == "expected"

    os.remove(filename)


def test_simulation_stochastic():

    filename = "test_simulation.csv"
    assert os.path.exists(filename) == False

    _ = numerical.main(
        10,
        delta=0.999,
        beta=1,
        number_of_steps=1,
        payoffs=numerical.donation_game(1, 3),
        mode="stochastic",
        filename=filename,
        seed=0,
        starting_resident=(0, 0, 0),
    )
    assert os.path.exists(filename) == True

    df = pd.read_csv(filename, header=None)

    assert len(df.columns) == 13
    assert len(df.values) == 2
    assert df.values[0][7] == "stochastic"

    os.remove(filename)


def test_simulation_success():

    filename = "test_simulation.csv"
    assert os.path.exists(filename) == False

    _ = numerical.main(
        10,
        delta=0.999,
        beta=1,
        number_of_steps=4,
        payoffs=numerical.donation_game(1, 3),
        mode="expected",
        filename=filename,
        seed=0,
        starting_resident=(1, 1, 1),
    )
    assert os.path.exists(filename) == True

    df = pd.read_csv(filename, header=None)

    assert len(df.columns) == 13
    assert len(df.values) == 5
    assert df.values[0][7] == "expected"
    assert all(
        df.values[-1][-3:]
        == [0.5680445610939323, 0.9255966382926608, 0.07103605819788694]
    )

    os.remove(filename)


def test_simulation_previous_experiment_file_is_delete():
    """
    This ensures that the results on new experiment are not appended to a file
    of previous results.
    """
    filename = "tests/example_simulation.csv"

    _ = numerical.main(
        10,
        delta=0.999,
        beta=1,
        number_of_steps=1,
        payoffs=numerical.donation_game(1, 3),
        mode="expected",
        filename=filename,
        seed=0,
        starting_resident=(1, 1, 1),
    )

    df = pd.read_csv(filename, header=None)

    assert len(df.columns) == 13
    assert len(df.values) == 2