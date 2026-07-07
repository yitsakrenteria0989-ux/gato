# Resumen del Curso — Ingeniería de Software Profesional

Proyecto construido: **API REST del juego Gato (Tic Tac Toe)** en Python/FastAPI.
Repositorio: https://github.com/yitsakrenteria0989-ux/gato
Producción: https://gato-api.onrender.com

---

## Módulo 1 — Buenas Prácticas de Python

### PEP 8 — Convenciones de estilo
- Nombres de funciones y variables en `snake_case`
- Nombres de clases en `PascalCase`
- Constantes en `UPPER_SNAKE_CASE`
- Máximo 88 caracteres por línea
- Imports agrupados: stdlib → third-party → local, separados por línea en blanco

### Type hints
```python
# Parámetros y retorno siempre anotados
def hacer_movimiento(game_id: UUID, player: Player, position: int) -> Game:
    ...

# Tipos opcionales
description: str | None = None

# Listas y dicts
board: list[str | None]
games: dict[UUID, Game]

# TypeAlias — nombrar tipos complejos
Board: TypeAlias = list[str | None]
```

### Herramientas de estilo
```bash
python -m ruff check .          # linter — detecta errores
python -m ruff check --fix .    # linter — corrige automáticamente
python -m black .               # formateador — aplica cambios
python -m black --check .       # formateador — solo verifica
```

### Principio SOLID — SRP (Single Responsibility)
Cada clase tiene una sola razón para cambiar.
```
main.py          → solo HTTP (routing, errores)
game_service.py  → solo reglas del juego
memory.py        → solo acceso a datos
```

### Principio SOLID — DIP (Dependency Inversion)
Depender de abstracciones, no de implementaciones concretas.
```python
# Abstracción (Protocol)
class GameRepository(Protocol):
    def save(self, game: Game) -> None: ...
    def find_by_id(self, game_id: UUID) -> Game | None: ...

# GameService depende del Protocol, no del dict concreto
class GameService:
    def __init__(self, repo: GameRepository) -> None:
        self._repo = repo
```

### Clean Code
- Funciones pequeñas que hacen una sola cosa
- Nombres que revelan intención (`_validate_move`, `_detect_winner`)
- No comentar el QUÉ, sino el POR QUÉ (y solo cuando no es obvio)
- `# noqa: E741` para suprimir reglas del linter cuando tiene sentido

### Configuración profesional
```python
# pydantic-settings lee variables de entorno automáticamente
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    app_name: str = "Gato API"
    port: int = 8000
    debug: bool = False

settings = Settings()
```
- `.env` → valores locales (nunca al repo)
- `.env.example` → plantilla pública (sí al repo)

---

## Módulo 2 — Estructura de Proyecto

### Arquitectura en capas
```
app/
├── domain/      → entidades puras (Game, Player, GameStatus)
├── repository/  → acceso a datos (Protocol + implementación)
├── service/     → reglas de negocio
└── api/         → HTTP (routes, middleware, dependencies)
```
Regla: cada capa solo importa de las capas por debajo de ella.

### Gestión de dependencias con uv
```bash
uv lock                  # generar/actualizar uv.lock
uv sync                  # instalar dependencias de producción
uv sync --extra dev      # instalar dependencias de desarrollo
```

### pyproject.toml — todo en un archivo
```toml
[project]
dependencies = ["fastapi", "uvicorn", "pydantic-settings"]

[project.optional-dependencies]
dev = ["pytest", "ruff", "black", "pytest-cov"]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "UP"]
```

---

## Módulo 3 — Pruebas Automatizadas

### Anatomía de un test — patrón AAA
```python
def test_create_game_estado_inicial(service):
    # Arrange — preparar
    # (fixture service ya está listo)

    # Act — ejecutar
    game = service.create_game()

    # Assert — verificar
    assert game.board == [None] * 9
    assert game.current_player == Player.X
    assert game.status == GameStatus.ONGOING
```

### pytest — comandos clave
```bash
python -m pytest                              # todos los tests
python -m pytest tests/ -v                   # verbose
python -m pytest tests/test_api.py::test_x   # un test específico
python -m pytest --cov=app                   # con cobertura
python -m pytest --cov=app --cov-report=term-missing  # líneas sin cubrir
```

### Fixtures y conftest
```python
# conftest.py — fixtures compartidas entre archivos
@pytest.fixture
def service():
    return GameService(repo=InMemoryGameRepository())

# Fixture que depende de otra (fixture chaining)
@pytest.fixture
def game(service):
    return service.create_game()
```

### Mocking
```python
from unittest.mock import MagicMock

def test_create_game_llama_save():
    repo = MagicMock()
    service = GameService(repo=repo)

    game = service.create_game()

    repo.save.assert_called_once_with(game)     # verificar llamada
    repo.find_by_id.return_value = None          # controlar retorno
```

### Integration testing con TestClient
```python
from fastapi.testclient import TestClient
from app.api.routes import app

@pytest.fixture
def client():
    fresh_service = GameService(repo=InMemoryGameRepository())
    app.dependency_overrides[get_service_singleton] = lambda: fresh_service
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_crear_partida(client):
    response = client.post("/games")
    assert response.status_code == 200
    assert response.json()["status"] == "ongoing"
```

### TDD — Red → Green → Refactor
1. Escribir el test (falla — Red)
2. Escribir el mínimo código para pasar (Green)
3. Refactorizar sin romper (Refactor)

### Cobertura — umbral automático
```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=app --cov-fail-under=85"
```

---

## Módulo 4 — Documentación

