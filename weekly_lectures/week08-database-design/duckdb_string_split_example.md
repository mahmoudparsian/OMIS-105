# DuckDB `string_split` Example

In DuckDB, the `string_split` function turns a delimited string (text with a
separator, such as a comma) into a **LIST**. It has three other names that do
exactly the same thing: `str_split`, `split`, and `string_to_array`.

To turn a comma-separated column into **one row per value**, combine
`string_split` with `unnest()`. This is the main SQL tool for fixing
**Rule 1 of First Normal Form** (one value per cell) — see
[`1nf_guide.md`](1nf_guide.md).

---

### 1. Create a simple table and insert data

The `tags` column holds several values in one cell, so this table is **not** in 1NF.

```sql
CREATE OR REPLACE TABLE products (
    id   INT,
    name VARCHAR,
    tags VARCHAR
);

INSERT INTO products VALUES
(1, 'Laptop',     'electronics,computer,work'),
(2, 'Bike',       'sports,outdoor'),
(3, 'Coffee Mug', 'kitchen');
```

### 2. Return a list per row

`string_split` alone keeps the values together, as a list inside one column:

```sql
SELECT
    id,
    name,
    string_split(tags, ',') AS tag_list
FROM products;
```

**Result:**

| id | name | tag_list |
| :--- | :--- | :--- |
| 1 | Laptop | [electronics, computer, work] |
| 2 | Bike | [sports, outdoor] |
| 3 | Coffee Mug | [kitchen] |

The type of `tag_list` is `VARCHAR[]` (a list of text). A list is useful for
analysis, but it is still **many values in one cell** — not 1NF.

### 3. Explode the list into multiple rows (`unnest`)

To turn each item into its own row, wrap the function in `unnest()`.
The other columns (`id`, `name`) are copied onto every new row:

```sql
SELECT
    id,
    name,
    unnest(string_split(tags, ',')) AS tag
FROM products;
```

**Result:**

| id | name | tag |
| :--- | :--- | :--- |
| 1 | Laptop | electronics |
| 1 | Laptop | computer |
| 1 | Laptop | work |
| 2 | Bike | sports |
| 2 | Bike | outdoor |
| 3 | Coffee Mug | kitchen |

3 rows became 6, and every cell holds **one** value: this result is in 1NF.
Its primary key is (`id`, `tag`).

### 4. Watch out for spaces after the comma

Real data often has a space after each comma: `'Laptop, Mouse'`.
If you split on `','` only, the space stays on the second value:

```sql
SELECT string_split('Laptop, Mouse', ',') AS items;
-- [Laptop, ' Mouse']   ← the second value is ' Mouse', with a leading space
```

Then `WHERE item = 'Mouse'` will not find it. Two fixes:

```sql
-- Fix 1: split on comma AND space
SELECT unnest(string_split('Laptop, Mouse', ', ')) AS item;

-- Fix 2: split on the comma, then remove the spaces with trim()
SELECT trim(item) AS item
FROM (SELECT unnest(string_split('Laptop, Mouse', ',')) AS item);
```

Both return two clean rows: `Laptop` and `Mouse`.
Fix 2 is safer when the spacing is not the same in every row.

---

**More:** [`duckdb_normalization_functions.md`](duckdb_normalization_functions.md)
shows the DuckDB tools for 1NF, 2NF, and 3NF together.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
