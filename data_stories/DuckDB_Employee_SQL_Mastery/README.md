DuckDB/Jupyter Project

1. I have the following schema
   defined as # schema
   
2. I have the following data for these 
   tables defined as # data

3. Want to develop a flagship Jupyter Notebook
   using DuckDB, which focuses on "group by",
   "join operation (inner, left, right)", 
   "ranking functions", and "sub-queries" 
   using "WITH".

4. The Notebook will have about 40 cells
   * basic (10 cells) 
   * intermediate (20 cells) 
   * intermediate+ (10)
   
5. Each cell will indicate
   a. what we are doing
   b. SQL solution in nice/pretty format
   c. display result set in a very nice tabulated 
      table with row numbers
   d. when possible, have a nice beautiful plot 
      using the result set (the plot must be meaningful)


6. Important: define all display/plot functions 
   outside of the notebook:
   I do not want my students to be tangled 
   with plotting code or with code used to 
   display/tabulation of result set.
   
   I want the Notebook to look clean and not tangled
   with plotting code or display of tabulation code.
   
7. Feel free to change the schema to fit DuckDB

8. If you have questions, let me know.

Where are your CSV data files located? 
I need the folder path to load them in the notebook.
define folder as: 
/Users/max/mp/data_analytics/SQL-Project-Employee-Database/mp_emps_project/data/

What plotting library do you prefer for the visualizations?
Matplotlib + Seaborn (Recommended)

How should the helper module (display/plot functions) be structured?
Single .py file (Recommended)

Should the notebook assume students run it in a specific environment?
Standard Jupyter

Thinking

Great! I have everything I need. Let me build this project — a clean Jupyter notebook with a separate helper module for all display/plot code.I'll create the notebook as JSON directly (since `.ipynb` files are just JSON) and the helper module. Let me build both files.Now let me create the Jupyter notebook. I'll build it as a Python script that generates the `.ipynb` JSON:Both files are ready. Let me clean up the build script:Here's your project — two files ready to go:

[View the Jupyter Notebook](computer:///Users/max/Library/Application%20Support/Claude/local-agent-mode-sessions/17406518-bf97-4472-94aa-60236611f432/e77d4f9a-42e6-42a2-8e2a-d58ec34b1a49/local_170d9761-fccd-41fb-83ee-ba43a34a07fd/outputs/DuckDB_Employee_SQL_Mastery.ipynb)

[View notebook_helpers.py](computer:///Users/max/Library/Application%20Support/Claude/local-agent-mode-sessions/17406518-bf97-4472-94aa-60236611f432/e77d4f9a-42e6-42a2-8e2a-d58ec34b1a49/local_170d9761-fccd-41fb-83ee-ba43a34a07fd/outputs/notebook_helpers.py)

---

**What you get:**

**`notebook_helpers.py`** — a single helper module with `display_result()` (styled HTML tables with row numbers) and 8 plotting functions (`plot_bar`, `plot_hbar`, `plot_pie`, `plot_line`, `plot_grouped_bar`, `plot_boxplot`, `plot_heatmap`, `plot_scatter`). Your students never see plotting code in the notebook cells.

**`DuckDB_Employee_SQL_Mastery.ipynb`** — 43 code cells structured as:

- 🟢 **Basic (10 cells):** GROUP BY, COUNT, AVG, SUM, HAVING, date extraction, single JOINs
- 🟡 **Intermediate (20 cells):** Multi-table INNER/LEFT/RIGHT JOINs, CTEs (WITH), RANK, DENSE_RANK, ROW_NUMBER, NTILE, PERCENT_RANK, LAG/LEAD, cumulative windows
- 🔴 **Intermediate+ (10 cells):** Chained multi-CTEs, correlated subqueries, CASE pivots, FILTER clauses, combined window functions, comprehensive analytics queries

**To run it:**
1. Place both files in the same directory as your CSV data folder, or adjust the `DATA_DIR` path in cell 2
2. Install: `pip install duckdb pandas matplotlib seaborn tabulate`
3. Launch: `jupyter notebook DuckDB_Employee_SQL_Mastery.ipynb`

The notebook assumes your CSVs use `%m/%d/%Y` date format (as shown in your sample data). Each cell is self-contained with a markdown header explaining the concept, clean SQL, and a meaningful visualization where appropriate.


# schema

-- Employee Database

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

# data

% ls -l
total 49176
-rw-r--r--@ 1 max  staff       188 May  4 18:41 departments.csv
-rw-r--r--@ 1 max  staff   4211384 May  4 18:37 dept_emp.csv
-rw-r--r--@ 1 max  staff       326 May  4 18:37 dept_manager.csv
-rw-r--r--@ 1 max  staff  15292685 May  4 18:38 employees.csv
-rw-r--r--@ 1 max  staff   4111638 May  4 18:39 salaries.csv
-rw-r--r--@ 1 max  staff       195 May  4 18:40 titles.csv

% wc -l *
      13 departments.csv
  331603 dept_emp.csv
      24 dept_manager.csv
  300024 employees.csv
  300024 salaries.csv
      10 titles.csv
  931698 total

% cat departments.csv
dept_id,dept_name
d001,Marketing
d002,Finance
d003,Human Resources
d004,Production
d005,Development
d006,Quality Management
d007,Sales
d008,Research
d009,Customer Service
d010,AI
d011,IT

% head dept_emp.csv
emp_id,dept_id
10001,d005
10002,d007
10003,d004
10004,d004
10005,d003
10006,d005
10007,d008
10008,d005
10009,d006

% head dept_manager.csv
dept_id,emp_id
d001,110022
d001,110039
d002,110085
d002,110114
d003,110183
d003,110228
d004,110303
d004,110344
d004,110386

% head employees.csv
emp_id,emp_title_id,birth_date,first_name,last_name,gender,hire_date
473302,s0001,7/25/1953,Hideyuki,Zallocco,M,4/28/1990
475053,e0002,11/18/1954,Byong,Delgrande,F,9/7/1991
57444,e0002,1/30/1958,Berry,Babb,F,3/21/1992
421786,s0001,9/28/1957,Xiong,Verhoeff,M,11/26/1987
282238,e0003,10/28/1952,Abdelkader,Baumann,F,1/18/1991
263976,e0003,10/30/1959,Eran,Cusworth,M,11/14/1986
273487,s0001,4/14/1957,Christoph,Parfitt,M,6/28/1991
461591,s0002,11/17/1964,Xudong,Samarati,M,11/13/1985
477657,e0002,12/18/1962,Lihong,Magliocco,M,10/23/1993

% head salaries.csv
emp_id,salary
10001,60117
10002,65828
10003,40006
10004,40054
10005,78228
10006,40000
10007,56724
10008,46671
10009,60929

% cat titles.csv
title_id,title
s0001,Staff
s0002,Senior Staff
e0001,Assistant Engineer
e0002,Engineer
e0003,Senior Engineer
e0004,Technique Leader
m0001,Manager
d0007,Director
d0008,Senior Director
