#!/bin/bash
echo "Step 18: show proxy env in container"
docker compose exec ollama env | grep -i proxy
echo "Step 18 complete."
