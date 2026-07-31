# GROUP BY Tutorial 101

* Database Environment: DuckDB
* Last updated: May 25, 2026

## Description

		1. The GROUP BY clause in SQL gathers rows 
		with identical values into summary rows.
		This is a reduction operation.
		
		2. In SQL, the GROUP BY clause functions as 
		a reduction operation by collapsing multiple 
		individual rows into a single summary row 
		based on shared values in specified columns. 
		
		3. It is most frequently used with aggregate 
		functions like COUNT(), SUM(), AVG(), MAX(), 
		and MIN() to run calculations on each separate 
		group.


## SQL Syntax	


			SELECT column_name(s), 
			       AGGREGATE_FUNCTION(column_name)
			FROM table_name
			WHERE condition
			GROUP BY column_name(s);
		

## DuckDB from Command Line

```sql
% duckdb
-- Loading resources from /Users/max/.duckdbrc
DuckDB v1.5.3 (Variegata)
Enter ".help" for usage hints.
```

## Create a Table with 2 Columns

```sql
duckdb ▸ CREATE TABLE scores(player VARCHAR, score INT);
```

## Insert 4 rows for Alex

```sql
duckdb ▸ INSERT INTO scores(player, score) VALUES('Alex', 10);
duckdb ▸ INSERT INTO scores(player, score) VALUES('Alex', 20);
duckdb ▸ INSERT INTO scores(player, score) VALUES('Alex', 30);
duckdb ▸ INSERT INTO scores(player, score) VALUES('Alex', NULL);
```

## Insert 4 rows for Jane
```sql
duckdb ▸ INSERT INTO scores(player, score) VALUES('Jane', 70);
duckdb ▸ INSERT INTO scores(player, score) VALUES('Jane', 90);
duckdb ▸ INSERT INTO scores(player, score) VALUES('Jane', NULL);
duckdb ▸ INSERT INTO scores(player, score) VALUES('Jane', NULL);
```

## View Table

```sql
duckdb ▸ SELECT * FROM scores;
┌─────────┬───────┐
│ player  │ score │
│ varchar │ int32 │
├─────────┼───────┤
│ Alex    │    10 │
│ Alex    │    20 │
│ Alex    │    30 │
│ Alex    │  NULL │
│ Jane    │    70 │
│ Jane    │    90 │
│ Jane    │  NULL │
│ Jane    │  NULL │
└─────────┴───────┘
```

## Find Average of scores per player

```sql
duckdb ▸ SELECT player, 
                AVG(score) AS avg_score
         FROM scores 
         GROUP BY player;
┌─────────┬───────────┐
│ player  │ avg_score │
│ varchar │  double   │
├─────────┼───────────┤
│ Jane    │      80.0 │
│ Alex    │      20.0 │
└─────────┴───────────┘
```

**NOTE:** `AVG()` ignores `NULL` values. Alex has 
scores 10, 20, 30, NULL — the average is 
(10+20+30)/3 = 20.0, not (10+20+30+0)/4.

## Find Minimum and Maximum of scores per player

```sql
duckdb ▸ SELECT player, 
                MIN(score) AS min_score, 
                MAX(score) AS max_score
          FROM scores 
          GROUP BY player;
┌─────────┬───────────┬───────────┐
│ player  │ min_score │ max_score │
│ varchar │   int32   │   int32   │
├─────────┼───────────┼───────────┤
│ Jane    │        70 │        90 │
│ Alex    │        10 │        30 │
└─────────┴───────────┴───────────┘
```

## COUNT(*) vs COUNT(column_name) per player

		COUNT(*) counts all rows in the group, 
		including NULLs. COUNT(column_name) counts 
		only non-NULL values in that column.

```sql
duckdb ▸ SELECT player, 
                COUNT(*) AS total_rows, 
                COUNT(score) AS non_null_scores
         FROM scores 
         GROUP BY player;
┌─────────┬────────────┬─────────────────┐
│ player  │ total_rows │ non_null_scores │
│ varchar │   int64    │      int64      │
├─────────┼────────────┼─────────────────┤
│ Alex    │          4 │               3 │
│ Jane    │          4 │               2 │
└─────────┴────────────┴─────────────────┘
```

**NOTE:** Alex has 4 rows but only 3 non-NULL scores. 
Jane has 4 rows but only 2 non-NULL scores.


## Find Sum of scores per player

```sql
duckdb ▸ SELECT player, 
                SUM(score) AS total_score
         FROM scores 
         GROUP BY player;
┌─────────┬─────────────┐
│ player  │ total_score │
│ varchar │   int128    │
├─────────┼─────────────┤
│ Alex    │          60 │
│ Jane    │         160 │
└─────────┴─────────────┘
```

