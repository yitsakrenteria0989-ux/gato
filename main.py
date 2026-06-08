from uuid import UUID

from fastapi import FastAPI

from models import Game, Player

app = FastAPI(title="Gato API")


@app.post("/games")
def create_game() -> Game:
    raise NotImplementedError


@app.get("/games/{game_id}")
def get_game(game_id: UUID) -> Game:
    raise NotImplementedError


@app.post("/games/{game_id}/move")
def make_move(game_id: UUID, player: Player, position: int) -> Game:
    raise NotImplementedError


@app.delete("/games/{game_id}")
def delete_game(game_id: UUID) -> None:
    raise NotImplementedError
