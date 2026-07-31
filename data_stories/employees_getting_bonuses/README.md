1. We have a csv file: employees.csv as:

%cat employees.csv
emp_id,emp_name,department,gender,hire_date,degree,salary
100,Alex,BUSINESS,MALE,02/10/2024,PHD,220000
200,Fred,BUSINESS,MALE,03/11/2024,MIS,170000
300,Barb,BUSINESS,FEMALE,02/03/2024,BS,200000
400,Rafa,SPORTS,MALE,03/11/2023,MS,270000
500,Novak,SPORTS,MALE,01/11/2023,MS,250000
600,Betty,SPORTS,FEMALE,01/11/2023,MS,210000
700,Dara,SOFTWARE,MALE,03/11/2023,MS,220000
800,David,SOFTWARE,MALE,01/11/2023,MS,200000
900,Max,SOFTWARE,MALE,01/11/2023,PHD,290000
950,Jenny,SOFTWARE,FEMALE,01/11/2023,MS,180000

2. You are the expert in DuckDB and Jupyter Notebook.
We are teaching the fundamentals of relational databases
to undergraduate students in business school.

3. Assume that they do not know SQL at all.

4. Read this file, and create a table called "employees"

5. Show 10 basic/simple queries

6. show  10 intermediate queries

7. Create a new table employees_with_bonuses,
which has a bonus column (round bonus value) 
and that bonus is calculated 
based in the department:

if department = BUSINESS => bonus = salary * 5%
if department = SPORTS => bonus = salary * 7%
if department = SOFTWARE => bonus = salary * 9%

create bonus column and a new salary too.

8. For each query: Explicitly tell what are we doing
and then an associated sql query and then result as a 
duckdb output (similar to duckdb CLI table output.)

===

The sandbox doesn't have network access to install DuckDB, 
so I'll create the notebook file directly with all queries 
and their expected DuckDB-style output. Let me build it now.
Now let me create the Jupyter notebook:
Let me verify the notebook structure is valid JSON:
Here are your files:

[View the Jupyter Notebook](computer:///Users/max/Library/Application%20Support/Claude/local-agent-mode-sessions/17406518-bf97-4472-94aa-60236611f432/e77d4f9a-42e6-42a2-8e2a-d58ec34b1a49/local_23717a8c-0a94-4436-be23-ee66a709ace2/outputs/SQL_Fundamentals_with_DuckDB.ipynb)

[View employees.csv](computer:///Users/max/Library/Application%20Support/Claude/local-agent-mode-sessions/17406518-bf97-4472-94aa-60236611f432/e77d4f9a-42e6-42a2-8e2a-d58ec34b1a49/local_23717a8c-0a94-4436-be23-ee66a709ace2/outputs/employees.csv)

The notebook contains 27 code cells and 52 markdown 
cells organized into three parts:

**Part 1 — 10 Basic Queries:** 
  SELECT all/specific columns, WHERE filtering, 
  comparison operators, ORDER BY, LIMIT, DISTINCT, 
  COUNT, AND/OR conditions, and column aliases.

**Part 2 — 10 Intermediate Queries:** 
  GROUP BY, aggregate functions (AVG/MIN/MAX/SUM), 
  HAVING, IN operator, BETWEEN, CASE WHEN, multi-column 
  grouping, subqueries, LIKE pattern matching, and window 
  functions (RANK).

**Part 3 — employees_with_bonuses table:** 
  Creates the new table with bonus (BUSINESS 5%, 
  SPORTS 7%, SOFTWARE 9%) rounded to whole numbers, 
  plus a new_salary column, followed by a department 
  summary query.

Each query includes a plain-English explanation of 
what we're doing, the SQL code, and the expected 
DuckDB CLI-style table output. Place both files in 
the same folder and run the notebook with 
`pip install duckdb` first.


