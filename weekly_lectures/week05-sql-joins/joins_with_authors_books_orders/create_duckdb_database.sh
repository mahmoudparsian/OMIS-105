#!/bin/bash
# ============================================================
# create_duckdb_database.sh
#
# Builds the "authors_books_orders" DuckDB database from the two
# SQL files in this folder:
#   db_schema.sql   -- CREATE TABLE statements (authors, books, orders)
#   db_records.sql  -- INSERT statements (sample data)
#
# Usage:
#   cd joins_with_authors_books_orders
#   ./create_duckdb_database.sh
#
# Result:
#   authors_books_orders.duckdb -- a ready-to-query DuckDB database with:
#     - authors (6 rows)  -- 2 have no books (author_id 5 and 6)
#     - books   (20 rows) -- 3 categories: SPORT, BUSINESS, COMPUTERS;
#                            4 never ordered (B06, B12, B17, B20)
#     - orders  (80 rows) -- order dates in 2025
# ============================================================

set -euo pipefail

# Always run from this script's own directory, regardless of where
# it is invoked from, so the .sql files resolve correctly.
cd "$(dirname "${BASH_SOURCE[0]}")"

DB_FILE="authors_books_orders.duckdb"

if ! command -v duckdb >/dev/null 2>&1; then
    echo "ERROR: the 'duckdb' CLI is not on your PATH." >&2
    echo "Install it from https://duckdb.org/docs/installation/ and try again." >&2
    exit 1
fi

echo "Removing any existing ${DB_FILE} ..."
rm -f "${DB_FILE}"

echo "Creating schema (authors, books, orders) ..."
duckdb "${DB_FILE}" < db_schema.sql

echo "Loading records (6 authors, 20 books, 80 orders) ..."
duckdb "${DB_FILE}" < db_records.sql

echo
echo "Done. Row counts:"
duckdb "${DB_FILE}" -c "
    SELECT 'authors' AS table_name, COUNT(*) AS row_count FROM authors
    UNION ALL SELECT 'books',  COUNT(*) FROM books
    UNION ALL SELECT 'orders', COUNT(*) FROM orders
    ORDER BY table_name;
"

echo
echo "Created ${PWD}/${DB_FILE}"
