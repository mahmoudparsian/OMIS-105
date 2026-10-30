# DuckDB SQL Subqueries: <br> A Complete Beginner-to-Advanced Tutorial

**A hands-on guide to SQL subqueries,****`WITH`****clauses, CTEs, and****`INNER JOIN`**

- **Database:** DuckDB
- **Level:** Beginner to intermediate, with advanced patterns
- **Approach:** Learn by running SQL queries and examining results
- **Prerequisites:** Basic familiarity with `SELECT`, `WHERE`, `GROUP BY`, and aggregate functions

---

## Table of Contents

1. Learning objectives
2. What is a subquery?
3. Part I — Start with one sales table
4. Basic subqueries
5. Scalar and single-row subqueries
6. Multi-row subqueries: IN and NOT IN
7. EXISTS and NOT EXISTS
8. Subqueries in SELECT
9. Subqueries in FROM
10. Correlated subqueries
11. Nested subqueries
12. ANY, ALL, and comparison operators
13. WITH and common table expressions
14. Recursive CTEs
15. Part II — Introduce two related tables
16. INNER JOIN fundamentals
17. Subqueries with two tables
18. JOIN versus subquery versus CTE
19. Advanced analytical examples
20. Common mistakes and debugging
21. Performance considerations in DuckDB
22. Practice exercises
23. Exercise solutions
24. Cheat sheet

---

# 1\. Learning objectives

By the end of this tutorial, you should be able to:

- Explain what a subquery is and why it is useful.
- Write subqueries inside `WHERE`, `SELECT`, and `FROM`.
- Distinguish scalar, single-row, multi-row, and correlated subqueries.
- Use `IN`, `NOT IN`, `EXISTS`, `NOT EXISTS`, `ANY`, and `ALL`.
- Write nested subqueries that solve multi-step problems.
- Use `WITH` to create readable, reusable query steps.
- Understand recursive CTEs.
- Query two related tables using `INNER JOIN` and subqueries.
- Recognize when a join, subquery, aggregation, or CTE is the clearest solution.
- Avoid common errors involving `NULL`, duplicate rows, and aggregate calculations.

## How to use this tutorial

Run the SQL examples in order in a DuckDB SQL editor, notebook, Python application, or DuckDB command-line client.

Most examples are independent after the initial table setup. The second part creates a new related table and expands the examples.

---

# 2\. What is a subquery?

A **subquery** is a SQL query written inside another SQL statement.

Consider this question:

> Which sales transactions have an amount greater than the average sale amount?

We can solve it in two steps:

**Step-1:** Calculate the average sale amount.

**Step-2:** Find transactions whose amounts exceed that average.

A subquery combines these steps into one statement.

```sql
SELECT *
FROM sales
WHERE amount > (
    SELECT AVG(amount)
    FROM sales
);
```

The inner query is:



```sql
SELECT AVG(amount)
FROM sales;
```

The outer query is:



```sql
SELECT *
FROM sales
WHERE amount > (...);
```

The inner query calculates a value. The outer query uses that value to filter the sales rows.

Conceptually, think of a subquery as a question inside a question.

- Inner question: What is the average sale?
- Outer question: Which sales exceed that average?

**Important:** This is a conceptual explanation, not a guarantee that DuckDB physically executes every inner query first. The optimizer may transform the SQL into a different execution plan.

## The main types of subqueries

| Type | Typical result | Common use |
| --- | --- | --- |
| Scalar | One value | Compare with an average or maximum |
| Single-row | One row | Compare several columns or use row comparisons |
| Multi-row | Multiple values | Filter with `IN`, `ANY`, or `ALL` |
| Correlated | Results depend on an outer row | Compare each sale with its own group |
| Derived table | A table-like result | Aggregate first, then filter or join |
| CTE | A named query result | Break a complex query into readable steps |
| Recursive CTE | Repeatedly generated rows | Hierarchies, sequences, and graph-like traversal |

A query may fit more than one category. For example, a correlated subquery can return a scalar value.

---

# 3\. Part I — Start with one sales table

We will use one table throughout the first part.

## 3.1 Create the table


```sql
DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    sale_id INTEGER,
    sale_date DATE,
    product VARCHAR,
    category VARCHAR,
    salesperson VARCHAR,
    region VARCHAR,
    quantity INTEGER,
    amount DECIMAL(10, 2)
);
```

The columns mean:

- `sale_id`: unique transaction identifier.
- `sale_date`: date of the transaction.
- `product`: product sold.
- `category`: product category.
- `salesperson`: employee who made the sale.
- `region`: geographical sales region.
- `quantity`: units sold.
- `amount`: total transaction amount.

## 3.2 Insert sample data

sql

```sql
INSERT INTO sales VALUES
(1,  DATE '2026-01-05', 'Laptop',    'Electronics', 'Alice', 'West',  2, 2400.00),
(2,  DATE '2026-01-06', 'Phone',     'Electronics', 'Bob',   'East',  3, 2100.00),
(3,  DATE '2026-01-07', 'Desk',      'Furniture',   'Alice', 'West',  1,  450.00),
(4,  DATE '2026-01-08', 'Chair',     'Furniture',   'Carol', 'East',  4,  800.00),
(5,  DATE '2026-01-09', 'Laptop',    'Electronics', 'Bob',   'West',  1, 1200.00),
(6,  DATE '2026-01-10', 'Monitor',   'Electronics', 'Alice', 'East',  2,  600.00),
(7,  DATE '2026-01-11', 'Desk',      'Furniture',   'Bob',   'East',  2,  900.00),
(8,  DATE '2026-01-12', 'Phone',     'Electronics', 'Carol', 'West',  1,  700.00),
(9,  DATE '2026-01-13', 'Chair',     'Furniture',   'Alice', 'West',  2,  400.00),
(10, DATE '2026-01-14', 'Monitor',   'Electronics', 'Bob',   'East',  3,  900.00),
(11, DATE '2026-01-15', 'Desk',      'Furniture',   'Carol', 'West',  1,  500.00),
(12, DATE '2026-01-16', 'Laptop',    'Electronics', 'Alice', 'East',  1, 1200.00),
(13, DATE '2026-01-17', 'Chair',     'Furniture',   'Bob',   'West',  3,  600.00),
(14, DATE '2026-01-18', 'Phone',     'Electronics', 'Alice', 'West',  2, 1400.00),
(15, DATE '2026-01-19', 'Desk',      'Furniture',   'Bob',   'East',  1,  450.00);
```

## 3.3 Inspect the table


```sql
SELECT *
FROM sales
ORDER BY sale_id;
```

Check how many rows exist:


```sql
SELECT COUNT(*) AS total_sales
FROM sales;
```

Expected result:

| `total_sales` |
| ------------- |
| 15            |

## 3.4 Calculate summary statistics


```sql
SELECT
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS average_sale,
    MIN(amount) AS smallest_sale,
    MAX(amount) AS largest_sale
FROM sales;
```

Expected results:

| transaction\_count | total\_revenue | average\_sale | smallest\_sale | largest\_sale |
| --- | --- | --- | --- | --- |
| 15 | 14600.00 | 973.333333 | 400.00 | 2400.00 |

These aggregates will become the building blocks for our subqueries.

---

# 4\. Basic subqueries

## 4.1 Find sales greater than the overall average


```sql
SELECT
    sale_id,
    product,
    salesperson,
    amount
FROM sales
WHERE amount > (
    SELECT AVG(amount)
    FROM sales
)
ORDER BY amount DESC;
```

The inner query returns approximately `973.33`.

