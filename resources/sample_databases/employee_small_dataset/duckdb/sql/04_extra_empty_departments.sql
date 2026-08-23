-- ============================================================
-- 04_extra_empty_departments.sql
-- Adds 3 departments that exist in `department` but have NO row
-- in `dept_emp` -- i.e., nobody works in them yet.
--
-- Why: these rows let students practice LEFT JOIN / IS NULL /
-- "find departments with no employees" style queries, which have
-- no matches in the original dataset (every original department
-- has employees).
--
-- dept_no continues after the original d001-d009 range.
-- ============================================================

INSERT INTO department (dept_no, dept_name) VALUES
    ('d010', 'Legal'),
    ('d011', 'Facilities'),
    ('d012', 'Public Relations');
