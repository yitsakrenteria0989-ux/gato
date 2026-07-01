# Changelog

## [0.1.0] - 2026-07-01

### Features
- Add TypeAlias Board and fix type hints
- Add Settings with pydantic-settings and .env support
- Add GET /games endpoint via TDD, fix test isolation with dependency override
- Add MoveRequest body schema and enrich OpenAPI metadata
- Add GET /games/{id}/board endpoint

### Refactors
- Extract GameService, main.py handles only HTTP
- Apply DIP with GameRepository Protocol
- Extract helper methods in GameService for clean code
- Reorganize into layered structure (domain/repository/service/api)
- Separate GameRepository Protocol from InMemoryGameRepository

### Tests
- Add first tests with fixtures and conftest
- Add move validation and turn change tests
- Add mock-based tests for repository interaction
- Add integration tests for HTTP endpoints
- Add coverage with pytest-cov, enforce 85% minimum

### Docs
- Add Google-style docstrings to GameService public methods
- Write complete README with installation, usage and dev sections
- Fix board diagram formatting in README
- Add git branching and stash commands to reference

### Chores
- Initial project setup
- Migrate to pyproject.toml with uv, add uv.lock
