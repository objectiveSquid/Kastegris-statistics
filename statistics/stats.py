from statistics_types import ActionSymbol, Action, RoundResult

import random


def avg(values: list[float]) -> float:
    return sum(values) / len(values)


class Statistics:
    def __init__(self, actions: list[Action]) -> None:
        self.actions = actions
        self.actions_count = len(actions)

        self.increase_score_actions = [
            action for action in actions if action.symbol == ActionSymbol.INCREASE_SCORE
        ]
        self.increase_score_actions_count = len(self.increase_score_actions)
        self.any_round_stop_actions_count = len(
            [
                action
                for action in actions
                if action.symbol != ActionSymbol.INCREASE_SCORE
            ]
        )
        self.round_stop_actions_count = len(
            [action for action in actions if action.symbol == ActionSymbol.LOST_ROUND]
        )
        self.reset_score_actions_count = len(
            [action for action in actions if action.symbol == ActionSymbol.RESET_SCORE]
        )
        self.lose_game_actions_count = len(
            [action for action in actions if action.symbol == ActionSymbol.LOSE_GAME]
        )

        self.average_point_gain = None
        self.average_round_length = None
        self.average_round_point_gain = None

        self.chance_of_point_gain = None
        self.chance_of_any_round_stop = None
        self.chance_of_round_stop = None
        self.chance_of_reset_score = None
        self.chance_of_lose_game = None

        self.run_stats()

    def simulate_round(self) -> RoundResult:
        result = RoundResult()
        actions = self.actions.copy()

        while True:
            chosen_action = random.choice(actions)
            result.points += chosen_action.value
            result.length += 1
            if chosen_action.symbol != ActionSymbol.INCREASE_SCORE:
                return result

    def simulate_many_rounds(self, num_rounds: int) -> list[RoundResult]:
        return [self.simulate_round() for _ in range(num_rounds)]

    def average_many_rounds(self, num_rounds: int) -> RoundResult:
        round_results = self.simulate_many_rounds(num_rounds)

        return RoundResult(
            avg([round_result.points for round_result in round_results]),
            avg([round_result.length for round_result in round_results]),
        )

    def run_stats(self) -> None:
        self.average_point_gain = avg(
            [action.value for action in self.increase_score_actions]
        )
        average_many_rounds_output = self.average_many_rounds(1000)
        self.average_round_length = average_many_rounds_output.length
        self.average_round_point_gain = average_many_rounds_output.points

        self.chance_of_point_gain = (
            self.increase_score_actions_count / self.actions_count
        )
        self.chance_of_any_round_stop = (
            self.any_round_stop_actions_count / self.actions_count
        )
        self.chance_of_round_stop = self.round_stop_actions_count / self.actions_count
        self.chance_of_reset_score = self.reset_score_actions_count / self.actions_count
        self.chance_of_lose_game = self.lose_game_actions_count / self.actions_count

    def __repr__(self) -> str:
        return "\n".join(
            [
                f"Average point gain: {round(self.average_point_gain, 2)}",
                f"Average round length: {round(self.average_round_length, 2)}",
                f"Average round point gain: {round(self.average_round_point_gain, 2)}",
                f"Chance of point gain: {round(self.chance_of_point_gain, 2)}",
                f"Chance of any round stop: {round(self.chance_of_any_round_stop, 2)}",
                f"Chance of round stop: {round(self.chance_of_round_stop, 2)}",
                f"Chance of reset score: {round(self.chance_of_reset_score, 2)}",
                f"Chance of lose game: {round(self.chance_of_lose_game, 2)}",
            ]
        )
