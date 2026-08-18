#!/usr/bin/env bash
#
# Run the Sailors & Boats smoke tests.
#
#   ./run_tests.sh                          # the project's own database
#   ./run_tests.sh /path/to/other.duckdb    # any other database
#
# Works from any directory. Exits 0 if every check passes, 1 otherwise, so it
# drops straight into a grading script or a pre-commit hook.
#
# The suite builds the database if the named file does not exist yet, and never
# clobbers one that does -- it does its write testing against a throwaway copy.

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

cd "$PROJECT_DIR"

load_dotenv
require_uv
# No require_db here: tests/test_smoke.py builds one if it is missing.
warn_if_locked "Marimo notebook" "marimo edit"
warn_if_locked "Streamlit app" "streamlit run app/streamlit_app.py"

announce "Running smoke tests with $(uv --version)."

export SAILORS_DB="$DB"

# `uv run` syncs the locked environment first, so a fresh clone needs no setup.
uv run python tests/test_smoke.py "$@"
