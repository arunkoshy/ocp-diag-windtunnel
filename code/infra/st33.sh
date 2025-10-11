#!/usr/bin/env bash
set -euo pipefail
cd ~/h100-inference

docker compose ps
docker inspect h100-ollama --format '{{.State.Status}}'
docker compose logs ollama --tail 50
