# Insurance Table SQL Practice — Level 1 (Basic)

	The goal of this homework/lab is to
	load some insurance data into a DuckDB
	table and perform some data analytics.

	All queries and results in this file were
	validated with DuckDB v1.5.5.


## 1. Insurance Data

```
file name: insurance_1440_records.csv   (1440 records + 1 header line)
```

| Column name | Description |
|-------------|-------------|
| age         | age of an insured person |
| gender      | male/female |
| bmi         | body mass index |
| children    | number of children |
| smoker      | yes/no |
| region      | southwest, southeast, northwest, northeast |
| charges     | insurance charges |


## 2. Table Schema

```sql
CREATE TABLE insurance (
    age      INTEGER,
    gender   VARCHAR,
    bmi      DOUBLE,
    children INTEGER,
    smoker   VARCHAR,
    region   VARCHAR,
    charges  DOUBLE
);
```

Notes:

* `bmi` and `charges` are stored as `DOUBLE` so that no digits from the
  CSV file are lost (e.g., `bmi = 22.705`, `charges = 16884.924`).
* `smoker` is declared as `VARCHAR` so it keeps the values `'yes'`/`'no'`.
  (If you let `read_csv_auto()` guess the types, DuckDB turns `smoker`
  into a `BOOLEAN` column with values `true`/`false`.)


## 3. Load Data Using DuckDB

	Load data into a DuckDB table named
	"insurance" in a database file
	named insurance_db.duckdb.


## 4. Instructions to Load CSV from Command Line

Open the DuckDB CLI with a persistent database file
(run it from the folder that contains the CSV file):

```bash
duckdb insurance_db.duckdb
```

Inside the DuckDB prompt, create the table (section 2) and load the CSV file:

```sql
COPY insurance FROM 'insurance_1440_records.csv' (HEADER true);
```

Verify:

```sql
SELECT COUNT(*) AS total_records
FROM insurance;
```

**Result:**

```text
┌───────────────┐
│ total_records │
│     int64     │
├───────────────┤
│          1440 │
└───────────────┘
```

Alternative (one step, DuckDB infers the column types — note that
`smoker` becomes `BOOLEAN` in this case):

```sql
CREATE TABLE insurance AS
SELECT * FROM read_csv_auto('insurance_1440_records.csv');
```

DuckDB tips:

* String literals use single quotes: `'yes'`, `'female'`
  (double quotes are for identifiers such as column names).
* String comparison is case-sensitive: `'Female' <> 'female'`.
* Without `ORDER BY`, DuckDB does **not** guarantee the order of
  the rows returned (especially after `GROUP BY`). Add `ORDER BY`
  whenever the order matters.
* In the results below, long outputs are truncated to 10 rows by
  the DuckDB CLI (`.maxrows 10`); the total row count is shown at
  the bottom of each result.


## 5. SQL Practice Queries (basic)


### Q1. Show all rows

```sql
SELECT *
FROM insurance;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    19 │ female  │   27.9 │        0 │ yes     │ southwest │   16884.924 │
│    18 │ male    │  33.77 │        1 │ no      │ southeast │   1725.5523 │
│    28 │ male    │   33.0 │        3 │ no      │ southeast │    4449.462 │
│    33 │ male    │ 22.705 │        0 │ no      │ northwest │ 21984.47061 │
│    32 │ male    │  28.88 │        0 │ no      │ northwest │   3866.8552 │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·     │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·     │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·     │
│    19 │ female  │   34.7 │        2 │ yes     │ southwest │   36397.576 │
│    19 │ female  │   20.6 │        0 │ no      │ southwest │    1731.677 │
│    26 │ female  │   33.4 │        0 │ yes     │ southwest │ 19795.93733 │
│    56 │ female  │   44.7 │        3 │ yes     │ southwest │   31411.685 │
│    26 │ female  │   25.8 │        0 │ yes     │ southwest │   22007.945 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  1440 rows (10 shown)     use .last to show entire result      7 columns
```

### Q2. List ages and charges

```sql
SELECT age, charges
FROM insurance;
```

**Result:**

```text
┌───────┬─────────────┐
│  age  │   charges   │
│ int32 │   double    │
├───────┼─────────────┤
│    19 │   16884.924 │
│    18 │   1725.5523 │
│    28 │    4449.462 │
│    33 │ 21984.47061 │
│    32 │   3866.8552 │
│     · │       ·     │
│     · │       ·     │
│     · │       ·     │
│    19 │   36397.576 │
│    19 │    1731.677 │
│    26 │ 19795.93733 │
│    56 │   31411.685 │
│    26 │   22007.945 │
└───────┴─────────────┘
       1440 rows     
      (10 shown)
```

### Q3. Find all smokers

```sql
SELECT *
FROM insurance
WHERE smoker = 'yes';
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    19 │ female  │   27.9 │        0 │ yes     │ southwest │   16884.924 │
│    62 │ female  │  26.29 │        0 │ yes     │ southeast │  27808.7251 │
│    27 │ male    │  42.13 │        0 │ yes     │ southeast │  39611.7577 │
│    30 │ male    │   35.3 │        0 │ yes     │ southwest │   36837.467 │
│    34 │ female  │  31.92 │        1 │ yes     │ northeast │  37701.8768 │
│     · │   ·     │     ·  │        · │  ·      │     ·     │       ·     │
│     · │   ·     │     ·  │        · │  ·      │     ·     │       ·     │
│     · │   ·     │     ·  │        · │  ·      │     ·     │       ·     │
│    28 │ female  │   30.2 │        0 │ yes     │ southwest │   38900.653 │
│    19 │ female  │   34.7 │        2 │ yes     │ southwest │   36397.576 │
│    26 │ female  │   33.4 │        0 │ yes     │ southwest │ 19795.93733 │
│    56 │ female  │   44.7 │        3 │ yes     │ southwest │   31411.685 │
│    26 │ female  │   25.8 │        0 │ yes     │ southwest │   22007.945 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  305 rows (10 shown)      use .last to show entire result      7 columns
```

