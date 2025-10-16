#!/usr/bin/env bash
set -euo pipefail
cd ~/h100-inference

file=docker-compose.yml
backup="${file}.bak.$(date +%s)"
cp "$file" "$backup"

python3 - "$file" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1])
lines = path.read_text().splitlines()

filtered = [ln for ln in lines if not ln.strip().lower().startswith('ollama_host:')]
filtered = [ln for ln in filtered if ln.strip() != 'command: ["serve", "--host", "0.0.0.0"]']

for idx, ln in enumerate(filtered):
    if ln.strip() == 'environment:':
        filtered.insert(idx + 1, '      OLLAMA_HOST: http://127.0.0.1:11434')
        break
else:
    filtered.append('    environment:')
    filtered.append('      OLLAMA_HOST: http://127.0.0.1:11434')

path.write_text("\n".join(filtered) + "\n")
PY

echo "Updated docker-compose.yml (backup at $backup)"
