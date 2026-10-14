-- db_schema.sql
-- Creates the tables (the structure only, no rows).
-- Run this file FIRST, then db_records.sql.

-- departments: one row per department
CREATE TABLE departments (
   dept_id   INT PRIMARY KEY,
   dept_name VARCHAR NOT NULL UNIQUE,
   location  VARCHAR NOT NULL
);

-- employees: one row per employee
CREATE TABLE employees (
   emp_id    INT PRIMARY KEY,
   name      VARCHAR NOT NULL,
   salary    INT NOT NULL CHECK (salary > 0),
   dept_id   INT,
   -- every employees.dept_id must exist in departments
   FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
