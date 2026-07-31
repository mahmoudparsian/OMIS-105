# Presidential Terms by Century

## What does this query do?

This query groups presidents by the century in which their term began and calculates several statistics for each century:

- Number of presidents
- Average days in office
- Shortest presidential term
- Longest presidential term

This allows us to compare presidential service across different centuries.

---

## SQL Query

```sql
SELECT CASE
           WHEN YEAR(term_start) < 1800 THEN '18th century'
           WHEN YEAR(term_start) < 1900 THEN '19th century'
           WHEN YEAR(term_start) < 2000 THEN '20th century'
           ELSE '21st century'
       END AS century,
       COUNT(*) AS presidents,
       AVG(term_end - term_start)::INTEGER AS avg_days_in_office,
       MIN(term_end - term_start) AS shortest_term,
       MAX(term_end - term_start) AS longest_term
FROM presidents
GROUP BY 1
ORDER BY 1;
```

---

## Step 1: Determine the Century

```sql
CASE
    WHEN YEAR(term_start) < 1800 THEN '18th century'
    WHEN YEAR(term_start) < 1900 THEN '19th century'
    WHEN YEAR(term_start) < 2000 THEN '20th century'
    ELSE '21st century'
END AS century
```

### What does this do?

The `CASE` expression assigns each president to a century based on the year their term started.

### Examples

| term_start | YEAR(term_start) | century |
|------------|------------------|----------|
| 1789-04-30 | 1789 | 18th century |
| 1861-03-04 | 1861 | 19th century |
| 1933-03-04 | 1933 | 20th century |
| 2021-01-20 | 2021 | 21st century |

Think of `CASE` as an SQL version of an IF-THEN-ELSE statement.

---

## Step 2: Count Presidents

```sql
COUNT(*) AS presidents
```

### What does this do?

Counts how many presidents belong to each century.

Example:

| century | presidents |
|----------|------------|
| 18th century | 2 |
| 19th century | 22 |
| 20th century | 20 |
| 21st century | 4 |

---

## Step 3: Calculate Average Days in Office

```sql
AVG(term_end - term_start)::INTEGER AS avg_days_in_office
```

### What does this do?

1. Calculates the number of days each president served.
2. Computes the average for all presidents in a century.
3. Converts the result to an integer.

Example:

| President | Days in Office |
|------------|---------------|
| President A | 1461 |
| President B | 2922 |
| President C | 1461 |

Average:

```text
(1461 + 2922 + 1461) / 3 = 1948
```

Result:

| avg_days_in_office |
|--------------------|
| 1948 |

---

## Step 4: Find the Shortest Presidential Term

```sql
MIN(term_end - term_start) AS shortest_term
```

### What does this do?

Finds the smallest number of days served by any president in that century.

Example:

| Days in Office |
|---------------|
| 31 |
| 199 |
| 1461 |
| 2922 |

Result:

```text
31
```

---

## Step 5: Find the Longest Presidential Term

```sql
MAX(term_end - term_start) AS longest_term
```

### What does this do?

Finds the largest number of days served by any president in that century.

Example:

| Days in Office |
|---------------|
| 31 |
| 199 |
| 1461 |
| 4422 |

Result:

```text
4422
```

---

## Step 6: Group the Data

```sql
GROUP BY 1
```

### What does this do?

Groups all presidents that belong to the same century.

The number `1` refers to the first item in the SELECT list:

```sql
CASE ... END AS century
```

Therefore:

```sql
GROUP BY 1
```

is equivalent to:

```sql
GROUP BY century
```

Many SQL developers prefer `GROUP BY century` because it is easier to read.

---

## Step 7: Sort the Results

```sql
ORDER BY 1
```

### What does this do?

Sorts the results by the first selected column:

```sql
century
```

Equivalent to:

```sql
ORDER BY century
```

---

## Example Result

| century | presidents | avg_days_in_office | shortest_term | longest_term |
|----------|------------|-------------------|---------------|--------------|
| 18th century | 2 | 2865 | 2865 | 2865 |
| 19th century | 22 | 1498 | 31 | 2922 |
| 20th century | 20 | 1675 | 199 | 4422 |
| 21st century | 4 | 1461 | 1461 | 1461 |

---

## Visual Summary

```text
presidents
     |
     v
Determine Century
(CASE expression)
     |
     v
18th century
19th century
20th century
21st century
     |
     v
GROUP BY century
     |
     v
COUNT presidents
AVG days in office
MIN days in office
MAX days in office
     |
     v
ORDER BY century
```

---

## Key Concepts Learned

1. **CASE** creates categories from data.
2. **YEAR()** extracts the year from a date.
3. **COUNT()** counts rows.
4. **AVG()** computes averages.
5. **MIN()** finds the smallest value.
6. **MAX()** finds the largest value.
7. **GROUP BY** creates summary groups.
8. **ORDER BY** sorts the results.
9. **Column positions (`GROUP BY 1`, `ORDER BY 1`)** refer to columns in the SELECT list.

---

## Plain-English Description

> Group presidents by the century in which their term began, then calculate how many presidents served in each century, their average length of service, and the shortest and longest presidential terms.
