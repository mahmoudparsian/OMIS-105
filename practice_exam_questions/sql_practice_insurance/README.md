# SQL Practice: Insurance Dataset (DuckDB)

100 practice queries with answers on a single `insurance` table.
Every query and result was validated with DuckDB v1.5.5.

| File | Coverage |
|------|----------|
|[`sql_practice_level_1.md`](./sql_practice_level_1.md)| Weeks 1-5, basic: 50 queries (SELECT, WHERE, ORDER BY, LIMIT, aggregates, GROUP BY, HAVING, CASE, LIKE) |
|[`sql_practice_level_2.md`](./sql_practice_level_2.md)| Weeks 1-5+, intermediate/advanced: 50 queries (sub-queries, CTEs, window and ranking functions, QUALIFY, FILTER, ROLLUP, PIVOT) |
|[`insurance_1440_records.csv`](./insurance_1440_records.csv)| The data: 1440 records + 1 header line |

Before you start, build the database `insurance_db.duckdb` by following the steps below.


## Creating the Insurance Database in DuckDB

To create a DuckDB database from the command line
and load the `insurance_1440_records.csv` file
into a table named `insurance`, follow these steps
(run them from this folder, the one that contains the CSV file).


### 1. Insurance Data

```
% wc -l insurance_1440_records.csv
    1441 insurance_1440_records.csv

% head -5 insurance_1440_records.csv
age,gender,bmi,children,smoker,region,charges
19,female,27.9,0,yes,southwest,16884.924
18,male,33.77,1,no,southeast,1725.5523
28,male,33,3,no,southeast,4449.462
33,male,22.705,0,no,northwest,21984.47061
```


### 2. Insurance Metadata

| Column name | Description |
|-------------|-------------|
| age         | age of an insured person |
| gender      | male/female |
| bmi         | body mass index |
| children    | number of children |
| smoker      | yes/no |
| region      | southwest, southeast, northwest, northeast |
| charges     | insurance charges |


### 3. Open the DuckDB CLI

Open your terminal and launch DuckDB.
You can create a persistent database file
(e.g., `insurance_db.duckdb`). To create
a file-based database, run:

```bash
duckdb insurance_db.duckdb
```


### 4. Create the Table from the CSV File

Once inside the DuckDB prompt (`D`),
create the table with an explicit schema and
load the CSV file with `COPY`:

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

COPY insurance FROM 'insurance_1440_records.csv' (HEADER true);
```

This is the schema used by `sql_practice_level_1.md`
and `sql_practice_level_2.md`: `smoker` keeps its
`'yes'`/`'no'` values, and `bmi`/`charges` keep all digits.


### Alternative: One-Liner from the Terminal

If you don't want to enter the interactive
DuckDB shell, you can execute the commands
directly from your system command line:

```bash
duckdb insurance_db.duckdb "CREATE TABLE insurance (age INTEGER, gender VARCHAR, bmi DOUBLE, children INTEGER, smoker VARCHAR, region VARCHAR, charges DOUBLE); COPY insurance FROM 'insurance_1440_records.csv' (HEADER true);"
```


### Alternative: Let DuckDB Infer the Types

DuckDB can also create and load the table in one
step using its automatic CSV reading capabilities:

```sql
CREATE TABLE insurance AS
SELECT * FROM read_csv_auto('insurance_1440_records.csv');
```

Note: with `read_csv_auto()`, DuckDB detects `smoker`
as `BOOLEAN` (true/false) and `age`/`children` as `BIGINT`.
The practice queries still run, but the results
show true/false instead of yes/no for `smoker`.


### 5. Verify It Worked

To verify that your table was created successfully
and contains your data, run:

```sql
SELECT COUNT(*) FROM insurance;
SELECT * FROM insurance LIMIT 5;
```


### 6. Log of Database Creation

```
% duckdb insurance_db.duckdb "CREATE TABLE insurance (age INTEGER, gender VARCHAR, bmi DOUBLE, children INTEGER, smoker VARCHAR, region VARCHAR, charges DOUBLE); COPY insurance FROM 'insurance_1440_records.csv' (HEADER true);"

% duckdb insurance_db.duckdb
DuckDB v1.5.5 (Variegata)
Enter ".help" for usage hints.

D .schema
CREATE TABLE insurance(age INTEGER, gender VARCHAR, bmi DOUBLE, children INTEGER, smoker VARCHAR, region VARCHAR, charges DOUBLE);

D SELECT COUNT(*) FROM insurance;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│         1440 │
└──────────────┘

D SELECT * FROM insurance LIMIT 5;
┌───────┬─────────┬────────┬──────────┬─────────┬───────────┬─────────────┐
│  age  │ gender  │  bmi   │ children │ smoker  │  region   │   charges   │
│ int32 │ varchar │ double │  int32   │ varchar │  varchar  │   double    │
├───────┼─────────┼────────┼──────────┼─────────┼───────────┼─────────────┤
│    19 │ female  │   27.9 │        0 │ yes     │ southwest │   16884.924 │
│    18 │ male    │  33.77 │        1 │ no      │ southeast │   1725.5523 │
│    28 │ male    │   33.0 │        3 │ no      │ southeast │    4449.462 │
│    33 │ male    │ 22.705 │        0 │ no      │ northwest │ 21984.47061 │
│    32 │ male    │  28.88 │        0 │ no      │ northwest │   3866.8552 │
└───────┴─────────┴────────┴──────────┴─────────┴───────────┴─────────────┘

D .exit
```
