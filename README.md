# Gato API

API REST del juego Gato (Tic Tac Toe) construida con FastAPI.

## Tablero

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/games` | Crear nueva partida |
| GET | `/games/{id}` | Ver estado actual |
| POST | `/games/{id}/move` | Hacer un movimiento |
| DELETE | `/games/{id}` | Abandonar partida |

## Correr en local

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
