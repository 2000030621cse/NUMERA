# ── Stage 1: build frontend ──────────────────────────────────────────
FROM node:22-bookworm-slim AS frontend

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install -g npm@12.0.2 && npm ci --no-audit --no-fund

COPY frontend/ ./
RUN npm run build

# ── Stage 2: FastAPI + static SPA ────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    STATIC_DIR=/app/static

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY --from=frontend /frontend/dist ./static

EXPOSE 8080

# Cloud Run sets PORT; bind all interfaces.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
