"""
display_utils.py  –  Pretty-print DuckDB / Pandas results in Jupyter notebooks.

Usage
-----
    from utils import show, show_query, show_cards, show_table_with_images

    show(df)                       # display a DataFrame as a styled table
    show_query(con, sql)           # run SQL, then display the result
    show(df, title="Top Earners") # optional title above the table
    show_cards(df)                 # display employee cards with avatars
    show_table_with_images(df)     # table with image_url rendered as avatars
"""

import pandas as pd
from IPython.display import display, HTML

# ── Colour palette (SCU-inspired) ──────────────────────────────────────────
_HEADER_BG   = "#2C3E50"   # dark blue-grey
_HEADER_FG   = "#FFFFFF"
_ROW_EVEN    = "#F8F9FA"
_ROW_ODD     = "#FFFFFF"
_BORDER      = "#DEE2E6"
_TITLE_COLOR = "#1A5276"


def _styled_html(df: pd.DataFrame, title: str | None = None) -> str:
    """Return an HTML string with a nicely formatted table."""
    # Add a 1-based row-number column
    df = df.copy()
    df.insert(0, "#", range(1, len(df) + 1))

    # Start building HTML
    parts: list[str] = []

    if title:
        parts.append(
            f'<h4 style="color:{_TITLE_COLOR}; font-family:Helvetica Neue,Helvetica,Arial,sans-serif; '
            f'margin-bottom:6px;">{title}</h4>'
        )

    parts.append(
        '<div style="overflow-x:auto; max-height:600px; overflow-y:auto;">'
        '<table style="border-collapse:collapse; font-family:Helvetica Neue,Helvetica,Arial,sans-serif; '
        f'font-size:13px; border:1px solid {_BORDER}; width:auto;">'
    )

    # Header row
    parts.append("<thead><tr>")
    for col in df.columns:
        parts.append(
            f'<th style="background:{_HEADER_BG}; color:{_HEADER_FG}; '
            f'padding:8px 12px; text-align:left; border:1px solid {_BORDER}; '
            f'position:sticky; top:0; z-index:1;">{col}</th>'
        )
    parts.append("</tr></thead>")

    # Data rows
    parts.append("<tbody>")
    for idx, row in df.iterrows():
        bg = _ROW_EVEN if idx % 2 == 0 else _ROW_ODD
        parts.append(f"<tr>")
        for val in row:
            cell = f"{val:,.0f}" if isinstance(val, (int, float)) and not isinstance(val, bool) else str(val)
            parts.append(
                f'<td style="padding:6px 12px; border:1px solid {_BORDER}; '
                f'background:{bg};">{cell}</td>'
            )
        parts.append("</tr>")
    parts.append("</tbody></table></div>")

    # Record count
    n = len(df)
    parts.append(
        f'<p style="font-size:11px; color:#888; margin-top:4px;">'
        f'{n} row{"s" if n != 1 else ""} returned</p>'
    )

    return "\n".join(parts)


def show(df: pd.DataFrame, title: str | None = None) -> None:
    """Display a Pandas DataFrame as a beautifully styled HTML table.

    Parameters
    ----------
    df : pd.DataFrame
        The data to display.
    title : str, optional
        An optional heading above the table.
    """
    display(HTML(_styled_html(df, title)))


