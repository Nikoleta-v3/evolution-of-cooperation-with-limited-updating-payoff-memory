import os
from importlib.machinery import SourceFileLoader

import pandas as pd

invasion = SourceFileLoader("invasion", "src/invasion.py").load_module()
numerical = SourceFileLoader("numerical", "src/numerical.py").load_module()


def test_invasion():

    filename = "test_invasion.csv"
    assert os.path.exists(filename) == False

    _ = invasion.simulate_until_invasion(
        10,
        delta=0.999,
        beta=1,
        payoffs=numerical.donation_game(1, 3),
        mode="expected",
        filename=filename,
        seed=0,
        starting_resident=(0, 0, 0),
    )
    assert os.path.exists(filename) == True

    df = pd.read_csv(filename, header=None)
    df.columns = [
        "R",
        "S",
        "T",
        "P",
        "N",
        "delta",
        "beta",
        "mode",
        "t",
        "cooperation",
        "score",
        "y",
        "p",
        "q",
    ]

    assert len(df.columns) == 14
    assert len(df.values) == 2
    assert df.iloc[-1]["mode"] == "expected"
    assert df.iloc[-1]["t"] == 3

    os.remove(filename)


def test_invasion_stochastic():

    filename = "test_invasion.csv"
    assert os.path.exists(filename) == False

    _ = invasion.simulate_until_invasion(
        10,
        delta=0.999,
        beta=1,
        payoffs=numerical.donation_game(1, 3),
        mode="stochastic",
        filename=filename,
        seed=0,
        starting_resident=(0, 0, 0),
    )
    assert os.path.exists(filename) == True

    df = pd.read_csv(filename, header=None)
    df.columns = [
        "R",
        "S",
        "T",
        "P",
        "N",
        "delta",
        "beta",
        "mode",
        "t",
        "cooperation",
        "score",
        "y",
        "p",
        "q",
    ]

    assert len(df.columns) == 14
    assert len(df.values) == 2
    assert df.iloc[-1]["mode"] == "stochastic"
    assert df.iloc[-1]["t"] == 3

    os.remove(filename)
