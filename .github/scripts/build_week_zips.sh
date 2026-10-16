#!/usr/bin/env bash
# Build one ZIP per week for students who do not use git.
#
#   weekNN-topic.zip
#   └── weekNN-topic/
#       ├── lectures/   ← weekly_lectures/weekNN-topic/
#       └── review/     ← weekly_reviews/weekNN-topic/
#
# Run from the repo root. GitHub Actions runs it on a fresh checkout,
# so only tracked files go into the ZIPs — gitignored answer keys and
# CLAUDE.md files never do.
#
# Usage: .github/scripts/build_week_zips.sh [output_dir]   (default: dist)
set -euo pipefail

out="${1:-dist}"
mkdir -p "$out"
out="$(cd "$out" && pwd)"
stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT

for lec in weekly_lectures/week*/; do
  week="$(basename "$lec")"
  mkdir -p "$stage/$week"
  cp -R "weekly_lectures/$week" "$stage/$week/lectures"
  if [ -d "weekly_reviews/$week" ]; then
    cp -R "weekly_reviews/$week" "$stage/$week/review"
  fi
  rm -f "$out/$week.zip"
  (cd "$stage" && zip -rqX "$out/$week.zip" "$week" \
      -x '*/.DS_Store' '*/__pycache__/*' '*/__marimo__/*')
  echo "built $week.zip"
done
