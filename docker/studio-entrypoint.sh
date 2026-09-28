#!/bin/bash
set -euo pipefail
for package in /workspace/studio/promo30 /workspace/studio/list-demo; do
    expected=$(sha256sum "$package/package-lock.json" | cut -d' ' -f1)
    actual=$(cat "$package/node_modules/.lock-hash" 2>/dev/null || true)
    if [ "$expected" != "$actual" ]; then
        (cd "$package" && npm ci --ignore-scripts && printf '%s\n' "$expected" > node_modules/.lock-hash)
    fi
done
exec "$@"
