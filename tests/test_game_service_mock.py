from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.service.game_service import GameService


def test_create_game_llama_save():
    # Arrange — repositorio falso
    repo = MagicMock()
    service = GameService(repo=repo)

    # Act
    game = service.create_game()

    # Assert — verificar que save fue llamado exactamente una vez con el juego
    repo.save.assert_called_once_with(game)


def test_get_game_cuando_repo_devuelve_none():
    # Arrange
    repo = MagicMock()
    repo.find_by_id.return_value = None  # ← controlas el retorno
    service = GameService(repo=repo)

    # Act + Assert
    with pytest.raises(KeyError):
        service.get_game(uuid4())
