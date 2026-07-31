SELECT c.name, o.product
FROM customers c
JOIN orders o ON c.id = o.customer_id;

SELECT c.name, o.product
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;

SELECT c.name, SUM(o.amount) AS total
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;
