"""
notebook_utils.py
=================
Helper module for the CRUD Employee Notebook.
Provides clean display, tabulation, and plotting
functions so notebook cells remain uncluttered.

Usage:
    from notebook_utils import show_table, show_sql, plot_bar, plot_pie, plot_hist, plot_grouped_bar
"""

import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np
from IPython.display import display, HTML
import warnings

warnings.filterwarnings("ignore")

# ── Colour palette ────────────────────────────────────────────────────────────
PALETTE = {
    "primary":   "#2563EB",   # blue
    "secondary": "#7C3AED",   # violet
    "accent":    "#0EA5E9",   # sky
    "success":   "#10B981",   # emerald
    "warning":   "#F59E0B",   # amber
    "danger":    "#EF4444",   # red
    "neutral":   "#64748B",   # slate
    "bg":        "#F8FAFC",
    "header_bg": "#1E3A5F",
    "header_fg": "#FFFFFF",
}

BAR_COLORS = [
    "#2563EB", "#7C3AED", "#0EA5E9", "#10B981",
    "#F59E0B", "#EF4444", "#EC4899", "#14B8A6", "#F97316",
]

# ── Table display ─────────────────────────────────────────────────────────────

def show_table(df: pd.DataFrame, title: str = "", max_rows: int = 50) -> None:
    """
    Render a pandas DataFrame as a beautifully styled HTML table
    with row numbers. Truncates to max_rows if needed.
    """
    if len(df) > max_rows:
        display_df = df.head(max_rows).copy()
        truncated = True
    else:
        display_df = df.copy()
        truncated = False

    # Build HTML rows
    rows_html = ""
    for i, (_, row) in enumerate(display_df.iterrows(), start=1):
        bg = "#FFFFFF" if i % 2 == 1 else "#F0F7FF"
        cells = f'<td style="padding:7px 12px;color:#374151;text-align:center;font-weight:600;color:{PALETTE["primary"]}">{i}</td>'
        for val in row:
            cells += f'<td style="padding:7px 14px;color:#1F2937">{val}</td>'
        rows_html += f'<tr style="background:{bg}">{cells}</tr>'

    # Build column headers
    header_cells = '<th style="padding:9px 12px;background:#1E3A5F;color:#FFFFFF;text-align:center">#</th>'
    for col in display_df.columns:
        header_cells += (
            f'<th style="padding:9px 14px;background:#1E3A5F;color:#FFFFFF;'
            f'text-align:left;white-space:nowrap">{col}</th>'
        )

    title_html = (
        f'<div style="font-size:15px;font-weight:700;color:{PALETTE["header_bg"]};'
        f'margin-bottom:6px;letter-spacing:.3px">{title}</div>'
        if title else ""
    )

    note = (
        f'<div style="font-size:12px;color:{PALETTE["neutral"]};margin-top:4px">'
        f'Showing first {max_rows} of {len(df)} rows.</div>'
        if truncated else
        f'<div style="font-size:12px;color:{PALETTE["neutral"]};margin-top:4px">'
        f'{len(df)} row(s) returned.</div>'
    )

    html = f"""
    {title_html}
    <div style="overflow-x:auto;border-radius:8px;
                box-shadow:0 2px 8px rgba(0,0,0,.10);margin-bottom:4px">
      <table style="border-collapse:collapse;width:100%;font-family:'Segoe UI',sans-serif;font-size:14px">
        <thead><tr>{header_cells}</tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    {note}
    """
    display(HTML(html))


# ── SQL pretty-printer ────────────────────────────────────────────────────────

