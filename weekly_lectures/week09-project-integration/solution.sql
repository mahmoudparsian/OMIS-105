-- Example structure

CREATE TABLE customers (id INT, name VARCHAR);
CREATE TABLE orders (id INT, customer_id INT, amount INT);

SELECT c.name, SUM(o.amount)
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;
