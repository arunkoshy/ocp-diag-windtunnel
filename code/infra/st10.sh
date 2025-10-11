#!/bin/bash

echo "Step 10: verify GPU status"

docker logs --tail=50 h100-ollama | grep -E "gpu|inference compute" || echo "No GPU entries yet"

echo "Step 10 complete."
