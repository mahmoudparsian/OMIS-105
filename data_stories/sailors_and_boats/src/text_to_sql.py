"""Text-to-SQL for the Sailors & Boats database, using the Claude API.

Two jobs live here:

1. **Harvest metadata.** We know this database exactly, so we tell Claude
   exactly — DDL, grain, row counts, the full value list for every
   low-cardinality column, the date range, sample rows, the join graph, the
   DuckDB dialect notes, and the traps in the data. Text-to-SQL accuracy is
   mostly a function of how well the schema is described; guessing is what
   makes these systems wrong.

2. **Refuse to run anything that isn't a read.** Generated SQL is untrusted
   input. `validate_select` parses it with DuckDB's own parser rather than
   pattern-matching the text, which is the difference between a guard and a
   speed bump.

The metadata is introspected from the live database rather than pasted in, so
it cannot drift from the schema the query will actually run against.
"""

from __future__ import annotations

import datetime as dt
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import duckdb

# Overridable via ANTHROPIC_MODEL (the .env defines it). Claude Opus 5 is the
# default: it thinks by default, takes the full effort ladder, and its 512-token
# prompt-cache minimum is the lowest of the current models, which matters
# because the schema brief is the cached part of every request.
MODEL = os.environ.get("ANTHROPIC_MODEL") or "claude-opus-5"
MAX_TOKENS = 8000

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Table functions a question could legitimately need. Everything else --
# read_csv, read_parquet, read_json, glob, read_text, duckdb_settings, ... --
# is a filesystem or catalog read wearing a SELECT costume, so the allowlist
# is short on purpose.
ALLOWED_TABLE_FUNCTIONS = {"generate_series", "range", "unnest"}


class SqlSafetyError(Exception):
    """The generated SQL is not a plain read and will not be executed."""


# ---------------------------------------------------------------------------
# 2. Safety: is this actually a read-only single SELECT?
# ---------------------------------------------------------------------------

def _walk(node: Any):
    """Yield every dict in a nested JSON structure."""
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from _walk(item)


def validate_select(sql: str, con: duckdb.DuckDBPyConnection) -> None:
    """Raise SqlSafetyError unless `sql` is exactly one read-only SELECT.

    Uses `json_serialize_sql`, which is DuckDB's *own* parser, instead of
    matching on the text. A regex looking for a leading "select" is defeated by
    a leading comment, a CTE, or a second statement after a semicolon; the
    parser is not. Anything DuckDB will not serialise as a single SELECT --
    INSERT, UPDATE, DELETE, DROP, ATTACH, COPY ... TO, PRAGMA, INSTALL, or two
    statements separated by `;` -- is rejected here.

    The one case the statement type does not catch is a SELECT that reads the
    filesystem through a table function (`SELECT * FROM read_csv('/etc/passwd')`
    parses as an ordinary SELECT). So table functions are allowlisted too.
    """
    if not sql or not sql.strip():
        raise SqlSafetyError("The query is empty.")

    try:
        raw = con.execute("SELECT json_serialize_sql(?)", [sql]).fetchone()[0]
        ast = json.loads(raw)
    except Exception as exc:  # malformed beyond parsing
        raise SqlSafetyError(f"DuckDB could not parse this as SQL: {exc}") from exc

    if ast.get("error"):
        raise SqlSafetyError(
            "Only a single read-only SELECT is allowed. DuckDB rejected this "
            f"statement: {ast.get('error_message', 'not a SELECT statement')}"
        )

    statements = ast.get("statements", [])
    if len(statements) != 1:
        raise SqlSafetyError(
            f"Expected exactly one statement, got {len(statements)}. "
            "Multiple statements separated by ';' are not allowed."
        )

    node_type = statements[0].get("node", {}).get("type")
    if node_type != "SELECT_NODE":
        raise SqlSafetyError(f"Only SELECT is allowed here (got {node_type}).")

    for node in _walk(ast):
        if node.get("type") == "TABLE_FUNCTION":
            name = (node.get("function") or {}).get("function_name", "?")
            if name.lower() not in ALLOWED_TABLE_FUNCTIONS:
                raise SqlSafetyError(
                    f"The table function {name}() is not allowed -- it can read "
                    f"outside the database. Allowed: "
                    f"{', '.join(sorted(ALLOWED_TABLE_FUNCTIONS))}."
                )


# ---------------------------------------------------------------------------
# 1. Metadata harvesting
# ---------------------------------------------------------------------------

