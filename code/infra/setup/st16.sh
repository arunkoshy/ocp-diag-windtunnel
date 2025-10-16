#!/bin/bash
echo "Step 16: pull with debug logs"

docker compose exec -e OLLAMA_DEBUG=debug ollama ollama pull phi3:mini 2>&1 | tee pull_debug.log

echo "Step 16 complete."
