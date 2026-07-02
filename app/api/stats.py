from fastapi import APIRouter

from app.api.routes import get_service_singleton

router = APIRouter()

@router.get("/stats")
def get_stats():
    s = get_service_singleton()
    games = s.list_games()
    total = len(games)
    wins_x = 0
    wins_o = 0
    draws = 0
    ongoing = 0
    for g in games:
        if g.status == "x_wins":
            wins_x = wins_x + 1
        if g.status == "o_wins":
            wins_o = wins_o + 1
        if g.status == "draw":
            draws = draws + 1
        if g.status == "ongoing":
            ongoing = ongoing + 1
    return {"total": total, "x_wins": wins_x, "o_wins": wins_o, "draws": draws, "ongoing": ongoing}
