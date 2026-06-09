#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"

rm -rf "$DIST"
mkdir -p "$DIST"

rsync -a \
  --exclude='.git' \
  --exclude='.github' \
  --exclude='dist' \
  --exclude='node_modules' \
  --exclude='cloudflare-worker' \
  --exclude='scripts' \
  --exclude='README.md' \
  --exclude='.gitignore' \
  --exclude='.DS_Store' \
  --exclude='*.log' \
  --exclude='__pycache__' \
  "$ROOT/" "$DIST/"

echo "✓ Built $(find "$DIST" -type f | wc -l | tr -d ' ') files into $DIST"
