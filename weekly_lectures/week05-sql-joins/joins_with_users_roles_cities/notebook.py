import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from plot_helpers import plot_bar, plot_hbar, plot_pie

    return plot_bar, plot_hbar, plot_pie


@app.cell
def _():
    from pathlib import Path

    import duckdb

    # Build a fresh in-memory database from the two SQL files in this
    # folder. No setup script is needed, and re-running is always safe.
    con = duckdb.connect(database=":memory:")
    con.execute(Path("01_schema.sql").read_text())
    con.execute(Path("02_records.sql").read_text())
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # OMIS 105 — Users / Roles / Cities Database

    **Course:** OMIS 105 — Introduction to Database Management Systems
    **Author:** Dr. Mahmoud Parsian
    **Tech Stack:** Python · DuckDB · Marimo

    ---

    ### About This Database

    A tiny 3-table database: `users`, `roles`, `cities`. Every user
    *may* have a `role_id` and a `city_id` that point back to
    `roles.id` and `cities.id`. A `NULL` means "not assigned yet".

    | Table | Rows | What it holds |
    |-------|-----:|----------------|
    | `roles`  | 7  | id, role, description — admin, user, superuser, tester, QA, developer, analyst |
    | `cities` | 8  | id, city, population — New York, Philadelphia, San Francisco, Sunnyvale, Cupertino, Detroit, San Jose, Santa Clara |
    | `users`  | 36 | id, name, role_id (FK), city_id (FK) — every name is unique |

    A join brings the extra columns along: join `users` to `roles`
    and you also get each user's role `description`; join to `cities`
    and you also get the city's `population` (2020 U.S. Census).

    On purpose, this dataset has gaps — the way real data usually does:

    - **2 roles are never assigned to a user** — `tester` and `QA`.
    - **2 cities have no users** — `Cupertino` and `Detroit`.
    - **5 users have no role** (`role_id` is `NULL`).
    - **4 users have no city** (`city_id` is `NULL`).
    - **2 of those users have neither** — `Zoe` and `Tom`.

    These gaps are why `INNER JOIN` and `LEFT JOIN` give *different*
    answers here. Watch the row counts as you go.

    ### 20 Practice Queries

    | Level | Count | Focus |
    |-------|-------|-------|
    | Simple | 10 | SELECT, WHERE, LIKE, IN, IS NULL, ORDER BY, LIMIT, DISTINCT, COUNT |
    | Intermediate | 10 | JOIN, LEFT JOIN + IS NULL, COALESCE, GROUP BY — 5 with plots |

    ### How to Use

    Run each cell in order. Read the markdown — it explains the *why*
    behind every query. The database is rebuilt from `01_schema.sql`
    and `02_records.sql` every time the notebook starts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Setup — Confirm the Database Loaded

    You should see 8 cities, 7 roles, and 36 users.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT 'roles'  AS table_name, COUNT(*) AS row_count FROM roles
        UNION ALL SELECT 'cities', COUNT(*) FROM cities
        UNION ALL SELECT 'users',  COUNT(*) FROM users
        ORDER BY table_name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # SIMPLE QUERIES

    ---

    ## S1 — SELECT + ORDER BY

    > *"List every user, alphabetically by name."*

    Notice the empty cells: those are `NULL` values in `role_id`
    and `city_id`.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT id, name, role_id, city_id
        FROM   users
        ORDER BY name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S2 — SELECT (all rows)

    > *"What roles exist in the system, and what does each one do?"*
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT id, role, description
        FROM   roles
        ORDER BY id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S3 — SELECT (all rows)

    > *"What cities exist in the system, largest first?"*

    `ORDER BY population DESC` sorts from the biggest number down.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT id, city, population
        FROM   cities
        ORDER BY population DESC;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S4 — WHERE + LIKE

    > *"Find every user whose name starts with 'Ja'."*

    `LIKE 'Ja%'` matches any string that starts with `Ja`.
    `%` means "anything, of any length".
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT id, name
        FROM   users
        WHERE  name LIKE 'Ja%'
        ORDER BY name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S5 — ORDER BY + LIMIT

    > *"Who are the first 5 users, by id?"*
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT id, name, role_id, city_id
        FROM   users
        ORDER BY id
        LIMIT 5;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S6 — DISTINCT

    > *"Which role ids are actually used by at least one user?"*

    `DISTINCT` removes duplicate values. Two things to notice:

    - `4` (tester) and `5` (QA) are **missing** — nobody has them.
    - `NULL` shows up as its own value — some users have no role.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT DISTINCT role_id
        FROM   users
        ORDER BY role_id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S7 — WHERE (equality)

    > *"Which users are admins (role_id = 1)?"*
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT id, name, role_id, city_id
        FROM   users
        WHERE  role_id = 1
        ORDER BY id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S8 — WHERE + IN

    > *"Which users live in city 1 (New York) or city 2 (Philadelphia)?"*

    `IN (1, 2)` is a short way to write `city_id = 1 OR city_id = 2`.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT id, name, city_id
        FROM   users
        WHERE  city_id IN (1, 2)
        ORDER BY city_id, name;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S9 — COUNT(*) vs. COUNT(column)

    > *"How many users are there — and how many have a role, and a city?"*

    - `COUNT(*)` counts **rows**.
    - `COUNT(role_id)` counts only rows where `role_id` is **not NULL**.

    So the three numbers below are different: 36, 31, and 32.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT COUNT(*)       AS total_users,
               COUNT(role_id) AS users_with_role,
               COUNT(city_id) AS users_with_city
        FROM   users;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S10 — WHERE + IS NULL

    > *"Which users have no role yet?"*

    To test for `NULL`, you **must** write `IS NULL`.
    `role_id = NULL` never matches anything — try it and see!
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT id, name, role_id, city_id
        FROM   users
        WHERE  role_id IS NULL
        ORDER BY id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # INTERMEDIATE QUERIES

    ---

    ## I1 — INNER JOIN (users + roles)

    > *"Show each user with their role name and description, not just
    > the role_id."*

    `JOIN` (short for `INNER JOIN`) keeps only rows that match on
    **both** sides. The 5 users with no role disappear, so we get
    **31** rows, not 36.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT u.id, u.name, r.role, r.description
        FROM   users u
        JOIN   roles r ON u.role_id = r.id
        ORDER BY u.id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I2 — INNER JOIN (users + cities)

    > *"Show each user with their city name and population, not just
    > the city_id."*

    Same idea: the 4 users with no city drop out — **32** rows.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT u.id, u.name, c.city, c.population
        FROM   users u
        JOIN   cities c ON u.city_id = c.id
        ORDER BY u.id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I3 — LEFT JOIN + GROUP BY

    > *"How many users hold each role — including roles nobody holds?"*

    We start `FROM roles` and `LEFT JOIN users`, so **every role**
    stays in the result. `COUNT(u.id)` counts only real matches, so
    `tester` and `QA` correctly show **0**. (With an inner `JOIN`,
    they would vanish from the list.)
    """)
    return


@app.cell
def _(con):
    df_role_counts = con.execute("""
        SELECT r.role,
               COUNT(u.id) AS num_users
        FROM   roles r
        LEFT JOIN users u ON u.role_id = r.id
        GROUP BY r.role
        ORDER BY num_users DESC, r.role;
    """).fetchdf()
    df_role_counts
    return (df_role_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Users per Role
    """)
    return


