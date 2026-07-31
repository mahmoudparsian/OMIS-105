SELECT COUNT(*) FROM sales;

SELECT SUM(price * quantity) FROM sales;

SELECT product, SUM(price * quantity)
FROM sales
GROUP BY product;

SELECT product, SUM(price * quantity) AS revenue
FROM sales
GROUP BY product
HAVING revenue > 1500;

SELECT product, SUM(price * quantity) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 1;