### Q4. Find all non-smokers

```sql
SELECT *
FROM insurance
WHERE smoker = 'no';
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    18 │ male    │  33.77 │        1 │ no      │ southeast │   1725.5523 │
│    28 │ male    │   33.0 │        3 │ no      │ southeast │    4449.462 │
│    33 │ male    │ 22.705 │        0 │ no      │ northwest │ 21984.47061 │
│    32 │ male    │  28.88 │        0 │ no      │ northwest │   3866.8552 │
│    31 │ female  │  25.74 │        0 │ no      │ southeast │   3756.6216 │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│    57 │ female  │   30.5 │        0 │ no      │ southwest │    10704.47 │
│    24 │ female  │   33.3 │        0 │ no      │ southwest │    1880.487 │
│    38 │ female  │   25.9 │        1 │ no      │ southwest │    5472.449 │
│    29 │ female  │   20.8 │        1 │ no      │ southwest │    3208.787 │
│    19 │ female  │   20.6 │        0 │ no      │ southwest │    1731.677 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  1135 rows (10 shown)     use .last to show entire result      7 columns
```

### Q5. List all unique regions

```sql
SELECT DISTINCT region
FROM insurance
ORDER BY region;
```

**Result:**

```text
┌───────────┐
│  region   │
│  varchar  │
├───────────┤
│ northeast │
│ northwest │
│ southeast │
│ southwest │
└───────────┘
```

### Q6. Count total records

solution-1:

```sql
SELECT COUNT(*)
FROM insurance;
```

**Result:**

```text
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│         1440 │
└──────────────┘
```

solution-2:

```sql
SELECT COUNT(*) AS total_records
FROM insurance;
```

**Result:**

```text
┌───────────────┐
│ total_records │
│     int64     │
├───────────────┤
│          1440 │
└───────────────┘
```

### Q7. Find people with BMI > 30

```sql
SELECT *
FROM insurance
WHERE bmi > 30;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    18 │ male    │  33.77 │        1 │ no      │ southeast │   1725.5523 │
│    28 │ male    │   33.0 │        3 │ no      │ southeast │    4449.462 │
│    46 │ female  │  33.44 │        1 │ no      │ southeast │   8240.5896 │
│    23 │ male    │   34.4 │        0 │ no      │ southwest │    1826.843 │
│    56 │ female  │  39.82 │        0 │ no      │ southeast │  11090.7178 │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│    24 │ female  │   33.3 │        0 │ no      │ southwest │    1880.487 │
│    28 │ female  │   30.2 │        0 │ yes     │ southwest │   38900.653 │
│    19 │ female  │   34.7 │        2 │ yes     │ southwest │   36397.576 │
│    26 │ female  │   33.4 │        0 │ yes     │ southwest │ 19795.93733 │
│    56 │ female  │   44.7 │        3 │ yes     │ southwest │   31411.685 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  772 rows (10 shown)      use .last to show entire result      7 columns
```

### Q8. Find people with children > 2

```sql
SELECT *
FROM insurance
WHERE children > 2;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    28 │ male    │   33.0 │        3 │ no      │ southeast │    4449.462 │
│    37 │ female  │  27.74 │        3 │ no      │ northwest │   7281.5056 │
│    59 │ female  │  27.72 │        3 │ no      │ southeast │  14001.1338 │
│    19 │ female  │   28.6 │        5 │ no      │ southwest │    4687.797 │
│    62 │ female  │ 32.965 │        3 │ no      │ northwest │ 15612.19335 │
│     · │  ·      │    ·   │        · │ ·       │     ·     │       ·     │
│     · │  ·      │    ·   │        · │ ·       │     ·     │       ·     │
│     · │  ·      │    ·   │        · │ ·       │     ·     │       ·     │
│    45 │ male    │  24.31 │        5 │ no      │ southeast │   9788.8659 │
│    60 │ male    │  33.11 │        3 │ no      │ southeast │  15919.8229 │
│    46 │ female  │   25.7 │        3 │ no      │ southwest │    9101.798 │
│    42 │ female  │   29.3 │        4 │ no      │ southwest │ 15828.82173 │
│    56 │ female  │   44.7 │        3 │ yes     │ southwest │   31411.685 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  213 rows (10 shown)      use .last to show entire result      7 columns
```

### Q9. Find females with charges > 10000

```sql
SELECT *
FROM insurance
WHERE (gender = 'female') AND
      (charges > 10000);
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    19 │ female  │   27.9 │        0 │ yes     │ southwest │   16884.924 │
│    60 │ female  │  25.84 │        0 │ no      │ northwest │ 28923.13692 │
│    62 │ female  │  26.29 │        0 │ yes     │ southeast │  27808.7251 │
│    56 │ female  │  39.82 │        0 │ no      │ southeast │  11090.7178 │
│    52 │ female  │  30.78 │        1 │ no      │ northeast │  10797.3362 │
│     · │   ·     │     ·  │        · │ ·       │     ·     │       ·     │
│     · │   ·     │     ·  │        · │ ·       │     ·     │       ·     │
│     · │   ·     │     ·  │        · │ ·       │     ·     │       ·     │
│    28 │ female  │   30.2 │        0 │ yes     │ southwest │   38900.653 │
│    19 │ female  │   34.7 │        2 │ yes     │ southwest │   36397.576 │
│    26 │ female  │   33.4 │        0 │ yes     │ southwest │ 19795.93733 │
│    56 │ female  │   44.7 │        3 │ yes     │ southwest │   31411.685 │
│    26 │ female  │   25.8 │        0 │ yes     │ southwest │   22007.945 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  320 rows (10 shown)      use .last to show entire result      7 columns
```

