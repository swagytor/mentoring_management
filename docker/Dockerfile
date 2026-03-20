# -----------------------------------------------------------
# Pre base image
# Installs base dependencies and sets up python
# -----------------------------------------------------------
FROM python:3.12 AS pre-base

WORKDIR /

RUN pip install pip==24.0 && \
    pip install poetry==1.8.3

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE=1

RUN poetry config virtualenvs.in-project true && \
    poetry config virtualenvs.create true && \
    poetry config cache-dir /tmp/poetry_cache

COPY ./app/poetry.lock ./app/pyproject.toml ./


# -----------------------------------------------------------
# Pre base image with dependencies for DEVELOPMENT
# Installs python dependencies with poetry
# -----------------------------------------------------------
FROM pre-base AS pre-base-dev-dependencies

RUN poetry install --no-interaction && \
    # clear poetry cache
    rm -rf /tmp/poetry_cache


# -----------------------------------------------------------
# Base image
# Copies python devendencies from pre base image for DEVELOPMENT and sets up python
# -----------------------------------------------------------
FROM python:3.12-slim AS dev-base

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE=1

RUN mkdir /app/
WORKDIR /app/

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

COPY --from=pre-base-dev-dependencies ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./app/ ./

# -----------------------------------------------------------
# Backend for DEVELOPMENT
# -----------------------------------------------------------
FROM dev-base AS dev-backend

WORKDIR /app/

COPY ./docker/backend/entrypoint.local.sh /entrypoint.sh

ENTRYPOINT ["bash", "/entrypoint.sh"]
