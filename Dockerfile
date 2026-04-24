ARG PY_VERSION=3.12

FROM python:${PY_VERSION}-slim AS build

WORKDIR /app

RUN pip install poetry poetry-plugin-bundle

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction

COPY README.md .prospector.yaml ./
COPY nais_verification/ ./nais_verification/
COPY tests/ ./tests/
RUN poetry install --no-interaction
RUN poetry run prospector
RUN poetry run pytest

RUN poetry bundle venv --without=dev --clear venv

FROM python:${PY_VERSION}-slim

ARG VERSION

WORKDIR /app
ENV PYTHONPATH=/app/venv/lib/python${PY_VERSION}/site-packages

COPY --from=build /app/venv /app/venv
ENTRYPOINT ["python", "/app/venv/bin/nais-verification"]
