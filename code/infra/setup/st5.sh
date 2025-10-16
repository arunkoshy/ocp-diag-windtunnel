#!/bin/bash

echo "Step 5: start Ollama container"

if ! docker compose up -d ollama; then
  echo "docker compose up failed"
  exit 1
fi

docker compose ps

echo "Step 5 complete."
