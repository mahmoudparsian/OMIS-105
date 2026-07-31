-- Sample answers vary

SELECT * FROM table;

SELECT a.col, b.col
FROM a JOIN b ON a.id = b.id;

SELECT category, SUM(value)
FROM review
GROUP BY category;
