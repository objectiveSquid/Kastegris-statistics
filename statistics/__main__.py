from statistics_types import ActionSymbol, Action
from stats import Statistics

import argparse


def main(actions: list[Action]) -> int:
    statistics = Statistics(actions)
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

    args = parser.parse_args()
    actions = args.dataset

    try:
        actions = parse_dataset_file(actions)
    except ValueError as error:
        print(error)
        exit(1)

    exit(main(actions))
