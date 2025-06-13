#!/bin/bash
set -e

echo "▶️ Applying Alembic migrations..."
alembic upgrade head

echo "🌱 Running seed script..."
python -m app.db.seed


echo "🚀 Starting FastAPI..."
exec uvicorn app.api.main:app --host 0.0.0.0 --port 8000