@dataclass
class Metadata:
    """Everything Claude needs to know about this database, introspected live."""

    ddl: str
    columns: list[dict] = field(default_factory=list)
    row_counts: dict[str, int] = field(default_factory=dict)
    enumerations: dict[str, list] = field(default_factory=dict)
    ranges: dict[str, dict] = field(default_factory=dict)
    samples: dict[str, list[dict]] = field(default_factory=dict)


def harvest(con: duckdb.DuckDBPyConnection) -> Metadata:
    """Introspect the live database. Never hand-maintained, so never stale."""
    ddl_rows = con.execute(
        """
        SELECT sql FROM duckdb_tables()
        WHERE schema_name = 'main' ORDER BY table_name
        """
    ).fetchall()
    ddl = "\n\n".join(r[0] for r in ddl_rows if r[0])

    columns = con.execute(
        """
        SELECT table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'main'
        ORDER BY table_name, ordinal_position
        """
    ).df().to_dict("records")

    row_counts = {
        t: con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        for t in ("sailors", "boats", "reserves")
    }

    # Every distinct value of every low-cardinality column. This is the single
    # highest-value piece of metadata for text-to-SQL: without it the model
    # guesses 'Red' when the data says 'red', and the query silently returns
    # nothing. With it, the guess is impossible.
    enumerations = {
        "boats.color": [r[0] for r in con.execute(
            "SELECT DISTINCT color FROM boats ORDER BY color").fetchall()],
        "boats.bname": [r[0] for r in con.execute(
            "SELECT DISTINCT bname FROM boats ORDER BY bname").fetchall()],
        "sailors.sname": [r[0] for r in con.execute(
            "SELECT DISTINCT sname FROM sailors ORDER BY sname").fetchall()],
        "sailors.rating": [r[0] for r in con.execute(
            "SELECT DISTINCT rating FROM sailors WHERE rating IS NOT NULL "
            "ORDER BY rating").fetchall()],
    }

    ranges = {
        "reserves.day": dict(zip(
            ("min", "max", "distinct_days"),
            con.execute(
                "SELECT min(day), max(day), count(DISTINCT day) FROM reserves"
            ).fetchone(),
        )),
        "sailors.age": dict(zip(
            ("min", "max"),
            con.execute("SELECT min(age), max(age) FROM sailors").fetchone(),
        )),
        "sailors.rating": dict(zip(
            ("min", "max", "n_null"),
            con.execute(
                "SELECT min(rating), max(rating), "
                "count(*) FILTER (WHERE rating IS NULL) FROM sailors"
            ).fetchone(),
        )),
    }

    samples = {
        t: con.execute(f"SELECT * FROM {t} ORDER BY 1 LIMIT 5").df().to_dict("records")
        for t in ("sailors", "boats", "reserves")
    }

    return Metadata(ddl=ddl, columns=columns, row_counts=row_counts,
                    enumerations=enumerations, ranges=ranges, samples=samples)


def _fmt(value: Any) -> str:
    if isinstance(value, (dt.date, dt.datetime)):
        return value.strftime("%Y-%m-%d")
    return str(value)


