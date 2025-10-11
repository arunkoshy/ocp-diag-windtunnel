#!/bin/bash
echo "Step 28: install curl inside container"
docker compose exec ollama sh -c \
  "apt-get update && apt-get install -y curl ca-certificates"
echo "Step 28 complete."
