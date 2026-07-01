from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models import Game, GameStatus, Player
from app.repository.base import GameRepository

_WINNING_COMBINATIONS: list[list[int]] = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


class GameService:
    def __init__(self, repo: GameRepository) -> None:
        self._repo = repo

    def create_game(self) -> Game:
        """Crea una partida. Siempre inicia Player.X"""
        game = Game(
            id=uuid4(),
            board=[None] * 9,
            current_player=Player.X,
            status=GameStatus.ONGOING,
            created_at=datetime.now(),
        )
        self._repo.save(game)
        return game

    def get_game(self, game_id: UUID) -> Game:
        """Recupera un juego en base a su id

        Args:
            game_id: id de la partida creada anteriormente

        Returns:
            Partida asociada al id

        Raises:
            KeyError: No existe partida con ese id
        """
        game = self._repo.find_by_id(game_id)
        if game is None:
            raise KeyError("Partida no encontrada")
        return game

    def _validate_move(self, game: Game, player: Player, position: int) -> None:
        if game.status != GameStatus.ONGOING:
            raise ValueError("La partida ya terminó")
        if game.current_player != player:
            raise ValueError("No es tu turno")
        if position < 0 or position > 8:
            raise ValueError("Posición inválida")
        if game.board[position] is not None:
            raise ValueError("Esa celda ya está ocupada")

    def _detects_winner_or_draw(self, game: Game, player: Player) -> Player | None:
        for combo in _WINNING_COMBINATIONS:
            a, b, c = combo
            if game.board[a] == game.board[b] == game.board[c] == player.value:
                return player
        return None

    def _update_game(self, game: Game, player: Player, winner: Player | None) -> None:
        if winner:
            game.status = GameStatus.X_WINS if player == Player.X else GameStatus.O_WINS
            game.winner = winner
        elif all(cell is not None for cell in game.board):
            game.status = GameStatus.DRAW
        else:
            game.current_player = Player.O if player == Player.X else Player.X

    def make_move(self, game_id: UUID, player: Player, position: int) -> Game:
        """Aplica un movimiento en una partida en curso
        El tablero utiliza indices del 0-8, de izquierda a derecha y arriba hacía abajo
        El turno inicial siempre es de Player.X

        Args:
            game_id: id de la partida
            player: jugador que hace el movimiento
            position: indice del tablero dónde se hará el movimiento

        Returns:
            El juego con el movimiento realizado

        Raises:
            KeyError: No existe partida con ese id
            ValueError: Se realiza un movimiento que viola las reglas
        """
        game = self.get_game(game_id)

        self._validate_move(game, player, position)

        game.board[position] = player.value

        winner = self._detects_winner_or_draw(game, player)

        self._update_game(game, player, winner)

        self._repo.save(game)
        return game

    def delete_game(self, game_id: UUID) -> None:
        """Borra una partida del repositorio

        Args:
            game_id: id de la partida a borrar

        Raises:
            KeyError: No hay partida con ese id
        """
        self._repo.delete(game_id)

    def list_games(self) -> list[Game]:
        """Retorna una lista de todos los juegos creados"""
        return self._repo.list_all()

