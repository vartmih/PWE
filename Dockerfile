FROM python:3.10-slim

RUN mkdir -p /usr/src/app
COPY pyproject.toml /usr/src/app

WORKDIR usr/src/app

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev

COPY . .

ENV PYTHONPATH=/usr/src/app/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1