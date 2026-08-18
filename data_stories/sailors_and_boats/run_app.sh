#!/usr/bin/env bash
#
# Launch the Sailors & Boats Streamlit application.
#
#   ./run_app.sh                          # the project's own database
#   ./run_app.sh /path/to/other.duckdb    # any other database
#   ./run_app.sh demo.duckdb --server.port 8600
#
# The first argument, if given, is the DuckDB database to open; anything after
# it is passed straight through to `streamlit run`. Works from any directory.
#
# The app WRITES to this database -- registrations and reservations land in the
# file you name. To experiment without touching the seeded data, copy it first:
#
#     cp sailors_and_boats.duckdb /tmp/scratch.duckdb
#     ./run_app.sh /tmp/scratch.duckdb

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

load_dotenv
require_uv
require_db
warn_if_locked "Marimo notebook" "marimo edit"

announce "Starting the marina desk app."
echo "  Press Ctrl-C to stop it."
echo

# src/sailors_db.py reads SAILORS_DB, so the app, its writes, and anything it
# imports all point at the same file.
export SAILORS_DB="$DB"

exec uv run streamlit run app/streamlit_app.py "$@"
