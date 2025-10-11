#!/bin/bash

echo "Step 8: stop container and set GPU access"

docker compose down

cat > docker-compose.yml <<'EOF'
services:
  ollama:
    image: ollama/ollama:latest
    container_name: h100-ollama
    ports:
      - "11434:11434"
    volumes:
      - ./data/ollama:/root/.ollama
    environment:
      NVIDIA_VISIBLE_DEVICES: all
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
              count: all
              driver: nvidia
    restart: unless-stopped
EOF

cat docker-compose.yml

echo "Step 8 complete."
