#!/usr/bin/env bash
set -euo pipefail
cd ~/h100-inference

file=docker-compose.yml
cp "$file" "${file}.bak.$(date +%s)"

python3 - "$file" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1])
lines = path.read_text().splitlines()

updated = []
for line in lines:
    if line.strip().startswith('OLLAMA_HOST:'):
        updated.append('      OLLAMA_HOST: http://0.0.0.0:11434')
    else:
        updated.append(line)

path.write_text("\n".join(updated) + "\n")
PY
