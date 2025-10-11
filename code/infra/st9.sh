#!/bin/bash

echo "Step 9: start Ollama with GPU access"

docker compose up -d ollama || { echo "docker compose up failed"; exit 1; }

docker compose ps

echo "Step 9 complete."
