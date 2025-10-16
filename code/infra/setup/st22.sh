#!/bin/bash
echo "Step 22: restart Ollama and follow logs"

docker compose up -d ollama || { echo "failed to start"; exit 1; }

sleep 2
docker logs -f h100-ollama
