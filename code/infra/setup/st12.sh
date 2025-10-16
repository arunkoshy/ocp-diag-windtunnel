#!/bin/bash

echo "Step 12: start Ollama with proxy + GPU"

docker compose up -d ollama || { echo "docker compose up failed"; exit 1; }

docker compose ps

echo "Step 12 complete."
