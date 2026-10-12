# Insurance Table SQL Practice — Level 2 (Intermediate and Advanced)

	This lab continues Level 1 with GROUP BY,
	HAVING, CASE, sub-queries, CTEs (WITH),
	and window (ranking) functions.

	All queries and results in this file were
	validated with DuckDB v1.5.5.


## 1. Table Schema

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

Given the relational table `insurance` with the following 7 columns:

~~~
age,
gender,
bmi,
children,
smoker,
region,
charges
~~~

The sample records are (first line is header):

~~~
age gender  bmi    children  smoker region     charges
19  female  27.9    0         yes    southwest  16884.924
18  male    33.77   1         no     southeast  1725.5523
28  male    33      3         no     southeast  4449.462
~~~


## 2. Load Data into DuckDB

From the folder that contains `insurance_1440_records.csv`:

```bash
duckdb insurance_db.duckdb
```

Then, inside the DuckDB prompt, run the `CREATE TABLE` statement above, followed by:

```sql
COPY insurance FROM 'insurance_1440_records.csv' (HEADER true);
```

DuckDB tips used in this file:

* Without `ORDER BY`, DuckDB does **not** guarantee row order (especially
  after `GROUP BY` or window functions), so most queries end with `ORDER BY`.
* `QUALIFY` filters on window-function results (like `HAVING` does for
  aggregates) — a DuckDB feature that saves writing a sub-query.
* `COUNT(*) FILTER (WHERE ...)` is a compact form of conditional aggregation.
* In the results below, long outputs are truncated to 10 rows by the
  DuckDB CLI (`.maxrows 10`); the total row count is shown at the bottom.


## 3. Queries


### Q1. Find region with highest average charges

```sql
SELECT region, AVG(charges) AS avg_charges
FROM insurance
GROUP BY region
ORDER BY avg_charges DESC
LIMIT 1;
```

**Result:**

```text
┌───────────┬────────────────────┐
│  region   │    avg_charges     │
│  varchar  │       double       │
├───────────┼────────────────────┤
│ southeast │ 15215.024430408172 │
└───────────┴────────────────────┘
```


### Q2. Find gender with lowest average BMI

```sql
SELECT gender, AVG(bmi) AS avg_bmi
FROM insurance
GROUP BY gender
ORDER BY avg_bmi ASC
LIMIT 1;
```

**Result:**

```text
┌─────────┬────────────────────┐
│ gender  │      avg_bmi       │
│ varchar │       double       │
├─────────┼────────────────────┤
│ female  │ 30.345225618631762 │
└─────────┴────────────────────┘
```


### Q3. Rank regions by total charges

```sql
SELECT region,
       SUM(charges) AS total_charges,
       RANK() OVER (ORDER BY SUM(charges) DESC) AS rnk
FROM insurance
GROUP BY region
ORDER BY rnk;
```

**Result:**

```text
┌───────────┬────────────────────┬───────┐
│  region   │   total_charges    │  rnk  │
│  varchar  │       double       │ int64 │
├───────────┼────────────────────┼───────┤
│ southeast │  6709825.773810004 │     1 │
│ southwest │      4394208.77819 │     2 │
│ northeast │  4343668.583308999 │     3 │
│ northwest │ 4035711.9965399993 │     4 │
└───────────┴────────────────────┴───────┘
```


### Q4. Rank genders by average charges

```sql
SELECT gender,
       AVG(charges) AS avg_charges,
       DENSE_RANK() OVER (ORDER BY AVG(charges) DESC) AS rnk
FROM insurance
GROUP BY gender
ORDER BY rnk;
```

**Result:**

```text
┌─────────┬────────────────────┬───────┐
│ gender  │    avg_charges     │  rnk  │
│ varchar │       double       │ int64 │
├─────────┼────────────────────┼───────┤
│ male    │  14317.26401946878 │     1 │
│ female  │ 12667.416776112075 │     2 │
└─────────┴────────────────────┴───────┘
```


### Q5. Find top 3 regions with highest average BMI

```sql
SELECT region, AVG(bmi) AS avg_bmi
FROM insurance
GROUP BY region
ORDER BY avg_bmi DESC
LIMIT 3;
```

**Result:**

```text
┌───────────┬────────────────────┐
│  region   │      avg_bmi       │
│  varchar  │       double       │
├───────────┼────────────────────┤
│ southeast │  33.35494331065762 │
│ southwest │  30.51714285714284 │
│ northwest │ 29.199784615384626 │
└───────────┴────────────────────┘
```


### Q6. Find second highest charges

```sql
WITH ranked AS
(
  SELECT charges,
         DENSE_RANK() OVER (ORDER BY charges DESC) AS rnk
  FROM insurance
)
SELECT charges
FROM ranked
WHERE rnk = 2;
```

**Result:**

```text
┌─────────────┐
│   charges   │
│   double    │
├─────────────┤
│ 62592.87309 │
└─────────────┘
```


### Q7. Find smokers paying above average charges

```sql
SELECT *
FROM insurance
WHERE (smoker = 'yes') AND
      charges > (SELECT AVG(charges) FROM insurance);
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
  304 rows (10 shown)      use .last to show entire result      7 columns
```


### Q8. Find non-smokers paying below average charges

```sql
SELECT *
FROM insurance
WHERE (smoker = 'no') AND
      charges < (SELECT AVG(charges) FROM insurance);
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬───────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │  charges  │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │  double   │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼───────────┤
│    18 │ male    │  33.77 │        1 │ no      │ southeast │ 1725.5523 │
│    28 │ male    │   33.0 │        3 │ no      │ southeast │  4449.462 │
│    32 │ male    │  28.88 │        0 │ no      │ northwest │ 3866.8552 │
│    31 │ female  │  25.74 │        0 │ no      │ southeast │ 3756.6216 │
│    46 │ female  │  33.44 │        1 │ no      │ southeast │ 8240.5896 │
│     · │   ·     │     ·  │        · │ ·       │     ·     │      ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │      ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │      ·    │
│    57 │ female  │   30.5 │        0 │ no      │ southwest │  10704.47 │
│    24 │ female  │   33.3 │        0 │ no      │ southwest │  1880.487 │
│    38 │ female  │   25.9 │        1 │ no      │ southwest │  5472.449 │
│    29 │ female  │   20.8 │        1 │ no      │ southwest │  3208.787 │
│    19 │ female  │   20.6 │        0 │ no      │ southwest │  1731.677 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴───────────┘
  985 rows (10 shown)     use .last to show entire result     7 columns
```


### Q9. Find average charges by (gender, smoker)

```sql
SELECT gender, smoker, AVG(charges) AS avg_charges
FROM insurance
GROUP BY gender, smoker
ORDER BY gender, smoker;
```

**Result:**

```text
┌─────────┬─────────┬────────────────────┐
│ gender  │ smoker  │    avg_charges     │
│ varchar │ varchar │       double       │
├─────────┼─────────┼────────────────────┤
│ female  │ no      │  8761.186913225158 │
│ female  │ yes     │ 30578.909805934956 │
│ male    │ no      │  8205.448549597195 │
│ male    │ yes     │ 33492.245521098914 │
└─────────┴─────────┴────────────────────┘
```


### Q10. Find top 5 youngest people with highest charges

```sql
SELECT *
FROM insurance
ORDER BY age ASC, charges DESC
LIMIT 5;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    18 │ female  │  42.24 │        0 │ yes     │ southeast │  38792.6856 │
│    18 │ male    │  38.17 │        0 │ yes     │ southeast │  36307.7983 │
│    18 │ female  │  36.85 │        0 │ yes     │ southeast │  36149.4835 │
│    18 │ male    │ 33.535 │        0 │ yes     │ northeast │ 34617.84065 │
│    18 │ male    │  31.68 │        2 │ yes     │ southeast │  34303.1672 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
```


### Q11. Using SQL, find the charges for customers in the southwest and southeast regions

solution-1 (list the individual charges):

```sql
SELECT region, age, gender, charges
FROM insurance
WHERE region IN ('southwest', 'southeast')
ORDER BY region, charges DESC;
```

