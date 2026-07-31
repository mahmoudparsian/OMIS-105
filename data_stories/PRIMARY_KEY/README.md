# You are an expert in DuckDB 
  and Relational DBMDS.
  
# We want to create a Jupyter
  notebook, which will read data/employees.csv
  and create an employees table in DuckDB:
  call this database as: employees

* This is going to be flagship Jupyter/DuckDB Notebook.

* We are going to teach PK (primary key) concept
  by using  employees table.
  
* Prove that without a PK, an employee can be inserted 
  many times
  
* show how to enforce the PK concept using the employees table

* This Notebook should assume that a student 
  does not know much about PK, DuckDB and CRUD
  operations. When possible define and explain 
  each operation in detail (you may use MarkDown 
  format for explanations)


* Teach CRUD for this set of employees
3 C's
3 R's 
3 U's
3 D's

for each CRUD:
-- show data before,
-- sql transformation (pretty print SQL, nice formatted)
-- show after transformation

* Make Notebook bullet-proof, so that I can run it
many times from beginning to the end.


Put files under:

/Users/max/mp/santa_clara_univ/OMIS_105/data_stories/PRIMARY_KEY/


* add more solid queries 
   -- pcercentage male/female employees
   -- percentage per department
   -- higest and lowest salaries
   -- higest and lowest salaries per department

  
* Each cell will indicate
   a. what we are doing
   b. SQL solution in nice/pretty format
   c. display result set in a very nice tabulated 
      table with row numbers
   d. when possible, have a nice beautiful plot 
      using the result set (the plot must be meaningful)
      
*  Important: define all display/plot functions 
   outside of the notebook:
   I do not want my students to be tangled 
   with plotting code or with code used to 
   display/tabulation of result set.

   I want the Notebook to look clean and not tangled
   with plotting code or display of tabulation code.
   Separate the plotting code to plot_util.py
   
---

my task is defined here: 
/Users/max/mp/santa_clara_univ/OMIS_105/data_stories/PRIMARY_KEY/README.md

I need access to that folder first.Now building the notebook:Both files are saved directly to your `PRIMARY_KEY` folder.

**What was built:**

`plot_util.py` — 5 clean utility functions (`display_table`, `plot_bar`, `plot_gender_pie`, `plot_salary_range`, `plot_dept_bar`). The notebook imports these, so students never see plotting/display code inline.

`primary_key.ipynb` — 55 cells (23 code, 32 markdown):

- **Section 0**: Setup — imports, connection, idempotent DB init
- **Section 1**: Table *without* PK → prove duplicate insertion works (and is bad)
- **Section 2**: Table *with* PK → prove duplicate is rejected with an error
- **Section 3 CRUD**: 3 × CREATE, 3 × READ, 3 × UPDATE, 3 × DELETE — each with before/SQL/after display + plots where meaningful
- **Section 4 Analytics**: gender % (pie), dept % (bar), overall min/max salary, min/max per department (grouped bar)
- **Section 5**: Summary table

Every cell that touches the DB first deletes/restores test data so the notebook runs cleanly from top to bottom any number of times.



