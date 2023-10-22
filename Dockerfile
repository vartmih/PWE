FROM python:3.10

RUN mkdir /PWE

COPY . /PWE

WORKDIR /PWE

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev