FROM python:3.12-slim-bullseye AS dependencies

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc

RUN pip install --upgrade pip setuptools wheel uv

RUN uv venv $VIRTUAL_ENV
COPY pyproject.toml uv.lock /usr/src/app/

WORKDIR /usr/src/app/
RUN uv pip install --requirement pyproject.toml
#RUN uv sync --frozen --no-dev --no-cache --active

FROM python:3.12-slim-bullseye AS production

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/usr/src

COPY --from=dependencies $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR /usr/src/