#!/bin/bash

set -e
cd ~/fresh

echo "Step 4: prepare data directory"

mkdir -p data/ollama
echo "Created data/ollama"

ls -ld data data/ollama

echo "Step 4 complete."
