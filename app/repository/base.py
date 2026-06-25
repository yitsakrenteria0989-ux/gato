from typing import Protocol
from uuid import UUID

from app.domain.models import Game


class GameRepository(Protocol):

    def save(self, game: Game) -> None: ...
    def find_by_id(self, game_id: UUID) -> Game | None: ...
    def delete(self, game_id: UUID) -> None: ...
