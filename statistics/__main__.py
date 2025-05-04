from statistics_types import ActionSymbol, Action
from stats import Statistics
from config import *

import argparse


def main(
    actions: list[Action],
    simulation_repeats: int,
    seed: int,
    stop_points: int,
) -> int:
    statistics = Statistics(actions, simulation_repeats, seed, stop_points)
    print(statistics)

    return 0


def parse_dataset_file(file: str) -> list[Action]:
    with open(file, "r") as fd:
        lines = fd.readlines()

    output = []
    for line_index, line in enumerate(lines):
        line = line.strip()

        # empty line check
        if line == "":
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Kastegris statistics")
    parser.add_argument(
        "dataset",
        type=str,
        help="The dataset file to use, must be formatted as described in the README.",
    )
    parser.add_argument(
        "-r",
        "--simulation_repeats",
        type=int,
        default=DEFAULT_SIMULATION_REPEATS,
        help="The number of times to run the simulation.",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=None,
        help="The seed to use for the random number generator.",
    )
    parser.add_argument(
        "-sp",
        "--stop-points",
        type=int,
        default=DEFAULT_STOP_POINTS,
        help="The number of points to stop each simulation at, -1 means to never stop.",
    )

    args = parser.parse_args()
    actions = args.dataset
    simulation_repeats = args.simulation_repeats
    seed = args.seed
    stop_points = args.stop_points

    try:
        actions = parse_dataset_file(actions)
    except ValueError as error:
        print(error)
        exit(1)

    exit(main(actions, simulation_repeats, seed, stop_points))
