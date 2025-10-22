FROM python:3.13-slim

WORKDIR /task_tracker

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.4

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY . .
