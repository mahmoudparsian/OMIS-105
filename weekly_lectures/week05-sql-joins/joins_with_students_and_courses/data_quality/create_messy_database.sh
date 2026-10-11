#!/bin/bash
# ============================================================
# create_messy_database.sh
#
# Builds the "students_courses_grades_messy" DuckDB database used by
# data_quality.py. It loads the clean data from the parent folder, then
# db_messy.sql copies it into raw_ tables with planted data-quality
# problems:
#
#   ../db_schema.sql   -- CREATE TABLE statements (students, courses, grades)
#   ../db_records.sql  -- INSERT statements (clean sample data)
#   db_messy.sql       -- raw_ copies + planted problems (SPOILER)
#
# Usage:
#   cd joins_with_students_and_courses/data_quality
#   ./create_messy_database.sh
#
# Result:
#   students_courses_grades_messy.duckdb -- with only these tables:
#       raw_students:   504 rows
#       raw_courses:     50 rows
#       raw_grades:   8,013 rows
#
# The clean database (create_duckdb_database.sh) is not touched.
# ============================================================

set -euo pipefail

# Always run from this script's own directory (data_quality/), regardless
# of where it is invoked from, so the .sql files resolve correctly.
cd "$(dirname "${BASH_SOURCE[0]}")"

DB_FILE="students_courses_grades_messy.duckdb"

if ! command -v duckdb >/dev/null 2>&1; then
    echo "ERROR: the 'duckdb' CLI is not on your PATH." >&2
    echo "Install it from https://duckdb.org/docs/installation/ and try again." >&2
    exit 1
fi

echo "Removing any existing ${DB_FILE} ..."
rm -f "${DB_FILE}"

echo "Loading clean schema and records ..."
duckdb "${DB_FILE}" < ../db_schema.sql
duckdb "${DB_FILE}" < ../db_records.sql

echo "Building raw_ tables with planted problems ..."
duckdb "${DB_FILE}" < db_messy.sql

echo
echo "Done. Row counts:"
duckdb "${DB_FILE}" -c "
    SELECT 'raw_students' AS table_name, COUNT(*) AS row_count FROM raw_students
    UNION ALL SELECT 'raw_courses', COUNT(*) FROM raw_courses
    UNION ALL SELECT 'raw_grades',  COUNT(*) FROM raw_grades
    ORDER BY table_name;
"

echo
echo "Created ${PWD}/${DB_FILE}"
