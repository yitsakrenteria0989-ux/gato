from datetime import datetime
from enum import Enum
from typing import TypeAlias
from uuid import UUID

Board: TypeAlias = list[str | None]


class Player(str, Enum):
    X = "X"
    O = "O"  # noqa: E741


class GameStatus(str, Enum):
    ONGOING = "ongoing"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"


class Game:
    def __init__(
        self,
        id: UUID,
        board: Board,
        current_player: Player,
        status: GameStatus,
        created_at: datetime,
        winner: Player | None = None,
    ) -> None:
        self.id = id
        self.board = board
        self.current_player = current_player
        self.status = status
        self.created_at = created_at
        self.winner = winner
