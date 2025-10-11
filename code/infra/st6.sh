#!/bin/bash

echo "Step 6: check Ollama status"

docker compose ps
docker logs --tail=20 h100-ollama

echo "Step 6 complete."
