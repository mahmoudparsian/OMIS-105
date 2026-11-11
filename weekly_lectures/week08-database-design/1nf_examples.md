# First Normal Form (1NF) — Examples

A table is in **First Normal Form (1NF)** when:

1. **One value per cell (atomic values):** no lists and no comma-separated values in a cell.
2. **No repeating groups:** no columns like `phone1`, `phone2`, `phone3` for the same kind of data.
3. **A primary key:** every row is unique, and a key (one column or several) identifies it.

Two housekeeping rules come with them: every column has a **unique name**, and every
value in a column has the **same data type** (for example, all dates or all text).

This page shows four small examples. The SQL behind them (`STRING_SPLIT`, `UNNEST`,
`UNION ALL`, `UNPIVOT`) is in [`1nf_guide.md`](1nf_guide.md).

---

## Example 1: A List in One Cell

### ❌ Before: not in 1NF

A student table where one column lists several courses, separated by commas:

| `student_id` | `student_name` | `courses_enrolled` |
|---|---|---|
| 101 | John Smith | Math, Physics |
| 102 | Sarah Lee | History |
| 103 | Max Smith | SQL, Java, AI |
| 104 | Jane Doe| Introduction to SQL |

**Why it breaks 1NF:** the `courses_enrolled` cell holds several values packed
together (`Math, Physics`). That makes searching, counting, and sorting hard:
`WHERE courses_enrolled = 'Math'` finds **no** rows.

### ✅ After: in 1NF

Split the list so that each row holds **one** fact: one student in one course.

| `student_id` | `student_name` | `course` |
|---|---|---|
| 101 | John Smith | Math |
| 101 | John Smith | Physics |
| 102 | Sarah Lee | History |
| 103 | Max Smith | SQL |
| 103 | Max Smith | Java |
| 103 | Max Smith | AI |
| 104 | Jane Doe| Introduction to SQL |

* **Primary key:** (`student_id`, `course`). Neither column alone is unique.
* `student_name` is now repeated. 1NF allows this; **2NF** removes it
  (see [`2nf_guide.md`](2nf_guide.md)).

### Going one step further: splitting a name

"Atomic" means *one value **for how we use the data***. If you often search or
sort by last name, store the parts of the name separately:

| `student_id` | `first_name` | `last_name` | `course` |
|---|---|---|---|
| 101 | John | Smith | Math |
| 101 | John | Smith | Physics |
| 102 | Sarah | Lee | History |
| 103 | Max | Smith | SQL |
| 103 | Max | Smith | Java |
| 103 | Max | Smith | AI |
| 104 | Jane | Doe| Introduction to SQL |

This is a design choice, not a strict 1NF rule. A full name in one column is
still in 1NF, but `WHERE last_name = 'Smith'` is easier than
`WHERE student_name LIKE '% Smith'`.

---

## Example 2: Repeating Columns (Phone Numbers)

### ❌ Before: repeating columns

A student table that stores up to three phone numbers in `phone1`, `phone2`, `phone3`:

| `student_id` | `student_name` | `phone1` | `phone2` | `phone3` |
|---|---|---|---|---|
| 101 | Alice | 555-1111 | 555-2222 | NULL |
| 102 | Bob | 555-3333 | NULL | NULL |
| 103 | Charlie | 555-4444 | 555-5555 | 555-6666 |

**Why this breaks 1NF:**

* Three columns store the **same kind** of data (a phone number).
* Students with fewer than three phones leave `NULL` gaps.
* A 4th phone number does not fit. You would have to change the table.

### ✅ After, way 1: one table, one row per phone

Remove the repeating columns and give each phone number its own row:

| `student_id` | `student_name` | `phone_number` |
|---|---|---|
| 101 | Alice | 555-1111 |
| 101 | Alice | 555-2222 |
| 102 | Bob | 555-3333 |
| 103 | Charlie | 555-4444 |
| 103 | Charlie | 555-5555 |
| 103 | Charlie | 555-6666 |

* **Primary key:** (`student_id`, `phone_number`)
* **Why it is 1NF:** every cell holds one value, and there are no repeating columns.
* **The downside:** names (Alice, Charlie) are repeated — redundancy.

### ✅ After, way 2 (better): a parent table and a child table

Split the data into a `students` table and a `student_phones` table, linked by
`student_id`:

**Table 1: `students`** — primary key `student_id`

| `student_id` | `student_name` |
|---|---|
| 101 | Alice |
| 102 | Bob |
| 103 | Charlie |

**Table 2: `student_phones`** (child table) — primary key `phone_id`;
`student_id` is a foreign key to `students`

| `phone_id` | `student_id` | `phone_number` |
|---|---|---|
| 1 | 101 | 555-1111 |
| 2 | 101 | 555-2222 |
| 3 | 102 | 555-3333 |
| 4 | 103 | 555-4444 |
| 5 | 103 | 555-5555 |
| 6 | 103 | 555-6666 |

