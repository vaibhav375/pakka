#!/bin/sh
# GitHub Pages can only publish the repo root or /docs, and the app lives in
# web/. This mirrors it so the static demo and the Amplify deploy serve the
# identical files.
set -e
cd "$(dirname "$0")/.."
# stamp the service worker cache with this commit, so a deploy actually
# replaces what a returning visitor has cached
STAMP=$(git rev-parse --short HEAD 2>/dev/null || date +%s)
sed -i.bak "s/pakka-__BUILD__/pakka-$STAMP/" web/sw.js && rm -f web/sw.js.bak

# everything, not a list that silently goes stale when a file is added
cp web/* docs/
echo "docs/ synced from web/"
