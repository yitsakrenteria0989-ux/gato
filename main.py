from uuid import UUID

from fastapi import FastAPI, HTTPException

from game_service import GameService
from models import Game, Player

app = FastAPI(title="Gato API")
service = GameService()


@app.post("/games")
def create_game() -> Game:
    return service.create_game()


@app.get("/games/{game_id}")
def get_game(game_id: UUID) -> Game:
    try:
        return service.get_game(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Partida no encontrada")


@app.post("/games/{game_id}/move")
def make_move(game_id: UUID, player: Player, position: int) -> Game:
    try:
        return service.make_move(game_id, player, position)
    except KeyError:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/games/{game_id}")
def delete_game(game_id: UUID) -> None:
    try:
        service.delete_game(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
