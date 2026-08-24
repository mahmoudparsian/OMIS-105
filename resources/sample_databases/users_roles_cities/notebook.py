import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium", sql_output="pandas")


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
    import duckdb

    # This notebook queries the DuckDB database built by create_duckdb.sh.
    # Run that script first (from this folder):
    #     ./create_duckdb.sh
    con = duckdb.connect("users_roles_cities.duckdb")
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
    has a `role_id` and a `city_id` that point back to `roles.id` and
    `cities.id`.

    | Table | Rows | What it holds |
    |-------|-----:|----------------|
    | `roles`  | 5  | id + role name (admin, user, superuser, tester, QA) |
    | `cities` | 6  | id + city name |
    | `users`  | 17 | id, name, role_id (FK), city_id (FK) |

    On purpose, this dataset is a little messy — the way real data
    usually is:

    - **2 roles are never assigned to a user** — `tester` and `QA`.
    - **2 cities have no residents** — `Cupertino` and `Detroit`.
    - **3 names repeat** — `Max`, `Barb`, and `Jane` each appear twice,
      as different people with different `id`s.

    These give us real rows to find with `LEFT JOIN ... IS NULL` and
    `GROUP BY ... HAVING` — see I5, I6, and I9 below.

    ### 20 Practice Queries

    | Level | Count | Focus |
    |-------|-------|-------|
    | Simple | 10 | SELECT, WHERE, LIKE, ORDER BY, LIMIT, DISTINCT, IN, COUNT |
    | Intermediate | 10 | JOIN, GROUP BY, LEFT JOIN + IS NULL, HAVING — 5 with plots |

    ### How to Use

    Run each cell in order. Read the markdown — it explains the *why*
    behind every query. In Marimo, SQL cells run directly against DuckDB
    — no Python wrappers needed!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    # Setup — Confirm the Database Loaded
    """)
    return


@app.cell
def _(cities, con, mo, roles, users):
    _df = mo.sql(
        f"""
        SELECT 'roles'  AS table_name, COUNT(*) AS row_count FROM roles
        UNION ALL SELECT 'cities', COUNT(*) FROM cities
        UNION ALL SELECT 'users',  COUNT(*) FROM users
        ORDER BY table_name;
        """,
        engine=con
    )
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
    """)
    return


@app.cell
def _(con, mo, users):
    _df = mo.sql(
        f"""
        SELECT id, name, role_id, city_id
        FROM   users
        ORDER BY name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S2 — SELECT (all rows)

    > *"What roles exist in the system?"*
    """)
    return


@app.cell
def _(con, mo, roles):
    _df = mo.sql(
        f"""
        SELECT id, role
        FROM   roles
        ORDER BY id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S3 — SELECT (all rows)

    > *"What cities exist in the system?"*
    """)
    return


@app.cell
def _(cities, con, mo):
    _df = mo.sql(
        f"""
        SELECT id, city
        FROM   cities
        ORDER BY id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S4 — WHERE + LIKE

    > *"Find every user whose name starts with 'Ja'."*

    `LIKE 'Ja%'` matches any string that starts with `Ja`.
    """)
    return


@app.cell
def _(con, mo, users):
    _df = mo.sql(
        f"""
        SELECT id, name
        FROM   users
        WHERE  name LIKE 'Ja%'
        ORDER BY name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S5 — ORDER BY + LIMIT

    > *"Who are the first 5 users, by id?"*
    """)
    return


@app.cell
def _(con, mo, users):
    _df = mo.sql(
        f"""
        SELECT id, name, role_id, city_id
        FROM   users
        ORDER BY id
        LIMIT 5;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S6 — DISTINCT

    > *"What distinct names appear in `users`?"*

    `DISTINCT` collapses duplicate rows — since `Max`, `Barb`, and
    `Jane` each belong to two different people, this list is
    *shorter* than the full `users` table.
    """)
    return


@app.cell
def _(con, mo, users):
    _df = mo.sql(
        f"""
        SELECT DISTINCT name
        FROM   users
        ORDER BY name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S7 — WHERE (equality)

    > *"Which users are admins (role_id = 1)?"*
    """)
    return


@app.cell
def _(con, mo, users):
    _df = mo.sql(
        f"""
        SELECT id, name, role_id, city_id
        FROM   users
        WHERE  role_id = 1
        ORDER BY id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S8 — WHERE + IN

    > *"Which users live in city 1 (New York) or city 2 (Philadelphia)?"*
    """)
    return


@app.cell
def _(con, mo, users):
    _df = mo.sql(
        f"""
        SELECT id, name, city_id
        FROM   users
        WHERE  city_id IN (1, 2)
        ORDER BY city_id, name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S9 — COUNT (simple aggregate)

    > *"How many users are there in total?"*
    """)
    return


