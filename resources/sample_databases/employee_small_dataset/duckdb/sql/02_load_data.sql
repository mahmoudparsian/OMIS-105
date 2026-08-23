-- ============================================================
-- 02_load_data.sql
-- Loads the base "employee" dataset (1000 employees, 9 departments)
-- from the CSV files under duckdb/data/ into the tables created by
-- 01_schema.sql. Paths are relative to duckdb/ (where create_duckdb.sh
-- runs the DuckDB CLI from).
-- ============================================================

COPY department  FROM 'data/department.csv'  (HEADER, AUTO_DETECT TRUE);
COPY employee    FROM 'data/employee.csv'    (HEADER, AUTO_DETECT TRUE);
COPY dept_manager FROM 'data/dept_manager.csv' (HEADER, AUTO_DETECT TRUE);
COPY dept_emp    FROM 'data/dept_emp.csv'    (HEADER, AUTO_DETECT TRUE);
COPY title       FROM 'data/title.csv'       (HEADER, AUTO_DETECT TRUE);
COPY salary      FROM 'data/salary.csv'      (HEADER, AUTO_DETECT TRUE);
