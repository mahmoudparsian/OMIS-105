# DuckDB `BETWEEN` Examples & Equivalents

Compiled by: Dr. M. Parsian <br>
Updated Date: 09/29/2026

* In SQL, the `BETWEEN` operator selects values within a given range. 
* The range is **inclusive**, meaning both the start and end values are included in the results.

* In DuckDB SQL, the BETWEEN operator filters query results to include values within a specific range. It is **inclusive**, meaning it includes both the lower and upper bounds

* Syntax:

```sql
SELECT * 
FROM table_name 
WHERE column_name BETWEEN lower_bound AND upper_bound;

Equivalent to: 

SELECT * 
FROM table_name 
WHERE (column_name >= lower_bound) AND 
      (column_name <= upper_bound);

```


Below are 4 simple examples showing how to use `BETWEEN` in **DuckDB**, alongside equivalent expressions using greater-than-or-equal (`>=`) and less-than-or-equal (`<=`) comparison operators.

---

## Sample Data Setup

We will use two simple tables (`products` and `employees`) for our examples.

```sql
-- Table 1: products
CREATE TABLE products (
    product_id INT,
    product_name VARCHAR,
    price DECIMAL(10, 2),
    created_date DATE
);

INSERT INTO products VALUES
(1, 'Laptop', 1200.00, '2023-01-15'),
(2, 'Mouse', 25.50, '2023-03-10'),
(3, 'Keyboard', 75.00, '2023-05-20'),
(4, 'Monitor', 300.00, '2023-07-01'),
(5, 'USB Cable', 10.00, '2023-09-12'),
(6, 'Webcam', 85.00, '2023-11-05');

-- Table 2: employees
CREATE TABLE employees (
    emp_id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    salary INT,
    hire_date DATE
);

INSERT INTO employees VALUES
(101, 'Alice', 'Smith', 65000, '2021-02-01'),
(102, 'Bob', 'Jones', 48000, '2022-06-15'),
(103, 'Charlie', 'Brown', 82000, '2019-11-20'),
(104, 'Diana', 'Prince', 55000, '2023-01-10'),
(105, 'Evan', 'Wright', 95000, '2018-04-05'),
(106, 'Fiona', 'Gallagher', 72000, '2020-08-30');
```

---

## Example 1: Numeric Range Filtering (Prices)

Filter products with prices between `$25.00` and `$100.00` inclusive.

### Using `BETWEEN`
```sql
SELECT product_id, product_name, price
FROM products
WHERE price BETWEEN 25.00 AND 100.00;
```

### Equivalent using `>=` and `<=`
```sql
SELECT product_id, product_name, price
FROM products
WHERE price >= 25.00 AND price <= 100.00;
```

---

## Example 2: Date Range Filtering (Dates)

Find employees hired between `2020-01-01` and `2022-12-31`.

### Using `BETWEEN`
```sql
SELECT emp_id, first_name, last_name, hire_date
FROM employees
WHERE hire_date BETWEEN DATE '2020-01-01' AND DATE '2022-12-31';
```

### Equivalent using `>=` and `<=`
```sql
SELECT emp_id, first_name, last_name, hire_date
FROM employees
WHERE hire_date >= DATE '2020-01-01' AND hire_date <= DATE '2022-12-31';
```

---

## Example 3: Text / Alphabetical Range Filtering (Names)

Find employees whose last name starts with letters from **'B'** through **'G'** (inclusive of strings starting with 'G').

### Using `BETWEEN`
```sql
SELECT emp_id, first_name, last_name
FROM employees
WHERE last_name BETWEEN 'B' AND 'GZ';
```

### Equivalent using `>=` and `<=`
```sql
SELECT emp_id, first_name, last_name
FROM employees
WHERE last_name >= 'B' AND last_name <= 'GZ';
```

---

## Example 4: Excluding a Range (`NOT BETWEEN`)

Find products whose prices are **not** in the range of `$50.00` to `$500.00`.

### Using `NOT BETWEEN`
```sql
SELECT product_id, product_name, price
FROM products
WHERE price NOT BETWEEN 50.00 AND 500.00;
```

### Equivalent using `<` and `>`
```sql
SELECT product_id, product_name, price
FROM products
WHERE price < 50.00 OR price > 500.00;
```