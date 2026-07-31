"""
display_utils.py
================
Utility functions for displaying DuckDB query results
as nicely formatted tables in Jupyter Notebooks.
Includes support for rendering cat avatar images inline.

Usage in notebook:
    from display_utils import run_query, show_table, run_and_show, show_gallery
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


def show_gallery(df, name_col='name', image_col='image_url',
                 detail_cols=None, title=None, columns=4, img_size=120):
    """
    Display cats as a visual gallery with avatar images in a grid layout.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing cat data with image URLs.
    name_col : str
        Column name for the cat's display name.
    image_col : str
        Column name containing the image URL.
    detail_cols : list of str, optional
        Additional columns to show below the name (e.g., ['breed', 'price']).
    title : str, optional
        Gallery title.
    columns : int
        Number of columns in the grid (default 4).
    img_size : int
        Image size in pixels (default 120).
    """
    if detail_cols is None:
        detail_cols = []

    styles = f"""
    <style>
        .cat-gallery {{
            display: grid;
            grid-template-columns: repeat({columns}, 1fr);
            gap: 16px;
            padding: 16px 0;
        }}
        .cat-card {{
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 12px;
            text-align: center;
            background: #ffffff;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .cat-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .cat-card img {{
            width: {img_size}px;
            height: {img_size}px;
            border-radius: 50%;
            border: 3px solid #e8f4fd;
            object-fit: cover;
            background: #f0f0f0;
        }}
        .cat-card .cat-name {{
            font-weight: 600;
            font-size: 13px;
            color: #2c3e50;
            margin: 8px 0 4px 0;
        }}
        .cat-card .cat-detail {{
            font-size: 11px;
            color: #7f8c8d;
            margin: 2px 0;
        }}
        .gallery-title {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 15px;
            font-weight: 600;
            color: #2c3e50;
            margin: 12px 0 4px 0;
        }}
        .gallery-count {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11px;
            color: #7f8c8d;
            margin: 2px 0 8px 0;
        }}
    </style>
    """

    title_html = ""
    if title:
        title_html = f'<div class="gallery-title">{title}</div>'

    count_html = f'<div class="gallery-count">{len(df)} cats</div>'

    cards_html = ""
    for _, row in df.iterrows():
        details = ""
        for col in detail_cols:
            if col in row.index:
                val = row[col]
                if col == 'price':
                    val = f"${val:,}"
                details += f'<div class="cat-detail">{col}: {val}</div>'

        cards_html += f"""
        <div class="cat-card">
            <img src="{row[image_col]}" alt="{row[name_col]}">
            <div class="cat-name">{row[name_col]}</div>
            {details}
        </div>
        """

    html = f"""
    {styles}
    {title_html}
    {count_html}
    <div class="cat-gallery">
        {cards_html}
    </div>
    """

    display(HTML(html))


def show_table_with_images(df, image_col='image_url', title=None,
                           max_rows=30, img_size=50):
    """
    Display a DataFrame as a styled table with inline thumbnail images.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with an image URL column.
    image_col : str
        Column name containing the image URL.
    title : str, optional
        Title above the table.
    max_rows : int
        Maximum rows to display.
    img_size : int
        Thumbnail size in pixels.
    """
    display_df = df.head(max_rows).copy()
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = '#'

    # Convert image URLs to inline <img> tags
    if image_col in display_df.columns:
        display_df[image_col] = display_df[image_col].apply(
            lambda url: f'<img src="{url}" width="{img_size}" '
                        f'height="{img_size}" style="border-radius:50%; '
                        f'border:2px solid #e8f4fd;">'
        )

    styles = """
    <style>
        .img-table {
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 13px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-width: 400px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .img-table thead tr {
            background-color: #2c3e50;
            color: #ffffff;
            text-align: left;
            font-weight: bold;
        }
        .img-table th, .img-table td {
            padding: 6px 12px;
            border-bottom: 1px solid #e0e0e0;
            vertical-align: middle;
        }
        .img-table tbody tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .img-table tbody tr:nth-child(odd) {
            background-color: #ffffff;
        }
        .img-table tbody tr:hover {
            background-color: #e8f4fd;
        }
        .img-table tbody tr:last-of-type {
            border-bottom: 3px solid #2c3e50;
        }
        .img-table-title {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 15px;
            font-weight: 600;
            color: #2c3e50;
            margin: 12px 0 4px 0;
        }
        .img-table-count {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11px;
            color: #7f8c8d;
            margin: 2px 0 8px 0;
        }
    </style>
    """

    title_html = ""
    if title:
        title_html = f'<div class="img-table-title">{title}</div>'

    total = len(df)
    shown = len(display_df)
    count_msg = f"Showing {shown} of {total} rows" if total > shown else f"{total} rows"
    count_html = f'<div class="img-table-count">{count_msg}</div>'

    table_html = display_df.to_html(classes='img-table', border=0,
                                     escape=False)

    display(HTML(styles + title_html + count_html + table_html))