def show_sql(sql: str, label: str = "SQL Statement") -> None:
    """
    Pretty-print a SQL string in a styled code block.
    Uses regex word-boundary matching so CSS inside the wrapper HTML
    is never touched — only whole SQL tokens in the raw SQL text are
    wrapped in <span> tags.
    """
    import re, html as html_mod

    # 1. Dedent & strip
    clean = textwrap.dedent(sql).strip()

    # 2. HTML-escape the raw SQL first so characters like < > & are safe
    escaped = html_mod.escape(clean)

    # 3. Keywords to highlight (multi-word first so they match before parts)
    keywords = [
        "PRIMARY KEY", "GROUP BY", "ORDER BY", "PARTITION BY",
        "READ_CSV_AUTO", "ROW_NUMBER", "NOT NULL",
        "SELECT", "FROM", "WHERE", "HAVING", "LIMIT",
        "INSERT", "INTO", "VALUES", "UPDATE", "SET",
        "DELETE", "CREATE", "TABLE", "DROP", "EXISTS",
        "NOT", "AND", "OR", "AS", "ON", "JOIN",
        "LEFT", "RIGHT", "INNER", "OUTER", "WITH",
        "OVER", "COUNT", "SUM", "AVG", "MIN", "MAX",
        "DISTINCT", "IN", "BETWEEN", "LIKE", "NULL", "IS",
        "CASE", "WHEN", "THEN", "ELSE", "END",
        "ASC", "DESC", "BY", "IF", "RANK",
        "INTEGER", "VARCHAR", "DATE", "COPY", "HEADER",
        "ROWS", "UNBOUNDED", "PRECEDING", "CURRENT", "FOLLOWING",
        "CROSS", "NTILE", "PERCENTILE_CONT", "WITHIN", "STRFTIME",
        "MONTH", "ROUND", "CONFLICT", "NOTHING",
    ]

    SPAN = '<span style="color:#93C5FD;font-weight:700">'
    END  = '</span>'

    def replacer(m):
        return SPAN + m.group(0) + END

    highlighted = escaped
    for kw in keywords:
        # Match the keyword case-insensitively at word boundaries
        # \b works for single-word tokens; for multi-word we use \s+ between words
        pattern = r'\b' + r'\s+'.join(re.escape(part) for part in kw.split()) + r'\b'
        highlighted = re.sub(pattern, replacer, highlighted, flags=re.IGNORECASE)

    # 4. Convert newlines → <br> and leading spaces → &nbsp;
    lines = highlighted.split("\n")
    html_lines = []
    for line in lines:
        # Count leading spaces
        stripped = line.lstrip(" ")
        n_spaces = len(line) - len(stripped)
        html_lines.append("&nbsp;" * n_spaces + stripped)
    highlighted = "<br>".join(html_lines)

    html = f"""
    <div style="margin:8px 0 12px 0">
      <div style="font-size:12px;font-weight:700;letter-spacing:1px;
                  color:{PALETTE['secondary']};margin-bottom:4px;
                  text-transform:uppercase">{label}</div>
      <div style="background:#0F172A;border-radius:8px;padding:16px 20px;
                  font-family:'Courier New',monospace;font-size:13.5px;
                  line-height:1.75;color:#E2E8F0;
                  box-shadow:0 2px 12px rgba(0,0,0,.25)">
        {highlighted}
      </div>
    </div>
    """
    display(HTML(html))


# ── Section header ─────────────────────────────────────────────────────────────

def show_header(title: str, subtitle: str = "", color: str = None) -> None:
    """Display a styled section header."""
    c = color or PALETTE["header_bg"]
    sub = (f'<div style="font-size:14px;color:{PALETTE["neutral"]};margin-top:4px">'
           f'{subtitle}</div>') if subtitle else ""
    display(HTML(f"""
    <div style="background:{c};color:#fff;padding:14px 20px;border-radius:8px;
                margin:18px 0 10px 0;box-shadow:0 3px 8px rgba(0,0,0,.2)">
      <div style="font-size:19px;font-weight:700;letter-spacing:.5px">{title}</div>
      {sub}
    </div>
    """))


def show_note(text: str, kind: str = "info") -> None:
    """Display a colour-coded note box (info / success / warning / danger).
    Uses pure CSS badges — no emoji — so it renders reliably in all Jupyter
    environments regardless of font or encoding support.
    """
    styles = {
        #           bg         border     label-bg   label-fg  word
        "info":    ("#EFF6FF", "#2563EB", "#2563EB", "#FFFFFF", "INFO"),
        "success": ("#F0FDF4", "#16A34A", "#16A34A", "#FFFFFF", "OK"),
        "warning": ("#FFFBEB", "#D97706", "#D97706", "#FFFFFF", "NOTE"),
        "danger":  ("#FEF2F2", "#DC2626", "#DC2626", "#FFFFFF", "ALERT"),
    }
    bg, border, label_bg, label_fg, word = styles.get(kind, styles["info"])
    display(HTML(
        '<div style="display:flex;align-items:center;gap:10px;'        f'background:{bg};border-left:4px solid {border};'        'padding:9px 14px;border-radius:0 6px 6px 0;'        'margin:8px 0;font-family:Segoe UI,sans-serif;font-size:14px;">'        f'<span style="background:{label_bg};color:{label_fg};'        'font-size:11px;font-weight:700;letter-spacing:.8px;'        f'padding:2px 7px;border-radius:4px;white-space:nowrap">{word}</span>'        f'<span style="color:#1F2937">{text}</span></div>'
    ))


# ── Plot helpers ───────────────────────────────────────────────────────────────

def _base_style(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=14, fontweight="bold", color="#1E3A5F", pad=12)
    ax.set_xlabel(xlabel, fontsize=11, color="#374151")
    ax.set_ylabel(ylabel, fontsize=11, color="#374151")
    ax.tick_params(colors="#4B5563")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#F8FAFC")
    ax.figure.patch.set_facecolor("white")


def plot_bar(df: pd.DataFrame, x_col: str, y_col: str,
             title: str = "", xlabel: str = "", ylabel: str = "",
             color: str = None, figsize=(9, 5)) -> None:
    """Vertical bar chart from a two-column DataFrame."""
    fig, ax = plt.subplots(figsize=figsize)
    colors = [color or BAR_COLORS[i % len(BAR_COLORS)] for i in range(len(df))]
    bars = ax.bar(df[x_col].astype(str), df[y_col], color=colors,
                  edgecolor="white", linewidth=1.2, zorder=3)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + max(df[y_col]) * 0.01,
                f"{h:,.0f}", ha="center", va="bottom", fontsize=10,
                fontweight="600", color="#1E3A5F")
    _base_style(ax, title, xlabel or x_col, ylabel or y_col)
    plt.tight_layout()
    plt.show()


