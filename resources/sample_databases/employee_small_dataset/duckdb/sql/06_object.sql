-- ============================================================
-- 06_object.sql
-- DuckDB-dialect equivalent of mysql/dataset_small/object.sql.
--
-- MySQL has stored FUNCTIONs/PROCEDUREs with DECLARE/BEGIN/END
-- bodies. DuckDB has no procedural stored routines -- instead it
-- has MACROs:
--   - a scalar MACRO returns one value, its body is a single
--     expression (often a scalar subquery in parentheses).
--   - a table MACRO (`AS TABLE ...`) returns a result set, and
--     stands in for a MySQL PROCEDURE that runs a SELECT.
-- Because macro bodies are single expressions, there is no
-- DECLARE/temp-table plumbing -- each macro below is a direct
-- translation of what the MySQL routine ultimately computes.
--
-- Depends on 01_schema.sql (tables) and 05_views.sql
-- (current_dept_emp), so run this file after those two.
-- ============================================================

DROP VIEW IF EXISTS v_full_employee;
DROP VIEW IF EXISTS v_full_department;
DROP MACRO IF EXISTS emp_dept_id;
DROP MACRO IF EXISTS emp_dept_name;
DROP MACRO IF EXISTS emp_name;
DROP MACRO IF EXISTS current_manager;
DROP MACRO TABLE IF EXISTS show_department;
DROP MACRO IF EXISTS employee_usage;
DROP MACRO TABLE IF EXISTS employee_help;

--
-- returns the department id of a given employee
-- (their most recent department, per current_dept_emp)
--
-- Note: the FROM table is given an alias (cde, d, e, dm below) even
-- though it isn't needed for readability -- DuckDB macro bodies get
-- inlined into the caller's query, and an *unaliased* table with the
-- same name as a table the caller also queries (e.g. calling
-- emp_name(emp_no) from a query already selecting FROM employee) can
-- make DuckDB's optimizer conflate the two scans and return more
-- than one row for what should be a single-row scalar subquery. An
-- explicit alias keeps the macro's internal scan distinct from
-- whatever the caller is doing.
--
CREATE MACRO emp_dept_id(employee_id) AS (
    SELECT dept_no
    FROM current_dept_emp AS cde
    WHERE cde.emp_no = employee_id
    LIMIT 1
);

--
-- returns the department name of a given employee
--
CREATE MACRO emp_dept_name(employee_id) AS (
    SELECT dept_name
    FROM department AS d
    WHERE d.dept_no = emp_dept_id(employee_id)
);

--
-- returns the employee name of a given employee id
--
CREATE MACRO emp_name(employee_id) AS (
    SELECT first_name || ' ' || last_name
    FROM employee AS e
    WHERE e.emp_no = employee_id
);

--
-- returns the manager of a department, choosing the
-- most recent one from the manager list
--
CREATE MACRO current_manager(dept_id) AS (
    SELECT emp_name(dm.emp_no)
    FROM dept_manager AS dm
    WHERE dm.dept_no = dept_id
    ORDER BY dm.from_date DESC
    LIMIT 1
);

--
-- selects the employee records with the latest department
--
CREATE VIEW v_full_employee AS
    SELECT
        emp_no,
        first_name, last_name,
        birth_date, gender,
        hire_date,
        emp_dept_name(emp_no) AS department
    FROM employee;

--
-- selects the department list with manager names
--
CREATE VIEW v_full_department AS
    SELECT
        dept_no, dept_name, current_manager(dept_no) AS manager
    FROM department;

--
-- shows each department with its manager and the number of
-- employees currently assigned to it (their latest dept_emp row).
--
-- The MySQL version builds this with two TEMPORARY TABLEs; DuckDB
-- can do the same job in one query by joining v_full_department to
-- current_dept_emp (already "one row per employee, latest dept").
--
CREATE MACRO show_department() AS TABLE
    SELECT
        v.dept_no,
        v.dept_name,
        v.manager,
        COUNT(*) AS num_employees
    FROM v_full_department v
        INNER JOIN current_dept_emp ce ON ce.dept_no = v.dept_no
    GROUP BY v.dept_no, v.dept_name, v.manager
    ORDER BY v.dept_no;

--
-- text-only "help" describing what's available, ported from the
-- MySQL employee_usage()/employee_help() function+procedure pair
--
CREATE MACRO employee_usage() AS (
'
    == USAGE ==
    ====================

    TABLE MACRO show_department()

        Shows each department with its manager and the
        number of employees currently in it.

    MACRO current_manager(dept_id)

        Shows who is the manager of a given department.

    MACRO emp_name(emp_id)

        Shows name and surname of a given employee.

    MACRO emp_dept_id(emp_id)

        Shows the current department of a given employee.
'
);

CREATE MACRO employee_help() AS TABLE
    SELECT employee_usage() AS info;
