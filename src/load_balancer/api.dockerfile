FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

# Install curl
RUN apt-get update; apt-get install -y curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY ./app /app/app

ENV MODULE_NAME=app.run_app