**NOTE:** Like `AVG()`, `SUM()` ignores `NULL` values.


## Combine multiple aggregates in one query

```sql
duckdb ▸ SELECT player, 
                COUNT(*) AS total_rows,
                COUNT(score) AS non_null_scores,
                SUM(score) AS total_score,
                AVG(score) AS avg_score,
                MIN(score) AS min_score,
                MAX(score) AS max_score
         FROM scores 
         GROUP BY player;
┌─────────┬────────────┬─────────────────┬─────────────┬───────────┬───────────┬───────────┐
│ player  │ total_rows │ non_null_scores │ total_score │ avg_score │ min_score │ max_score │
│ varchar │   int64    │      int64      │   int128    │  double   │   int32   │   int32   │
├─────────┼────────────┼─────────────────┼─────────────┼───────────┼───────────┼───────────┤
│ Alex    │          4 │               3 │          60 │      20.0 │        10 │        30 │
│ Jane    │          4 │               2 │         160 │      80.0 │        70 │        90 │
└─────────┴────────────┴─────────────────┴─────────────┴───────────┴───────────┴───────────┘
```


## HAVING: filter groups after aggregation

		The WHERE clause filters rows BEFORE grouping.
		The HAVING clause filters groups AFTER aggregation.

```sql
-- Find players whose average score is greater than 50
duckdb ▸ SELECT player, 
                AVG(score) AS avg_score
         FROM scores 
         GROUP BY player
         HAVING AVG(score) > 50;
┌─────────┬───────────┐
│ player  │ avg_score │
│ varchar │  double   │
├─────────┼───────────┤
│ Jane    │      80.0 │
└─────────┴───────────┘
```

```sql
-- Find players who have more than 2 non-NULL scores
duckdb ▸ SELECT player, 
                COUNT(score) AS non_null_scores
         FROM scores 
         GROUP BY player
         HAVING COUNT(score) > 2;
┌─────────┬─────────────────┐
│ player  │ non_null_scores │
│ varchar │      int64      │
├─────────┼─────────────────┤
│ Alex    │               3 │
└─────────┴─────────────────┘
```


## STRING_AGG and LIST: concatenate grouped values

		STRING_AGG() concatenates values into a 
		comma-separated string. LIST() collects 
		values into a DuckDB list (array).

```sql
duckdb ▸ SELECT player, 
                STRING_AGG(score::VARCHAR, ', ') AS scores_csv,
                LIST(score) AS scores_list
         FROM scores 
         GROUP BY player;
┌─────────┬────────────┬──────────────────┐
│ player  │ scores_csv │   scores_list    │
│ varchar │  varchar   │    int32[]       │
├─────────┼────────────┼──────────────────┤
│ Alex    │ 10, 20, 30 │ [10, 20, 30]     │
│ Jane    │ 70, 90     │ [70, 90]         │
└─────────┴────────────┴──────────────────┘
```

**NOTE:** Both `STRING_AGG()` and `LIST()` skip 
`NULL` values by default.


## GROUP BY with multiple columns

		First, let us add a 'team' column to our table.

```sql
duckdb ▸ ALTER TABLE scores ADD COLUMN team VARCHAR;
duckdb ▸ UPDATE scores SET team = 'Red' WHERE player = 'Alex';
duckdb ▸ UPDATE scores SET team = 'Blue' WHERE player = 'Jane';
```

```sql
-- Now insert a player on a different team
duckdb ▸ INSERT INTO scores(player, score, team) VALUES('Alex', 50, 'Blue');
duckdb ▸ INSERT INTO scores(player, score, team) VALUES('Jane', 40, 'Red');
```

```sql
duckdb ▸ SELECT * FROM scores;
┌─────────┬───────┬─────────┐
│ player  │ score │  team   │
│ varchar │ int32 │ varchar │
├─────────┼───────┼─────────┤
│ Alex    │    10 │ Red     │
│ Alex    │    20 │ Red     │
│ Alex    │    30 │ Red     │
│ Alex    │  NULL │ Red     │
│ Jane    │    70 │ Blue    │
│ Jane    │    90 │ Blue    │
│ Jane    │  NULL │ Blue    │
│ Jane    │  NULL │ Blue    │
│ Alex    │    50 │ Blue    │
│ Jane    │    40 │ Red     │
└─────────┴───────┴─────────┘
```

