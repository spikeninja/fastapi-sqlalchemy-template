# Fastapi SQLAlchemy project template.
**Technologies used**: 
- FastAPI
- SQLAlchemy
- Pydantic
- Dishka
- Taskiq
- Redis
- PostgreSQL

## Installation
Install all dependencies by **uv**:

```shell
uv sync
```

## Development
1) Replace `PROJECT_NAME` prefix by your custom name in `compose-dev.yml`
2) Run `cp .env.example .env` and adjust all env variables
3) Run `docker compose -f compose-dev.yml up -d`.
4) Go to `http://localhost:8001/docs`.

## Production
1) Replace `PROJECT_NAME` prefix by your custom name in `compose.yml`
2) Run `cp .env.example .env` and adjust all env variables
3) Run `docker compose -f compose.yml up -d`.
4) Go to `http://localhost:8001/docs`.

## Migrations (WIP):