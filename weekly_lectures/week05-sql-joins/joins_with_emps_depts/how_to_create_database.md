# How to Create a <br> DuckDB Database

Given `db_schema_and_records.sql` file (which 
defines tables and populates tables), several
methods are presented to create a DuckDB database.
The goal is to create a DuckDB database called 
`emps_depts_db.duckdb`.

## Method 1

#### Create Database

```sh
% rm -f emps_depts_db.duckdb*
% duckdb emps_depts_db.duckdb 
D .read db_schema_and_records.sql
```

#### Check/Verify Created Database

```sql
% duckdb emps_depts_db.duckdb
DuckDB v1.5.5 (Variegata)

duckdb ▸ .schema
CREATE TABLE departments(
  dept_id INTEGER PRIMARY KEY, 
  dept_name VARCHAR
);

CREATE TABLE employees(
  emp_id INTEGER PRIMARY KEY, 
  emp_name VARCHAR, 
  salary INTEGER, 
  dept_id INTEGER, 
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);


duckdb ▸ SELECT * FROM departments;
┌─────────┬─────────────┐
│ dept_id │  dept_name  │
│  int32  │   varchar   │
├─────────┼─────────────┤
│      10 │ Engineering │
│      20 │ Marketing   │
│      30 │ Sales       │
│      40 │ Finance     │
└─────────┴─────────────┘

duckdb ▸ SELECT * FROM employees;
┌────────┬──────────┬────────┬─────────┐
│ emp_id │ emp_name │ salary │ dept_id │
│ int32  │ varchar  │ int32  │  int32  │
├────────┼──────────┼────────┼─────────┤
│      1 │ Alice    │  65000 │      10 │
│      2 │ Bob      │  78000 │      20 │
│      3 │ Rafa     │  82000 │      20 │
│      4 │ Charlie  │  75000 │      10 │
│      5 │ Diana    │  70000 │    NULL │
│      6 │ Jane     │  80000 │    NULL │
└────────┴──────────┴────────┴─────────┘

duckdb ▸ .exit
%
```

## Method 2

#### Create Database

```sh
% rm -f emps_depts_db.duckdb*
duckdb emps_depts_db.duckdb -c ".read db_schema_and_records.sql"
```

## Method 3

```
% rm -f emps_depts_db.duckdb*
% duckdb emps_depts_db.duckdb < db_schema_and_records.sql
```
