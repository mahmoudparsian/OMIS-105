#!/usr/bin/env bash
# =============================================================================
# create_duckdb.sh  --  Build movies_db.duckdb from the converted SQL files.
#
# Usage:
#     ./create_duckdb.sh
#
# Requirements:
#     - DuckDB CLI on your PATH.  Install on macOS with:
#           brew install duckdb
#       or download from https://duckdb.org/docs/installation/
#
# What it does:
#     1. (Re)generates the DuckDB-compatible SQL in duckdb_sql/ from the
#        original MySQL dumps (only if python3 is available; safe to skip).
#     2. Builds a fresh movies_db.duckdb by loading the 12 SQL files in
#        dependency order (reference tables first, then movies, then the
#        junction/bridge tables).
#     3. Runs validation queries (table list + row counts + integrity).
# =============================================================================
set -euo pipefail

# Always run from the directory that contains this script.
cd "$(dirname "$0")"

DB="movies_db.duckdb"
SQL_DIR="duckdb_sql"

# --- 0. sanity: duckdb present? ------------------------------------------------
if ! command -v duckdb >/dev/null 2>&1; then
  echo "ERROR: the 'duckdb' CLI was not found on your PATH."
  echo "       Install it with:  brew install duckdb"
  echo "       or download from: https://duckdb.org/docs/installation/"
  exit 1
fi
echo ">> using $(duckdb --version)"

# --- 1. (re)generate converted SQL (optional) ---------------------------------
if command -v python3 >/dev/null 2>&1 && [ -f scripts/convert_to_duckdb.py ]; then
  echo ">> regenerating $SQL_DIR/ from the original MySQL dumps"
  python3 scripts/convert_to_duckdb.py
fi

# --- 2. build a fresh database -------------------------------------------------
echo ">> building $DB (fresh)"
rm -f "$DB"

# Load order matters: parents before children (FK enforcement).
FILES=(
  "$SQL_DIR/01_reference_data.sql"
  "$SQL_DIR/02_keyword.sql"
  "$SQL_DIR/03_person.sql"
  "$SQL_DIR/04_production_company.sql"
  "$SQL_DIR/05_movie.sql"
  "$SQL_DIR/06_movie_cast.sql"
  "$SQL_DIR/07_movie_company.sql"
  "$SQL_DIR/08_movie_crew.sql"
  "$SQL_DIR/09_movie_genres.sql"
  "$SQL_DIR/10_movie_keywords.sql"
  "$SQL_DIR/11_movie_languages.sql"
  "$SQL_DIR/12_production_country.sql"
)

# Build a single command stream of .read directives and pipe it to duckdb.
{
  for f in "${FILES[@]}"; do
    echo ".read ${f}"
  done
} | duckdb "$DB"

echo ">> load complete"

# --- 3. validate ---------------------------------------------------------------
echo ">> validating $DB"
duckdb "$DB" < "$SQL_DIR/validate.sql"

echo ""
echo ">> SUCCESS: $DB is ready.  Open an interactive session with:"
echo "       duckdb $DB"