The outer query returns sales with an amount greater than that value.

Expected result:

| `sale_id` | `product` | `salesperson` | `amount` |
| --- | --- | --- | --- |
| 1 | Laptop | Alice | 2400.00 |
| 2 | Phone | Bob | 2100.00 |
| 14 | Phone | Alice | 1400.00 |
| 5 | Laptop | Bob | 1200.00 |
| 12 | Laptop | Alice | 1200.00 |

The last two transactions shown have amounts of 1200.00. They are both above the average.

## 4.2 Find the largest sale


```sql
SELECT *
FROM sales
WHERE amount = (
    SELECT MAX(amount)
    FROM sales
);
```

* The inner query calculates the maximum amount. 
* The outer query finds rows equal to it.


## 4.3 Find sales equal to the smallest sale

```sql
SELECT
    sale_id,
    product,
    amount
FROM sales
WHERE amount = (
    SELECT MIN(amount)
    FROM sales
);
```

This illustrates a general pattern:

sql

```
SELECT columns
FROM table_name
WHERE column_name comparison_operator (
    SELECT aggregate_function(column_name)
    FROM table_name
);
```

You can replace the aggregate function with 
`AVG`, `MAX`, `MIN`, `SUM`, or `COUNT` when 
the comparison makes sense.

**Beginner takeaway:** A subquery is especially 
useful when the value you need to compare against 
must itself be calculated from data.

---

# 5\. Scalar and single-row subqueries

## 5.1 What is a scalar subquery?

A scalar subquery returns one value: one row and one column.

Example:


```sql
SELECT AVG(amount)
FROM sales;
```

This query returns one number, so it can be used in a scalar context.


```sql
SELECT
    sale_id,
    amount,
    (SELECT AVG(amount) FROM sales) AS average_sale
FROM sales
ORDER BY sale_id;
```

Each output row displays the transaction amount and the overall average.

## 5.2 Compare with a scalar subquery


```sql
SELECT sale_id, amount
FROM sales
WHERE amount > (
    SELECT AVG(amount)
    FROM sales
);
```

The comparison expects one value on the right side.

## 5.3 What if a scalar subquery returns multiple rows?

For example:

sql

```
SELECT *
FROM sales
WHERE amount = (
    SELECT amount
    FROM sales
    WHERE region = 'West'
);
```

* The inner query returns several amounts. 
* A scalar comparison cannot use several values this way, 
* so DuckDB raises an error.

Use `IN` when you want to compare against a set of values:


```sql
SELECT *
FROM sales
WHERE amount IN (
    SELECT amount
    FROM sales
    WHERE region = 'West'
);
```

This fixes the cardinality problem, although the query 
has a different meaning: it finds sales whose amounts 
match any amount from the West region.

## 5.4 Single-row subqueries

A single-row subquery returns one row, potentially with 
multiple columns. It can be useful with row comparisons 
where the database supports the relevant syntax.

For example, DuckDB supports row comparisons:



```sql
SELECT sale_id, product, amount
FROM sales
WHERE (product, amount) = (
    SELECT product, amount
    FROM sales
    WHERE sale_id = 1
);
```

* The inner query returns the product and amount for sale 1. 
* The outer query finds rows with the same pair of values.
* Because this compares both columns, it is different from comparing `amount` alone.

**Rule:** Always understand how many rows and columns a subquery can return before choosing the outer comparison.

---

# 6\. Multi-row subqueries: IN and NOT IN

## 6.1 IN

`IN` checks whether a value matches any value in a set.

Find sales whose products appear in the West region:


```sql
SELECT
    sale_id,
    product,
    region,
    amount
FROM sales
WHERE product IN (
    SELECT product
    FROM sales
    WHERE region = 'West'
)
ORDER BY sale_id;
```

* The inner query produces the set of products sold in the West. 
* The outer query returns rows with those products.
* This example is useful for learning `IN`, but it is worth 
  noticing that several products appear in both regions.

## 6.2 NOT IN

Find products that do not appear in the West region:


```sql
SELECT DISTINCT product
FROM sales
WHERE product NOT IN (
    SELECT product
    FROM sales
    WHERE region = 'West'
);
```

With our sample data, the result is empty because every 
product in the table has been sold in the West.

## 6.3 IN with a grouped subquery

Find salespeople who have generated more than 3000 in total revenue:


```sql
SELECT
    sale_id,
    salesperson,
    amount
FROM sales
WHERE salesperson IN (
    SELECT salesperson
    FROM sales
    GROUP BY salesperson
    HAVING SUM(amount) > 3000
)
ORDER BY sale_id;
```

* The inner query identifies qualifying salespeople. 
* The outer query retrieves their individual transactions.

**This is an important distinction:**

- The inner query operates on salesperson-level totals.
- The outer query operates on individual sales.

## 6.4 A warning about NOT IN and NULL

`NOT IN` can behave unexpectedly when the inner query contains `NULL`.

Consider:



```sql
SELECT 1
WHERE 2 NOT IN (1, NULL);
```

The result is no row. SQL cannot establish that `2` is 
different from every item because one item is unknown.

* When using `NOT IN`, consider whether the subquery can return `NULL`. 
* Often, `NOT EXISTS` is safer for finding unmatched rows.

For example:


```sql
SELECT DISTINCT s.product
FROM sales AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM sales AS w
    WHERE w.product = s.product
      AND w.region = 'West'
);
```

This version expresses the question directly: return products for which no West-region row matches.

---

# 7\. EXISTS and NOT EXISTS

## 7.1 What does EXISTS mean?

`EXISTS` checks whether a subquery returns at least one row.

It does not require the inner query to return a particular column value.

Example:


```sql
SELECT *
FROM sales AS s
WHERE EXISTS (
    SELECT 1
    FROM sales AS x
    WHERE x.amount > 2000
);
```

Because at least one sale exceeds 2000, 
the condition is true for every row in `sales`. 
This query is deliberately simple to illustrate the logic.

The expression `SELECT 1` is conventional: `EXISTS` cares 
about whether a row exists, not the selected value.

## 7.2 Correlate EXISTS with the outer row

Find salespeople who have at least one sale above 2000:


```sql
SELECT DISTINCT s.salesperson
FROM sales AS s
WHERE EXISTS (
    SELECT 1
    FROM sales AS x
    WHERE x.salesperson = s.salesperson
      AND x.amount > 2000
);
```

The inner query refers to `s.salesperson`, which comes from the outer query.

The result includes Alice and Bob because each has at least one qualifying transaction.

## 7.3 Find salespeople with no sale above 2000


```sql
SELECT DISTINCT s.salesperson
FROM sales AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM sales AS x
    WHERE x.salesperson = s.salesperson
      AND x.amount > 2000
);
```

Carol is returned because she has no sale greater than 2000.

## 7.4 EXISTS versus IN

Both can solve some of the same problems.

Using `IN`:


```sql
SELECT DISTINCT salesperson
FROM sales
WHERE salesperson IN (
    SELECT salesperson
    FROM sales
    WHERE amount > 2000
);
```

Using `EXISTS`:


```sql
SELECT DISTINCT s.salesperson
FROM sales AS s
WHERE EXISTS (
    SELECT 1
    FROM sales AS x
    WHERE x.salesperson = s.salesperson
      AND x.amount > 2000
);
```

Both express the idea of identifying salespeople with a qualifying sale.

* Use `EXISTS` when the question is naturally about whether a 
  matching row exists. 
* Use `IN` when membership in a set is the clearest expression.

---

# 8\. Subqueries in SELECT