def build_schema_brief(meta: Metadata) -> str:
    """Render the metadata as the schema section of the system prompt.

    Ordered stable-first so it caches as one prefix: the brief never varies
    between questions, so it is written once to the prompt cache and read back
    at roughly a tenth the price on every question after the first.
    """
    lines: list[str] = []

    lines.append("## Tables (exact DDL, read from the live database)\n")
    lines.append("```sql")
    lines.append(meta.ddl.strip())
    lines.append("```\n")

    lines.append("## What one row means (the grain)\n")
    lines.append("- `sailors` — one person. Key `sid`.")
    lines.append("- `boats` — one physical hull. Key `bid`.")
    lines.append("- `reserves` — **one boat, on one day.** Key `(bid, day)`,")
    lines.append("  plus `UNIQUE (sid, day)`.")
    lines.append("")
    lines.append("The `reserves` grain is the thing to internalise. The primary key is")
    lines.append("`(bid, day)`, NOT `(sid, bid, day)`. Consequences you can rely on:")
    lines.append("")
    lines.append("- A boat has **at most one** holder on any given day. A query asking")
    lines.append("  \"who has boat 101 on 1998-10-10\" returns 0 or 1 rows, never more.")
    lines.append("- A sailor has **at most one** boat on any given day — the mirror")
    lines.append("  rule, from `UNIQUE (sid, day)`. \"What did Dustin sail on")
    lines.append("  1998-10-10\" also returns 0 or 1 rows. So on any single day the")
    lines.append("  sailors out and the boats out are matched one-to-one, and")
    lines.append("  `count(*)` over a day counts both.")
    lines.append("- Therefore a question like \"who had more than one boat at once\"")
    lines.append("  has no answer in this database — the schema forbids it. Say so")
    lines.append("  rather than writing a query that returns nothing.")
    lines.append("- \"Is boat B free on day D\" is `NOT EXISTS (SELECT 1 FROM reserves")
    lines.append("  WHERE bid = B AND day = D)`. Free and booked are complements.")
    lines.append("  \"Is sailor S free on day D\" is the same shape on `sid`.\n")

    lines.append("## Row counts\n")
    for table, n in meta.row_counts.items():
        lines.append(f"- `{table}`: {n} rows")
    lines.append("")

    lines.append("## Exact column values (use these literals verbatim)\n")
    for col, values in meta.enumerations.items():
        shown = ", ".join(repr(v) for v in values)
        lines.append(f"- `{col}` — {len(values)} distinct: {shown}")
    lines.append("")
    lines.append("Colours are stored lower-case and constrained by a CHECK, so")
    lines.append("`WHERE color = 'red'` is correct and `'Red'` matches nothing.\n")

    lines.append("## Ranges\n")
    for col, r in meta.ranges.items():
        parts = ", ".join(f"{k}={_fmt(v)}" for k, v in r.items())
        lines.append(f"- `{col}` — {parts}")
    lines.append("")

    lines.append("## Sample rows\n")
    for table, rows in meta.samples.items():
        lines.append(f"`{table}` (first {len(rows)}):")
        lines.append("```")
        for row in rows:
            lines.append("  " + "  ".join(f"{k}={_fmt(v)}" for k, v in row.items()))
        lines.append("```")
    lines.append("")

    lines.append("## Join graph\n")
    lines.append("There is exactly one path between sailors and boats, through `reserves`:")
    lines.append("")
    lines.append("```")
    lines.append("  sailors.sid  ──<  reserves.sid")
    lines.append("  boats.bid    ──<  reserves.bid")
    lines.append("```")
    lines.append("")
    lines.append("```sql")
    lines.append("FROM sailors s")
    lines.append("JOIN reserves r ON r.sid = s.sid")
    lines.append("JOIN boats    b ON b.bid = r.bid")
    lines.append("```")
    lines.append("")
    lines.append("There is no direct sailors↔boats relationship. A question about")
    lines.append("sailors and boats together always goes through `reserves`.\n")

    lines.append("## Traps in this specific data\n")
    lines.append("- **Two different sailors are named 'Horatio'** (sid 64 and sid 74).")
    lines.append("  Never join or group on `sname` — use `sid`.")
    lines.append("- **Two different boats are named 'Interlake'** (bid 101 and 102).")
    lines.append("  Same rule: identity is `bid`.")
    lines.append("- **Some sailors have `rating IS NULL`.** `AVG(rating)` skips them,")
    lines.append("  `COUNT(*)` counts them, `COUNT(rating)` does not, and")
    lines.append("  `GROUP BY rating` gives NULL its own group. `WHERE rating > 5`")
    lines.append("  silently excludes them — add `OR rating IS NULL` if they belong.")
    lines.append("- **Some sailors have never reserved anything, and some boats have")
    lines.append("  never been reserved.** Any 'who has never…' / 'which were never…'")
    lines.append("  question needs `LEFT JOIN … WHERE … IS NULL` or `NOT EXISTS` — an")
    lines.append("  inner join drops exactly the rows the question is asking for.")
    lines.append("- **The database stores no row for a day on which nothing happened.**")
    lines.append("  Questions about idle days, utilisation, or gaps need a calendar")
    lines.append("  built with `generate_series`, left-joined to `reserves`.\n")

    lines.append("## DuckDB dialect notes\n")
    lines.append("- Dates: `DATE '1998-10-10'`, `date_trunc('month', day)`,")
    lines.append("  `strftime(day, '%Y-%m-%d')`, `day - INTERVAL 7 DAY`. Subtracting")
    lines.append("  two DATEs yields an integer number of days.")
    lines.append("- Calendar spine: "
                 "`SELECT unnest(generate_series(DATE 'a', DATE 'b', INTERVAL 1 DAY))::DATE`")
    lines.append("- Conditional aggregate: `count(*) FILTER (WHERE cond)`")
    lines.append("- `QUALIFY` filters window functions without a subquery.")
    lines.append("- `EXCEPT`, `INTERSECT`, `GROUP BY ALL`, and `ORDER BY ALL` all work.")
    lines.append("- String concatenation is `||`.")

    return "\n".join(lines)