### Q10. Find males younger than 25

```sql
SELECT *
FROM insurance
WHERE (gender = 'male') AND
      (age < 25);
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    18 │ male    │  33.77 │        1 │ no      │ southeast │   1725.5523 │
│    23 │ male    │   34.4 │        0 │ no      │ southwest │    1826.843 │
│    19 │ male    │   24.6 │        1 │ no      │ southwest │    1837.237 │
│    23 │ male    │ 23.845 │        0 │ no      │ northeast │  2395.17155 │
│    18 │ male    │   34.1 │        0 │ no      │ southeast │    1137.011 │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │
│    18 │ male    │  43.01 │        0 │ no      │ southeast │   1449.3959 │
│    21 │ male    │  36.85 │        0 │ no      │ southeast │   1694.3045 │
│    23 │ male    │  32.56 │        0 │ no      │ southeast │   1824.2854 │
│    19 │ male    │  30.25 │        0 │ yes     │ southeast │  32548.3405 │
│    20 │ male    │  35.31 │        1 │ no      │ southeast │ 27924.28875 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  159 rows (10 shown)      use .last to show entire result      7 columns
```

### Q11. Find top 5 highest charges

```sql
SELECT *
FROM insurance
ORDER BY charges DESC
LIMIT 5;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    54 │ female  │  47.41 │        0 │ yes     │ southeast │ 63770.42801 │
│    45 │ male    │  30.36 │        0 │ yes     │ southeast │ 62592.87309 │
│    52 │ male    │ 34.485 │        3 │ yes     │ northwest │ 60021.39897 │
│    31 │ female  │ 38.095 │        1 │ yes     │ northeast │ 58571.07448 │
│    33 │ female  │  35.53 │        0 │ yes     │ northwest │ 55135.40209 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
```

### Q12. Find top 5 lowest charges

```sql
SELECT *
FROM insurance
ORDER BY charges ASC
LIMIT 5;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬───────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │  charges  │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │  double   │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼───────────┤
│    18 │ male    │  23.21 │        0 │ no      │ southeast │ 1121.8739 │
│    18 │ male    │  30.14 │        0 │ no      │ southeast │ 1131.5066 │
│    18 │ male    │  33.33 │        0 │ no      │ southeast │ 1135.9407 │
│    18 │ male    │  33.66 │        0 │ no      │ southeast │ 1136.3994 │
│    18 │ male    │   34.1 │        0 │ no      │ southeast │  1137.011 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴───────────┘
```

### Q13. Find average BMI

solution-1:

```sql
SELECT AVG(bmi)
FROM insurance;
```

**Result:**

```text
┌────────────────────┐
│      avg(bmi)      │
│       double       │
├────────────────────┤
│ 30.786579861111107 │
└────────────────────┘
```

solution-2:

```sql
SELECT AVG(bmi) AS avg_bmi
FROM insurance;
```

**Result:**

```text
┌────────────────────┐
│      avg_bmi       │
│       double       │
├────────────────────┤
│ 30.786579861111107 │
└────────────────────┘
```

### Q14. Find maximum charges

solution-1:

```sql
SELECT MAX(charges)
FROM insurance;
```

**Result:**

```text
┌──────────────┐
│ max(charges) │
│    double    │
├──────────────┤
│  63770.42801 │
└──────────────┘
```

solution-2:

```sql
SELECT MAX(charges) AS maximum_charges
FROM insurance;
```

**Result:**

```text
┌─────────────────┐
│ maximum_charges │
│     double      │
├─────────────────┤
│     63770.42801 │
└─────────────────┘
```

### Q15. Find minimum charges

solution-1:

```sql
SELECT MIN(charges)
FROM insurance;
```

**Result:**

```text
┌──────────────┐
│ min(charges) │
│    double    │
├──────────────┤
│    1121.8739 │
└──────────────┘
```

solution-2:

```sql
SELECT MIN(charges) AS minimum_charges
FROM insurance;
```

**Result:**

```text
┌─────────────────┐
│ minimum_charges │
│     double      │
├─────────────────┤
│       1121.8739 │
└─────────────────┘
```

### Q16. Count smokers

solution-1:

```sql
SELECT COUNT(*)
FROM insurance
WHERE smoker = 'yes';
```

**Result:**

```text
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│          305 │
└──────────────┘
```

solution-2:

```sql
SELECT COUNT(*) AS smokers_count
FROM insurance
WHERE smoker = 'yes';
```

**Result:**

```text
┌───────────────┐
│ smokers_count │
│     int64     │
├───────────────┤
│           305 │
└───────────────┘
```

### Q17. Count non-smokers

solution-1:

```sql
SELECT COUNT(*)
FROM insurance
WHERE smoker = 'no';
```

**Result:**

```text
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│         1135 │
└──────────────┘
```

solution-2:

```sql
SELECT COUNT(*) AS non_smokers_count
FROM insurance
WHERE smoker = 'no';
```

**Result:**

```text
┌───────────────────┐
│ non_smokers_count │
│       int64       │
├───────────────────┤
│              1135 │
└───────────────────┘
```

### Q18. Average charges for smokers

solution-1:

```sql
SELECT AVG(charges)
FROM insurance
WHERE smoker = 'yes';
```

**Result:**

```text
┌────────────────────┐
│    avg(charges)    │
│       double       │
├────────────────────┤
│ 32317.359314655743 │
└────────────────────┘
```

