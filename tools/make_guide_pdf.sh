#!/bin/sh
# Rebuild "Pakka - Explained.pdf" from GUIDE.md.
#
# pandoc for the structure, then Chromium for the paged output. weasyprint
# would be the tidier choice but it wants native libraries that are not always
# there; a headless browser is already on any machine that runs the tests.
set -e
cd "$(dirname "$0")/.."
OUT="${TMPDIR:-/tmp}/pakka-guide"
mkdir -p "$OUT"

pandoc GUIDE.md -f markdown+pipe_tables-blank_before_blockquote -t html5 -s \
  --metadata title="Pakka, explained" -o "$OUT/body.html"

python3 - "$OUT" <<'PY'
import pathlib, sys
out = pathlib.Path(sys.argv[1])
body = (out / "body.html").read_text()
css = pathlib.Path("tools/guide-pdf.css").read_text()
(out / "guide.html").write_text(body.replace("</head>", f"<style>\n{css}\n</style>\n</head>", 1))
PY

# playwright is a dev-only dependency and may live in an npx cache rather than
# beside this repo, so find it rather than assuming
PW=$(node -e 'try{console.log(require.resolve("playwright"))}catch(e){}' 2>/dev/null)
if [ -z "$PW" ]; then
  PW=$(find "$HOME/.npm/_npx" "$HOME/node_modules" -maxdepth 4 -type d -name playwright 2>/dev/null | head -1)
  [ -n "$PW" ] && NODE_PATH=$(dirname "$PW") && export NODE_PATH
fi
if ! node -e 'require("playwright")' 2>/dev/null; then
  echo "playwright not found. Install it with: npm i -g playwright" >&2
  exit 1
fi

PAKKA_OUT="$OUT" node -e '
const { chromium } = require("playwright");
const out = process.env.PAKKA_OUT;
(async () => {
  const exe = process.env.PAKKA_CHROME || undefined;
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage();
  await p.goto("file://" + out + "/guide.html", { waitUntil: "networkidle" });
  await p.emulateMedia({ media: "print" });
  await p.pdf({ path: "Pakka - Explained.pdf", format: "A4", printBackground: true,
    margin: { top: "18mm", bottom: "16mm", left: "17mm", right: "17mm" },
    displayHeaderFooter: true, headerTemplate: "<div></div>",
    footerTemplate: `<div style="width:100%;font-family:Times New Roman,serif;font-size:8pt;color:#888;padding:0 17mm;display:flex;justify-content:space-between"><span>Pakka, explained</span><span class="pageNumber"></span></div>` });
  await b.close();
})();
'
echo "wrote Pakka - Explained.pdf"
