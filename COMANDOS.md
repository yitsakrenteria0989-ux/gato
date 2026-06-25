# Referencia de Comandos — Curso de Ingeniería de Software

## Ruff (linter)

```bash
python -m ruff check .                  # revisar todos los archivos
python -m ruff check archivo.py         # revisar un archivo específico
python -m ruff check --fix .            # corregir automáticamente lo que pueda
```

## Black (formateador)

```bash
python -m black .                       # formatear todos los archivos
python -m black archivo.py              # formatear un archivo específico
python -m black --check .               # verificar sin modificar (solo reporta)
```

## Pytest (tests)

```bash
python -m pytest                        # correr todos los tests
python -m pytest tests/ -v              # verbose (muestra nombre de cada test)
python -m pytest tests/test_api.py      # correr un archivo específico
python -m pytest tests/test_api.py::test_create_game   # correr un test específico

# Cobertura
python -m pytest --cov=app              # reporte de cobertura básico
python -m pytest --cov=app --cov-report=term-missing   # muestra líneas sin cubrir
```

## uv (gestor de dependencias)

```bash
uv lock                                 # generar/actualizar uv.lock
uv sync                                 # instalar dependencias de producción
uv sync --extra dev                     # instalar dependencias de desarrollo
```

## pip

```bash
pip install paquete==1.0.0              # instalar un paquete
pip install -r requirements.txt         # instalar desde archivo (método antiguo)
```

## Uvicorn (servidor)

```bash
uvicorn main:app --reload               # correr servidor con recarga automática
uvicorn app.api.routes:app --reload     # correr desde ruta específica
```

## Git

```bash
git init                                # inicializar repositorio
git status                              # ver estado del repositorio
git add .                               # agregar todos los cambios al staging
git add archivo.py                      # agregar un archivo específico
git commit -m "mensaje"                 # hacer commit
git log --oneline                       # ver historial resumido
```

## Python

```bash
python -c "from app.api.routes import app; print('OK')"   # verificar imports
```
