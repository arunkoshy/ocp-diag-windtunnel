#!/usr/bin/env bash
set -euo pipefail
cd ~/h100-inference

docker compose up -d

echo "Waiting for Ollama..."
for _ in {1..20}; do
  if curl -sf http://127.0.0.1:11434/api/tags >/dev/null; then
    break
  fi
  sleep 2
done

curl -sS http://127.0.0.1:11434/api/tags | jq '.models[] | select(.name=="deepseek-r1:32b")'
