from __future__ import annotations

import pandas as pd
from IPython.display import display, Markdown, HTML
import matplotlib.pyplot as plt


def show_note(text: str) -> None:
    display(Markdown(text))


def pretty_sql(sql: str) -> None:
    display(Markdown("### SQL Solution"))
    display(Markdown(f"```sql\n{sql.strip()}\n```"))


def show_df(df: pd.DataFrame, title: str | None = None) -> pd.DataFrame:
    if title:
        display(Markdown(f"### {title}"))

    out = df.copy()
    out.insert(0, "row_num", range(1, len(out) + 1))

    display(
        out.style
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#f3f4f6"),
                ("font-weight", "bold"),
                ("padding", "6px"),
                ("border", "1px solid #d1d5db"),
                ("text-align", "left")
            ]},
            {"selector": "td", "props": [
                ("padding", "6px"),
                ("border", "1px solid #e5e7eb"),
                ("text-align", "left"),
                ("vertical-align", "middle"),
                ("max-width", "80ch"),
                ("white-space", "nowrap"),
                ("overflow", "hidden"),
                ("text-overflow", "ellipsis")
            ]}
        ])
        .hide(axis="index")
    )
    return out


def show_df_with_images(df: pd.DataFrame,
                        image_column: str = "image_url",
                        title: str | None = None,
                        image_width: int = 70) -> pd.DataFrame:
    if title:
        display(Markdown(f"### {title}"))

    out = df.copy()
    out.insert(0, "row_num", range(1, len(out) + 1))

    if image_column in out.columns:
        out[image_column] = out[image_column].apply(
            lambda x: f'<img src="{x}" width="{image_width}" style="border-radius:12px;">'
        )

    html = out.to_html(escape=False, index=False)
    display(HTML(html))
    return out


def run_query(con, sql: str, title: str | None = None) -> pd.DataFrame:
    pretty_sql(sql)
    df = con.execute(sql).df()
    show_df(df, title or "Result")
    return df


def run_query_with_images(con,
                          sql: str,
                          image_column: str = "image_url",
                          title: str | None = None) -> pd.DataFrame:
    pretty_sql(sql)
    df = con.execute(sql).df()

    show_df(df, f"{title or 'Result'} — Raw Database Values")
    show_df_with_images(
        df,
        image_column=image_column,
        title=f"{title or 'Result'} — Rendered Avatar Images"
    )
    return df


def run_statement(con, sql: str, message: str | None = None) -> None:
    pretty_sql(sql)
    con.execute(sql)
    if message:
        display(Markdown(f"✅ {message}"))


def plot_bar(df: pd.DataFrame,
             x: str,
             y: str,
             title: str,
             ylabel: str | None = None) -> None:
    ax = df.plot(kind="bar", x=x, y=y, figsize=(8, 4), legend=False)
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel(ylabel or y)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def plot_pie(df: pd.DataFrame,
             labels_col: str,
             values_col: str,
             title: str) -> None:
    ax = df.set_index(labels_col)[values_col].plot(
        kind="pie",
        autopct="%1.1f%%",
        figsize=(6, 6)
    )
    ax.set_ylabel("")
    ax.set_title(title)
    plt.tight_layout()
    plt.show()
