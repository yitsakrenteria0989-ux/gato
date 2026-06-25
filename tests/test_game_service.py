from uuid import uuid4

import pytest

from app.domain.models import GameStatus, Player


@pytest.fixture
def game(service):
    return service.create_game()


def test_create_empty_game(service):
    # Act
    game = service.create_game()

    # Assert
    assert game.board == [None] * 9
    assert game.current_player == Player.X
    assert game.status == GameStatus.ONGOING
    assert game.winner is None


def test_non_existing_id(service):
    # Arrange
    id_inexistente = uuid4()

    # Act + Assert
    with pytest.raises(KeyError):
        service.get_game(id_inexistente)


def test_valid_move(service, game):
    # Act
    update_game = service.make_move(game.id, Player.X, position=0)

    # Assert
    assert update_game.board[0] == "X"
    assert update_game.current_player == Player.O


def test_out_of_turn_player(service, game):
    # Act + Assert
    service.make_move(game.id, Player.X, position=0)
    with pytest.raises(ValueError):
        service.make_move(game.id, Player.X, position=1)
