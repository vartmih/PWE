FROM python:3.10 as pwe_api

RUN mkdir /PWE

COPY . /PWE

WORKDIR /PWE

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev