-- Create departments table
CREATE OR REPLACE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50)
);

-- Insert sample data
INSERT INTO departments VALUES 
(10, 'Engineering'),
(20, 'Marketing'),
(30, 'Sales'),
(40, 'Finance');


-- Create employees table
CREATE OR REPLACE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    salary INT,
    dept_id INT,
    
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- Insert sample data
INSERT INTO employees (emp_id, emp_name, dept_id, salary) 
VALUES 
(1, 'Alice', 10, 65000),
(2, 'Bob', 20, 78000),
(3, 'Rafa', 20, 82000),
(4, 'Charlie', 10, 75000),
(5, 'Diana', NULL, 70000),
(6, 'Jane', NULL, 80000);