def plot_horizontal_bar(df: pd.DataFrame, x_col: str, y_col: str,
                        title: str = "", xlabel: str = "", ylabel: str = "",
                        figsize=(9, 5)) -> None:
    """Horizontal bar chart."""
    fig, ax = plt.subplots(figsize=figsize)
    colors = [BAR_COLORS[i % len(BAR_COLORS)] for i in range(len(df))]
    bars = ax.barh(df[x_col].astype(str), df[y_col], color=colors,
                   edgecolor="white", linewidth=1.1, zorder=3)
    ax.xaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + max(df[y_col]) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{w:,.0f}", va="center", fontsize=10,
                fontweight="600", color="#1E3A5F")
    ax.invert_yaxis()
    _base_style(ax, title, xlabel or y_col, ylabel or x_col)
    plt.tight_layout()
    plt.show()


def plot_pie(df: pd.DataFrame, label_col: str, value_col: str,
             title: str = "", figsize=(7, 7)) -> None:
    """Pie / donut chart."""
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        df[value_col],
        labels=df[label_col],
        autopct="%1.1f%%",
        colors=BAR_COLORS[:len(df)],
        startangle=140,
        pctdistance=0.80,
        wedgeprops=dict(width=0.6, edgecolor="white", linewidth=2),
    )
    for t in texts:
        t.set_fontsize(11)
        t.set_color("#1F2937")
    for at in autotexts:
        at.set_fontsize(10)
        at.set_color("white")
        at.set_fontweight("bold")
    ax.set_title(title, fontsize=14, fontweight="bold", color="#1E3A5F", pad=16)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    plt.show()


def plot_hist(series: pd.Series, title: str = "", xlabel: str = "",
              bins: int = 8, color: str = None, figsize=(9, 5)) -> None:
    """Histogram of a numeric series."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(series.dropna(), bins=bins, color=color or PALETTE["primary"],
            edgecolor="white", linewidth=1.2, zorder=3)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    _base_style(ax, title, xlabel or series.name or "", "Count")
    plt.tight_layout()
    plt.show()


def plot_grouped_bar(df: pd.DataFrame, group_col: str, value_col: str,
                     hue_col: str, title: str = "",
                     xlabel: str = "", ylabel: str = "",
                     figsize=(10, 5)) -> None:
    """
    Grouped bar chart.
    df should already be aggregated: one row per (group_col, hue_col) pair.
    """
    groups  = df[group_col].unique()
    hues    = df[hue_col].unique()
    x       = np.arange(len(groups))
    width   = 0.8 / len(hues)

    fig, ax = plt.subplots(figsize=figsize)
    for i, hue in enumerate(hues):
        sub    = df[df[hue_col] == hue]
        vals   = [sub.loc[sub[group_col] == g, value_col].values[0]
                  if g in sub[group_col].values else 0 for g in groups]
        offset = (i - len(hues) / 2 + 0.5) * width
        bars   = ax.bar(x + offset, vals, width * 0.9,
                        label=str(hue), color=BAR_COLORS[i % len(BAR_COLORS)],
                        edgecolor="white", zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(groups, fontsize=10)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax.legend(title=hue_col, fontsize=10)
    _base_style(ax, title, xlabel or group_col, ylabel or value_col)
    plt.tight_layout()
    plt.show()


def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str,
                 label_col: str = None, title: str = "",
                 figsize=(9, 5)) -> None:
    """Scatter plot, optionally with labelled points."""
    fig, ax = plt.subplots(figsize=figsize)
    sc = ax.scatter(df[x_col], df[y_col],
                    c=range(len(df)), cmap="Blues_r",
                    s=90, edgecolors="#1E3A5F", linewidths=0.7, zorder=3)
    if label_col:
        for _, row in df.iterrows():
            ax.annotate(str(row[label_col]),
                        (row[x_col], row[y_col]),
                        textcoords="offset points", xytext=(6, 4),
                        fontsize=9, color="#374151")
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, zorder=0)
    ax.xaxis.grid(True, linestyle="--", alpha=0.4, zorder=0)
    _base_style(ax, title, x_col, y_col)
    plt.tight_layout()
    plt.show()


def plot_line(df: pd.DataFrame, x_col: str, y_col: str,
              title: str = "", xlabel: str = "", ylabel: str = "",
              color: str = None, figsize=(9, 5)) -> None:
    """Line chart."""
    fig, ax = plt.subplots(figsize=figsize)
    c = color or PALETTE["primary"]
    ax.plot(df[x_col].astype(str), df[y_col], marker="o",
            color=c, linewidth=2.2, markersize=7,
            markerfacecolor="white", markeredgecolor=c, markeredgewidth=2, zorder=3)
    ax.fill_between(range(len(df)), df[y_col], alpha=0.08, color=c)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    _base_style(ax, title, xlabel or x_col, ylabel or y_col)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
