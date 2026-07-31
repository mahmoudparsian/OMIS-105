"""
In-N-Out POS + Analytics  ·  Streamlit + DuckDB
OMIS-105 Introduction to DBMS  ·  Santa Clara University

A point-of-sale that writes real transactions into a normalized DuckDB
database, plus a live analytics dashboard and a SQL playground.

Run:
    pip install -r requirements.txt
    python build_db.py        # one-time: creates innout.duckdb with demo data
    streamlit run app.py
"""

import os
from datetime import datetime

import altair as alt
import duckdb
import pandas as pd
import streamlit as st

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "innout.duckdb")


def _load_dotenv():
    """Load KEY=VALUE pairs from a local .env into os.environ (e.g. the
    ANTHROPIC_API_KEY). Uses python-dotenv if available, else a tiny parser."""
    env_path = os.path.join(HERE, ".env")
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        return
    except Exception:
        pass
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip()
            if v[:1] in ('"', "'"):            # quoted value: take inside quotes
                v = v[1:].split(v[0], 1)[0]
            else:                              # strip an inline  # comment
                v = v.split(" #", 1)[0].split("\t#", 1)[0].strip()
            os.environ.setdefault(k.strip(), v)


_load_dotenv()

RED = "#E31837"
YELLOW = "#FFC72C"

st.set_page_config(page_title="In-N-Out POS · DuckDB",
                   page_icon="🍔", layout="wide")