**Result:**

```text
┌───────────┬───────┬─────────┬─────────────┐
│  region   │  age  │ gender  │   charges   │
│  varchar  │ int32 │ varchar │   double    │
├───────────┼───────┼─────────┼─────────────┤
│ southeast │    54 │ female  │ 63770.42801 │
│ southeast │    45 │ male    │ 62592.87309 │
│ southeast │    54 │ male    │  54260.7499 │
│ southeast │    64 │ male    │  49889.2612 │
│ southeast │    64 │ male    │  49577.6624 │
│     ·     │     · │  ·      │        ·    │
│     ·     │     · │  ·      │        ·    │
│     ·     │     · │  ·      │        ·    │
│ southwest │    19 │ male    │    1253.936 │
│ southwest │    19 │ male    │    1252.407 │
│ southwest │    19 │ male    │    1242.816 │
│ southwest │    19 │ male    │     1242.26 │
│ southwest │    19 │ male    │    1241.565 │
└───────────┴───────┴─────────┴─────────────┘
  791 rows (10 shown)             4 columns
```

solution-2 (summarize the charges per region):

```sql
SELECT region,
       COUNT(*)               AS num_customers,
       ROUND(SUM(charges), 2) AS total_charges,
       ROUND(AVG(charges), 2) AS avg_charges
FROM insurance
WHERE region IN ('southwest', 'southeast')
GROUP BY region
ORDER BY region;
```

**Result:**

```text
┌───────────┬───────────────┬───────────────┬─────────────┐
│  region   │ num_customers │ total_charges │ avg_charges │
│  varchar  │     int64     │    double     │   double    │
├───────────┼───────────────┼───────────────┼─────────────┤
│ southeast │           441 │    6709825.77 │    15215.02 │
│ southwest │           350 │    4394208.78 │    12554.88 │
└───────────┴───────────────┴───────────────┴─────────────┘
```


### Q12. Using SQL, find the distribution of charges for customers in each region based on gender ('male', 'female')

```sql
SELECT region,
       gender,
       COUNT(*)               AS num_customers,
       ROUND(MIN(charges), 2) AS min_charges,
       ROUND(AVG(charges), 2) AS avg_charges,
       ROUND(MAX(charges), 2) AS max_charges,
       ROUND(SUM(charges), 2) AS total_charges
FROM insurance
WHERE gender IN ('male', 'female')
GROUP BY region, gender
ORDER BY region, gender;
```

**Result:**

```text
┌───────────┬─────────┬───────────────┬─────────────┬─────────────┬─────────────┬───────────────┐
│  region   │ gender  │ num_customers │ min_charges │ avg_charges │ max_charges │ total_charges │
│  varchar  │ varchar │     int64     │   double    │   double    │   double    │    double     │
├───────────┼─────────┼───────────────┼─────────────┼─────────────┼─────────────┼───────────────┤
│ northeast │ female  │           161 │     2196.47 │     12953.2 │    58571.07 │    2085465.71 │
│ northeast │ male    │           163 │      1694.8 │    13854.01 │    48549.18 │    2258202.88 │
│ northwest │ female  │           164 │     2117.34 │    12479.87 │     55135.4 │    2046698.75 │
│ northwest │ male    │           161 │     1621.34 │    12354.12 │     60021.4 │    1989013.25 │
│ southeast │ female  │           175 │     1607.51 │    13499.67 │    63770.43 │    2362442.12 │
│ southeast │ male    │           266 │     1121.87 │    16343.55 │    62592.87 │    4347383.66 │
│ southwest │ female  │           187 │     1727.79 │     11807.0 │    48824.45 │    2207908.76 │
│ southwest │ male    │           163 │     1241.57 │    13412.88 │    52590.83 │    2186300.02 │
└───────────┴─────────┴───────────────┴─────────────┴─────────────┴─────────────┴───────────────┘
```


### Q13. Using SQL, create the following result:

~~~
+-------------+----------------------------------------+
| age_group   | average_charge                         |
+-------------+----------------------------------------+
|  0-19       | average-charge for age_group of 0-19   |
|  20-40      | average-charge for age_group of 20-40  |
|  41-60      | average-charge for age_group of 41-60  |
|  61-70      | average-charge for age_group of 61-70  |
|  70+        | average-charge for age_group of 70+    |
+-------------+----------------------------------------+
~~~

Note: the oldest person in the data is 64, so no `70+` row appears.

```sql
SELECT
    CASE
        WHEN age BETWEEN 0  AND 19 THEN '0-19'
        WHEN age BETWEEN 20 AND 40 THEN '20-40'
        WHEN age BETWEEN 41 AND 60 THEN '41-60'
        WHEN age BETWEEN 61 AND 70 THEN '61-70'
        ELSE '70+'
    END AS age_group,
    AVG(charges) AS average_charge
FROM insurance
GROUP BY age_group
ORDER BY MIN(age);
```

**Result:**

```text
┌───────────┬────────────────────┐
│ age_group │   average_charge   │
│  varchar  │       double       │
├───────────┼────────────────────┤
│ 0-19      │   8527.97050374305 │
│ 20-40     │ 10881.277218881576 │
│ 41-60     │ 16124.050396247876 │
│ 61-70     │ 21641.466129696964 │
└───────────┴────────────────────┘
```


## 4. Ranking Functions and Sub-Queries


### Q14. Rank charges within each region

This query assigns a rank to each insurance charge within its respective region, ordered from highest to lowest.

```sql
SELECT
    age,
    gender,
    bmi,
    children,
    smoker,
    region,
    charges,
    RANK() OVER (PARTITION BY region ORDER BY charges DESC) AS region_charge_rank
FROM insurance
ORDER BY region, region_charge_rank;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┬────────────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │ region_charge_rank │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │       int64        │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┼────────────────────┤
│    31 │ female  │ 38.095 │        1 │ yes     │ northeast │ 58571.07448 │                  1 │
│    54 │ male    │ 40.565 │        3 │ yes     │ northeast │ 48549.17835 │                  2 │
│    61 │ female  │ 36.385 │        1 │ yes     │ northeast │ 48517.56315 │                  3 │
│    59 │ female  │ 36.765 │        1 │ yes     │ northeast │ 47896.79135 │                  4 │
│    51 │ female  │  37.05 │        3 │ yes     │ northeast │  46255.1125 │                  5 │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │                  · │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │                  · │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │                  · │
│    19 │ male    │   28.7 │        0 │ no      │ southwest │    1253.936 │                346 │
│    19 │ male    │   27.6 │        0 │ no      │ southwest │    1252.407 │                347 │
│    19 │ male    │   20.7 │        0 │ no      │ southwest │    1242.816 │                348 │
│    19 │ male    │   20.3 │        0 │ no      │ southwest │     1242.26 │                349 │
│    19 │ male    │   19.8 │        0 │ no      │ southwest │    1241.565 │                350 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┴────────────────────┘
  1440 rows (10 shown)                use .last to show entire result                8 columns
```

### Q15. Find the top 3 highest charges overall

This query first ranks all insurance charges from highest to lowest and then uses a CTE to select only the top 3 records.

```sql
WITH ranked_charges AS
(  SELECT
        age,
        gender,
        bmi,
        children,
        smoker,
        region,
        charges,
        RANK() OVER (ORDER BY charges DESC) AS overall_charge_rank
   FROM insurance
)
SELECT
    age,
    gender,
    bmi,
    children,
    smoker,
    region,
    charges,
    overall_charge_rank
FROM ranked_charges
WHERE overall_charge_rank <= 3
ORDER BY overall_charge_rank;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┬─────────────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │ overall_charge_rank │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │        int64        │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┼─────────────────────┤
│    54 │ female  │  47.41 │        0 │ yes     │ southeast │ 63770.42801 │                   1 │
│    45 │ male    │  30.36 │        0 │ yes     │ southeast │ 62592.87309 │                   2 │
│    52 │ male    │ 34.485 │        3 │ yes     │ northwest │ 60021.39897 │                   3 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┴─────────────────────┘
```

