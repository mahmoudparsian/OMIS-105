-- ============================================================
-- 03_extra_unassigned_employees.sql
-- Adds 3 employees who exist in `employee` but have NO row in
-- `dept_emp` -- i.e., they are not assigned to any department.
--
-- Why: these rows let students practice LEFT JOIN / IS NULL /
-- "find employees with no department" style queries, which have
-- no matches in the original dataset (every original employee
-- belongs to a department).
--
-- emp_no starts at 20001 so it can never collide with the
-- original range (10001-11000).
-- ============================================================

INSERT INTO employee (emp_no, birth_date, first_name, last_name, gender, hire_date) VALUES
    (20001, '1998-03-14', 'Ava',   'Nguyen',  'F', '2024-01-08'),
    (20002, '1995-11-02', 'Diego', 'Ramirez', 'M', '2024-02-19'),
    (20003, '2000-07-25', 'Priya', 'Shah',    'F', '2024-03-04');