solution-2:

```sql
SELECT AVG(charges) AS avg_charges_for_smokers
FROM insurance
WHERE smoker = 'yes';
```

**Result:**

```text
┌─────────────────────────┐
│ avg_charges_for_smokers │
│         double          │
├─────────────────────────┤
│      32317.359314655743 │
└─────────────────────────┘
```

### Q19. Average charges for non-smokers

solution-1:

```sql
SELECT AVG(charges)
FROM insurance
WHERE smoker = 'no';
```

**Result:**

```text
┌───────────────────┐
│   avg(charges)    │
│      double       │
├───────────────────┤
│ 8481.604000774443 │
└───────────────────┘
```

solution-2:

```sql
SELECT AVG(charges) AS avg_charges_for_non_smokers
FROM insurance
WHERE smoker = 'no';
```

**Result:**

```text
┌─────────────────────────────┐
│ avg_charges_for_non_smokers │
│           double            │
├─────────────────────────────┤
│           8481.604000774443 │
└─────────────────────────────┘
```

### Q20. Find all records from southeast

```sql
SELECT *
FROM insurance
WHERE region = 'southeast';
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    18 │ male    │  33.77 │        1 │ no      │ southeast │   1725.5523 │
│    28 │ male    │   33.0 │        3 │ no      │ southeast │    4449.462 │
│    31 │ female  │  25.74 │        0 │ no      │ southeast │   3756.6216 │
│    46 │ female  │  33.44 │        1 │ no      │ southeast │   8240.5896 │
│    62 │ female  │  26.29 │        0 │ yes     │ southeast │  27808.7251 │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·     │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·     │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·     │
│    59 │ male    │   29.7 │        2 │ no      │ southeast │   12925.886 │
│    37 │ male    │  36.19 │        0 │ no      │ southeast │ 19214.70553 │
│    64 │ male    │  40.48 │        0 │ no      │ southeast │  13831.1152 │
│    53 │ male    │  31.35 │        0 │ no      │ southeast │ 27346.04207 │
│    34 │ male    │  34.21 │        0 │ no      │ southeast │   3935.1799 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  441 rows (10 shown)      use .last to show entire result      7 columns
```

### Q21. Find average age of females

solution-1:

```sql
SELECT AVG(age)
FROM insurance
WHERE gender = 'female';
```

**Result:**

```text
┌───────────────────┐
│     avg(age)      │
│      double       │
├───────────────────┤
│ 39.37700145560407 │
└───────────────────┘
```

solution-2:

```sql
SELECT AVG(age) AS avg_age_females
FROM insurance
WHERE gender = 'female';
```

**Result:**

```text
┌───────────────────┐
│  avg_age_females  │
│      double       │
├───────────────────┤
│ 39.37700145560407 │
└───────────────────┘
```

### Q22. Find average age of males

solution-1:

```sql
SELECT AVG(age)
FROM insurance
WHERE gender = 'male';
```

**Result:**

```text
┌──────────────────┐
│     avg(age)     │
│      double      │
├──────────────────┤
│ 39.0863213811421 │
└──────────────────┘
```

solution-2:

```sql
SELECT AVG(age) AS average_age_of_males
FROM insurance
WHERE gender = 'male';
```

**Result:**

```text
┌──────────────────────┐
│ average_age_of_males │
│        double        │
├──────────────────────┤
│     39.0863213811421 │
└──────────────────────┘
```

### Q23. Find people with charges between 5000 and 10000

solution-1:

```sql
SELECT *
FROM insurance
WHERE charges BETWEEN 5000 AND 10000;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │  charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double   │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼────────────┤
│    46 │ female  │  33.44 │        1 │ no      │ southeast │  8240.5896 │
│    37 │ female  │  27.74 │        3 │ no      │ northwest │  7281.5056 │
│    37 │ male    │  29.83 │        2 │ no      │ northeast │  6406.4107 │
│    37 │ male    │ 28.025 │        2 │ no      │ northwest │ 6203.90175 │
│    41 │ male    │  21.78 │        1 │ no      │ southeast │  6272.4772 │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·    │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·    │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·    │
│    41 │ female  │   27.4 │        1 │ no      │ southwest │   6496.886 │
│    46 │ female  │   25.7 │        3 │ no      │ southwest │   9101.798 │
│    43 │ female  │   37.9 │        0 │ no      │ southwest │   6474.013 │
│    45 │ female  │   29.9 │        1 │ no      │ southwest │   8337.748 │
│    38 │ female  │   25.9 │        1 │ no      │ southwest │   5472.449 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴────────────┘
  369 rows (10 shown)     use .last to show entire result      7 columns
```

solution-2:

```sql
SELECT *
FROM insurance
WHERE (charges >= 5000) AND
      (charges <= 10000);
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │  charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double   │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼────────────┤
│    46 │ female  │  33.44 │        1 │ no      │ southeast │  8240.5896 │
│    37 │ female  │  27.74 │        3 │ no      │ northwest │  7281.5056 │
│    37 │ male    │  29.83 │        2 │ no      │ northeast │  6406.4107 │
│    37 │ male    │ 28.025 │        2 │ no      │ northwest │ 6203.90175 │
│    41 │ male    │  21.78 │        1 │ no      │ southeast │  6272.4772 │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·    │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·    │
│     · │  ·      │     ·  │        · │ ·       │     ·     │       ·    │
│    41 │ female  │   27.4 │        1 │ no      │ southwest │   6496.886 │
│    46 │ female  │   25.7 │        3 │ no      │ southwest │   9101.798 │
│    43 │ female  │   37.9 │        0 │ no      │ southwest │   6474.013 │
│    45 │ female  │   29.9 │        1 │ no      │ southwest │   8337.748 │
│    38 │ female  │   25.9 │        1 │ no      │ southwest │   5472.449 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴────────────┘
  369 rows (10 shown)     use .last to show entire result      7 columns
```

