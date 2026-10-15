# `CASE` Expression — Step by Step <br> with DuckDB

* **Course:** OMIS 105 — Introduction to Database Management Systems
* **Author:** Dr. M. Parsian
* **Tech Stack:** DuckDB · SQL

---

## What You Will Learn

This tutorial assumes you have **never seen** a `CASE` expression.
We start very small and add one idea at a time.

| Part | Level | What you learn |
|------|-------|----------------|
| [Part 1](#part-1--basic) | Basic | What `CASE` is, `WHEN` / `THEN` / `ELSE` / `END`, more than two outcomes, "first match wins", the missing `ELSE`, the short (simple) form |
| [Part 2](#part-2--basic) | Basic+ | The wrong-order trap, `AND` / `IN` / `BETWEEN` inside `WHEN`, `NULL` values, `CASE` that returns numbers, `CASE` in `ORDER BY`, the "same type" rule |
| [Part 3](#part-3--intermediate) | Intermediate | `GROUP BY` a `CASE`, conditional counting and summing, `CASE` with `JOIN`, `CASE` on totals (customer segments), safe division, `CASE` in `UPDATE` |

Every query in this file was run in DuckDB, and every result you see
is the real output.

**How to follow along:** open the DuckDB shell (`duckdb`) or the
companion notebook `case_expression_notebook.py`, run the setup
script in Section 0, and then type each query yourself. Typing is
better than copying — your hands learn, too.

---

## 0. The Sample Data

A tiny online store keeps 2 tables.

| Table | Rows | Columns |
|-------|-----:|---------|
| `products` | 8 | `product_id`, `product_name`, `category`, `price`, `stock` |
| `orders` | 11 | `order_id`, `customer`, `product_id`, `quantity`, `status`, `order_date` |

`orders.product_id` points to `products.product_id`
(one product can appear in many orders).

Run this setup script once:

```sql
CREATE OR REPLACE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    product_name VARCHAR,
    category     VARCHAR,
    price        DECIMAL(8, 2),
    stock        INTEGER          -- NULL means "we don't know"
);

INSERT INTO products VALUES
    (1, 'Laptop',     'Electronics', 1200.00,    5),
    (2, 'Mouse',      'Electronics',   25.00,  150),
    (3, 'Desk Chair', 'Furniture',    180.00,    0),
    (4, 'Notebook',   'Office',         3.00,  500),
    (5, 'Monitor',    'Electronics',  300.00,   12),
    (6, 'Bookshelf',  'Furniture',     95.00,    8),
    (7, 'Pen Pack',   'Office',         6.00, NULL),
    (8, 'Headphones', 'Electronics',   80.00,   40);

CREATE OR REPLACE TABLE orders (
    order_id   INTEGER PRIMARY KEY,
    customer   VARCHAR,
    product_id INTEGER,
    quantity   INTEGER,
    status     VARCHAR,           -- shipped, pending, cancelled, returned
    order_date DATE
);

INSERT INTO orders VALUES
    (101, 'Alice', 1,  1, 'shipped',   DATE '2026-01-05'),
    (102, 'Bob',   2,  3, 'pending',   DATE '2026-01-07'),
    (103, 'Alice', 4, 10, 'shipped',   DATE '2026-02-02'),
    (104, 'Carol', 3,  2, 'cancelled', DATE '2026-02-10'),
    (105, 'Dan',   5,  2, 'shipped',   DATE '2026-02-15'),
    (106, 'Bob',   8,  1, 'returned',  DATE '2026-03-01'),
    (107, 'Carol', 6,  1, 'shipped',   DATE '2026-03-03'),
    (108, 'Dan',   7,  5, 'shipped',   DATE '2026-03-20'),
    (109, 'Alice', 2,  2, 'cancelled', DATE '2026-03-22'),
    (110, 'Eve',   1,  1, 'shipped',   DATE '2026-03-28'),
    (111, 'Eve',   2,  4, 'pending',   DATE '2026-04-02');
```

Let's look at both tables.

```sql
SELECT * FROM products;
```

| product_id | product_name | category | price | stock |
|---:|---|---|---:|---:|
| 1 | Laptop | Electronics | 1200.00 | 5 |
| 2 | Mouse | Electronics | 25.00 | 150 |
| 3 | Desk Chair | Furniture | 180.00 | 0 |
| 4 | Notebook | Office | 3.00 | 500 |
| 5 | Monitor | Electronics | 300.00 | 12 |
| 6 | Bookshelf | Furniture | 95.00 | 8 |
| 7 | Pen Pack | Office | 6.00 | NULL |
| 8 | Headphones | Electronics | 80.00 | 40 |

*8 rows*

```sql
SELECT * FROM orders;
```

| order_id | customer | product_id | quantity | status | order_date |
|---:|---|---:|---:|---|---|
| 101 | Alice | 1 | 1 | shipped | 2026-01-05 |
| 102 | Bob | 2 | 3 | pending | 2026-01-07 |
| 103 | Alice | 4 | 10 | shipped | 2026-02-02 |
| 104 | Carol | 3 | 2 | cancelled | 2026-02-10 |
| 105 | Dan | 5 | 2 | shipped | 2026-02-15 |
| 106 | Bob | 8 | 1 | returned | 2026-03-01 |
| 107 | Carol | 6 | 1 | shipped | 2026-03-03 |
| 108 | Dan | 7 | 5 | shipped | 2026-03-20 |
| 109 | Alice | 2 | 2 | cancelled | 2026-03-22 |
| 110 | Eve | 1 | 1 | shipped | 2026-03-28 |
| 111 | Eve | 2 | 4 | pending | 2026-04-02 |

*11 rows*

Notice two things we will use later:

- The Desk Chair has `stock = 0` (sold out).
- The Pen Pack has `stock = NULL` (nobody counted it yet).

---

## What Is a `CASE` Expression?

A `CASE` expression lets SQL **make a decision for each row**.

You already know this idea from everyday life:

> **If** the price is under $100, **then** call it "Cheap".
> **Otherwise**, call it "Expensive".

In Python you would write `if ... elif ... else`.
In SQL you write `CASE ... WHEN ... THEN ... ELSE ... END`.

```sql
CASE
    WHEN <condition 1> THEN <result 1>
    WHEN <condition 2> THEN <result 2>
    ...
    ELSE <default result>
END
```

| Keyword | Meaning |
|---------|---------|
| `CASE`  | "I am starting a decision." |
| `WHEN`  | "Test this condition." (a yes/no question) |
| `THEN`  | "If the answer is yes, give back this value." |
| `ELSE`  | "If no `WHEN` said yes, give back this value." (optional) |
| `END`   | "The decision is finished." (required!) |

Two important facts:

1. `CASE` is an **expression**. It produces **one value** for each row —
   just like `price * 2` or `UPPER(product_name)` do. So you can put
   it anywhere a value can go: in `SELECT`, `ORDER BY`, `GROUP BY`,
   inside `SUM()`, and more.
2. `CASE` does **not** change your table. It only changes what you
   see in the result.

---

## Part 1 — Basic

### B1. Your first `CASE`: two outcomes

**Question:** Label each product as `'Cheap'` (under $100) or
`'Expensive'`.

```sql
SELECT product_name,
       price,
       CASE
           WHEN price < 100 THEN 'Cheap'
           ELSE 'Expensive'
       END AS price_label
FROM products;
```

| product_name | price | price_label |
|---|---:|---|
| Laptop | 1200.00 | Expensive |
| Mouse | 25.00 | Cheap |
| Desk Chair | 180.00 | Expensive |
| Notebook | 3.00 | Cheap |
| Monitor | 300.00 | Expensive |
| Bookshelf | 95.00 | Cheap |
| Pen Pack | 6.00 | Cheap |
| Headphones | 80.00 | Cheap |

*8 rows*

**How to read it:** for each row, DuckDB asks "Is `price < 100`?"
If yes, the answer is `'Cheap'`. If no, the `ELSE` gives
`'Expensive'`.

`AS price_label` gives the new column a name. Without it, the column
header would be the whole `CASE ... END` text — hard to read.

---

### B2. More than two outcomes

**Question:** Put each product into a price tier:

- under $20 → `'Budget'`
- under $200 → `'Mid-range'`
- everything else → `'Premium'`

Just add more `WHEN` lines.

```sql
SELECT product_name,
       price,
       CASE
           WHEN price < 20  THEN 'Budget'
           WHEN price < 200 THEN 'Mid-range'
           ELSE 'Premium'
       END AS price_tier
FROM products;
```

| product_name | price | price_tier |
|---|---:|---|
| Laptop | 1200.00 | Premium |
| Mouse | 25.00 | Mid-range |
| Desk Chair | 180.00 | Mid-range |
| Notebook | 3.00 | Budget |
| Monitor | 300.00 | Premium |
| Bookshelf | 95.00 | Mid-range |
| Pen Pack | 6.00 | Budget |
| Headphones | 80.00 | Mid-range |

*8 rows*

---

### B3. How `CASE` thinks: the first match wins

`CASE` checks the `WHEN` lines **from top to bottom**. As soon as one
condition is true, it returns that `THEN` value and **stops**. The
lines below are never checked for that row.

Let's follow the Notebook (price = 3.00) and the Monitor (price = 300.00)
through the query in B2:

| Row | `price < 20`? | `price < 200`? | `ELSE` | Result |
|-----|---------------|----------------|--------|--------|
| Notebook (3.00) | **yes → stop** | (not checked) | (not checked) | `Budget` |
| Monitor (300.00) | no | no | **used** | `Premium` |

The Notebook's price is also less than 200 — but that does not
matter. `CASE` already stopped at the first `WHEN`.
This is why we did not need to write `price >= 20 AND price < 200`
in the second line. Keep this rule in mind; it comes back in P1.

---

### B4. What if you forget the `ELSE`?

`ELSE` is optional. But if no `WHEN` matches and there is no `ELSE`,
the result is **`NULL`** (empty, "unknown").

```sql
SELECT product_name,
       category,
       CASE
           WHEN category = 'Electronics' THEN 'Tech'
           WHEN category = 'Furniture'   THEN 'Home'
       END AS dept_label          -- no ELSE!
FROM products;
```

| product_name | category | dept_label |
|---|---|---|
| Laptop | Electronics | Tech |
| Mouse | Electronics | Tech |
| Desk Chair | Furniture | Home |
| Notebook | Office | NULL |
| Monitor | Electronics | Tech |
| Bookshelf | Furniture | Home |
| Pen Pack | Office | NULL |
| Headphones | Electronics | Tech |

*8 rows*

The two `Office` products got `NULL`, because no `WHEN` matched them.

**Good habit:** always write an `ELSE`, even if it is only
`ELSE 'Other'`. Then a missing case is easy to see.

---

### B5. The short form: "simple" `CASE`

When every `WHEN` compares **the same column** with `=`, you can use a
shorter form. Write the column **once**, right after `CASE`:

```sql
SELECT product_name,
       category,
       CASE category
           WHEN 'Electronics' THEN 'Tech'
           WHEN 'Furniture'   THEN 'Home'
           ELSE 'Other'
       END AS dept_label
FROM products;
```

| product_name | category | dept_label |
|---|---|---|
| Laptop | Electronics | Tech |
| Mouse | Electronics | Tech |
| Desk Chair | Furniture | Home |
| Notebook | Office | Other |
| Monitor | Electronics | Tech |
| Bookshelf | Furniture | Home |
| Pen Pack | Office | Other |
| Headphones | Electronics | Tech |

*8 rows*

The two forms side by side:

| Searched `CASE` (long form) | Simple `CASE` (short form) |
|-----------------------------|----------------------------|
| `CASE WHEN category = 'Office' THEN ...` | `CASE category WHEN 'Office' THEN ...` |
| Any condition: `<`, `>`, `AND`, `OR`, `IN`, `LIKE`, `IS NULL`, ... | Only "equals" (`=`) on one column |
| Works for everything | Shorter, easy to read for code → label lookups |

**Tip:** when in doubt, use the long (searched) form. It can do
everything the short form can do, and more.

---

## Part 2 — Basic+

### P1. The wrong-order trap

Remember B3: the first true `WHEN` wins. So **order matters**.
Here we put the conditions in the wrong order — the biggest
range first:

```sql
SELECT product_name,
       price,
       CASE
           WHEN price < 200 THEN 'Mid-range'   -- too wide, checked first!
           WHEN price < 20  THEN 'Budget'      -- never reached
           ELSE 'Premium'
       END AS price_tier
FROM products;
```

| product_name | price | price_tier |
|---|---:|---|
| Laptop | 1200.00 | Premium |
| Mouse | 25.00 | Mid-range |
| Desk Chair | 180.00 | Mid-range |
| Notebook | 3.00 | Mid-range |
| Monitor | 300.00 | Premium |
| Bookshelf | 95.00 | Mid-range |
| Pen Pack | 6.00 | Mid-range |
| Headphones | 80.00 | Mid-range |

*8 rows*

There is **no error** — but the answer is **wrong**. The Notebook ($3)
and the Pen Pack ($6) should be `'Budget'`. They are caught by
`price < 200` first, so the `'Budget'` line is never reached.

**Rule:** when the ranges overlap, put the **narrowest** condition
first (or write ranges that do not overlap, like `BETWEEN 20 AND 199.99`).

---

### P2. Richer conditions: `AND`, `IN`, `BETWEEN`

A `WHEN` can hold **any** condition you could write in a `WHERE`
clause.

**Question:** Give each order a short note for the warehouse team.

```sql
SELECT order_id,
       customer,
       quantity,
       status,
       CASE
           WHEN status IN ('cancelled', 'returned')       THEN 'No action'
           WHEN status = 'pending' AND quantity >= 3      THEN 'Big order - pack today'
           WHEN status = 'pending'                        THEN 'Pack this week'
           WHEN order_date BETWEEN DATE '2026-03-01'
                               AND DATE '2026-03-31'      THEN 'Shipped in March'
           ELSE 'Shipped earlier'
       END AS warehouse_note
FROM orders
ORDER BY order_id;
```

| order_id | customer | quantity | status | warehouse_note |
|---:|---|---:|---|---|
| 101 | Alice | 1 | shipped | Shipped earlier |
| 102 | Bob | 3 | pending | Big order - pack today |
| 103 | Alice | 10 | shipped | Shipped earlier |
| 104 | Carol | 2 | cancelled | No action |
| 105 | Dan | 2 | shipped | Shipped earlier |
| 106 | Bob | 1 | returned | No action |
| 107 | Carol | 1 | shipped | Shipped in March |
| 108 | Dan | 5 | shipped | Shipped in March |
| 109 | Alice | 2 | cancelled | No action |
| 110 | Eve | 1 | shipped | Shipped in March |
| 111 | Eve | 4 | pending | Big order - pack today |

*11 rows*

Read the `WHEN` lines as plain English:

- `status IN ('cancelled', 'returned')` — the status is one of these two.
  (It is a short way to write `status = 'cancelled' OR status = 'returned'`.)
- `status = 'pending' AND quantity >= 3` — **both** must be true.
- `order_date BETWEEN ... AND ...` — the date is in March (both ends included).

Notice line 2 comes **before** line 3. A big pending order matches
both, and we want the more specific message (see P1).

---

### P3. `CASE` and `NULL` values

The Pen Pack's stock is `NULL` (unknown). Let's build a stock report.

```sql
SELECT product_name,
       stock,
       CASE
           WHEN stock IS NULL THEN 'Unknown - please count'
           WHEN stock = 0     THEN 'Sold out'
           WHEN stock < 10    THEN 'Low - reorder'
           ELSE 'In stock'
       END AS stock_status
FROM products;
```

| product_name | stock | stock_status |
|---|---:|---|
| Laptop | 5 | Low - reorder |
| Mouse | 150 | In stock |
| Desk Chair | 0 | Sold out |
| Notebook | 500 | In stock |
| Monitor | 12 | In stock |
| Bookshelf | 8 | Low - reorder |
| Pen Pack | NULL | Unknown - please count |
| Headphones | 40 | In stock |

*8 rows*

Two things to learn here:

**1. Test for `NULL` with `IS NULL`, and test it first.**
`NULL < 10` is not true and not false — it is *unknown*. A `WHEN`
only fires when its condition is **true**, so a `NULL` row would
skip every `WHEN` and fall into the `ELSE` (`'In stock'` — wrong!).

**2. The short form cannot find `NULL`.**
`CASE stock WHEN NULL THEN ...` looks right, but it means
`stock = NULL`, which is never true — not even when `stock` *is*
`NULL`:

```sql
SELECT product_name,
       stock,
       CASE stock
           WHEN NULL THEN 'Unknown'      -- this NEVER matches
           WHEN 0    THEN 'Sold out'
           ELSE 'Has a number'
       END AS wrong_check
FROM products
WHERE product_id IN (3, 7);
```

| product_name | stock | wrong_check |
|---|---:|---|
| Desk Chair | 0 | Sold out |
| Pen Pack | NULL | Has a number |

*2 rows*

The Pen Pack should say `'Unknown'`, but it says `'Has a number'`.
For `NULL`, always use the long form with `IS NULL`.

---

### P4. `CASE` can return numbers, too

So far `CASE` returned text labels. It can also return numbers — and
then you can do math with them.

**Question:** This week there is a sale: Electronics 10% off,
Furniture 20% off, everything else no discount. Show the sale price.

```sql
SELECT product_name,
       category,
       price,
       CASE category
           WHEN 'Electronics' THEN 0.10
           WHEN 'Furniture'   THEN 0.20
           ELSE 0.00
       END AS discount,
       ROUND(price * (1 - CASE category
                              WHEN 'Electronics' THEN 0.10
                              WHEN 'Furniture'   THEN 0.20
                              ELSE 0.00
                          END), 2) AS sale_price
FROM products;
```

| product_name | category | price | discount | sale_price |
|---|---|---:|---:|---:|
| Laptop | Electronics | 1200.00 | 0.10 | 1080.00 |
| Mouse | Electronics | 25.00 | 0.10 | 22.50 |
| Desk Chair | Furniture | 180.00 | 0.20 | 144.00 |
| Notebook | Office | 3.00 | 0.00 | 3.00 |
| Monitor | Electronics | 300.00 | 0.10 | 270.00 |
| Bookshelf | Furniture | 95.00 | 0.20 | 76.00 |
| Pen Pack | Office | 6.00 | 0.00 | 6.00 |
| Headphones | Electronics | 80.00 | 0.10 | 72.00 |

*8 rows*

The `CASE` inside `sale_price` gives back one number per row, and
`price * (1 - that number)` uses it (`ROUND(..., 2)` keeps 2 decimals). A `CASE` can sit **inside**
a bigger calculation — it is just a value.

---

### P5. `CASE` in `ORDER BY`: a custom sort order

`ORDER BY status` would sort alphabetically:
cancelled, pending, returned, shipped. But the team wants to see
**pending first** (they need action), then shipped, then the rest.

The trick: turn each status into a **sort number**.

```sql
SELECT order_id,
       customer,
       status
FROM orders
ORDER BY CASE status
             WHEN 'pending' THEN 1
             WHEN 'shipped' THEN 2
             ELSE 3
         END,
         order_id;
```

| order_id | customer | status |
|---:|---|---|
| 102 | Bob | pending |
| 111 | Eve | pending |
| 101 | Alice | shipped |
| 103 | Alice | shipped |
| 105 | Dan | shipped |
| 107 | Carol | shipped |
| 108 | Dan | shipped |
| 110 | Eve | shipped |
| 104 | Carol | cancelled |
| 106 | Bob | returned |
| 109 | Alice | cancelled |

*11 rows*

The `CASE` is not shown in the result. It is only used to decide the
order. The second sort key, `order_id`, breaks ties inside each group.

---

### P6. The "same type" rule

Every `THEN` and the `ELSE` must give back the **same kind of value**:
all text, or all numbers, or all dates. A column cannot be text in
one row and a number in the next.

Here we mix text (`'Sold out'`) with a number (`stock`):

```sql
SELECT product_name,
       CASE
           WHEN stock = 0 THEN 'Sold out'
           ELSE stock
       END AS stock_info
FROM products;
```

DuckDB stops with an error:

```text
Conversion Error: Could not convert string 'Sold out' to INT32
```

DuckDB decided the column is a number (`INT32`), then found the
text `'Sold out'` and could not turn it into a number.

**Fix:** make every branch the same type. Here, turn the number into
text with `CAST(... AS VARCHAR)`:

```sql
SELECT product_name,
       CASE
           WHEN stock = 0 THEN 'Sold out'
           ELSE CAST(stock AS VARCHAR)
       END AS stock_info
FROM products;
```

| product_name | stock_info |
|---|---|
| Laptop | 5 |
| Mouse | 150 |
| Desk Chair | Sold out |
| Notebook | 500 |
| Monitor | 12 |
| Bookshelf | 8 |
| Pen Pack | NULL |
| Headphones | 40 |

*8 rows*

(The Pen Pack shows `NULL`: `stock = 0` is unknown for `NULL`, so the
`ELSE` runs, and `CAST(NULL AS VARCHAR)` is still `NULL`.)

---

## Part 3 — Intermediate

### I1. `GROUP BY` a `CASE`

Because `CASE` makes a new value for each row, you can **group by**
that value.

**Question:** How many products are in each price tier, and what is
their average price?

```sql
SELECT CASE
           WHEN price < 20  THEN 'Budget'
           WHEN price < 200 THEN 'Mid-range'
           ELSE 'Premium'
       END                AS price_tier,
       COUNT(*)           AS num_products,
       ROUND(AVG(price), 2) AS avg_price,
       STRING_AGG(product_name, ', ' ORDER BY product_name) AS products
FROM products
GROUP BY price_tier
ORDER BY avg_price;
```

| price_tier | num_products | avg_price | products |
|---|---:|---:|---|
| Budget | 2 | 4.5 | Notebook, Pen Pack |
| Mid-range | 4 | 95.0 | Bookshelf, Desk Chair, Headphones, Mouse |
| Premium | 2 | 750.0 | Laptop, Monitor |

*3 rows*

The `products` column is an "x-ray": `STRING_AGG` lists the rows
inside each group, so you can check the counts with your own eyes.

**DuckDB note:** `GROUP BY price_tier` uses the alias from `SELECT`.
DuckDB allows this. Some other databases do not — there you must
repeat the whole `CASE` in the `GROUP BY`.

---

### I2. Conditional counting: `SUM(CASE ...)`

This is the most useful `CASE` pattern in business reports.

**Question:** For each customer, how many orders were shipped,
pending, and cancelled/returned — **side by side in one row**?

The idea: make a column that is `1` when the row matches and `0` when
it does not. Then `SUM` adds up the 1s — that is a count!

```sql
SELECT customer,
       COUNT(*) AS total_orders,
       SUM(CASE WHEN status = 'shipped' THEN 1 ELSE 0 END) AS shipped,
       SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending,
       SUM(CASE WHEN status IN ('cancelled', 'returned')
                THEN 1 ELSE 0 END)                         AS cancelled_or_returned
FROM orders
GROUP BY customer
ORDER BY customer;
```

| customer | total_orders | shipped | pending | cancelled_or_returned |
|---|---:|---:|---:|---:|
| Alice | 3 | 2 | 0 | 1 |
| Bob | 2 | 0 | 1 | 1 |
| Carol | 2 | 1 | 0 | 1 |
| Dan | 2 | 2 | 0 | 0 |
| Eve | 2 | 1 | 1 | 0 |

*5 rows*

Let's x-ray Alice (orders 101, 103, 109) for the `shipped` column:

| order_id | status | `CASE WHEN status = 'shipped' THEN 1 ELSE 0 END` |
|---------:|--------|:--:|
| 101 | shipped | 1 |
| 103 | shipped | 1 |
| 109 | cancelled | 0 |
| | **SUM** | **2** |

**Same result, two other ways** (good to recognize when you read
other people's SQL):

- `COUNT(CASE WHEN status = 'shipped' THEN 1 END)` — no `ELSE`, so
  non-matching rows become `NULL`, and `COUNT` skips `NULL`s.
- `COUNT(*) FILTER (WHERE status = 'shipped')` — DuckDB's `FILTER`
  clause, a shortcut for exactly this pattern.

---

### I3. Conditional sums with a `JOIN`

`SUM(CASE ...)` can add up **amounts**, not just 1s.

**Question:** For each product category, how much money did we
**earn** (shipped orders) and how much did we **lose** (cancelled or
returned orders)? Amount = `quantity * price`.

`orders` has the quantity; `products` has the price and category. So
we `JOIN` them first.

```sql
SELECT p.category,
       SUM(CASE WHEN o.status = 'shipped'
                THEN o.quantity * p.price ELSE 0 END) AS earned,
       SUM(CASE WHEN o.status IN ('cancelled', 'returned')
                THEN o.quantity * p.price ELSE 0 END) AS lost,
       SUM(CASE WHEN o.status = 'pending'
                THEN o.quantity * p.price ELSE 0 END) AS waiting
FROM orders AS o
JOIN products AS p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY earned DESC;
```

| category | earned | lost | waiting |
|---|---:|---:|---:|
| Electronics | 3000.00 | 130.00 | 175.00 |
| Furniture | 95.00 | 360.00 | 0.00 |
| Office | 60.00 | 0.00 | 0.00 |

*3 rows*

One query, one row per category, three different money columns.
Without `CASE`, you would need three separate queries.

---

### I4. `CASE` on totals: customer segments

`CASE` can also test the result of an aggregate like `SUM(...)`.

**Question:** Put each customer into a loyalty segment based on how
much they spent on **shipped** orders:

- $1,000 or more → `'Gold'`
- $500 or more → `'Silver'`
- more than $0 → `'Bronze'`
- $0 → `'No purchases yet'`

```sql
SELECT o.customer,
       SUM(CASE WHEN o.status = 'shipped'
                THEN o.quantity * p.price ELSE 0 END) AS total_spent,
       CASE
           WHEN SUM(CASE WHEN o.status = 'shipped'
                         THEN o.quantity * p.price ELSE 0 END) >= 1000 THEN 'Gold'
           WHEN SUM(CASE WHEN o.status = 'shipped'
                         THEN o.quantity * p.price ELSE 0 END) >= 500  THEN 'Silver'
           WHEN SUM(CASE WHEN o.status = 'shipped'
                         THEN o.quantity * p.price ELSE 0 END) > 0     THEN 'Bronze'
           ELSE 'No purchases yet'
       END AS segment
FROM orders AS o
JOIN products AS p ON o.product_id = p.product_id
GROUP BY o.customer
ORDER BY total_spent DESC;
```

| customer | total_spent | segment |
|---|---:|---|
| Alice | 1230.00 | Gold |
| Eve | 1200.00 | Gold |
| Dan | 630.00 | Silver |
| Carol | 95.00 | Bronze |
| Bob | 0.00 | No purchases yet |

*5 rows*

That works, but we typed the same `SUM(CASE ...)` four times. A **CTE**
(`WITH`) computes it once and gives it a name. Then the outer `CASE`
is short and easy to read:

```sql
WITH spending AS (
    SELECT o.customer,
           SUM(CASE WHEN o.status = 'shipped'
                    THEN o.quantity * p.price ELSE 0 END) AS total_spent
    FROM orders AS o
    JOIN products AS p ON o.product_id = p.product_id
    GROUP BY o.customer
)
SELECT customer,
       total_spent,
       CASE
           WHEN total_spent >= 1000 THEN 'Gold'
           WHEN total_spent >= 500  THEN 'Silver'
           WHEN total_spent > 0     THEN 'Bronze'
           ELSE 'No purchases yet'
       END AS segment
FROM spending
ORDER BY total_spent DESC;
```

| customer | total_spent | segment |
|---|---:|---|
| Alice | 1230.00 | Gold |
| Eve | 1200.00 | Gold |
| Dan | 630.00 | Silver |
| Carol | 95.00 | Bronze |
| Bob | 0.00 | No purchases yet |

*5 rows*

Same result, much cleaner. (CTEs are covered fully in Week 7 and Week 9.)

---

### I5. Safe division: avoid dividing by zero

**Question:** For each customer, what percent of their ordered
**units** were cancelled or returned?

A percent is `part / total`. If `total` were 0, the division would
fail or give a meaningless value. A `CASE` can guard against it:
"if the total is 0, give `NULL`; otherwise divide."

```sql
WITH units AS (
    SELECT customer,
           SUM(quantity) AS total_units,
           SUM(CASE WHEN status IN ('cancelled', 'returned')
                    THEN quantity ELSE 0 END) AS bad_units
    FROM orders
    GROUP BY customer
)
SELECT customer,
       total_units,
       bad_units,
       CASE
           WHEN total_units = 0 THEN NULL
           ELSE ROUND(100.0 * bad_units / total_units, 1)
       END AS pct_bad
FROM units
ORDER BY pct_bad DESC, customer;
```

| customer | total_units | bad_units | pct_bad |
|---|---:|---:|---:|
| Carol | 3 | 2 | 66.7 |
| Bob | 4 | 1 | 25.0 |
| Alice | 13 | 2 | 15.4 |
| Dan | 7 | 0 | 0.0 |
| Eve | 5 | 0 | 0.0 |

*5 rows*

In our data no customer has 0 units, so the guard never fires — but
in real data it will, someday. The `CASE` makes the query safe
**before** that day comes.

---

### I6. `CASE` in `UPDATE`: change many rows in one statement

Until now, `CASE` only changed what we **see**. Inside an `UPDATE`,
it changes the **stored data**.

**Question:** Next month prices change: Electronics +5%,
Office +10%, Furniture stays the same.

To keep our original `products` table safe, we first make a copy and
update the copy.

```sql
CREATE OR REPLACE TABLE new_prices AS
SELECT product_id, product_name, category, price AS old_price, price AS new_price
FROM products;

UPDATE new_prices
SET new_price = CASE category
                    WHEN 'Electronics' THEN ROUND(new_price * 1.05, 2)
                    WHEN 'Office'      THEN ROUND(new_price * 1.10, 2)
                    ELSE new_price            -- keep the same price
                END;

SELECT * FROM new_prices ORDER BY category, product_id;
```

| product_id | product_name | category | old_price | new_price |
|---:|---|---|---:|---:|
| 1 | Laptop | Electronics | 1200.00 | 1260.00 |
| 2 | Mouse | Electronics | 25.00 | 26.25 |
| 5 | Monitor | Electronics | 300.00 | 315.00 |
| 8 | Headphones | Electronics | 80.00 | 84.00 |
| 3 | Desk Chair | Furniture | 180.00 | 180.00 |
| 6 | Bookshelf | Furniture | 95.00 | 95.00 |
| 4 | Notebook | Office | 3.00 | 3.30 |
| 7 | Pen Pack | Office | 6.00 | 6.60 |

*8 rows*

One `UPDATE` changed three categories in three different ways.

**Why `ELSE new_price` matters here:** without it, Furniture would
get `NULL` (see B4) — and the update would **erase** those prices.
In an `UPDATE`, a missing `ELSE` can destroy data.

---

## Common Mistakes

| Mistake | What happens | Fix |
|---------|--------------|-----|
| Forgetting `END` | Syntax error | Every `CASE` needs its own `END` |
| No `ELSE` | Unmatched rows get `NULL` (B4) — in an `UPDATE`, data is erased (I6) | Always write an `ELSE` |
| Wide condition first | No error, but wrong labels (P1) | Narrowest condition first |
| `CASE col WHEN NULL` | Never matches (P3) | Use `WHEN col IS NULL` (long form) |
| `NULL` not tested first | `NULL` rows fall into `ELSE` (P3) | Put `WHEN col IS NULL` at the top |
| Mixing text and numbers | `Conversion Error` (P6) | Same type in every branch (`CAST`) |
| No `AS` alias | Ugly column name | `END AS my_label` |

---

## Cheat Sheet

```sql
-- Searched CASE (long form): any condition
CASE
    WHEN price < 20  THEN 'Budget'
    WHEN price < 200 THEN 'Mid-range'
    ELSE 'Premium'
END AS price_tier

-- Simple CASE (short form): one column, "equals" only
CASE status
    WHEN 'pending' THEN 1
    WHEN 'shipped' THEN 2
    ELSE 3
END

-- Where CASE can go
SELECT   CASE ... END AS label         -- a new column
ORDER BY CASE ... END                  -- a custom sort order
GROUP BY label                         -- buckets (DuckDB allows the alias)
SUM(CASE WHEN ... THEN 1 ELSE 0 END)   -- conditional count
SUM(CASE WHEN ... THEN amount ELSE 0 END)  -- conditional sum
UPDATE t SET col = CASE ... END        -- different change per row
```

**Rules to remember**

1. `WHEN` lines are checked top to bottom. The **first** true one wins.
2. No match and no `ELSE` → `NULL`.
3. Every branch must return the **same type**.
4. Test `NULL` with `IS NULL`, and put that test first.

---

## Practice Exercises

Try each one before you open the solution.

<details>
<summary><b>Exercise 1.</b> Label each order by quantity: 1 → <code>'Single'</code>, 2 to 4 → <code>'Few'</code>, 5 or more → <code>'Bulk'</code>.</summary>

```sql
SELECT order_id,
       quantity,
       CASE
           WHEN quantity = 1 THEN 'Single'
           WHEN quantity <= 4 THEN 'Few'
           ELSE 'Bulk'
       END AS size_label
FROM orders
ORDER BY order_id;
```

| order_id | quantity | size_label |
|---:|---:|---|
| 101 | 1 | Single |
| 102 | 3 | Few |
| 103 | 10 | Bulk |
| 104 | 2 | Few |
| 105 | 2 | Few |
| 106 | 1 | Single |
| 107 | 1 | Single |
| 108 | 5 | Bulk |
| 109 | 2 | Few |
| 110 | 1 | Single |
| 111 | 4 | Few |

*11 rows*

</details>

<details>
<summary><b>Exercise 2.</b> For each category, count products under $100 and products $100 or more, in one row per category.</summary>

```sql
SELECT category,
       SUM(CASE WHEN price < 100  THEN 1 ELSE 0 END) AS under_100,
       SUM(CASE WHEN price >= 100 THEN 1 ELSE 0 END) AS from_100_up
FROM products
GROUP BY category
ORDER BY category;
```

| category | under_100 | from_100_up |
|---|---:|---:|
| Electronics | 2 | 2 |
| Furniture | 1 | 1 |
| Office | 2 | 0 |

*3 rows*

</details>

<details>
<summary><b>Exercise 3.</b> List all products with sold-out items first, then unknown stock, then everything else. Inside each group, sort by name.</summary>

```sql
SELECT product_name, stock
FROM products
ORDER BY CASE
             WHEN stock = 0     THEN 1
             WHEN stock IS NULL THEN 2
             ELSE 3
         END,
         product_name;
```

| product_name | stock |
|---|---:|
| Desk Chair | 0 |
| Pen Pack | NULL |
| Bookshelf | 8 |
| Headphones | 40 |
| Laptop | 5 |
| Monitor | 12 |
| Mouse | 150 |
| Notebook | 500 |

*8 rows*

</details>

<details>
<summary><b>Exercise 4.</b> Add a column <code>is_final</code>: <code>'Yes'</code> if the order is shipped, cancelled, or returned; <code>'No'</code> if it is pending.</summary>

```sql
SELECT order_id,
       status,
       CASE
           WHEN status IN ('shipped', 'cancelled', 'returned') THEN 'Yes'
           ELSE 'No'
       END AS is_final
FROM orders
ORDER BY order_id;
```

| order_id | status | is_final |
|---:|---|---|
| 101 | shipped | Yes |
| 102 | pending | No |
| 103 | shipped | Yes |
| 104 | cancelled | Yes |
| 105 | shipped | Yes |
| 106 | returned | Yes |
| 107 | shipped | Yes |
| 108 | shipped | Yes |
| 109 | cancelled | Yes |
| 110 | shipped | Yes |
| 111 | pending | No |

*11 rows*

</details>

<details>
<summary><b>Exercise 5.</b> For each month of 2026, show the number of orders and the number of shipped orders. (Hint: <code>MONTH(order_date)</code>.)</summary>

```sql
SELECT MONTH(order_date) AS order_month,
       COUNT(*) AS orders,
       SUM(CASE WHEN status = 'shipped' THEN 1 ELSE 0 END) AS shipped
FROM orders
GROUP BY order_month
ORDER BY order_month;
```

| order_month | orders | shipped |
|---:|---:|---:|
| 1 | 2 | 1 |
| 2 | 3 | 2 |
| 3 | 5 | 3 |
| 4 | 1 | 0 |

*4 rows*

</details>

---

## Summary

- `CASE` is SQL's **if-then-else**. It gives back **one value per row**.
- Write it as `CASE WHEN ... THEN ... ELSE ... END AS name`.
- The **first** true `WHEN` wins, so order matters.
- Without `ELSE`, unmatched rows become `NULL`.
- Use the long form for ranges and `NULL` checks; the short form for
  simple "equals" lookups.
- `CASE` works in `SELECT`, `ORDER BY`, `GROUP BY`, inside `SUM` and
  `COUNT`, and in `UPDATE`.
- `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` is the classic way to count
  several things side by side in one report.

**Next step:** open `case_expression_notebook.py` in Marimo and run
every query yourself. Then change a number or a condition and watch
the result change.

---
*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
