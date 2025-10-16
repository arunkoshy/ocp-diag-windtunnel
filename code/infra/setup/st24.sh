#!/bin/bash

echo "Step 24: test registry using helper curl container"

docker run --rm \
  --network container:h100-ollama \
  -e HTTP_PROXY=http://sampleproxy:443 \
  -e HTTPS_PROXY=http://sampleproxy:443 \
  -e ALL_PROXY=http://sampleproxy:443 \
  -e NO_PROXY=127.0.0.1,localhost \
  curlimages/curl:8.5.0 \
  curl -v https://registry.ollama.ai/v2/library/phi3/manifests/mini -o /tmp/phi3-manifest.json

echo "Step 24 complete."
