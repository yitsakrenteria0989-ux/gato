from datetime import datetime
from enum import Enum
from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel

Board: TypeAlias = list[str | None]


class Player(str, Enum):
    X = "X"
    O = "O"  # noqa: E741


class GameStatus(str, Enum):
    ONGOING = "ongoing"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"


class Game(BaseModel):
    id: UUID
    board: Board
    current_player: Player
    status: GameStatus
    created_at: datetime
    winner: Player | None = None


class MoveRequest(BaseModel):
    player: Player
    position: int

    model_config = {
        "json_schema_extra": {
            "example": {"player": "X", "position": 0}
        }
    }
