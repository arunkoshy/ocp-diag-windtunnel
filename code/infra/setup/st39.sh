#!/usr/bin/env bash
set -euo pipefail
cd ~/h100-inference

docker compose exec ollama ollama run deepseek-r1:32b "Give a one-sentence summary of why NVIDIA H100 GPUs are well-suited for large language models."
