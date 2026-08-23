-- ============================================================
-- 01_schema.sql
-- DuckDB schema for the "employee" sample database.
-- This is a DuckDB-dialect equivalent of mysql/dataset_small/employee.sql
-- (singular table names, same columns, same relationships).
-- ============================================================

DROP TABLE IF EXISTS dept_emp;
DROP TABLE IF EXISTS dept_manager;
DROP TABLE IF EXISTS title;
DROP TABLE IF EXISTS salary;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS department;

CREATE TABLE employee (
    emp_no      INTEGER     NOT NULL,
    birth_date  DATE        NOT NULL,
    first_name  VARCHAR(14) NOT NULL,
    last_name   VARCHAR(16) NOT NULL,
    gender      VARCHAR(1)  NOT NULL CHECK (gender IN ('M', 'F')),
    hire_date   DATE        NOT NULL,
    PRIMARY KEY (emp_no)
);

CREATE TABLE department (
    dept_no     VARCHAR(4)  NOT NULL,
    dept_name   VARCHAR(40) NOT NULL,
    PRIMARY KEY (dept_no),
    UNIQUE (dept_name)
);

CREATE TABLE dept_manager (
    emp_no      INTEGER     NOT NULL,
    dept_no     VARCHAR(4)  NOT NULL,
    from_date   DATE        NOT NULL,
    to_date     DATE        NOT NULL,
    PRIMARY KEY (emp_no, dept_no),
    FOREIGN KEY (emp_no)  REFERENCES employee (emp_no),
    FOREIGN KEY (dept_no) REFERENCES department (dept_no)
);

CREATE TABLE dept_emp (
    emp_no      INTEGER     NOT NULL,
    dept_no     VARCHAR(4)  NOT NULL,
    from_date   DATE        NOT NULL,
    to_date     DATE        NOT NULL,
    PRIMARY KEY (emp_no, dept_no),
    FOREIGN KEY (emp_no)  REFERENCES employee (emp_no),
    FOREIGN KEY (dept_no) REFERENCES department (dept_no)
);

CREATE TABLE title (
    emp_no      INTEGER     NOT NULL,
    title       VARCHAR(50) NOT NULL,
    from_date   DATE        NOT NULL,
    to_date     DATE,
    PRIMARY KEY (emp_no, title, from_date),
    FOREIGN KEY (emp_no) REFERENCES employee (emp_no)
);

CREATE TABLE salary (
    emp_no      INTEGER     NOT NULL,
    amount      INTEGER     NOT NULL,
    from_date   DATE        NOT NULL,
    to_date     DATE        NOT NULL,
    PRIMARY KEY (emp_no, from_date),
    FOREIGN KEY (emp_no) REFERENCES employee (emp_no)
);
