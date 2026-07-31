-- Employee Database
-- Create In Order then go to next table; 
-- First, create Table, Inside the table 
-- define Column Name and set INT or VARCHAR, etc.. 
-- then define Primary Key

CREATE TABLE department (
    dept_id   VARCHAR  NOT NULL,
    dept_name VARCHAR  NOT NULL,
    CONSTRAINT pk_Department PRIMARY KEY (dept_id)
);

CREATE TABLE employee (
    emp_id       INT     NOT NULL,
    emp_title_id VARCHAR NOT NULL,
    birth_date   DATE    NOT NULL,
    first_name   VARCHAR NOT NULL,
    last_name    VARCHAR NOT NULL,
    gender       VARCHAR NOT NULL,
    hire_date    DATE    NOT NULL,
    CONSTRAINT pk_Employee PRIMARY KEY (emp_id)
);

CREATE TABLE department_manager (
    dept_id VARCHAR NOT NULL,
    emp_id  INT     NOT NULL,
    CONSTRAINT pk_DepartmentManager PRIMARY KEY (dept_id, emp_id)
);


CREATE TABLE department_employee (
    emp_id  INT     NOT NULL,
    dept_id VARCHAR NOT NULL,
    CONSTRAINT pk_DepartmentEmployee PRIMARY KEY (emp_id, dept_id)
);

CREATE TABLE salaries (
    emp_id INT   NOT NULL,
    salary INT   NOT NULL,
    CONSTRAINT pk_Salaries PRIMARY KEY (emp_id)
);

CREATE TABLE titles (
    title_id VARCHAR NOT NULL,
    title    VARCHAR NOT NULL,
    CONSTRAINT pk_titles PRIMARY KEY (title_id),
    CONSTRAINT uc_titles_title UNIQUE (title)
);

ALTER TABLE department_manager 
ADD CONSTRAINT fk_DepartmentManager_dept_id FOREIGN KEY(dept_id)
REFERENCES department (dept_id);

ALTER TABLE department_manager 
ADD CONSTRAINT fk_DepartmentManager_emp_id FOREIGN KEY(emp_id)
REFERENCES employee (emp_id);

ALTER TABLE department_employee 
ADD CONSTRAINT fk_DepartmentEmployee_emp_id FOREIGN KEY(emp_id)
REFERENCES employee (emp_id);

ALTER TABLE department_employee 
ADD CONSTRAINT fk_DepartmentEmployee_dept_id FOREIGN KEY(dept_id)
REFERENCES department (dept_id);

ALTER TABLE salaries 
ADD CONSTRAINT fk_Salaries_emp_id FOREIGN KEY(emp_id)
REFERENCES employee (emp_id);

ALTER TABLE employee 
ADD CONSTRAINT fk_employee_emp_title_id FOREIGN KEY(emp_title_id)
REFERENCES titles (title_id);