### Q16. Rank BMI within each smoking status

This query ranks individuals based on their BMI within their respective smoking categories (smoker or non-smoker).

```sql
SELECT
    age,
    gender,
    bmi,
    children,
    smoker,
    region,
    charges,
    DENSE_RANK() OVER (PARTITION BY smoker ORDER BY bmi DESC)
      AS smoker_bmi_rank
FROM insurance
ORDER BY smoker, smoker_bmi_rank;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┬─────────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │ smoker_bmi_rank │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │      int64      │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┼─────────────────┤
│    18 │ male    │  53.13 │        0 │ no      │ southeast │   1163.4627 │               1 │
│    23 │ male    │  50.38 │        1 │ no      │ southeast │   2438.0552 │               2 │
│    58 │ male    │  49.06 │        0 │ no      │ southeast │  11381.3254 │               3 │
│    58 │ male    │  49.06 │        0 │ no      │ southeast │  17381.3254 │               3 │
│    46 │ female  │  48.07 │        2 │ no      │ northeast │   9432.9253 │               4 │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │               · │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │               · │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │               · │
│    39 │ female  │   18.3 │        5 │ yes     │ southwest │    19023.26 │             213 │
│    27 │ female  │ 17.955 │        2 │ yes     │ northeast │ 15006.57945 │             214 │
│    32 │ female  │ 17.765 │        2 │ yes     │ northwest │  32734.1863 │             215 │
│    18 │ male    │  17.29 │        2 │ yes     │ northeast │  12829.4551 │             216 │
│    26 │ female  │ 17.195 │        2 │ yes     │ northeast │ 14455.64405 │             217 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┴─────────────────┘
  1440 rows (10 shown)              use .last to show entire result               8 columns
```

### Q17. Identify the charges that are in the top 50% within their region

This query uses the `NTILE` function to divide the charges within each region into two equal groups (50%). It then selects the records that fall into the first group (representing the top 50%).

```sql
SELECT
    age,
    gender,
    bmi,
    children,
    smoker,
    region,
    charges
FROM (
    SELECT
        age,
        gender,
        bmi,
        children,
        smoker,
        region,
        charges,
        NTILE(2) OVER (PARTITION BY region ORDER BY charges DESC) AS charge_half
    FROM insurance
) AS charge_groups
WHERE charge_half = 1
ORDER BY region, charges DESC;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    31 │ female  │ 38.095 │        1 │ yes     │ northeast │ 58571.07448 │
│    54 │ male    │ 40.565 │        3 │ yes     │ northeast │ 48549.17835 │
│    61 │ female  │ 36.385 │        1 │ yes     │ northeast │ 48517.56315 │
│    59 │ female  │ 36.765 │        1 │ yes     │ northeast │ 47896.79135 │
│    51 │ female  │  37.05 │        3 │ yes     │ northeast │  46255.1125 │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│     · │   ·     │     ·  │        · │ ·       │     ·     │        ·    │
│    45 │ female  │   25.7 │        3 │ no      │ southwest │    9101.798 │
│    46 │ female  │   25.7 │        3 │ no      │ southwest │    9101.798 │
│    48 │ male    │   30.2 │        2 │ no      │ southwest │     8968.33 │
│    50 │ female  │   25.6 │        0 │ no      │ southwest │    8932.084 │
│    46 │ female  │   30.2 │        2 │ no      │ southwest │    8825.086 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  721 rows (10 shown)      use .last to show entire result      7 columns
```


### Q18. Rank individuals by charges

This query assigns a rank to each individual based on
their `charges` in descending order.

```sql
SELECT
    age,
    gender,
    bmi,
    charges,
    RANK() OVER (ORDER BY charges DESC) AS rank_by_charges
FROM
    insurance
ORDER BY rank_by_charges;
```

**Result:**

```text
┌───────┬─────────┬────────┬─────────────┬─────────────────┐
│  age  │ gender  │  bmi   │   charges   │ rank_by_charges │
│ int32 │ varchar │ double │   double    │      int64      │
├───────┼─────────┼────────┼─────────────┼─────────────────┤
│    54 │ female  │  47.41 │ 63770.42801 │               1 │
│    45 │ male    │  30.36 │ 62592.87309 │               2 │
│    52 │ male    │ 34.485 │ 60021.39897 │               3 │
│    31 │ female  │ 38.095 │ 58571.07448 │               4 │
│    33 │ female  │  35.53 │ 55135.40209 │               5 │
│     · │  ·      │     ·  │        ·    │               · │
│     · │  ·      │     ·  │        ·    │               · │
│     · │  ·      │     ·  │        ·    │               · │
│    18 │ male    │   34.1 │    1137.011 │            1436 │
│    18 │ male    │  33.66 │   1136.3994 │            1437 │
│    18 │ male    │  33.33 │   1135.9407 │            1438 │
│    18 │ male    │  30.14 │   1131.5066 │            1439 │
│    18 │ male    │  23.21 │   1121.8739 │            1440 │
└───────┴─────────┴────────┴─────────────┴─────────────────┘
  1440 rows (10 shown)                           5 columns
```

### Q19. Find the top 3 most expensive charges for smokers

Using a sub-query, this identifies the top 3 most
expensive charges among smokers.

```sql
SELECT *
FROM (
    SELECT
        age,
        gender,
        bmi,
        charges,
        RANK() OVER (PARTITION BY smoker ORDER BY charges DESC) AS rank_by_smoker
    FROM
        insurance
    WHERE smoker = 'yes'
) ranked_smokers
WHERE rank_by_smoker <= 3
ORDER BY rank_by_smoker;
```

**Result:**

```text
┌───────┬─────────┬────────┬─────────────┬────────────────┐
│  age  │ gender  │  bmi   │   charges   │ rank_by_smoker │
│ int32 │ varchar │ double │   double    │     int64      │
├───────┼─────────┼────────┼─────────────┼────────────────┤
│    54 │ female  │  47.41 │ 63770.42801 │              1 │
│    45 │ male    │  30.36 │ 62592.87309 │              2 │
│    52 │ male    │ 34.485 │ 60021.39897 │              3 │
└───────┴─────────┴────────┴─────────────┴────────────────┘
```

### Q20. Average charges per region, ranked

This query calculates the average charges per region
and ranks the regions by average charges.

```sql
SELECT
    region,
    AVG(charges) AS avg_charges,
    DENSE_RANK() OVER (ORDER BY AVG(charges) DESC) AS rank_by_region
FROM
    insurance
GROUP BY
    region
ORDER BY rank_by_region;
```

**Result:**

```text
┌───────────┬────────────────────┬────────────────┐
│  region   │    avg_charges     │ rank_by_region │
│  varchar  │       double       │     int64      │
├───────────┼────────────────────┼────────────────┤
│ southeast │ 15215.024430408172 │              1 │
│ northeast │   13406.3845163858 │              2 │
│ southwest │      12554.8822234 │              3 │
│ northwest │ 12417.575373969228 │              4 │
└───────────┴────────────────────┴────────────────┘
```

### Q21. Find the oldest person in each region

Here, we use a sub-query to find the oldest person in each region.
Note: several people can share the maximum age in a region;
`ROW_NUMBER()` keeps just one of them (use `RANK()` to keep all ties).

```sql
SELECT
    region,
    age,
    gender,
    charges
FROM (
    SELECT
        region,
        age,
        gender,
        charges,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY age DESC, charges DESC) AS row_num
    FROM
        insurance
) ranked_by_region
WHERE
    row_num = 1
ORDER BY region;
```

**Result:**

```text
┌───────────┬───────┬─────────┬─────────────┐
│  region   │  age  │ gender  │   charges   │
│  varchar  │ int32 │ varchar │   double    │
├───────────┼───────┼─────────┼─────────────┤
│ northeast │    64 │ female  │ 16069.08475 │
│ northwest │    64 │ male    │ 30166.61817 │
│ southeast │    64 │ male    │  49889.2612 │
│ southwest │    64 │ female  │    47928.03 │
└───────────┴───────┴─────────┴─────────────┘
```


