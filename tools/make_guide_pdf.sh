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

node -e '
const { chromium } = require("playwright");
const out = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto("file://" + out + "/guide.html", { waitUntil: "networkidle" });
  await p.emulateMedia({ media: "print" });
  await p.pdf({ path: "Pakka - Explained.pdf", format: "A4", printBackground: true,
    margin: { top: "18mm", bottom: "16mm", left: "17mm", right: "17mm" },
    displayHeaderFooter: true, headerTemplate: "<div></div>",
    footerTemplate: `<div style="width:100%;font-family:Times New Roman,serif;font-size:8pt;color:#888;padding:0 17mm;display:flex;justify-content:space-between"><span>Pakka, explained</span><span class="pageNumber"></span></div>` });
  await b.close();
})();
' -- "$OUT"
echo "wrote Pakka - Explained.pdf"
