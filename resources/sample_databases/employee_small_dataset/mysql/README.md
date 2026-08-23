# Employee Sample Database for MySQL

This repo is based on the work from `https://github.com/datacharmer/test_db` with the following improvements:

* datasets:

* dataset_small (~600 KB). ~0.3% of the dataset_full (1000 employees vs 300024 employees).

* Use singular form instead of plural form to name the table (e.g. `employees` -> `employee`).


## Schema

![Schema](schema.png)

## Prerequisites

You need a MySQL database server (5.0+) and run the commands below through a
user that has the following privileges:

    SELECT, INSERT, UPDATE, DELETE,
    CREATE, DROP, RELOAD, REFERENCES,
    INDEX, ALTER, SHOW DATABASES,
    CREATE TEMPORARY TABLES,
    LOCK TABLES, EXECUTE, CREATE VIEW

## Installation:

1. Download the repository
2. Change directory to the repository
3. Change directory to  `dataset_small`

Run:

```bash
cd dataset_small
```

Then run

```
mysql < employee.sql
```

## Testing the installation

### Testing `dataset_small`

    // Under 'dataset_small' directory
    mysql -t < test_employee_md5.sql

    +----------------------+
    | INFO                 |
    +----------------------+
    | TESTING INSTALLATION |
    +----------------------+
    +--------------+-----------------+----------------------------------+
    | table_name   | expected_record | expected_crc                     |
    +--------------+-----------------+----------------------------------+
    | department   |               9 | d1af5e170d2d1591d776d5638d71fc5f |
    | dept_emp     |            1103 | e302aa5b56a69b49e40eb0d60674addc |
    | dept_manager |              16 | 8ff425d5ad6dc56975998d1893b8dca9 |
    | employee     |            1000 | 595460127fb609c2b110b1796083e242 |
    | salary       |            9488 | 61f22cfece4d34f5bb94c9f05a3da3ef |
    | title        |            1470 | ba77dd331ce00f76c1643a7d73cdcee6 |
    +--------------+-----------------+----------------------------------+
    +--------------+------------------+----------------------------------+
    | table_name   | found_records    | found_crc                        |
    +--------------+------------------+----------------------------------+
    | department   |                9 | d1af5e170d2d1591d776d5638d71fc5f |
    | dept_emp     |             1103 | e302aa5b56a69b49e40eb0d60674addc |
    | dept_manager |               16 | 8ff425d5ad6dc56975998d1893b8dca9 |
    | employee     |             1000 | 595460127fb609c2b110b1796083e242 |
    | salary       |             9488 | 61f22cfece4d34f5bb94c9f05a3da3ef |
    | title        |             1470 | ba77dd331ce00f76c1643a7d73cdcee6 |
    +--------------+------------------+----------------------------------+
    +--------------+---------------+-----------+
    | table_name   | records_match | crc_match |
    +--------------+---------------+-----------+
    | department   | OK            | ok        |
    | dept_emp     | OK            | ok        |
    | dept_manager | OK            | ok        |
    | employee     | OK            | ok        |
    | salary       | OK            | ok        |
    | title        | OK            | ok        |
    +--------------+---------------+-----------+
    +------------------+
    | computation_time |
    +------------------+
    | 00:00:00         |
    +------------------+
    +---------+--------+
    | summary | result |
    +---------+--------+
    | CRC     | OK     |
    | count   | OK     |
    +---------+--------+

## Installing the function (optional)

```bash
mysql < object.sql
```

**If you are connecting to a cloud instance such as AWS RDS. You MUST turn off binary logging first. Otherwise, you will encounter error**

    You do not have the SUPER privilege and binary logging is enabled (you *might* want to use the less safe log_bin_trust_function_creators variable)
       
