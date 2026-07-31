import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # GROUP BY Tutorial 101

    * Database Environment: DuckDB
    * Last updated: May 25, 2026
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Description

    ```
    1. The GROUP BY clause in SQL gathers rows
    with identical values into summary rows.
    This is a reduction operation.

    2. In SQL, the GROUP BY clause functions as
    a reduction operation by collapsing multiple
    individual rows into a single summary row
    based on shared values in specified columns.

    3. It is most frequently used with aggregate
    functions like COUNT(), SUM(), AVG(), MAX(),
    and MIN() to run calculations on each separate
    group.
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SQL Syntax

    ```sql
    SELECT column_name(s),
           AGGREGATE_FUNCTION(column_name)
    FROM table_name
    WHERE condition
    GROUP BY column_name(s);
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: import DuckDB and matplotlib
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.style.use('ggplot')
    import duckdb

    return duckdb, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create a Table with 2 Columns
    """)
    return


@app.cell
def _(duckdb):
    duckdb.sql("CREATE TABLE scores(player VARCHAR, score INT)")
    duckdb.sql("SHOW TABLES").show()
    duckdb.sql("DESCRIBE scores").show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Insert 4 rows for Alex
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("INSERT INTO scores(player, score) VALUES('Alex', 10)")
    duckdb.sql("INSERT INTO scores(player, score) VALUES('Alex', 20)")
    duckdb.sql("INSERT INTO scores(player, score) VALUES('Alex', 30)")
    duckdb.sql("INSERT INTO scores(player, score) VALUES('Alex', NULL)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Insert 4 rows for Jane
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("INSERT INTO scores(player, score) VALUES('Jane', 70)")
    duckdb.sql("INSERT INTO scores(player, score) VALUES('Jane', 90)")
    duckdb.sql("INSERT INTO scores(player, score) VALUES('Jane', NULL)")
    duckdb.sql("INSERT INTO scores(player, score) VALUES('Jane', NULL)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## View Table
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("SELECT * FROM scores").show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Find Average of scores per player
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("""
        SELECT player, 
               AVG(score) AS avg_score
        FROM scores 
        GROUP BY player
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **NOTE:**

    * `AVG()` ignores `NULL` values.

    * Alex has scores `{10, 20, 30, NULL}`

    * the average is `(10+20+30)/3 = 20.0`, not `(10+20+30+0)/4`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot: Average score per player
    """)
    return


@app.cell
def _(duckdb, plt, scores):
    duckdb.sql("""
        SELECT player, 
               AVG(score) AS avg_score
        FROM scores 
        GROUP BY player
        ORDER BY player
    """).df().plot.bar(x='player', y='avg_score', title='Average Score per Player', legend=False)
    plt.ylabel('Average Score')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Find Minimum and Maximum of scores per player
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("""
        SELECT player, 
               MIN(score) AS min_score, 
               MAX(score) AS max_score
        FROM scores 
        GROUP BY player
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot: Min and Max scores per player
    """)
    return


@app.cell
def _(duckdb, plt, scores):
    duckdb.sql("""
        SELECT player, 
               MIN(score) AS min_score, 
               MAX(score) AS max_score
        FROM scores 
        GROUP BY player
        ORDER BY player
    """).df().plot.bar(x='player', y=['min_score', 'max_score'], title='Min & Max Scores per Player')
    plt.ylabel('Score')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## COUNT(*) vs COUNT(column_name) per player

    ### `COUNT(*)` counts all rows in the group, including NULLs.

    ### `COUNT(column_name)` counts only non-NULL values in that column.
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("""
        SELECT player, 
               COUNT(*) AS total_rows, 
               COUNT(score) AS non_null_scores
        FROM scores 
        GROUP BY player
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **NOTE:** Alex has 4 rows but only 3 non-NULL scores.
    Jane has 4 rows but only 2 non-NULL scores.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot: COUNT(*) vs COUNT(score)
    """)
    return


@app.cell
def _(duckdb, plt, scores):
    duckdb.sql("""
        SELECT player, 
               COUNT(*) AS total_rows, 
               COUNT(score) AS non_null_scores
        FROM scores 
        GROUP BY player
        ORDER BY player
    """).df().plot.bar(x='player', y=['total_rows', 'non_null_scores'], title='COUNT(*) vs COUNT(score)')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Find Sum of scores per player
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("""
        SELECT player, 
               SUM(score) AS total_score
        FROM scores 
        GROUP BY player
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **NOTE:** Like `AVG()`, `SUM()` ignores `NULL` values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot: Total score per player
    """)
    return


@app.cell
def _(duckdb, plt, scores):
    duckdb.sql("""
        SELECT player, 
               SUM(score) AS total_score
        FROM scores 
        GROUP BY player
        ORDER BY player
    """).df().plot.bar(x='player', y='total_score', title='Total Score per Player', legend=False, color=['#4C72B0', '#DD8452'])
    plt.ylabel('Total Score')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Combine multiple aggregates in one query
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("""
        SELECT player, 
               COUNT(*) AS total_rows,
               COUNT(score) AS non_null_scores,
               SUM(score) AS total_score,
               AVG(score) AS avg_score,
               MIN(score) AS min_score,
               MAX(score) AS max_score
        FROM scores 
        GROUP BY player
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## HAVING: filter groups after aggregation

    #### The WHERE clause filters rows BEFORE grouping.
    #### The HAVING clause filters groups AFTER aggregation.
    """)
    return


@app.cell
def _(duckdb, scores):
    # Find players whose average score is greater than 50
    duckdb.sql("""
        SELECT player, 
               AVG(score) AS avg_score
        FROM scores 
        GROUP BY player
        HAVING AVG(score) > 50
    """).show()
    return


@app.cell
def _(duckdb, scores):
    # Find players who have more than 2 non-NULL scores
    duckdb.sql("""
        SELECT player, 
               COUNT(score) AS non_null_scores
        FROM scores 
        GROUP BY player
        HAVING COUNT(score) > 2
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## STRING_AGG and LIST: concatenate grouped values

    STRING_AGG() concatenates values into a
    comma-separated string. LIST() collects
    values into a DuckDB list (array).
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("""
        SELECT player, 
               STRING_AGG(score::VARCHAR, ', ') AS scores_csv,
               LIST(score) AS scores_list
        FROM scores 
        GROUP BY player
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **NOTE:** Both `STRING_AGG()` and `LIST()` skip
    `NULL` values by default.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## GROUP BY with multiple columns

    First, let us add a 'team' column to our table.
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("ALTER TABLE scores ADD COLUMN team VARCHAR")
    duckdb.sql("UPDATE scores SET team = 'Red' WHERE player = 'Alex'")
    duckdb.sql("UPDATE scores SET team = 'Blue' WHERE player = 'Jane'")
    return


@app.cell
def _(duckdb, scores):
    # Now insert a player on a different team
    duckdb.sql("INSERT INTO scores(player, score, team) VALUES('Alex', 50, 'Blue')")
    duckdb.sql("INSERT INTO scores(player, score, team) VALUES('Jane', 40, 'Red')")
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("SELECT * FROM scores").show()
    return


@app.cell
def _(duckdb, scores):
    # GROUP BY two columns: team and player
    duckdb.sql("""
        SELECT team,
               player, 
               COUNT(score) AS games,
               SUM(score) AS total_score,
               AVG(score) AS avg_score
        FROM scores 
        GROUP BY team, player
        ORDER BY team, player
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot: Total score by team and player
    """)
    return


@app.cell
def _(duckdb, plt, scores):
    duckdb.sql("""
        SELECT team || ' - ' || player AS team_player,
               SUM(score) AS total_score
        FROM scores 
        GROUP BY team, player
        ORDER BY team, player
    """).df().plot.bar(x='team_player', y='total_score', title='Total Score by Team & Player', legend=False, color=['#4C72B0', '#DD8452', '#55A868', '#C44E52'])
    plt.ylabel('Total Score')
    plt.xlabel('')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(duckdb, scores):
    # GROUP BY team only
    duckdb.sql("""
        SELECT team,
               COUNT(score) AS games,
               SUM(score) AS total_score,
               AVG(score) AS avg_score
        FROM scores 
        GROUP BY team
        ORDER BY team
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot: Team total scores
    """)
    return


@app.cell
def _(duckdb, plt, scores):
    duckdb.sql("""
        SELECT team,
               SUM(score) AS total_score
        FROM scores 
        GROUP BY team
        ORDER BY team
    """).df().plot.bar(x='team', y='total_score', title='Total Score by Team', legend=False, color=['#4C72B0', '#C44E52'])
    plt.ylabel('Total Score')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## WHERE + GROUP BY + HAVING together

    Execution order: WHERE filters rows first,
    then GROUP BY groups them, then HAVING
    filters the groups.
    """)
    return


