#!/usr/bin/env bash
# ALTERNATIVE PDF pipeline (fallback for machines without a LaTeX install).
# The default is make_pdf.sh, which uses pandoc + xelatex for real
# typesetting; this script instead regenerates why_you_must_learn_SQL.html
# and prints it to PDF via headless Chrome.
#
# Pipeline: pandoc (Markdown -> standalone HTML, styled by pdf_style.css)
#           -> headless Chrome (HTML -> PDF via --print-to-pdf)
# This is the same rendering path as "export HTML, open in Chrome, Save as PDF" —
# just scripted into one command instead of three manual steps.
#
# Requires: pandoc (brew install pandoc), Google Chrome.
#
# Usage:
#   ./make_pdf_html.sh [output.pdf]     # defaults to why_you_must_learn_SQL_html.pdf
#                                       # (pass why_you_must_learn_SQL.pdf to
#                                       # override the LaTeX-built default)

set -euo pipefail
cd "$(dirname "$0")"

MD="why_you_must_learn_SQL.md"
HTML="why_you_must_learn_SQL.html"
PDF="${1:-why_you_must_learn_SQL_html.pdf}"
CSS="pdf_style.css"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [[ ! -x "$CHROME" ]]; then
  echo "error: Google Chrome not found at: $CHROME" >&2
  echo "Edit CHROME= in this script if it's installed elsewhere." >&2
  exit 1
fi

echo "==> pandoc: $MD -> $HTML"
pandoc "$MD" -o "$HTML" \
  --standalone \
  --css="$CSS" \
  --metadata title="Why You Must Learn SQL" \
  --embed-resources \
  --syntax-highlighting=tango

echo "==> headless Chrome: $HTML -> $PDF"
"$CHROME" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PDF" \
  --print-to-pdf-no-header \
  "file://$(pwd)/$HTML" 2>/dev/null

echo "==> done: $PDF"