### Q24. Find distinct BMI values

```sql
SELECT DISTINCT bmi
FROM insurance
ORDER BY bmi;
```

**Result:**

```text
┌────────────┐
│    bmi     │
│   double   │
├────────────┤
│      15.96 │
│     16.815 │
│     17.195 │
│      17.29 │
│     17.385 │
│        ·   │
│        ·   │
│        ·   │
│      48.07 │
│      49.06 │
│      50.38 │
│      52.58 │
│      53.13 │
└────────────┘
   548 rows 
  (10 shown)
```

### Q25. Find people with exactly 2 children

```sql
SELECT *
FROM insurance
WHERE children = 2;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    37 │ male    │  29.83 │        2 │ no      │ northeast │   6406.4107 │
│    37 │ male    │ 28.025 │        2 │ no      │ northwest │  6203.90175 │
│    55 │ female  │ 32.775 │        2 │ no      │ northwest │ 12268.63225 │
│    31 │ male    │   36.3 │        2 │ yes     │ southwest │     38711.0 │
│    31 │ female  │  36.63 │        2 │ no      │ southeast │   4949.7587 │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│    44 │ female  │   26.7 │        2 │ yes     │ southwest │     22478.6 │
│    32 │ female  │   25.8 │        2 │ no      │ southwest │    4934.705 │
│    60 │ female  │   34.8 │        2 │ no      │ southwest │ 36910.60803 │
│    53 │ female  │   33.3 │        2 │ no      │ southwest │   14806.839 │
│    19 │ female  │   34.7 │        2 │ yes     │ southwest │   36397.576 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  257 rows (10 shown)      use .last to show entire result      7 columns
```

### Q26. Find youngest person

Note: many people are 18 years old (the minimum age), so `LIMIT 1`
returns just one of them. Q43 shows how to get the minimum age itself.

```sql
SELECT *
FROM insurance
ORDER BY age ASC
LIMIT 1;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬───────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │  charges  │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │  double   │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼───────────┤
│    18 │ male    │  33.77 │        1 │ no      │ southeast │ 1725.5523 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴───────────┘
```

### Q27. Find oldest person

Note: as in Q26, several people share the maximum age (64).

```sql
SELECT *
FROM insurance
ORDER BY age DESC
LIMIT 1;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    64 │ male    │   24.7 │        1 │ no      │ northwest │ 30166.61817 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
```

### Q28. Find average charges per region

solution-1:

```sql
SELECT region, AVG(charges)
FROM insurance
GROUP BY region
ORDER BY region;
```

**Result:**

```text
┌───────────┬────────────────────┐
│  region   │    avg(charges)    │
│  varchar  │       double       │
├───────────┼────────────────────┤
│ northeast │   13406.3845163858 │
│ northwest │ 12417.575373969228 │
│ southeast │ 15215.024430408172 │
│ southwest │      12554.8822234 │
└───────────┴────────────────────┘
```

solution-2:

```sql
SELECT region, AVG(charges) AS average_charges_per_region
FROM insurance
GROUP BY region
ORDER BY region;
```

**Result:**

```text
┌───────────┬────────────────────────────┐
│  region   │ average_charges_per_region │
│  varchar  │           double           │
├───────────┼────────────────────────────┤
│ northeast │           13406.3845163858 │
│ northwest │         12417.575373969228 │
│ southeast │         15215.024430408172 │
│ southwest │              12554.8822234 │
└───────────┴────────────────────────────┘
```

### Q29. Find average BMI per gender

solution-1:

```sql
SELECT gender, AVG(bmi)
FROM insurance
GROUP BY gender
ORDER BY gender;
```

**Result:**

```text
┌─────────┬────────────────────┐
│ gender  │      avg(bmi)      │
│ varchar │       double       │
├─────────┼────────────────────┤
│ female  │ 30.345225618631762 │
│ male    │ 31.189249667994655 │
└─────────┴────────────────────┘
```

solution-2:

```sql
SELECT gender, AVG(bmi) AS avg_bmi_per_gender
FROM insurance
GROUP BY gender
ORDER BY gender;
```

**Result:**

```text
┌─────────┬────────────────────┐
│ gender  │ avg_bmi_per_gender │
│ varchar │       double       │
├─────────┼────────────────────┤
│ female  │ 30.345225618631762 │
│ male    │ 31.189249667994655 │
└─────────┴────────────────────┘
```

### Q30. Find total charges per region

solution-1:

```sql
SELECT region, SUM(charges)
FROM insurance
GROUP BY region
ORDER BY region;
```

**Result:**

```text
┌───────────┬────────────────────┐
│  region   │    sum(charges)    │
│  varchar  │       double       │
├───────────┼────────────────────┤
│ northeast │  4343668.583308999 │
│ northwest │ 4035711.9965399993 │
│ southeast │  6709825.773810004 │
│ southwest │      4394208.77819 │
└───────────┴────────────────────┘
```

solution-2:

```sql
SELECT region, SUM(charges) AS total_charges_per_region
FROM insurance
GROUP BY region
ORDER BY region;
```

**Result:**

```text
┌───────────┬──────────────────────────┐
│  region   │ total_charges_per_region │
│  varchar  │          double          │
├───────────┼──────────────────────────┤
│ northeast │        4343668.583308999 │
│ northwest │       4035711.9965399993 │
│ southeast │        6709825.773810004 │
│ southwest │            4394208.77819 │
└───────────┴──────────────────────────┘
```

### Q31. List all records where the person is a smoker, youngest first