**Why this is best:** it is in 1NF, each name is stored **once**, there are no
empty `NULL` slots, and a student can have any number of phones.

---

## Example 3: Repeating Columns (Items in an Order)

### ❌ Before: repeating columns

An `orders` table that tracks up to three items with `item1`, `item2`, `item3`:

| `order_id` | `customer_name` | `item1` | `item2` | `item3` |
|---|---|---|---|---|
| 5001 | David | Laptop | Mouse | NULL |
| 5002 | Emma | Keyboard | NULL | NULL |
| 5003 | Frank | Monitor | Desk | Chair |

**Why this breaks 1NF:**

* **Repeating group:** `item1`, `item2`, `item3` hold the same kind of data.
* **Empty slots:** Emma bought one thing, so two cells are `NULL`.
* **A hard limit:** a 4th item (a lamp) does not fit — there is no `item4` column.

### ✅ After: a parent table and a child table

**Table 1: `orders`** (parent table) — primary key `order_id`.
It holds only facts about the **whole** order.

| `order_id` | `customer_name` |
|---|---|
| 5001 | David |
| 5002 | Emma |
| 5003 | Frank |

**Table 2: `order_items`** (child table) — primary key `order_item_id`;
`order_id` is a foreign key to `orders`. Each item gets its own row.

| `order_item_id` | `order_id` | `item_name` |
|---|---|---|
| 1 | 5001 | Laptop |
| 2 | 5001 | Mouse |
| 3 | 5002 | Keyboard |
| 4 | 5003 | Monitor |
| 5 | 5003 | Desk |
| 6 | 5003 | Chair |

Now an order can have any number of items.

---

## Example 4: A Repeating *Group* of Columns (Mechanics and Cars)

Sometimes a **pair** of columns repeats, not just one column.

### ❌ Before: repeating column pairs

