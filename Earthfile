VERSION 0.6

ARG PY_VERSION=3.10

build:
    FROM python:${PY_VERSION}-slim

    WORKDIR /app

    RUN pip install poetry poetry-plugin-bundle

    COPY pyproject.toml poetry.lock .
    RUN poetry install --no-root --no-interaction

    COPY --dir README.md .prospector.yaml nais_verification tests .
    RUN poetry install --no-interaction
    RUN poetry run prospector
    RUN poetry run pytest

    RUN poetry bundle venv --without=dev --clear venv
    SAVE ARTIFACT venv venv

docker:
    FROM python:${PY_VERSION}-slim

    WORKDIR /app
    ENV PYTHONPATH=/app/venv/lib/python${PY_VERSION}/site-packages

    COPY --dir +build/venv .
    ENTRYPOINT ["python", "/app/venv/bin/nais-verification"]

    # builtins must be declared
    ARG EARTHLY_GIT_PROJECT_NAME
    ARG EARTHLY_GIT_SHORT_HASH

    ARG IMAGE_BASE=$EARTHLY_GIT_PROJECT_NAME
    ARG VERSION=$EARTHLY_GIT_SHORT_HASH
    SAVE IMAGE --push ${IMAGE_BASE}:${VERSION} ${IMAGE_BASE}:latest
