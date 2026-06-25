from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.routes import app


@pytest.fixture
def client():
    return TestClient(app)

def test_create_game(client):
    # Act
    response = client.post("/games")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ongoing"
    assert data["current_player"] == "X"
    assert data["board"] == [None] * 9
    assert data["winner"] is None


def test_non_existing_id(client):
    # Arrange
    id_false = uuid4()

    # Act
    response = client.get(f"/games/{id_false}")

    # Assert
    assert response.status_code == 404


def test_make_move(client):
    # Arrange — crear partida primero
    game_id = client.post("/games").json()["id"]

    # Act
    response = client.post(
        f"/games/{game_id}/move",
        params={"player": "X", "position": 0},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["board"][0] == "X"
