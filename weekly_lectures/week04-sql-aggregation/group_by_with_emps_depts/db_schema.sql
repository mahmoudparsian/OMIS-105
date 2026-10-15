CREATE OR REPLACE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR
);


CREATE OR REPLACE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR,
    job_title VARCHAR,
    salary INT,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

