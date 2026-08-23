#!/bin/bash
# ============================================================
# create_duckdb.sh
#
# Creates a DuckDB version of the "employee" database (a DuckDB
# equivalent of ../mysql/dataset_small). Everything this script
# needs lives under duckdb/ -- it does NOT read from ../mysql/.
#
# Usage:
#   cd duckdb
#   ./create_duckdb.sh
#
# Result:
#   duckdb/employee.duckdb  -- a ready-to-query DuckDB database with:
#     - department, employee, dept_emp, dept_manager, title, salary
#     - dept_emp_latest_date, current_dept_emp views
#     - 3 employees with no department (see sql/03_*.sql)
#     - 3 departments with no employees (see sql/04_*.sql)
#     - emp_dept_id, emp_dept_name, emp_name, current_manager macros,
#       v_full_employee, v_full_department views, and show_department()
#       / employee_help() table macros (see sql/06_object.sql)
# ============================================================

set -euo pipefail

# Always run from the duckdb/ directory, regardless of where the
# script is invoked from, so the relative paths in the .sql files
# (e.g. 'data/employee.csv') resolve correctly.
cd "$(dirname "${BASH_SOURCE[0]}")"

DB_FILE="employee.duckdb"

if ! command -v duckdb >/dev/null 2>&1; then
    echo "ERROR: the 'duckdb' CLI is not on your PATH." >&2
    echo "Install it from https://duckdb.org/docs/installation/ and try again." >&2
    exit 1
fi

echo "Removing any existing ${DB_FILE} ..."
rm -f "${DB_FILE}"

echo "Creating schema ..."
duckdb "${DB_FILE}" < sql/01_schema.sql

echo "Loading base data (9 departments, 1000 employees) ..."
duckdb "${DB_FILE}" < sql/02_load_data.sql

echo "Adding 3 employees with no department ..."
duckdb "${DB_FILE}" < sql/03_extra_unassigned_employees.sql

echo "Adding 3 departments with no employees ..."
duckdb "${DB_FILE}" < sql/04_extra_empty_departments.sql

echo "Creating views ..."
duckdb "${DB_FILE}" < sql/05_views.sql

echo "Creating macros, views, and table macros (object.sql port) ..."
duckdb "${DB_FILE}" < sql/06_object.sql

echo
echo "Done. Row counts:"
duckdb "${DB_FILE}" -c "
    SELECT 'department'    AS table_name, COUNT(*) AS row_count FROM department
    UNION ALL SELECT 'employee',      COUNT(*) FROM employee
    UNION ALL SELECT 'dept_emp',      COUNT(*) FROM dept_emp
    UNION ALL SELECT 'dept_manager',  COUNT(*) FROM dept_manager
    UNION ALL SELECT 'title',         COUNT(*) FROM title
    UNION ALL SELECT 'salary',        COUNT(*) FROM salary
    ORDER BY table_name;
"

echo
echo "Created ${PWD}/${DB_FILE}"
