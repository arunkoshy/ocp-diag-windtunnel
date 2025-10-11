#!/usr/bin/env bash
set -euo pipefail
cd ~/h100-inference

file=docker-compose.yml
cp "$file" "${file}.bak.$(date +%s)"

python3 - "$file" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1])
lines = path.read_text().splitlines()

cleaned = [line for line in lines if line.strip().lower() != 'ollama_host:http://0.0.0.0:11434']
if not any(l.strip().startswith('command:') for l in cleaned):
    for i, line in enumerate(cleaned):
        if line.strip() == 'container_name: h100-ollama':
            cleaned.insert(i + 1, '    command: ["serve", "--host", "0.0.0.0"]')
            break

path.write_text("\n".join(cleaned) + "\n")
PY
