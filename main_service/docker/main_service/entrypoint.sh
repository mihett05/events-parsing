#!/bin/bash


while ! poetry run alembic upgrade head  2>&1; do
  echo "Migration is in progress status"
  sleep 3
done

echo "Docker is fully configured successfully."

exec poetry run python3 main_service.py