```sql
-- GROUP BY two columns: team and player
duckdb ▸ SELECT team,
                player, 
                COUNT(score) AS games,
                SUM(score) AS total_score,
                AVG(score) AS avg_score
         FROM scores 
         GROUP BY team, player
         ORDER BY team, player;
┌─────────┬─────────┬───────┬─────────────┬───────────┐
│  team   │ player  │ games │ total_score │ avg_score │
│ varchar │ varchar │ int64 │   int128    │  double   │
├─────────┼─────────┼───────┼─────────────┼───────────┤
│ Blue    │ Alex    │     1 │          50 │      50.0 │
│ Blue    │ Jane    │     2 │         160 │      80.0 │
│ Red     │ Alex    │     3 │          60 │      20.0 │
│ Red     │ Jane    │     1 │          40 │      40.0 │
└─────────┴─────────┴───────┴─────────────┴───────────┘
```

```sql
-- GROUP BY team only
duckdb ▸ SELECT team,
                COUNT(score) AS games,
                SUM(score) AS total_score,
                AVG(score) AS avg_score
         FROM scores 
         GROUP BY team
         ORDER BY team;
┌─────────┬───────┬─────────────┬───────────┐
│  team   │ games │ total_score │ avg_score │
│ varchar │ int64 │   int128    │  double   │
├─────────┼───────┼─────────────┼───────────┤
│ Blue    │     3 │         210 │      70.0 │
│ Red     │     4 │         100 │      25.0 │
└─────────┴───────┴─────────────┴───────────┘
```


## WHERE + GROUP BY + HAVING together

		Execution order: WHERE filters rows first, 
		then GROUP BY groups them, then HAVING 
		filters the groups.

```sql
-- Among non-NULL scores > 15, find teams 
-- whose average exceeds 40
duckdb ▸ SELECT team,
                AVG(score) AS avg_score,
                COUNT(score) AS num_scores
         FROM scores 
         WHERE score > 15
         GROUP BY team
         HAVING AVG(score) > 40
         ORDER BY avg_score DESC;
┌─────────┬───────────┬────────────┐
│  team   │ avg_score │ num_scores │
│ varchar │  double   │   int64    │
├─────────┼───────────┼────────────┤
│ Blue    │      70.0 │          3 │
└─────────┴───────────┴────────────┘
```


## GROUP BY with ORDER BY on aggregate

```sql
-- Rank teams by total score (descending)
duckdb ▸ SELECT team,
                SUM(score) AS total_score
         FROM scores 
         GROUP BY team
         ORDER BY total_score DESC;
┌─────────┬─────────────┐
│  team   │ total_score │
│ varchar │   int128    │
├─────────┼─────────────┤
│ Blue    │         210 │
│ Red     │         100 │
└─────────┴─────────────┘
```


## Rank players by score 

```sql
duckdb ▸ SELECT player, 
                score, 
                RANK() OVER(ORDER BY score DESC) as rnk 
         FROM scores;
┌─────────┬───────┬───────┐
│ player  │ score │  rnk  │
│ varchar │ int32 │ int64 │
├─────────┼───────┼───────┤
│ Jane    │    90 │     1 │
│ Jane    │    70 │     2 │
│ Alex    │    30 │     3 │
│ Alex    │    20 │     4 │
│ Alex    │    10 │     5 │
│ Alex    │  NULL │     6 │
│ Jane    │  NULL │     6 │
│ Jane    │  NULL │     6 │
└─────────┴───────┴───────┘
```

## Rank each player by score 

```sql
duckdb ▸ SELECT player, 
                score, 
                RANK() OVER(PARTITION BY player ORDER BY score DESC) as rnk 
         FROM scores;
┌─────────┬───────┬───────┐
│ player  │ score │  rnk  │
│ varchar │ int32 │ int64 │
├─────────┼───────┼───────┤
│ Jane    │    90 │     1 │
│ Jane    │    70 │     2 │
│ Jane    │  NULL │     3 │
│ Jane    │  NULL │     3 │
|---------|-------|-------|
│ Alex    │    30 │     1 │
│ Alex    │    20 │     2 │
│ Alex    │    10 │     3 │
│ Alex    │  NULL │     4 │
└─────────┴───────┴───────┘
```

## Find top-2 score per player 

```sql
duckdb ▸ WITH ranked AS (
            SELECT player, 
                   score, 
                   RANK() OVER (
                        PARTITION BY player 
                        ORDER BY score DESC
                   ) 
                    as rnk 
            FROM scores
         ) 
         SELECT player, 
                score, 
                rnk 
         FROM ranked 
         WHERE rnk <= 2;
┌─────────┬───────┬───────┐
│ player  │ score │  rnk  │
│ varchar │ int32 │ int64 │
├─────────┼───────┼───────┤
│ Alex    │    30 │     1 │
│ Alex    │    20 │     2 │
|---------|-------|-------|
│ Jane    │    90 │     1 │
│ Jane    │    70 │     2 │
└─────────┴───────┴───────┘
```