@app.cell
def _(con, mo, users):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS total_users
        FROM   users;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## S10 — ORDER BY (multiple columns)

    > *"List every user grouped by city, then alphabetically within
    > each city."*
    """)
    return


@app.cell
def _(con, mo, users):
    _df = mo.sql(
        f"""
        SELECT id, name, city_id
        FROM   users
        ORDER BY city_id, name;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ---
    # INTERMEDIATE QUERIES

    ---

    ## I1 — JOIN (users + roles)

    > *"Show each user with their role name, not just the role_id."*
    """)
    return


@app.cell
def _(con, mo, roles, users):
    _df = mo.sql(
        f"""
        SELECT u.id, u.name, r.role
        FROM   users u
        JOIN   roles r ON u.role_id = r.id
        ORDER BY u.id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I2 — JOIN (users + cities)

    > *"Show each user with their city name, not just the city_id."*
    """)
    return


@app.cell
def _(cities, con, mo, users):
    _df = mo.sql(
        f"""
        SELECT u.id, u.name, c.city
        FROM   users u
        JOIN   cities c ON u.city_id = c.id
        ORDER BY u.id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I3 — JOIN + GROUP BY

    > *"How many users hold each role?"*
    """)
    return


@app.cell
def _(con, mo, roles, users):
    df_role_counts = mo.sql(
        f"""
        SELECT r.role,
               COUNT(u.id) AS num_users
        FROM   roles r
        JOIN   users u ON u.role_id = r.id
        GROUP BY r.role
        ORDER BY num_users DESC;
        """,
        engine=con
    )
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
    ## I4 — JOIN + GROUP BY

    > *"How many users live in each city?"*
    """)
    return


@app.cell
def _(cities, con, mo, users):
    df_city_counts = mo.sql(
        f"""
        SELECT c.city,
               COUNT(u.id) AS num_users
        FROM   cities c
        JOIN   users u ON u.city_id = c.id
        GROUP BY c.city
        ORDER BY num_users DESC;
        """,
        engine=con
    )
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
def _(con, mo, roles, users):
    _df = mo.sql(
        f"""
        SELECT r.id, r.role
        FROM   roles r
        LEFT JOIN users u ON r.id = u.role_id
        WHERE  u.id IS NULL
        ORDER BY r.id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I6 — LEFT JOIN + IS NULL (Cities With No Residents)

    > *"Which cities have no users living there?"*

    Same idea as I5, flipped around: `LEFT JOIN` from `cities`, then
    keep only the rows where `users` had no match.
    """)
    return


@app.cell
def _(cities, con, mo, users):
    _df = mo.sql(
        f"""
        SELECT c.id, c.city
        FROM   cities c
        LEFT JOIN users u ON c.id = u.city_id
        WHERE  u.id IS NULL
        ORDER BY c.id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I7 — Three-Table JOIN

    > *"Show every user with their role name AND city name, side by
    > side."*
    """)
    return


@app.cell
def _(cities, con, mo, roles, users):
    _df = mo.sql(
        f"""
        SELECT u.id, u.name, r.role, c.city
        FROM   users u
        JOIN   roles  r ON u.role_id = r.id
        JOIN   cities c ON u.city_id = c.id
        ORDER BY u.id;
        """,
        engine=con
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I8 — JOIN + GROUP BY (Role Share)

    > *"What percentage of users hold each role?"*
    """)
    return


@app.cell
def _(con, mo, roles, users):
    df_role_share = mo.sql(
        f"""
        SELECT r.role,
               COUNT(u.id) AS num_users
        FROM   roles r
        JOIN   users u ON u.role_id = r.id
        GROUP BY r.role
        ORDER BY num_users DESC;
        """,
        engine=con
    )
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
    ## I9 — GROUP BY + HAVING (Repeated Names)

    > *"Which names belong to more than one user?"*

    `HAVING COUNT(*) > 1` filters *groups*, not rows — it keeps only
    the names that show up more than once, which is how we catch
    `Max`, `Barb`, and `Jane`, each a different person sharing a name.
    """)
    return


@app.cell
def _(con, mo, users):
    df_dup_names = mo.sql(
        f"""
        SELECT name,
               COUNT(*) AS num_users
        FROM   users
        GROUP BY name
        HAVING COUNT(*) > 1
        ORDER BY num_users DESC, name;
        """,
        engine=con
    )
    return (df_dup_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Visualizing: Names Shared by More Than One User
    """)
    return


@app.cell
def _(df_dup_names, plot_hbar):
    plot_hbar(df_dup_names, x="num_users", y="name",
              title="Repeated Names in `users`", xlabel="Users")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## I10 — Three-Table JOIN + GROUP BY (Top Role/City Combos)

    > *"What are the 5 most common role + city combinations?"*

    Grouping by two columns at once (`role`, `city`) shows *where each
    kind of user is concentrated* — for example, most admins turn out
    to live in San Francisco.
    """)
    return


@app.cell
def _(cities, con, mo, roles, users):
    df_combos = mo.sql(
        f"""
        SELECT r.role,
               c.city,
               COUNT(*) AS num_users
        FROM   users u
        JOIN   roles  r ON u.role_id = r.id
        JOIN   cities c ON u.city_id = c.id
        GROUP BY r.role, c.city
        ORDER BY num_users DESC, r.role, c.city
        LIMIT 5;
        """,
        engine=con
    )
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
      `ORDER BY`, `LIMIT`, `DISTINCT`, `COUNT(*)`
    - **Intermediate:** `JOIN`, `GROUP BY`, `LEFT JOIN` + `IS NULL`,
      `HAVING`, multi-column `GROUP BY`

    The 2 unused roles, 2 empty cities, and 3 repeated names (built
    into `02_records.sql`) gave I5, I6, and I9 real rows to find — in
    a perfectly tidy dataset, those queries would return nothing to
    look at.

    ---
    *OMIS 105 — Introduction to Database Management Systems — Fall 2026*
    """)
    return


if __name__ == "__main__":
    app.run()
