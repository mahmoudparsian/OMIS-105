#!/usr/bin/env python3
"""Smoke-test plot_util against every plotted query using real result data.

Builds a pandas DataFrame from each query's SQLite result (column access works
the same as the polars/pandas frames marimo will hand the notebook) and calls
the matching plot_util function, confirming a Figure is produced with no error.
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import query_specs
import plot_util
from test_queries import load_db, sqlite_compat
import matplotlib.pyplot as plt

con = load_db()
specs = query_specs.NB1 + query_specs.NB2
plotted = [s for s in specs if s.get("plot")]
ok = 0
for spec in plotted:
    cur = con.execute(sqlite_compat(spec["sql"]))
    cols = [d[0] for d in cur.description]
    df = pd.DataFrame(cur.fetchall(), columns=cols)
    fig = plot_util.plot(df, spec["plot"])
    assert fig is not None and hasattr(fig, "savefig"), spec["id"]
    # ensure it can actually render
    fig.savefig("/tmp/_plot_check.png", dpi=60)
    plt.close(fig)
    ok += 1
    print(f"  {spec['id']:24s} {spec['plot']['kind']:5s} -> Figure OK ({len(df)} rows)")

print(f"\nRESULT: {ok}/{len(plotted)} plots rendered with no error")
