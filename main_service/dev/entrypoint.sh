#!/bin/bash


while ! poetry run alembic upgrade head  2>&1; do
  echo "Migration is in progress status"
  sleep 3
done

echo "Docker is fully configured successfully."

exec poetry run uvicorn infrastructure.server:app --host 0.0.0.0 --port 8000
