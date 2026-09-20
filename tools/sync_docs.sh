#!/bin/sh
# GitHub Pages can only publish the repo root or /docs, and the app lives in
# web/. This mirrors it so the static demo and the Amplify deploy serve the
# identical files.
set -e
cd "$(dirname "$0")/.."
# everything, not a list that silently goes stale when a file is added
cp web/* docs/
echo "docs/ synced from web/"
