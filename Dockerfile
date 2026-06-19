# ─── STAGE 1: Dependencies ────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Copiamos SOLO requirements.txt primero (capa cacheable)
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ─── STAGE 2: Production ─────────────────────────────────────────
FROM python:3.11-slim AS production

LABEL org.opencontainers.image.description="Demo CI/CD Pipeline - Flask API"
LABEL org.opencontainers.image.source="https://github.com/alonsodon/demo-cicd-pipeline"

WORKDIR /app

# Copiamos dependencias instaladas del builder
COPY --from=builder /install /usr/local

# Copiamos el código
COPY app/ ./app/

# Instala curl (necesario para el HEALTHCHECK) y limpia la caché de apt en el mismo RUN
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Seguridad: usuario no-root
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000

# Docker sabe si el contenedor está sano antes de mandarle tráfico
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "flask", "--app", "app.main", "run", "--host=0.0.0.0", "--port=8000"]
