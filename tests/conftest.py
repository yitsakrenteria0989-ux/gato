import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_service_singleton
from app.api.routes import app
from app.repository.memory import InMemoryGameRepository
from app.service.game_service import GameService


@pytest.fixture
def service():
    return GameService(repo=InMemoryGameRepository())


@pytest.fixture
def client():
    fresh_service = GameService(repo=InMemoryGameRepository())
    app.dependency_overrides[get_service_singleton] = lambda: fresh_service
    yield TestClient(app)
    app.dependency_overrides.clear()
