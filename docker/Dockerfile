FROM python:3.12-slim-bullseye

WORKDIR /usr/src

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc

RUN pip3 install --upgrade pip setuptools wheel uv

COPY ./uv.lock /usr/src/uv.lock
COPY ./pyproject.toml /usr/src/pyproject.toml

RUN python -m uv sync --frozen --no-cache --no-dev && rm -rf /root/.cache/pip

WORKDIR /usr/src/app