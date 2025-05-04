from statistics_types import ActionSymbol, Action, RoundResult
from config import *

import statistics
import random


class Statistics:
    def __init__(
        self,
        actions: list[Action],
        simulation_repeats: int = DEFAULT_SIMULATION_REPEATS,
        random_seed: int | None = None,
        stop_points: int = DEFAULT_STOP_POINTS,
    ) -> None:
        if random_seed is not None:
            random.seed(random_seed)

        self.simulation_repeats = simulation_repeats
        self.random_seed = random_seed
        self.stop_points = stop_points

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
        self.average_round_total_point_gain = None
        self.average_round_final_point_gain = None

        self.chance_of_point_gain = None
        self.chance_of_any_round_stop = None
        self.chance_of_round_stop = None
        self.chance_of_reset_score = None
        self.chance_of_lose_game = None

        self.run_stats(simulation_repeats, stop_points)

    def simulate_round(self, stop_points: int) -> RoundResult:
        result = RoundResult()
        actions = self.actions.copy()

        while stop_points == -1 or result.total_points < stop_points:
            chosen_action = random.choice(actions)
            result.total_points += chosen_action.value
            result.final_points = result.total_points
            result.length += 1
            if chosen_action.symbol != ActionSymbol.INCREASE_SCORE:
                result.final_points = 0
                break

        return result

    def simulate_many_rounds(
        self, num_rounds: int, stop_points: int
    ) -> list[RoundResult]:
        return [self.simulate_round(stop_points) for _ in range(num_rounds)]

    def average_many_rounds(self, num_rounds: int, stop_points: int) -> RoundResult:
        round_results = self.simulate_many_rounds(num_rounds, stop_points)

        return RoundResult(
            statistics.fmean(
                [round_result.total_points for round_result in round_results]
            ),
            statistics.fmean(
                [round_result.final_points for round_result in round_results]
            ),
            statistics.fmean([round_result.length for round_result in round_results]),
        )

    def run_stats(
        self,
        simulation_repeats: int = DEFAULT_SIMULATION_REPEATS,
        stop_points: int = DEFAULT_STOP_POINTS,
    ) -> None:
        self.average_point_gain = statistics.fmean(
            [action.value for action in self.increase_score_actions]
        )
        average_many_rounds_output = self.average_many_rounds(
            simulation_repeats, stop_points
        )
        self.average_round_length = average_many_rounds_output.length
        self.average_round_total_point_gain = average_many_rounds_output.total_points
        self.average_round_final_point_gain = average_many_rounds_output.final_points

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
                # dataset info
                f"[ DATA ] Total actions count: {self.actions_count}",
                f"[ DATA ] Increase score actions count: {self.increase_score_actions_count}",
                f"[ DATA ] Any round stop actions count: {self.any_round_stop_actions_count}",
                f"[ DATA ] Round stop actions count: {self.round_stop_actions_count}",
                f"[ DATA ] Reset score actions count: {self.reset_score_actions_count}",
                f"[ DATA ] Lose game actions count: {self.lose_game_actions_count}",
                "",
                # inputs
                f"[ INFO ] Simulation repeats: {self.simulation_repeats:,}",
                f"[ INFO ] Random seed: {self.random_seed if self.random_seed is not None else 'Unknown'}",
                f"[ INFO ] Stop points: {self.stop_points if self.stop_points != -1 else 'Never'}",
                "",
                # outputs
                f"[ STAT ] Average point gain: {round(self.average_point_gain, 2)}",
                f"[ SIM ]  Average round length: {round(self.average_round_length, 2)}",
                f"[ SIM ]  Average round total point gain: {round(self.average_round_total_point_gain, 2)}",
                f"[ SIM ]  Average round final point gain: {round(self.average_round_final_point_gain, 2)}",
                f"[ STAT ] Chance of point gain: {round(self.chance_of_point_gain, 2)}",
                f"[ STAT ] Chance of any round stop: {round(self.chance_of_any_round_stop, 2)}",
                f"[ STAT ] Chance of round stop: {round(self.chance_of_round_stop, 2)}",
                f"[ STAT ] Chance of reset score: {round(self.chance_of_reset_score, 2)}",
                f"[ STAT ] Chance of lose game: {round(self.chance_of_lose_game, 2)}",
            ]
        )
