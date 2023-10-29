FROM python:3.10

COPY . /usr/src/pwe

WORKDIR usr/src/pwe

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1