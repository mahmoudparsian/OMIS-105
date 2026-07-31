# 10 Queries with CTEs and Ranking Functions

**1. Find the top 3 most expensive cats overall**
```sql
WITH ranked AS (
  SELECT name, price,
         ROW_NUMBER() OVER (ORDER BY price DESC) AS rn
  FROM cats
)
SELECT * FROM ranked WHERE rn <= 3;
```

**2. Find the cheapest cat per breed**
```sql
WITH cheapest AS (
  SELECT breed, name, price,
         RANK() OVER (PARTITION BY breed ORDER BY price ASC) AS rnk
  FROM cats
)
SELECT * FROM cheapest WHERE rnk = 1;
```

**3. Find the most expensive cat per country**
```sql
WITH exp AS (
  SELECT country, name, price,
         ROW_NUMBER() OVER (PARTITION BY country ORDER BY price DESC) AS rn
  FROM cats
)
SELECT * FROM exp WHERE rn = 1;
```

**4. Find cats whose price is above the average of their breed**
```sql
WITH breed_avg AS (
  SELECT breed, AVG(price) AS avg_price
  FROM cats GROUP BY breed
)
SELECT c.name, c.breed, c.price
FROM cats c
JOIN breed_avg b ON c.breed=b.breed
WHERE c.price > b.avg_price;
```

**5. Find the 2 youngest cats per breed**
```sql
WITH ranked AS (
  SELECT name, breed, date_of_birth,
         ROW_NUMBER() OVER (PARTITION BY breed ORDER BY date_of_birth DESC) AS rn
  FROM cats
)
SELECT * FROM ranked WHERE rn <= 2;
```

**6. Rank breeds by average price**
```sql
WITH breed_price AS (
  SELECT breed, AVG(price) AS avg_price
  FROM cats GROUP BY breed
)
SELECT breed, avg_price,
       RANK() OVER (ORDER BY avg_price DESC) AS rnk
FROM breed_price;
```

**7. Find cats with the maximum number of tricks**
```sql
WITH trick_counts AS (
  SELECT c.cat_id, c.name, COUNT(ct.trick_id) AS cnt
  FROM cats c
  JOIN cat_tricks ct ON c.cat_id=ct.cat_id
  GROUP BY c.cat_id, c.name
),
ranked AS (
  SELECT *, RANK() OVER (ORDER BY cnt DESC) AS rnk
  FROM trick_counts
)
SELECT * FROM ranked WHERE rnk = 1;
```

**8. Find the top 5 oldest cats**
```sql
WITH ranked AS (
  SELECT name, date_of_birth,
         ROW_NUMBER() OVER (ORDER BY date_of_birth ASC) AS rn
  FROM cats
)
SELECT * FROM ranked WHERE rn <= 5;
```

**9. Find the most common trick per country**
```sql
WITH trick_counts AS (
  SELECT c.country, t.trick, COUNT(*) AS cnt
  FROM cats c
  JOIN cat_tricks ct ON c.cat_id=ct.cat_id
  JOIN tricks t ON t.trick_id=ct.trick_id
  GROUP BY c.country, t.trick
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY country ORDER BY cnt DESC) AS rn
  FROM trick_counts
)
SELECT * FROM ranked WHERE rn = 1;
```

**10. Find the most expensive male and female cat per breed**
```sql
WITH ranked AS (
  SELECT breed, gender, name, price,
         ROW_NUMBER() OVER (PARTITION BY breed, gender ORDER BY price DESC) AS rn
  FROM cats
)
SELECT * FROM ranked WHERE rn = 1;
```

