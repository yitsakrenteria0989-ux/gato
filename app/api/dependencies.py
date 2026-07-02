from app.repository.memory import InMemoryGameRepository
from app.service.game_service import GameService


def get_service() -> GameService:
    return GameService(repo=InMemoryGameRepository())


_service = get_service()


def get_service_singleton() -> GameService:
    return _service
