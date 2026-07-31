"""
display_utils.py
================
Utility functions for displaying DuckDB query results
as nicely formatted tables in Jupyter Notebooks.

Usage in notebook:
    from display_utils import run_query, show_table
"""

import duckdb
from IPython.display import display, HTML


def run_query(con, sql):
    """
    Execute a SQL query and return the result as a Pandas DataFrame.

    Parameters
    ----------
    con : duckdb.DuckDBPyConnection
        Active DuckDB connection.
    sql : str
        SQL query string.

    Returns
    -------
    pandas.DataFrame
        Query result.
    """
    return con.execute(sql).fetchdf()


def show_table(df, title=None, max_rows=50):
    """
    Display a DataFrame as a beautifully styled HTML table
    with row numbers, alternating row colors, and a title.

    Parameters
    ----------
    df : pandas.DataFrame
        The data to display.
    title : str, optional
        Title displayed above the table.
    max_rows : int
        Maximum number of rows to display.
    """
    display_df = df.head(max_rows).copy()
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = '#'

    styles = """
    <style>
        .styled-table {
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 13px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-width: 400px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .styled-table thead tr {
            background-color: #2c3e50;
            color: #ffffff;
            text-align: left;
            font-weight: bold;
        }
        .styled-table th, .styled-table td {
            padding: 8px 14px;
            border-bottom: 1px solid #e0e0e0;
        }
        .styled-table tbody tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .styled-table tbody tr:nth-child(odd) {
            background-color: #ffffff;
        }
        .styled-table tbody tr:hover {
            background-color: #e8f4fd;
            transition: background-color 0.2s ease;
        }
        .styled-table tbody tr:last-of-type {
            border-bottom: 3px solid #2c3e50;
        }
        .table-title {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 15px;
            font-weight: 600;
            color: #2c3e50;
            margin: 12px 0 4px 0;
        }
        .row-count {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11px;
            color: #7f8c8d;
            margin: 2px 0 8px 0;
        }
    </style>
    """

    title_html = ""
    if title:
        title_html = f'<div class="table-title">{title}</div>'

    total = len(df)
    shown = len(display_df)
    count_msg = f"Showing {shown} of {total} rows" if total > shown else f"{total} rows"
    count_html = f'<div class="row-count">{count_msg}</div>'

    table_html = display_df.to_html(classes='styled-table', border=0)

    display(HTML(styles + title_html + count_html + table_html))


def run_and_show(con, sql, title=None, max_rows=50):
    """
    Execute a query and display the result as a styled table.
    Combines run_query() and show_table() in one call.

    Parameters
    ----------
    con : duckdb.DuckDBPyConnection
        Active DuckDB connection.
    sql : str
        SQL query string.
    title : str, optional
        Title displayed above the table.
    max_rows : int
        Maximum rows to display.

    Returns
    -------
    pandas.DataFrame
        Query result (for further use / plotting).
    """
    df = run_query(con, sql)
    show_table(df, title=title, max_rows=max_rows)
    return df