@app.cell
def _(duckdb, scores):
    # Among non-NULL scores > 15, find teams 
    # whose average exceeds 40
    duckdb.sql("""
        SELECT team,
               AVG(score) AS avg_score,
               COUNT(score) AS num_scores
        FROM scores 
        WHERE score > 15
        GROUP BY team
        HAVING AVG(score) > 40
        ORDER BY avg_score DESC
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## GROUP BY with ORDER BY on aggregate
    """)
    return


@app.cell
def _(duckdb, scores):
    # Rank teams by total score (descending)
    duckdb.sql("""
        SELECT team,
               SUM(score) AS total_score
        FROM scores 
        GROUP BY team
        ORDER BY total_score DESC
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rank players by score
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("""
        SELECT player, 
               score, 
               RANK() OVER(ORDER BY score DESC) as rnk 
        FROM scores
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rank each player by score
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("""
        SELECT player, 
               score, 
               RANK() OVER(PARTITION BY player ORDER BY score DESC) as rnk 
        FROM scores
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Find top-2 score per player
    """)
    return


@app.cell
def _(duckdb, scores):
    duckdb.sql("""
        WITH ranked AS (
            SELECT player, 
                   score, 
                   RANK() OVER (
                        PARTITION BY player 
                        ORDER BY score DESC
                   ) as rnk 
            FROM scores
        ) 
        SELECT player, 
               score, 
               rnk 
        FROM ranked 
        WHERE rnk <= 2
    """).show()
    return


if __name__ == "__main__":
    app.run()
