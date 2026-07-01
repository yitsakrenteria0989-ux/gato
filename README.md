# Gato API

API REST del juego Gato (Tic Tac Toe) construida con FastAPI.
Permite jugar partidas de dos jugadores vía HTTP.


## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) — gestor de dependencias

## Instalación

```bash
git clone <url-del-repo>
cd gato
uv sync --extra dev
uvicorn app.api.routes:app --reload
```

## Uso

### Crear una partida
Comando para generar una partida que se guarda de forma local
```bash
curl -X POST http://localhost:8000/games
```

### Ver estatus de una partida
Comando para observar el estatus de una partida generada, ej. ONGOING, X_WINS
```bash
curl http://localhost:8000/games/{id}
```

### Hacer un movimiento
Comando para realizar un movimiento en el tablero para el jugador en turno.

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```
```bash
curl -X POST "http://localhost:8000/games/{id}/move?player=X&position=0"
```

### Borrar una partida
Comando para borrar una partida en la memoria de la API
```bash
curl -X DELETE http://localhost:8000/games/{id}
```

## Desarrollo

### Correr tests
```bash
python -m pytest
```

### Verificar estilo
```bash
python -m ruff check .
python -m black --check .
```


