import dataclasses
import enum


class ActionSymbol(enum.Enum):
    RESET_SCORE = "---"
    LOST_ROUND = "-"
    INCREASE_SCORE = "number"


@dataclasses.dataclass(frozen=True)
class Action:
    symbol: ActionSymbol
    value: int = 0


class RoundStopReason(enum.Enum):
    QUIT = "quit"
    LOST_ROUND = ActionSymbol.LOST_ROUND.value
    RESET_SCORE = ActionSymbol.RESET_SCORE.value


@dataclasses.dataclass()
class RoundResult:
    total_points: float = 0
    final_points: float = 0
    length: float = 0
    stop_reason: RoundStopReason | None = None


@dataclasses.dataclass()
class GameResult:
    rounds: list[RoundResult] = None  # type: ignore
    _total_points: float = None  # type: ignore
    _final_points: float = None  # type: ignore
    _throws_count: float = None  # type: ignore
    _length: float = None  # type: ignore

    def __post_init__(self) -> None:
        if self.rounds is None:
            self.rounds = []

    @property
    def total_points(self) -> float:
        if self._total_points is not None:
            return self._total_points
        if len(self.rounds) == 0:
            return 0
        return sum([round.total_points for round in self.rounds])

    @property
    def final_points(self) -> float:
        if self._final_points is not None:
            return self._final_points
        if len(self.rounds) == 0:
            return 0
        return max([round.final_points for round in self.rounds])

    @property
    def throws_count(self) -> float:
        if self._throws_count is not None:
            return self._throws_count
        if len(self.rounds) == 0:
            return 0
        return sum([round.length for round in self.rounds])

    @property
    def length(self) -> float:
        if self._length is not None:
            return self._length
        if len(self.rounds) == 0:
            return 0
        return len(self.rounds)