### Q22. Find the average charges grouped by smoker status and gender

```sql
SELECT smoker,
       gender,
       AVG(charges) AS avg_charges
FROM insurance
GROUP BY smoker, gender
ORDER BY smoker, gender;
```

**Result:**

```text
┌─────────┬─────────┬────────────────────┐
│ smoker  │ gender  │    avg_charges     │
│ varchar │ varchar │       double       │
├─────────┼─────────┼────────────────────┤
│ no      │ female  │  8761.186913225158 │
│ no      │ male    │  8205.448549597195 │
│ yes     │ female  │ 30578.909805934956 │
│ yes     │ male    │ 33492.245521098914 │
└─────────┴─────────┴────────────────────┘
```

### Q23. List individuals whose charges are above the overall average

```sql
SELECT *
FROM insurance
WHERE charges > (SELECT AVG(charges) FROM insurance);
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    19 │ female  │   27.9 │        0 │ yes     │ southwest │   16884.924 │
│    33 │ male    │ 22.705 │        0 │ no      │ northwest │ 21984.47061 │
│    60 │ female  │  25.84 │        0 │ no      │ northwest │ 28923.13692 │
│    62 │ female  │  26.29 │        0 │ yes     │ southeast │  27808.7251 │
│    27 │ male    │  42.13 │        0 │ yes     │ southeast │  39611.7577 │
│     · │  ·      │     ·  │        · │  ·      │     ·     │       ·     │
│     · │  ·      │     ·  │        · │  ·      │     ·     │       ·     │
│     · │  ·      │     ·  │        · │  ·      │     ·     │       ·     │
│    28 │ female  │   30.2 │        0 │ yes     │ southwest │   38900.653 │
│    19 │ female  │   34.7 │        2 │ yes     │ southwest │   36397.576 │
│    26 │ female  │   33.4 │        0 │ yes     │ southwest │ 19795.93733 │
│    56 │ female  │   44.7 │        3 │ yes     │ southwest │   31411.685 │
│    26 │ female  │   25.8 │        0 │ yes     │ southwest │   22007.945 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
  454 rows (10 shown)      use .last to show entire result      7 columns
```

### Q24. Get the number of children per smoker group

```sql
SELECT smoker, SUM(children) AS total_children
FROM insurance
GROUP BY smoker
ORDER BY smoker;
```

**Result:**

```text
┌─────────┬────────────────┐
│ smoker  │ total_children │
│ varchar │     int128     │
├─────────┼────────────────┤
│ no      │           1227 │
│ yes     │            337 │
└─────────┴────────────────┘
```

### Q25. List all individuals who have the highest charges in their region (correlated sub-query)

```sql
SELECT *
FROM insurance i
WHERE charges = (
  SELECT MAX(charges)
  FROM insurance
  WHERE region = i.region
)
ORDER BY region;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    31 │ female  │ 38.095 │        1 │ yes     │ northeast │ 58571.07448 │
│    52 │ male    │ 34.485 │        3 │ yes     │ northwest │ 60021.39897 │
│    54 │ female  │  47.41 │        0 │ yes     │ southeast │ 63770.42801 │
│    60 │ male    │   32.8 │        0 │ yes     │ southwest │ 52590.82939 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘
```

---

## 🔶 Complex Queries

### Q26. Rank individuals within each region based on their charges (highest to lowest)

```sql
SELECT *,
       RANK() OVER (PARTITION BY region ORDER BY charges DESC)
        AS charge_rank
FROM insurance
ORDER BY region, charge_rank;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │ charge_rank │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │    int64    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┼─────────────┤
│    31 │ female  │ 38.095 │        1 │ yes     │ northeast │ 58571.07448 │           1 │
│    54 │ male    │ 40.565 │        3 │ yes     │ northeast │ 48549.17835 │           2 │
│    61 │ female  │ 36.385 │        1 │ yes     │ northeast │ 48517.56315 │           3 │
│    59 │ female  │ 36.765 │        1 │ yes     │ northeast │ 47896.79135 │           4 │
│    51 │ female  │  37.05 │        3 │ yes     │ northeast │  46255.1125 │           5 │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │           · │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │           · │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │           · │
│    19 │ male    │   28.7 │        0 │ no      │ southwest │    1253.936 │         346 │
│    19 │ male    │   27.6 │        0 │ no      │ southwest │    1252.407 │         347 │
│    19 │ male    │   20.7 │        0 │ no      │ southwest │    1242.816 │         348 │
│    19 │ male    │   20.3 │        0 │ no      │ southwest │     1242.26 │         349 │
│    19 │ male    │   19.8 │        0 │ no      │ southwest │    1241.565 │         350 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┴─────────────┘
  1440 rows (10 shown)            use .last to show entire result             8 columns
```

### Q27. Find the top 3 individuals with the highest charges in each region

```sql
SELECT *
FROM (
  SELECT *,
         RANK() OVER (PARTITION BY region ORDER BY charges DESC)
           AS rnk
  FROM insurance
) ranked
WHERE rnk <= 3
ORDER BY region, rnk;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┬───────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │  rnk  │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │ int64 │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┼───────┤
│    31 │ female  │ 38.095 │        1 │ yes     │ northeast │ 58571.07448 │     1 │
│    54 │ male    │ 40.565 │        3 │ yes     │ northeast │ 48549.17835 │     2 │
│    61 │ female  │ 36.385 │        1 │ yes     │ northeast │ 48517.56315 │     3 │
│    52 │ male    │ 34.485 │        3 │ yes     │ northwest │ 60021.39897 │     1 │
│    33 │ female  │  35.53 │        0 │ yes     │ northwest │ 55135.40209 │     2 │
│    58 │ male    │ 36.955 │        2 │ yes     │ northwest │ 47496.49445 │     3 │
│    54 │ female  │  47.41 │        0 │ yes     │ southeast │ 63770.42801 │     1 │
│    45 │ male    │  30.36 │        0 │ yes     │ southeast │ 62592.87309 │     2 │
│    54 │ male    │  34.21 │        2 │ yes     │ southeast │  54260.7499 │     3 │
│    60 │ male    │   32.8 │        0 │ yes     │ southwest │ 52590.82939 │     1 │
│    28 │ male    │   36.4 │        1 │ yes     │ southwest │ 51194.55914 │     2 │
│    63 │ female  │   37.7 │        0 │ yes     │ southwest │    48824.45 │     3 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┴───────┘
  12 rows                                                               8 columns
```

### Q28. Calculate the average charges for individuals grouped by age group: `<30`, `30–50`, and `>50`

```sql
SELECT age_group, AVG(charges) AS avg_charge
FROM (
  SELECT *,
         CASE
           WHEN age < 30 THEN '<30'
           WHEN age BETWEEN 30 AND 50 THEN '30-50'
           ELSE '>50'
         END AS age_group
  FROM insurance
) age_groups
GROUP BY age_group
ORDER BY MIN(age);
```

**Result:**

```text
┌───────────┬────────────────────┐
│ age_group │     avg_charge     │
│  varchar  │       double       │
├───────────┼────────────────────┤
│ <30       │  9438.231524192048 │
│ 30-50     │ 13459.589475174125 │
│ >50       │ 18468.134890260404 │
└───────────┴────────────────────┘
```

### Q29. List individuals who pay more than the average charge for their age group

