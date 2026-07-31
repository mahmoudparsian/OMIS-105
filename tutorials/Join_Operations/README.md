Consider the following schemas:

departments(
   dept_id,
   dept_name,
   dept_location,
   dept_manager,
   created_date
)

countries(
   country_code,  -- 3 characters
   country_name,
   population
)

employees(
   emp_id, 
   emp_name, 
   salary,       -- as an integer
   dept_id,      -- points to departments.dept_id
   country_code, -- points to countries.country_code
   gender,       -- MALE/FEMALE/UNKNOWN
   education,    -- BA, BS, MS, MSIS, PHD, MBA, LAW
   dob,          -- date of birth
   hire_date     -- date of hire
)

1. make sure data looks as real as possible

2. Create departments table with 7 departments,
   but do not use 2 of them at all 
   
   5 used departments: SALES, BUSINESS, MARKETING, SOFTWARE, HARDWARE
   
   2 not used department: AI, IT

3. create 10 countries: USA, CANADA, CHINA, INDIA, ...

4. Create 2000 employees with real names, 
   
   -- do not use "emp_name_1", "emp_name_2", ...

   -- 10 employees will have a dept_id = "TOP-SECRET"
      and it is not defined in the departments table
       
   -- only 50 employees have PHD degrees
   -- only 30 employees have LAW degrees
   -- only 100 employees have MSIS degrees
   -- only 40 employees have MBA degrees
   -- the rest have BA, BS, MS degrees
   -- do not balance country_code for employees
   -- we have 500 from USA 
   -- we have 300 from CHINA 
   -- we have 400 from INDIA
   -- the rest is from other countries (mixed)
   
5. Create three CSV files as:
   employees.csv
   departments.csv
   countries.csv
    
6. The main goal is to teach SQL's JOIN operations
-- inner join
-- left join
-- right join

7. you are the expert in Jupyter/Notebook/DuckDB.  

8. Create a Jupyter/Notebook/DuckDB by reading 
this file and showing basic statistics

9. The goal is to teach SQL's "JOIN" by creating 
   20 notebooks cells. 

10. For each cell:

a. Create a NL query: what are we doing: 
   Explain this in a simple English

b. how we implement in DuckDB's SQL Group By.
   show a beautifully formatted SQL
   
c. show the result set in a very nice beautiful table 
   (not a regular table).
   Define  table render/display functions in a separate file
   (display_tables.py) and then import and use them in 
   the notebook (render/display functions code should not 
   be in the notebook)

d. show a beautiful and meaningful plot for the result set.
   Define a generic plot functions in a separate file
   (plots.py) and then import and use them in 
   the notebook (plot code should not be in the notebook)
   
=====

Update employees.csv as:

1. Create 3060 employees with real names, 
   
   -- do not use "emp_name_1", "emp_name_2", ...

   -- 10 employees will have a dept_id = "TOP-SECRET"
      and it is not defined in the departments table
       
   -- do not balance country_code for employees

900 from USA
200 from Canada
500 from China
800 from India
150 from United Kingdom
100 from Germany
150 from Brazil
50  from Australia
120 from Japan
90  from France

2. Salaries for USA and INDIA will be higher salaries

3. Do not use the same salaries per country or department

4. Employees in SALES make more in salaries