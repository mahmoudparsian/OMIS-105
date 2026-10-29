# SQL Joins


### What is a SQL JOIN?

		SQL joins combine data from two 
		tables ( called **left table** 
		and **right table**) based on 
		a shared column (such as `key`, 
		`customer_id`, `department_id`).
	
### Types of Join operations:

		1. INNER JOIN (or JOIN)
		2. LEFT JOIN
		3. RIGHT JOIN



Join Type	 |What It Returns	| Common Use Case|
|----|----|----|
|`INNER JOIN`	|Only rows that have **matching values in both tables**.|	When you need complete records and want to filter out unmatched data (e.g., pulling a list of orders that have valid customer profiles).|
|`LEFT JOIN`|	**All rows from the left table**, plus any matching rows from the right table. *Unmatched right rows return NULL.*|	When your left table is your primary dataset and you want to keep it intact while adding optional matching info (e.g., listing all users, even if they haven't made a purchase).|
|`RIGHT JOIN`|	**All rows from the right table**, plus any matching rows from the left table. *Unmatched left rows return NULL.*|	Mirror image of a LEFT JOIN. It is rarely used in practice because you can achieve the same result by rewriting the query as a LEFT JOIN and swapping the table order.|


## 1. INNER JOIN (The Sweet Spot)

```sql
-- left table:  table1
-- right table: table2
SELECT columns
FROM table1             
INNER JOIN table2 
  ON table1.key = table2.key;
```

* `INNER JOIN` **is the same as** `JOIN`

* What it means: Keeps only the **matching rows** 
  that exist in both tables.

*  Real-world example: You have a list of Students 
   and a list of Club Members.  An Inner Join shows 
   only the students who actually joined a club. If 
   a student is in no club—or a club has no students 
   listed—they disappear from your result. 
   
### INNER JOIN Keys: Example 1: 

```
table1.key = { 1, 2, 5, 7, 8}
table2.key = { 1, 2, 3, 8 }

table1 INNER JOIN table2: { 1, 2, 8 }

Matching keys are: { 1, 2, 8 }
```

### INNER JOIN Keys: Example 2: 

```
table1.key = { 'USA', 'CHINA', 'CANADA', 'GERMANY', 'ITALY'}
table2.key = { 'USA', 'MEXICO', 'FRANCE', 'CHINA'}

table1 INNER JOIN table2: { 'USA', 'CHINA' }

Matching keys are: { 'USA', 'CHINA' }
```

### INNER JOIN Keys: Example 3: 

```
table1.key = { CANADA', 'GERMANY', 'ITALY'}
table2.key = { 'USA', 'MEXICO', 'FRANCE' }

table1 INNER JOIN table2: { }

Matching keys are: { }

There are NO Matching keys.
```


## 2. LEFT JOIN (All from the Left)

```sql
-- table1: LEFT Table
-- table2: RIGHT Table
SELECT columns
FROM table1             
LEFT JOIN table2 
  ON table1.key = table2.key;
```

* What it means: Keeps every single row from the 
  left table (table1), plus any matching data from 
  the right table (table2). If there is no match on 
  the right, it fills those columns with NULL

* Real-world example: You list all your Customers (left) 
  and their latest Orders (right). A Left Join shows 
  every single customer, even the ones who have never 
  bought anything yet (their order info just shows NULL). 

## 3. RIGHT JOIN (All from the Right)

```sql
-- table1: LEFT Table
-- table2: RIGHT Table
SELECT columns
FROM table1 
RIGHT JOIN table2 
  ON table1.key = table2.key;
```

* What it means: Keeps every single row from the 
  right table (table2), plus any matching data 
  from the left table (table1). If there is no 
  match on the left, it fills those columns with NULL. 

* Real-world example: The exact opposite of a Left Join. 
  If Orders is on the right and Customers is on the left, 
  a Right Join keeps every order, even if the customer 
  record is missing or deleted. 

# Quick Summary

* `INNER JOIN`: Only what matches in both.

* `LEFT JOIN`: All from the left + matches from the right.

* `RIGHT JOIN`: All from the right + matches from the left. 

# 3 SQL JOINs in Simple Example


users

|`id`	| `name`|
|---|---
|1 |	Alice|
|2	| Bob|

orders

|`order_id`	|`user_id`	|`product`
|---|---|---|
|10	|2|	Book
|20	|3	| Pen

```sql
duckdb ▸ CREATE TABLE users (
           id INTEGER,
           name VARCHAR
         );

duckdb ▸ INSERT INTO users(id, name)
         VALUES
         (1, 'Alice'),
         (2    , 'Bob');

duckdb ▸ CREATE TABLE orders (
            order_id INTEGER,
            user_id  INTEGER,
            product  VARCHAR
         );
         
duckdb ▸ INSERT INTO orders (order_id, user_id, product)
         VALUES
         (10, 2, 'Book'),
         (20, 3, 'Pen');

duckdb ▸ SELECT * FROM users;
┌───────┬─────────┐
│  id   │  name   │
├───────┼─────────┤
│     1 │ Alice   │
│     2 │ Bob     │
└───────┴─────────┘

duckdb ▸ SELECT * FROM orders;
┌──────────┬─────────┬─────────┐
│ order_id │ user_id │ product │
├──────────┼─────────┼─────────┤
│       10 │       2 │ Book    │
│       20 │       3 │ Pen     │
└──────────┴─────────┴─────────┘
```



## 1. INNER JOIN

```sql
SELECT u.id, u.name,
       o.order_id, o.user_id, o.product
FROM users AS u
INNER JOIN orders AS o
   ON u.id = o.user_id;
┌───────┬─────────┬──────────┬─────────┬─────────┐
│  id   │  name   │ order_id │ user_id │ product │
├───────┼─────────┼──────────┼─────────┼─────────┤
│     2 │ Bob     │       10 │       2 │ Book    │
└───────┴─────────┴──────────┴─────────┴─────────┘
```

• Why? Only Bob (`id` 2) matches an entry 
in the orders table. Alice has no orders, 
and the Pen (`user_id` 3) has no matching 
user, so both are dropped.

## 2. LEFT JOIN (or LEFT OUTER JOIN)

A LEFT JOIN returns all rows from the left table, 
plus the matching rows from the right table. If 
there is no match, the columns from the right 
table will contain NULL.

```sql
SELECT u.id, u.name,
       o.order_id, o.user_id, o.product
FROM users AS u
LEFT JOIN orders AS o
  ON u.id = o.user_id;
┌───────┬─────────┬──────────┬─────────┬─────────┐
│  id   │  name   │ order_id │ user_id │ product │
├───────┼─────────┼──────────┼─────────┼─────────┤
│     2 │ Bob     │       10 │       2 │ Book    │
│     1 │ Alice   │     NULL │    NULL │ NULL    │
└───────┴─────────┴──────────┴─────────┴─────────┘
```

• Why? Alice is included because she exists 
in the left (users) table, even though she 
has no matching orders. The missing product 
data is filled with NULL.

## 3. RIGHT JOIN (or RIGHT OUTER JOIN)

A RIGHT JOIN returns all rows from the 
right table, plus the matching rows from 
the left table. If there is no match, the 
columns from the left table will contain NULL.


```
SELECT o.order_id, o.user_id, o.product,
                u.id, u.name
         FROM users AS u
         RIGHT JOIN orders AS o
            ON u.id = o.user_id;
┌──────────┬─────────┬─────────┬───────┬─────────┐
│ order_id │ user_id │ product │  id   │  name   │
├──────────┼─────────┼─────────┼───────┼─────────┤
│       10 │       2 │ Book    │     2 │ Bob     │
│       20 │       3 │ Pen     │  NULL │ NULL    │
└──────────┴─────────┴─────────┴───────┴─────────┘
```


• Why? The Pen is included because it exists 
in the right (orders) table, even though its
`user_id` (3) doesn't match any user in our 
system. The missing user data is filled with NULL.


----

# SQL Joins in DuckDB

```sql
CREATE table table1 (
  key INTEGER,
  a   VARCHAR,
  b   VARCHAR
);

INSERT INTO table1(key, a, b)
VALUES
(1, 'a1', 'b1'),
(2, 'a2', 'b2'),
(5, 'a5', 'b5'),
(7, 'a7', 'b7');

CREATE table table2 (
  key INTEGER,
  c   VARCHAR,
  d   VARCHAR
);

INSERT INTO table2(key, c, d)
VALUES
(1, 'c1', 'd1'),
(2, 'c2', 'd2'),
(3, 'c3', 'd3');

duckdb ▸ SELECT * FROM table1;
┌───────┬─────────┬─────────┐
│  key  │    a    │    b    │
│ int32 │ varchar │ varchar │
├───────┼─────────┼─────────┤
│     1 │ a1      │ b1      │
│     2 │ a2      │ b2      │
│     5 │ a5      │ b5      │
│     7 │ a7      │ b7      │
└───────┴─────────┴─────────┘

duckdb ▸ SELECT * FROM table2;
┌───────┬─────────┬─────────┐
│  key  │    c    │    d    │
│ int32 │ varchar │ varchar │
├───────┼─────────┼─────────┤
│     1 │ c1      │ d1      │
│     2 │ c2      │ d2      │
│     3 │ c3      │ d3      │
└───────┴─────────┴─────────┘
```

# `INNER JOIN` Queries

```sql
SELECT table1.key, table1.a, table1.b,
       table2.key, table2.c, table2.d
FROM table1
INNER JOIN table2
   ON table1.key = table2.key;
   
┌───────┬─────────┬─────────┬───────┬─────────┬─────────┐
│  key  │    a    │    b    │  key  │    c    │    d    │
│ int32 │ varchar │ varchar │ int32 │ varchar │ varchar │
├───────┼─────────┼─────────┼───────┼─────────┼─────────┤
│     1 │ a1      │ b1      │     1 │ c1      │ d1      │
│     2 │ a2      │ b2      │     2 │ c2      │ d2      │
└───────┴─────────┴─────────┴───────┴─────────┴─────────┘
```

* Keep only one `key` in output

```sql
SELECT table1.key, table1.a, table1.b,
       table2.c, table2.d
FROM table1
INNER JOIN table2
   ON table1.key = table2.key;
   
┌───────┬─────────┬─────────┬─────────┬─────────┐
│  key  │    a    │    b    │    c    │    d    │
│ int32 │ varchar │ varchar │ varchar │ varchar │
├───────┼─────────┼─────────┼─────────┼─────────┤
│     1 │ a1      │ b1      │ c1      │ d1      │
│     2 │ a2      │ b2      │ c2      │ d2      │
└───────┴─────────┴─────────┴─────────┴─────────┘
```

* Use Alias

```sql
SELECT  t1.key, t1.a, t1.b,
        t2.c, t2.d
FROM table1 AS t1
INNER JOIN table2 AS t2
   ON t1.key = t2.key;
   
┌───────┬─────────┬─────────┬─────────┬─────────┐
│  key  │    a    │    b    │    c    │    d    │
│ int32 │ varchar │ varchar │ varchar │ varchar │
├───────┼─────────┼─────────┼─────────┼─────────┤
│     1 │ a1      │ b1      │ c1      │ d1      │
│     2 │ a21     │ b21     │ c23     │ d23     │
│     2 │ a22     │ b22     │ c23     │ d23     │
│     2 │ a21     │ b21     │ c22     │ d22     │
│     2 │ a22     │ b22     │ c22     │ d22     │
│     2 │ a21     │ b21     │ c21     │ d21     │
│     2 │ a22     │ b22     │ c21     │ d21     │
└───────┴─────────┴─────────┴─────────┴─────────┘
```

* Use `USING`

```
   In DuckDB, the USING keyword serves as a 
   convenient shorthand for specifying join 
   keys when both the left and right tables 
   share identical column names.

   USING(key) -> ON t1.key = t2.key 
```

```sql
SELECT  t1.a, t1.b,
        t2.c, t2.d
FROM table1 AS t1
INNER JOIN table2 AS t2
USING(key);
                           
┌─────────┬─────────┬─────────┬─────────┐
│    a    │    b    │    c    │    d    │
│ varchar │ varchar │ varchar │ varchar │
├─────────┼─────────┼─────────┼─────────┤
│ a1      │ b1      │ c1      │ d1      │
│ a2      │ b2      │ c2      │ d2      │
└─────────┴─────────┴─────────┴─────────┘
```

## `LEFT JOIN`

```sql
SELECT table1.key, table1.a, table1.b,
       table2.key, table2.c, table2.d
FROM table1
LEFT JOIN table2
   ON table1.key = table2.key;
┌───────┬─────────┬─────────┬───────┬─────────┬─────────┐
│  key  │    a    │    b    │  key  │    c    │    d    │
│ int32 │ varchar │ varchar │ int32 │ varchar │ varchar │
├───────┼─────────┼─────────┼───────┼─────────┼─────────┤
│     1 │ a1      │ b1      │     1 │ c1      │ d1      │
│     2 │ a2      │ b2      │     2 │ c2      │ d2      │
│     5 │ a5      │ b5      │  NULL │ NULL    │ NULL    │
│     7 │ a7      │ b7      │  NULL │ NULL    │ NULL    │
└───────┴─────────┴─────────┴───────┴─────────┴─────────┘
```

* Use Alias

```sql
SELECT t1.key, t1.a, t1.b,
       t2.key, t2.c, t2.d
FROM table1 AS t1
LEFT JOIN table2 AS t2
   ON t1.key = t2.key;

┌───────┬─────────┬─────────┬───────┬─────────┬─────────┐
│  key  │    a    │    b    │  key  │    c    │    d    │
│ int32 │ varchar │ varchar │ int32 │ varchar │ varchar │
├───────┼─────────┼─────────┼───────┼─────────┼─────────┤
│     1 │ a1      │ b1      │     1 │ c1      │ d1      │
│     2 │ a2      │ b2      │     2 │ c2      │ d2      │
│     5 │ a5      │ b5      │  NULL │ NULL    │ NULL    │
│     7 │ a7      │ b7      │  NULL │ NULL    │ NULL    │
└───────┴─────────┴─────────┴───────┴─────────┴─────────┘
```

* Use `USING`

```sql
SELECT t1.key, t1.a, t1.b,
       t2.key, t2.c, t2.d
FROM table1 AS t1
LEFT JOIN table2 AS t2
   USING (key);  -- ON t1.key = t2.key
         
┌───────┬─────────┬─────────┬───────┬─────────┬─────────┐
│  key  │    a    │    b    │  key  │    c    │    d    │
│ int32 │ varchar │ varchar │ int32 │ varchar │ varchar │
├───────┼─────────┼─────────┼───────┼─────────┼─────────┤
│     1 │ a1      │ b1      │     1 │ c1      │ d1      │
│     2 │ a2      │ b2      │     2 │ c2      │ d2      │
│     5 │ a5      │ b5      │  NULL │ NULL    │ NULL    │
│     7 │ a7      │ b7      │  NULL │ NULL    │ NULL    │
└───────┴─────────┴─────────┴───────┴─────────┴─────────┘
```

```sql 
SELECT t1.key as t1_key, t1.a, t1.b,
       t2.key as t2_key, t2.c, t2.d
FROM table1 AS t1
LEFT JOIN table2 AS t2
   USING (key);   -- ON t1.key = t2.key
         
┌────────┬─────────┬─────────┬────────┬─────────┬─────────┐
│ t1_key │    a    │    b    │ t2_key │    c    │    d    │
│ int32  │ varchar │ varchar │ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┼────────┼─────────┼─────────┤
│      1 │ a1      │ b1      │      1 │ c1      │ d1      │
│      2 │ a2      │ b2      │      2 │ c2      │ d2      │
│      5 │ a5      │ b5      │   NULL │ NULL    │ NULL    │
│      7 │ a7      │ b7      │   NULL │ NULL    │ NULL    │
└────────┴─────────┴─────────┴────────┴─────────┴─────────┘
```

```sql
SELECT t1.key, t1.a, t1.b,
       t2.c, t2.d
FROM table1 AS t1
LEFT JOIN table2 AS t2
   USING (key);   -- ON t1.key = t2.key
         
┌───────┬─────────┬─────────┬─────────┬─────────┐
│  key  │    a    │    b    │    c    │    d    │
│ int32 │ varchar │ varchar │ varchar │ varchar │
├───────┼─────────┼─────────┼─────────┼─────────┤
│     1 │ a1      │ b1      │ c1      │ d1      │
│     2 │ a2      │ b2      │ c2      │ d2      │
│     5 │ a5      │ b5      │ NULL    │ NULL    │
│     7 │ a7      │ b7      │ NULL    │ NULL    │
└───────┴─────────┴─────────┴─────────┴─────────┘
```

# `RIGHT JOIN`

```sql
SELECT table1.key as t1_key, table1.a, table1.b,
       table2.key AS t2_key, table2.c, table2.d
FROM table1
RIGHT JOIN table2
   ON table1.key = table2.key;
   
┌────────┬─────────┬─────────┬────────┬─────────┬─────────┐
│ t1_key │    a    │    b    │ t2_key │    c    │    d    │
│ int32  │ varchar │ varchar │ int32  │ varchar │ varchar │
├────────┼─────────┼─────────┼────────┼─────────┼─────────┤
│      1 │ a1      │ b1      │      1 │ c1      │ d1      │
│      2 │ a2      │ b2      │      2 │ c2      │ d2      │
│   NULL │ NULL    │ NULL    │      3 │ c3      │ d3      │
└────────┴─────────┴─────────┴────────┴─────────┴─────────┘


```sql
SELECT table1.a, table1.b,
       table2.key AS t2_key, table2.c, table2.d
FROM table1
RIGHT JOIN table2
  ON table1.key = table2.key;
┌─────────┬─────────┬────────┬─────────┬─────────┐
│    a    │    b    │ t2_key │    c    │    d    │
│ varchar │ varchar │ int32  │ varchar │ varchar │
├─────────┼─────────┼────────┼─────────┼─────────┤
│ a1      │ b1      │      1 │ c1      │ d1      │
│ a2      │ b2      │      2 │ c2      │ d2      │
│ NULL    │ NULL    │      3 │ c3      │ d3      │
└─────────┴─────────┴────────┴─────────┴─────────┘
```

```sql
SELECT table1.a, table1.b,
       table2.key, table2.c, table2.d
FROM table1
RIGHT JOIN table2
   USING(key);
   
┌─────────┬─────────┬───────┬─────────┬─────────┐
│    a    │    b    │  key  │    c    │    d    │
│ varchar │ varchar │ int32 │ varchar │ varchar │
├─────────┼─────────┼───────┼─────────┼─────────┤
│ a1      │ b1      │     1 │ c1      │ d1      │
│ a2      │ b2      │     2 │ c2      │ d2      │
│ NULL    │ NULL    │     3 │ c3      │ d3      │
└─────────┴─────────┴───────┴─────────┴─────────┘
```

# Joins with New Sets of Data

```sql
CREATE table table1 (
  key INTEGER,
  a   VARCHAR,
  b   VARCHAR
);

INSERT INTO table1(key, a, b)
VALUES
(1, 'a1', 'b1'),
(2, 'a21', 'b21'),
(2, 'a22', 'b22'),
(5, 'a5', 'b5'),
(7, 'a7', 'b7');

CREATE table table2 (
  key INTEGER,
  c   VARCHAR,
  d   VARCHAR
);

INSERT INTO table2(key, c, d)
VALUES
(1, 'c1', 'd1'),
(2, 'c21', 'd21'),
(2, 'c22', 'd22'),
(2, 'c23', 'd23'),
(3, 'c3', 'd3');

SELECT * FROM table1;
┌───────┬─────────┬─────────┐
│  key  │    a    │    b    │
│ int32 │ varchar │ varchar │
├───────┼─────────┼─────────┤
│     1 │ a1      │ b1      │
│     2 │ a21     │ b21     │
│     2 │ a22     │ b22     │
│     5 │ a5      │ b5      │
│     7 │ a7      │ b7      │
└───────┴─────────┴─────────┘

duckdb ▸ SELECT * FROM table2;
┌───────┬─────────┬─────────┐
│  key  │    c    │    d    │
│ int32 │ varchar │ varchar │
├───────┼─────────┼─────────┤
│     1 │ c1      │ d1      │
│     2 │ c21     │ d21     │
│     2 │ c22     │ d22     │
│     2 │ c23     │ d23     │
│     3 │ c3      │ d3      │
└───────┴─────────┴─────────┘

```

## INNER JOIN

```sql
SELECT  t1.key, t1.a, t1.b,
        t2.c, t2.d
FROM table1 AS t1
INNER JOIN table2 AS t2
   ON t1.key = t2.key;
┌───────┬─────────┬─────────┬─────────┬─────────┐
│  key  │    a    │    b    │    c    │    d    │
│ int32 │ varchar │ varchar │ varchar │ varchar │
├───────┼─────────┼─────────┼─────────┼─────────┤
│     1 │ a1      │ b1      │ c1      │ d1      │
│     2 │ a21     │ b21     │ c23     │ d23     │
│     2 │ a22     │ b22     │ c23     │ d23     │
│     2 │ a21     │ b21     │ c22     │ d22     │
│     2 │ a22     │ b22     │ c22     │ d22     │
│     2 │ a21     │ b21     │ c21     │ d21     │
│     2 │ a22     │ b22     │ c21     │ d21     │
└───────┴─────────┴─────────┴─────────┴─────────┘
```


## LEFT JOIN

```sql
SELECT  t1.key, t1.a, t1.b,
        t2.c, t2.d
FROM table1 AS t1
LEFT JOIN table2 AS t2
   ON t1.key = t2.key;
┌───────┬─────────┬─────────┬─────────┬─────────┐
│  key  │    a    │    b    │    c    │    d    │
│ int32 │ varchar │ varchar │ varchar │ varchar │
├───────┼─────────┼─────────┼─────────┼─────────┤
│     1 │ a1      │ b1      │ c1      │ d1      │
│     2 │ a21     │ b21     │ c23     │ d23     │
│     2 │ a22     │ b22     │ c23     │ d23     │
│     2 │ a21     │ b21     │ c22     │ d22     │
│     2 │ a22     │ b22     │ c22     │ d22     │
│     2 │ a21     │ b21     │ c21     │ d21     │
│     2 │ a22     │ b22     │ c21     │ d21     │
│     5 │ a5      │ b5      │ NULL    │ NULL    │
│     7 │ a7      │ b7      │ NULL    │ NULL    │
└───────┴─────────┴─────────┴─────────┴─────────┘
```

# RIGHT JOIN

```sql
SELECT table1.a, table1.b,
       table2.key AS t2_key, table2.c, table2.d
FROM table1
RIGHT JOIN table2
   ON table1.key = table2.key;
┌─────────┬─────────┬────────┬─────────┬─────────┐
│    a    │    b    │ t2_key │    c    │    d    │
│ varchar │ varchar │ int32  │ varchar │ varchar │
├─────────┼─────────┼────────┼─────────┼─────────┤
│ a1      │ b1      │      1 │ c1      │ d1      │
│ a22     │ b22     │      2 │ c21     │ d21     │
│ a22     │ b22     │      2 │ c22     │ d22     │
│ a22     │ b22     │      2 │ c23     │ d23     │
│ a21     │ b21     │      2 │ c21     │ d21     │
│ a21     │ b21     │      2 │ c22     │ d22     │
│ a21     │ b21     │      2 │ c23     │ d23     │
│ NULL    │ NULL    │      3 │ c3      │ d3      │
└─────────┴─────────┴────────┴─────────┴─────────┘
```


* Use `USING`

```sql
SELECT key, table1.a, table1.b,
       table2.c, table2.d
FROM table1
RIGHT JOIN table2
   USING(key);
┌───────┬─────────┬─────────┬─────────┬─────────┐
│  key  │    a    │    b    │    c    │    d    │
│ int32 │ varchar │ varchar │ varchar │ varchar │
├───────┼─────────┼─────────┼─────────┼─────────┤
│     1 │ a1      │ b1      │ c1      │ d1      │
│     2 │ a22     │ b22     │ c21     │ d21     │
│     2 │ a22     │ b22     │ c22     │ d22     │
│     2 │ a22     │ b22     │ c23     │ d23     │
│     2 │ a21     │ b21     │ c21     │ d21     │
│     2 │ a21     │ b21     │ c22     │ d22     │
│     2 │ a21     │ b21     │ c23     │ d23     │
│     3 │ NULL    │ NULL    │ c3      │ d3      │
└───────┴─────────┴─────────┴─────────┴─────────┘
```

# Join Operations with Cats and Toys

```sql
CREATE table cats (
  cat_id    INTEGER,
  cat_name  VARCHAR
);

INSERT INTO cats(cat_id, cat_name)
VALUES
(1, 'Kitty'),
(2, 'Hugo'),
(3, 'Sam'),
(4, 'Misty'),
(5, 'June');

CREATE table toys (
  toy_id    INTEGER,
  toy_name  VARCHAR,
  cat_id    INTEGER
);

INSERT INTO toys(toy_id, toy_name, cat_id)
VALUES
(1, 'ball', 3),
(2, 'spring', NULL),
(3, 'mouse', 1),
(4, 'mouse', 4),
(5, 'ball', 1),
(6, 'fish', 3);

SELECT * FROM cats;
┌────────┬──────────┐
│ cat_id │ cat_name │
│ int32  │ varchar  │
├────────┼──────────┤
│      1 │ Kitty    │
│      2 │ Hugo     │
│      3 │ Sam      │
│      4 │ Misty    │
│      5 │ June     │
└────────┴──────────┘

SELECT * FROM toys;
┌────────┬──────────┬────────┐
│ toy_id │ toy_name │ cat_id │
│ int32  │ varchar  │ int32  │
├────────┼──────────┼────────┤
│      1 │ ball     │      3 │
│      2 │ spring   │   NULL │
│      3 │ mouse    │      1 │
│      4 │ mouse    │      4 │
│      5 │ ball     │      1 │
│      6 │ fish     │      3 │
└────────┴──────────┴────────┘
```

## INNER JOIN

#### Find cats, which have toys

```sql
         SELECT  c.cat_id, c.cat_name,
                 t.toy_id, t.toy_name
         FROM cats AS c
         INNER JOIN toys AS t
            ON c.cat_id = t.cat_id
         ORDER BY  c.cat_id;
┌────────┬──────────┬────────┬──────────┐
│ cat_id │ cat_name │ toy_id │ toy_name │
│ int32  │ varchar  │ int32  │ varchar  │
├────────┼──────────┼────────┼──────────┤
│      1 │ Kitty    │      3 │ mouse    │
│      1 │ Kitty    │      5 │ ball     │
│      3 │ Sam      │      1 │ ball     │
│      3 │ Sam      │      6 │ fish     │
│      4 │ Misty    │      4 │ mouse    │
└────────┴──────────┴────────┴──────────┘
```

## LEFT JOIN

#### Find cats, which have toys or no toys

```sql
         SELECT  c.cat_id, c.cat_name,
                 t.toy_id, t.toy_name
         FROM cats AS c
         LEFT JOIN toys AS t
            ON c.cat_id = t.cat_id
         ORDER BY  c.cat_id;

┌────────┬──────────┬────────┬──────────┐
│ cat_id │ cat_name │ toy_id │ toy_name │
│ int32  │ varchar  │ int32  │ varchar  │
├────────┼──────────┼────────┼──────────┤
│      1 │ Kitty    │      3 │ mouse    │
│      1 │ Kitty    │      5 │ ball     │
│      2 │ Hugo     │   NULL │ NULL     │
│      3 │ Sam      │      1 │ ball     │
│      3 │ Sam      │      6 │ fish     │
│      4 │ Misty    │      4 │ mouse    │
│      5 │ June     │   NULL │ NULL     │
└────────┴──────────┴────────┴──────────┘

NOTE: Hugo and June have no toys.

```

## RIGHT JOIN

#### Find all toys, with associated cats

```sql
         SELECT  c.cat_id, c.cat_name,
                 t.toy_id, t.toy_name
         FROM cats AS c
         RIGHT JOIN toys AS t
            ON c.cat_id = t.cat_id
         ORDER BY  c.cat_id;
┌────────┬──────────┬────────┬──────────┐
│ cat_id │ cat_name │ toy_id │ toy_name │
│ int32  │ varchar  │ int32  │ varchar  │
├────────┼──────────┼────────┼──────────┤
│      1 │ Kitty    │      3 │ mouse    │
│      1 │ Kitty    │      5 │ ball     │
│      3 │ Sam      │      1 │ ball     │
│      3 │ Sam      │      6 │ fish     │
│      4 │ Misty    │      4 │ mouse    │
│   NULL │ NULL     │      2 │ spring   │
└────────┴──────────┴────────┴──────────┘
```

```sql
SELECT  c.cat_id AS "c.cat_id", c.cat_name,
        t.cat_id AS "t.cat_id", t.toy_id, t.toy_name
FROM cats AS c
RIGHT JOIN toys AS t
   ON c.cat_id = t.cat_id
ORDER BY  c.cat_id;
┌──────────┬──────────┬──────────┬────────┬──────────┐
│ c.cat_id │ cat_name │ t.cat_id │ toy_id │ toy_name │
│  int32   │ varchar  │  int32   │ int32  │ varchar  │
├──────────┼──────────┼──────────┼────────┼──────────┤
│        1 │ Kitty    │        1 │      3 │ mouse    │
│        1 │ Kitty    │        1 │      5 │ ball     │
│        3 │ Sam      │        3 │      1 │ ball     │
│        3 │ Sam      │        3 │      6 │ fish     │
│        4 │ Misty    │        4 │      4 │ mouse    │
│     NULL │ NULL     │     NULL │      2 │ spring   │
└──────────┴──────────┴──────────┴────────┴──────────┘
```

## Find cats with no Toys

```sql
memory D SELECT  c.cat_id, c.cat_name,
                 t.cat_id, t.toy_id, t.toy_name
          FROM cats AS c
          LEFT JOIN toys AS t
          ON c.cat_id = t.cat_id
            WHERE t.cat_id is NULL;
┌────────┬──────────┬────────┬────────┬──────────┐
│ cat_id │ cat_name │ cat_id │ toy_id │ toy_name │
│ int32  │ varchar  │ int32  │ int32  │ varchar  │
├────────┼──────────┼────────┼────────┼──────────┤
│      5 │ June     │   NULL │   NULL │ NULL     │
│      2 │ Hugo     │   NULL │   NULL │ NULL     │
└────────┴──────────┴────────┴────────┴──────────┘
```


# References

[1. 6 SQL Joins you MUST know! (Animated + Practice)(YouTube VIDEO)](https://www.youtube.com/watch?v=Yh4CrPHVBdE&t=18s)

[2. 6 SQL Joins you MUST know! (Animated + Practice)(YouTube VIDEO)](https://www.youtube.com/watch?v=9prkapPewGs)