```sql
SELECT *
FROM insurance
WHERE smoker = 'yes'
ORDER BY age ASC;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    18 │ female  │  27.28 │        3 │ yes     │ southeast │  18223.4512 │
│    18 │ male    │  31.68 │        2 │ yes     │ southeast │  34303.1672 │
│    18 │ male    │  31.73 │        0 │ yes     │ northeast │  33732.6867 │
│    18 │ female  │  36.85 │        0 │ yes     │ southeast │  36149.4835 │
│    18 │ male    │ 33.535 │        0 │ yes     │ northeast │ 34617.84065 │
│     · │  ·      │    ·   │        · │  ·      │     ·     │       ·     │
│     · │  ·      │    ·   │        · │  ·      │     ·     │       ·     │
│     · │  ·      │    ·   │        · │  ·      │     ·     │       ·     │
│    64 │ male    │  33.88 │        0 │ yes     │ southeast │  46889.2612 │
│    64 │ male    │  23.76 │        0 │ yes     │ southeast │  26926.5144 │
│    64 │ male    │  36.96 │        2 │ yes     │ southeast │  49577.6624 │
│    64 │ female  │   31.3 │        2 │ yes     │ southwest │   47291.055 │
│    64 │ female  │ 26.885 │        0 │ yes     │ northwest │ 29330.98315 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  305 rows (10 shown)      use .last to show entire result      7 columns
```

### Q32. Get the average BMI of all individuals, rounded to 2 decimals

```sql
SELECT ROUND(AVG(bmi), 2) AS average_bmi
FROM insurance;
```

**Result:**

```text
┌─────────────┐
│ average_bmi │
│   double    │
├─────────────┤
│       30.79 │
└─────────────┘
```

### Q33. Count how many individuals are from each region

```sql
SELECT region,
       COUNT(*) AS count
FROM insurance
GROUP BY region
ORDER BY region;
```

**Result:**

```text
┌───────────┬───────┐
│  region   │ count │
│  varchar  │ int64 │
├───────────┼───────┤
│ northeast │   324 │
│ northwest │   325 │
│ southeast │   441 │
│ southwest │   350 │
└───────────┴───────┘
```

### Q34. Find the maximum charges for a female individual

```sql
SELECT MAX(charges) AS max_female_charges
FROM insurance
WHERE gender = 'female';
```

**Result:**

```text
┌────────────────────┐
│ max_female_charges │
│       double       │
├────────────────────┤
│        63770.42801 │
└────────────────────┘
```

### Q35. Count the number of distinct regions

```sql
SELECT COUNT(DISTINCT region) AS number_of_regions
FROM insurance;
```

**Result:**

```text
┌───────────────────┐
│ number_of_regions │
│       int64       │
├───────────────────┤
│                 4 │
└───────────────────┘
```

### Q36. Find people from the southwest or northwest regions

solution-1:

```sql
SELECT *
FROM insurance
WHERE region IN ('southwest', 'northwest');
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    19 │ female  │   27.9 │        0 │ yes     │ southwest │   16884.924 │
│    33 │ male    │ 22.705 │        0 │ no      │ northwest │ 21984.47061 │
│    32 │ male    │  28.88 │        0 │ no      │ northwest │   3866.8552 │
│    37 │ female  │  27.74 │        3 │ no      │ northwest │   7281.5056 │
│    60 │ female  │  25.84 │        0 │ no      │ northwest │ 28923.13692 │
│     · │   ·     │     ·  │        · │ ·       │     ·     │       ·     │
│     · │   ·     │     ·  │        · │ ·       │     ·     │       ·     │
│     · │   ·     │     ·  │        · │ ·       │     ·     │       ·     │
│    19 │ female  │   34.7 │        2 │ yes     │ southwest │   36397.576 │
│    19 │ female  │   20.6 │        0 │ no      │ southwest │    1731.677 │
│    26 │ female  │   33.4 │        0 │ yes     │ southwest │ 19795.93733 │
│    56 │ female  │   44.7 │        3 │ yes     │ southwest │   31411.685 │
│    26 │ female  │   25.8 │        0 │ yes     │ southwest │   22007.945 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  675 rows (10 shown)      use .last to show entire result      7 columns
```

solution-2:

```sql
SELECT *
FROM insurance
WHERE (region = 'southwest') OR
      (region = 'northwest');
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    19 │ female  │   27.9 │        0 │ yes     │ southwest │   16884.924 │
│    33 │ male    │ 22.705 │        0 │ no      │ northwest │ 21984.47061 │
│    32 │ male    │  28.88 │        0 │ no      │ northwest │   3866.8552 │
│    37 │ female  │  27.74 │        3 │ no      │ northwest │   7281.5056 │
│    60 │ female  │  25.84 │        0 │ no      │ northwest │ 28923.13692 │
│     · │   ·     │     ·  │        · │ ·       │     ·     │       ·     │
│     · │   ·     │     ·  │        · │ ·       │     ·     │       ·     │
│     · │   ·     │     ·  │        · │ ·       │     ·     │       ·     │
│    19 │ female  │   34.7 │        2 │ yes     │ southwest │   36397.576 │
│    19 │ female  │   20.6 │        0 │ no      │ southwest │    1731.677 │
│    26 │ female  │   33.4 │        0 │ yes     │ southwest │ 19795.93733 │
│    56 │ female  │   44.7 │        3 │ yes     │ southwest │   31411.685 │
│    26 │ female  │   25.8 │        0 │ yes     │ southwest │   22007.945 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  675 rows (10 shown)      use .last to show entire result      7 columns
```

### Q37. Count people who are NOT from the southeast region

solution-1:

```sql
SELECT COUNT(*) AS not_southeast_count
FROM insurance
WHERE region <> 'southeast';
```