### Docstrings Google style
```python
def make_move(self, game_id: UUID, player: Player, position: int) -> Game:
    """Aplica un movimiento en una partida en curso.

    El tablero usa índices 0-8, de izquierda a derecha, arriba-abajo.

    Args:
        game_id: ID de la partida.
        player: Jugador que hace el movimiento.
        position: Posición en el tablero (0-8).

    Returns:
        Estado actualizado del juego.

    Raises:
        KeyError: Si game_id no existe.
        ValueError: Si el movimiento viola una regla del juego.
    """
```
- Documentar solo lo NO obvio: formato de parámetros, excepciones, restricciones
- Métodos privados (`_nombre`) no necesitan docstring

### README efectivo
Estructura mínima:
1. Descripción (2-3 líneas)
2. Requisitos
3. Instalación (comandos ejecutables)
4. Uso (ejemplos curl reales)
5. Desarrollo (tests, linting)

### OpenAPI con FastAPI
FastAPI genera `/docs` automáticamente desde type hints.
```python
# Enriquecer con ejemplos
class MoveRequest(BaseModel):
    player: Player
    position: int
    model_config = {"json_schema_extra": {"example": {"player": "X", "position": 0}}}

# Metadata de la app
app = FastAPI(title="Gato API", version="0.1.0", description="...")
```

---

## Módulo 5 — Git Profesional

### Conventional Commits
```
type(scope): descripción

feat: nueva funcionalidad
fix: corrección de bug
docs: solo documentación
refactor: cambio sin nueva funcionalidad ni bug fix
test: agregar o corregir tests
chore: mantenimiento (deps, config)
ci: cambios en CI/CD
```

### Flujo trunk-based
```bash
git checkout -b feature/nombre   # nueva rama
# ... commits ...
git checkout master
git merge feature/nombre
git branch -d feature/nombre     # limpiar
```

### Comandos Git esenciales
```bash
git log --oneline -5             # historial resumido
git stash                        # guardar trabajo sin commitear
git stash pop                    # recuperar
git branch                       # ver ramas
git checkout -b nombre           # crear y cambiar a rama
git merge nombre                 # merge a la rama actual
git branch -d nombre             # eliminar rama mergeada
```

### pre-commit hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
```
```bash
pre-commit install          # activar (una sola vez por repo)
pre-commit run --all-files  # correr manualmente
```

---

## Módulo 6 — CI/CD y Producción

### GitHub Actions
```yaml
# .github/workflows/ci.yml
jobs:
  test:
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: uv sync --extra dev
      - run: python -m ruff check .
      - run: python -m black --check .
      - run: python -m pytest --cov=app --cov-fail-under=85

  deploy:
    needs: test                    # solo si test pasa
    if: github.ref == 'refs/heads/master'
    steps:
      - run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK }}"
```

### Docker multi-stage
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen --no-install-project

FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "app.api.routes:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker compose up --build    # levantar con Docker Compose
docker compose down          # detener
```

### Render — deploy
```yaml
# render.yaml
services:
  - type: web
    name: gato-api
    buildCommand: pip install uv && uv sync --no-dev --frozen
    startCommand: uvicorn app.api.routes:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
```

### Health check y logs
```python
# Health check
@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "version": settings.app_version}

# Logger centralizado
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    # formato: timestamp | nivel | módulo | mensaje
    ...
```

---

## FastAPI — capacidades

| Feature | Para qué |
|---------|----------|
| Routes | mapear URL + método HTTP a función |
| Path params | `/games/{id}` — extraídos automáticamente |
| Query params | `?status=ongoing` — opcionales con defaults |
| Request body | JSON validado con Pydantic |
| Response model | filtrar campos en la respuesta |
| Status codes | `status_code=201` para crear, `204` para delete |
| HTTPException | errores HTTP con código y mensaje |
| Depends | inyección de dependencias reutilizable |
| APIRouter | agrupar endpoints en archivos separados |
| StaticFiles | servir HTML/CSS/JS |
| CORS Middleware | permitir llamadas desde el browser |
| Exception handlers | manejar excepciones globalmente |
| Background tasks | trabajo asíncrono post-respuesta |
| Lifespan events | startup/shutdown (conectar BD) |
| Validators Pydantic | validación personalizada de campos |
| WebSockets | comunicación en tiempo real |
| File upload | recibir archivos del cliente |
| Streaming | enviar datos progresivamente |

---

## Estructura final del proyecto

```
gato/
├── app/
│   ├── api/
│   │   ├── dependencies.py   ← get_service_singleton
│   │   ├── routes.py         ← endpoints principales
│   │   └── stats.py          ← APIRouter de /stats
│   ├── domain/
│   │   └── models.py         ← Game, Player, GameStatus, MoveRequest
│   ├── repository/
│   │   ├── base.py           ← GameRepository (Protocol)
│   │   └── memory.py         ← InMemoryGameRepository
│   ├── service/
│   │   └── game_service.py   ← reglas del juego
│   ├── config.py             ← Settings con pydantic-settings
│   └── logger.py             ← logger centralizado
├── tests/
│   ├── conftest.py           ← fixtures compartidas
│   ├── test_api.py           ← integration tests
│   ├── test_game_service.py  ← unit tests
│   └── test_game_service_mock.py ← tests con mocks
├── static/
│   └── index.html            ← UI del juego
├── .github/
│   ├── workflows/ci.yml      ← GitHub Actions
│   └── pull_request_template.md
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── pyproject.toml
├── uv.lock
├── .env.example
├── .pre-commit-config.yaml
├── CHANGELOG.md
└── COMANDOS.md
```