A subquery in the `SELECT` list calculates a value for each output row.

## 8.1 Show the average next to every sale


```sql
SELECT
    sale_id,
    product,
    amount,
    (SELECT AVG(amount) FROM sales) AS average_sale
FROM sales
ORDER BY sale_id;
```

The average is repeated on each output row.

This can be helpful when comparing each transaction with a benchmark.

## 8.2 Compare each sale with the overall average

sql

```
SELECT
    sale_id,
    product,
    amount,
    (SELECT AVG(amount) FROM sales) AS average_sale,
    amount - (SELECT AVG(amount) FROM sales) AS difference_from_average
FROM sales
ORDER BY sale_id;
```

* A positive difference means the transaction is above average. 
* A negative difference means it is below average.

A cleaner alternative is to calculate the average once in a CTE:



```sql
WITH overall AS (
    SELECT AVG(amount) AS average_sale
    FROM sales
)
SELECT
    s.sale_id,
    s.product,
    s.amount,
    o.average_sale,
    s.amount - o.average_sale AS difference_from_average
FROM sales AS s
CROSS JOIN overall AS o
ORDER BY s.sale_id;
```

The `CROSS JOIN` is safe here because `overall` returns exactly one row.

## 8.3 A scalar subquery must have scalar cardinality

If a subquery used in the `SELECT` list returns multiple rows 
where one value is required, the query fails.

For example, this is not a valid way to attach all West-region 
amounts to every sale:



```sql
-- Incorrect: the inner query can return multiple rows.
SELECT
    sale_id,
    (
        SELECT amount
        FROM sales
        WHERE region = 'West'
    ) AS west_amount
FROM sales;
```

Choose an aggregate, a join, a list-producing expression, or 
another appropriate technique depending on the desired output.

---

# 9\. Subqueries in FROM

A subquery in the `FROM` clause is often called a **derived table**.

It produces a table-like result that the outer query can filter or aggregate.

## 9.1 Aggregate first, then filter

Find salespeople with total revenue above 3000:


```sql
SELECT
    salesperson,
    total_revenue
FROM (
    SELECT
        salesperson,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
) AS salesperson_totals
WHERE total_revenue > 3000
ORDER BY total_revenue DESC;
```

The inner query calculates one row per salesperson.

The outer query filters the aggregated results.

The alias `salesperson_totals` is important: a derived table needs a name.

## 9.2 Calculate average revenue per salesperson



```sql
SELECT AVG(total_revenue) AS average_salesperson_revenue
FROM (
    SELECT
        salesperson,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
) AS salesperson_totals;
```

This is different from `AVG(amount)`.

- `AVG(amount)` calculates the average transaction amount.
- This query calculates each salesperson's total and then averages those totals.

Understanding which level you are aggregating is one of the most important SQL skills.

## 9.3 Multiple aggregation levels

Find salespeople whose total revenue exceeds the average salesperson total:



```sql
SELECT
    salesperson,
    total_revenue
FROM (
    SELECT
        salesperson,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
) AS salesperson_totals
WHERE total_revenue > (
    SELECT AVG(total_revenue)
    FROM (
        SELECT SUM(amount) AS total_revenue
        FROM sales
        GROUP BY salesperson
    ) AS totals
)
ORDER BY total_revenue DESC;
```

This query has two levels of aggregation:

1. Sum transaction amounts per salesperson.
2. Average those salesperson totals.

It is valid, but it repeats logic. The next section 
introduces `WITH`, which often makes this kind of 
query easier to read.

---

# 10\. Correlated subqueries

A **correlated subquery** refers to a column from the outer query.

Unlike a self-contained subquery, its logic depends on the current outer row.

## 10.1 Compare each sale with its salesperson's average


```sql
SELECT
    s.sale_id,
    s.salesperson,
    s.amount
FROM sales AS s
WHERE s.amount > (
    SELECT AVG(x.amount)
    FROM sales AS x
    WHERE x.salesperson = s.salesperson
)
ORDER BY s.salesperson, s.amount DESC;
```

The condition:


```sql
x.salesperson = s.salesperson
```

connects the inner query to the current outer row.

Conceptually:

1. Identify an outer sale.
2. Calculate the average for that sale's salesperson.
3. Compare the sale amount with that average.
4. Repeat the logic for the other outer rows.

The optimizer may use a more efficient execution strategy 
than literally running the inner query once per row.

## 10.2 Find the highest sale for each salesperson


```sql
SELECT
    s.sale_id,
    s.salesperson,
    s.product,
    s.amount
FROM sales AS s
WHERE s.amount = (
    SELECT MAX(x.amount)
    FROM sales AS x
    WHERE x.salesperson = s.salesperson
)
ORDER BY s.salesperson;
```

This returns all tied maximum transactions if a salesperson 
has multiple sales at their maximum amount.

## 10.3 Find sales above their region's average


```sql
SELECT
    s.sale_id,
    s.region,
    s.amount
FROM sales AS s
WHERE s.amount > (
    SELECT AVG(x.amount)
    FROM sales AS x
    WHERE x.region = s.region
)
ORDER BY s.region, s.amount DESC;
```

This is a common analytical pattern: compare a record 
with a benchmark calculated for its group.

## 10.4 Correlated subquery versus window function

The same problem can often be solved using a window function:



```sql
SELECT
    sale_id,
    salesperson,
    amount
FROM (
    SELECT
        sale_id,
        salesperson,
        amount,
        AVG(amount) OVER (
            PARTITION BY salesperson
        ) AS salesperson_average
    FROM sales
) AS x
WHERE amount > salesperson_average
ORDER BY salesperson, amount DESC;
```

The window function makes the group average available alongside each transaction.

Neither approach is universally better. Choose the version that is easiest to understand and maintain, then compare performance if it matters.

---

# 11\. Nested subqueries

A nested subquery is a subquery inside another subquery.

## 11.1 Find salespeople whose total revenue exceeds the average salesperson revenue


```sql
SELECT
    salesperson,
    SUM(amount) AS total_revenue
FROM sales
GROUP BY salesperson
HAVING SUM(amount) > (
    SELECT AVG(person_total)
    FROM (
        SELECT SUM(amount) AS person_total
        FROM sales
        GROUP BY salesperson
    ) AS totals
)
ORDER BY total_revenue DESC;
```

The inner derived table calculates total revenue per salesperson.

The next level calculates the average of those totals.

The outer query returns salespeople whose totals exceed that average.

## 11.2 Find products sold in regions where average sale amount exceeds 900


```sql
SELECT DISTINCT product
FROM sales
WHERE region IN (
    SELECT region
    FROM sales
    GROUP BY region
    HAVING AVG(amount) > 900
)
ORDER BY product;
```

* The inner query determines which regions qualify. 
* The outer query finds products sold in those regions.


## 11.3 Understand nested-query structure

When reading a nested query, start with the deepest subquery and work outward.

Ask these questions:

1. What rows does the innermost query return?
2. Does it return a scalar, one row, or multiple rows?
3. How does the next query use that result?
4. What does the final query return?

If a nested query is becoming difficult to follow, 
consider breaking it into named CTEs.

---

# 12\. ANY, ALL, and comparison operators

SQL provides comparison operators that work with sets of values.

DuckDB supports quantified comparisons such as `ANY` and `ALL`.

## 12.1 Greater than ANY

Find sales whose amount is greater than at least one West-region sale:


```sql
SELECT
    sale_id,
    amount
FROM sales
WHERE amount > ANY (
    SELECT amount
    FROM sales
    WHERE region = 'West'
)
ORDER BY amount;
```

