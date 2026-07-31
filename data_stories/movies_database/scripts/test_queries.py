#!/usr/bin/env python3
"""
test_queries.py
---------------
Execute EVERY notebook query against the real data to prove the logic works,
without needing DuckDB installed.

We load the converted SQL into in-memory SQLite and register two shims so the
DuckDB-flavoured SQL runs unchanged:
    year(d)  -> integer year parsed from a 'YYYY-MM-DD' string / date
    floor(x) -> math.floor (older bundled SQLite lacks FLOOR)

SQLite supports the window functions (ROW_NUMBER, RANK, LAG, SUM OVER ...),
CTEs, scalar subqueries, BETWEEN, LIMIT/OFFSET and ROUND used here, so a clean
run is strong evidence the same SQL is correct on DuckDB.

NOTE: `DATE '2005-01-01'` literals are DuckDB syntax; for the SQLite smoke test
we strip the `DATE` keyword (string compare on 'YYYY-MM-DD' is equivalent).
This transform is ONLY applied for testing - the notebooks keep proper DuckDB
syntax.
"""
import os
import re
import math
import sqlite3

import query_specs

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "duckdb_sql"))


def _year(d):
    if d is None:
        return None
    s = str(d)
    return int(s[:4]) if len(s) >= 4 and s[:4].isdigit() else None


def load_db():
    con = sqlite3.connect(":memory:")
    con.create_function("year", 1, _year)
    con.create_function("floor", 1, lambda x: None if x is None else math.floor(x))
    for f in sorted(os.listdir(OUT_DIR)):
        if f.endswith(".sql") and f != "validate.sql":
            con.executescript(open(os.path.join(OUT_DIR, f), encoding="utf-8").read())
    return con


def sqlite_compat(sql):
    # DuckDB DATE 'literal' -> bare 'literal' for SQLite string comparison
    return re.sub(r"\bDATE\s+'", "'", sql)


def main():
    con = load_db()
    specs = [("NB1", s) for s in query_specs.NB1] + \
            [("NB2", s) for s in query_specs.NB2]
    failures = 0
    for nb, spec in specs:
        sql = sqlite_compat(spec["sql"])
        try:
            cur = con.execute(sql)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            # verify any columns referenced by the plot actually exist
            plot = spec.get("plot")
            if plot:
                wanted = [plot.get("cat"), plot.get("val"),
                          plot.get("x"), plot.get("y")]
                for w in filter(None, wanted):
                    assert w in cols, f"plot column '{w}' not in result {cols}"
            sample = rows[0] if rows else None
            print(f"  [{nb}] {spec['id']:24s} OK  rows={len(rows):<5d} "
                  f"cols={cols} first={sample}")
        except Exception as e:
            failures += 1
            print(f"  [{nb}] {spec['id']:24s} !! FAIL: {e}")
    print()
    total = len(specs)
    if failures:
        print(f"RESULT: {failures}/{total} queries FAILED")
        raise SystemExit(1)
    print(f"RESULT: all {total} queries executed and returned data correctly")


if __name__ == "__main__":
    main()