```sql
SELECT *
FROM (
  SELECT *,
         AVG(charges) OVER (PARTITION BY
           CASE
             WHEN age < 30 THEN '<30'
             WHEN age BETWEEN 30 AND 50 THEN '30-50'
             ELSE '>50'
           END
         ) AS avg_group_charge
  FROM insurance
) grouped
WHERE charges > avg_group_charge
ORDER BY age, charges DESC;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┬────────────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │  avg_group_charge  │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │       double       │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┼────────────────────┤
│    18 │ female  │  42.24 │        0 │ yes     │ southeast │  38792.6856 │  9438.231524192048 │
│    18 │ male    │  38.17 │        0 │ yes     │ southeast │  36307.7983 │  9438.231524192048 │
│    18 │ female  │  36.85 │        0 │ yes     │ southeast │  36149.4835 │  9438.231524192048 │
│    18 │ male    │ 33.535 │        0 │ yes     │ northeast │ 34617.84065 │  9438.231524192048 │
│    18 │ male    │  31.68 │        2 │ yes     │ southeast │  34303.1672 │  9438.231524192048 │
│     · │  ·      │    ·   │        · │  ·      │     ·     │       ·     │          ·         │
│     · │  ·      │    ·   │        · │  ·      │     ·     │       ·     │          ·         │
│     · │  ·      │    ·   │        · │  ·      │     ·     │       ·     │          ·         │
│    64 │ male    │  33.88 │        0 │ yes     │ southeast │  46889.2612 │ 18468.134890260404 │
│    64 │ male    │   24.7 │        1 │ no      │ northwest │ 30166.61817 │ 18468.134890260404 │
│    64 │ female  │ 26.885 │        0 │ yes     │ northwest │ 29330.98315 │ 18468.134890260404 │
│    64 │ female  │  22.99 │        0 │ yes     │ southeast │  27037.9141 │ 18468.134890260404 │
│    64 │ male    │  23.76 │        0 │ yes     │ southeast │  26926.5144 │ 18468.134890260404 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┴────────────────────┘
  410 rows (10 shown)                use .last to show entire result                 8 columns
```

### Q30. Find each region's share (percentage) of total charges

A window function over an aggregate: `SUM(SUM(charges)) OVER ()` is the grand total.

```sql
SELECT region,
       ROUND(SUM(charges), 2) AS total_charges,
       ROUND(100.0 * SUM(charges) / SUM(SUM(charges)) OVER (), 2) AS pct_of_total
FROM insurance
GROUP BY region
ORDER BY pct_of_total DESC;
```

**Result:**

```text
┌───────────┬───────────────┬──────────────┐
│  region   │ total_charges │ pct_of_total │
│  varchar  │    double     │    double    │
├───────────┼───────────────┼──────────────┤
│ southeast │    6709825.77 │        34.44 │
│ southwest │    4394208.78 │        22.55 │
│ northeast │    4343668.58 │        22.29 │
│ northwest │     4035712.0 │        20.71 │
└───────────┴───────────────┴──────────────┘
```

### Q31. Count smokers and non-smokers in each region, and the smoker percentage (FILTER)

```sql
SELECT region,
       COUNT(*)                                  AS total,
       COUNT(*) FILTER (WHERE smoker = 'yes')    AS smokers,
       COUNT(*) FILTER (WHERE smoker = 'no')     AS non_smokers,
       ROUND(100.0 * COUNT(*) FILTER (WHERE smoker = 'yes') / COUNT(*), 2)
                                                 AS smoker_pct
FROM insurance
GROUP BY region
ORDER BY smoker_pct DESC;
```

**Result:**

```text
┌───────────┬───────┬─────────┬─────────────┬────────────┐
│  region   │ total │ smokers │ non_smokers │ smoker_pct │
│  varchar  │ int64 │  int64  │    int64    │   double   │
├───────────┼───────┼─────────┼─────────────┼────────────┤
│ southeast │   441 │     114 │         327 │      25.85 │
│ northeast │   324 │      67 │         257 │      20.68 │
│ southwest │   350 │      66 │         284 │      18.86 │
│ northwest │   325 │      58 │         267 │      17.85 │
└───────────┴───────┴─────────┴─────────────┴────────────┘
```

### Q32. Find the median charges for smokers and non-smokers

solution-1 (DuckDB `MEDIAN`):

```sql
SELECT smoker,
       MEDIAN(charges)        AS median_charges,
       ROUND(AVG(charges), 2) AS avg_charges
FROM insurance
GROUP BY smoker
ORDER BY smoker;
```

**Result:**

```text
┌─────────┬────────────────┬─────────────┐
│ smoker  │ median_charges │ avg_charges │
│ varchar │     double     │   double    │
├─────────┼────────────────┼─────────────┤
│ no      │      7345.7266 │      8481.6 │
│ yes     │    34617.84065 │    32317.36 │
└─────────┴────────────────┴─────────────┘
```

solution-2 (standard SQL `PERCENTILE_CONT`):

```sql
SELECT smoker,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY charges) AS median_charges
FROM insurance
GROUP BY smoker
ORDER BY smoker;
```

**Result:**

```text
┌─────────┬────────────────┐
│ smoker  │ median_charges │
│ varchar │     double     │
├─────────┼────────────────┤
│ no      │      7345.7266 │
│ yes     │    34617.84065 │
└─────────┴────────────────┘
```

### Q33. Find the 2 highest charges for each gender (QUALIFY)

solution-1 (DuckDB `QUALIFY`):

```sql
SELECT gender, age, smoker, region, charges,
       ROW_NUMBER() OVER (PARTITION BY gender ORDER BY charges DESC) AS rn
FROM insurance
QUALIFY rn <= 2
ORDER BY gender, rn;
```

**Result:**

```text
┌─────────┬───────┬─────────┬───────────┬─────────────┬───────┐
│ gender  │  age  │ smoker  │  region   │   charges   │  rn   │
│ varchar │ int32 │ varchar │  varchar  │   double    │ int64 │
├─────────┼───────┼─────────┼───────────┼─────────────┼───────┤
│ female  │    54 │ yes     │ southeast │ 63770.42801 │     1 │
│ female  │    31 │ yes     │ northeast │ 58571.07448 │     2 │
│ male    │    45 │ yes     │ southeast │ 62592.87309 │     1 │
│ male    │    52 │ yes     │ northwest │ 60021.39897 │     2 │
└─────────┴───────┴─────────┴───────────┴─────────────┴───────┘
```

solution-2 (sub-query, works in any SQL database):

```sql
SELECT *
FROM (
  SELECT gender, age, smoker, region, charges,
         ROW_NUMBER() OVER (PARTITION BY gender ORDER BY charges DESC) AS rn
  FROM insurance
) t
WHERE rn <= 2
ORDER BY gender, rn;
```

**Result:**

```text
┌─────────┬───────┬─────────┬───────────┬─────────────┬───────┐
│ gender  │  age  │ smoker  │  region   │   charges   │  rn   │
│ varchar │ int32 │ varchar │  varchar  │   double    │ int64 │
├─────────┼───────┼─────────┼───────────┼─────────────┼───────┤
│ female  │    54 │ yes     │ southeast │ 63770.42801 │     1 │
│ female  │    31 │ yes     │ northeast │ 58571.07448 │     2 │
│ male    │    45 │ yes     │ southeast │ 62592.87309 │     1 │
│ male    │    52 │ yes     │ northwest │ 60021.39897 │     2 │
└─────────┴───────┴─────────┴───────────┴─────────────┴───────┘
```

### Q34. Running total of charges by age

First aggregate per age, then compute a cumulative sum with a window frame.

```sql
SELECT age,
       ROUND(SUM(charges), 2) AS total_charges,
       ROUND(SUM(SUM(charges)) OVER (ORDER BY age
             ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_total
FROM insurance
GROUP BY age
ORDER BY age;
```

**Result:**

```text
┌───────┬───────────────┬───────────────┐
│  age  │ total_charges │ running_total │
│ int32 │    double     │    double     │
├───────┼───────────────┼───────────────┤
│    18 │     493255.31 │     493255.31 │
│    19 │     734772.44 │    1228027.75 │
│    20 │     358250.22 │    1586277.97 │
│    21 │     170901.14 │    1757179.11 │
│    22 │     280362.12 │    2037541.23 │
│     · │         ·     │         ·     │
│     · │         ·     │         ·     │
│     · │         ·     │         ·     │
│    60 │     571499.64 │   17340909.99 │
│    61 │     565719.24 │   17906629.22 │
│    62 │     468769.69 │   18375398.91 │
│    63 │     517815.89 │    18893214.8 │
│    64 │     590200.34 │   19483415.13 │
└───────┴───────────────┴───────────────┘
  47 rows (10 shown)          3 columns
```