For a nonempty set of ordinary, non-`NULL` numeric 
values, `x > ANY (set)` is true when `x` exceeds at 
least one value in the set.

It is therefore similar to comparing against the 
minimum value, although the quantified comparison 
has its own `NULL` and empty-set semantics.

## 12.2 Greater than ALL

Find sales whose amount is greater than every West-region sale:


```sql
SELECT
    sale_id,
    amount
FROM sales
WHERE amount > ALL (
    SELECT amount
    FROM sales
    WHERE region = 'West'
)
ORDER BY amount;
```

For a nonempty set without `NULL`, `x > ALL (set)` 
means `x` exceeds the maximum value in that set.

## 12.3 ANY versus ALL

| Expression | Meaning for a nonempty set without NULL |
| --- | --- |
| `x > ANY (set)` | Greater than at least one value |
| `x > ALL (set)` | Greater than every value |
| `x = ANY (set)` | Matches at least one value; similar to `IN` |
| `x <> ALL (set)` | Different from every value |

* Be careful with empty sets and `NULL` values. 
* SQL uses three-valued logic: `TRUE`, `FALSE`, and `UNKNOWN`.
* For most beginner tasks, `IN`, `EXISTS`, `MIN`, and `MAX` 
  are often more intuitive. 
* Learn `ANY` and `ALL` when the question explicitly involves 
  comparing against some or all values in a set.

---

# 13\. WITH and common table expressions

This is one of the most important sections of the tutorial.

A **common table expression (CTE)** gives a query result a 
name for use within a larger statement.

CTEs are introduced with `WITH`.

## 13.1 Basic CTE


```sql
WITH average_sale AS (
    SELECT AVG(amount) AS avg_amount
    FROM sales
)
SELECT
    s.sale_id,
    s.product,
    s.amount,
    a.avg_amount
FROM sales AS s
CROSS JOIN average_sale AS a
WHERE s.amount > a.avg_amount
ORDER BY s.amount DESC;
```

Read the query in two parts:

1. `average_sale` calculates the average.
2. The main query uses the named result.
3. A CTE does not create a permanent table. 
   Its name is available to the statement in which it is defined.

## 13.2 Multiple CTEs

You can define multiple CTEs, separated by commas.


```sql
WITH salesperson_totals AS (
    SELECT
        salesperson,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
),
overall_average AS (
    SELECT AVG(total_revenue) AS avg_revenue
    FROM salesperson_totals
)
SELECT
    st.salesperson,
    st.total_revenue,
    oa.avg_revenue
FROM salesperson_totals AS st
CROSS JOIN overall_average AS oa
WHERE st.total_revenue > oa.avg_revenue
ORDER BY st.total_revenue DESC;
```

* The first CTE calculates total revenue by salesperson.

* The second CTE calculates the average of those totals.

* The final query compares each salesperson's total with the average.

## 13.3 A CTE that replaces a nested derived table

Compare this:


```sql
SELECT
    salesperson,
    total_revenue
FROM (
    SELECT
        salesperson,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
) AS totals
WHERE total_revenue > 3000;
```

With this:


```sql
WITH totals AS (
    SELECT
        salesperson,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
)
SELECT
    salesperson,
    total_revenue
FROM totals
WHERE total_revenue > 3000;
```

* Both express the same logical operation. 
* The CTE version gives the intermediate result a name before the final query uses it.

## 13.4 Reusing a CTE


```sql
WITH totals AS (
    SELECT
        salesperson,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
)
SELECT
    t1.salesperson,
    t1.total_revenue,
    (
        SELECT AVG(t2.total_revenue)
        FROM totals AS t2
    ) AS average_person_total
FROM totals AS t1
ORDER BY t1.total_revenue DESC;
```

The named result `totals` is referenced more than once.

This is useful for readability, but it does not mean 
a CTE is always physically computed and stored exactly 
once. DuckDB can inline or materialize CTEs depending 
on the query and applicable optimizer rules.

## 13.5 CTE with filtering and aggregation


```sql
WITH west_sales AS (
    SELECT *
    FROM sales
    WHERE region = 'West'
),
product_totals AS (
    SELECT
        product,
        SUM(amount) AS total_revenue
    FROM west_sales
    GROUP BY product
)
SELECT
    product,
    total_revenue
FROM product_totals
WHERE total_revenue > 1000
ORDER BY total_revenue DESC;
```

The steps are:

1. Filter transactions to the West region.
2. Calculate revenue by product.
3. Keep products whose total revenue exceeds 1000.

The names make the transformation easier to understand.

## 13.6 CTE versus subquery

Use a subquery when the intermediate logic is short 
and naturally belongs inside another expression.

Use a CTE when:

- The query has multiple logical steps.
- An intermediate result needs a meaningful name.
- The result is referenced more than once.
- The query is difficult to read because of nested parentheses.
- You want to make a complex analytical transformation easier to maintain.

CTEs and subqueries are not fundamentally different kinds of data. They are alternative ways of expressing query logic.

## 13.7 Recursive CTEs

A recursive CTE repeatedly generates rows using 
a previously generated result. It is useful for 
sequences, hierarchical data, and graph traversal.

Here is a simple number sequence:


```sql
WITH RECURSIVE numbers(n) AS (
    SELECT 1

    UNION ALL

    SELECT n + 1
    FROM numbers
    WHERE n < 10
)
SELECT n
FROM numbers
ORDER BY n;
```

Expected output:


```text
1
2
3
4
5
6
7
8
9
10
```

The anchor query creates the first row, `1`.

The recursive query generates the next value 
from the previous result, stopping when `n` reaches 10.

A recursive CTE has two conceptual parts:

- **Anchor member:** establishes the initial result.
- **Recursive member:** generates additional rows.

Use a clear stopping condition. A recursive query 
without an appropriate termination condition can 
generate far more rows than intended.

---

# 14\. Additional subquery patterns with one table

## 14.1 Aggregate in the outer query, filter with a subquery

Find total revenue per salesperson for salespeople 
who have made a transaction above 1500:


```sql
SELECT
    salesperson,
    SUM(amount) AS total_revenue
FROM sales
WHERE salesperson IN (
    SELECT salesperson
    FROM sales
    WHERE amount > 1500
)
GROUP BY salesperson
ORDER BY total_revenue DESC;
```

## 14.2 Compare a product with its own category average


```sql
SELECT
    s.sale_id,
    s.product,
    s.category,
    s.amount
FROM sales AS s
WHERE s.amount > (
    SELECT AVG(x.amount)
    FROM sales AS x
    WHERE x.category = s.category
)
ORDER BY s.category, s.amount DESC;
```

This compares each transaction with the average for its category.

## 14.3 Find duplicate product names


```sql
SELECT product, 
       COUNT(*) AS transaction_count
FROM sales
GROUP BY product
HAVING COUNT(*) > 1
ORDER BY transaction_count DESC;
```

* This query does not require a subquery. 
* That is an important lesson: SQL problems do not always need one.
* A direct aggregation is often simpler than wrapping a query inside another query.

---

# 15\. Part II — Introduce two related tables

Now we will use two tables:

- `sales`: transaction information.
- `products`: product information.

The tables are related by `product_id`.

Using a numeric key rather than repeating the product name makes the relationship explicit and avoids depending on text labels to identify products.

## 15.1 Create the products table



```sql
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INTEGER,
    product_name VARCHAR,
    category VARCHAR,
    list_price DECIMAL(10, 2)
);
```

Insert sample products:



