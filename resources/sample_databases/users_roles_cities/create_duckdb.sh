#!/bin/bash
# ============================================================
# create_duckdb.sh
#
# Builds the "users_roles_cities" DuckDB database from the two
# SQL files in this folder:
#   01_schema.sql   -- CREATE TABLE statements (roles, cities, users)
#   02_records.sql  -- INSERT statements (sample data)
#
# Usage:
#   cd users_roles_cities
#   ./create_duckdb.sh
#
# Result:
#   users_roles_cities.duckdb -- a ready-to-query DuckDB database with:
#     - roles   (5 rows)  -- 2 never assigned to a user (tester, QA)
#     - cities  (6 rows)  -- 2 with no residents (Cupertino, Detroit)
#     - users   (17 rows) -- some names repeat (Max, Barb, Jane)
# ============================================================

set -euo pipefail

# Always run from this script's own directory, regardless of where
# it is invoked from, so the .sql files resolve correctly.
cd "$(dirname "${BASH_SOURCE[0]}")"

DB_FILE="users_roles_cities.duckdb"

if ! command -v duckdb >/dev/null 2>&1; then
    echo "ERROR: the 'duckdb' CLI is not on your PATH." >&2
    echo "Install it from https://duckdb.org/docs/installation/ and try again." >&2
    exit 1
fi

echo "Removing any existing ${DB_FILE} ..."
rm -f "${DB_FILE}"

echo "Creating schema (roles, cities, users) ..."
duckdb "${DB_FILE}" < 01_schema.sql

echo "Loading records (5 roles, 6 cities, 17 users) ..."
duckdb "${DB_FILE}" < 02_records.sql

echo
echo "Done. Row counts:"
duckdb "${DB_FILE}" -c "
    SELECT 'roles'  AS table_name, COUNT(*) AS row_count FROM roles
    UNION ALL SELECT 'cities', COUNT(*) FROM cities
    UNION ALL SELECT 'users',  COUNT(*) FROM users
    ORDER BY table_name;
"

echo
echo "Created ${PWD}/${DB_FILE}"
