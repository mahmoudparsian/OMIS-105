#!/usr/bin/env bash
# Build one ZIP per week for students who do not use git.
#
#   weekNN-topic.zip          (and bonus-weekNN-topic.zip for weekly_lectures/bonus/)
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

# build_one <lectures_dir> <zip_name>
#   The review folder is the same path with weekly_reviews/ in front.
build_one() {
  local lec="${1%/}" name="$2"
  local week rev
  week="$(basename "$lec")"
  rev="weekly_reviews/${lec#weekly_lectures/}"
  rm -rf "$stage/$week"
  mkdir -p "$stage/$week"
  cp -R "$lec" "$stage/$week/lectures"
  if [ -d "$rev" ]; then
    cp -R "$rev" "$stage/$week/review"
  fi
  rm -f "$out/$name.zip"
  (cd "$stage" && zip -rqX "$out/$name.zip" "$week" \
      -x '*/.DS_Store' '*/__pycache__/*' '*/__marimo__/*')
  echo "built $name.zip"
}

for lec in weekly_lectures/week*/; do
  build_one "$lec" "$(basename "$lec")"
done

# Optional bonus weeks: weekly_lectures/bonus/weekNN-topic/
#   → bonus-weekNN-topic.zip (same lectures/ + review/ layout inside)
for lec in weekly_lectures/bonus/week*/; do
  [ -d "$lec" ] || continue
  build_one "$lec" "bonus-$(basename "$lec")"
done
