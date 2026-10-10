#!/bin/bash
# ============================================================
# create_duckdb_database.sh
#
# Builds the "students_courses_grades" DuckDB database from the two
# SQL files in this folder:
#
#   db_schema.sql   -- CREATE TABLE statements (students, courses, grades)
#   db_records.sql  -- INSERT statements (sample data)
#
# Usage:
#   cd joins_with_students_and_courses
#   ./create_duckdb_database.sh
#
# Result:
#   students_courses_grades.duckdb -- a ready-to-query DuckDB database with:
#       students:   500 rows
#       courses:     50 rows
#       grades:   8,000 rows
# ============================================================

set -euo pipefail

# Always run from this script's own directory, regardless of where
# it is invoked from, so the .sql files resolve correctly.
cd "$(dirname "${BASH_SOURCE[0]}")"

DB_FILE="students_courses_grades.duckdb"

if ! command -v duckdb >/dev/null 2>&1; then
    echo "ERROR: the 'duckdb' CLI is not on your PATH." >&2
    echo "Install it from https://duckdb.org/docs/installation/ and try again." >&2
    exit 1
fi

echo "Removing any existing ${DB_FILE} ..."
rm -f "${DB_FILE}"

echo "Creating schema (students, courses, grades) ..."
duckdb "${DB_FILE}" < db_schema.sql

echo "Loading records ..."
duckdb "${DB_FILE}" < db_records.sql

echo
echo "Done. Row counts:"
duckdb "${DB_FILE}" -c "
    SELECT 'students' AS table_name, COUNT(*) AS row_count FROM students
    UNION ALL SELECT 'courses',  COUNT(*) FROM courses
    UNION ALL SELECT 'grades', COUNT(*) FROM grades
    ORDER BY table_name;
"

echo
echo "Created ${PWD}/${DB_FILE}"
