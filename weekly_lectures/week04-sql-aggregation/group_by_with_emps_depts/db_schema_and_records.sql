CREATE OR REPLACE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR
);

INSERT INTO departments VALUES 
(10, 'Engineering'), 
(20, 'Marketing'), 
(30, 'Sales'), 
(40, 'Finance'),
(50, 'IT');

CREATE OR REPLACE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR,
    job_title VARCHAR,
    salary INT,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

INSERT INTO employees VALUES 
(1, 'Max', 'Engineer', 90000, 10),
(2, 'Bob', 'Salesperson', 130000, 10),
(3, 'Alice', 'Engineer', 70000, 10),
(4, 'Jenny', 'Salesperson', 120000, 10),
(5, 'Eve', 'Engineer', 95000, 10),
(6, 'Donald', 'Engineer', 95000, 10),
(7, 'Rafa', 'VP', 140000, 10),
(8, 'Barbara', 'VP', 170000, 20),
(9, 'Charlie', 'Marketer', 70000, 20),
(10, 'Dara', 'Marketer', 80000, 20),
(11, 'Jeff', 'Marketer', 80000, 20),
(12, 'Diana', 'Salesperson', 80000, 30),
(13, 'David', 'VP', 180000, 30);
