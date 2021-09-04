import sys

import glob

import tqdm

import pandas as pd

if __name__ == "__main__":  # pragma: no cover
    folder = sys.argv[1]
    starting_characters = sys.argv[2]

    in_columns = [
        "y",
        "p",
        "q",
        "average cooperation rate",
        "average score",
        "t",
    ]

    # in_columns = [
    #     "p_1",
    #     "p_2",
    #     "p_3",
    #     "p_4",
    #     "y",
    #     "average cooperation rate",
    #     "average score",
    #     "t",
    # ]

    print(f"{folder}/{starting_characters}*.csv")
    csv_files = glob.glob(f"{folder}/{starting_characters}*.csv")

    for file in tqdm.tqdm(csv_files):
        df = pd.read_csv(file, header=None)
        df = df.drop_duplicates()
        df.columns = in_columns

        frequencies = []
        previous = 0
        for value in df["t"][1:]:
            frequencies.append(value - previous)
            previous = value
        frequencies.append(sum(df['t']) - previous)

        df["frequencies"] = frequencies

        df.to_csv(f"{folder}clean_{file[len(folder):]}", index=False)
