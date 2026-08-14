# CRUD  of Employees Data using Notebook and DuckDB

* We are going to teach CRUD of employee data
  by using DuckDB and Marimo Notebook.

* This Notebook should assume that a student 
  does not know much about DuckDB and CRUD
  operations. When possible define and explain 
  each operation in detail (you may use MarkDown 
  format for explanations)


1. Create an employees table with the following records:

```
(emp_id, emp_name, department, salary, gender)
(100, 'Alex', 'SALES', 120000, 'MALE')
(200, 'Jeff', 'SALES', 140000, 'MALE')
(300, 'Rafa', 'BUSINESS', 150000, 'MALE')
(400, 'Susan', 'SALES', 150000, 'FMALE')
(500, 'Jen', 'BUSINESS', 160000, 'FEMALE')
(600, 'Barb', 'BUSINESS', 180000, 'FEMALE')
(700, 'Dara', 'AI', 190000, 'MALE')
(800, 'Venus', 'AI', 200000, 'FEMALE')
(900, 'Margie', 'SALES', 140000, 'FEMALE')
(910, 'Betty', 'SALES', 170000, 'FEMALE')
```

2. Create one table (employees) from INSERTS, 
and  another one (call it employees_backup) table 
by reading a CSV file (the exact records).

All operations to be done by using the employees table.


3. Teach CRUD for this set of employees

```
4 C's
4 R's (may be more R's)
4 U's
4 D's
```

For each CRUD:

* show data before,
* sql transformation (pretty print SQL, nice formatted)
* show after transformation

4. Make Notebook bullet-proof, so that I can run it
many times from beginning to the end.

5. More basic queries:

* 10 basic queries, using select, where, from, limit

* 10 queries using GROUP BY, HAVING, LIMIT



6. Create a data/ folder and 
   put all of the data as CSV files,
   then read these CSV's to create DuckDB Tables.

7. add more solid queries with plots

```
   -- pcercentage male/female employees
   -- percentage per department
   -- higest and lowest salaries
   -- higest and lowest salaries per department
```

8. convert them to DuckDB environment: convert 
  it into a single Notebook/DuckDB
  
9. Each cell will indicate

```
   a. what we are doing
   b. SQL solution in nice/pretty format
   c. display result set in a very nice tabulated 
      table with row numbers
   d. when possible, have a nice beautiful plot 
      using the result set (the plot must be meaningful)
```
      
10.  Important: define all display/plot functions 
   outside of the notebook:
   
   I do not want my students to be tangled 
   with plotting code or with code used to 
   display/tabulation of result set.

   I want the Notebook to look clean and not tangled
   with plotting code or display of tabulation code.

15. All files are under this folder:

```
data_stories/CRUD_100_10_rows/
```


```
CRUD_100_10_rows/
├── CRUD_Employees_DuckDB.ipynb   ← the flagship notebook
├── crud_helpers.py               ← all display/plot code (students ignore this)
└── data/
    └── employees.csv             ← source CSV for employees_backup table
```

---

### What's inside the notebook

**Setup** — one import line loads all helpers; a fresh `duckdb.connect()` ensures the notebook is safe to re-run from top to bottom every time.

**Two tables** — `employees` built from INSERT statements; `employees_backup` loaded with `read_csv_auto()` from the CSV.

**4 C's (INSERT)** — single row, multi-row, INSERT-SELECT from backup, NULL placeholder; before/after shown for each.

**4 R's (SELECT)** — all rows, specific columns, WHERE filter, WHERE+LIMIT; then 10 basic SELECT queries (vowel names, BETWEEN, IN, AND/OR, etc.) and 10 GROUP BY/HAVING queries (counts, AVG, SUM, MIN/MAX, top dept by payroll, gender distribution per dept, etc.).

**4 U's (UPDATE)** — fix the `FMALE` typo, bulk 10% raise for SALES, dept transfer, salary cap; before/after for each.

**4 D's (DELETE)** — by ID, by department, by salary condition, full wipe; before/after for each.

**5 Analytics plots** — gender donut, department headcount bar + pie, all-salary ranked horizontal bar (color-coded by dept), min/max grouped bar, average salary bar.

**`crud_helpers.py`** contains `print_sql`, `show_table`, `run`, `section`, `plot_hbar`, `plot_vbar`, `plot_pie`, `plot_salary_range` — completely invisible to students in the notebook cells.

