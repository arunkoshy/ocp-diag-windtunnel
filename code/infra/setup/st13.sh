#!/bin/bash

echo "Step 13: review Ollama logs"

docker logs --tail=50 h100-ollama

echo "Step 13 complete."
