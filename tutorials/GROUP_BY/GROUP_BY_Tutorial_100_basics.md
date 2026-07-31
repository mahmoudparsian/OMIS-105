# Understanding GROUP BY

```
% duckdb
-- Loading resources from /Users/max/.duckdbrc
DuckDB v1.5.2 (Variegata)
Enter ".help" for usage hints.

memory D CREATE TABLE scores (country VARCHAR, score INT);

memory D INSERT INTO scores VALUES 
         ('USA', 100), ('USA', 200), ('USA', 300), ('USA', 1000);

memory D INSERT INTO scores VALUES 
         ('CANADA', 10), ('CANADA', 20), ('CANADA', 90);

memory D SELECT * FROM scores;
┌─────────┬───────┐
│ country │ score │
│ varchar │ int32 │
├─────────┼───────┤
│ USA     │   100 │
│ USA     │   200 │
│ USA     │   300 │
│ USA     │  1000 │
│ CANADA  │    10 │
│ CANADA  │    20 │
│ CANADA  │    90 │
└─────────┴───────┘
memory D SELECT country, 
                MIN(score) as min_score, 
                MAX(score) as max_score, 
                AVG(score) as avg_score, 
                LISTAGG(score)  
         FROM scores 
         GROUP BY country;
┌─────────┬───────────┬───────────┬───────────┬──────────────────┐
│ country │ min_score │ max_score │ avg_score │  listagg(score)  │
│ varchar │   int32   │   int32   │  double   │     varchar      │
├─────────┼───────────┼───────────┼───────────┼──────────────────┤
│ USA     │       100 │      1000 │     400.0 │ 100,200,300,1000 │
│ CANADA  │        10 │        90 │      40.0 │ 10,20,90         │
└─────────┴───────────┴───────────┴───────────┴──────────────────┘

memory D WITH ranked AS (
              SELECT country, 
                     score, 
                     RANK() OVER (ORDER BY score DESC) as rnk 
              FROM scores
         ) 
         SELECT  country, 
                 score, 
                 rnk 
         FROM ranked 
         WHERE rnk <=2;
         
┌─────────┬───────┬───────┐
│ country │ score │  rnk  │
│ varchar │ int32 │ int64 │
├─────────┼───────┼───────┤
│ USA     │  1000 │     1 │
│ USA     │   300 │     2 │
└─────────┴───────┴───────┘

memory D WITH ranked AS (
            SELECT country, 
                   score, 
                   RANK() OVER (
                        PARTITION BY country 
                        ORDER BY score DESC
                    ) as rnk 
            FROM scores
         ) 
         SELECT  country, 
                 score, 
                 rnk 
         FROM ranked 
         WHERE rnk <=2;
┌─────────┬───────┬───────┐
│ country │ score │  rnk  │
│ varchar │ int32 │ int64 │
├─────────┼───────┼───────┤
│ USA     │  1000 │     1 │
│ USA     │   300 │     2 │
│ CANADA  │    90 │     1 │
│ CANADA  │    20 │     2 │
└─────────┴───────┴───────┘

memory D WITH ranked AS (
            SELECT country, 
                   score, 
                   RANK() OVER (
                        PARTITION BY country 
                        ORDER BY score ASC
                    ) as rnk 
            FROM scores
         ) 
         SELECT  country, 
                 score, 
                 rnk 
         FROM ranked 
         WHERE rnk <=2;
┌─────────┬───────┬───────┐
│ country │ score │  rnk  │
│ varchar │ int32 │ int64 │
├─────────┼───────┼───────┤
│ CANADA  │    10 │     1 │
│ CANADA  │    20 │     2 │
│ USA     │   100 │     1 │
│ USA     │   200 │     2 │
└─────────┴───────┴───────┘
```