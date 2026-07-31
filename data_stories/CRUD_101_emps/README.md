# CRUD  of Employees Data 

We are going to teach CRUD of employee data
by using DuckDB and Jupyter Notebook.

This Notebook should assume that a student 
does not know much about DuckDB and CRUD
operations. When possible define and explain 
each operation in detail.


1. Create a CSV file with the following columns:

emp_id: unique id of an employee
emp_name: name of  employee: John Smith
department: SALES, IT, AI, BUSINESS, MARKETING
salary: integer range: 81,000 to 230,000
gender: MALE/FEMALE (50% MALE, 50% FEMALE)
degree: BA, BS, MIS, MS, PHD
hire_date: 2015-01-01 to 2015-12-31
country: USA, CANADA, ITALY, GERMANY, CHINA
image_url: avatar for employee 
age: age of employees: 22 to 52

2. Number of records: 10

   Make data to look real feel

3. 2 employees per country

4. 2 different degrees per country


5. Use DuckDB for all of our tasks.

6. Read this CSV file and create employees table

7. Teach CRUD for this set of employees
4 C's
4 R's (may be more R's)
4 U's
4 D's

for each CRUD:
-- show data before,
-- transformation
-- show after transformation

8. Make Notebook bullet-proof, so that I can run it
many times from beginning to the end.

9. More queries:

   when possible render image_url column

   10 basic queries, using select, where, from, limit

   10 queries using GROUP BY, HAVING, LIMIT

   10 intermediate queries, ranking, sub queries, ...


Put files under:

/Users/max/mp/OMIS_105/data_stories/CRUD_101_emps/
/Users/max/mp/OMIS_105/data_stories/CRUD_101_emps/data

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

/Users/max/mp/OMIS_105/data_stories/CRUD_101_emps/


