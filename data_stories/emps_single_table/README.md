# Employees Data Exploration

1. Create a CSV file with the following columns:

emp_id: unique id of an employee
emp_name: name of  employee: John Smith
department: SALES, IT, AI, BUSINESS, MARKETING
salary: integer range: 81,000 to 230,000
gender: MALE/FEMALE (42% MALE, 58% FEMALE)
degree: BA, BS, MIS, MS, PHD
hire_date: 2015-01-01 to 2015-12-31
country: USA, CANADA, ITALY, GERMANY, CHINA, INDIA
image_url: avatar for employee 
age: age of employees: 22 to 72

2. Number of records: 1100

   Make data to look real feel

3. 
400 : from USA
100 : from CANADA 
150 : from ITALY
150 : from GERMANY 
300 : from CHINA
200 : from INDIA

4. Only 
100 have PHD (mostly from USA, then CHINA)
200 have MIS
250 have MS
250 have MIS
100 have BA
200 have BS


5. but use DuckDB for all of our tasks.

6. Identify realistic queries for this set of employees

10 basic queries, using select, where, from, limit

10 queries using GROUP BY, HAVING, LIMIT

10 intermediate queries, ranking, sub queries, ...


Put files under:

/Users/max/mp/OMIS_105/data_stories/emps_single_table/
/Users/max/mp/OMIS_105/data_stories/emps_single_table/data

In Jupyter/notebook/DuckDB:

Create tables from created CSV files.


7. Create a data/ folder and 
   put all of the data as CSV files,
   then read these CSV's to create DuckDB Tables.

8. add more solid queries with plots

9. convert them to DuckDB environment: convert 
  it into a single Jupyter/Notebook/DuckDB. 
  
6. Each cell will indicate
   a. what we are doing
   b. SQL solution in nice/pretty format
   c. display result set in a very nice tabulated 
      table with row numbers
   d. when possible, have a nice beautiful plot 
      using the result set (the plot must be meaningful)
      
10.  Important: define all display/plot functions 
   outside of the notebook:
   I do not want my students to be tangled 
   with plotting code or with code used to 
   display/tabulation of result set.

   I want the Notebook to look clean and not tangled
   with plotting code or display of tabulation code.

11. You can write all of your output to this folder:

/Users/max/mp/OMIS_105/data_stories/emps_single_table/

