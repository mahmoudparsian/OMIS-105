import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import duckdb

    ## The database is a file named "my_1st_db.duckdb",
    ## created in the same folder as this notebook.
    ## This works on Mac, Windows, and molab.
    ##
    ## To keep it somewhere else, give a full path:
    ##    Mac:     DATABASE_URL = "/Users/YourName/my_1st_db.duckdb"
    ##    Windows: DATABASE_URL = r"C:\Users\YourName\my_1st_db.duckdb"

    DATABASE_URL = "my_1st_db.duckdb"
    custom_engine = duckdb.connect(DATABASE_URL, read_only=False)

    print("custom_engine=", custom_engine)
    return (custom_engine,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(custom_engine, mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE TABLE scores (
            country VARCHAR,
            name VARCHAR,
            score INT
        );
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        DESC scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        INSERT INTO scores 
        VALUES
        ('USA', 'alex', 30),
        ('USA', 'jane', 68),
        ('USA', 'barb', 90);

        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        INSERT INTO scores 
        VALUES
        ('GERMANY', 'mo', 300),
        ('GERMANY', 'ted', 168);

        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT country, 
               name, 
               score
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT name, 
               score
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT country
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT DISTINCT country
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        INSERT INTO scores 
        VALUES
        ('CANADA', 'alex', 300),
        ('CANADA', 'jane', 69),
        ('CANADA', 'barb', 94),
        ('CANADA', 'ted', 93);
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*)
        FROM scores 
        GROUP BY country;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*) AS num_of_rows
        FROM scores 
        GROUP BY country;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*) AS num_of_rows
        FROM scores 
        GROUP BY country
        ORDER BY country;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*) AS num_of_rows
        FROM scores 
        GROUP BY country
        ORDER BY country DESC;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT MIN(score) AS min_score,
               MAX(score) AS max_score,
               AVG(score) AS avg_score,
               count(*) as count_of_rows
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        INSERT INTO scores (name, score, country)
        VALUES
        ('alex', 40, 'JAPAN'),
        ('Terry', 168, 'JAPAN');

        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT * 
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        -- Find the number of people per country
        SELECT country,
               count(*) AS num_of_rows
        FROM scores 
        GROUP BY country
        ORDER BY country DESC;
        """,
        engine=custom_engine
    )
    return


if __name__ == "__main__":
    app.run()
