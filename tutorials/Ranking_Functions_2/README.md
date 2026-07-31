# Jupyter/Notebook/DuckDB.

Master flagship tutorial of Ranking Functions

Create a Jupyter/Notebook/DuckDB (20 cells) 
to teach the fundamental concepts of 
Ranking Functions (row_number, rank, dense_rank)
and sub-queries with using the "WITH" only 
(note the focus is ranking functions).

Render output of sql queries in a very nice 
high quality rendered tables (keep the rendering 
code outside)

for this create a 1000 rows table of employees
to be read as a CSV file:

emp_id,     -- 1, 2, 3, ...
emp_name,   -- real names: Alex Smith, ...
dept_id,    -- SALES, BUSINESS, AI, MARKETING, SOFTWARE, HARDWARE
country,    -- 5 countries: USA, CANADA, GERMANY, CHINA, INDIA
gender,     -- MALE/FEMALE
salary,     -- integer 80,000, 81,000, ... , 280,000
degree,     -- BA, BS, MS, MSIS, PHD
performance -- yearly performance from 1 to 10
hire_date   -- date of hire (spans for 3 years

100 SALES, 
50  BUSINESS, 
150 AI, 
50  MARKETING, 
400 SOFTWARE 
250 HARDWARE

600 USA, 
200 CANADA, 
100 GERMANY, 
50  CHINA, 
50  INDIA

PHD makes the highest salaries

this is for students who have not used ranking
functions at all (start with 10 basic cells, 
5 intermediate, 5 intermediate+)

May be you can use ranking functions at the very end 
of this tutorial

All SQL output renders via the styled `show()` helper — 
dark navy headers, alternating rows, hover highlights, 
and row counts.