# Few-shot examples. Chosen to cover the shapes that go wrong most often --
# absence, division, the calendar spine, and the (bid, day) key -- rather than
# to demonstrate basic SELECT, which needs no demonstration.
FEW_SHOT = """\
## Worked examples

Q: Which boats has nobody ever reserved?
```sql
SELECT b.bid, b.bname, b.color
FROM boats b
WHERE NOT EXISTS (SELECT 1 FROM reserves r WHERE r.bid = b.bid)
ORDER BY b.bid
```
(Absence question — an inner join would return the opposite set.)

Q: Who had boat 103 on 1998-10-08?
```sql
SELECT s.sid, s.sname
FROM reserves r
JOIN sailors s ON s.sid = r.sid
WHERE r.bid = 103 AND r.day = DATE '1998-10-08'
```
(At most one row, because `(bid, day)` is the primary key.)

Q: Which sailors have reserved every red boat?
```sql
SELECT s.sid, s.sname
FROM sailors s
WHERE NOT EXISTS (
    SELECT b.bid FROM boats b WHERE b.color = 'red'
    EXCEPT
    SELECT r.bid FROM reserves r WHERE r.sid = s.sid
)
ORDER BY s.sid
```
(Relational division: "for all" is written as a double negative.)

Q: How busy was the fleet each day in October 1998?
```sql
WITH calendar AS (
    SELECT unnest(generate_series(DATE '1998-10-01', DATE '1998-10-31',
                                  INTERVAL 1 DAY))::DATE AS day
)
SELECT c.day,
       count(r.bid) AS boats_out,
       round(100.0 * count(r.bid) / (SELECT count(*) FROM boats), 1) AS pct_fleet_out
FROM calendar c
LEFT JOIN reserves r ON r.day = c.day
GROUP BY c.day
ORDER BY c.day
```
(The quiet days exist only because the calendar spine manufactures them.)

Q: How many reservations does each sailor have, including those with none?
```sql
SELECT s.sid, s.sname, count(r.bid) AS n_reservations
FROM sailors s
LEFT JOIN reserves r ON r.sid = s.sid
GROUP BY s.sid, s.sname
ORDER BY n_reservations DESC, s.sid
```
(`count(r.bid)` gives 0 for the unmatched rows; `count(*)` would give 1.)
"""

INSTRUCTIONS = """\
You translate questions about a marina database into DuckDB SQL.

Rules:
- Emit exactly one `SELECT` (a leading `WITH` is fine). Never `INSERT`,
  `UPDATE`, `DELETE`, `CREATE`, `DROP`, `ATTACH`, `COPY`, or `PRAGMA` — the
  query runs read-only and anything else is rejected before execution.
- Use only the tables, columns, and literal values given in the schema brief.
  If the question names something that is not in the data, say so in
  `assumptions` rather than inventing a column.
- Prefer explicit `JOIN … ON` over comma joins, and qualify every column with
  its table alias.
- **Never qualify a SELECT output alias.** `SELECT x AS from_day … ORDER BY
  t.from_day` is a binder error, because `from_day` is a name you invented in
  the output, not a column of `t`. In `ORDER BY` write the alias bare
  (`ORDER BY from_day`) or repeat the underlying expression
  (`ORDER BY t.prev_day`). The same applies in `GROUP BY` and `HAVING`.
- Return the columns a person actually asked for, plus the identifiers needed
  to make the answer readable — a question about sailors should return
  `sname`, not just `sid`.
- Order the result unless the question implies otherwise; an unordered result
  is not reproducible.
- If the question is ambiguous, choose the most useful reading, write the SQL
  for it, and record the choice in `assumptions`.
"""


def build_system_prompt(meta: Metadata) -> str:
    return "\n\n".join([INSTRUCTIONS, "# Database", build_schema_brief(meta), FEW_SHOT])


# ---------------------------------------------------------------------------
# The API call
# ---------------------------------------------------------------------------

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "sql": {
            "type": "string",
            "description": "A single DuckDB SELECT statement answering the question. No trailing semicolon.",
        },
        "explanation": {
            "type": "string",
            "description": "Two or three sentences explaining what the query does and why it is shaped that way.",
        },
        "assumptions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Any ambiguity you resolved, or anything the question asked for that the data cannot answer. Empty if the question was unambiguous.",
        },
        "confidence": {
            "type": "string",
            "enum": ["high", "medium", "low"],
            "description": "How confident you are that this SQL answers the question asked.",
        },
    },
    "required": ["sql", "explanation", "assumptions", "confidence"],
    "additionalProperties": False,
}


