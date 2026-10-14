-- db_records.sql
-- Adds the rows. Run this file AFTER db_schema.sql.
-- departments must be loaded before employees (foreign key).

INSERT INTO departments (dept_id, dept_name, location) VALUES
   (10, 'Sales',       'San Jose'),
   (20, 'Engineering', 'Santa Clara'),
   (30, 'Marketing',   'Palo Alto');

INSERT INTO employees (emp_id, name, salary, dept_id) VALUES
   (1, 'Alice', 95000,  20),
   (2, 'Bob',   72000,  10),
   (3, 'Chen',  88000,  20),
   (4, 'Diana', 67000,  30),
   (5, 'Omar',  70000,  10),
   (6, 'Priya', 99000,  NULL);
