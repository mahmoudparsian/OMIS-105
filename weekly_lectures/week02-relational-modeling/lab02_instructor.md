# Lab 2: Relational Thinking — INSTRUCTOR SOLUTIONS

## OMIS 105 — Database Management Systems
**Week 2 | Answer Key**

---

## Part 1: Key Identification (15 points)

**Q1.** (5 pts) Primary keys:
- `categories`: `category_id` — unique integer identifying each category
- `products`: `product_id` — unique integer identifying each product
- `customers`: `customer_id` — unique integer identifying each customer

All are surrogate keys (auto-assigned integers with no business meaning).

**Q2.** (3 pts) `category_id` in `products` is a foreign key referencing `categories(category_id)`.

**Q3.** (4 pts) Yes, email is a candidate key:

```sql
SELECT email, COUNT(*) AS cnt
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```
> Returns 0 rows → every email is unique → email qualifies as a candidate key.

**Q4.** (3 pts) Example: `order_items(order_id, product_id)` — neither column is unique alone (an order can have multiple items, a product can appear in multiple orders), but together they uniquely identify each line item.

---

## Part 2: Relationship Analysis (15 points)

**Q5.** (6 pts)
- categories → products: **1:M** (one category has many products, each product belongs to one category)
- customers → orders: **1:M** (one customer can place many orders, each order belongs to one customer)
- products ↔ suppliers: **M:M** (one product can have multiple suppliers, one supplier can supply multiple products)

**Q6.** (4 pts)

```sql
SELECT c.category_name, COUNT(*) AS product_count
FROM categories c, products p
WHERE c.category_id = p.category_id
GROUP BY c.category_name
ORDER BY product_count DESC;
```

**Q7.** (5 pts)
- customers → reviews: **1:M** (one customer writes many reviews)
- products → reviews: **1:M** (one product can have many reviews)
- customers ↔ products (through reviews): effectively **M:M** — a customer can review many products, a product can be reviewed by many customers. The reviews table acts as a junction table with additional attributes (rating, text).

---

## Part 3: Schema Creation (20 points)

**Q8.** (8 pts)

```sql
CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER REFERENCES customers(customer_id),
    order_date   DATE NOT NULL,
    status       VARCHAR CHECK (status IN ('processing','shipped','completed','cancelled')),
    total_amount DECIMAL(10,2) CHECK (total_amount > 0)
);
```
> Award full credit if all 5 constraints are present (PK, FK, NOT NULL, CHECK on status, CHECK on amount).

**Q9.** (7 pts)

```sql
CREATE TABLE order_items (
    order_id   INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity   INTEGER CHECK (quantity > 0),
    unit_price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_id)
);
```

**Q10.** (5 pts)

```sql
INSERT INTO orders VALUES (1, 1, '2024-06-01', 'completed', 150.00);
INSERT INTO orders VALUES (2, 2, '2024-06-02', 'shipped', 75.50);
INSERT INTO orders VALUES (3, 1, '2024-06-03', 'processing', 200.00);

INSERT INTO order_items VALUES (1, 1, 1, 150.00);
INSERT INTO order_items VALUES (2, 3, 2, 25.00);
INSERT INTO order_items VALUES (2, 5, 1, 25.50);
INSERT INTO order_items VALUES (3, 2, 1, 120.00);
INSERT INTO order_items VALUES (3, 7, 2, 40.00);

SELECT * FROM orders;
SELECT * FROM order_items;
```

---

## Part 4: Referential Integrity (10 points)

**Q11.** (5 pts)

```sql
INSERT INTO orders VALUES (99, 9999, '2024-01-01', 'processing', 50.00);
```
> **Note**: DuckDB may or may not enforce FK constraints depending on version. If it succeeds, explain that in a production DBMS this would fail. The concept is what matters.

**Q12.** (5 pts)

```sql
SELECT p.product_id, p.product_name, p.category_id
FROM products p
WHERE p.category_id NOT IN (SELECT category_id FROM categories);
```
> Should return 0 rows (data integrity holds).

---

## Part 5: ER Diagram (15 points)

**Q13.** (15 pts)

```
┌─────────────┐         ┌──────────────┐
│ instructors │         │   students   │
│─────────────│         │──────────────│
│PK inst_id   │──┐      │PK student_id │──┐
│ name        │  │      │ name         │  │
│ department  │  │      │ email        │  │
└─────────────┘  │      │ major        │  │
                 │      └──────────────┘  │
            ┌────┴────┐             ┌─────┴──────┐
            │ courses │             │enrollments │
            │─────────│             │────────────│
            │PK c_id  │─────────────│FK c_id     │
            │ title   │             │FK s_id     │
            │ credits │             │ semester   │
            │ dept    │             │ grade      │
            │FK inst  │             │PK(s_id,c_id│
            └─────────┘             │  ,semester)│
                                    └────────────┘
```

**Relationships**:
- instructors → courses: 1:M
- students ↔ courses (through enrollments): M:M
- The enrollments table is the junction table with composite PK

**Grading**: 5 pts for correct entities/attributes, 5 pts for correct relationships, 5 pts for correct cardinality.

---

## Part 6: Challenge (5 bonus)

**Q14.** Sample music streaming schema:

```sql
CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    genre VARCHAR
);

CREATE TABLE albums (
    album_id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    artist_id INTEGER REFERENCES artists(artist_id),
    release_year INTEGER
);

CREATE TABLE songs (
    song_id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    album_id INTEGER REFERENCES albums(album_id),
    duration_seconds INTEGER
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE
);

-- M:M: users can have many playlists, playlists have many songs
CREATE TABLE playlists (
    playlist_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    name VARCHAR
);

CREATE TABLE playlist_songs (
    playlist_id INTEGER REFERENCES playlists(playlist_id),
    song_id INTEGER REFERENCES songs(song_id),
    position INTEGER,
    PRIMARY KEY (playlist_id, song_id)
);
```

---

## Grading Rubric

| Part | Points |
|------|--------|
| Part 1: Key Identification | 15 |
| Part 2: Relationship Analysis | 15 |
| Part 3: Schema Creation | 20 |
| Part 4: Referential Integrity | 10 |
| Part 5: ER Diagram | 15 |
| **Subtotal** | **75** |
| Part 6: Challenge | 5 |
| **Maximum** | **80** |

