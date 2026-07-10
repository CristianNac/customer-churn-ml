FROM python:3.13-slim-bookworm AS base
RUN pip install --no-cache-dir uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
WORKDIR /app

FROM base AS deps
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.13-slim-bookworm AS production
RUN groupadd --system app && useradd --system --gid app --create-home app
WORKDIR /app
COPY --from=deps --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app app/ ./

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app" \
    PYTHONUNBUFFERED=1

USER app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
