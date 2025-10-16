#!/bin/bash
# filepath: ~/st3.sh

set -e
cd ~/h100-inference

echo "Step 3: write docker-compose.yml"

cat > docker-compose.yml <<'EOF'
services:
  ollama:
    image: ollama/ollama:latest
    container_name: h100-ollama
    ports:
      - "11434:11434"
    volumes:
      - ./data/ollama:/root/.ollama
    restart: unless-stopped
EOF

echo "Created docker-compose.yml"
cat docker-compose.yml

echo "Step 3 complete."
