#!/bin/bash

echo "Step 23: curl from inside the container"

docker compose exec ollama curl -v --connect-timeout 15 \
  https://registry.ollama.ai/v2/library/phi3/manifests/mini \
  -o /tmp/phi3-manifest.json

STATUS=$?
echo "curl exit code: $STATUS"
docker compose exec ollama ls -l /tmp/phi3-manifest.json 2>/dev/null || true

echo "Step 23 complete."