A garage tracks which cars each mechanic fixes today, with
`car1_vin`, `car1_model`, `car2_vin`, `car2_model`
(a **VIN** is a car's unique Vehicle Identification Number):

| `mechanic_id` | `mechanic_name` | `car1_vin` | `car1_model` | `car2_vin` | `car2_model` |
|---|---|---|---|---|---|
| M401 | Carlos | VIN123 | Toyota Camry | VIN456 | Ford F-150 |
| M402 | Aisha | VIN789 | Honda Civic | NULL | NULL |

**Why this breaks 1NF:**

* **A repeating group:** the pair (`vin`, `model`) repeats across the row (`car1_…`, `car2_…`).
* **Empty slots:** Aisha works on one car, so the `car2_…` cells are `NULL`.
* **Not flexible:** a 3rd car for Carlos needs two new columns, `car3_vin` and `car3_model`.

### ✅ After: a parent table and a child table

**Table 1: `mechanics`** — primary key `mechanic_id`

| `mechanic_id` | `mechanic_name` |
|---|---|
| M401 | Carlos |
| M402 | Aisha |

**Table 2: `repair_assignments`** — primary key `assignment_id`;
`mechanic_id` is a foreign key to `mechanics`

| `assignment_id` | `mechanic_id` | `vehicle_vin` | `vehicle_model` |
|---|---|---|---|
| 1 | M401 | VIN123 | Toyota Camry |
| 2 | M401 | VIN456 | Ford F-150 |
| 3 | M402 | VIN789 | Honda Civic |

**Why it works:** every cell holds one value, the columns no longer repeat across
the row, and a mechanic can get any number of cars without changing the table.

---

## Quick Self-Check

For each table you design, ask:

1. Does any cell hold a list? → split it into rows.
2. Do any columns end in `1`, `2`, `3` (or repeat as a group)? → turn them into rows,
   usually in a child table.
3. What is the primary key? → if no column (or set of columns) is unique, add an ID.

---

## Complete Example: From a Non-1NF Table to 1NF, Step by Step

This last example puts everything together. We start with one bad table that
breaks **both** 1NF rules, and we fix it with SQL, one step at a time. Every
result below is real DuckDB output, so you can run the code and compare.

### The story

A campus book club keeps its members in one table. The `genres` column holds a
**list**, and the phone numbers are **repeating columns**.

### Step 1: Create the bad table

```sql
CREATE OR REPLACE TABLE club_members_bad (
    member_id   INT,
    member_name VARCHAR,
    genres      VARCHAR,     -- a list in one cell        (breaks Rule 1)
    phone_1     VARCHAR,     -- repeating columns          (breaks Rule 2)
    phone_2     VARCHAR
);

INSERT INTO club_members_bad VALUES
(1, 'Ana',   'Mystery, Sci-Fi',          '408-555-0101', '408-555-0102'),
(2, 'Ben',   'Romance',                  '650-555-0201', NULL),
(3, 'Chloe', 'Sci-Fi, History, Mystery', '408-555-0301', NULL);

SELECT * FROM club_members_bad;
```

| member_id | member_name | genres | phone_1 | phone_2 |
|---|---|---|---|---|
| 1 | Ana | Mystery, Sci-Fi | 408-555-0101 | 408-555-0102 |
| 2 | Ben | Romance | 650-555-0201 | NULL |
| 3 | Chloe | Sci-Fi, History, Mystery | 408-555-0301 | NULL |

### Step 2: See the problem

Who likes Sci-Fi? Ana and Chloe do — but SQL cannot see it:

```sql
SELECT member_name
FROM club_members_bad
WHERE genres = 'Sci-Fi';
```

**Result: 0 rows.** No cell is exactly `'Sci-Fi'`; the cells are
`'Mystery, Sci-Fi'` and `'Sci-Fi, History, Mystery'`. A list in a cell hides
the data from `WHERE`, `GROUP BY`, and `JOIN`.

### Step 3: Plan the new tables

Ask: *"What does each column describe, and can it have more than one value?"*

| Column | One value or many? | Goes to |
|---|---|---|
| `member_name` | one per member | `members`(**member_id**, member_name) |
| `genres` | **many** per member | `member_genres`(**member_id, genre**) — one row per genre |
| `phone_1`, `phone_2` | **many** per member | `member_phones`(**member_id, phone**) — one row per phone |

### Step 4: Build `members` — the facts with one value

```sql
CREATE OR REPLACE TABLE members AS
SELECT member_id, member_name
FROM club_members_bad;

SELECT * FROM members ORDER BY member_id;
```

| member_id | member_name |
|---|---|
| 1 | Ana |
| 2 | Ben |
| 3 | Chloe |

### Step 5: Fix the list — `STRING_SPLIT` + `UNNEST`

`STRING_SPLIT(genres, ', ')` turns `'Mystery, Sci-Fi'` into the list
`['Mystery', 'Sci-Fi']`. `UNNEST(...)` turns that list into **rows**. The other
columns in the `SELECT` (`member_id`) are copied onto each new row.

```sql
CREATE OR REPLACE TABLE member_genres AS
SELECT
    member_id,
    UNNEST(STRING_SPLIT(genres, ', ')) AS genre
FROM club_members_bad;

SELECT * FROM member_genres ORDER BY member_id, genre;
```

| member_id | genre |
|---|---|
| 1 | Mystery |
| 1 | Sci-Fi |
| 2 | Romance |
| 3 | History |
| 3 | Mystery |
| 3 | Sci-Fi |

3 rows became 6: one row for each (member, genre) pair.

### Step 6: Fix the repeating columns — `UNION ALL`

Take each phone column in turn, and skip the empty ones (`IS NOT NULL`).
`UNION ALL` stacks the results into one table.

```sql
CREATE OR REPLACE TABLE member_phones AS
SELECT member_id, phone_1 AS phone FROM club_members_bad WHERE phone_1 IS NOT NULL
UNION ALL
SELECT member_id, phone_2          FROM club_members_bad WHERE phone_2 IS NOT NULL;

SELECT * FROM member_phones ORDER BY member_id, phone;
```

| member_id | phone |
|---|---|
| 1 | 408-555-0101 |
| 1 | 408-555-0102 |
| 2 | 650-555-0201 |
| 3 | 408-555-0301 |

The two `NULL` phones are gone, and a member can now have **any** number of phones.

### Step 7: Check the primary keys

A key must be unique. If these queries return **0 rows**, no
(member, genre) or (member, phone) pair appears twice:

```sql
SELECT member_id, genre, COUNT(*) AS copies
FROM member_genres
GROUP BY member_id, genre
HAVING COUNT(*) > 1;            -- 0 rows ✅

SELECT member_id, phone, COUNT(*) AS copies
FROM member_phones
GROUP BY member_id, phone
HAVING COUNT(*) > 1;            -- 0 rows ✅
```

### Step 8: Ask the question again

Now the Sci-Fi question works, with a JOIN:

```sql
SELECT m.member_name
FROM members m
JOIN member_genres g ON m.member_id = g.member_id
WHERE g.genre = 'Sci-Fi'
ORDER BY m.member_name;
```

| member_name |
|---|
| Ana |
| Chloe |

And a question that was impossible before — how many members like each genre:

```sql
SELECT genre, COUNT(*) AS members
FROM member_genres
GROUP BY genre
ORDER BY members DESC, genre;
```

| genre | members |
|---|---|
| Mystery | 2 |
| Sci-Fi | 2 |
| History | 1 |
| Romance | 1 |

### What we did

| Step | Rule fixed | SQL tool |
|---|---|---|
| 5 | Rule 1: one value per cell | `UNNEST(STRING_SPLIT(...))` |
| 6 | Rule 2: no repeating groups | `UNION ALL` (or `UNPIVOT`) |
| 4, 7 | Rule 3: a primary key | a table per "thing" + `GROUP BY … HAVING COUNT(*) > 1` |

One table became three: `members`, `member_genres`, and `member_phones`, linked
by `member_id`. Each member's name is stored **once**, so these tables are
already in 2NF too.

---

*OMIS 105 — Introduction to Database Management Systems — Fall 2026*
