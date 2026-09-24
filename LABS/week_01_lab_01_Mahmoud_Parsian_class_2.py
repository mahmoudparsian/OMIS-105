import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import duckdb

    ## windows:
    ##    DATABASE_URL = 'C:/Users/YourName/my_1st_db.duckdb'
    ##    DATABASE_URL = r"C:\Users\YourName\my_1st_db.duckdb"

    DATABASE_URL = "/Users/mparsian/mp/duckdb_databases/my_1st_db.duckdb"
    cutom_engine = duckdb.connect(DATABASE_URL, read_only=False)

    print("cutom_engine=", cutom_engine)
    return (cutom_engine,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(cutom_engine, mo):
    _df = mo.sql(
        f"""
        CREATE TABLE scores (
            country VARCHAR,
            name VARCHAR,
            score INT
        );
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        DESC scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        INSERT INTO scores 
        VALUES
        ('USA', 'alex', 30),
        ('USA', 'jane', 68),
        ('USA', 'barb', 90);

        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        INSERT INTO scores 
        VALUES
        ('GERMANY', 'mo', 300),
        ('GERMANY', 'ted', 168);

        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT country, 
               name, 
               score
        FROM scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT name, 
               score
        FROM scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT country
        FROM scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT DISTINCT country
        FROM scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        INSERT INTO scores 
        VALUES
        ('CANADA', 'alex', 300),
        ('CANADA', 'jane', 69),
        ('CANADA', 'barb', 94),
        ('CANADA', 'ted', 93);
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*)
        FROM scores 
        GROUP BY country;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*) AS num_of_rows
        FROM scores 
        GROUP BY country;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*) AS num_of_rows
        FROM scores 
        GROUP BY country
        ORDER BY country;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*) AS num_of_rows
        FROM scores 
        GROUP BY country
        ORDER BY country DESC;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT MIN(score) AS min_score,
               MAX(score) AS max_score,
               AVG(score) AS avg_score,
               count(*) as count_of_rows
        FROM scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        INSERT INTO scores (name, score, country)
        VALUES
        ('alex', 40, 'JAPAN'),
        ('Terry', 168, 'JAPAN');

        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM scores;
        """,
        engine=cutom_engine
    )
    return


@app.cell
def _(cutom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*) AS num_of_rows
        FROM scores 
        GROUP BY country
        ORDER BY country DESC;
        """,
        engine=cutom_engine
    )
    return


if __name__ == "__main__":
    app.run()
