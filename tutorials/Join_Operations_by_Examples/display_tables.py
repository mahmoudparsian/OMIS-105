"""
display_tables.py
-----------------
Beautiful HTML table rendering utilities for the SQL JOINs tutorial.
Import and use these functions in the Jupyter notebook.
"""

from IPython.display import display, HTML
import pandas as pd


# ── Colour palette ────────────────────────────────────────────────────────────
PALETTE = {
    "primary":      "#1a1a2e",   # deep navy
    "secondary":    "#16213e",
    "accent":       "#0f3460",
    "highlight":    "#e94560",   # vivid red-pink
    "highlight2":   "#f5a623",   # amber
    "text_light":   "#eaeaea",
    "text_muted":   "#a0a4b8",
    "row_even":     "#f8f9ff",
    "row_odd":      "#ffffff",
    "header_bg":    "#1a1a2e",
    "border":       "#dde1f0",
    "null_bg":      "#fff3cd",
    "null_text":    "#856404",
    "match_bg":     "#d4edda",
    "match_text":   "#155724",
}


_BASE_STYLE = """
<style>
  .sql-table-wrapper {{
    font-family: 'Segoe UI', system-ui, sans-serif;
    margin: 16px 0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(26,26,46,0.12);
    border: 1px solid {border};
  }}
  .sql-table-title {{
    background: linear-gradient(135deg, {primary} 0%, {accent} 100%);
    color: {text_light};
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .sql-table-title .badge {{
    background: {highlight};
    color: white;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
  }}
  .sql-table-wrapper table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  .sql-table-wrapper thead tr {{
    background: {secondary};
    color: {text_light};
  }}
  .sql-table-wrapper thead th {{
    padding: 10px 16px;
    text-align: left;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-right: 1px solid rgba(255,255,255,0.08);
    white-space: nowrap;
  }}
  .sql-table-wrapper thead th:last-child {{ border-right: none; }}
  .sql-table-wrapper tbody tr:nth-child(even) {{ background: {row_even}; }}
  .sql-table-wrapper tbody tr:nth-child(odd)  {{ background: {row_odd}; }}
  .sql-table-wrapper tbody tr:hover {{ background: #e8eeff; transition: background 0.15s; }}
  .sql-table-wrapper tbody td {{
    padding: 9px 16px;
    border-right: 1px solid {border};
    border-bottom: 1px solid {border};
    color: #2d2d3a;
    vertical-align: middle;
  }}
  .sql-table-wrapper tbody td:last-child {{ border-right: none; }}
  .sql-table-wrapper .null-cell {{
    background: {null_bg};
    color: {null_text};
    font-style: italic;
    font-size: 11px;
    font-weight: 600;
  }}
  .sql-table-wrapper .num-cell {{
    font-family: 'Consolas', 'Courier New', monospace;
    text-align: right;
    color: {accent};
    font-weight: 600;
  }}
  .sql-table-wrapper .id-cell {{
    font-family: 'Consolas', 'Courier New', monospace;
    color: {highlight};
    font-weight: 700;
    font-size: 12px;
  }}
  .sql-table-footer {{
    background: {row_even};
    border-top: 2px solid {border};
    padding: 8px 16px;
    font-size: 11px;
    color: {text_muted};
    text-align: right;
  }}
</style>
""".format(**PALETTE)


def _cell_html(value, col_name: str) -> str:
    """Render a single <td> with smart styling."""
    col_lower = col_name.lower()
    if value is None or (isinstance(value, float) and pd.isna(value)) or str(value) in ("None", "nan", "NaN", ""):
        return '<td class="null-cell">NULL</td>'
    if col_lower in ("emp_id","dept_id","country_code") or col_lower.endswith("_id") or col_lower.endswith("_code"):
        return f'<td class="id-cell">{value}</td>'
    if col_lower in ("salary","population","count","total","avg","cnt","avg_salary",
                     "total_salary","num_employees","headcount","employee_count"):
        try:
            n = float(str(value).replace(",",""))
            formatted = f"{n:,.0f}" if n == int(n) else f"{n:,.2f}"
            return f'<td class="num-cell">{formatted}</td>'
        except Exception:
            pass
    return f"<td>{value}</td>"


def render_table(df: pd.DataFrame, title: str = "Result Set",
                 icon: str = "📋", max_rows: int = 50) -> None:
    """
    Render a pandas DataFrame as a styled HTML table.

    Parameters
    ----------
    df      : DataFrame to display
    title   : Caption shown in the header bar
    icon    : Emoji icon for the header
    max_rows: Truncate display after this many rows
    """
    if df is None or len(df) == 0:
        display(HTML(f"<p><em>No rows returned.</em></p>"))
        return

    total = len(df)
    shown = df.head(max_rows)

    # Header
    badge_text = f"{total:,} row{'s' if total != 1 else ''}"
    cols = list(shown.columns)

    thead = "".join(f"<th>{c}</th>" for c in cols)

    tbody_rows = []
    for _, row in shown.iterrows():
        cells = "".join(_cell_html(row[c], c) for c in cols)
        tbody_rows.append(f"<tr>{cells}</tr>")
    tbody = "\n".join(tbody_rows)

    footer = f"Showing {len(shown):,} of {total:,} rows • {len(cols)} column{'s' if len(cols)!=1 else ''}"
    if total > max_rows:
        footer += f" • {total - max_rows:,} rows hidden"

    html = f"""
    {_BASE_STYLE}
    <div class="sql-table-wrapper">
      <div class="sql-table-title">
        <span>{icon}</span>
        <span>{title}</span>
        <span class="badge">{badge_text}</span>
      </div>
      <table>
        <thead><tr>{thead}</tr></thead>
        <tbody>{tbody}</tbody>
      </table>
      <div class="sql-table-footer">{footer}</div>
    </div>
    """
    display(HTML(html))


