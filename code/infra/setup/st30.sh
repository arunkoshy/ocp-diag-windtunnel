#!/bin/bash

echo "Step 30: call pulling API"

curl -sS -X POST http://localhost:11434/api/pull \
  -d '{"model":"phi3:mini","insecure":true}' \
  -o pull_response.json

cat pull_response.json

echo
echo "Step 30 complete."
