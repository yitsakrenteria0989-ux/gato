from uuid import uuid4

import pytest

from app.domain.models import GameStatus, Player


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
