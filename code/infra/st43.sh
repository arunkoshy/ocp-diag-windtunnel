#!/usr/bin/env bash
set -euo pipefail
cd ~/h100-inference

python3 -m venv .venv
. .venv/Scripts/activate
pip install --upgrade pip requests

cat <<'PY' > ollama_demo.py
import requests, sys, json

url = "http://127.0.0.1:11434/api/generate"
payload = {"model": "deepseek-r1:32b", "prompt": sys.argv[1] if len(sys.argv) > 1 else "Hello from Python."}
resp = requests.post(url, json=payload, stream=True)
for line in resp.iter_lines():
    if line:
        data = json.loads(line)
        if chunk := data.get("response"):
            print(chunk, end="", flush=True)
        if data.get("done"):
            print()
            break
PY
