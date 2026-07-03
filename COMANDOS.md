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

## Git — básico

```bash
git init                                # inicializar repositorio
git status                              # ver estado del repositorio
git add .                               # agregar todos los cambios al staging
git add archivo.py                      # agregar un archivo específico
git commit -m "mensaje"                 # hacer commit
git log --oneline                       # ver historial resumido
git log --oneline -5                    # ver últimos 5 commits
```

## Git — ramas

```bash
git branch                              # ver ramas existentes
git checkout -b nombre-rama             # crear y cambiar a nueva rama
git checkout main                       # volver a main/master
git merge nombre-rama                   # mergear rama en la rama actual
git branch -d nombre-rama              # eliminar rama ya mergeada
git rebase main                         # rebasar la rama actual sobre main
```

## Git — stash

```bash
git stash                               # guardar cambios sin commitear
git stash list                          # ver stashes guardados
git stash pop                           # recuperar el último stash
git stash drop                          # descartar el último stash
git checkout -- .                       # descartar todos los cambios no commiteados
```

## pre-commit

```bash
pre-commit install          # activar hooks en el repo local (una sola vez)
pre-commit run --all-files  # correr todos los hooks manualmente
pre-commit run ruff         # correr solo un hook específico
```

## Python

```bash
python -c "from app.api.routes import app; print('OK')"   # verificar imports
```
