-- Customers
CREATE TABLE customers (id INT, name VARCHAR);

-- Orders
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    product VARCHAR,
    price INT
);