```sql
INSERT INTO products VALUES
(101, 'Laptop',  'Electronics', 1200.00),
(102, 'Phone',   'Electronics',  700.00),
(103, 'Desk',    'Furniture',    450.00),
(104, 'Chair',   'Furniture',    200.00),
(105, 'Monitor', 'Electronics',  300.00),
(106, 'Tablet',  'Electronics',  500.00);
```

## 15.2 Create a new sales table with product IDs

To keep the two-table examples self-contained, 
we will replace the original `sales` table with 
a version that includes `product_id`.


```sql
DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    sale_id INTEGER,
    sale_date DATE,
    product_id INTEGER,
    salesperson VARCHAR,
    region VARCHAR,
    quantity INTEGER,
    amount DECIMAL(10, 2)
);
```

Insert the same transactions using product IDs:


```sql
INSERT INTO sales VALUES
(1,  DATE '2026-01-05', 101, 'Alice', 'West',  2, 2400.00),
(2,  DATE '2026-01-06', 102, 'Bob',   'East',  3, 2100.00),
(3,  DATE '2026-01-07', 103, 'Alice', 'West',  1,  450.00),
(4,  DATE '2026-01-08', 104, 'Carol', 'East',  4,  800.00),
(5,  DATE '2026-01-09', 101, 'Bob',   'West',  1, 1200.00),
(6,  DATE '2026-01-10', 105, 'Alice', 'East',  2,  600.00),
(7,  DATE '2026-01-11', 103, 'Bob',   'East',  2,  900.00),
(8,  DATE '2026-01-12', 102, 'Carol', 'West',  1,  700.00),
(9,  DATE '2026-01-13', 104, 'Alice', 'West',  2,  400.00),
(10, DATE '2026-01-14', 105, 'Bob',   'East',  3,  900.00),
(11, DATE '2026-01-15', 103, 'Carol', 'West',  1,  500.00),
(12, DATE '2026-01-16', 101, 'Alice', 'East',  1, 1200.00),
(13, DATE '2026-01-17', 104, 'Bob',   'West',  3,  600.00),
(14, DATE '2026-01-18', 102, 'Alice', 'West',  2, 1400.00),
(15, DATE '2026-01-19', 103, 'Bob',   'East',  1,  450.00);
```

Verify the tables:


```sql
SELECT * FROM products ORDER BY product_id;

SELECT * FROM sales ORDER BY sale_id;
```

We now have six products and fifteen sales transactions.

Notice that product 106, Tablet, has no matching 
sales transaction. This will help us understand 
matching rows, unmatched rows, and `EXISTS`.

**Important:** Run this setup after completing 
the first part. The new `sales` table replaces 
the earlier version.

---

# 16\. INNER JOIN fundamentals

An `INNER JOIN` combines rows from two tables 
when their join condition matches.

## 16.1 Basic INNER JOIN


```sql
SELECT
    s.sale_id,
    p.product_name,
    p.category,
    s.salesperson,
    s.amount
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
ORDER BY s.sale_id;
```

The condition:

```sql
ON s.product_id = p.product_id
```

connects each transaction to its product.

* Every sales row in our sample has a matching product. 
* Therefore, this query returns fifteen rows.

## 16.2 Filter the joined results

Find electronics sales above 1000:


```sql
SELECT
    s.sale_id,
    p.product_name,
    s.amount
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
WHERE p.category = 'Electronics'
  AND s.amount > 1000
ORDER BY s.amount DESC;
```

* The join provides the product category. 
* The `WHERE` clause filters the combined rows.

## 16.3 Aggregate after joining

Calculate revenue by product:


```sql
SELECT
    p.product_name,
    SUM(s.amount) AS total_revenue
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC;
```

Only products with matching sales appear because 
this is an `INNER JOIN`.

## 16.4 Find products without sales

An `INNER JOIN` is not the right tool when you want 
to keep unmatched products. A `LEFT JOIN` can expose 
missing matches:


```sql
SELECT
    p.product_id,
    p.product_name
FROM products AS p
LEFT JOIN sales AS s
    ON p.product_id = s.product_id
WHERE s.sale_id IS NULL;
```

Expected result:

| `product_id` | `product_name` |
| --- | --- |
| 106 | Tablet |

We will also solve this problem using `NOT EXISTS` later.

---

# 17\. Subqueries with two tables

This section combines subqueries with joins.

## 17.1 Use a subquery to filter sales by product category

Find transactions for products in the Furniture category:


```sql
SELECT
    sale_id,
    product_id,
    amount
FROM sales
WHERE product_id IN (
    SELECT product_id
    FROM products
    WHERE category = 'Furniture'
)
ORDER BY sale_id;
```

* The inner query returns furniture product IDs. 
* The outer query selects transactions that reference those IDs.

Compare it with the join version:


```sql
SELECT
    s.sale_id,
    s.product_id,
    s.amount
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
WHERE p.category = 'Furniture'
ORDER BY s.sale_id;
```

* Both are appropriate for this task. 
* The join version is often more natural when the 
  final output needs columns from both tables.

## 17.2 Use EXISTS to find products that have sales


```sql
SELECT
    p.product_id,
    p.product_name
FROM products AS p
WHERE EXISTS (
    SELECT 1
    FROM sales AS s
    WHERE s.product_id = p.product_id
)
ORDER BY p.product_id;
```

This returns products for which at least one matching 
transaction exists.

Each product appears at most once in the outer result, 
because the outer table contains one row per product 
and `EXISTS` tests existence rather than returning all 
matching sales.

## 17.3 Use NOT EXISTS to find products without sales



```sql
SELECT
    p.product_id,
    p.product_name
FROM products AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM sales AS s
    WHERE s.product_id = p.product_id
)
ORDER BY p.product_id;
```

Expected result:

| `product_id` | `product_name` |
| --- | --- |
| 106 | Tablet |

This is an example of an **anti-join pattern**: 
return rows from one table that have no matching 
row in another.

## 17.4 Compare the two anti-join patterns

Using `LEFT JOIN`:


```sql
SELECT p.product_id, p.product_name
FROM products AS p
LEFT JOIN sales AS s
    ON p.product_id = s.product_id
WHERE s.sale_id IS NULL;
```

Using `NOT EXISTS`:


```sql
SELECT p.product_id, p.product_name
FROM products AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM sales AS s
    WHERE s.product_id = p.product_id
);
```

Both identify products without sales.

`NOT EXISTS` often communicates the business 
question directly and avoids the `NULL` pitfalls 
associated with `NOT IN`.

## 17.5 Find sales above the average sale amount for their product category


```sql
SELECT
    s.sale_id,
    p.product_name,
    p.category,
    s.amount
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
WHERE s.amount > (
    SELECT AVG(s2.amount)
    FROM sales AS s2
    INNER JOIN products AS p2
        ON s2.product_id = p2.product_id
    WHERE p2.category = p.category
)
ORDER BY p.category, s.amount DESC;
```

* This is a correlated subquery involving two tables.

* The inner query calculates the average transaction 
  amount for the category of the current outer product.

* The outer query returns transactions above that 
  category average.

* The reference `p.category` is from the outer query. 
  That reference makes the inner query correlated.


## 17.6 Find the highest transaction for each product


```sql
SELECT
    s.sale_id,
    p.product_name,
    s.amount
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
WHERE s.amount = (
    SELECT MAX(s2.amount)
    FROM sales AS s2
    WHERE s2.product_id = s.product_id
)
ORDER BY p.product_name;
```

This finds each product's highest transaction amount.

