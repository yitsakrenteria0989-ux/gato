from datetime import datetime
from uuid import UUID, uuid4

from models import Game, GameStatus, Player

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
    def __init__(self) -> None:
        self._games: dict[UUID, Game] = {}

    def create_game(self) -> Game:
        game = Game(
            id=uuid4(),
            board=[None] * 9,
            current_player=Player.X,
            status=GameStatus.ONGOING,
            created_at=datetime.now(),
        )
        self._games[game.id] = game
        return game

    def get_game(self, game_id: UUID) -> Game:
        if game_id not in self._games:
            raise KeyError("Partida no encontrada")
        return self._games[game_id]

    def make_move(self, game_id: UUID, player: Player, position: int) -> Game:
        if game_id not in self._games:
            raise KeyError("Partida no encontrada")

        game = self._games[game_id]

        if game.status != GameStatus.ONGOING:
            raise ValueError("La partida ya terminó")
        if game.current_player != player:
            raise ValueError("No es tu turno")
        if position < 0 or position > 8:
            raise ValueError("Posición inválida")
        if game.board[position] is not None:
            raise ValueError("Esa celda ya está ocupada")

        game.board[position] = player.value

        winner = None
        for combo in _WINNING_COMBINATIONS:
            a, b, c = combo
            if game.board[a] == game.board[b] == game.board[c] == player.value:
                winner = player
                break

        if winner:
            game.status = GameStatus.X_WINS if player == Player.X else GameStatus.O_WINS
            game.winner = winner
        elif all(cell is not None for cell in game.board):
            game.status = GameStatus.DRAW
        else:
            game.current_player = Player.O if player == Player.X else Player.X

        return game

    def delete_game(self, game_id: UUID) -> None:
        if game_id not in self._games:
            raise KeyError("Partida no encontrada")
        del self._games[game_id]
