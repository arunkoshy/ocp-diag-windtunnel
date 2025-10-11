#!/bin/bash
# filepath: ~/st2.sh

set -e
WORKDIR=~/h100-inference

echo "Step 2: prepare workspace"

if [ -d "$WORKDIR" ]; then
  echo "Directory $WORKDIR already exists."
else
  mkdir -p "$WORKDIR"
  echo "Created $WORKDIR"
fi

ls -ld "$WORKDIR"

echo "Step 2 complete."
