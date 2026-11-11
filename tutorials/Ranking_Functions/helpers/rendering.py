import pandas as pd
import marimo as _mo  # marimo's own display tools (students do not install IPython)
def display(*objs):
    for _obj in objs:
        _mo.output.append(_obj)
HTML = _mo.Html

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

    # Plain pandas HTML + the same CSS (DataFrame.style would need jinja2,
    # which students do not install)
    css = "".join(
        f".rank-table {s['selector']}{{" + ";".join(f"{k}:{v}" for k, v in s["props"]) + "}"
        for s in styles
    )
    html = f"<style>{css}</style>" + df_display.to_html(
        index=False, classes="rank-table", border=0)

    header = ""
    if title:
        header += f"<h3 style='color:#0b3c5d'>{title}</h3>"

    # ✅ Show both displayed rows and total rows
    footer = f"<p><b>Showing:</b> {len(df_display)} rows"
    if max_rows is not None:
        footer += f" (of {len(df)})"
    footer += "</p>"

    display(HTML(header + html + footer))
