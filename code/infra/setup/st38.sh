#!/usr/bin/env bash
set -euo pipefail
cd ~/h100-inference

docker compose exec ollama ollama pull deepseek-r1:32b
docker compose exec ollama ollama list