def render_join_comparison(left_df: pd.DataFrame, right_df: pd.DataFrame,
                            left_title: str = "Left Table",
                            right_title: str = "Right Table") -> None:
    """Show two DataFrames side by side for join illustration."""
    style = _BASE_STYLE

    def _mini_table(df, title, icon="📄"):
        cols = list(df.columns)
        thead = "".join(f"<th>{c}</th>" for c in cols)
        rows = []
        for _, row in df.iterrows():
            cells = "".join(_cell_html(row[c], c) for c in cols)
            rows.append(f"<tr>{cells}</tr>")
        tbody = "\n".join(rows)
        return f"""
        <div class="sql-table-wrapper" style="flex:1;min-width:0;">
          <div class="sql-table-title">{icon} {title}
            <span class="badge">{len(df)} rows</span>
          </div>
          <table>
            <thead><tr>{thead}</tr></thead>
            <tbody>{tbody}</tbody>
          </table>
        </div>"""

    html = f"""
    {style}
    <div style="display:flex;gap:20px;align-items:flex-start;">
      {_mini_table(left_df,  left_title,  "⬅️")}
      {_mini_table(right_df, right_title, "➡️")}
    </div>
    """
    display(HTML(html))


def render_summary_card(stats: dict, title: str = "Summary Statistics",
                        icon: str = "📊") -> None:
    """
    Render a dictionary of key→value pairs as a compact summary card.
    """
    cards = ""
    for k, v in stats.items():
        if isinstance(v, float):
            v_str = f"{v:,.2f}"
        elif isinstance(v, int):
            v_str = f"{v:,}"
        else:
            v_str = str(v)
        cards += f"""
        <div style="background:#f8f9ff;border:1px solid #dde1f0;border-radius:10px;
                    padding:14px 20px;min-width:130px;text-align:center;flex:1;">
          <div style="font-size:11px;color:#a0a4b8;text-transform:uppercase;
                      letter-spacing:0.8px;font-weight:600;margin-bottom:4px;">{k}</div>
          <div style="font-size:22px;font-weight:700;color:#1a1a2e;">{v_str}</div>
        </div>"""

    html = f"""
    {_BASE_STYLE}
    <div class="sql-table-wrapper">
      <div class="sql-table-title">{icon} {title}</div>
      <div style="display:flex;flex-wrap:wrap;gap:12px;padding:16px;">{cards}</div>
    </div>
    """
    display(HTML(html))


def render_sql(sql: str, label: str = "SQL Query") -> None:
    """Pretty-print a SQL query block."""
    import re
    keywords = r'\b(SELECT|FROM|JOIN|LEFT|RIGHT|INNER|OUTER|FULL|ON|WHERE|GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|AS|AND|OR|NOT|NULL|IS|IN|BETWEEN|LIKE|COUNT|SUM|AVG|MIN|MAX|DISTINCT|USING|UNION|WITH|CASE|WHEN|THEN|ELSE|END|BY|DESC|ASC|ROUND|COALESCE|CAST)\b'

    def highlight(m):
        return f'<span style="color:#e94560;font-weight:700;">{m.group(0)}</span>'

    escaped = sql.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    highlighted = re.sub(keywords, highlight, escaped, flags=re.IGNORECASE)

    html = f"""
    <div style="margin:12px 0;border-radius:10px;overflow:hidden;
                box-shadow:0 2px 12px rgba(26,26,46,0.10);">
      <div style="background:#0f3460;color:#a0c4ff;padding:8px 16px;
                  font-size:11px;font-weight:700;letter-spacing:1px;">
        🔷 {label.upper()}
      </div>
      <pre style="background:#1a1a2e;color:#eaeaea;margin:0;padding:16px 20px;
                  font-family:'Consolas','Courier New',monospace;font-size:13px;
                  line-height:1.7;overflow-x:auto;">{highlighted}</pre>
    </div>
    """
    display(HTML(html))


def render_section_header(number: int, title: str, subtitle: str = "",
                           join_type: str = "") -> None:
    """Render a styled section header for each notebook cell."""
    join_colors = {
        "INNER JOIN": ("#0f3460","#4fc3f7"),
        "LEFT JOIN":  ("#1b5e20","#81c784"),
        "RIGHT JOIN": ("#4a148c","#ce93d8"),
        "CROSS JOIN": ("#e65100","#ffb74d"),
        "FULL JOIN":  ("#880e4f","#f48fb1"),
        "":           ("#37474f","#90a4ae"),
    }
    bg, accent = join_colors.get(join_type, join_colors[""])
    join_badge = f'<span style="background:{accent};color:{bg};border-radius:20px;padding:3px 12px;font-size:12px;font-weight:700;margin-left:12px;">{join_type}</span>' if join_type else ""

    html = f"""
    <div style="border-left:5px solid {accent};background:linear-gradient(135deg,{bg}ee,{bg}88);
                padding:16px 20px;border-radius:0 12px 12px 0;margin:24px 0 8px 0;
                box-shadow:0 2px 12px rgba(0,0,0,0.15);">
      <div style="display:flex;align-items:center;">
        <span style="background:{accent};color:{bg};border-radius:50%;width:32px;height:32px;
                     display:inline-flex;align-items:center;justify-content:center;
                     font-weight:800;font-size:15px;margin-right:14px;flex-shrink:0;">
          {number}
        </span>
        <div>
          <div style="color:#fff;font-size:17px;font-weight:700;letter-spacing:0.3px;">
            {title}{join_badge}
          </div>
          {f'<div style="color:rgba(255,255,255,0.7);font-size:12px;margin-top:3px;">{subtitle}</div>' if subtitle else ''}
        </div>
      </div>
    </div>
    """
    display(HTML(html))
