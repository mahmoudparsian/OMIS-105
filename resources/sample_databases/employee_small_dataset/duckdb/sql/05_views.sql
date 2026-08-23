-- ============================================================
-- 05_views.sql
-- Convenience views, ported from mysql/dataset_small/employee.sql.
-- ============================================================

CREATE OR REPLACE VIEW dept_emp_latest_date AS
    SELECT emp_no, MAX(from_date) AS from_date, MAX(to_date) AS to_date
    FROM dept_emp
    GROUP BY emp_no;

-- Shows only the current department for each employee.
CREATE OR REPLACE VIEW current_dept_emp AS
    SELECT l.emp_no, d.dept_no, l.from_date, l.to_date
    FROM dept_emp d
        INNER JOIN dept_emp_latest_date l
        ON d.emp_no = l.emp_no AND d.from_date = l.from_date AND l.to_date = d.to_date;
