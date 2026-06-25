from uuid import UUID

from app.domain.models import Game


class InMemoryGameRepository:
    def __init__(self) -> None:
        self._games: dict[UUID, Game] = {}

    def save(self, game: Game) -> None:
        self._games[game.id] = game

    def find_by_id(self, game_id: UUID) -> Game | None:
        return self._games.get(game_id)

    def delete(self, game_id: UUID) -> None:
        if game_id not in self._games:
            raise KeyError("Partida no encontrada")
        del self._games[game_id]
