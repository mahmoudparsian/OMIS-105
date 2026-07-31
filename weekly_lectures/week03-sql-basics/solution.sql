SELECT * FROM sales;

SELECT product, price FROM sales;

SELECT * FROM sales WHERE price > 700;

SELECT * FROM sales WHERE product = 'Laptop';

SELECT * FROM sales ORDER BY price DESC;

SELECT * FROM sales
WHERE price > 700 AND quantity >= 2;
