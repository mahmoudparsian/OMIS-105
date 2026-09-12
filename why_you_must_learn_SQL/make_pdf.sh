#!/usr/bin/env bash
# DEFAULT PDF pipeline: regenerate why_you_must_learn_SQL.pdf from the .md via
# real LaTeX typesetting (pandoc -> xelatex). See make_pdf_html.sh for the
# older HTML/Chrome route (kept as a fallback for machines without a LaTeX
# install).
#
# Why LaTeX: proper justified text, hyphenation, and kerning — noticeably
# more polished than a browser print for prose-heavy pages. The one thing it
# does NOT handle out of the box is this doc's reference tables: cells like
# `products.product_id` have no space/hyphen for LaTeX to break on, so a
# column just overflows into the next one. fix_table_widths.lua works around
# that:
#   1. sizes each table column from its longest cell instead of pandoc's
#      default (equal widths based on the markdown separator row), and
#   2. wraps inline code inside table cells in \seqsplit, which allows a
#      break between any two characters as a last resort.
#
# No --toc / --number-sections: the .md already has its own hand-built
# "## Table of Contents" section right after the title block, linking to
# <a id="section-N"></a> anchors placed before each numbered heading (plain
# raw-HTML anchors, not pandoc's {#id} attribute syntax — chosen so the .md
# still renders correctly as plain Markdown on GitHub). Pandoc's automatic
# --toc would print a second, redundant TOC *before* the title, and
# --number-sections would double up with the numbers already in the heading
# text (e.g. "2.1 1 — The Question..."). PDF sidebar bookmarks still work
# without --toc — hyperref generates those from the headings regardless.
#
# fix_anchors.lua makes those <a id="section-N"></a> anchors resolve in the
# PDF too: pandoc's LaTeX writer otherwise just drops raw HTML it can't use,
# so the manual TOC's links would point at nothing.
#
# fix_image_sizing.lua gives images in the PDF a sane width (the .md has no
# {width=...} attribute on them, for the same GitHub-portability reason).
#
# Requires: pandoc, a LaTeX install with xelatex (e.g. MacTeX / BasicTeX).
#
# Usage:
#   ./make_pdf.sh [output.pdf]     # defaults to why_you_must_learn_SQL.pdf

set -euo pipefail
cd "$(dirname "$0")"

MD="why_you_must_learn_SQL.md"
PDF="${1:-why_you_must_learn_SQL.pdf}"

if ! command -v xelatex >/dev/null 2>&1; then
  echo "error: xelatex not found. Install MacTeX or BasicTeX, then retry." >&2
  exit 1
fi

echo "==> pandoc + xelatex: $MD -> $PDF"
pandoc "$MD" -o "$PDF" \
  --pdf-engine=xelatex \
  --lua-filter=fix_table_widths.lua \
  --lua-filter=fix_anchors.lua \
  --lua-filter=fix_image_sizing.lua \
  -V geometry:margin=1in \
  -V mainfont="Arial Unicode MS" \
  -V monofont="Menlo" \
  -V fontsize=11pt \
  -V linkcolor=blue \
  -V header-includes="\usepackage{seqsplit}\usepackage{float}" \
  --syntax-highlighting=tango

echo "==> done: $PDF"