def credentials_available() -> bool:
    """Whether an Anthropic credential is resolvable without prompting."""
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        return True
    # `ant auth login` stores a profile the SDK picks up with no env var set.
    config = Path(os.environ.get("ANTHROPIC_CONFIG_DIR", Path.home() / ".config" / "anthropic"))
    return (config / "credentials").is_dir()


def dry_run(sql: str, con: duckdb.DuckDBPyConnection) -> str | None:
    """Bind-check a query without running it. Returns an error message or None.

    `EXPLAIN` makes DuckDB parse and bind the statement -- resolving every
    table, column and alias -- but not execute it. That catches the whole class
    of mistakes a language model actually makes (a column that does not exist,
    a qualified output alias, a typo in a CTE name) before the user clicks Run,
    and costs nothing.
    """
    try:
        con.execute("EXPLAIN " + sql)
        return None
    except Exception as exc:
        return str(exc).strip().splitlines()[0]


def repair_sql(question: str, broken_sql: str, error: str, meta: Metadata,
               model: str = MODEL, effort: str = "medium") -> dict:
    """Send a failing query back with its error and ask for a fix.

    Text-to-SQL will occasionally emit SQL that does not bind; the useful
    question is what the app does next. Handing the model the exact database
    error alongside its own query is by far the strongest repair signal
    available, and it reuses the cached schema brief, so a retry costs about
    the same as the original question.
    """
    import anthropic

    client = anthropic.Anthropic()
    ask = (
        f"This query was written to answer: {question}\n\n"
        f"```sql\n{broken_sql}\n```\n\n"
        f"The database rejected it:\n\n    {error}\n\n"
        "Return a corrected query that answers the original question. Fix the "
        "cause of this specific error rather than rewriting from scratch, and "
        "say in `assumptions` what was wrong."
    )
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=[{"type": "text", "text": build_system_prompt(meta),
                 "cache_control": {"type": "ephemeral"}}],
        output_config={"effort": effort,
                       "format": {"type": "json_schema", "schema": RESPONSE_SCHEMA}},
        messages=[{"role": "user", "content": ask}],
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("Claude declined to repair this query.")
    text = next((b.text for b in response.content if b.type == "text"), None)
    if not text:
        raise RuntimeError(f"No text in the repair response ({response.stop_reason}).")
    result = json.loads(text)
    u = response.usage
    result["_usage"] = {
        "input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
        "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", 0) or 0,
        "cache_creation_input_tokens": getattr(u, "cache_creation_input_tokens", 0) or 0,
        "model": response.model,
    }
    return result


def generate_sql(question: str, meta: Metadata, model: str = MODEL,
                 effort: str = "medium") -> dict:
    """Ask Claude for SQL. Returns the parsed structured response plus usage.

    The system prompt carries a `cache_control` breakpoint: the schema brief is
    identical for every question, so it is written to the prompt cache once and
    read back at roughly a tenth the input price on every question after — the
    brief is the bulk of the request, so this is most of the per-question cost.

    `effort` defaults to medium: schema-grounded SQL generation is not a task
    that rewards deep deliberation, and medium keeps latency usable in a UI.
    """
    import anthropic  # imported lazily so the rest of the app runs without it

    client = anthropic.Anthropic()

    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=[
            {
                "type": "text",
                "text": build_system_prompt(meta),
                # Stable across every question -> cache it.
                "cache_control": {"type": "ephemeral"},
            }
        ],
        output_config={
            "effort": effort,
            "format": {"type": "json_schema", "schema": RESPONSE_SCHEMA},
        },
        messages=[{"role": "user", "content": question}],
    )

    if response.stop_reason == "refusal":
        raise RuntimeError(
            "Claude declined to answer this question. Rephrase it and try again."
        )

    text = next((b.text for b in response.content if b.type == "text"), None)
    if not text:
        raise RuntimeError(
            f"No text in the response (stop_reason={response.stop_reason}). "
            "If this says max_tokens, the question needs a larger budget."
        )

    result = json.loads(text)
    usage = response.usage
    result["_usage"] = {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0) or 0,
        "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0) or 0,
        "model": response.model,
    }
    return result
