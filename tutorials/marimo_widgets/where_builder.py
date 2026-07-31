"""
where_builder.py
================
Helper functions for the SQL WHERE Clause Builder notebook.
Builds WHERE clauses from column name, operator, and raw user input.
Keeps the notebook cells clean and focused on the interactive widgets.

Usage in notebook:
    from where_builder import query_with_where, query_with_two_conditions
"""


# Text columns that need single quotes around values
DEFAULT_TEXT_COLS = {"product_name", "category"}


def build_where(col, op, raw_value, text_cols=None):
    """
    Build a complete SQL WHERE clause from user inputs.

    Parameters
    ----------
    col : str
        Column name (e.g., "price", "category").
    op : str
        SQL operator (e.g., "=", ">=", "LIKE", "IN", "BETWEEN").
    raw_value : str
        Raw text entered by the user.
    text_cols : set, optional
        Column names that hold text (need quoting).
        Defaults to {"product_name", "category"}.

    Returns
    -------
    (where_clause, error)
        On success: (str, None)  — e.g., ("WHERE price >= 50", None)
        On failure: (None, str)  — e.g., (None, "BETWEEN needs two values...")
    """
    if text_cols is None:
        text_cols = DEFAULT_TEXT_COLS

    raw = (raw_value or "").strip()
    is_text = col in text_cols

    if not raw:
        return None, "Please enter a value in the text box above."

    if op == "BETWEEN":
        parts = [p.strip() for p in raw.split(",")]
        if len(parts) != 2:
            return None, "BETWEEN needs exactly two values separated by a comma. Example: `20, 80`"
        if is_text:
            where = f"WHERE {col} BETWEEN '{parts[0]}' AND '{parts[1]}'"
        else:
            where = f"WHERE {col} BETWEEN {parts[0]} AND {parts[1]}"

    elif op == "IN":
        parts = [p.strip() for p in raw.split(",")]
        if is_text:
            in_list = ", ".join(f"'{p}'" for p in parts)
        else:
            in_list = ", ".join(parts)
        where = f"WHERE {col} IN ({in_list})"

    elif op == "LIKE":
        where = f"WHERE {col} LIKE '{raw}'"

    else:
        # Simple operators: =, !=, >, <, >=, <=
        if is_text:
            where = f"WHERE {col} {op} '{raw}'"
        else:
            where = f"WHERE {col} {op} {raw}"

    return where, None


def build_condition(col, op, raw_value, text_cols=None):
    """
    Build a single SQL condition (without the WHERE keyword).

    Parameters
    ----------
    col : str
        Column name.
    op : str
        SQL operator (simple operators only: =, !=, >, <, >=, <=, LIKE).
    raw_value : str
        Raw text entered by the user.
    text_cols : set, optional
        Column names that hold text. Defaults to {"product_name", "category"}.

    Returns
    -------
    (condition, error)
        On success: (str, None)  — e.g., ("price >= 50", None)
        On failure: (None, str)  — e.g., (None, "Please enter a value...")
    """
    if text_cols is None:
        text_cols = DEFAULT_TEXT_COLS

    raw = (raw_value or "").strip()
    is_text = col in text_cols

    if not raw:
        return None, "Please enter a value."

    if op == "LIKE":
        condition = f"{col} LIKE '{raw}'"
    elif is_text:
        condition = f"{col} {op} '{raw}'"
    else:
        condition = f"{col} {op} {raw}"

    return condition, None


def run_filtered_query(con, where_clause, table="products", order_by="product_id"):
    """
    Run a SELECT query with the given WHERE clause.

    Parameters
    ----------
    con : duckdb.DuckDBPyConnection
        Active DuckDB connection.
    where_clause : str
        Complete WHERE clause (e.g., "WHERE price >= 50").
    table : str
        Table name. Default: "products".
    order_by : str
        Column to sort by. Default: "product_id".

    Returns
    -------
    (df, sql, error)
        On success: (DataFrame, sql_string, None)
        On failure: (None, sql_string, error_message)
    """
    sql = f"SELECT *\nFROM   {table}\n{where_clause}\nORDER BY {order_by};"
    try:
        df = con.execute(sql).df()
        return df, sql, None
    except Exception as e:
        return None, sql, str(e)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HIGH-LEVEL FUNCTIONS (used directly by notebook cells)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def query_with_where(con, col, op, raw_value, total_rows=12):
    """
    Build a WHERE clause, run the query, return (markdown, dataframe).

    The notebook cell only needs to wrap the result in mo.md() / mo.ui.table().

    Returns
    -------
    (markdown_text, df_or_none)
        markdown_text : str   — ready to pass to mo.md()
        df_or_none    : DataFrame or None
    """
    where, err = build_where(col, op, raw_value)
    if err:
        return f"**{err}**", None

    df, sql, query_err = run_filtered_query(con, where)
    if query_err:
        md = (
            f"**Generated SQL:**\n```sql\n{sql}\n```\n"
            f"**Error:** `{query_err}`\n\n"
            f"Check your value — text columns need words, numeric columns need numbers."
        )
        return md, None

    md = (
        f"**Generated SQL:**\n```sql\n{sql}\n```\n"
        f"**Result:** {len(df)} of {total_rows} product(s) matched the filter"
    )
    return md, df


def query_with_two_conditions(con, col_a, op_a, val_a, col_b, op_b, val_b, logic="AND", total_rows=12):
    """
    Build a two-condition WHERE clause (AND / OR), run it, return (markdown, dataframe).

    Returns
    -------
    (markdown_text, df_or_none)
    """
    cond_a, err_a = build_condition(col_a, op_a, val_a)
    cond_b, err_b = build_condition(col_b, op_b, val_b)

    if err_a or err_b:
        return "**Please enter values for both conditions.**", None

    where = f"WHERE {cond_a}\n  {logic} {cond_b}"
    df, sql, query_err = run_filtered_query(con, where)

    logic_meaning = "both conditions must be true" if logic == "AND" else "either condition can be true"

    if query_err:
        md = (
            f"**Generated SQL:**\n```sql\n{sql}\n```\n"
            f"**Error:** `{query_err}`\n\n"
            f"Check your values — text columns need words, numeric columns need numbers."
        )
        return md, None

    md = (
        f"**Generated SQL:**\n```sql\n{sql}\n```\n"
        f"**Result:** {len(df)} product(s) matched "
        f"({logic} means {logic_meaning})"
    )
    return md, df
