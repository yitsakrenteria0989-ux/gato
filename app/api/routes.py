from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException

from app.config import settings
from app.domain.models import Game, MoveRequest
from app.repository.memory import InMemoryGameRepository
from app.service.game_service import GameService

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST para jugar partidas de Gato (Tic Tac Toe) vía HTTP.",
)


def get_service() -> GameService:
    return GameService(repo=InMemoryGameRepository())


_service = get_service()


def get_service_singleton() -> GameService:
    return _service


@app.post("/games")
def create_game(service: GameService = Depends(get_service_singleton)) -> Game:
    return service.create_game()


@app.get("/games")
def list_games(service: GameService = Depends(get_service_singleton)) -> list[Game]:
    return service.list_games()


@app.get("/games/{game_id}")
def get_game(
    game_id: UUID, service: GameService = Depends(get_service_singleton)
) -> Game:
    try:
        return service.get_game(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Partida no encontrada")


@app.post("/games/{game_id}/move")
def make_move(
    game_id: UUID,
    body: MoveRequest,
    service: GameService = Depends(get_service_singleton),
) -> Game:
    try:
        return service.make_move(game_id, body.player, body.position)
    except KeyError:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/games/{game_id}")
def delete_game(
    game_id: UUID, service: GameService = Depends(get_service_singleton)
) -> None:
    try:
        service.delete_game(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
