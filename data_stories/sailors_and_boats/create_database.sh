#!/usr/bin/env bash
#
# Create the Sailors & Boats database from the SQL files in database/sql/.
#
#   ./create_database.sh                          # create the project's database
#   ./create_database.sh --verify                 # create it, then try 10 forbidden inserts
#   ./create_database.sh /tmp/scratch.duckdb      # create one somewhere else
#   ./create_database.sh --force                  # replace an existing database
#
# Every database/sql/*.sql file runs in filename order, so the numeric prefixes are the
# execution order: 01_schema.sql builds the tables and constraints, then
# 02_data.sql loads the rows. Adding database/sql/03_something.sql is enough to have it
# run — nothing here lists filenames.
#
# The database is a build artifact: this script is how you regenerate it, and
# database/sql/ is the source of truth. It will NOT overwrite an existing database
# unless you pass --force, because the app writes real rows into it.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=_shared.sh
source "$PROJECT_DIR/_shared.sh"

case "${1:-}" in
    -h|--help) show_help "${BASH_SOURCE[0]}"; exit 0 ;;
esac

resolve_db "${1:-}"
# Only consume the first argument if resolve_db took it as the database.
[ "${DB_IS_DEFAULT:-1}" -eq 0 ] && shift || true

FORCE=0
VERIFY=0
for arg in "$@"; do
    case "$arg" in
        --force)  FORCE=1 ;;
        --verify) VERIFY=1 ;;
        *) echo "error: unknown option '$arg' (expected --force or --verify)" >&2; exit 2 ;;
    esac
done

cd "$PROJECT_DIR"

# When the caller named a database, echo it back in the suggested commands so
# they can be copy-pasted; when they used the default, leave it off.
DB_ARG=""
[ "${DB_IS_DEFAULT:-1}" -eq 0 ] && DB_ARG=" \"$DB\""

load_dotenv
require_uv
warn_if_locked "Marimo notebook" "marimo edit"
warn_if_locked "Streamlit app" "streamlit run app/streamlit_app.py"

# --- refuse to silently destroy data ----------------------------------------
# `build()` deletes the file before recreating it. That is correct for a build
# artifact and wrong for a database somebody has been registering sailors into,
# so an existing file needs an explicit --force.
if [ -f "$DB" ] && [ "$FORCE" -eq 0 ]; then
    echo "error: a database already exists at"                            >&2
    echo "         $DB"                                                   >&2
    echo                                                                  >&2
    if rows=$(uv run python -c "
import duckdb, sys
try:
    c = duckdb.connect(sys.argv[1], read_only=True)
    print('%d sailors, %d boats, %d reservations' % c.execute(
        'SELECT (SELECT count(*) FROM sailors), (SELECT count(*) FROM boats),'
        ' (SELECT count(*) FROM reserves)').fetchone())
except Exception:
    print('unreadable — it may be open in another program')
" "$DB" 2>/dev/null); then
        echo "       It currently holds $rows."                           >&2
    fi
    echo                                                                  >&2
    echo "Recreating it from database/sql/ would discard anything added through the"  >&2
    echo "app. If that is what you want:"                                 >&2
    echo                                                                  >&2
    echo "    ./create_database.sh${DB_ARG} --force"                     >&2
    exit 3
fi

announce "Creating the database from database/sql/*.sql."

echo "  scripts, in order:"
for f in database/sql/*.sql; do
    echo "    $f"
done
echo

export SAILORS_DB="$DB"

if [ "$VERIFY" -eq 1 ]; then
    uv run python src/build_database.py --verify
else
    uv run python src/build_database.py
fi

echo
echo "Done. Next:"
echo "    ./run_app.sh${DB_ARG}        # the marina desk app"
echo "    ./run_notebook.sh${DB_ARG}   # the guided SQL notebook"
echo "    ./run_notebook_level_01.sh${DB_ARG}   # ..._02, _03, _04 -- the four levels"
echo "    ./run_tests.sh${DB_ARG}      # the full suite"
