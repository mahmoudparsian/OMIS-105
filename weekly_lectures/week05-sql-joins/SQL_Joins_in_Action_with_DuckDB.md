# SQL Joins in Action

DuckDB supports a robust set of join operations, 
ranging from standard relational SQL joins to highly 
optimized, advanced extensions designed specifically 
for analytical workflows and time-series data.

DuckDB supports all traditional SQL join types out 
of the box, using an advanced vectorized hash join 
engine to optimize performance under the hood.

| Join Type	| Behavior	| Syntax Example   |
|-----------|-----------|------------------|
|INNER JOIN	|Returns rows only when the join condition is met in both tables.	| `FROM t1 JOIN t2 ON t1.id = t2.id` |
|LEFT JOIN	|Returns all rows from the left table, plus matched rows from the right (fills with NULL if no match).	| `FROM t1 LEFT JOIN t2 ON t1.id = t2.id` |
|RIGHT JOIN	|Returns all rows from the right table, plus matched rows from the left. | `FROM t1 RIGHT JOIN t2 ON t1.id = t2.id` |
|FULL OUTER JOIN|	Combines LEFT and RIGHT behaviors; retains all rows from both tables, filling mismatches with NULL.	| `FROM t1 FULL JOIN t2 ON t1.id = t2.id` |
|CROSS JOIN	|Creates a Cartesian product, matching every row of the left table with every row of the right table.	| `FROM t1 CROSS JOIN t2`|


# Understanding SQL Joins: <br> Intuition and Mathematics

Imagine you have two spreadsheets or data tables, **A** and **B**. 

* **Table A** has columns: `(key, value1)`
* **Table B** has columns: `(key, value2)`

In mathematical terms, a relation (or table) is a set of ordered pairs (tuples):

$A = \{(k, v_1) \mid k \in K_A, v_1 \in V_1\}$

$B = \{(k, v_2) \mid k \in K_B, v_2 \in V_2\}$

<br>
To handle cases where a `key` exists in one table but 
not the other, we introduce a special symbol called 
**NULL**, which represents missing information.

---

## 1. Inner Join

### Simple Explanation
An **Inner Join** keeps only the rows where the 
`key` matches in **both** Table **A** and Table 
**B**. If a key is present in **A** but not in 
**B** (or vice versa), it is dropped.

### Mathematical Definition
The Inner Join (denoted by $\bowtie$) filters the 
Cross Join to keep only elements where

$k_1 = k_2$:


$$A \bowtie B = \{ (k, v_1, v_2) \mid (k, v_1) \in A \text{ and } (k, v_2) \in B \}$$


<br>
Alternatively, using set-builder notation on the Cartesian product:


$$A \bowtie B = \{ (k_1, v_1, v_2) \mid (k_1, v_1, k_2, v_2) \in A \times B \text{ such that } k_1 = k_2 \}$$

---

## 2. Left Join (Left Outer Join)

### Simple Explanation
A **Left Join** keeps **all** rows from Table 
**A** (the left table). 

* If a key from Table **A** matches a key in 
  Table **B**, the corresponding $v_2$ value is attached.

* If a key from Table **A** has no match in Table **B**, 
  the row is still included, but $v_2$ is filled with `NULL`.

### Mathematical Definition
The Left Join (denoted by $\Leftbowtie$) is the union 
of the Inner Join and the unmatched rows of **A** padded 
with `NULL`:


$$A \Leftbowtie B = (A \bowtie B) \cup \{ (k, v_1, \text{NULL}) \mid (k, v_1) \in A \text{ and } \nexists \, v_2 \text{ such that } (k, v_2) \in B \}$$


---

## 3. Right Join (Right Outer Join)

### Simple Explanation
A **Right Join** is the exact opposite of a Left Join. 
It keeps **all** rows from Table **B** (the right table).

* If a key from Table **B** matches a key in Table **A**, 
  the corresponding $v_1$ value is attached.
  
* If a key from Table **B** has no match in Table **A**, 
  the row is included, but $v_1$ is filled with `NULL`.

### Mathematical Definition
The Right Join (denoted by $\Rightbowtie$) is the union 
of the Inner Join and the unmatched rows of **B** padded 
with `NULL`:


$$A \Rightbowtie B = (A \bowtie B) \cup \{ (k, \text{NULL}, v_2) \mid (k, v_2) \in B \text{ and } \nexists \, v_1 \text{ such that } (k, v_1) \in A \}$$


---

## 4. Full Join (Full Outer Join)

### Simple Explanation
A **Full Join** keeps **everything**. It combines 
all matching rows, all unmatched rows from Table **A**
(padded with `NULL` for $v_2$), and all unmatched rows 
from Table **B** (padded with `NULL` for $v_1$).

