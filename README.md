# Demo CI/CD Pipeline

A production-grade CI/CD pipeline for a Python Flask REST API, demonstrating modern DevOps practices.

![CI](https://github.com/alonsodon/demo-cicd-pipeline/actions/workflows/ci.yml/badge.svg)

## Pipeline Architecture

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│   PUSH to   │────▶│   lint      │────▶│   test (pytest)  │
│    main     │     │ flake8+black│     │                  │
└─────────────┘     └─────────────┘     └────────┬─────────┘
                                                 │ if main branch
                                                 ▼
                                         ┌──────────────────┐
                                         │   build & push   │
                                         │  Docker → GHCR   │
                                         │ (with GHA cache) │
                                         └──────────────────┘
```

## Stack

- **API:** Python 3.11, Flask
- **CI/CD:** GitHub Actions (3-stage pipeline)
- **Container:** Docker multi-stage build (builder + production)
- **Registry:** GitHub Container Registry (GHCR)
- **Quality:** flake8, black, pytest

## Run locally

```bash
# Without Docker
pip install -r requirements-dev.txt
flask --app app.main run --port 8000

# With Docker
docker build -t demo-api .
docker run -p 8000:8000 demo-api

# Pull the published image instead of building it yourself
docker pull ghcr.io/TU_USUARIO/demo-cicd-pipeline:latest
docker run -p 8000:8000 ghcr.io/TU_USUARIO/demo-cicd-pipeline:latest

# Run tests
pytest tests/ -v
```

## Endpoints

| Method | Path            | Description                           |
| ------ | --------------- | ------------------------------------- |
| GET    | `/health`       | Health check (status + uptime)        |
| GET    | `/greet/<name>` | Returns a greeting for `name`         |
| POST   | `/echo`         | Echoes back the JSON body it receives |

## Key decisions

- **Multi-stage Dockerfile**: separate build and production stages reduce final image size — the production image never contains build tools, only what's needed to run the app.
- **Health check**: the `/health` endpoint allows Docker and Kubernetes to know when the service is actually ready, replacing fragile `sleep N` patterns with a real readiness signal.
- **Layer caching**: `cache-from: type=gha` reuses unchanged Docker layers between CI runs, cutting build times significantly when only application code changes.
- **`needs: lint` / `needs: test`**: jobs are chained — the Docker build never runs if code quality checks or tests fail, preventing broken code from ever reaching the registry.
- **Non-root container user**: the production image runs as `appuser` instead of root, reducing the impact of a potential container compromise.