If several transactions tie for the highest amount, 
all tied rows are returned.

## 17.7 Find products whose total revenue exceeds average product revenue


```sql
WITH product_totals AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(s.amount) AS total_revenue
    FROM products AS p
    INNER JOIN sales AS s
        ON p.product_id = s.product_id
    GROUP BY p.product_id, p.product_name
),
average_product_revenue AS (
    SELECT AVG(total_revenue) AS avg_revenue
    FROM product_totals
)
SELECT
    pt.product_name,
    pt.total_revenue
FROM product_totals AS pt
CROSS JOIN average_product_revenue AS a
WHERE pt.total_revenue > a.avg_revenue
ORDER BY pt.total_revenue DESC;
```

This combines several important skills:

1. Join sales with products.
2. Aggregate sales by product.
3. Calculate the average of the product totals.
4. Compare each product total with that average.

Notice that the average is calculated over product totals, not individual transactions.

## 17.8 Use a subquery in FROM with a join

Calculate revenue by category using an intermediate table:


```sql
SELECT
    category_totals.category,
    SUM(category_totals.product_revenue) AS total_revenue
FROM (
    SELECT
        p.category,
        p.product_id,
        SUM(s.amount) AS product_revenue
    FROM products AS p
    INNER JOIN sales AS s
        ON p.product_id = s.product_id
    GROUP BY p.category, p.product_id
) AS category_totals
GROUP BY category_totals.category
ORDER BY total_revenue DESC;
```

* The derived table calculates revenue by product. 
* The outer query aggregates those results by category.

The same result can be expressed more simply with a 
direct join and grouping:


```sql
SELECT
    p.category,
    SUM(s.amount) AS total_revenue
FROM products AS p
INNER JOIN sales AS s
    ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
```

The simpler version is preferable when no intermediate 
aggregation is needed.

## 17.9 Use a CTE to make a two-table query readable


```sql
WITH joined_sales AS (
    SELECT
        s.sale_id,
        s.product_id,
        p.product_name,
        p.category,
        s.salesperson,
        s.amount
    FROM sales AS s
    INNER JOIN products AS p
        ON s.product_id = p.product_id
),
product_totals AS (
    SELECT
        product_id,
        product_name,
        category,
        SUM(amount) AS total_revenue
    FROM joined_sales
    GROUP BY product_id, product_name, category
)
SELECT *
FROM product_totals
WHERE total_revenue > 1500
ORDER BY total_revenue DESC;
```

Here, the CTEs represent logical steps:

- `joined_sales` combines the tables.
- `product_totals` aggregates transactions by product.
- The final query filters the totals.

This is a good approach for queries that will be maintained or extended by other developers.

---

# 18\. JOIN versus subquery versus CTE

There is no universal rule that joins are always faster or subqueries are always slower. DuckDB's optimizer can transform many equivalent queries into similar execution plans.

Choose syntax based on the question, required output, and readability.

| Requirement | Commonly clear approach |
| --- | --- |
| Return columns from two matching tables | `INNER JOIN` |
| Filter rows based on a set of values | `IN (subquery)` |
| Check whether a related row exists | `EXISTS` |
| Find rows without a match | `NOT EXISTS` or `LEFT JOIN ... IS NULL` |
| Compare a value with an aggregate | Scalar subquery |
| Calculate a group-specific benchmark | Correlated subquery or window function |
| Create a table-like intermediate result | Derived table or CTE |
| Break a complex query into named steps | `WITH` |
| Generate hierarchical or iterative results | Recursive CTE |

## 18.1 Three equivalent-looking ways to filter products

Using a subquery:


```sql
SELECT product_id, product_name
FROM products
WHERE product_id IN (
    SELECT product_id
    FROM sales
);
```

Using `EXISTS`:


```sql
SELECT p.product_id, p.product_name
FROM products AS p
WHERE EXISTS (
    SELECT 1
    FROM sales AS s
    WHERE s.product_id = p.product_id
);
```

Using a join:


```sql
SELECT DISTINCT p.product_id, p.product_name
FROM products AS p
INNER JOIN sales AS s
    ON p.product_id = s.product_id;
```

These return the products with sales for this dataset.

The `DISTINCT` in the join version is necessary 
to remove repeated product rows caused by multiple 
transactions.

The `IN` and `EXISTS` versions naturally return 
each qualifying product once, given the unique 
product rows in `products`.

## 18.2 Why JOIN can create duplicates

Suppose one product has ten sales.

A join between the product row and the sales 
table produces ten joined rows for that product. 
That is correct relational behavior.

If you want one row per product, use an appropriate 
aggregation or `DISTINCT`.

Do not add `DISTINCT` automatically. First decide 
whether multiple rows are meaningful in your result.

## 18.3 When a CTE is not necessary

This is perfectly reasonable:


```sql
SELECT *
FROM sales
WHERE amount > 1000;
```

* There is no need to wrap it in a CTE just 
  because CTEs are available.

* Use additional structure when it improves 
  clarity or expresses a genuinely multi-step 
  calculation.

---

# 19\. Advanced analytical examples

## 19.1 Top sale per category

Return every transaction tied for the highest 
amount within its product category:


```sql
SELECT
    s.sale_id,
    p.product_name,
    p.category,
    s.amount
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
WHERE s.amount = (
    SELECT MAX(s2.amount)
    FROM sales AS s2
    INNER JOIN products AS p2
        ON s2.product_id = p2.product_id
    WHERE p2.category = p.category
)
ORDER BY p.category, s.amount DESC;
```

## 19.2 Compare each product's revenue with its category average


```sql
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(s.amount) AS total_revenue
    FROM products AS p
    INNER JOIN sales AS s
        ON p.product_id = s.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT
    pr.product_name,
    pr.category,
    pr.total_revenue
FROM product_revenue AS pr
WHERE pr.total_revenue > (
    SELECT AVG(pr2.total_revenue)
    FROM product_revenue AS pr2
    WHERE pr2.category = pr.category
)
ORDER BY pr.category, pr.total_revenue DESC;
```

* This example is particularly useful because it 
compares **product-level revenue** with the 
**average product-level revenue in the same category**.

* The average is not the average transaction amount.

## 19.3 Use a window function instead

The same comparison can be written with a window function:


```sql
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(s.amount) AS total_revenue
    FROM products AS p
    INNER JOIN sales AS s
        ON p.product_id = s.product_id
    GROUP BY p.product_id, p.product_name, p.category
),
scored_products AS (
    SELECT
        *,
        AVG(total_revenue) OVER (
            PARTITION BY category
        ) AS category_average
    FROM product_revenue
)
SELECT
    product_name,
    category,
    total_revenue,
    category_average
FROM scored_products
WHERE total_revenue > category_average
ORDER BY category, total_revenue DESC;
```

* The first CTE calculates product totals. 
* The second calculates the average for each 
  category using a window function. 
* The final query filters products above that average.

This is often a very readable pattern for analytical work.

## 19.4 Revenue by region above the average regional revenue


```sql
WITH region_totals AS (
    SELECT
        region,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY region
)
SELECT
    region,
    total_revenue
FROM region_totals
WHERE total_revenue > (
    SELECT AVG(total_revenue)
    FROM region_totals
)
ORDER BY total_revenue DESC;
```

This example uses only the sales table in the 
two-table schema.

It demonstrates that a CTE can simplify nested 
aggregation even when joins are not needed.

## 19.5 Products with no transactions using NOT IN safely

A version that explicitly excludes `NULL` from the 
inner result is:


