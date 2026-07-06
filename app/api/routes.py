from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException

from app.api.dependencies import get_service_singleton
from app.api.stats import router as stats_router
from app.config import settings
from app.domain.models import Game, MoveRequest
from app.service.game_service import GameService

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST para jugar partidas de Gato (Tic Tac Toe) vía HTTP.",
)

app.include_router(stats_router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "version": settings.app_version}


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


@app.get("/games/{game_id}/board")
def get_board(
    game_id: UUID, service: GameService = Depends(get_service_singleton)
) -> dict:
    try:
        game = service.get_game(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Partida no encontrada")

    b = game.board
    display = (
        f"{b[0] or '·'} | {b[1] or '·'} | {b[2] or '·'}\n"
        f"{b[3] or '·'} | {b[4] or '·'} | {b[5] or '·'}\n"
        f"{b[6] or '·'} | {b[7] or '·'} | {b[8] or '·'}"
    )
    return {"board": display}
