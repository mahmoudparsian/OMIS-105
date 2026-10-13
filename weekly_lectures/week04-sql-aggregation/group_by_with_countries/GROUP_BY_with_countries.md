# `GROUP BY` Explained

```sql
% duckdb

D CREATE TABLE countries (
     country VARCHAR, 
     score INT
  );

D DESC countries;
┌─────────────────┐
│    countries    │
│                 │
│ country varchar │
│ score   integer │
└─────────────────┘

D INSERT INTO countries(country, score)
    VALUES
     ('USA', 20), ('USA', 40), ('USA', 15),
     ('CANADA', 25), ('CANADA', 65),
     ('INDIA', 80);

D SELECT * FROM countries;
┌─────────┬───────┐
│ country │ score │
│ varchar │ int32 │
├─────────┼───────┤
│ USA     │    20 │
│ USA     │    40 │
│ USA     │    15 │
│ CANADA  │    25 │
│ CANADA  │    65 │
│ INDIA   │    80 │
└─────────┴───────┘

D SELECT country,
         AVG(score) AS avg_score
FROM countries
GROUP BY country;
┌─────────┬───────────┐
│ country │ avg_score │
│ varchar │  double   │
├─────────┼───────────┤
│ USA     │      25.0 │
│ CANADA  │      45.0 │
│ INDIA   │      80.0 │
└─────────┴───────────┘

D SELECT country,
         AVG(score) AS avg_score, 
         GROUP_CONCAT(score)
FROM countries
GROUP BY country;
┌─────────┬───────────┬─────────────────────┐
│ country │ avg_score │ group_concat(score) │
│ varchar │  double   │       varchar       │
├─────────┼───────────┼─────────────────────┤
│ INDIA   │      80.0 │ 80                  │ <- 80.0 = (80 / 1)
│ CANADA  │      45.0 │ 25,65               │ <- 45.0 = (25+65) / 2
│ USA     │      25.0 │ 20,40,15            │ <- 25.0 = (20+40+15) / 3
└─────────┴───────────┴─────────────────────┘

D SELECT country,
         AVG(score) AS avg_score, 
         LIST(score)
FROM countries
GROUP BY country;
┌─────────┬───────────┬──────────────┐
│ country │ avg_score │ list(score)  │
│ varchar │  double   │   int32[]    │
├─────────┼───────────┼──────────────┤
│ USA     │      25.0 │ [20, 40, 15] │
│ CANADA  │      45.0 │ [25, 65]     │
│ INDIA   │      80.0 │ [80]         │
└─────────┴───────────┴──────────────┘
```