### Q35. Compare the average charges of each age with the previous age (LAG)

```sql
WITH by_age AS (
  SELECT age, AVG(charges) AS avg_charges
  FROM insurance
  GROUP BY age
)
SELECT age,
       ROUND(avg_charges, 2)                                AS avg_charges,
       ROUND(LAG(avg_charges) OVER (ORDER BY age), 2)       AS prev_age_avg,
       ROUND(avg_charges - LAG(avg_charges) OVER (ORDER BY age), 2) AS change
FROM by_age
ORDER BY age;
```

**Result:**

```text
┌───────┬─────────────┬──────────────┬──────────┐
│  age  │ avg_charges │ prev_age_avg │  change  │
│ int32 │   double    │    double    │  double  │
├───────┼─────────────┼──────────────┼──────────┤
│    18 │     6850.77 │         NULL │     NULL │
│    19 │    10205.17 │      6850.77 │   3354.4 │
│    20 │    11195.32 │     10205.17 │   990.15 │
│    21 │     5512.94 │     11195.32 │ -5682.38 │
│    22 │    10012.93 │      5512.94 │  4499.99 │
│     · │        ·    │         ·    │     ·    │
│     · │        ·    │         ·    │     ·    │
│     · │        ·    │         ·    │     ·    │
│    60 │    21980.76 │      18214.1 │  3766.66 │
│    61 │    22628.77 │     21980.76 │   648.01 │
│    62 │    19532.07 │     22628.77 │  -3096.7 │
│    63 │    20712.64 │     19532.07 │  1180.57 │
│    64 │    23608.01 │     20712.64 │  2895.38 │
└───────┴─────────────┴──────────────┴──────────┘
  47 rows (10 shown)                  4 columns
```

### Q36. Split people into 4 quartiles by charges and summarize each quartile (NTILE)

```sql
WITH q AS (
  SELECT *,
         NTILE(4) OVER (ORDER BY charges) AS charge_quartile
  FROM insurance
)
SELECT charge_quartile,
       COUNT(*)                                AS num_people,
       ROUND(MIN(charges), 2)                  AS min_charges,
       ROUND(MAX(charges), 2)                  AS max_charges,
       COUNT(*) FILTER (WHERE smoker = 'yes')  AS smokers
FROM q
GROUP BY charge_quartile
ORDER BY charge_quartile;
```

**Result:**

```text
┌─────────────────┬────────────┬─────────────┬─────────────┬─────────┐
│ charge_quartile │ num_people │ min_charges │ max_charges │ smokers │
│      int64      │   int64    │   double    │   double    │  int64  │
├─────────────────┼────────────┼─────────────┼─────────────┼─────────┤
│               1 │        360 │     1121.87 │     4719.52 │       0 │
│               2 │        360 │     4719.74 │     9487.64 │       0 │
│               3 │        360 │     9500.57 │    17496.31 │      31 │
│               4 │        360 │    17560.38 │    63770.43 │     274 │
└─────────────────┴────────────┴─────────────┴─────────────┴─────────┘
```

### Q37. For each region, compare smokers' and non-smokers' average charges (CTE + conditional aggregation)

```sql
WITH region_avgs AS (
  SELECT region,
         AVG(charges) FILTER (WHERE smoker = 'yes') AS avg_smoker,
         AVG(charges) FILTER (WHERE smoker = 'no')  AS avg_non_smoker
  FROM insurance
  GROUP BY region
)
SELECT region,
       ROUND(avg_smoker, 2)                  AS avg_smoker,
       ROUND(avg_non_smoker, 2)              AS avg_non_smoker,
       ROUND(avg_smoker / avg_non_smoker, 2) AS smoker_ratio
FROM region_avgs
ORDER BY smoker_ratio DESC;
```

**Result:**

```text
┌───────────┬────────────┬────────────────┬──────────────┐
│  region   │ avg_smoker │ avg_non_smoker │ smoker_ratio │
│  varchar  │   double   │     double     │    double    │
├───────────┼────────────┼────────────────┼──────────────┤
│ southeast │   35200.04 │        8247.77 │         4.27 │
│ southwest │    31889.8 │        8061.56 │         3.96 │
│ northwest │    30192.0 │        8556.46 │         3.53 │
│ northeast │   29673.54 │        9165.53 │         3.24 │
└───────────┴────────────┴────────────────┴──────────────┘
```

### Q38. Show how much each person's charges differ from their region's average

```sql
SELECT region, age, gender, smoker,
       charges,
       ROUND(AVG(charges) OVER (PARTITION BY region), 2)           AS region_avg,
       ROUND(charges - AVG(charges) OVER (PARTITION BY region), 2) AS diff_from_region_avg
FROM insurance
ORDER BY diff_from_region_avg DESC;
```

**Result:**

```text
┌───────────┬───────┬─────────┬─────────┬─────────────┬────────────┬──────────────────────┐
│  region   │  age  │ gender  │ smoker  │   charges   │ region_avg │ diff_from_region_avg │
│  varchar  │ int32 │ varchar │ varchar │   double    │   double   │        double        │
├───────────┼───────┼─────────┼─────────┼─────────────┼────────────┼──────────────────────┤
│ southeast │    54 │ female  │ yes     │ 63770.42801 │   15215.02 │              48555.4 │
│ northwest │    52 │ male    │ yes     │ 60021.39897 │   12417.58 │             47603.82 │
│ southeast │    45 │ male    │ yes     │ 62592.87309 │   15215.02 │             47377.85 │
│ northeast │    31 │ female  │ yes     │ 58571.07448 │   13406.38 │             45164.69 │
│ northwest │    33 │ female  │ yes     │ 55135.40209 │   12417.58 │             42717.83 │
│     ·     │     · │  ·      │ ·       │        ·    │       ·    │                 ·    │
│     ·     │     · │  ·      │ ·       │        ·    │       ·    │                 ·    │
│     ·     │     · │  ·      │ ·       │        ·    │       ·    │                 ·    │
│ southeast │    18 │ male    │ no      │    1137.011 │   15215.02 │            -14078.01 │
│ southeast │    18 │ male    │ no      │   1136.3994 │   15215.02 │            -14078.63 │
│ southeast │    18 │ male    │ no      │   1135.9407 │   15215.02 │            -14079.08 │
│ southeast │    18 │ male    │ no      │   1131.5066 │   15215.02 │            -14083.52 │
│ southeast │    18 │ male    │ no      │   1121.8739 │   15215.02 │            -14093.15 │
└───────────┴───────┴─────────┴─────────┴─────────────┴────────────┴──────────────────────┘
  1440 rows (10 shown)             use .last to show entire result              7 columns
```

### Q39. Subtotals by region and smoker status, with region totals and a grand total (ROLLUP)

`NULL` in the result marks a subtotal row (all smokers of that region) or the grand total.

```sql
SELECT region,
       smoker,
       COUNT(*)               AS num_people,
       ROUND(SUM(charges), 2) AS total_charges
FROM insurance
GROUP BY ROLLUP (region, smoker)
ORDER BY region NULLS LAST, smoker NULLS LAST;
```

**Result:**

```text
┌───────────┬─────────┬────────────┬───────────────┐
│  region   │ smoker  │ num_people │ total_charges │
│  varchar  │ varchar │   int64    │    double     │
├───────────┼─────────┼────────────┼───────────────┤
│ northeast │ no      │        257 │    2355541.64 │
│ northeast │ yes     │         67 │    1988126.94 │
│ northeast │ NULL    │        324 │    4343668.58 │
│ northwest │ no      │        267 │    2284575.81 │
│ northwest │ yes     │         58 │    1751136.18 │
│ northwest │ NULL    │        325 │     4035712.0 │
│ southeast │ no      │        327 │    2697021.33 │
│ southeast │ yes     │        114 │    4012804.45 │
│ southeast │ NULL    │        441 │    6709825.77 │
│ southwest │ no      │        284 │    2289481.76 │
│ southwest │ yes     │         66 │    2104727.02 │
│ southwest │ NULL    │        350 │    4394208.78 │
│ NULL      │ NULL    │       1440 │   19483415.13 │
└───────────┴─────────┴────────────┴───────────────┘
  13 rows                                4 columns
```

