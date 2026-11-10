# DuckDB string_split Example

In DuckDB, the `string_split` function (also known as `str_split` or `split`) turns a delimited string into a **LIST**. 

To expand a comma-separated column into individual rows, combine `string_split` with `unnest()`.

### 1. Create a simple table and insert data

```sql
CREATE TABLE products (
    id INT,
    name VARCHAR,
    tags VARCHAR
);

INSERT INTO products VALUES
(1, 'Laptop', 'electronics,computer,work'),
(2, 'Bike', 'sports,outdoor'),
(3, 'Coffee Mug', 'kitchen');
```

### 2. Return a list per row

If you want to keep the split values grouped as a list inside a column:

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
| 1 | Laptop | ['electronics', 'computer', 'work'] |
| 2 | Bike | ['sports', 'outdoor'] |
| 3 | Coffee Mug | ['kitchen'] |

### 3. Explode the list into multiple rows (unnest)

To turn each delimited item into its own row, wrap the function in `unnest()`:

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
