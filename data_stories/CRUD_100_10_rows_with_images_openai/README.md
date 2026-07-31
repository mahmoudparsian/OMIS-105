# CRUD  of Employees Data using Jupyter/DuckDB

* This is going to be flagship Jupyter/DuckDB Notebook.

* We are going to teach CRUD of employee data
  by using DuckDB and Jupyter Notebook.

* This Notebook should assume that a student 
  does not know much about DuckDB and CRUD
  operations. 
  
  When possible define and explain 
  each CRUD operation in detail (you 
  may use MarkDown format for explanations)

1. Create an employees table with the following records:
metadata should be as exact:

(emp_id, emp_name, department, salary, gender, image_url)
(100, 'Alex', 'SALES', 120000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Alex')
(200, 'Jeff', 'SALES', 140000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Jeff')
(300, 'Rafa', 'BUSINESS', 150000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Rafa')
(400, 'Susan', 'SALES', 150000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Susan')
(500, 'Jen', 'BUSINESS', 160000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Jen')
(600, 'Barb', 'BUSINESS', 180000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Barb')
(700, 'Dara', 'AI', 190000, 'MALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Dara')
(800, 'Venus', 'AI', 200000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Venus')
(900, 'Margie', 'SALES', 140000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Margie')
(910, 'Betty', 'SALES', 170000, 'FEMALE', 'https://api.dicebear.com/7.x/adventurer/svg?seed=Betty')

2. Create one table (employees) from INSERTS, 
and  another one (call it employees_backup) table 
by reading a CSV file (the exact records).

All operations to be done by using the employees table.


3. Teach CRUD for this set of employees
4 C's
4 R's (may be more R's)
4 U's
4 D's

for each CRUD:
-- show data before,
-- sql transformation (pretty print SQL, nice formatted)
-- show after transformation

4. Make Notebook bullet-proof, so that I can run it
many times from beginning to the end.

5. More basic queries:

   10 basic queries, using select, where, from, limit

   10 queries using GROUP BY, HAVING, LIMIT


Put files under:

/Users/max/mp/OMIS_105/data_stories/CRUD_100_10_rows_with_images_openai/
/Users/max/mp/OMIS_105/data_stories/CRUD_100_10_rows_with_images_openai/data


6. Create a data/ folder and 
   put all of the data as CSV files,
   then read these CSV's to create DuckDB Tables.

7. add more solid queries with plots
   -- pcercentage male/female employees
   -- percentage per department
   -- higest and lowest salaries
   -- higest and lowest salaries per department

8. convert them to DuckDB environment: convert 
  it into a single Jupyter/Notebook/DuckDB. 
  
9. Each cell will indicate
   a. what we are doing
   b. SQL solution in nice/pretty format
   c. display result set in a very nice tabulated 
      table with row numbers
   d. when possible, have a nice beautiful plot 
      using the result set (the plot must be meaningful)
      
10. Important: define all display/plot functions 
   outside of the notebook:
   I do not want my students to be tangled 
   with plotting code or with code used to 
   display/tabulation of result set.

   I want the Notebook to look clean and not tangled
   with plotting code or display of tabulation code.

11. You can write all of your output to this folder:

/Users/max/mp/OMIS_105/data_stories/CRUD_100_10_rows_with_images_openai/

