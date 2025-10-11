#!/bin/bash
echo "Step 21: enable debug logging"

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
      HTTP_PROXY: http://sampleproxy:443
      HTTPS_PROXY: http://sampleproxy:443
      ALL_PROXY: http://sampleproxy:443
      http_proxy: http://sampleproxy:443
      https_proxy: http://sampleproxy:443
      all_proxy: http://sampleproxy:443
      NO_PROXY: 127.0.0.1,localhost
      no_proxy: 127.0.0.1,localhost
      OLLAMA_DEBUG: debug
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

echo "Step 21 complete."
