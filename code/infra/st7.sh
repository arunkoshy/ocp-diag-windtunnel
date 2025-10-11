#!/bin/bash

echo "Step 7: test Ollama API"

curl -s http://localhost:11434/api/tags || { echo "API request failed"; exit 1; }
echo

echo "Step 7 complete."
