# CASE Expressions <br> with DuckDB

Welcome to this beginner-friendly guide on SQL `CASE` expressions! If you have ever wanted to write "if-then-else" logic directly inside your database queries, the `CASE` expression is your go-to tool. 

By the end of this tutorial, you will understand how `CASE` works, how to use it for simple lookups, and how to apply it to more advanced grouping and conditional aggregation. We will be using **DuckDB**, a high-performance analytical database, to run our queries.

---

## 1. Setting Up Our Environment and Data

To follow along, let's create a simple database schema. Imagine we manage a small online bookstore. We have a single table called `books` with 10 records tracking book titles, genres, prices, and stock quantities.

Run the following SQL commands in your DuckDB console or script:

```sql
-- Create the books table
CREATE TABLE books (
    book_id INTEGER,
    title VARCHAR,
    genre VARCHAR,
    price DECIMAL(5,2),
    stock_quantity INTEGER
);

-- Insert 10 sample records
INSERT INTO books VALUES
(1, 'The Database Journey', 'Tech', 45.00, 12),
(2, 'SQL for Beginners', 'Tech', 29.99, 4),
(3, 'Advanced DuckDB', 'Tech', 55.50, 2),
(4, 'The Mystery of the Missing Byte', 'Mystery', 15.00, 25),
(5, 'Midnight Cipher', 'Mystery', 18.50, 8),
(6, 'Whispers in the Code', 'Mystery', 22.00, 0),
(7, 'Galactic Empire', 'Sci-Fi', 12.99, 30),
(8, 'Starlight Odyssey', 'Sci-Fi', 14.50, 15),
(9, 'Cooking Made Easy', 'Lifestyle', 24.99, 10),
(10, 'Bake Your Own Bread', 'Lifestyle', 19.99, 5);
```

Let's verify our data by viewing all 10 records:

```sql
SELECT * FROM books;
```

---

## 2. What is a CASE Expression?

Think of a `CASE` expression as a programmatic `if-then-else` statement inside your SQL query. It evaluates a list of conditions and returns one of multiple possible result expressions.

There are two main flavors of `CASE` expressions in SQL:

1. **Simple CASE:** Compares an expression to a set of simple values.
2. **Searched CASE:** Evaluates a series of boolean conditions.

---

## 3. Simple Examples: Basic Conditional Logic

Let's start with a **Searched CASE** expression. Suppose we want to categorize our books based on their price into three simple tiers: `Budget`, `Standard`, and `Premium`.

### Example 3.1: Categorizing by Price

```sql
SELECT 
    title,
    price,
    CASE 
        WHEN price < 20.00 THEN 'Budget'
        WHEN price BETWEEN 20.00 AND 40.00 THEN 'Standard'
        ELSE 'Premium'
    END AS price_category
FROM books;
```

**How it works:**

* DuckDB looks at each row's `price`.
* It checks the `WHEN` conditions from top to bottom. The moment a condition evaluates to true, it returns the corresponding `THEN` value and stops looking further down that case block.
* If none of the `WHEN` conditions match, it falls back to the `ELSE` clause (returning `'Premium'`).
* `END AS price_category` gives a nice custom header to our new calculated column.

---

## 4. Intermediate Examples: Advanced Applications

Now that you know how to write a basic conditional column, let's look at more intermediate use cases.

### Example 4.1: Handling Inventory and Stock Statuses

Suppose we want to flag inventory urgency for store operations:

* If stock is `0`, label it as `'Out of Stock'`.
* If stock is less than `6`, label it as `'Low Stock'`.
* Otherwise, label it as `'In Stock'`.

```sql
SELECT 
    title,
    stock_quantity,
    CASE 
        WHEN stock_quantity = 0 THEN 'Out of Stock'
        WHEN stock_quantity < 6 THEN 'Low Stock'
        ELSE 'In Stock'
    END AS stock_status
FROM books;
```

### Example 4.2: Conditional Aggregation (Counting with CASE)

One of the most powerful uses of `CASE` expressions is inside aggregate functions like `SUM` or `COUNT`. This allows you to pivot or count specific subsets of data in a single query without complex `JOIN` statements or subqueries.

Suppose we want to count how many books are **Tech** books versus **Non-Tech** books in a single summary row:

```sql
SELECT 
    COUNT(*) AS total_books,
    SUM(CASE WHEN genre = 'Tech' THEN 1 ELSE 0 END) 
       AS tech_book_count,
    SUM(CASE WHEN genre != 'Tech' THEN 1 ELSE 0 END) 
       AS non_tech_book_count
FROM books;
```

**How this works:**

* Inside the `SUM()`, the `CASE` expression evaluates to `1` when the condition is met and `0` otherwise.
* Summing those 1s and 0s effectively gives us a conditional count!

### Example 4.3: Dynamic Sorting (ORDER BY with CASE)

You can also use `CASE` inside an `ORDER BY` clause to create custom sort orders. For example, suppose we want to sort our books by stock status urgency first (`Out of Stock` $\rightarrow$ `Low Stock` $\rightarrow$ `In Stock`), and then by title.

```sql
SELECT 
    title,
    stock_quantity,
    CASE 
        WHEN stock_quantity = 0 THEN 'Out of Stock'
        WHEN stock_quantity < 6 THEN 'Low Stock'
        ELSE 'In Stock'
    END AS stock_status
FROM books
ORDER BY 
    CASE stock_status
        WHEN 'Out of Stock' THEN 1
        WHEN 'Low Stock' THEN 2
        ELSE 3
    END,
    title ASC;
```

Notice how we used a **Simple CASE** format here inside the `ORDER BY` clause, matching the exact string values of `stock_status` to numerical sorting weights (`1`, `2`, `3`).

---

## Summary Checklist

- **`CASE` works like If-Else:** It evaluates conditions sequentially and returns a value.
- **Always include `END`:** Every `CASE` expression must terminate with the `END` keyword (and optionally an alias using `AS`).
- **Powerful with Aggregates:** You can place `CASE` inside `SUM()` or `COUNT()` to do conditional counting.
- **Flexible Sorting:** Use `CASE` inside `ORDER BY` to control custom sorting sequences.
