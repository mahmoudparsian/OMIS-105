#!/usr/bin/env bash
#
# Open the Sailors & Boats Marimo notebook.
#
#   ./run_notebook.sh                          # the project's own database
#   ./run_notebook.sh /path/to/other.duckdb    # any other database
#   ./run_notebook.sh demo.duckdb --port 2719
#
# The first argument, if given, is the DuckDB database to open; anything after
# it is passed straight through to `marimo edit`. Works from any directory.
#
# The notebook opens the database READ-ONLY -- it explores, it never writes.
# That also means it cannot start while the Streamlit app holds the file: DuckDB
# allows many readers or one writer, never both at once.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=_shared.sh
source "$PROJECT_DIR/_shared.sh"

case "${1:-}" in
    -h|--help) show_help "${BASH_SOURCE[0]}"; exit 0 ;;
esac

# Resolve the database BEFORE changing directory -- a relative path belongs to
# the caller's working directory, not the project's.
resolve_db "${1:-}"
# Only consume the first argument if resolve_db took it as the database.
[ "${DB_IS_DEFAULT:-1}" -eq 0 ] && shift || true

cd "$PROJECT_DIR"

open_notebook notebooks/notebook_guided.py "$@"
