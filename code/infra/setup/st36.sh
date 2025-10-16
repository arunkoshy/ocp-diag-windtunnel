#!/usr/bin/env bash
set -euo pipefail

nvidia-smi --list-gpus
nvidia-smi --query-gpu=index,name,memory.total,memory.free,temperature.gpu --format=csv
nvidia-smi topo -m
