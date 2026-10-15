## Create DuckDB Database: Method-1

#### Create Database named `emps_depts_db.duckdb`
```
% rm  -f  emps_depts_db.duckdb
% duckdb emps_depts_db.duckdb 
.read db_schema.sql
.read db_records.sql
```

## Create DuckDB Database: Method-2

#### Create Database named `emps_depts_db.duckdb`

```
duckdb emps_depts_db.duckdb -c ".read db_schema.sql" -c ".read db_records.sql"
```

---

## Create DuckDB Database: Method-3

#### Create Database named `emps_depts_db.duckdb`
```
% rm -f  emps_depts_db.duckdb
% duckdb emps_depts_db.duckdb < db_schema.sql db_records.sql
```
#### View Database `emps_depts_db.duckdb`

```
% duckdb emps_depts_db.duckdb
-- Loading resources from /Users/max/.duckdbrc
DuckDB v1.5.5 (Variegata)
Enter ".help" for usage hints.
duckdb ▸ .schema
CREATE TABLE departments(
   dept_id INTEGER PRIMARY KEY, 
   dept_name VARCHAR
);

CREATE TABLE employees(
   emp_id INTEGER PRIMARY KEY, 
   emp_name VARCHAR, 
   job_title VARCHAR, 
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
│      50 │ IT          │
└─────────┴─────────────┘
Run Time (s): real 0.002 user 0.001288 sys 0.000401
changes:   0   total_changes: 0

duckdb ▸ SELECT * FROM employees;
┌────────┬──────────┬─────────────┬────────┬─────────┐
│ emp_id │ emp_name │  job_title  │ salary │ dept_id │
│ int32  │ varchar  │   varchar   │ int32  │  int32  │
├────────┼──────────┼─────────────┼────────┼─────────┤
│      1 │ Max      │ Engineer    │  90000 │      10 │
│      2 │ Bob      │ Salesperson │ 130000 │      10 │
│      3 │ Alice    │ Engineer    │  70000 │      10 │
│      4 │ Jenny    │ Salesperson │ 120000 │      10 │
│      5 │ Eve      │ Engineer    │  95000 │      10 │
│      6 │ Donald   │ Engineer    │  95000 │      10 │
│      7 │ Rafa     │ VP          │ 140000 │      10 │
│      8 │ Barbara  │ VP          │ 170000 │      20 │
│      9 │ Charlie  │ Marketer    │  70000 │      20 │
│     10 │ Dara     │ Marketer    │  80000 │      20 │
│     11 │ Jeff     │ Marketer    │  80000 │      20 │
│     12 │ Diana    │ Salesperson │  80000 │      30 │
│     13 │ David    │ VP          │ 180000 │      30 │
└────────┴──────────┴─────────────┴────────┴─────────┘
  13 rows                                  5 columns
Run Time (s): real 0.003 user 0.001374 sys 0.000418
changes:   0   total_changes: 0
duckdb ▸ .exit
%
```
