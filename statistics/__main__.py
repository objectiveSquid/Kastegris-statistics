from statistics_types import ActionSymbol, Action
from stats import Statistics
from config import *

import argparse
import os


def main(
    actions: list[Action],
    round_simulation_repeats: int,
    game_simulation_repeats: int,
    seed: int,
    round_stop_points: int,
    game_stop_points: int,
) -> int:
    statistics = Statistics(
        actions,
        round_simulation_repeats,
        game_simulation_repeats,
        seed,
        round_stop_points,
        game_stop_points,
    )
    print(statistics)

    return 0


def parse_dataset_file(file: str) -> list[Action]:
    try:
        with open(file, "r") as fd:
            lines = fd.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found: {file}")

    output = []
    for line_index, line in enumerate(lines):
        line = line.strip()

        # empty line check
        if line == "":
            continue

        # comment check
        if line.startswith("#"):
            continue

        # point increase
        if line.isdigit():
            output.append(Action(ActionSymbol.INCREASE_SCORE, int(line)))
            continue

        # everything else
        try:
            output.append(Action(ActionSymbol(line.strip())))
        except ValueError:
            raise ValueError(f"Unknown symbol in dataset, line {line_index}: {line}")

    return output


def parse_many_datasets(datasets: list[str]) -> list[Action]:
    new_files = []
    for path in datasets:
        if os.path.isdir(path):
            new_files.extend([os.path.join(path, file) for file in os.listdir(path)])
        else:
            new_files.append(path)

    output = []

    for file in new_files:
        output.extend(parse_dataset_file(file))

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Kastegris statistics")
    parser.add_argument(
        "datasets",
        nargs="+",
        help="The datasets to use. If an entry is a directory, all files in it will be used. Must be formatted as described in the README.",
    )
    parser.add_argument(
        "-rr",
        "--round-simulation-repeats",
        type=int,
        default=DEFAULT_ROUND_SIMULATION_REPEATS,
        help="The number of times to run the round simulations.",
    )
    parser.add_argument(
        "-gr",
        "--game-simulation-repeats",
        type=int,
        default=DEFAULT_GAME_SIMULATION_REPEATS,
        help="The number of times to run the game simulations.",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=None,
        help="The seed to use for the random number generator.",
    )
    parser.add_argument(
        "-rs",
        "--round-stop-points",
        type=int,
        default=DEFAULT_ROUND_STOP_POINTS,
        help="The number of points to stop each round simulation at, -1 means to never stop.",
    )
    parser.add_argument(
        "-gs",
        "--game-stop-points",
        type=int,
        default=DEFAULT_GAME_STOP_POINTS,
        help="The number of points to stop each game simulation at.",
    )

    args = parser.parse_args()
    datasets = args.datasets
    round_simulation_repeats = args.round_simulation_repeats
    game_simulation_repeats = args.game_simulation_repeats
    seed = args.seed
    round_stop_points = args.round_stop_points
    game_stop_points = args.game_stop_points

    try:
        actions = parse_many_datasets(datasets)
    except ValueError as error:
        print(error)
        exit(1)

    if game_stop_points < 1:
        print(
            "--game-stop-points parameter must be greater than or equal to 1. Use --help for more information."
        )
        exit(1)

    exit(
        main(
            actions,
            round_simulation_repeats,
            game_simulation_repeats,
            seed,
            round_stop_points,
            game_stop_points,
        )
    )