# ---------------------------------------------------------------------------
# Styling — In-N-Out red & yellow
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
  .stApp {{ background: #fffdf7; color: #1a1a1a; }}
  /* Force dark, readable text even if the user's Streamlit is in dark mode */
  .stApp, .stApp p, .stApp span, .stApp li, .stApp label,
  .stApp h1, .stApp h2, .stApp h3, .stApp h4,
  [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] {{
      color: #1a1a1a;
  }}
  .stApp h1, .stApp h2, .stApp h3 {{ color: {RED}; }}
  [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {{
      color: #6b6b6b !important;
  }}
  div.stButton > button {{
      background: {RED}; color: white !important; border: none;
      border-radius: 6px; font-weight: 700; padding: 0.45rem 1rem;
  }}
  div.stButton > button:hover {{ background: #b5122a; color: {YELLOW} !important; }}
  [data-testid="stMetricValue"] {{ color: {RED}; }}
  .receipt {{ font-family: 'Courier New', monospace; background: #fff;
              color: #1a1a1a; border: 2px dashed {RED};
              border-radius: 8px; padding: 18px; }}
  /* Coding font + comfortable size for the SQL editor */
  .stTextArea textarea {{
      font-family: 'JetBrains Mono', 'Fira Code', 'SFMono-Regular', Menlo,
                   Consolas, 'Liberation Mono', monospace;
      font-size: 0.95rem; line-height: 1.5; color: #1a1a1a;
      background: #fbf7ec; tab-size: 2;
  }}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
@st.cache_resource
def get_con():
    """One read-write DuckDB connection shared across reruns."""
    return duckdb.connect(DB_PATH)


def q(sql: str, params=None) -> pd.DataFrame:
    return get_con().execute(sql, params or []).df()


def show_sql(sql: str, label: str = "🔍 Show SQL"):
    """Reveal the SQL behind a result — on request, per the class spec."""
    with st.expander(label):
        st.code(sql.strip(), language="sql")


ER_DOT_FILE = os.path.join(HERE, "er_diagram.dot")


@st.cache_data
def load_er_dot():
    """Graphviz DOT for the Schema-page ER diagram, kept in its own file."""
    try:
        with open(ER_DOT_FILE, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


@st.cache_resource
def get_demo_con():
    """A SEPARATE in-memory DuckDB used only by the Transactions demo page.
    Completely isolated from innout.duckdb so the demo can never affect the
    real orders/menu data."""
    c = duckdb.connect(":memory:")
    c.execute("""CREATE TABLE demo_tills (
                     name    VARCHAR PRIMARY KEY,
                     balance DECIMAL(10,2) CHECK (balance >= 0));""")
    c.execute("INSERT INTO demo_tills VALUES ('Front Till', 100.00), "
              "('Drive-Thru Till', 100.00);")
    return c


# ---------------------------------------------------------------------------
# Natural-language → SQL via Claude (optional; needs the anthropic SDK + key)
# ---------------------------------------------------------------------------
# Configuration read from the .env file (loaded above by _load_dotenv()).
# Both values come straight from .env:
#   ANTHROPIC_API_KEY=sk-ant-...
#   ANTHROPIC_MODEL=claude-sonnet-4-6
# The `or` chains skip empty values so a blank entry falls back to a default.
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY") or ""
ANTHROPIC_MODEL = (os.environ.get("ANTHROPIC_MODEL")
                   or "claude-sonnet-4-6")

# System prompt for the NL→SQL helper. Loaded from an external file so it's
# easy to edit without touching code. Precedence:
#   1. ANTHROPIC_SYSTEM_PROMPT in .env (full override)
#   2. nl2sql_system_prompt.md next to this file
#   3. a short built-in fallback
NL2SQL_PROMPT_FILE = os.path.join(HERE, "nl2sql_system_prompt.md")


def _load_nl2sql_prompt():
    override = os.environ.get("ANTHROPIC_SYSTEM_PROMPT")
    if override:
        return override
    try:
        with open(NL2SQL_PROMPT_FILE, encoding="utf-8") as f:
            text = f.read().strip()
            if text:
                return text
    except Exception:
        pass
    return (
        "You are a DuckDB SQL expert helping an intro DBMS student. "
        "Given the schema, write exactly ONE read-only DuckDB SQL query that "
        "answers the question. Use only tables/columns in the schema. Return "
        "ONLY the SQL — no prose, no explanation, no markdown code fences.")


NL2SQL_SYSTEM_PROMPT = _load_nl2sql_prompt()


def _anthropic_key():
    """API key from .env (ANTHROPIC_API_KEY) or .streamlit/secrets.toml."""
    if ANTHROPIC_API_KEY:
        return ANTHROPIC_API_KEY
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return None


def claude_status():
    """Return (ready: bool, message: str) describing whether NL→SQL works."""
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False, "Run `pip install anthropic` to enable Ask-Claude."
    if not _anthropic_key():
        return False, ("Set your key first:  "
                       "`export ANTHROPIC_API_KEY=sk-ant-...`  "
                       "(or add it to `.streamlit/secrets.toml`).")
    return True, ""


@st.cache_data
def schema_context():
    """A compact text description of every table + columns for the prompt."""
    tbls = list(q("SELECT table_name FROM information_schema.tables "
                  "WHERE table_schema='main' ORDER BY table_name")["table_name"])
    lines = []
    for t in tbls:
        info = q(f"SELECT * FROM pragma_table_info('{t}')")
        cols = ", ".join(f"{r['name']} {r['type']}"
                         for _, r in info.iterrows())
        lines.append(f"{t}({cols})")
    return "\n".join(lines)


def ask_claude_for_sql(question):
    """Send the schema + question to Claude; return a single DuckDB query.
    Uses the ANTHROPIC_MODEL and system prompt configured above (from .env)."""
    import anthropic
    client = anthropic.Anthropic(api_key=_anthropic_key())
    msg = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=700,
        system=NL2SQL_SYSTEM_PROMPT,
        messages=[{"role": "user",
                   "content": f"Schema:\n{schema_context()}\n\n"
                              f"Question: {question}"}],
    )
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") ==
                   "text").strip()
    # Strip accidental code fences
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.lower().startswith("sql"):
            text = text[3:]
    return text.strip()


# ---------------------------------------------------------------------------
# Playground result viewer: a table + a configurable Altair chart
# ---------------------------------------------------------------------------
def _alt_type(df, col):
    import pandas.api.types as pt
    if pt.is_numeric_dtype(df[col]):
        return "Q"
    if pt.is_datetime64_any_dtype(df[col]):
        return "T"
    return "N"


def playground_chart(df):
    """Render chart-type + column pickers and an Altair chart of the result."""
    import pandas.api.types as pt
    num_cols = [c for c in df.columns if pt.is_numeric_dtype(df[c])]
    all_cols = list(df.columns)
    if not num_cols:
        st.info("No numeric column in this result to plot — the table view "
                "tells the whole story here.")
        return
    cat_cols = [c for c in all_cols if c not in num_cols] or all_cols

    # Smart default chart: a time column → Line, otherwise Bar
    default_x = cat_cols[0]
    default_type = "Line" if _alt_type(df, default_x) == "T" else "Bar"
    types = ["Bar", "Horizontal bar", "Line", "Area", "Pie", "Scatter"]

    cc = st.columns(4)
    ctype = cc[0].selectbox("Chart type", types,
                            index=types.index(default_type), key="pg_ctype")
    x = cc[1].selectbox("X / category", all_cols,
                        index=all_cols.index(default_x), key="pg_x")
    y = cc[2].selectbox("Y / value", num_cols, index=0, key="pg_y")
    color_opts = ["(none)"] + [c for c in cat_cols if c != x]
    color = cc[3].selectbox("Color / group", color_opts, key="pg_color")
    color = None if color == "(none)" else color

    tooltip = [x, y] + ([color] if color else [])
    color_enc = (alt.Color(f"{color}:N", title=color,
                           scale=alt.Scale(scheme="tableau10"))
                 if color else alt.value(RED))

    if ctype == "Pie":
        dfp = df.groupby(x, as_index=False)[y].sum()
        total = dfp[y].sum()
        dfp["__share"] = dfp[y] / total if total else 0
        base = alt.Chart(dfp).encode(
            theta=alt.Theta(f"{y}:Q", stack=True),
            color=alt.Color(f"{x}:N", title=x,
                            scale=alt.Scale(scheme="tableau10"),
                            legend=alt.Legend(orient="right", labelLimit=320)),
            tooltip=[alt.Tooltip(f"{x}:N", title=x),
                     alt.Tooltip(f"{y}:Q", title=y, format=",.2f"),
                     alt.Tooltip("__share:Q", title="share", format=".1%")])
        arc = base.mark_arc(innerRadius=55, stroke="#fff", strokeWidth=2)
        # Short % label on each slice; full names live in the legend.
        labels = base.mark_text(radius=98, fontSize=13, fontWeight="bold",
                                color="white").encode(
            text=alt.Text("__share:Q", format=".0%"))
        chart = arc + labels
    elif ctype == "Horizontal bar":
        chart = alt.Chart(df).mark_bar().encode(
            y=alt.Y(f"{x}:{_alt_type(df, x)}",
                    sort="-x" if _alt_type(df, x) == "N" else None, title=x),
            x=alt.X(f"{y}:Q", title=y), color=color_enc, tooltip=tooltip)
    elif ctype == "Line":
        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X(f"{x}:{_alt_type(df, x)}", title=x),
            y=alt.Y(f"{y}:Q", title=y), color=color_enc, tooltip=tooltip)
    elif ctype == "Area":
        chart = alt.Chart(df).mark_area(opacity=0.75).encode(
            x=alt.X(f"{x}:{_alt_type(df, x)}", title=x),
            y=alt.Y(f"{y}:Q", title=y), color=color_enc, tooltip=tooltip)
    elif ctype == "Scatter":
        chart = alt.Chart(df).mark_circle(size=110, opacity=0.7).encode(
            x=alt.X(f"{x}:{_alt_type(df, x)}", title=x),
            y=alt.Y(f"{y}:Q", title=y), color=color_enc, tooltip=tooltip)
    else:   # Bar
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(f"{x}:{_alt_type(df, x)}",
                    sort="-y" if _alt_type(df, x) == "N" else None, title=x),
            y=alt.Y(f"{y}:Q", title=y), color=color_enc, tooltip=tooltip)

    chart = chart.properties(height=400).configure_axis(
        labelColor="#1a1a1a", titleColor="#1a1a1a", labelFontSize=12,
        titleFontSize=13).configure_legend(
        labelColor="#1a1a1a", titleColor="#1a1a1a").configure_view(
        strokeWidth=0)
    st.altair_chart(chart, use_container_width=True)


def playground_results(df):
    """Show a query result as a Table tab and a Chart tab."""
    if df is None:
        return
    if df.empty:
        st.info("Query ran successfully but returned 0 rows.")
        return
    st.success(f"{len(df):,} row(s) · {len(df.columns)} column(s)")
    tab_table, tab_chart = st.tabs(["📋 Table", "📈 Chart"])
    with tab_table:
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download CSV", df.to_csv(index=False),
                           "query_results.csv", "text/csv",
                           key="pg_download")
    with tab_chart:
        playground_chart(df)


def try_violation(sql, params=None):
    """Attempt an INSERT that *should* break a constraint, inside a
    transaction that is ALWAYS rolled back so the database is never modified.
    Returns (accepted: bool, message: str)."""
    con = get_con()
    try:
        con.execute("BEGIN")
        con.execute(sql, params or [])
        con.execute("ROLLBACK")     # undo even if it unexpectedly succeeded
        return True, "The database ACCEPTED this row (no constraint fired)."
    except Exception as e:
        try:
            con.execute("ROLLBACK")
        except Exception:
            pass
        return False, str(e)


def add_store(store_name, city, state):
    """Insert a new store and return its generated store_id."""
    con = get_con()
    new_id = con.execute(
        "SELECT coalesce(max(store_id), 0) + 1 FROM stores").fetchone()[0]
    con.execute("INSERT INTO stores VALUES (?, ?, ?, ?)",
                [new_id, store_name, city, state])
    return new_id


def sql_lit(v):
    """Render a Python value as a SQL literal, for showing the exact
    statements that ran (teaching aid — not used to actually execute)."""
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def place_order(store_id, order_type, payment, cart, subtotal, tax, total):
    """Write one order to orders + order_items + order_item_modifiers,
    atomically. Returns (transaction_id, list_of_executed_SQL_statements).
    The SQL strings carry the real values that were inserted, so the UI can
    show exactly what just happened."""
    con = get_con()
    executed = ["BEGIN;"]
    con.execute("BEGIN")
    try:
        oid = con.execute("SELECT nextval('seq_order_id')").fetchone()[0]
        ts = datetime.now().replace(microsecond=0)
        seq = con.execute(
            """SELECT count(*) FROM orders
               WHERE store_id = ? AND order_ts::DATE = ?::DATE""",
            [store_id, ts]).fetchone()[0] + 1
        txn = f"INO-{store_id:02d}-{ts:%Y%m%d}-{seq:05d}"
        con.execute("""INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    [oid, txn, store_id, ts, order_type, payment,
                     subtotal, TAX_RATE, tax, total])
        executed.append(
            "INSERT INTO orders\n"
            "  (order_id, transaction_id, store_id, order_ts, order_type,\n"
            "   payment_method, subtotal, tax_rate, tax_amount, total)\n"
            f"VALUES ({oid}, {sql_lit(txn)}, {store_id}, "
            f"{sql_lit(str(ts))}, {sql_lit(order_type)}, {sql_lit(payment)}, "
            f"{subtotal}, {TAX_RATE}, {tax}, {total});")
        for ln in cart:
            oiid = con.execute(
                "SELECT nextval('seq_order_item_id')").fetchone()[0]
            con.execute("""INSERT INTO order_items VALUES (?,?,?,?,?,?,?,?)""",
                        [oiid, oid, ln["item_id"], ln["combo_id"], ln["size_id"],
                         ln["qty"], ln["unit_price"], ln["line_total"]])
            executed.append(
                f"-- line: {ln['qty']}x {ln['label']}\n"
                "INSERT INTO order_items\n"
                "  (order_item_id, order_id, item_id, combo_id, size_id,\n"
                "   quantity, unit_price, line_total)\n"
                f"VALUES ({oiid}, {oid}, {sql_lit(ln['item_id'])}, "
                f"{sql_lit(ln['combo_id'])}, {ln['size_id']}, {ln['qty']}, "
                f"{ln['unit_price']}, {ln['line_total']});")
            for mid, name, delta in ln["mods"]:
                con.execute(
                    "INSERT INTO order_item_modifiers VALUES (?,?,?)",
                    [oiid, mid, delta])
                executed.append(
                    f"-- modifier: {name}\n"
                    "INSERT INTO order_item_modifiers "
                    "(order_item_id, modifier_id, price_delta)\n"
                    f"VALUES ({oiid}, {mid}, {delta});")
        con.execute("COMMIT")
        executed.append("COMMIT;")
        return txn, executed
    except Exception:
        con.execute("ROLLBACK")
        raise


def db_ready() -> bool:
    if not os.path.exists(DB_PATH):
        return False
    try:
        return q("SELECT count(*) AS n FROM orders")["n"][0] >= 0
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Gate: build the database if it doesn't exist yet
# ---------------------------------------------------------------------------
if not db_ready():
    st.title("🍔 In-N-Out POS")
    st.warning("Database not found. Build it once to load the menu and "
               "~1,500 demo orders.")
    if st.button("⚙️  Build innout.duckdb now"):
        import build_db
        try:
            get_con().close()       # release any handle to the file first
        except Exception:
            pass
        get_con.clear()
        build_db.main()
        st.rerun()
    st.info("Or run `python build_db.py` in a terminal, then refresh.")
    st.stop()


# ---------------------------------------------------------------------------
# Reference data (cached) for building POS widgets
# ---------------------------------------------------------------------------
@st.cache_data
def ref():
    return {
        "stores": q("SELECT * FROM stores ORDER BY store_id"),
        "items": q("""SELECT i.item_id, i.item_name, i.description,
                             i.category_id, c.category_name, i.is_secret_menu
                      FROM menu_items i JOIN menu_categories c USING(category_id)
                      ORDER BY c.sort_order, i.item_id"""),
        "prices": q("SELECT * FROM item_prices"),
        "sizes": q("SELECT * FROM sizes ORDER BY sort_order"),
        "mods": q("SELECT * FROM modifiers ORDER BY modifier_id"),
        "combos": q("SELECT * FROM combos ORDER BY combo_id"),
    }


R = ref()
TAX_RATE = 0.0925

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.title("🍔 In-N-Out")
st.sidebar.caption("DuckDB + Streamlit · OMIS-105")
page = st.sidebar.radio("Go to", ["🧾 Point of Sale", "📊 Dashboard",
                                  "🧪 SQL Playground", "🗂️ Schema",
                                  "🏪 Stores", "🔄 Transactions"])

store_row = st.sidebar.selectbox(
    "Register / Store",
    list(R["stores"].itertuples(index=False)),
    format_func=lambda r: r.store_name,
)
STORE_ID = store_row.store_id

n_orders = q("SELECT count(*) n FROM orders")["n"][0]
st.sidebar.metric("Orders in database", f"{n_orders:,}")

per_store_sql = """
SELECT s.store_name, count(o.order_id) AS orders
FROM stores s
LEFT JOIN orders o ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY orders DESC;"""
st.sidebar.caption("Orders per store")
st.sidebar.dataframe(q(per_store_sql), hide_index=True,
                     use_container_width=True)
with st.sidebar.expander("🔍 Show SQL"):
    st.code(per_store_sql.strip(), language="sql")


# ===========================================================================
# PAGE 1 · POINT OF SALE
# ===========================================================================
CAT_EMOJI = {"Burgers": "🍔", "Sides": "🍟", "Beverages": "🥤", "Shakes": "🥤"}


def add_to_cart(kind, label, item_id, combo_id, size_id, size_name,
                qty, unit_price, mods):
    line = round((unit_price + sum(d for *_, d in mods)) * qty, 2)
    st.session_state.cart.append({
        "kind": kind, "label": label, "item_id": item_id, "combo_id": combo_id,
        "size_id": int(size_id), "size_name": size_name, "qty": int(qty),
        "unit_price": float(unit_price), "mods": mods, "line_total": line,
    })


if page == "🧾 Point of Sale":
    # POS-specific styling for the menu cards & ticket
    st.markdown("""
    <style>
      .price-tag { color:#E31837; font-weight:800; font-size:1.1rem; }
      .card-name { font-weight:700; font-size:1.02rem; line-height:1.2; }
      table.ticket-totals { width:100%; border-collapse:collapse;
                            font-size:1rem; margin-top:.3rem; }
      table.ticket-totals td { padding:4px 2px; }
      table.ticket-totals td:last-child { text-align:right; font-variant-numeric:tabular-nums; }
      table.ticket-totals tr.grand td { border-top:2px solid #E31837;
            font-weight:800; font-size:1.25rem; color:#E31837; padding-top:8px; }
    </style>""", unsafe_allow_html=True)

    st.title("🧾 Point of Sale")
    st.caption(f"Register: {store_row.store_name} — every placed order "
               "writes a real transaction into DuckDB.")

    with st.expander("💡 Why a database? — what to watch for", expanded=True):
        st.markdown(
            "Placing an order here doesn't just save a file — it writes a "
            "**transaction** into a normalized database, atomically, across "
            "three linked tables (`orders`, `order_items`, "
            "`order_item_modifiers`), stamped with a unique `transaction_id`. "
            "Ring up a sale, then open the **📊 Dashboard**: your order is "
            "already in the revenue, the charts, and the recent-transactions "
            "list. That round-trip — *record an event, then ask questions of "
            "it* — is what a database is **for**. Click any **🔍 Show SQL** to "
            "see the exact query behind every number.")

    if "cart" not in st.session_state:
        st.session_state.cart = []

    left, right = st.columns([3, 2], gap="large")

    # ---- Menu ------------------------------------------------------------
    with left:
        cat_names = list(R["items"].category_name.unique())
        options = ["🍔 Combos"] + [f"{CAT_EMOJI.get(c, '🍴')} {c}"
                                   for c in cat_names]
        sel = st.segmented_control("Menu", options, default=options[0],
                                   label_visibility="collapsed")
        sel = sel or options[0]
        chosen_cat = "Combos" if sel == options[0] else sel.split(" ", 1)[1]

        def card_cols(n):
            """Yield item records grouped into rows of 3 columns."""
            n = list(n)
            for i in range(0, len(n), 3):
                yield st.columns(3), n[i:i + 3]

        if chosen_cat == "Combos":
            for cols, chunk in card_cols(R["combos"].itertuples(index=False)):
                for col, c in zip(cols, chunk):
                    with col, st.container(border=True):
                        st.markdown(f"**{c.combo_name}**")
                        st.caption(c.description)
                        st.markdown(f"<span class='price-tag'>${c.price:.2f}"
                                    "</span>", unsafe_allow_html=True)
                        if st.button("＋ Add", key=f"combo_{c.combo_id}",
                                     use_container_width=True):
                            add_to_cart("combo", c.combo_name, None, c.combo_id,
                                        1, "Regular", 1, c.price, [])
                            st.rerun()
        elif chosen_cat == "Sides":
            # Simplified: present the two ways people order fries as clear,
            # one-tap cards. "Animal Style Fries" is still stored as
            # French Fries + the Animal Style modifier (normalized).
            fries_price = float(R["prices"][(R["prices"].item_id == 6)
                                & (R["prices"].size_id == 1)].price.iloc[0])
            animal = R["mods"][R["mods"].modifier_name == "Animal Style"].iloc[0]
            animal_mod = [(int(animal.modifier_id), animal.modifier_name,
                           float(animal.price_delta))]
            side_cards = [
                ("French Fries",
                 "Freshly made, 100% real potatoes", []),
                ("Animal Style Fries",
                 "Fries topped with melted cheese, grilled onions & spread",
                 animal_mod),
            ]
            scols = st.columns(2)
            for i, (card_name, desc, mods) in enumerate(side_cards):
                with scols[i], st.container(border=True):
                    st.markdown(f"**{card_name}**")
                    st.caption(desc)
                    st.markdown(f"<span class='price-tag'>${fries_price:.2f}"
                                "</span>", unsafe_allow_html=True)
                    if st.button("＋ Add", key=f"side_{i}",
                                 use_container_width=True):
                        add_to_cart("item", card_name, 6, None, 1, "Regular",
                                    1, fries_price, mods)
                        st.rerun()
        else:
            items = R["items"][R["items"].category_name == chosen_cat]
            for cols, chunk in card_cols(items.itertuples(index=False)):
                for col, it in zip(cols, chunk):
                    iid = int(it.item_id)
                    avail = (R["prices"][R["prices"].item_id == iid]
                             .merge(R["sizes"], on="size_id")
                             .sort_values("sort_order"))
                    has_sizes = len(avail) > 1
                    if it.category_id == 1:
                        pool = R["mods"][R["mods"].applies_to.isin(
                            ["burger", "any"])]
                    elif iid == 6:
                        pool = R["mods"][R["mods"].applies_to.isin(
                            ["fries", "any"])]
                    else:
                        pool = R["mods"].iloc[0:0]
                    has_mods = len(pool) > 0

                    name = it.item_name + (" ⭐" if it.is_secret_menu else "")
                    price_lbl = (f"from ${avail.price.min():.2f}" if has_sizes
                                 else f"${avail.price.iloc[0]:.2f}")

                    with col, st.container(border=True):
                        st.markdown(f"**{name}**")
                        if pd.notna(it.description) and it.description:
                            st.caption(it.description)
                        st.markdown(f"<span class='price-tag'>{price_lbl}"
                                    "</span>", unsafe_allow_html=True)

                        if not (has_sizes or has_mods):
                            if st.button("＋ Add", key=f"add_{iid}",
                                         use_container_width=True):
                                add_to_cart("item", it.item_name, iid, None,
                                            int(avail.size_id.iloc[0]),
                                            avail.size_name.iloc[0], 1,
                                            float(avail.price.iloc[0]), [])
                                st.rerun()
                        else:
                            with st.popover("＋ Add", use_container_width=True):
                                st.markdown(f"**{it.item_name}**")
                                if has_sizes:
                                    sc = st.radio(
                                        "Size",
                                        list(avail.itertuples(index=False)),
                                        key=f"sz_{iid}", horizontal=True,
                                        format_func=lambda r:
                                            f"{r.size_name} · ${r.price:.2f}")
                                    size_id, size_name = sc.size_id, sc.size_name
                                    unit = float(sc.price)
                                else:
                                    size_id = int(avail.size_id.iloc[0])
                                    size_name = avail.size_name.iloc[0]
                                    unit = float(avail.price.iloc[0])
                                picked = []
                                if has_mods:
                                    picked = st.multiselect(
                                        "Customizations",
                                        list(pool.itertuples(index=False)),
                                        key=f"md_{iid}",
                                        format_func=lambda m: m.modifier_name
                                        + (f" (+${m.price_delta:.2f})"
                                           if m.price_delta else ""))
                                qty = st.number_input("Quantity", 1, 20, 1,
                                                      key=f"qty_{iid}")
                                if st.button("Add to ticket", key=f"go_{iid}",
                                             use_container_width=True):
                                    mods = [(int(m.modifier_id), m.modifier_name,
                                             float(m.price_delta))
                                            for m in picked]
                                    add_to_cart("item", it.item_name, iid, None,
                                                size_id, size_name, qty, unit,
                                                mods)
                                    st.rerun()

    # ---- Order ticket ----------------------------------------------------
    with right:
        st.subheader("🧾 Order Ticket")
        cart = st.session_state.cart
        if not cart:
            st.info("Your ticket is empty. Tap items on the menu to add them.")
        else:
            for idx, ln in enumerate(cart):
                with st.container(border=True):
                    c1, c2, c3 = st.columns([6, 2, 1], vertical_alignment="center")
                    size = ("" if ln["size_name"] == "Regular"
                            else f" · {ln['size_name']}")
                    c1.markdown(f"**{ln['qty']}× {ln['label']}**{size}")
                    if ln["mods"]:
                        c1.caption("+ " + ", ".join(m[1] for m in ln["mods"]))
                    c2.markdown(f"${ln['line_total']:.2f}")
                    if c3.button("✕", key=f"del_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()

            subtotal = round(sum(l["line_total"] for l in cart), 2)
            tax = round(subtotal * TAX_RATE, 2)
            total = round(subtotal + tax, 2)
            st.markdown(f"""
<table class="ticket-totals">
  <tr><td>Subtotal</td><td>${subtotal:.2f}</td></tr>
  <tr><td>Tax ({TAX_RATE * 100:g}%)</td><td>${tax:.2f}</td></tr>
  <tr class="grand"><td>Total</td><td>${total:.2f}</td></tr>
</table>""", unsafe_allow_html=True)
            st.write("")

            order_type = st.selectbox("Order type",
                                      ["Drive-Thru", "Dine-In", "Takeout"])
            payment = st.selectbox("Payment", ["Card", "Mobile", "Cash"])

            cbtn, xbtn = st.columns(2)
            if cbtn.button("✅ Place order", use_container_width=True):
                txn, executed_sql = place_order(
                    STORE_ID, order_type, payment, cart,
                    subtotal, tax, total)
                st.session_state.last_receipt = {
                    "txn": txn, "cart": list(cart), "subtotal": subtotal,
                    "tax": tax, "total": total, "type": order_type,
                    "payment": payment, "sql": executed_sql,
                }
                st.session_state.cart = []
                st.rerun()
            if xbtn.button("🗑️ Clear", use_container_width=True):
                st.session_state.cart = []
                st.rerun()

        # Receipt of the just-placed order
        if st.session_state.get("last_receipt"):
            rc = st.session_state.last_receipt
            lines = "".join(
                f"{l['qty']}x {l['label']:<22} {l['line_total']:>6.2f}\n"
                + ("".join(f"     + {m[1]}\n" for m in l["mods"]))
                for l in rc["cart"])
            st.markdown(f"""<div class="receipt">
IN-N-OUT BURGER<br>{store_row.store_name}<br>
Txn: {rc['txn']}<br>{rc['type']} · {rc['payment']}<br>
------------------------------<br>
<pre style="margin:0">{lines}</pre>
------------------------------<br>
Subtotal {rc['subtotal']:>18.2f}<br>
Tax      {rc['tax']:>18.2f}<br>
<b>TOTAL    {rc['total']:>18.2f}</b><br>
</div>""", unsafe_allow_html=True)
            st.success(f"Saved as transaction {rc['txn']}")

    show_sql("""
-- Placing an order writes to THREE tables inside one transaction:
INSERT INTO orders (order_id, transaction_id, store_id, order_ts, order_type,
                    payment_method, subtotal, tax_rate, tax_amount, total)
VALUES (nextval('seq_order_id'), ?, ?, now(), ?, ?, ?, ?, ?, ?);

INSERT INTO order_items (order_item_id, order_id, item_id, combo_id, size_id,
                         quantity, unit_price, line_total)
VALUES (nextval('seq_order_item_id'), ?, ?, ?, ?, ?, ?, ?);

INSERT INTO order_item_modifiers (order_item_id, modifier_id, price_delta)
VALUES (?, ?, ?);
""", "🔍 Show SQL behind 'Place order'")

    # Full-width view of the statements that actually ran for the last order
    if st.session_state.get("last_receipt", {}).get("sql"):
        with st.expander("🔍 Show the SQL that *actually* ran (real values)",
                         expanded=True):
            st.caption("The same template above, now committed with the last "
                       "order's real keys and prices:")
            st.code("\n\n".join(st.session_state.last_receipt["sql"]),
                    language="sql")


# ===========================================================================
# PAGE 2 · DASHBOARD
# ===========================================================================
if page == "📊 Dashboard":
    st.title("📊 Live Analytics Dashboard")
    st.caption("Every metric is a SQL query against the same database the "
               "register writes to. Expand **Show SQL** to see how.")

    kpi = q("""
        SELECT count(*)                         AS orders,
               sum(total)                        AS revenue,
               avg(total)                        AS avg_order,
               (SELECT sum(quantity) FROM order_items) AS items_sold
        FROM orders
    """)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total orders", f"{int(kpi.orders[0]):,}")
    k2.metric("Revenue", f"${kpi.revenue[0]:,.0f}")
    k3.metric("Avg order value", f"${kpi.avg_order[0]:.2f}")
    k4.metric("Items sold", f"{int(kpi.items_sold[0]):,}")
    show_sql("""
SELECT count(*) AS orders, sum(total) AS revenue, avg(total) AS avg_order,
       (SELECT sum(quantity) FROM order_items) AS items_sold
FROM orders;""")

    kpi2 = q("""
        SELECT
            (SELECT count(*) FROM stores)                       AS stores,
            (SELECT avg(line_total) FROM order_items)            AS avg_line,
            (SELECT count(*) FILTER (WHERE combo_id IS NOT NULL)
                  * 100.0 / count(*) FROM order_items)           AS combo_pct,
            (SELECT count(DISTINCT order_item_id)
               FROM order_item_modifiers) * 100.0
               / (SELECT count(*) FROM order_items)              AS custom_pct
    """)
    j1, j2, j3, j4 = st.columns(4)
    j1.metric("Stores", f"{int(kpi2.stores[0]):,}")
    j2.metric("Avg line item", f"${kpi2.avg_line[0]:.2f}")
    j3.metric("Combo attach rate", f"{kpi2.combo_pct[0]:.1f}%")
    j4.metric("Lines customized", f"{kpi2.custom_pct[0]:.1f}%")
    show_sql("""
SELECT
  (SELECT count(*) FROM stores) AS stores,
  (SELECT avg(line_total) FROM order_items) AS avg_line,
  -- share of order lines that are combos
  (SELECT count(*) FILTER (WHERE combo_id IS NOT NULL) * 100.0 / count(*)
   FROM order_items) AS combo_pct,
  -- share of lines that carry at least one modifier
  (SELECT count(DISTINCT order_item_id) FROM order_item_modifiers) * 100.0
   / (SELECT count(*) FROM order_items) AS custom_pct;""")

    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Revenue by day")
        sql = """
SELECT order_ts::DATE AS day, sum(total) AS revenue
FROM orders GROUP BY day ORDER BY day;"""
        d = q(sql)
        st.line_chart(d.set_index("day")["revenue"], color=RED)
        show_sql(sql)

    with c2:
        st.subheader("Orders by hour of day")
        sql = """
SELECT date_part('hour', order_ts) AS hour, count(*) AS orders
FROM orders GROUP BY hour ORDER BY hour;"""
        d = q(sql)
        st.bar_chart(d.set_index("hour")["orders"], color=YELLOW)
        show_sql(sql)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Top 10 menu items")
        sql = """
SELECT m.item_name, sum(oi.quantity) AS qty_sold
FROM order_items oi
JOIN menu_items m ON m.item_id = oi.item_id
GROUP BY m.item_name
ORDER BY qty_sold DESC
LIMIT 10;"""
        d = q(sql)
        st.bar_chart(d.set_index("item_name")["qty_sold"], horizontal=True,
                     color=RED)
        show_sql(sql)

    with c4:
        st.subheader("Revenue by category")
        sql = """
SELECT c.category_name,
       sum(oi.line_total) AS revenue
FROM order_items oi
JOIN menu_items m    ON m.item_id = oi.item_id
JOIN menu_categories c ON c.category_id = m.category_id
GROUP BY c.category_name
ORDER BY revenue DESC;"""
        d = q(sql)
        st.bar_chart(d.set_index("category_name")["revenue"], color=YELLOW)
        st.caption("Combo lines are excluded here (they have no single item_id) "
                   "— a teachable nuance of the normalized model.")
        show_sql(sql)

    c5, c6 = st.columns(2)
    with c5:
        st.subheader("Revenue by store")
        sql = """
SELECT s.store_name, count(*) AS orders, sum(o.total) AS revenue
FROM orders o JOIN stores s ON s.store_id = o.store_id
GROUP BY s.store_name ORDER BY revenue DESC;"""
        d = q(sql)
        st.dataframe(d, hide_index=True, use_container_width=True)
        show_sql(sql)

    with c6:
        st.subheader("Most-loved customizations")
        sql = """
SELECT md.modifier_name, count(*) AS times_added
FROM order_item_modifiers oim
JOIN modifiers md ON md.modifier_id = oim.modifier_id
GROUP BY md.modifier_name ORDER BY times_added DESC LIMIT 8;"""
        d = q(sql)
        st.bar_chart(d.set_index("modifier_name")["times_added"],
                     horizontal=True, color=RED)
        show_sql(sql)

    c7, c8 = st.columns(2)
    with c7:
        st.subheader("Order type mix")
        sql = """
SELECT order_type, count(*) AS orders, sum(total) AS revenue
FROM orders GROUP BY order_type ORDER BY revenue DESC;"""
        d = q(sql)
        st.bar_chart(d.set_index("order_type")["revenue"], color=RED)
        show_sql(sql)
    with c8:
        st.subheader("Payment method mix")
        sql = """
SELECT payment_method, count(*) AS orders, sum(total) AS revenue
FROM orders GROUP BY payment_method ORDER BY revenue DESC;"""
        d = q(sql)
        st.bar_chart(d.set_index("payment_method")["revenue"], color=YELLOW)
        show_sql(sql)

    st.subheader("Order type mix by store")
    sql = """
SELECT s.store_name, o.order_type, count(*) AS orders
FROM orders o
JOIN stores s ON s.store_id = o.store_id
GROUP BY s.store_name, o.order_type
ORDER BY s.store_name, o.order_type;"""
    d = q(sql)
    if d.empty:
        st.info("No orders yet.")
    else:
        pivot = d.pivot(index="store_name", columns="order_type",
                        values="orders").fillna(0).astype(int)
        st.bar_chart(pivot)
        st.dataframe(pivot, use_container_width=True)
        st.caption("Stacked bars show each store's split across "
                   "Drive-Thru / Dine-In / Takeout.")
    show_sql(sql)

    st.divider()
    st.subheader("🔥 Busiest times — orders by weekday & hour")
    sql = """
SELECT dayname(order_ts)                 AS weekday,
       date_part('hour', order_ts)::INT  AS hour,
       count(*)                          AS orders
FROM orders
GROUP BY weekday, hour
ORDER BY hour;"""
    d = q(sql)
    if d.empty:
        st.info("No orders yet.")
    else:
        order_days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                      "Friday", "Saturday", "Sunday"]
        heat = (
            alt.Chart(d).mark_rect().encode(
                x=alt.X("hour:O", title="Hour of day"),
                y=alt.Y("weekday:N", sort=order_days, title=None),
                color=alt.Color("orders:Q", title="Orders",
                                scale=alt.Scale(scheme="reds")),
                tooltip=["weekday", "hour", "orders"],
            ).properties(height=240)
        )
        st.altair_chart(heat, use_container_width=True)
        st.caption("Darker = more orders. The lunch and dinner rushes light up.")
    show_sql(sql)

    st.divider()
    c9, c10 = st.columns([3, 2])
    with c9:
        st.subheader("Cumulative revenue (running total)")
        sql = """
SELECT day,
       sum(daily) OVER (ORDER BY day) AS cumulative_revenue
FROM (
    SELECT order_ts::DATE AS day, sum(total) AS daily
    FROM orders GROUP BY day
) ORDER BY day;"""
        d = q(sql)
        st.area_chart(d.set_index("day")["cumulative_revenue"], color=RED)
        st.caption("A SQL window function (SUM ... OVER (ORDER BY day)) "
                   "accumulates revenue over the year.")
        show_sql(sql)
    with c10:
        st.subheader("Best seller at each store")
        sql = """
SELECT s.store_name, m.item_name, sum(oi.quantity) AS sold
FROM order_items oi
JOIN orders o     ON o.order_id  = oi.order_id
JOIN stores s     ON s.store_id  = o.store_id
JOIN menu_items m ON m.item_id   = oi.item_id
GROUP BY s.store_name, m.item_name
QUALIFY row_number() OVER (PARTITION BY s.store_name
                           ORDER BY sum(oi.quantity) DESC) = 1
ORDER BY sold DESC;"""
        st.dataframe(q(sql), hide_index=True, use_container_width=True)
        st.caption("QUALIFY + ROW_NUMBER() picks each store's #1 item.")
        show_sql(sql)

    st.divider()
    st.subheader("Monthly revenue by store")
    sql = """
SELECT date_trunc('month', o.order_ts) AS month,
       s.store_name,
       sum(o.total) AS revenue
FROM orders o
JOIN stores s ON s.store_id = o.store_id
GROUP BY month, s.store_name
ORDER BY month, s.store_name;"""
    d = q(sql)
    if d.empty:
        st.info("No orders yet.")
    else:
        d["month"] = pd.to_datetime(d["month"]).dt.strftime("%Y-%m")
        pivot = d.pivot(index="month", columns="store_name",
                        values="revenue").fillna(0).round(2)
        st.bar_chart(pivot)
        st.dataframe(pivot, use_container_width=True)
    show_sql(sql)

    st.divider()
    st.subheader("🧾 Recent transactions")
    sql = """
SELECT o.transaction_id, o.order_ts, s.store_name, o.order_type,
       o.payment_method, count(oi.order_item_id) AS lines, o.total
FROM orders o
JOIN stores s        ON s.store_id = o.store_id
JOIN order_items oi  ON oi.order_id = o.order_id
GROUP BY ALL
ORDER BY o.order_ts DESC
LIMIT 15;"""
    st.dataframe(q(sql), hide_index=True, use_container_width=True)
    show_sql(sql)


# ===========================================================================
# PAGE 3 · SQL PLAYGROUND
# ===========================================================================
if page == "🧪 SQL Playground":
    st.title("🧪 SQL Playground")
    st.caption("Ask a question in plain English and let Claude draft the SQL, "
               "or write your own. Read-only (SELECT / WITH / EXPLAIN) for "
               "safety — review every query before you run it.")

    EXAMPLES = {
        "— pick an example —": "",
        "Best-selling burgers": """SELECT m.item_name, sum(oi.quantity) AS sold
FROM order_items oi JOIN menu_items m ON m.item_id = oi.item_id
WHERE m.category_id = 1
GROUP BY m.item_name ORDER BY sold DESC;""",
        "Average basket size per order type": """SELECT o.order_type,
       round(avg(o.total), 2) AS avg_check,
       count(*) AS orders
FROM orders o GROUP BY o.order_type ORDER BY avg_check DESC;""",
        "Busiest hour at each store": """SELECT s.store_name,
       date_part('hour', o.order_ts) AS hour,
       count(*) AS orders
FROM orders o JOIN stores s ON s.store_id = o.store_id
GROUP BY s.store_name, hour
QUALIFY row_number() OVER (PARTITION BY s.store_name ORDER BY count(*) DESC) = 1
ORDER BY orders DESC;""",
        "Items that are never customized": """SELECT m.item_name
FROM menu_items m
WHERE m.item_id NOT IN (
    SELECT oi.item_id FROM order_items oi
    JOIN order_item_modifiers oim ON oim.order_item_id = oi.order_item_id
    WHERE oi.item_id IS NOT NULL)
ORDER BY m.item_name;""",
        "Combo vs à la carte revenue": """SELECT
  CASE WHEN combo_id IS NOT NULL THEN 'Combo' ELSE 'A la carte' END AS kind,
  count(*) AS lines, round(sum(line_total), 2) AS revenue
FROM order_items GROUP BY kind;""",
    }

    if "pg_sql" not in st.session_state:
        st.session_state.pg_sql = "SELECT * FROM orders LIMIT 20;"

    # ---- Ask Claude (natural language → SQL) ----------------------------
    st.markdown("#### 🤖 Ask in plain English")
    ready, why = claude_status()
    with st.form("ask_claude", clear_on_submit=False):
        question = st.text_input(
            "Question",
            placeholder="e.g. Which store sells the most shakes on weekends?",
            label_visibility="collapsed")
        asked = st.form_submit_button("✨ Ask Claude", disabled=not ready)
    if not ready:
        st.info(why)
    if asked and question.strip():
        try:
            with st.spinner("Claude is writing SQL…"):
                generated = ask_claude_for_sql(question.strip())
            st.session_state.pg_sql = generated
            st.success("Claude wrote a query — review it below, then Run.")
        except Exception as e:
            st.error(f"Claude error: {e}")

    # ---- Examples (load into the editor) --------------------------------
    def _load_example():
        chosen = st.session_state.pg_example
        if EXAMPLES.get(chosen):
            st.session_state.pg_sql = EXAMPLES[chosen]

    st.selectbox("Or load an example", list(EXAMPLES.keys()),
                 key="pg_example", on_change=_load_example)

    # ---- Editor + run ---------------------------------------------------
    st.text_area("SQL", height=340, key="pg_sql")

    if st.button("▶️ Run query"):
        sql = st.session_state.pg_sql
        clean = sql.strip().rstrip(";").lstrip().lower()
        if not clean.startswith(("select", "with", "explain", "describe",
                                 "show", "pragma", "summarize")):
            st.session_state.pg_result = None
            st.error("Only read-only statements are allowed here "
                     "(SELECT / WITH / EXPLAIN / DESCRIBE / SHOW / PRAGMA).")
        else:
            try:
                # New result set → reset the chart pickers to fresh defaults
                for k in ("pg_ctype", "pg_x", "pg_y", "pg_color"):
                    st.session_state.pop(k, None)
                st.session_state.pg_result = q(sql)
            except Exception as e:
                st.session_state.pg_result = None
                st.error(f"Query error: {e}")

    # Render the most recent result (persists across chart-option changes)
    if isinstance(st.session_state.get("pg_result"), pd.DataFrame):
        st.divider()
        st.subheader("Results")
        playground_results(st.session_state.pg_result)


# ===========================================================================
# PAGE 4 · SCHEMA
# ===========================================================================
if page == "🗂️ Schema":
    st.title("🗂️ Database Schema")
    st.caption("A fully normalized relational model — the heart of the lesson.")

    st.markdown("""
**Relationships (one-to-many, parent → child):**

- `menu_categories` → `menu_items`
- `menu_items` → `item_prices` ← `sizes`  *(price of each item at each size)*
- `menu_items` → `combos`  *(the combo's headline burger)*
- `stores` → `orders` → `order_items` → `order_item_modifiers` ← `modifiers`
- `menu_items` / `combos` / `sizes` → `order_items`

`orders.transaction_id` is the human-readable business key; `order_id` is the
surrogate primary key the foreign keys point to.
""")

    st.subheader("Entity-Relationship (ER) diagram")
    er_dot = load_er_dot()
    if er_dot:
        st.graphviz_chart(er_dot, use_container_width=True)
    else:
        st.info("ER diagram file `er_diagram.dot` not found.")

    st.markdown("""
**How to read this diagram**

- Each box is a **table**. `PK` marks the **primary key** (the unique id for a
  row); `FK` marks a **foreign key** (a pointer to another table's PK);
  `UQ` marks a **unique** business key.
- The **crow's-foot** end of each line (the "many" side) sits on the *child*
  table. So one `stores` row connects to **many** `orders`; one `orders` row to
  **many** `order_items`. Read each line as *"one parent has many children."*
- The two **yellow** boxes are **bridge (junction) tables** that resolve
  many-to-many relationships:
  - `item_prices` — one item can come in many sizes, and one size applies to
    many items, so the price lives at the *intersection* `(item_id, size_id)`.
  - `order_item_modifiers` — one order line can carry many modifiers, and one
    modifier can appear on many lines.
- `order_items` carries **two** nullable foreign keys, `item_id` *or*
  `combo_id`. A line is one or the other — enforced by a `CHECK` constraint —
  which is why combo lines don't join to `menu_items`.
""")

    # Logical order (reference tables first, then transaction tables)
    LOGICAL = ["stores", "menu_categories", "sizes", "menu_items",
               "item_prices", "modifiers", "combos", "orders",
               "order_items", "order_item_modifiers"]
    tbls = list(q("SELECT table_name FROM information_schema.tables "
                  "WHERE table_schema='main'")["table_name"])
    table_list = [x for x in LOGICAL if x in tbls] + \
                 [x for x in tbls if x not in LOGICAL]

    st.subheader("Tables at a glance")
    overview = []
    for tname in table_list:
        nrow = q(f"SELECT count(*) AS n FROM {tname}")["n"][0]
        ncol = q(f"SELECT count(*) AS n FROM pragma_table_info('{tname}')")["n"][0]
        overview.append({"table": tname, "rows": int(nrow),
                         "columns": int(ncol)})
    st.dataframe(pd.DataFrame(overview), hide_index=True,
                 use_container_width=True)

    st.divider()
    st.subheader("🔍 Inspect a table")
    t = st.selectbox("Choose a table", table_list)

    rowcount = int(q(f"SELECT count(*) AS n FROM {t}")["n"][0])
    # SELECT * avoids quoting the reserved words `name`/`type`; rename in pandas
    info = q(f"SELECT * FROM pragma_table_info('{t}')")
    cons = q(f"""SELECT constraint_type, constraint_text,
                        constraint_column_names
                 FROM duckdb_constraints() WHERE table_name = '{t}'""")

    # Which columns participate in a foreign key?
    fk_cols = set()
    for _, r in cons.iterrows():
        if r["constraint_type"] == "FOREIGN KEY":
            cn = r["constraint_column_names"]
            if cn is not None:
                for c in cn:
                    fk_cols.add(c)

    m1, m2, m3 = st.columns(3)
    m1.metric("Rows", f"{rowcount:,}")
    m2.metric("Columns", f"{len(info):,}")
    m3.metric("Foreign keys", f"{len(fk_cols):,}")

    st.markdown("**Columns & metadata**")
    meta = pd.DataFrame({
        "column": info["name"],
        "type": info["type"],
        "nullable": info["notnull"].map(lambda x: "NO" if x else "YES"),
        "default": info["dflt_value"],
        "key": [", ".join((["🔑 PK"] if pk else [])
                          + (["🔗 FK"] if name in fk_cols else []))
                for name, pk in zip(info["name"], info["pk"])],
    })
    st.dataframe(meta, hide_index=True, use_container_width=True)

    if len(cons):
        st.markdown("**Constraints** (keys, checks, uniqueness)")
        st.dataframe(cons[["constraint_type", "constraint_text"]],
                     hide_index=True, use_container_width=True)

    st.markdown("**Sample rows**")
    n_rows = st.slider("Rows to preview", 5, 100, 10, 5, key="schema_rows")
    st.dataframe(q(f"SELECT * FROM {t} LIMIT {n_rows}"),
                 use_container_width=True)

    show_sql(f"""-- column metadata
SELECT * FROM pragma_table_info('{t}');

-- constraints (PK / FK / CHECK / UNIQUE)
SELECT constraint_type, constraint_text
FROM duckdb_constraints() WHERE table_name = '{t}';

-- sample rows
SELECT * FROM {t} LIMIT {n_rows};""")

    # -- Constraint demo ---------------------------------------------------
    st.divider()
    st.subheader("🧨 Try to break it — watch the database say no")
    st.caption("Each button attempts an INSERT that violates a constraint. "
               "It runs inside a transaction that is **always rolled back**, "
               "so your data is never changed — you just see the exact error "
               "the database raises to protect its own integrity.")

    a_order = q("SELECT min(order_id) AS x FROM orders")["x"][0]
    a_txn = q("SELECT min(transaction_id) AS x FROM orders")["x"][0]
    valid_order = int(a_order) if a_order is not None else 1

    DEMOS = [
        ("Orphan foreign key",
         "Add an order line that points to order #999999 — an order that "
         "doesn't exist. The FOREIGN KEY refuses it.",
         "INSERT INTO order_items VALUES "
         "(999999, 999999, 1, NULL, 1, 1, 1.00, 1.00);",
         "INSERT INTO order_items VALUES "
         "(999999, 999999, 1, NULL, 1, 1, 1.00, 1.00)", None),
        ("Duplicate primary key",
         "Add a second store with store_id = 1, which already exists. The "
         "PRIMARY KEY must be unique.",
         "INSERT INTO stores VALUES (1, 'Copycat', 'Nowhere', 'CA');",
         "INSERT INTO stores VALUES (1, 'Copycat', 'Nowhere', 'CA')", None),
        ("Broken CHECK constraint",
         "Add an order line that is neither an item nor a combo (both NULL). "
         "The CHECK (item_id IS NOT NULL OR combo_id IS NOT NULL) blocks it.",
         "INSERT INTO order_items VALUES\n"
         f"  (999998, {valid_order}, NULL, NULL, 1, 1, 1.00, 1.00);",
         "INSERT INTO order_items VALUES (?,?,?,?,?,?,?,?)",
         [999998, valid_order, None, None, 1, 1, 1.00, 1.00]),
        ("Duplicate UNIQUE key",
         "Add an order reusing an existing transaction_id. That column is "
         "UNIQUE — no two receipts can share a number.",
         "INSERT INTO orders VALUES (999997, '<existing txn>', 1, now(),\n"
         "  'Dine-In', 'Card', 1.00, 0.0925, 0.09, 1.09);",
         "INSERT INTO orders VALUES (999997, ?, 1, now(), "
         "'Dine-In', 'Card', 1.00, 0.0925, 0.09, 1.09)",
         [a_txn]),
    ]

    dcols = st.columns(2)
    for i, (title, desc, shown_sql, run_sql, params) in enumerate(DEMOS):
        with dcols[i % 2], st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(desc)
            st.code(shown_sql, language="sql")
            if st.button(f"Run it ▶", key=f"demo_{i}"):
                accepted, msg = try_violation(run_sql, params)
                if accepted:
                    st.warning("⚠️ " + msg)
                else:
                    st.error("🛡️ Rejected by the database:")
                    st.code(msg, language="text")


# ===========================================================================
# PAGE 5 · STORES
# ===========================================================================
if page == "🏪 Stores":
    st.title("🏪 Stores")
    st.caption("Review the restaurants in the database, or open a new one. "
               "Adding a store is a single INSERT — and it instantly becomes "
               "selectable as a register on the Point of Sale screen.")

    st.subheader("Current stores")
    sql = """
SELECT s.store_id, s.store_name, s.city, s.state,
       count(o.order_id)              AS orders,
       coalesce(round(sum(o.total), 2), 0) AS revenue
FROM stores s
LEFT JOIN orders o ON o.store_id = s.store_id
GROUP BY ALL
ORDER BY s.store_id;"""
    st.dataframe(q(sql), hide_index=True, use_container_width=True)
    show_sql(sql)

    st.divider()
    st.subheader("➕ Open a new store")
    with st.form("add_store_form", clear_on_submit=True):
        store_name = st.text_input(
            "Store name", placeholder="In-N-Out #500 – Cupertino")
        c1, c2 = st.columns([3, 1])
        city = c1.text_input("City", placeholder="Cupertino")
        state = c2.text_input("State", value="CA", max_chars=2)
        submitted = st.form_submit_button("Add store")

    if submitted:
        if not store_name.strip() or not city.strip():
            st.error("Please enter at least a store name and city.")
        else:
            new_id = add_store(store_name.strip(), city.strip(),
                               (state.strip() or "CA").upper())
            ref.clear()   # refresh cached stores so the register dropdown updates
            st.success(f"Opened store #{new_id}: {store_name.strip()} — "
                       "it's now available as a register on the POS screen.")
            st.rerun()

    show_sql("""
-- Adding a store is one INSERT; store_id is generated from the current max:
INSERT INTO stores (store_id, store_name, city, state)
VALUES ((SELECT coalesce(max(store_id), 0) + 1 FROM stores), ?, ?, ?);
""", "🔍 Show SQL behind 'Add store'")


# ===========================================================================
# PAGE 6 · TRANSACTIONS (atomicity demo — fully isolated in-memory sandbox)
# ===========================================================================
if page == "🔄 Transactions":
    st.title("🔄 Transactions: COMMIT vs ROLLBACK")
    st.caption("Move cash between two tills and watch what a transaction "
               "guarantees. This runs in a **separate in-memory database** — "
               "it never touches your orders or menu data.")

    with st.expander("💡 What is a transaction? (the **A** in ACID)",
                     expanded=True):
        st.markdown(
            "A **transaction** groups several writes so they happen "
            "**all-or-nothing** (*atomicity*). Moving money is the classic "
            "example: it's two steps — *debit* one till and *credit* the "
            "other. If the system fails after the debit but before the "
            "credit, money would vanish into thin air. A transaction prevents "
            "that: either **`COMMIT`** makes *both* steps permanent, or "
            "**`ROLLBACK`** undoes *everything*, as if nothing happened.")

    amount = st.slider("Amount to transfer (Front Till → Drive-Thru Till)",
                       5, 100, 40, 5, format="$%d")
    scenario = st.radio(
        "Pick a scenario",
        ["✅ Everything works → COMMIT",
         "💥 Failure after the debit → ROLLBACK"],
        help="The 'failure' simulates a crash/power-loss between the two "
             "writes — the most important case a transaction protects against.")
    fail = scenario.startswith("💥")

    def run_txn_demo(amount, fail):
        con = get_demo_con()
        con.execute("UPDATE demo_tills SET balance = 100.00")   # reset baseline
        steps = []

        def snap(label, kind, sql=None, note=None):
            df = con.execute("SELECT name AS till, balance FROM demo_tills "
                             "ORDER BY name DESC").df()
            steps.append({"label": label, "kind": kind, "sql": sql,
                          "note": note, "df": df,
                          "total": float(df["balance"].sum())})

        snap("Starting balances — committed, books balanced", "ok")

        con.execute("BEGIN")
        snap("BEGIN — open a transaction", "begin", sql="BEGIN TRANSACTION;")

        con.execute("UPDATE demo_tills SET balance = balance - ? "
                    "WHERE name = 'Front Till'", [amount])
        snap(f"Debit Front Till by ${amount} (uncommitted)", "write",
             sql=f"UPDATE demo_tills SET balance = balance - {amount}\n"
                 f"WHERE name = 'Front Till';",
             note="Notice the total cash no longer adds to $200 — the books "
                  "are momentarily out of balance *inside* the transaction.")

        if not fail:
            con.execute("UPDATE demo_tills SET balance = balance + ? "
                        "WHERE name = 'Drive-Thru Till'", [amount])
            snap(f"Credit Drive-Thru Till by ${amount} (uncommitted)", "write",
                 sql=f"UPDATE demo_tills SET balance = balance + {amount}\n"
                     f"WHERE name = 'Drive-Thru Till';")
            con.execute("COMMIT")
            snap("COMMIT — both writes are now permanent", "commit",
                 sql="COMMIT;",
                 note="Total is back to $200 and the transfer is saved. "
                      "Atomicity held: both steps landed together.")
        else:
            snap("💥 Crash before the credit could run!", "fail",
                 note="The credit never happened. Without a transaction, the "
                      "Front Till would be permanently short — money lost.")
            con.execute("ROLLBACK")
            snap("ROLLBACK — the whole transaction is undone", "rollback",
                 sql="ROLLBACK;",
                 note="The debit is reversed. Balances are back to the "
                      "starting state and total is $200 again — as if nothing "
                      "ever happened. That's atomicity.")
        return steps

    if st.button("▶️ Run the transaction step by step"):
        steps = run_txn_demo(amount, fail)
        st.divider()
        badge = {"ok": "🟢", "begin": "🔵", "write": "🟡", "commit": "🟢",
                 "fail": "🔴", "rollback": "🟣"}
        for i, s in enumerate(steps, 1):
            with st.container(border=True):
                st.markdown(f"### {badge.get(s['kind'], '•')} "
                            f"Step {i} — {s['label']}")
                if s["sql"]:
                    st.code(s["sql"], language="sql")
                left, right = st.columns([3, 1])
                left.dataframe(s["df"], hide_index=True,
                               use_container_width=True)
                balanced = abs(s["total"] - 200.0) < 0.005
                right.metric("Total cash", f"${s['total']:.2f}",
                             delta=None if balanced else "off the books!",
                             delta_color="off" if balanced else "inverse")
                if s["note"]:
                    if s["kind"] in ("fail",):
                        st.error(s["note"])
                    elif s["kind"] in ("commit", "rollback"):
                        st.success(s["note"])
                    else:
                        st.info(s["note"])

        st.divider()
        if fail:
            st.success("**Takeaway:** the failure left the database exactly "
                       "as it started. `ROLLBACK` guarantees a half-finished "
                       "transaction never corrupts your data.")
        else:
            st.success("**Takeaway:** `COMMIT` made both writes permanent "
                       "together. A reader never sees just one half of a "
                       "transaction.")

    show_sql("""
-- The whole demo is just these statements on an isolated in-memory table:
BEGIN TRANSACTION;
  UPDATE demo_tills SET balance = balance - 40 WHERE name = 'Front Till';
  UPDATE demo_tills SET balance = balance + 40 WHERE name = 'Drive-Thru Till';
COMMIT;     -- ...or ROLLBACK; to undo BOTH updates atomically
""", "🔍 Show the SQL this page runs")
