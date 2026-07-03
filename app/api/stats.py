from fastapi import APIRouter, Depends

from app.api.dependencies import get_service_singleton
from app.domain.models import GameStatus
from app.service.game_service import GameService

router = APIRouter()


@router.get("/stats")
def get_stats(service: GameService = Depends(get_service_singleton)) -> dict:
    games = service.list_games()
    total = len(games)
    wins_x = 0
    wins_o = 0
    draws = 0
    ongoing = 0
    for game in games:
        if game.status == GameStatus.X_WINS:
            wins_x += 1
        if game.status == GameStatus.O_WINS:
            wins_o += 1
        if game.status == GameStatus.DRAW:
            draws += 1
        if game.status == GameStatus.ONGOING:
            ongoing += 1
    return {
        "total": total,
        "x_wins": wins_x,
        "o_wins": wins_o,
        "draws": draws,
        "ongoing": ongoing,
    }
