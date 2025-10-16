#!/bin/bash

echo "Step 11: add proxy variables to docker-compose"

HTTP_PROXY=${HTTP_PROXY:-http://sampleproxy:443}
HTTPS_PROXY=${HTTPS_PROXY:-http://sampleproxy:443}
ALL_PROXY=${ALL_PROXY:-http://sampleproxy:443}
NO_PROXY=${no_proxy:-127.0.0.1,localhost,}

docker compose down

cat > docker-compose.yml <<EOF
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
      HTTP_PROXY: $HTTP_PROXY
      HTTPS_PROXY: $HTTPS_PROXY
      ALL_PROXY: $ALL_PROXY
      http_proxy: $HTTP_PROXY
      https_proxy: $HTTPS_PROXY
      all_proxy: $ALL_PROXY
      NO_PROXY: $NO_PROXY
      no_proxy: $NO_PROXY
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

echo "Step 11 complete."