**Result:**

```text
┌─────────────────────┐
│ not_southeast_count │
│        int64        │
├─────────────────────┤
│                 999 │
└─────────────────────┘
```

solution-2:

```sql
SELECT COUNT(*) AS not_southeast_count
FROM insurance
WHERE region NOT IN ('southeast');
```

**Result:**

```text
┌─────────────────────┐
│ not_southeast_count │
│        int64        │
├─────────────────────┤
│                 999 │
└─────────────────────┘
```

### Q38. Find smokers aged 30 to 40, highest charges first

```sql
SELECT *
FROM insurance
WHERE (smoker = 'yes') AND
      (age BETWEEN 30 AND 40)
ORDER BY charges DESC;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    31 │ female  │ 38.095 │        1 │ yes     │ northeast │ 58571.07448 │
│    33 │ female  │  35.53 │        0 │ yes     │ northwest │ 55135.40209 │
│    30 │ male    │  35.53 │        0 │ yes     │ southeast │  46950.2567 │
│    37 │ female  │   47.6 │        2 │ yes     │ southwest │   46113.511 │
│    34 │ female  │  30.21 │        1 │ yes     │ northwest │  43943.8761 │
│     · │   ·     │     ·  │        · │  ·      │     ·     │       ·     │
│     · │   ·     │     ·  │        · │  ·      │     ·     │       ·     │
│     · │   ·     │     ·  │        · │  ·      │     ·     │       ·     │
│    32 │ female  │   24.6 │        0 │ yes     │ southwest │   17496.306 │
│    30 │ male    │  22.99 │        2 │ yes     │ northwest │  17361.7661 │
│    40 │ male    │   19.8 │        1 │ yes     │ southeast │   17179.522 │
│    33 │ female  │ 19.095 │        2 │ yes     │ northeast │ 16776.30405 │
│    38 │ male    │   19.3 │        0 │ yes     │ southwest │   15820.699 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  68 rows (10 shown)      use .last to show entire result       7 columns
```

### Q39. Find the average charges rounded to 2 decimal places

```sql
SELECT ROUND(AVG(charges), 2) AS avg_charges
FROM insurance;
```

**Result:**

```text
┌─────────────┐
│ avg_charges │
│   double    │
├─────────────┤
│    13530.15 │
└─────────────┘
```

### Q40. Count people by number of children

```sql
SELECT children,
       COUNT(*) AS num_people
FROM insurance
GROUP BY children
ORDER BY children;
```

**Result:**

```text
┌──────────┬────────────┐
│ children │ num_people │
│  int32   │   int64    │
├──────────┼────────────┤
│        0 │        624 │
│        1 │        346 │
│        2 │        257 │
│        3 │        167 │
│        4 │         27 │
│        5 │         19 │
└──────────┴────────────┘
```

### Q41. Count smokers and non-smokers for each gender

```sql
SELECT gender,
       smoker,
       COUNT(*) AS num_people
FROM insurance
GROUP BY gender, smoker
ORDER BY gender, smoker;
```

**Result:**

```text
┌─────────┬─────────┬────────────┐
│ gender  │ smoker  │ num_people │
│ varchar │ varchar │   int64    │
├─────────┼─────────┼────────────┤
│ female  │ no      │        564 │
│ female  │ yes     │        123 │
│ male    │ no      │        571 │
│ male    │ yes     │        182 │
└─────────┴─────────┴────────────┘
```

### Q42. Find regions with more than 350 people (HAVING)

```sql
SELECT region,
       COUNT(*) AS num_people
FROM insurance
GROUP BY region
HAVING COUNT(*) > 350
ORDER BY num_people DESC;
```

**Result:**

```text
┌───────────┬────────────┐
│  region   │ num_people │
│  varchar  │   int64    │
├───────────┼────────────┤
│ southeast │        441 │
└───────────┴────────────┘
```

### Q43. Find the minimum, maximum, and average age in one query

```sql
SELECT MIN(age)           AS min_age,
       MAX(age)           AS max_age,
       ROUND(AVG(age), 1) AS avg_age
FROM insurance;
```

**Result:**

```text
┌─────────┬─────────┬─────────┐
│ min_age │ max_age │ avg_age │
│  int32  │  int32  │ double  │
├─────────┼─────────┼─────────┤
│      18 │      64 │    39.2 │
└─────────┴─────────┴─────────┘
```

### Q44. Show each person's monthly charges (charges / 12) — first 10 rows

```sql
SELECT age,
       gender,
       charges,
       ROUND(charges / 12, 2) AS monthly_charges
FROM insurance
LIMIT 10;
```

**Result:**

```text
┌───────┬─────────┬─────────────┬─────────────────┐
│  age  │ gender  │   charges   │ monthly_charges │
│ int32 │ varchar │   double    │     double      │
├───────┼─────────┼─────────────┼─────────────────┤
│    19 │ female  │   16884.924 │         1407.08 │
│    18 │ male    │   1725.5523 │           143.8 │
│    28 │ male    │    4449.462 │          370.79 │
│    33 │ male    │ 21984.47061 │         1832.04 │
│    32 │ male    │   3866.8552 │          322.24 │
│    31 │ female  │   3756.6216 │          313.05 │
│    46 │ female  │   8240.5896 │          686.72 │
│    37 │ female  │   7281.5056 │          606.79 │
│    37 │ male    │   6406.4107 │          533.87 │
│    60 │ female  │ 28923.13692 │         2410.26 │
└───────┴─────────┴─────────────┴─────────────────┘
  10 rows                               4 columns
```

### Q45. Label each person with a BMI category (CASE)

