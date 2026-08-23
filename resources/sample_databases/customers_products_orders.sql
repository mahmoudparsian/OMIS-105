-- Database: DuckDB
-- 3 Tables: { customers, products, orders }

-- Create customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR,
    email VARCHAR,
    signup_date DATE
);

-- Populate customers table
INSERT INTO customers VALUES
(1, 'Alice Smith', 'alice@example.com', '2026-01-15'),
(2, 'Bob Jones', 'bob@example.com', '2026-02-20'),
(3, 'Charlie Brown', 'charlie@example.com', '2026-03-05');

-- Create products table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR,
    category VARCHAR,
    price DECIMAL(10, 2)
);

-- Populate products table
INSERT INTO products VALUES
(101, 'Mechanical Keyboard', 'Electronics', 89.99),
(102, 'Ergonomic Mouse', 'Electronics', 49.50),
(103, 'Coffee Mug', 'Kitchen', 15.00),
(104, 'Desk Mat', 'Office', 25.00);

-- Create orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    order_date TIMESTAMP,
    quantity INTEGER
);

-- Populate orders table
INSERT INTO orders VALUES
(1001, 1, 101, '2026-08-20 10:30:00', 1),
(1002, 1, 103, '2026-08-20 10:32:00', 2),
(1003, 2, 102, '2026-08-21 14:15:00', 1),
(1004, 3, 104, '2026-08-22 09:00:00', 3),
(1005, 2, 101, '2026-08-22 11:45:00', 1);


