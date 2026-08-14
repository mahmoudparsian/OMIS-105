# 🐈‍⬛ Cats, Breeds & Tricks — with Avatar Images

**OMIS-105 · Week 2 — Relational Modeling** *(schema)*
**→ revisit in Weeks 3 and 5** *(the notebook's later sections)*

The same four-table cat show database as `cats_and_breeds/`, plus a unique avatar
image for every cat. The images are not decoration — they make result sets something
students actually want to look at.

**Pick one of the two cat stories, not both.** They teach the same schema.

---

## Run it

```bash
marimo edit cats_and_breeds_duckdb_marimo.py    # interactive
marimo run  cats_and_breeds_duckdb_marimo.py    # read-only
```

Needs an **internet connection** — the avatars are fetched from robohash.org at
display time.

| File | Role |
|---|---|
| `cats_and_breeds_duckdb_marimo.py` | The notebook — 6 sections |
| `display_utils.py` | Table display **and the image gallery** |
| `plot_utils.py` | Chart functions |
| `README.MP.md` | The design discussion behind the image feature |
| `data/*.csv` | Four CSV files |

---

## The schema

```
   breeds                    cats                     cat_tricks              tricks
┌──────────────┐      ┌──────────────────┐      ┌──────────────────┐    ┌─────────────┐
│ breed_id  PK │◄─FK──│ cat_id        PK │◄─FK──│ cat_id        FK │    │ trick_id PK │
│ breed_name   │      │ breed_id      FK │      │ trick_id      FK │───►│ trick_name  │
│ …            │      │ name, age, …     │      │  composite PK    │    │ difficulty  │
└──────────────┘      │ image_url        │      └──────────────────┘    └─────────────┘
                      └──────────────────┘
      1 ─── many              many ─────────── many
```

| Table | Rows |
|---|---|
| `breeds` | 15 |
| `cats` | 80 (includes `image_url`) |
| `tricks` | 15 |
| `cat_tricks` | 374 — the junction table |

`cat_tricks` is the important one: a cat knows many tricks and a trick is known by
many cats, and that relationship cannot live in a column. See `cats_and_breeds/`'s
README for the longer explanation.

---

## Which section belongs to which week

| Notebook section | Teaches | Week |
|---|---|---|
| Database Schema, Create Tables | PK, FK, junction table | **2** |
| Section 1 — Meet the Cats (gallery) | Reading a result set | **1–2** |
| Section 2 — Basic SELECT | `SELECT`, `WHERE`, `ORDER BY` | **3** |
| Section 3 — JOIN Queries | `INNER`/`LEFT JOIN` | **5** |
| Section 4 — CTEs | `WITH … AS` | *beyond the core* |
| Section 5 — Window & Ranking | `ROW_NUMBER`, `RANK` | *beyond the core* |
| Section 6 — Advanced Analytics | mixed | *beyond the core* |

---

## The image feature

Every cat gets a deterministic avatar from **RoboHash** (`set=4`, kitten avatars):

```
https://robohash.org/Luna?set=4
```

- **The same name always produces the same image**, so nothing has to be stored and no
  API key is needed.
- The `image_url` column is **just text** — the database has no idea it is a picture.
- `display_utils.py` is what turns that text into a thumbnail.

`README.MP.md` records the design discussion behind this, including the options that
were rejected. It is a good short read on a genuine data-modelling question: *should
a derived, deterministic value be stored in a column at all?*

---

## Teaching notes

- **The gallery earns its place in section 1.** Students who have only seen numeric
  result sets tend to treat a query as maths homework. Seeing 80 cats appear makes
  "the database returned rows" feel like a real thing.
- Good discussion question: `image_url` is fully derivable from `name`. Should it be
  stored, or computed on display? There is a defensible answer either way, which is
  what makes it worth asking.
- If your class has limited internet, use `cats_and_breeds/` instead — identical
  schema, no external requests.