@app.cell
def _(df_role_counts, plot_bar):
    plot_bar(df_role_counts, x="role", y="num_users",
             title="Number of Users per Role", ylabel="Users")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I4 — LEFT JOIN + GROUP BY

    > *"How many users live in each city — including empty cities?"*

    Same pattern as I3, starting from `cities`. `Cupertino` and
    `Detroit` show **0**. We also show `population`. Every column in
    `SELECT` that is not inside `COUNT()` must also be in `GROUP BY`.
    """)
    return


@app.cell
def _(con):
    df_city_counts = con.execute("""
        SELECT c.city,
               c.population,
               COUNT(u.id) AS num_users
        FROM   cities c
        LEFT JOIN users u ON u.city_id = c.id
        GROUP BY c.city, c.population
        ORDER BY num_users DESC, c.city;
    """).fetchdf()
    df_city_counts
    return (df_city_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Users per City
    """)
    return


@app.cell
def _(df_city_counts, plot_bar):
    plot_bar(df_city_counts, x="city", y="num_users",
             title="Number of Users per City", ylabel="Users")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I5 — LEFT JOIN + IS NULL (Roles Never Used)

    > *"Which roles have never been assigned to a user?"*

    A `LEFT JOIN` keeps every row from `roles`, even ones with no
    match in `users`. Where there's no match, `u.id` comes back
    `NULL` — that's how we find the unused roles.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT r.id, r.role, r.description
        FROM   roles r
        LEFT JOIN users u ON r.id = u.role_id
        WHERE  u.id IS NULL
        ORDER BY r.id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I6 — LEFT JOIN + IS NULL (Cities With No Users)

    > *"Which cities have no users living there?"*

    Same idea as I5, flipped around: `LEFT JOIN` from `cities`, then
    keep only the rows where `users` had no match.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT c.id, c.city, c.population
        FROM   cities c
        LEFT JOIN users u ON c.id = u.city_id
        WHERE  u.id IS NULL
        ORDER BY c.id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I7 — Three-Table LEFT JOIN + COALESCE

    > *"Show every user with their role and city details — all 36."*

    Two `LEFT JOIN`s keep every user. `COALESCE(x, '(none)')` returns
    `x` if it is not `NULL`, otherwise `'(none)'` — a friendlier
    label than an empty cell. `population` is a number, so we leave
    it as `NULL` rather than mix in text.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT u.id,
               u.name,
               COALESCE(r.role, '(none)')        AS role,
               COALESCE(r.description, '(none)') AS description,
               COALESCE(c.city, '(none)')        AS city,
               c.population
        FROM   users u
        LEFT JOIN roles  r ON u.role_id = r.id
        LEFT JOIN cities c ON u.city_id = c.id
        ORDER BY u.id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I8 — LEFT JOIN + GROUP BY (Role Share)

    > *"What share of users hold each role — counting users with no role?"*

    This time we start `FROM users`, so every user is counted once.
    Users with no role are grouped under `'(no role)'`.
    """)
    return


@app.cell
def _(con):
    df_role_share = con.execute("""
        SELECT COALESCE(r.role, '(no role)') AS role,
               COUNT(*)                      AS num_users
        FROM   users u
        LEFT JOIN roles r ON u.role_id = r.id
        GROUP BY COALESCE(r.role, '(no role)')
        ORDER BY num_users DESC, role;
    """).fetchdf()
    df_role_share
    return (df_role_share,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Role Distribution (%)
    """)
    return