### Q40. Build a region × smoker table of average charges (PIVOT)

solution-1 (DuckDB `PIVOT`):

```sql
PIVOT insurance
ON smoker
USING ROUND(AVG(charges), 2)
GROUP BY region
ORDER BY region;
```

**Result:**

```text
┌───────────┬─────────┬──────────┐
│  region   │   no    │   yes    │
│  varchar  │ double  │  double  │
├───────────┼─────────┼──────────┤
│ northeast │ 9165.53 │ 29673.54 │
│ northwest │ 8556.46 │  30192.0 │
│ southeast │ 8247.77 │ 35200.04 │
│ southwest │ 8061.56 │  31889.8 │
└───────────┴─────────┴──────────┘
```

solution-2 (standard SQL with `CASE`):

```sql
SELECT region,
       ROUND(AVG(CASE WHEN smoker = 'no'  THEN charges END), 2) AS "no",
       ROUND(AVG(CASE WHEN smoker = 'yes' THEN charges END), 2) AS "yes"
FROM insurance
GROUP BY region
ORDER BY region;
```

**Result:**

```text
┌───────────┬─────────┬──────────┐
│  region   │   no    │   yes    │
│  varchar  │ double  │  double  │
├───────────┼─────────┼──────────┤
│ northeast │ 9165.53 │ 29673.54 │
│ northwest │ 8556.46 │  30192.0 │
│ southeast │ 8247.77 │ 35200.04 │
│ southwest │ 8061.56 │  31889.8 │
└───────────┴─────────┴──────────┘
```

### Q41. Find duplicate records (rows that appear more than once)

```sql
SELECT age, gender, bmi, children, smoker, region, charges,
       COUNT(*) AS num_copies
FROM insurance
GROUP BY age, gender, bmi, children, smoker, region, charges
HAVING COUNT(*) > 1
ORDER BY num_copies DESC, charges DESC;
```

**Result:**

```text
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┬────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │ num_copies │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │   int64    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┼────────────┤
│    63 │ male    │  35.09 │        0 │ yes     │ southeast │  47055.5321 │          2 │
│    61 │ male    │  35.86 │        0 │ yes     │ southeast │  46599.1084 │          2 │
│    46 │ male    │  42.35 │        3 │ yes     │ southeast │  46151.1245 │          2 │
│    25 │ male    │  45.54 │        2 │ yes     │ southeast │  42112.2356 │          2 │
│    42 │ male    │  26.07 │        1 │ yes     │ southeast │ 38245.59327 │          2 │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │          · │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │          · │
│     · │  ·      │     ·  │        · │ ·       │     ·     │        ·    │          · │
│    19 │ female  │   20.6 │        0 │ no      │ southwest │    1731.677 │          2 │
│    18 │ male    │  29.37 │        1 │ no      │ southeast │   1719.4363 │          2 │
│    19 │ male    │  30.59 │        0 │ no      │ northwest │   1639.5631 │          2 │
│    20 │ male    │  33.33 │        0 │ no      │ southeast │   1391.5287 │          2 │
│    18 │ male    │  34.43 │        0 │ no      │ southeast │   1137.4697 │          2 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┴────────────┘
  52 rows (10 shown)             use .last to show entire result             8 columns
```

### Q42. For each region, find the age and BMI of the person with the highest charges (ARG_MAX)

solution-1 (DuckDB `ARG_MAX(value, ordering_column)`):

```sql
SELECT region,
       MAX(charges)          AS max_charges,
       ARG_MAX(age, charges) AS age_of_max,
       ARG_MAX(bmi, charges) AS bmi_of_max
FROM insurance
GROUP BY region
ORDER BY region;
```

**Result:**

```text
┌───────────┬─────────────┬────────────┬────────────┐
│  region   │ max_charges │ age_of_max │ bmi_of_max │
│  varchar  │   double    │   int32    │   double   │
├───────────┼─────────────┼────────────┼────────────┤
│ northeast │ 58571.07448 │         31 │     38.095 │
│ northwest │ 60021.39897 │         52 │     34.485 │
│ southeast │ 63770.42801 │         54 │      47.41 │
│ southwest │ 52590.82939 │         60 │       32.8 │
└───────────┴─────────────┴────────────┴────────────┘
```

solution-2 (`QUALIFY` with `ROW_NUMBER`):

```sql
SELECT region, charges AS max_charges, age AS age_of_max, bmi AS bmi_of_max
FROM insurance
QUALIFY ROW_NUMBER() OVER (PARTITION BY region ORDER BY charges DESC) = 1
ORDER BY region;
```

**Result:**

```text
┌───────────┬─────────────┬────────────┬────────────┐
│  region   │ max_charges │ age_of_max │ bmi_of_max │
│  varchar  │   double    │   int32    │   double   │
├───────────┼─────────────┼────────────┼────────────┤
│ northeast │ 58571.07448 │         31 │     38.095 │
│ northwest │ 60021.39897 │         52 │     34.485 │
│ southeast │ 63770.42801 │         54 │      47.41 │
│ southwest │ 52590.82939 │         60 │       32.8 │
└───────────┴─────────────┴────────────┴────────────┘
```

### Q43. Measure how strongly age, BMI, and children are correlated with charges (CORR)

```sql
SELECT ROUND(CORR(age, charges), 4)      AS corr_age_charges,
       ROUND(CORR(bmi, charges), 4)      AS corr_bmi_charges,
       ROUND(CORR(children, charges), 4) AS corr_children_charges
FROM insurance;
```

**Result:**

```text
┌──────────────────┬──────────────────┬───────────────────────┐
│ corr_age_charges │ corr_bmi_charges │ corr_children_charges │
│      double      │      double      │        double         │
├──────────────────┼──────────────────┼───────────────────────┤
│           0.2977 │              0.2 │                0.0688 │
└──────────────────┴──────────────────┴───────────────────────┘
```

### Q44. Find the standard deviation and coefficient of variation of charges per region

```sql
SELECT region,
       ROUND(AVG(charges), 2)                        AS avg_charges,
       ROUND(STDDEV(charges), 2)                     AS stddev_charges,
       ROUND(STDDEV(charges) / AVG(charges), 4)      AS coeff_of_variation
FROM insurance
GROUP BY region
ORDER BY coeff_of_variation DESC;
```

**Result:**

```text
┌───────────┬─────────────┬────────────────┬────────────────────┐
│  region   │ avg_charges │ stddev_charges │ coeff_of_variation │
│  varchar  │   double    │     double     │       double       │
├───────────┼─────────────┼────────────────┼────────────────────┤
│ southeast │    15215.02 │       14222.39 │             0.9348 │
│ southwest │    12554.88 │        11664.5 │             0.9291 │
│ northwest │    12417.58 │       11072.28 │             0.8917 │
│ northeast │    13406.38 │        11255.8 │             0.8396 │
└───────────┴─────────────┴────────────────┴────────────────────┘
```

### Q45. Find the non-smokers in the top 1% of charges among non-smokers (PERCENT_RANK)

```sql
SELECT age, gender, bmi, region, charges,
       ROUND(PERCENT_RANK() OVER (ORDER BY charges DESC), 4) AS pct_rank
FROM insurance
WHERE smoker = 'no'
QUALIFY pct_rank <= 0.01
ORDER BY charges DESC;
```

**Result:**