```sql
SELECT
    product_id,
    product_name
FROM products
WHERE product_id NOT IN (
    SELECT product_id
    FROM sales
    WHERE product_id IS NOT NULL
);
```

This works for the current schema and data.

Nevertheless, for anti-join logic, `NOT EXISTS` 
is often the more direct expression and does not 
have the same `NOT IN` null-trap.

## 19.6 Calculate a percentage of total revenue


```sql
WITH total_revenue AS (
    SELECT SUM(amount) AS grand_total
    FROM sales
)
SELECT
    s.sale_id,
    s.amount,
    t.grand_total,
    100.0 * s.amount / NULLIF(t.grand_total, 0) AS percent_of_total
FROM sales AS s
CROSS JOIN total_revenue AS t
ORDER BY s.sale_id;
```

* `NULLIF(t.grand_total, 0)` prevents division by zero. 
* If the grand total were zero, the expression would 
  return `NULL` instead of dividing by zero.

## 19.7 Build a reusable reporting query


```sql
WITH joined_sales AS (
    SELECT
        s.sale_id,
        s.region,
        s.salesperson,
        s.amount,
        p.product_name,
        p.category
    FROM sales AS s
    INNER JOIN products AS p
        ON s.product_id = p.product_id
),
category_region_totals AS (
    SELECT
        category,
        region,
        SUM(amount) AS total_revenue
    FROM joined_sales
    GROUP BY category, region
),
category_averages AS (
    SELECT
        category,
        AVG(total_revenue) AS average_region_revenue
    FROM category_region_totals
    GROUP BY category
)
SELECT
    crt.category,
    crt.region,
    crt.total_revenue,
    ca.average_region_revenue
FROM category_region_totals AS crt
INNER JOIN category_averages AS ca
    ON crt.category = ca.category
WHERE crt.total_revenue > ca.average_region_revenue
ORDER BY crt.category, crt.total_revenue DESC;
```

This query follows a reporting pipeline:

1. Combine transactions with product information.
2. Calculate revenue by category and region.
3. Calculate average regional revenue within each category.
4. Return regions above their category's average.

It demonstrates how joins, aggregation, 
CTEs, and comparisons work together.

---

# 20\. Common mistakes and debugging

## 20.1 Using `=` when the subquery returns multiple rows

**Incorrect:**


```sql
SELECT *
FROM sales
WHERE product_id = (
    SELECT product_id
    FROM sales
);
```

The inner query returns multiple rows.

Use `IN` when membership is intended:


```sql
SELECT *
FROM sales
WHERE product_id IN (
    SELECT product_id
    FROM sales
);
```

## 20.2 Forgetting the alias for a derived table

**Incorrect:**


```sql
SELECT *
FROM (
    SELECT product_id
    FROM sales
);
```

In DuckDB, a derived table should be given 
an alias for portable, clear SQL:


```sql
SELECT *
FROM (
    SELECT product_id
    FROM sales
) AS product_ids;
```

## 20.3 Using an aggregate in WHERE at the wrong query level

**Incorrect:**


```sql
SELECT salesperson, SUM(amount)
FROM sales
WHERE SUM(amount) > 3000
GROUP BY salesperson;
```

* The `WHERE` clause filters input rows before grouping. 
* Aggregate filters belong in `HAVING`.

**Correct:**


```sql
SELECT salesperson, SUM(amount) AS total_revenue
FROM sales
GROUP BY salesperson
HAVING SUM(amount) > 3000;
```

Alternatively, aggregate in a subquery and filter the derived result:


```sql
SELECT *
FROM (
    SELECT salesperson, SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
) AS totals
WHERE total_revenue > 3000;
```

## 20.4 Confusing a transaction average with an average of group totals

These queries answer different questions.

Average transaction amount:

```sql
SELECT AVG(amount)
FROM sales;
```

Average salesperson total:


```sql
SELECT AVG(total_revenue)
FROM (
    SELECT SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
) AS totals;
```

Always identify the level at which the metric is calculated.

## 20.5 Using NOT IN without checking for NULL

**Risky:**


```sql
SELECT product_id
FROM products
WHERE product_id NOT IN (
    SELECT product_id
    FROM sales
);
```

If the subquery contains `NULL`, the results 
may not match your expectations.

**Prefer:**


```sql
SELECT p.product_id
FROM products AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM sales AS s
    WHERE s.product_id = p.product_id
);
```

## 20.6 Getting duplicates after a join

* A join returns one row for every matching pair of rows. 
* Multiple sales for the same product therefore generate multiple joined rows.
* If the goal is one row per product, aggregate the sales or use `DISTINCT` where appropriate.

## 20.7 Forgetting correlated aliases

Use explicit aliases to distinguish the outer and inner tables:


```sql
SELECT s.sale_id
FROM sales AS s
WHERE s.amount > (
    SELECT AVG(x.amount)
    FROM sales AS x
    WHERE x.salesperson = s.salesperson
);
```

Here, `s` refers to the outer row and `x` 
refers to rows examined by the inner query.

## 20.8 Assuming a CTE is a permanent table

* A CTE exists for the statement in which 
  it is defined. 
* To persist results, use a table or another 
  appropriate storage mechanism.

## 20.9 Assuming every subquery is evaluated literally first

SQL describes the requested result, not a mandatory 
step-by-step physical execution plan.

DuckDB can optimize joins, subqueries, and CTEs. 
For performance-sensitive work, inspect the actual 
plan with:


```sql
EXPLAIN
SELECT *
FROM sales
WHERE amount > (
    SELECT AVG(amount)
    FROM sales
);
```

For actual execution profiling, DuckDB also 
provides profiling features, which are useful 
when investigating a real workload.

---

# 21\. Performance considerations in DuckDB

DuckDB is a column-oriented analytical database, 
so efficient SQL should express the desired operation 
clearly and allow its optimizer to work.

## 21.1 Prefer clear SQL first

* Do not automatically replace every subquery with a join. 
* Many subqueries can be optimized effectively, and 
  some patterns are clearer as subqueries.

For example, existence checks are naturally expressed 
with `EXISTS`:


```sql
SELECT p.product_name
FROM products AS p
WHERE EXISTS (
    SELECT 1
    FROM sales AS s
    WHERE s.product_id = p.product_id
);
```

## 21.2 Avoid unnecessary repeated calculations

If several expressions use the same intermediate 
aggregation, a CTE may improve readability and 
may help avoid repeated work, depending on the 
query and optimization decisions.

However, CTE materialization is not guaranteed 
in every situation.

## 21.3 Use EXPLAIN


```sql
EXPLAIN
SELECT
    p.product_name,
    SUM(s.amount) AS total_revenue
FROM products AS p
INNER JOIN sales AS s
    ON p.product_id = s.product_id
GROUP BY p.product_name;
```

The output describes the planned operators. 
Look for operations such as scans, joins, 
filters, and aggregations.

## 21.4 Measure rather than guess

For large datasets, compare equivalent queries 
using realistic data. Factors include:

- Number of rows.
- Number of distinct keys.
- Data types.
- Amount of aggregation.
- Whether intermediate results can be reused.
- Query plan choices.

* Correctness and readability should come first. 
* Optimize based on measurements.

---

# 22\. Practice exercises

Try these exercises before reading the solutions.

## Beginner

**Exercise 1:** Find all sales transactions above the overall average amount.

**Exercise 2:** Find the smallest transaction using a scalar subquery.

**Exercise 3:** Find salespeople who have at least one transaction above 1500 using `EXISTS`.

**Exercise 4:** Calculate total revenue by salesperson using a derived table, then return totals above 3000.

