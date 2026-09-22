#!/usr/bin/env bash
# Wrapper for Problem #1: 
#   build the DuckDB users table, then dedupe
#   keeping the oldest entry per email.
#
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "==> Step 1: creating and seeding DuckDB 'users' table"
python3 db_setup.py

echo
echo "==> Step 2: deduplicating (keep oldest entry per email)"
python3 problem1_keep_oldest.py
