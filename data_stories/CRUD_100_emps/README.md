# CRUD  of Employees Data 

* This is going to be flagship Jupyter Notebook.

* We are going to teach CRUD of employee data
  by using DuckDB and Jupyter Notebook.

* This Notebook should assume that a student 
  does not know much about DuckDB and CRUD
  operations. When possible define and explain 
  each operation in detail (you may use MarkDown 
  format for explanations)


1. Create an employees table with the following records:

emp_id: integer, unique id of an employee: 100, 101, 102, 103, ...
emp_name:  name of  employee:  John Smith
department: SALES, IT, AI, BUSINESS, MARKETING
salary: integer range: 81,000 to 230,000
gender: MALE/FEMALE (4 MALE, 5 FEMALE)
degree: BA, BS, MIS, MS, PHD
hire_date: 2015-01-01 to 2015-12-31
country: USA, CANADA, CHINA


2. Number of records: 9

   All of these are created by SQL's INSERT statement   

   Make data to look real feel

3. 3 employees per country

4. assign proper degrees per country


5. Use DuckDB for all of our tasks.

6. Read this CSV file and create employees table

7. Teach CRUD for this set of employees
4 C's
4 R's (may be more R's)
4 U's
4 D's

for each CRUD:
-- show data before,
-- sql transformation (pretty print SQL, nice formatted)
-- show after transformation

8. Make Notebook bullet-proof, so that I can run it
many times from beginning to the end.

9. More queries:

   10 basic queries, using select, where, from, limit

   10 queries using GROUP BY, HAVING, LIMIT

   10 intermediate queries, ranking, sub queries, ...


Put files under:

/Users/max/mp/OMIS_105/data_stories/CRUD_100_emps/
/Users/max/mp/OMIS_105/data_stories/CRUD_100_emps/data

In Jupyter/notebook/DuckDB:

Create tables from created CSV files.


10. Create a data/ folder and 
   put all of the data as CSV files,
   then read these CSV's to create DuckDB Tables.

11. add more solid queries with plots

12. convert them to DuckDB environment: convert 
  it into a single Jupyter/Notebook/DuckDB. 
  
13. Each cell will indicate
   a. what we are doing
   b. SQL solution in nice/pretty format
   c. display result set in a very nice tabulated 
      table with row numbers
   d. when possible, have a nice beautiful plot 
      using the result set (the plot must be meaningful)
      
14.  Important: define all display/plot functions 
   outside of the notebook:
   I do not want my students to be tangled 
   with plotting code or with code used to 
   display/tabulation of result set.

   I want the Notebook to look clean and not tangled
   with plotting code or display of tabulation code.

15. You can write all of your output to this folder:

/Users/max/mp/OMIS_105/data_stories/CRUD_100_emps/

Now let me create all the files. This is a substantial project — I'll build the helper module, CSV data, and the full Jupyter notebook.Now let me create the full Jupyter notebook:Now let's verify the files and copy them to the output directory:Here's everything you need — place all three files under your target folder:

```
/Users/max/mp/OMIS_105/data_stories/CRUD_100_emps/
    ├── CRUD_Employees_DuckDB.ipynb   ← the main notebook
    ├── notebook_utils.py             ← all display/plot helpers
    └── data/
        └── employees.csv             ← 9 employees, 3 per country
```

---

### What's inside

**`notebook_utils.py`** — completely hidden from students; contains:
- `show_table()` — styled HTML table with row numbers and zebra stripes
- `show_sql()` — syntax-highlighted SQL in a dark code block
- `show_header()` / `show_note()` — section banners and colour-coded callouts
- `plot_bar`, `plot_horizontal_bar`, `plot_pie`, `plot_hist`, `plot_grouped_bar`, `plot_scatter`, `plot_line`

**`CRUD_Employees_DuckDB.ipynb`** — 79 cells total (52 code, 27 markdown):

| Section | Cells | Coverage |
|---------|-------|----------|
| Setup | 1 | pip install, imports, DuckDB connect |
| **C** — Create | 4 | CREATE TABLE, INSERT, COPY TO CSV, READ_CSV_AUTO |
| **R** — Read | 4 | SELECT *, WHERE, specific columns, AND/OR |
| **U** — Update | 4 | single row, department-wide, multi-column, CASE WHEN |
| **D** — Delete | 4 | single row, condition, AND/LIKE, subquery (with restore) |
| Basic Queries | 10 | SELECT/WHERE/LIMIT/BETWEEN/IN/DISTINCT/computed cols |
| Aggregate Queries | 10 | GROUP BY, HAVING, COUNT/SUM/AVG/MIN/MAX |
| Intermediate Queries | 10 | RANK, ROW_NUMBER, NTILE, CTEs, subqueries, running totals |
| Visualisations | 5 | histogram, horizontal bar, scatter, grouped bar, hire-month bar |

Every cell follows the pattern: **header → SQL (pretty-printed) → before/after table → plot**.


