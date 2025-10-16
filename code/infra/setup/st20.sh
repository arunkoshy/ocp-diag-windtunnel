#!/bin/bash

echo "Step 20: test curl to Ollama registry through proxy"

curl -v --connect-timeout 15 \
     --proxy http://sampleproxy:443 \
     https://registry.ollama.ai/v2/library/phi3/manifests/mini \
     -o /tmp/phi3-manifest.json

STATUS=$?
echo "curl exit code: $STATUS"
[ $STATUS -eq 0 ] && ls -l /tmp/phi3-manifest.json

echo "Step 20 complete."
