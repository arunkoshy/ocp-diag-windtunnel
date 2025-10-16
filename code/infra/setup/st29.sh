#!/bin/bash

echo "Step 29: curl registry from inside container"

docker compose exec ollama curl -sS \
  https://registry.ollama.ai/v2/library/phi3/manifests/mini \
  -o /tmp/phi3-manifest.json || { echo "curl failed"; exit 1; }

docker compose exec ollama ls -l /tmp/phi3-manifest.json
docker compose exec ollama head -n 5 /tmp/phi3-manifest.json

echo "Step 29 complete."
