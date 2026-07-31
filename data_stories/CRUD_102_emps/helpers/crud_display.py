"""
Display and plotting helpers for the CRUD 101 Employees notebook.

Teaching goal:
- Keep SQL notebook cells clean.
- Hide display/table/plot formatting details from students.
- Make result sets easy to read with row numbers and optional image rendering.
"""

from __future__ import annotations

from pathlib import Path
from IPython.display import display, HTML, Markdown
import matplotlib.pyplot as plt
import pandas as pd


def show_title(title: str, level: int = 3) -> None:
    """Display a Markdown heading."""
    level = max(1, min(level, 6))
    display(Markdown(f"{'#' * level} {title}"))


def show_sql(sql: str) -> None:
    """Display SQL in a readable code block."""
    clean_sql = sql.strip()
    display(Markdown(f"```sql\n{clean_sql}\n```"))


def _render_image_url(url: str, size: int = 54) -> str:
    """Return small HTML image for a URL."""
    if pd.isna(url) or not str(url).startswith("http"):
        return ""
    safe_url = str(url)
    return (
        f'<img src="{safe_url}" width="{size}" height="{size}" '
        f'style="border-radius:50%; object-fit:cover; border:1px solid #ddd;" />'
    )


def display_table(
    df: pd.DataFrame,
    title: str | None = None,
    max_rows: int | None = None,
    render_images: bool = True,
) -> pd.DataFrame:
    """
    Display a DataFrame with row numbers and optional image rendering.

    Returns the original DataFrame so it can be reused for plots.
    """
    if title:
        show_title(title, level=4)

    out = df.copy()
    if max_rows is not None:
        out = out.head(max_rows)

    out.insert(0, "row_num", range(1, len(out) + 1))

    if render_images and "image_url" in out.columns:
        out["avatar"] = out["image_url"].apply(_render_image_url)
        cols = ["row_num", "avatar"] + [c for c in out.columns if c not in ["row_num", "avatar"]]
        out = out[cols]
        html = out.to_html(escape=False, index=False)
    else:
        html = out.to_html(index=False)

    display(HTML(
        """
        <style>
            table.dataframe {border-collapse: collapse; font-size: 14px; margin: 8px 0 18px 0;}
            table.dataframe th {background: #f3f4f6; color: #111827; padding: 8px; border: 1px solid #d1d5db; text-align: left;}
            table.dataframe td {padding: 8px; border: 1px solid #e5e7eb; vertical-align: middle;}
            table.dataframe tr:nth-child(even) {background: #fafafa;}
        </style>
        """ + html
    ))
    return df


def run_sql(
    con,
    sql: str,
    title: str | None = None,
    show_query: bool = True,
    render_images: bool = True,
    max_rows: int | None = None,
) -> pd.DataFrame:
    """
    Run SQL using DuckDB, display the SQL, display the result table,
    and return the result as a pandas DataFrame.
    """
    if title:
        show_title(title, level=3)
    if show_query:
        show_sql(sql)
    df = con.execute(sql).df()
    return display_table(df, max_rows=max_rows, render_images=render_images)


def execute_sql(con, sql: str, title: str | None = None, show_query: bool = True) -> None:
    """Run SQL that does not return a result set, such as INSERT, UPDATE, DELETE, CREATE."""
    if title:
        show_title(title, level=3)
    if show_query:
        show_sql(sql)
    con.execute(sql)
    display(Markdown("✅ SQL statement executed successfully."))


def plot_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize: tuple[int, int] = (8, 4),
    rotation: int = 0,
) -> None:
    """Create a simple bar chart from a query result."""
    ax = df.plot(kind="bar", x=x, y=y, legend=False, figsize=figsize)
    ax.set_title(title)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.tick_params(axis="x", rotation=rotation)
    plt.tight_layout()
    plt.show()


def plot_horizontal_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize: tuple[int, int] = (8, 4),
) -> None:
    """Create a horizontal bar chart from a query result."""
    ax = df.plot(kind="barh", x=x, y=y, legend=False, figsize=figsize)
    ax.set_title(title)
    ax.set_xlabel(xlabel or y)
    ax.set_ylabel(ylabel or x)
    plt.tight_layout()
    plt.show()


def plot_pie(
    df: pd.DataFrame,
    labels: str,
    values: str,
    title: str,
    figsize: tuple[int, int] = (6, 6),
) -> None:
    """Create a pie chart from a query result."""
    ax = df.set_index(labels)[values].plot(kind="pie", autopct="%1.0f%%", figsize=figsize)
    ax.set_title(title)
    ax.set_ylabel("")
    plt.tight_layout()
    plt.show()


def plot_line(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize: tuple[int, int] = (8, 4),
) -> None:
    """Create a line chart from a query result."""
    ax = df.plot(kind="line", x=x, y=y, marker="o", legend=False, figsize=figsize)
    ax.set_title(title)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    plt.tight_layout()
    plt.show()
