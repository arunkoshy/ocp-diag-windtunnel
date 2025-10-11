#!/bin/bash
echo "Step 19: tail logs while pulling"

docker logs -f h100-ollama &
LOGPID=$!
sleep 1

docker compose exec ollama ollama pull phi3:mini

sleep 1
kill $LOGPID 2>/dev/null
echo "Step 19 complete."
