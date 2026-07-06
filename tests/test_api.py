from uuid import uuid4


def test_create_game(client):
    response = client.post("/games")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ongoing"
    assert data["current_player"] == "X"
    assert data["board"] == [None] * 9
    assert data["winner"] is None


def test_non_existing_id(client):
    id_false = uuid4()

    response = client.get(f"/games/{id_false}")

    assert response.status_code == 404


def test_make_move(client):
    game_id = client.post("/games").json()["id"]

    response = client.post(
        f"/games/{game_id}/move",
        json={"player": "X", "position": 0},
    )

    assert response.status_code == 200
    assert response.json()["board"][0] == "X"


def test_list_games(client):
    client.post("/games")
    client.post("/games")

    response = client.get("/games")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_stats(client):
    client.post("/games")
    client.post("/games")
    client.post("/games")

    response = client.get("/stats")

    data = response.json()
    assert response.status_code == 200
    assert data["total"] == 3
    assert data["ongoing"] == 3


def test_stats_o_wins(client):
    game_id = client.post("/games").json()["id"]
    for player, position in [
        ("X", 0),
        ("O", 3),
        ("X", 1),
        ("O", 4),
        ("X", 7),
        ("O", 5),
    ]:
        client.post(
            f"/games/{game_id}/move", json={"player": player, "position": position}
        )

    data = client.get("/stats").json()
    assert data["o_wins"] == 1
    assert data["ongoing"] == 0


def test_stats_draw(client):
    game_id = client.post("/games").json()["id"]
    for player, position in [
        ("X", 0),
        ("O", 4),
        ("X", 1),
        ("O", 3),
        ("X", 5),
        ("O", 2),
        ("X", 6),
        ("O", 8),
        ("X", 7),
    ]:
        client.post(
            f"/games/{game_id}/move", json={"player": player, "position": position}
        )

    data = client.get("/stats").json()
    assert data["draws"] == 1
    assert data["ongoing"] == 0
