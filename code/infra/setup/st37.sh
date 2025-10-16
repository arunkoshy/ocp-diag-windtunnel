#!/usr/bin/env bash
set -euo pipefail
cd ~/h100-inference

docker compose exec ollama nvidia-smi --query-gpu=index,name,memory.total,memory.free --format=csv
docker compose exec ollama ollama --version
docker compose exec ollama ollama list
docker compose exec ollama ollama show phi3:mini | head -n 40
