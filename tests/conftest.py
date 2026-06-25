import pytest

from app.repository.memory import InMemoryGameRepository
from app.service.game_service import GameService


@pytest.fixture
def service():
    return GameService(repo=InMemoryGameRepository())
