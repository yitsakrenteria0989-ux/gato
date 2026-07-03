# Stage 1: instalar dependencias
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen --no-install-project

# Stage 2: imagen de producción
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.api.routes:app", "--host", "0.0.0.0", "--port", "8000"]
