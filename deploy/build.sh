#!/bin/bash

set -e

prompt_with_default() {
  local prompt="$1"
  local default="$2"
  local var_name="$3"
  local input=""

  while [ -z "$input" ]; do
    if [ -n "$default" ]; then
      read -r -p "$prompt (default: $default): " input
      input=${input:-$default}
    else
      read -r -p "$prompt: " input
    fi
  done

  eval "$var_name='$input'"
}

if [ -z "$REGISTRY" ]; then
  echo "REGISTRY environment variable not set."
  prompt_with_default "Enter Docker registry URL" "registry.events.lovepaw.ru" REGISTRY
else
  echo "Using registry from environment: $REGISTRY"
fi

if [ -z "$API_DOMAIN" ]; then
    echo "API_DOMAIN environment variable not set."
  prompt_with_default "Enter api domain" "api.events.lovepaw.ru" API_DOMAIN
else
  echo "Using api domain from environment: $API_DOMAIN"
fi

docker build -t $REGISTRY/main-service:latest ./main_service
docker push --all-tags $REGISTRY/main-service

docker build -t $REGISTRY/main-service-migrations:latest -f ./main_service/migrations.dockerfile ./main_service
docker push --all-tags $REGISTRY/main-service-migrations

docker build -t $REGISTRY/parser:latest ./parser
docker build -t $REGISTRY/frontend:latest ./frontend --build-arg VITE_BASE_API_URL=$API_DOMAIN