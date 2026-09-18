#!/usr/bin/env bash
# Builds ecommerce_database.duckdb, the persistent on-disk database every
# notebook in this course connects to. Safe to re-run any time: it always
# rebuilds from the same seeded data in ecommerce_data.py, so the output
# file is byte-for-byte reproducible.
set -euo pipefail
cd "$(dirname "$0")"

python3 -c "
from ecommerce_data import build_database, DB_PATH
build_database()
print(f'Built {DB_PATH}')
"
