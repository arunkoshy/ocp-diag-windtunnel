#!/bin/bash

echo "Step 27: pull with live debug output"

docker logs -f h100-ollama &
LOGPID=$!
sleep 2

docker compose exec ollama ollama pull phi3:mini

sleep 1
kill $LOGPID 2>/dev/null

echo "Step 27 complete."
