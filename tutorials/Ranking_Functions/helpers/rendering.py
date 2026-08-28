import pandas as pd
from IPython.display import display, HTML

def show(df, title=None, add_row_numbers=True, max_rows=None):
    """
    Render a DataFrame with:
    - Dark navy header
    - Alternating row colors
    - Hover highlight
    - Row count
    - Optional row numbering
    - Optional row limiting (NEW)
    """

    if df is None or len(df) == 0:
        display(HTML("<b>No rows returned</b>"))
        return

    df_display = df.copy()

    # ✅ Apply max_rows (NEW)
    if max_rows is not None:
        df_display = df_display.head(max_rows)

    # ✅ Add row numbers
    if add_row_numbers:
        df_display.insert(0, "row_num", range(1, len(df_display) + 1))

    styles = [
        dict(selector="th", props=[
            ("background-color", "#0b3c5d"),
            ("color", "white"),
            ("font-weight", "bold"),
            ("text-align", "center"),
            ("padding", "8px")
        ]),
        dict(selector="td", props=[
            ("padding", "6px"),
            ("text-align", "center")
        ]),
        dict(selector="tr:nth-child(even)", props=[
            ("background-color", "#f2f2f2")
        ]),
        dict(selector="tr:hover", props=[
            ("background-color", "#ffeaa7")
        ])
    ]

    styled = (
        df_display.style
        .set_table_styles(styles)
        .hide(axis="index")
    )

    html = styled.to_html()

    header = ""
    if title:
        header += f"<h3 style='color:#0b3c5d'>{title}</h3>"

    # ✅ Show both displayed rows and total rows
    footer = f"<p><b>Showing:</b> {len(df_display)} rows"
    if max_rows is not None:
        footer += f" (of {len(df)})"
    footer += "</p>"

    display(HTML(header + html + footer))
