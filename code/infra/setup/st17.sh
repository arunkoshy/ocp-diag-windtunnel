#!/bin/bash

echo "Step 17: collect latest Ollama logs"

docker logs h100-ollama > ollama.log
tail -n 50 ollama.log

echo "Full log saved to ollama.log"
echo "Step 17 complete."
