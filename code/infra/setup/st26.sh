#!/bin/bash

echo "Step 26: start Ollama (debug enabled)"

docker compose up -d ollama || { echo "docker compose up failed"; exit 1; }

docker logs --tail=20 h100-ollama

echo "Step 26 complete."
