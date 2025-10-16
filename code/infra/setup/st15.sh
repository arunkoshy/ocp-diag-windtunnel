#!/bin/bash

echo "Step 15: inspect recent Ollama logs"

docker logs --tail=200 h100-ollama

echo "Step 15 complete."