@app.cell
def _(df_role_share, plot_pie):
    plot_pie(df_role_share, labels="role", values="num_users",
             title="Share of Users by Role")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I9 — LEFT JOIN + IS NULL (Users With Missing Data)

    > *"Which users are missing a role, a city, or both?"*

    We `LEFT JOIN` users to both lookup tables. A `NULL` on the right
    side means "no match". `CASE` turns the two checks into one
    readable label.
    """)
    return


@app.cell
def _(con):
    con.execute("""
        SELECT u.id,
               u.name,
               CASE
                   WHEN r.id IS NULL AND c.id IS NULL THEN 'no role, no city'
                   WHEN r.id IS NULL                  THEN 'no role'
                   ELSE                                    'no city'
               END AS missing
        FROM   users u
        LEFT JOIN roles  r ON u.role_id = r.id
        LEFT JOIN cities c ON u.city_id = c.id
        WHERE  r.id IS NULL OR c.id IS NULL
        ORDER BY u.id;
    """).fetchdf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### How complete is our user data?

    The same `CASE` idea, now grouped over **all** users.
    """)
    return


@app.cell
def _(con):
    df_completeness = con.execute("""
        SELECT CASE
                   WHEN r.id IS NULL AND c.id IS NULL THEN 'no role, no city'
                   WHEN r.id IS NULL                  THEN 'no role only'
                   WHEN c.id IS NULL                  THEN 'no city only'
                   ELSE                                    'role and city'
               END      AS status,
               COUNT(*) AS num_users
        FROM   users u
        LEFT JOIN roles  r ON u.role_id = r.id
        LEFT JOIN cities c ON u.city_id = c.id
        GROUP BY status
        ORDER BY num_users DESC, status;
    """).fetchdf()
    df_completeness
    return (df_completeness,)


@app.cell
def _(df_completeness, plot_hbar):
    plot_hbar(df_completeness, x="num_users", y="status",
              title="User Data Completeness", xlabel="Users")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I10 — Three-Table JOIN + GROUP BY (Top Role/City Combos)

    > *"What are the 5 most common role + city combinations?"*

    Here an inner `JOIN` is the right choice: a combination needs
    *both* a role and a city. Grouping by two columns shows where
    each kind of user is concentrated — for example, admins in
    San Francisco.
    """)
    return


@app.cell
def _(con):
    df_combos = con.execute("""
        SELECT r.role,
               c.city,
               COUNT(*) AS num_users
        FROM   users u
        JOIN   roles  r ON u.role_id = r.id
        JOIN   cities c ON u.city_id = c.id
        GROUP BY r.role, c.city
        ORDER BY num_users DESC, r.role, c.city
        LIMIT 5;
    """).fetchdf()
    df_combos
    return (df_combos,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Top 5 Role + City Combinations
    """)
    return


@app.cell
def _(df_combos, plot_hbar):
    _df_plot = df_combos.assign(
        role_city=df_combos["role"] + " — " + df_combos["city"]
    )
    plot_hbar(_df_plot, x="num_users", y="role_city",
              title="Top 5 Role + City Combinations", xlabel="Users")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## Summary

    In this notebook we practiced:

    - **Simple:** `SELECT`, `WHERE` + `LIKE`, `WHERE` + `IN`,
      `IS NULL`, `ORDER BY`, `LIMIT`, `DISTINCT`,
      `COUNT(*)` vs. `COUNT(column)`
    - **Intermediate:** `INNER JOIN`, `LEFT JOIN`, `LEFT JOIN` +
      `IS NULL`, `COALESCE`, `CASE`, `GROUP BY`, multi-column `GROUP BY`

    The key lesson: **`INNER JOIN` drops rows that have no match;
    `LEFT JOIN` keeps them and fills the gaps with `NULL`.** The
    unused roles, empty cities, and users with missing data (all
    built into `02_records.sql`) make that difference visible.

    For more practice, see `users_roles_cities_join_operations.md`.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