def show_cards(
    df: pd.DataFrame,
    title: str | None = None,
    img_col: str = "image_url",
    name_col: str = "emp_name",
    columns: int = 4,
) -> None:
    """Display employees as visual cards with avatar images.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain at least *img_col* and *name_col*.  Any other
        columns are shown as detail lines on the card.
    title : str, optional
        Heading displayed above the card grid.
    img_col : str
        Column that holds the image URL (default ``image_url``).
    name_col : str
        Column used as the card title (default ``emp_name``).
    columns : int
        Number of cards per row (default 4).
    """
    parts: list[str] = []

    if title:
        parts.append(
            f'<h4 style="color:{_TITLE_COLOR}; font-family:Helvetica Neue,'
            f'Helvetica,Arial,sans-serif; margin-bottom:8px;">{title}</h4>'
        )

    parts.append(
        '<div style="display:flex; flex-wrap:wrap; gap:16px;">'
    )

    detail_cols = [c for c in df.columns if c not in (img_col, name_col)]

    for _, row in df.iterrows():
        img_url = row[img_col]
        name = row[name_col]

        details_html = ""
        for col in detail_cols:
            val = row[col]
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                val = f"{val:,.0f}"
            details_html += (
                f'<div style="font-size:11px; color:#555; margin-top:2px;">'
                f'<b>{col}:</b> {val}</div>'
            )

        card = (
            f'<div style="width:{100 // columns - 2}%; min-width:160px; '
            f'border:1px solid {_BORDER}; border-radius:10px; padding:14px; '
            f'background:#FFFFFF; text-align:center; '
            f'box-shadow:0 2px 6px rgba(0,0,0,0.08);">'
            f'<img src="{img_url}" '
            f'style="width:72px; height:72px; border-radius:50%; '
            f'border:3px solid {_HEADER_BG}; margin-bottom:8px;" />'
            f'<div style="font-weight:bold; font-size:13px; color:{_HEADER_BG};">'
            f'{name}</div>'
            f'{details_html}'
            f'</div>'
        )
        parts.append(card)

    parts.append("</div>")
    parts.append(
        f'<p style="font-size:11px; color:#888; margin-top:6px;">'
        f'{len(df)} employee{"s" if len(df) != 1 else ""} shown</p>'
    )
    display(HTML("\n".join(parts)))


def show_table_with_images(
    df: pd.DataFrame,
    title: str | None = None,
    img_col: str = "image_url",
    img_size: int = 40,
) -> None:
    """Display a table where the *img_col* is rendered as a small avatar.

    Parameters
    ----------
    df : pd.DataFrame
        The data to display.
    title : str, optional
        Heading above the table.
    img_col : str
        Column containing image URLs (default ``image_url``).
    img_size : int
        Avatar diameter in pixels (default 40).
    """
    df = df.copy()
    df.insert(0, "#", range(1, len(df) + 1))

    parts: list[str] = []

    if title:
        parts.append(
            f'<h4 style="color:{_TITLE_COLOR}; font-family:Helvetica Neue,'
            f'Helvetica,Arial,sans-serif; margin-bottom:6px;">{title}</h4>'
        )

    parts.append(
        '<div style="overflow-x:auto; max-height:600px; overflow-y:auto;">'
        '<table style="border-collapse:collapse; font-family:Helvetica Neue,'
        f'Helvetica,Arial,sans-serif; font-size:13px; border:1px solid {_BORDER};">'
    )

    # Header
    parts.append("<thead><tr>")
    for col in df.columns:
        label = "Avatar" if col == img_col else col
        parts.append(
            f'<th style="background:{_HEADER_BG}; color:{_HEADER_FG}; '
            f'padding:8px 12px; text-align:left; border:1px solid {_BORDER}; '
            f'position:sticky; top:0; z-index:1;">{label}</th>'
        )
    parts.append("</tr></thead><tbody>")

    # Rows
    for idx, row in df.iterrows():
        bg = _ROW_EVEN if idx % 2 == 0 else _ROW_ODD
        parts.append("<tr>")
        for col in df.columns:
            val = row[col]
            if col == img_col:
                cell = (
                    f'<img src="{val}" width="{img_size}" height="{img_size}" '
                    f'style="border-radius:50%; border:2px solid {_BORDER};" />'
                )
            elif isinstance(val, (int, float)) and not isinstance(val, bool):
                cell = f"{val:,.0f}"
            else:
                cell = str(val)
            parts.append(
                f'<td style="padding:6px 12px; border:1px solid {_BORDER}; '
                f'background:{bg}; vertical-align:middle;">{cell}</td>'
            )
        parts.append("</tr>")

    parts.append("</tbody></table></div>")
    parts.append(
        f'<p style="font-size:11px; color:#888; margin-top:4px;">'
        f'{len(df)} row{"s" if len(df) != 1 else ""} returned</p>'
    )
    display(HTML("\n".join(parts)))


def show_query(con, sql: str, title: str | None = None) -> pd.DataFrame:
    """Execute *sql* on a DuckDB connection and display the result.

    Parameters
    ----------
    con : duckdb.DuckDBPyConnection
        An open DuckDB connection.
    sql : str
        The SQL query to run.
    title : str, optional
        Heading shown above the result table.

    Returns
    -------
    pd.DataFrame
        The query result (so you can chain further operations).
    """
    df = con.execute(sql).fetchdf()
    show(df, title)
    return df
