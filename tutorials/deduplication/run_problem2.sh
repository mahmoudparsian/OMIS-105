#!/usr/bin/env bash
# Wrapper for Problem #2: 
#   build the DuckDB users table, then dedupe
#   keeping the most recently verified entry per email.
#
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "==> Step 1: creating and seeding DuckDB 'users' table"
python3 db_setup.py

echo
echo "==> Step 2: deduplicating (keep most recently verified entry per email)"
python3 problem2_keep_most_recently_verified.py
