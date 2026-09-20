#!/bin/sh
# GitHub Pages can only publish the repo root or /docs, and the app lives in
# web/. This mirrors it so the static demo and the Amplify deploy serve the
# identical files.
set -e
cd "$(dirname "$0")/.."
cp web/index.html web/styles.css web/app.js web/config.js web/rules.generated.js docs/
echo "docs/ synced from web/"
