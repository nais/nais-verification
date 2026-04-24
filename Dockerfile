ARG PY_VERSION=3.12

FROM jdxcode/mise:latest AS base
WORKDIR /app

# Pre-install lots of tools
RUN --mount=type=cache,target=/root/.cache/mise \
    --mount=type=bind,target=/app \
    mise trust -a && \
    mise install

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0
ENV UV_NO_EDITABLE=1
ENV UV_PROJECT_ENVIRONMENT=/venv


FROM base AS build

# Load mise config and project files and run install with that config
COPY .mise-tasks ./.mise-tasks/
COPY mise.toml pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/mise \
    mise trust -a && mise install

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Load sources and install project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,target=/app,rw \
    uv sync --locked

# Run ci tasks
RUN --mount=type=bind,target=/app,rw \
    mise run ci

# Remove dev dependencies
ENV UV_NO_DEV=1
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,target=/app,rw \
    uv sync --locked

RUN ${UV_PROJECT_ENVIRONMENT}/bin/python -c "import nais_verification" ## Minimal testing that imports actually work


FROM python:${PY_VERSION}-slim AS docker
WORKDIR /app

# Load built virtualenv
COPY --from=build /venv /app/.venv
# Retarget virtualenv to the python in this image
RUN ln --force --logical --symbolic --target-directory /app/.venv/bin /usr/local/bin/python*

# Set PATH putting virtualenv first
ENV PATH="/app/.venv/bin:/bin:/usr/bin:/usr/local/bin"
# Test that the virtualenv still actually works
RUN python -c "import nais_verification" ## Minimal testing that imports actually work

ENTRYPOINT ["python", "/app/.venv/bin/nais-verification"]
