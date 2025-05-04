import dataclasses
import enum


class ActionSymbol(enum.Enum):
    LOSE_GAME = "-----"
    RESET_SCORE = "---"
    LOST_ROUND = "-"
    INCREASE_SCORE = "number"


@dataclasses.dataclass(frozen=True)
class Action:
    symbol: ActionSymbol
    value: int = 0


@dataclasses.dataclass()
class RoundResult:
    total_points: float = 0
    final_points: float = 0
    length: float = 0
