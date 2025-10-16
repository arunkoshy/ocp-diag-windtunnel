#!/usr/bin/env bash
set -euo pipefail

curl -sS http://127.0.0.1:11434/api/tags | jq '.models[] | select(.name=="deepseek-r1:32b")'
