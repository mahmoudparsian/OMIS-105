Consider the following: 

# Sales Data Exploration

## Introduction
Sales analysis over a PostgreSQL database, 
aiming to discover diverse insights. 

We are NOT going to use PostgreSQL,
but use DuckDB for all of our tasks.

Identify best seller products, biggest customers, 
and sales growth rate.

In this database, we have records of orders for 
different types of paper placed by companies such 
as Walmart, Microsoft, among others. We can see 
how much of each type of paper was ordered, how 
much was spent, who was responsible for the order, 
in which region the company is located, and the dates 
of the different web events each company has conducted 

A SQL analysis of sales on differents types of paper.
sales-analysis.md

* [Sales Analysis](https://github.com/jenny-4/sales-data-exploration/blob/main/sales-analysis.md)

## Datasets used
- <strong>accounts</strong>: This table contains all the different companies, their id (account_id), website, contact of point and the sale representative id
- <strong>orders</strong>: Timestamp of every order, the quantity ordered of every type of paper (standard_qty, gloss_qty, poster_qty), the total, how much money was spend in each type of paper (standard_amt_usd, gloss_amt_usd, poster_amt_usd) and the total in dollars.
- <strong>region</strong>: Four regions: Northeast, Midwest, Southeast, West
- <strong>sales_reps</strong>: This table shows all the sales representative names with their corresponding id and region_id.
- <strong>web_events</strong>: All the web events conducted by each company, the account_id, the date each web event was conducted and the channel (facebook, twitter, etc)

## Entity Relationship Diagram
![alt text](https://github.com/jenny-4/sales-data-exploration/blob/main/ERD.png)


1. Review  files under folder:

/Users/max/mp/OMIS_105/data_stories/sales-data-exploration/

and merge this and proper queries into a very nice 
Jupyter/Notebook/DuckDB.

Using sql_schema.sql, create CSV files
for each table under:

/Users/max/mp/OMIS_105/data_stories/sales-data-exploration/data/

In Jupyter/notebook/DuckDB:

Create tables from created CSV files.


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

/Users/max/mp/OMIS_105/data_stories/sales-data-exploration/

