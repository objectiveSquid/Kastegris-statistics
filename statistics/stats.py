from statistics_types import (
    ActionSymbol,
    Action,
    RoundResult,
    GameResult,
    RoundStopReason,
)
from config import *

import statistics
import random


class Statistics:
    def __init__(
        self,
        actions: list[Action],
        round_simulation_repeats: int = DEFAULT_ROUND_SIMULATION_REPEATS,
        game_simulation_repeats: int = DEFAULT_GAME_SIMULATION_REPEATS,
        random_seed: int | None = None,
        round_stop_points: int = DEFAULT_ROUND_STOP_POINTS,
        game_stop_points: int = DEFAULT_GAME_STOP_POINTS,
    ) -> None:
        if random_seed is not None:
            random.seed(random_seed)

        self.round_simulation_repeats = round_simulation_repeats
        self.game_simulation_repeats = game_simulation_repeats
        self.random_seed = random_seed
        self.round_stop_points = round_stop_points
        self.game_stop_points = game_stop_points

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

        self.run_stats(
            round_simulation_repeats,
            game_simulation_repeats,
            round_stop_points,
            game_stop_points,
        )

    def simulate_round(self, stop_points: int) -> RoundResult:
        result = RoundResult(stop_reason=RoundStopReason.QUIT)
        actions = self.actions.copy()

        while stop_points == -1 or result.final_points < stop_points:
            chosen_action = random.choice(actions)
            result.total_points += chosen_action.value
            result.final_points = result.total_points
            result.length += 1
            if chosen_action.symbol != ActionSymbol.INCREASE_SCORE:
                result.final_points = 0
                result.stop_reason = RoundStopReason(chosen_action.symbol.value)
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

    def simulate_game(
        self,
        round_stop_points: int = DEFAULT_ROUND_STOP_POINTS,
        game_stop_points: int = DEFAULT_GAME_STOP_POINTS,
    ) -> GameResult:
        result = GameResult([], 0, 0, 0, 0)

        while result.final_points < game_stop_points:
            round_result = self.simulate_round(round_stop_points)
            result.rounds.append(round_result)
            result._total_points += round_result.total_points
            if round_result.stop_reason == RoundStopReason.QUIT:
                result._final_points += round_result.final_points
            elif round_result.stop_reason == RoundStopReason.RESET_SCORE:
                result._final_points = 0
            result._throws_count += round_result.length
            result._length += 1

        return result

    def simulate_many_games(
        self,
        num_games: int = DEFAULT_GAME_SIMULATION_REPEATS,
        round_stop_points: int = DEFAULT_ROUND_STOP_POINTS,
        game_stop_points: int = DEFAULT_GAME_STOP_POINTS,
    ) -> list[GameResult]:
        return [
            self.simulate_game(round_stop_points, game_stop_points)
            for _ in range(num_games)
        ]

    def average_many_games(
        self,
        num_games: int = DEFAULT_GAME_SIMULATION_REPEATS,
        round_stop_points: int = DEFAULT_ROUND_STOP_POINTS,
        game_stop_points: int = DEFAULT_GAME_STOP_POINTS,
    ) -> GameResult:
        game_results = self.simulate_many_games(
            num_games, round_stop_points, game_stop_points
        )

        return GameResult(
            [],
            statistics.fmean(
                [game_result.total_points for game_result in game_results]
            ),
            statistics.fmean(
                [game_result.final_points for game_result in game_results]
            ),
            statistics.fmean(
                [game_result.throws_count for game_result in game_results]
            ),
            statistics.fmean([game_result.length for game_result in game_results]),
        )

    def run_stats(
        self,
        round_simulation_repeats: int = DEFAULT_ROUND_SIMULATION_REPEATS,
        game_simulation_repeats: int = DEFAULT_GAME_SIMULATION_REPEATS,
        round_stop_points: int = DEFAULT_ROUND_STOP_POINTS,
        game_stop_points: int = DEFAULT_GAME_STOP_POINTS,
    ) -> None:
        # other stats
        self.average_point_gain = statistics.fmean(
            [action.value for action in self.increase_score_actions]
        )

        # round simulations
        average_many_rounds_output = self.average_many_rounds(
            round_simulation_repeats, round_stop_points
        )
        self.average_round_length = average_many_rounds_output.length
        self.average_round_total_point_gain = average_many_rounds_output.total_points
        self.average_round_final_point_gain = average_many_rounds_output.final_points

        # game simulations
        average_many_games_output = self.average_many_games(
            game_simulation_repeats, round_stop_points, game_stop_points
        )
        self.average_game_throw_count = average_many_games_output.throws_count
        self.average_game_length = average_many_games_output.length

        # chances of actions
        self.chance_of_point_gain = (
            self.increase_score_actions_count / self.actions_count
        )
        self.chance_of_any_round_stop = (
            self.any_round_stop_actions_count / self.actions_count
        )
        self.chance_of_round_stop = self.round_stop_actions_count / self.actions_count
        self.chance_of_reset_score = self.reset_score_actions_count / self.actions_count

    def __repr__(self) -> str:
        return "\n".join(
            [
                # dataset info
                f" --- Dataset information ---",
                f"[ DATA ] Total actions count: {self.actions_count}",
                f"[ DATA ] Increase score actions count: {self.increase_score_actions_count}",
                f"[ DATA ] Any round stop actions count: {self.any_round_stop_actions_count}",
                f"[ DATA ] Round stop actions count: {self.round_stop_actions_count}",
                f"[ DATA ] Reset score actions count: {self.reset_score_actions_count}",
                "",
                # inputs
                " --- Input parameters ---",
                f"[ INFO ] Simulation repeats: {self.round_simulation_repeats:,}",
                f"[ INFO ] Random seed: {self.random_seed if self.random_seed is not None else 'Unknown'}",
                f"[ INFO ] Stop points for a round: {self.round_stop_points if self.round_stop_points != -1 else 'Never'}",
                f"[ INFO ] Stop points for a game: {self.game_stop_points if self.game_stop_points != -1 else 'Never'}",
                "",
                # outputs
                " --- Output statistics ---",
                f"[ STAT ] Average point gain: {round(self.average_point_gain, 2)}",
                f"[ SIM ]  Average round length: {round(self.average_round_length, 2)}",
                f"[ SIM ]  Average round total point gain: {round(self.average_round_total_point_gain, 2)}",
                f"[ SIM ]  Average round final point gain: {round(self.average_round_final_point_gain, 2)}",
                f"[ SIM ]  Average amount of throws until game ends: {round(self.average_game_throw_count, 2)}",
                f"[ SIM ]  Average amount of rounds until game ends: {round(self.average_game_length, 2)}",
                "",
                f"[ STAT ] Chance of point gain: {round(self.chance_of_point_gain, 2)}",
                f"[ STAT ] Chance of any round stop: {round(self.chance_of_any_round_stop, 2)}",
                f"[ STAT ] Chance of round stop: {round(self.chance_of_round_stop, 2)}",
                f"[ STAT ] Chance of reset score: {round(self.chance_of_reset_score, 2)}",
            ]
        )
