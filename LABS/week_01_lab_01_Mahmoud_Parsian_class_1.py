import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb

    ## windows:
    ##    DATABASE_URL = 'C:/Users/YourName/my_1st_db.duckdb'
    ##    DATABASE_URL = r"C:\Users\YourName\my_1st_db.duckdb"

    DATABASE_URL = "/Users/mparsian/mp/duckdb_databases/first_database.duckdb"
    custom_engine = duckdb.connect(DATABASE_URL, read_only=False)

    print("custom_engine=", custom_engine)
    return (custom_engine,)


@app.cell
def _():
    return


@app.cell
def _(custom_engine, mo):
    _df = mo.sql(
        f"""
        CREATE TABLE scores(
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
        ('USA', 'alex', 20),
        ('USA', 'jane', 40),
        ('USA', 'dave', 80);
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
        ('INDIA', 'raj', 30),
        ('INDIA', 'ab', 45),
        ('INDIA', 'david', 85);
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
        SELECT name, score 
        FROM scores;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT MIN(score) as min_score,
               MAX(score) as max_score,
               AVG(score) as avg_score
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
        ('SPAIN', 'al', 100),
        ('SPAIN', 'barb', 40),
        ('SPAIN', 'max', 190);
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
        SELECT MIN(score) as min_score,
               MAX(score) as max_score,
               AVG(score) as avg_score
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
        ('CHINA', 'sam', 78),
        ('CHINA', 'kun', 88);
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

        SELECT DISTINCT country 
        FROM scores
        ORDER BY country;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT DISTINCT country 
        FROM scores
        ORDER BY country DESC;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT score
        FROM scores
        ORDER BY score;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT score
        FROM scores
        ORDER BY score DESC;
        """,
        engine=custom_engine
    )
    return


@app.cell
def _(custom_engine, mo, scores):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) 
        FROM scores;
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
        SELECT country,
               count(*) AS count_of_scores
        FROM scores
        GROUP BY country;
        """,
        engine=custom_engine
    )
    return


if __name__ == "__main__":
    app.run()