**Exercise 5:** Use a CTE to calculate the average transaction amount and return transactions above it.

## Intermediate

**Exercise 6:** Find transactions above their salesperson's average transaction amount.

**Exercise 7:** Find products that have no sales using `NOT EXISTS`.

**Exercise 8:** Find transactions for products in the Electronics category using `IN`.

**Exercise 9:** Use `INNER JOIN` to show product name, category, and transaction amount.

**Exercise 10:** Calculate total revenue by product, then find products whose total exceeds average product revenue.

## Advanced

**Exercise 11:** Find the highest transaction amount in each product category, returning all tied transactions.

**Exercise 12:** Calculate product revenue and compare each product with the average revenue of products in its category.

**Exercise 13:** Use multiple CTEs to calculate revenue by region and identify regions above average regional revenue.

**Exercise 14:** Use `> ALL` to find sales that exceed every West-region transaction amount.

**Exercise 15:** Generate the numbers 1 through 20 with a recursive CTE.

---

# 23\. Exercise solutions

## Solution 1


```sql
SELECT *
FROM sales
WHERE amount > (
    SELECT AVG(amount)
    FROM sales
);
```

## Solution 2

```sql
SELECT *
FROM sales
WHERE amount = (
    SELECT MIN(amount)
    FROM sales
);
```

## Solution 3

```sql
SELECT DISTINCT s.salesperson
FROM sales AS s
WHERE EXISTS (
    SELECT 1
    FROM sales AS x
    WHERE x.salesperson = s.salesperson
      AND x.amount > 1500
);
```

## Solution 4

```sql
SELECT *
FROM (
    SELECT
        salesperson,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
) AS totals
WHERE total_revenue > 3000
ORDER BY total_revenue DESC;
```

## Solution 5

```sql
WITH average_sale AS (
    SELECT AVG(amount) AS avg_amount
    FROM sales
)
SELECT s.*
FROM sales AS s
CROSS JOIN average_sale AS a
WHERE s.amount > a.avg_amount;
```

## Solution 6

```sql
SELECT s.*
FROM sales AS s
WHERE s.amount > (
    SELECT AVG(x.amount)
    FROM sales AS x
    WHERE x.salesperson = s.salesperson
);
```

## Solution 7

```sql
SELECT p.product_id, p.product_name
FROM products AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM sales AS s
    WHERE s.product_id = p.product_id
);
```

## Solution 8

```sql
SELECT *
FROM sales
WHERE product_id IN (
    SELECT product_id
    FROM products
    WHERE category = 'Electronics'
);
```

## Solution 9

```sql
SELECT
    p.product_name,
    p.category,
    s.amount
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
ORDER BY s.sale_id;
```

## Solution 10

```sql
WITH product_totals AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(s.amount) AS total_revenue
    FROM products AS p
    INNER JOIN sales AS s
        ON p.product_id = s.product_id
    GROUP BY p.product_id, p.product_name
)
SELECT *
FROM product_totals
WHERE total_revenue > (
    SELECT AVG(total_revenue)
    FROM product_totals
)
ORDER BY total_revenue DESC;
```

## Solution 11

```sql
SELECT
    s.sale_id,
    p.product_name,
    p.category,
    s.amount
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id
WHERE s.amount = (
    SELECT MAX(s2.amount)
    FROM sales AS s2
    INNER JOIN products AS p2
        ON s2.product_id = p2.product_id
    WHERE p2.category = p.category
);
```

## Solution 12

```sql
WITH product_totals AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(s.amount) AS total_revenue
    FROM products AS p
    INNER JOIN sales AS s
        ON p.product_id = s.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT *
FROM product_totals AS pt
WHERE pt.total_revenue > (
    SELECT AVG(other.total_revenue)
    FROM product_totals AS other
    WHERE other.category = pt.category
)
ORDER BY pt.category, pt.total_revenue DESC;
```

## Solution 13

```sql
WITH region_totals AS (
    SELECT
        region,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY region
),
average_region AS (
    SELECT AVG(total_revenue) AS avg_revenue
    FROM region_totals
)
SELECT
    r.region,
    r.total_revenue
FROM region_totals AS r
CROSS JOIN average_region AS a
WHERE r.total_revenue > a.avg_revenue
ORDER BY r.total_revenue DESC;
```

## Solution 14

```sql
SELECT *
FROM sales
WHERE amount > ALL (
    SELECT amount
    FROM sales
    WHERE region = 'West'
);
```

## Solution 15

```sql
WITH RECURSIVE numbers(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1
    FROM numbers
    WHERE n < 20
)
SELECT n
FROM numbers
ORDER BY n;
```

---

# 24\. Cheat sheet

## Subquery patterns

**Scalar subquery**

```sql
SELECT *
FROM sales
WHERE amount > (
    SELECT AVG(amount)
    FROM sales
);
```

**Multi-row subquery**

```sql
SELECT *
FROM sales
WHERE product_id IN (
    SELECT product_id
    FROM products
    WHERE category = 'Electronics'
);
```

**Existence check**

```sql
SELECT p.*
FROM products AS p
WHERE EXISTS (
    SELECT 1
    FROM sales AS s
    WHERE s.product_id = p.product_id
);
```

**Anti-join**

```sql
SELECT p.*
FROM products AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM sales AS s
    WHERE s.product_id = p.product_id
);
```

**Correlated subquery**

```sql
SELECT s.*
FROM sales AS s
WHERE s.amount > (
    SELECT AVG(x.amount)
    FROM sales AS x
    WHERE x.salesperson = s.salesperson
);
```

**Derived table**

```sql
SELECT *
FROM (
    SELECT salesperson, 
           SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
) AS totals
WHERE total_revenue > 3000;
```

**CTE (common table expression)**

```sql
WITH totals AS (
    SELECT salesperson, 
           SUM(amount) AS total_revenue
    FROM sales
    GROUP BY salesperson
)
SELECT *
FROM totals
WHERE total_revenue > 3000;
```

**Join**

```sql
SELECT p.product_name, 
       s.amount
FROM sales AS s
INNER JOIN products AS p
    ON s.product_id = p.product_id;
```

## Final mental model

- **Scalar subquery:** Give me one value.
- **`IN`****:** Is this value in the returned set?
- **`EXISTS`****:** Does a matching row exist?
- **`NOT EXISTS`****:** Is there no matching row?
- **Correlated subquery:** Calculate something using the current outer row.
- **Derived table:** Treat a query result as a table.
- **`WITH`****:** Name the intermediate query steps.
- **Recursive CTE:** Repeatedly generate rows from prior results.
- **`INNER JOIN`****:** Combine matching rows from related tables.
- **Window function:** Calculate group-level metrics while retaining individual rows.

* The most important habit is to identify the shape 
of the inner result before writing the outer query. 
* Ask whether the inner query returns **one value**, 
  a **set of values**, a **table of rows**, or a result 
  that depends on the current outer row.

Once that becomes second nature, subqueries, joins, and CTEs become different tools for expressing the same underlying idea: transforming data in clear, logical steps.

---

## Suggested learning sequence

1. Run the setup SQL and inspect the sample data.
2. Practice scalar subqueries and `IN`.
3. Move on to `EXISTS` and correlated subqueries.
4. Learn derived tables and nested aggregation.
5. Practice `WITH` and multiple CTEs.
6. Create the two-table schema and practice joins.
7. Solve the exercises without looking at the solutions.
8. Use `EXPLAIN` to begin exploring DuckDB query plans.

**End of tutorial.**