### Mathematical Definition
The Full Join (denoted by $\leftouterjoin$ or $\bowtie_{F}$) 
is the union of the Left Join and the Right Join:


$$A \bowtie_{F} B = (A \Leftbowtie B) \cup (A \Rightbowtie B)$$


Expanding this fully:

$$
\begin{aligned}
A \bowtie_{F} B = & \{ (k, v_1, v_2) \mid (k, v_1) \in A \text{ and } (k, v_2) \in B \} \\
& \cup \{ (k, v_1, \text{NULL}) \mid (k, v_1) \in A \text{ and } \nexists \, v_2 \text{ such that } (k, v_2) \in B \} \\
& \cup \{ (k, \text{NULL}, v_2) \mid (k, v_2) \in B \text{ and } \nexists \, v_1 \text{ such that } (k, v_1) \in A \}
\end{aligned}
$$

---

## 5. Cross Join (Cartesian Product)

### Simple Explanation
A **Cross Join** pairs *every single row* of Table 
**A** with *every single row* of Table **B**, 
regardless of whether their keys match. If Table 
**A** has 3 rows and Table **B** has 4 rows, the 
result will have `3 x 4 = 12` rows.

### Mathematical Definition
The Cross Join is the Cartesian product ($A \times B$):


$$A \times B = \{ (k_1, v_1, k_2, v_2) \mid (k_1, v_1) \in A \text{ and } (k_2, v_2) \in B \}$$


---

## Summary Matrix

| Join Type | Symbol | Matches Included? | Unmatched Left ($A$)? | Unmatched Right ($B$)? |
| :--- | :---: | :---: | :---: | :---: |
| **Cross Join** | $\times$ | All pairs ($N \times M$) | N/A | N/A |
| **Inner Join** | $\bowtie$ | Yes | No | No |
| **Left Join** | $\Leftbowtie$ | Yes | Yes (with $\text{NULL}$) | No |
| **Right Join** | $\Rightbowtie$ | Yes | No | Yes (with $\text{NULL}$) |
| **Full Join** | $\bowtie_{F}$ | Yes | Yes (with $\text{NULL}$) | Yes (with $\text{NULL}$) |

---

# Join Examples in DuckDB

