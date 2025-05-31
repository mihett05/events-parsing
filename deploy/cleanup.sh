#!/bin/sh
set -euo pipefail

REGISTRY="http://registry:5000"
KEEP=5

echo "Starting registry cleanup..."
apk add --no-cache curl jq >/dev/null

# Verify registry connectivity
if ! curl -sS --retry 3 --retry-delay 2 "$REGISTRY/v2/_catalog" >/dev/null; then
  echo "ERROR: Could not connect to registry at $REGISTRY"
  echo "Troubleshooting:"
  echo "1. Ensure registry container is running"
  echo "2. Verify network connectivity between containers"
  echo "3. Check registry URL"
  exit 1
fi

REPOS=$(curl -sS "$REGISTRY/v2/_catalog" \
  | jq -r '.repositories[]' \
  | sort)

echo "Discovered repositories: $(echo $REPOS | tr '\n' ' ')"

for REPO in $REPOS; do
  echo "Processing repository: $REPO"

  TAGS=$(curl -sS "$REGISTRY/v2/$REPO/tags/list" \
    | jq -r '.tags[] // empty' \
    | sort)

  if [ -z "$TAGS" ]; then
    echo "  No tags found, skipping."
    continue
  fi

  echo "  Found ${TAGS} tags"
  TIMESTAMP_FILE=$(mktemp)
  while read -r TAG; do
    echo "  - Fetching $TAG"
    MANIFEST=$(curl -sS -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
      "$REGISTRY/v2/$REPO/manifests/$TAG")

    CONFIG_DIGEST=$(echo "$MANIFEST" | jq -r '.config.digest')
    
    if [ -z "$CONFIG_DIGEST" ] || [ "$CONFIG_DIGEST" = "null" ]; then
      echo "    ! Could not get config digest, using default timestamp"
      CREATED="1970-01-01T00:00:00Z"
    else
      CONFIG_JSON=$(curl -sS "$REGISTRY/v2/$REPO/blobs/$CONFIG_DIGEST")
      CREATED=$(echo "$CONFIG_JSON" | jq -r '.created')
      CREATED=${CREATED:-1970-01-01T00:00:00Z}
    fi

    echo "$CREATED $TAG" >> "$TIMESTAMP_FILE"
  done <<EOF
$TAGS
EOF

  TO_KEEP_FILE=$(mktemp)
  sort -r "$TIMESTAMP_FILE" | head -n "$KEEP" | awk '{print $2}' > "$TO_KEEP_FILE"

  TO_DELETE=$(echo "$TAGS" | grep -xvF -f "$TO_KEEP_FILE" || true)

  rm -f "$TIMESTAMP_FILE" "$TO_KEEP_FILE"

  if [ -z "$TO_DELETE" ]; then
    TAG_COUNT=$(echo "$TAGS" | wc -l)
    echo "  All $TAG_COUNT tags are within the last $KEEP creations—nothing to delete."
    continue
  fi

  echo "  Deleting ${TO_DELETE} tags"
  for TAG in $TO_DELETE; do
    echo "  - Deleting $REPO:$TAG"
    DIGEST=$(curl -sSI -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
      "$REGISTRY/v2/$REPO/manifests/$TAG" \
      | awk -F': ' '/Docker-Content-Digest/ {print $2}' \
      | tr -d '\r')

    if [ -n "$DIGEST" ]; then
      curl -sS -X DELETE "$REGISTRY/v2/$REPO/manifests/$DIGEST" >/dev/null \
        && echo "    -> deleted digest $DIGEST"
    else
      echo "    ! could not find digest for $TAG"
    fi
  done
done

echo "Locating registry container for garbage collection..."
REGISTRY_CONTAINER=$(docker ps -q --filter label=com.docker.compose.service=registry)
if [ -z "$REGISTRY_CONTAINER" ]; then
  echo "Trying alternative container discovery..."
  REGISTRY_CONTAINER=$(docker ps -q --filter name=registry)
fi

if [ -z "$REGISTRY_CONTAINER" ]; then
  echo "ERROR: Failed to find registry container!"
  echo "Running containers:"
  docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
  exit 1
fi

echo "Found registry container: $REGISTRY_CONTAINER"
echo "Running garbage collection..."
docker exec -i "$REGISTRY_CONTAINER" \
  registry garbage-collect /etc/docker/registry/config.yml --delete-untagged=true

echo "Cleanup complete!"