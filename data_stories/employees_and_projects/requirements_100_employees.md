Now we have:

% ls -l data/
total 48
-rw-r--r--@ 1 max  staff   215 May  5 12:06 department.csv
-rw-r--r--@ 1 max  staff   634 May  5 12:07 dependent.csv
-rw-r--r--@ 1 max  staff   131 May  5 12:07 dept_locations.csv
-rw-r--r--@ 1 max  staff  2908 May  5 12:06 employee.csv
-rw-r--r--@ 1 max  staff   359 May  5 12:06 project.csv
-rw-r--r--@ 1 max  staff   726 May  5 12:06 works_on.csv
employees_and_projects  % wc -l data/*
       6 data/department.csv
      17 data/dependent.csv
      11 data/dept_locations.csv
      21 data/employee.csv
      13 data/project.csv
      41 data/works_on.csv
      

1. Created a new folder /Users/max/mp/OMIS_105/data_stories/employees_and_projects/data2/
   to update/upgrade/add more rows to the following CSV files:
        
   * Make number of employees to 100
     with real names (not emp_1, emp_2, ...)

   * Add more rows to works_on.csv with respect 
     to 100 employees: for new records, make hours
     between 10 and 40 (randomly)
     
   * add more records to dependent.csv (based on added new employees)

   * do not add any rows to:
      department.csv
      dept_locations.csv
      project.csv
      
    
and merge all of this and proper queries into a very nice 
Jupyter/Notebook/DuckDB: you can use the following which you created
before as a basis for new notebook:

/Users/max/mp/OMIS_105/data_stories/employees_and_projects/employees_and_projects.ipynb

New notebook should be called as:

/Users/max/mp/OMIS_105/data_stories/employees_and_projects/employees_and_projects_100.ipynb

2. Add a new column (image_url) to employee table
   (similar to the cats, but human avatars).
   So each employee will have a unique image.

3. add more rows to all of the tables 
   (keep all data in newly created folder ./data/*.csv)

3. Create a data/ folder and 
   put all of the data as CSV files,
   then read these CSV's to create DuckDB Tables.

4. add more solid queries with plots

5. convert them to DuckDB environment: convert 
  it into a single Jupyter/Notebook/DuckDB. 
  
6. Each cell will indicate
   a. what we are doing
   b. SQL solution in nice/pretty format
   c. display result set in a very nice tabulated 
      table with row numbers
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

/Users/max/mp/OMIS_105/data_stories/employees_and_projects/

BUT, do not remove any files, you may add new files.

Let me generate the full 100-employee dataset with a Python script:Data generated. Let me verify integrity:Data is solid — 100 employees, well-distributed across departments, 42 with dependents. Now let me build the notebook:Now let me run the full verification — notebook structure, SQL syntax, data integrity, and confirm no plot code leaked into the notebook:Let me also verify the final file listing:Clean up the build scripts (minimize them, since I can't delete):Everything is complete. Here's what was created (no existing files were removed):

**New folder `./data2/` — 100-employee dataset:**

| File | Rows | Notes |
|------|------|-------|
| `employee.csv` | 100 | Real diverse names, unique DiceBear avatar per person, salaries $24K–$58K |
| `works_on.csv` | 256 | All 100 employees assigned to 1–4 of the 12 projects, hours 10–40 |
| `dependent.csv` | 83 | 42 employees have dependents (spouses, sons, daughters) |
| `department.csv` | 5 | Unchanged (Research, Admin, HQ, Engineering, Marketing) |
| `project.csv` | 12 | Unchanged |
| `dept_locations.csv` | 10 | Unchanged |

**New notebook `employees_and_projects_100.ipynb`** — 81 cells, **35 SQL queries**, each with:
- Markdown explaining what we're doing
- Formatted SQL in a code block
- Nicely tabulated result set with row numbers
- Meaningful plot where appropriate (bar, donut, scatter, heatmap, lollipop, grouped bar, stacked bar, dual-axis, line, pie)

SQL concepts covered: SELECT, JOIN, LEFT JOIN, GROUP BY/HAVING, CASE, subqueries, correlated subqueries, CTEs, UNION ALL, EXISTS, window functions (RANK, DENSE_RANK, NTILE, SUM OVER), STDDEV_POP, STRING_AGG, FLOOR binning, and a comprehensive dashboard query.

All plot/display code stays in `display_utils.py` — the notebook is clean for students.

[View the notebook](computer:///Users/max/mp/OMIS_105/data_stories/employees_and_projects/employees_and_projects_100.ipynb)