```sql
% duckdb
DuckDB v1.5.5 (Variegata)
Enter ".help" for usage hints.

duckdb ▸ CREATE TABLE A (
           key INT,
           value VARCHAR
         );

duckdb ▸ INSERT INTO A
         VALUES
         (1, 'a1'),
         (1, 'a2'),
         (2, 'b1'),
         (2, 'b2'),
         (2, 'b3'),
         (3, 'c1'),
         (4, 'd1');

duckdb ▸ SELECT * FROM A;
┌───────┬─────────┐
│  key  │  value  │
│ int32 │ varchar │
├───────┼─────────┤
│     1 │ a1      │
│     1 │ a2      │
│     2 │ b1      │
│     2 │ b2      │
│     2 │ b3      │
│     3 │ c1      │
│     4 │ d1      │
└───────┴─────────┘

duckdb ▸ CREATE TABLE B (
                    key INT,
                    value VARCHAR
                  );

duckdb ▸ INSERT INTO B
                  VALUES
                  (1, 'p1'),
                  (1, 'p2'),
                  (2, 't1'),
                  (2, 't2'),
                  (5, 'x1'),
                  (6, 'y1');

duckdb ▸ SELECT * FROM B;
┌───────┬─────────┐
│  key  │  value  │
│ int32 │ varchar │
├───────┼─────────┤
│     1 │ p1      │
│     1 │ p2      │
│     2 │ t1      │
│     2 │ t2      │
│     5 │ x1      │
│     6 │ y1      │
└───────┴─────────┘


duckdb ▸ SELECT A.key AS A_key,
                B.key AS B_key, 
                A.value AS A_value, 
                B.value AS B_value
         FROM A
         INNER JOIN B on A.key = B.key
         ORDER BY A.key;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p2      │
│     1 │     1 │ a2      │ p2      │
│     1 │     1 │ a1      │ p1      │
│     1 │     1 │ a2      │ p1      │
│     2 │     2 │ b1      │ t2      │
│     2 │     2 │ b2      │ t2      │
│     2 │     2 │ b3      │ t2      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b3      │ t1      │
└───────┴───────┴─────────┴─────────┘
  10 rows                 4 columns


duckdb ▸ SELECT A.key AS A_key,
                B.key AS B_key, 
                A.value AS A_value, 
                B.value AS B_value
         FROM A
         LEFT JOIN B on A.key = B.key
         ORDER BY A.key;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p2      │
│     1 │     1 │ a2      │ p2      │
│     1 │     1 │ a1      │ p1      │
│     1 │     1 │ a2      │ p1      │
│     2 │     2 │ b1      │ t2      │
│     2 │     2 │ b2      │ t2      │
│     2 │     2 │ b3      │ t2      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b3      │ t1      │
│     3 │  NULL │ c1      │ NULL    │
│     4 │  NULL │ d1      │ NULL    │
└───────┴───────┴─────────┴─────────┘
  12 rows                 4 columns

duckdb ▸ SELECT A.key AS A_key,
                B.key AS B_key, 
                A.value AS A_value, 
                B.value AS B_value
         FROM A
         RIGHT JOIN B on A.key = B.key
         ORDER BY A.key;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p2      │
│     1 │     1 │ a2      │ p2      │
│     1 │     1 │ a1      │ p1      │
│     1 │     1 │ a2      │ p1      │
│     2 │     2 │ b1      │ t2      │
│     2 │     2 │ b2      │ t2      │
│     2 │     2 │ b3      │ t2      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b3      │ t1      │
│  NULL │     5 │ NULL    │ x1      │
│  NULL │     6 │ NULL    │ y1      │
└───────┴───────┴─────────┴─────────┘
  12 rows                 4 columns

duckdb ▸ SELECT A.key AS A_key,
                B.key AS B_key, 
                A.value AS A_value, 
                B.value AS B_value
         FROM A
         FULL JOIN B on A.key = B.key
         ORDER BY A.key;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p2      │
│     1 │     1 │ a2      │ p2      │
│     1 │     1 │ a1      │ p1      │
│     1 │     1 │ a2      │ p1      │
│     2 │     2 │ b1      │ t2      │
│     2 │     2 │ b2      │ t2      │
│     2 │     2 │ b3      │ t2      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b3      │ t1      │
│     3 │  NULL │ c1      │ NULL    │
│     4 │  NULL │ d1      │ NULL    │
│  NULL │     5 │ NULL    │ x1      │
│  NULL │     6 │ NULL    │ y1      │
└───────┴───────┴─────────┴─────────┘
  14 rows                 4 columns


duckdb ▸ SELECT A.key AS A_key,
                B.key AS B_key, 
                A.value AS A_value, 
                B.value AS B_value
         FROM A
         CROSS JOIN B
         ORDER BY A.key;
┌───────┬───────┬─────────┬─────────┐
│ A_key │ B_key │ A_value │ B_value │
│ int32 │ int32 │ varchar │ varchar │
├───────┼───────┼─────────┼─────────┤
│     1 │     1 │ a1      │ p1      │
│     1 │     2 │ a1      │ t1      │
│     1 │     6 │ a2      │ y1      │
│     1 │     6 │ a1      │ y1      │
│     1 │     5 │ a2      │ x1      │
│     1 │     5 │ a1      │ x1      │
│     1 │     2 │ a2      │ t2      │
│     1 │     1 │ a1      │ p2      │
│     1 │     1 │ a2      │ p2      │
│     1 │     2 │ a1      │ t2      │
│     1 │     2 │ a2      │ t1      │
│     1 │     1 │ a2      │ p1      │
│     2 │     1 │ b3      │ p2      │
│     2 │     5 │ b1      │ x1      │
│     2 │     6 │ b3      │ y1      │
│     2 │     6 │ b2      │ y1      │
│     2 │     2 │ b1      │ t1      │
│     2 │     2 │ b2      │ t1      │
│     2 │     2 │ b3      │ t1      │
│     2 │     6 │ b1      │ y1      │
│     2 │     1 │ b1      │ p1      │
│     2 │     1 │ b2      │ p1      │
│     2 │     1 │ b1      │ p2      │
│     2 │     2 │ b1      │ t2      │
│     2 │     2 │ b2      │ t2      │
│     2 │     2 │ b3      │ t2      │
│     2 │     1 │ b3      │ p1      │
│     2 │     1 │ b2      │ p2      │
│     2 │     5 │ b2      │ x1      │
│     2 │     5 │ b3      │ x1      │
│     3 │     1 │ c1      │ p1      │
│     3 │     5 │ c1      │ x1      │
│     3 │     2 │ c1      │ t2      │
│     3 │     2 │ c1      │ t1      │
│     3 │     1 │ c1      │ p2      │
│     3 │     6 │ c1      │ y1      │
│     4 │     1 │ d1      │ p1      │
│     4 │     6 │ d1      │ y1      │
│     4 │     5 │ d1      │ x1      │
│     4 │     2 │ d1      │ t1      │
│     4 │     1 │ d1      │ p2      │
│     4 │     2 │ d1      │ t2      │
└───────┴───────┴─────────┴─────────┘
  42 rows                 4 columns

duckdb ▸
```