BMI categories: under 18.5 = underweight, 18.5 to under 25 = normal,
25 to under 30 = overweight, 30 and above = obese.

```sql
SELECT age,
       gender,
       bmi,
       CASE
           WHEN bmi < 18.5 THEN 'underweight'
           WHEN bmi < 25   THEN 'normal'
           WHEN bmi < 30   THEN 'overweight'
           ELSE 'obese'
       END AS bmi_category
FROM insurance
LIMIT 10;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────────┐
│  age  │ gender  │  bmi   │ bmi_category │
│ int32 │ varchar │ double │   varchar    │
├───────┼─────────┼────────┼──────────────┤
│    19 │ female  │   27.9 │ overweight   │
│    18 │ male    │  33.77 │ obese        │
│    28 │ male    │   33.0 │ obese        │
│    33 │ male    │ 22.705 │ normal       │
│    32 │ male    │  28.88 │ overweight   │
│    31 │ female  │  25.74 │ overweight   │
│    46 │ female  │  33.44 │ obese        │
│    37 │ female  │  27.74 │ overweight   │
│    37 │ male    │  29.83 │ overweight   │
│    60 │ female  │  25.84 │ overweight   │
└───────┴─────────┴────────┴──────────────┘
  10 rows                       4 columns
```

### Q46. Find people from regions whose name starts with 'north' (LIKE)

```sql
SELECT *
FROM insurance
WHERE region LIKE 'north%';
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    33 │ male    │ 22.705 │        0 │ no      │ northwest │ 21984.47061 │
│    32 │ male    │  28.88 │        0 │ no      │ northwest │   3866.8552 │
│    37 │ female  │  27.74 │        3 │ no      │ northwest │   7281.5056 │
│    37 │ male    │  29.83 │        2 │ no      │ northeast │   6406.4107 │
│    60 │ female  │  25.84 │        0 │ no      │ northwest │ 28923.13692 │
│     · │   ·     │    ·   │        · │ ·       │     ·     │       ·     │
│     · │   ·     │    ·   │        · │ ·       │     ·     │       ·     │
│     · │   ·     │    ·   │        · │ ·       │     ·     │       ·     │
│    42 │ female  │  32.87 │        0 │ no      │ northeast │   7050.0213 │
│    23 │ female  │ 24.225 │        2 │ no      │ northeast │ 22395.74424 │
│    50 │ male    │  30.97 │        3 │ no      │ northwest │  10600.5483 │
│    18 │ female  │  31.92 │        0 │ no      │ northeast │   2205.9808 │
│    61 │ female  │  29.07 │        0 │ yes     │ northwest │  29141.3603 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  649 rows (10 shown)      use .last to show entire result      7 columns
```

### Q47. List people sorted by region (A–Z), then by charges (highest first) — first 10 rows

```sql
SELECT region, age, gender, charges
FROM insurance
ORDER BY region ASC, charges DESC
LIMIT 10;
```

**Result:**

```text
┌───────────┬───────┬─────────┬─────────────┐
│  region   │  age  │ gender  │   charges   │
│  varchar  │ int32 │ varchar │   double    │
├───────────┼───────┼─────────┼─────────────┤
│ northeast │    31 │ female  │ 58571.07448 │
│ northeast │    54 │ male    │ 48549.17835 │
│ northeast │    61 │ female  │ 48517.56315 │
│ northeast │    59 │ female  │ 47896.79135 │
│ northeast │    51 │ female  │  46255.1125 │
│ northeast │    62 │ male    │ 45710.20785 │
│ northeast │    51 │ female  │  44641.1974 │
│ northeast │    36 │ male    │ 43753.33705 │
│ northeast │    53 │ male    │ 43254.41795 │
│ northeast │    55 │ male    │ 42303.69215 │
└───────────┴───────┴─────────┴─────────────┘
  10 rows                         4 columns
```

### Q48. Show the 6th to 10th highest charges (LIMIT with OFFSET)

```sql
SELECT *
FROM insurance
ORDER BY charges DESC
LIMIT 5 OFFSET 5;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    54 │ male    │  34.21 │        2 │ yes     │ southeast │  54260.7499 │
│    60 │ male    │   32.8 │        0 │ yes     │ southwest │ 52590.82939 │
│    28 │ male    │   36.4 │        1 │ yes     │ southwest │ 51194.55914 │
│    64 │ male    │  33.88 │        0 │ yes     │ southeast │  49889.2612 │
│    64 │ male    │  36.96 │        2 │ yes     │ southeast │  49577.6624 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
```

### Q49. Find the total number of children covered by all policies

```sql
SELECT SUM(children) AS total_children
FROM insurance;
```

**Result:**

```text
┌────────────────┐
│ total_children │
│     int128     │
├────────────────┤
│           1564 │
└────────────────┘
```

### Q50. For smokers and non-smokers, show count, min, max, and average charges

```sql
SELECT smoker,
       COUNT(*)               AS num_people,
       ROUND(MIN(charges), 2) AS min_charges,
       ROUND(MAX(charges), 2) AS max_charges,
       ROUND(AVG(charges), 2) AS avg_charges
FROM insurance
GROUP BY smoker
ORDER BY smoker;
```

**Result:**

```text
┌─────────┬────────────┬─────────────┬─────────────┬─────────────┐
│ smoker  │ num_people │ min_charges │ max_charges │ avg_charges │
│ varchar │   int64    │   double    │   double    │   double    │
├─────────┼────────────┼─────────────┼─────────────┼─────────────┤
│ no      │       1135 │     1121.87 │    36910.61 │      8481.6 │
│ yes     │        305 │    12829.46 │    63770.43 │    32317.36 │
└─────────┴────────────┴─────────────┴─────────────┴─────────────┘
```