```text
┌───────┬─────────┬────────┬───────────┬─────────────┬──────────┐
│  age  │ gender  │  bmi   │  region   │   charges   │ pct_rank │
│ int32 │ varchar │ double │  varchar  │   double    │  double  │
├───────┼─────────┼────────┼───────────┼─────────────┼──────────┤
│    59 │ female  │   34.8 │ southwest │ 36910.60803 │      0.0 │
│    60 │ female  │   34.8 │ southwest │ 36910.60803 │      0.0 │
│    61 │ female  │  33.33 │ southeast │ 36580.28216 │   0.0018 │
│    55 │ female  │   26.8 │ southwest │ 35160.13457 │   0.0026 │
│    52 │ female  │ 37.525 │ northwest │ 33471.97189 │   0.0035 │
│    44 │ male    │ 29.735 │ northeast │ 32108.66282 │   0.0044 │
│    62 │ female  │  36.86 │ northeast │ 31620.00106 │   0.0053 │
│    50 │ male    │ 25.365 │ northwest │ 30284.64294 │   0.0062 │
│    60 │ male    │ 28.595 │ northeast │ 30259.99556 │   0.0071 │
│    64 │ male    │   24.7 │ northwest │ 30166.61817 │   0.0079 │
│    55 │ male    │ 37.715 │ northwest │ 30063.58055 │   0.0088 │
│    53 │ female  │   32.3 │ northeast │ 29186.48236 │   0.0097 │
└───────┴─────────┴────────┴───────────┴─────────────┴──────────┘
  12 rows                                             6 columns
```

### Q46. Count people in each BMI category, split by smoker status

```sql
SELECT CASE
           WHEN bmi < 18.5 THEN '1-underweight'
           WHEN bmi < 25   THEN '2-normal'
           WHEN bmi < 30   THEN '3-overweight'
           ELSE '4-obese'
       END AS bmi_category,
       COUNT(*) FILTER (WHERE smoker = 'yes') AS smokers,
       COUNT(*) FILTER (WHERE smoker = 'no')  AS non_smokers,
       ROUND(AVG(charges), 2)                 AS avg_charges
FROM insurance
GROUP BY bmi_category
ORDER BY bmi_category;
```

**Result:**

```text
┌───────────────┬─────────┬─────────────┬─────────────┐
│ bmi_category  │ smokers │ non_smokers │ avg_charges │
│    varchar    │  int64  │    int64    │   double    │
├───────────────┼─────────┼─────────────┼─────────────┤
│ 1-underweight │       5 │          15 │      8852.2 │
│ 2-normal      │      56 │         182 │    10557.71 │
│ 3-overweight  │      79 │         329 │    11069.55 │
│ 4-obese       │     165 │         609 │    15862.09 │
└───────────────┴─────────┴─────────────┴─────────────┘
```

### Q47. Find the second highest charges in each region

```sql
SELECT region, age, gender, smoker, charges
FROM insurance
QUALIFY DENSE_RANK() OVER (PARTITION BY region ORDER BY charges DESC) = 2
ORDER BY region;
```

**Result:**

```text
┌───────────┬───────┬─────────┬─────────┬─────────────┐
│  region   │  age  │ gender  │ smoker  │   charges   │
│  varchar  │ int32 │ varchar │ varchar │   double    │
├───────────┼───────┼─────────┼─────────┼─────────────┤
│ northeast │    54 │ male    │ yes     │ 48549.17835 │
│ northwest │    33 │ female  │ yes     │ 55135.40209 │
│ southeast │    45 │ male    │ yes     │ 62592.87309 │
│ southwest │    28 │ male    │ yes     │ 51194.55914 │
└───────────┴───────┴─────────┴─────────┴─────────────┘
```

### Q48. Find people whose charges are more than 50% above the average for their (region, smoker) group (correlated sub-query)

```sql
SELECT i.region, i.smoker, i.age, i.bmi, i.charges
FROM insurance i
WHERE i.charges > 1.5 * (
        SELECT AVG(x.charges)
        FROM insurance x
        WHERE x.region = i.region AND
              x.smoker = i.smoker
      )
ORDER BY i.region, i.smoker, i.charges DESC;
```

**Result:**

```text
┌───────────┬─────────┬───────┬────────┬─────────────┐
│  region   │ smoker  │  age  │  bmi   │   charges   │
│  varchar  │ varchar │ int32 │ double │   double    │
├───────────┼─────────┼───────┼────────┼─────────────┤
│ northeast │ no      │    44 │ 29.735 │ 32108.66282 │
│ northeast │ no      │    62 │  36.86 │ 31620.00106 │
│ northeast │ no      │    60 │ 28.595 │ 30259.99556 │
│ northeast │ no      │    53 │   32.3 │ 29186.48236 │
│ northeast │ no      │    34 │  22.42 │ 27375.90478 │
│     ·     │ ·       │     · │     ·  │      ·      │
│     ·     │ ·       │     · │     ·  │      ·      │
│     ·     │ ·       │     · │     ·  │      ·      │
│ southwest │ yes     │    60 │   32.8 │ 52590.82939 │
│ southwest │ yes     │    28 │   36.4 │ 51194.55914 │
│ southwest │ yes     │    63 │   37.7 │    48824.45 │
│ southwest │ yes     │    60 │   39.9 │   48173.361 │
│ southwest │ yes     │    64 │   33.8 │    47928.03 │
└───────────┴─────────┴───────┴────────┴─────────────┘
  215 rows (10 shown)                      5 columns
```

### Q49. Group people into age decades (10s, 20s, ...) and summarize (integer division)

```sql
SELECT (age // 10) * 10        AS age_decade,
       COUNT(*)                AS num_people,
       ROUND(AVG(bmi), 2)      AS avg_bmi,
       ROUND(AVG(charges), 2)  AS avg_charges
FROM insurance
GROUP BY age_decade
ORDER BY age_decade;
```

**Result:**

```text
┌────────────┬────────────┬─────────┬─────────────┐
│ age_decade │ num_people │ avg_bmi │ avg_charges │
│   int32    │   int64    │ double  │   double    │
├────────────┼────────────┼─────────┼─────────────┤
│         10 │        144 │   30.09 │     8527.97 │
│         20 │        309 │   29.99 │     9862.43 │
│         30 │        271 │   30.53 │    11894.08 │
│         40 │        303 │   30.74 │    14648.88 │
│         50 │        288 │   31.64 │    16777.73 │
│         60 │        125 │   32.26 │    21712.04 │
└────────────┴────────────┴─────────┴─────────────┘
```

### Q50. Compare each region's smoker rate and average charges with the overall values (multiple CTEs + CROSS JOIN)

```sql
WITH overall AS (
  SELECT AVG(CASE WHEN smoker = 'yes' THEN 1.0 ELSE 0.0 END) AS smoker_rate,
         AVG(charges)                                         AS avg_charges
  FROM insurance
),
by_region AS (
  SELECT region,
         AVG(CASE WHEN smoker = 'yes' THEN 1.0 ELSE 0.0 END) AS smoker_rate,
         AVG(charges)                                         AS avg_charges
  FROM insurance
  GROUP BY region
)
SELECT r.region,
       ROUND(100 * r.smoker_rate, 2)                AS region_smoker_pct,
       ROUND(100 * o.smoker_rate, 2)                AS overall_smoker_pct,
       ROUND(r.avg_charges, 2)                      AS region_avg_charges,
       ROUND(o.avg_charges, 2)                      AS overall_avg_charges,
       CASE WHEN r.avg_charges > o.avg_charges
            THEN 'above average' ELSE 'below average'
       END                                          AS charges_vs_overall
FROM by_region r
CROSS JOIN overall o
ORDER BY r.region;
```

**Result:**

```text
┌───────────┬───────────────────┬────────────────────┬────────────────────┬─────────────────────┬────────────────────┐
│  region   │ region_smoker_pct │ overall_smoker_pct │ region_avg_charges │ overall_avg_charges │ charges_vs_overall │
│  varchar  │      double       │       double       │       double       │       double        │      varchar       │
├───────────┼───────────────────┼────────────────────┼────────────────────┼─────────────────────┼────────────────────┤
│ northeast │             20.68 │              21.18 │           13406.38 │            13530.15 │ below average      │
│ northwest │             17.85 │              21.18 │           12417.58 │            13530.15 │ below average      │
│ southeast │             25.85 │              21.18 │           15215.02 │            13530.15 │ above average      │
│ southwest │             18.86 │              21.18 │           12554.88 │            13530.15 │ below average      │
└───────────┴───────────────────┴────────────────────┴────────────────────┴─────────────────────┴────────────────────┘
```
