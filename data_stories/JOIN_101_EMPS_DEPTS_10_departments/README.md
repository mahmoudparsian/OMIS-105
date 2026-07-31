# JOIN 101  of Employees and Departments using Jupyter/DuckDB

* This is going to be flagship Jupyter/DuckDB Notebook
for JOIN operations (inner, left, right)

* Before this, Students have no knowledge of 
  join operations at all

* We are going to teach JOIN of employee data
  by departments data using DuckDB and Jupyter Notebook.

* This Notebook should assume that a student 
  does not know much about DuckDB and JOIN
  operations. When possible define and explain 
  each join operation in detail (you may use MarkDown 
  format for explanations)


1. Create 
   -- an employees table from data/employees.csv
   -- an departments table from data/departments.csv



2. for left and right join purposes:
  
  -- some employees have departments, 
     not defined in department table

  -- some departments have no employees assigned

  
3. Assume that students (reader of jupyter notebook)
   have no knowledge of join operations at all


4. Make Notebook bullet-proof, so that I can run it
many times from beginning to the end.

5. Queries:

   5 basic queries, using select, where, from, limit, group by

   15 queries using join operations with explanation


Put files under:

/Users/max/mp/OMIS_105/data_stories/JOIN_101_EMPS_DEPTS/
/Users/max/mp/OMIS_105/data_stories/JOIN_101_EMPS_DEPTS/data


6. Each cell will indicate
   a. what we are doing
   b. SQL solution in nice/pretty format
   c. display result set in a simple nice table 
      with row numbers
   d. when possible, have a nice beautiful plot 
      using the result set (the plot must be meaningful)
      
7.  Important: define all display/plot functions 
   outside of the notebook:
   I do not want my students to be tangled 
   with plotting code or with code used to 
   display/tabulation of result set.

   I want the Notebook to look clean and not tangled
   with plotting code or display of tabulation code.

8. You can write all of your output to this folder:

/Users/max/mp/OMIS_105/data_stories/JOIN_101_EMPS_DEPTS/

Now let me create the helper utilities module:Now the big notebook:All files are in place. Here's a summary of everything delivered:

---

## ✅ What was created

**Location:** `/Users/max/mp/OMIS_105/data_stories/JOIN_101_EMPS_DEPTS/`

### Files

| File | Size | Purpose |
|------|------|---------|
| `JOIN_101_EMPS_DEPTS.ipynb` | 43 KB | The flagship notebook (82 cells) |
| `notebook_utils.py` | 15 KB | All display/plot helpers — kept *outside* the notebook |
| `data/employees.csv` | 25 rows | Employees — 2 have unknown dept IDs (88, 99) |
| `data/departments.csv` | 9 rows | Departments — 2 have no employees (Legal, Customer Success) |

---

### Notebook structure

| Section | Content |
|---------|---------|
| **Section 0** | Setup — imports, DuckDB connection, file paths |
| **Section 1** | Create tables (idempotent — safe to re-run) + table previews |
| **Section 2** | 5 basic queries (SELECT / WHERE / GROUP BY / LIMIT) with charts |
| **Section 3** | Concept intro — what is a JOIN? Venn diagrams for all 3 types |
| **Section 4** | 10 INNER JOIN queries with explanations + plots |
| **Section 5** | 5 LEFT JOIN queries — NULLs, unmatched detection, COALESCE |
| **Section 6** | 5 RIGHT JOIN queries — empty departments, budget analysis |
| **Summary** | Cheat sheet + when-to-use guide |

### `notebook_utils.py` functions (called cleanly in 1 line each)
`show_df()` · `bar_chart()` · `pie_chart()` · `grouped_bar()` · `scatter_chart()` · `salary_hist()` · `draw_join_venn()` · `match_summary_bar()`
