#!/bin/bash

echo "Step 1: Prerequisite check"

command -v docker >/dev/null || { echo "Docker missing"; exit 1; }
echo "Docker OK: $(docker --version)"

if docker compose version >/dev/null 2>&1; then
  echo "docker compose OK: $(docker compose version | head -n1)"
elif command -v docker-compose >/dev/null; then
  echo "docker-compose OK: $(docker-compose --version)"
else
  echo "Docker Compose missing"; exit 1;
fi

if command -v nvidia-smi >/dev/null; then
  echo "NVIDIA drivers OK"
  nvidia-smi | head -n 10
else
  echo "nvidia-smi missing"; exit 1;
fi

echo "Step 1 complete."
