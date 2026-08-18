#!/usr/bin/env bash
#
# Shared helpers for run_app.sh, run_notebook.sh and run_tests.sh.
# Not meant to be run directly -- the other scripts `source` it.

# ---------------------------------------------------------------------------
# resolve_db <arg>
#
# Turns an optional database argument into an absolute path in $DB.
# MUST be called before cd-ing to the project, because a relative path is
# relative to wherever the user actually stood when they typed the command.
# ---------------------------------------------------------------------------
resolve_db() {
    local arg="${1:-}"
    # A leading-dash first argument is a flag for the underlying tool, not a
    # database path -- `./run_app.sh --server.port 8600` should mean the default
    # database, not a file literally named "--server.port".
    case "$arg" in
        -*) arg="" ;;
    esac
    if [ -z "$arg" ]; then
        DB="$PROJECT_DIR/sailors_and_boats.duckdb"
        DB_IS_DEFAULT=1
    else
        case "$arg" in
            /*) DB="$arg" ;;
            *)  DB="$PWD/$arg" ;;
        esac
        DB_IS_DEFAULT=0
    fi
}

# ---------------------------------------------------------------------------
# require_db  -- the database must already exist; say how to make one if not.
# ---------------------------------------------------------------------------
require_db() {
    if [ ! -f "$DB" ]; then
        echo "error: no database at $DB"                                     >&2
        echo                                                                 >&2
        echo "Build one there with:"                                         >&2
        echo "    SAILORS_DB=\"$DB\" uv run python src/build_database.py"    >&2
        echo                                                                 >&2
        echo "or omit the argument to use the project's own database."       >&2
        exit 2
    fi
}

# ---------------------------------------------------------------------------
# load_dotenv
#
# Export everything in .env if the file exists. Streamlit and marimo do NOT
# read .env on their own, and neither does the Anthropic SDK -- without this a
# key sitting in .env looks like no key at all, and the "Ask in English" page
# reports no credential.
#
# Values already in the environment win: an explicit
# `ANTHROPIC_API_KEY=... ./run_app.sh` overrides the file.
# ---------------------------------------------------------------------------
load_dotenv() {
    [ -f "$PROJECT_DIR/.env" ] || return 0
    local line key value
    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in ''|'#'*) continue ;; esac
        line="${line#export }"
        key="${line%%=*}"
        [ "$key" = "$line" ] && continue          # no '=' on this line
        key="${key%"${key##*[![:space:]]}"}"      # trim trailing space in key
        value="${line#*=}"
        value="${value#"${value%%[![:space:]]*}"}"   # trim leading space

        case "$value" in
            \"*)  value="${value#\"}"; value="${value%%\"*}" ;;   # "quoted" -- keep as-is
            \'*)  value="${value#\'}"; value="${value%%\'*}" ;;   # 'quoted' -- keep as-is
            *)
                # Unquoted: an inline comment ends the value. Without this,
                # `MODEL=claude-sonnet-4-6   # swap later` yields a model id
                # with the comment glued on, and the API 404s on it.
                value="${value%%[[:space:]]#*}"
                value="${value%"${value##*[![:space:]]}"}"   # trim trailing space
                ;;
        esac

        # Values already exported win, so `KEY=... ./run_app.sh` overrides .env.
        if [ -z "$(eval "printf '%s' \"\${$key:-}\"")" ]; then
            export "$key=$value"
        fi
    done < "$PROJECT_DIR/.env"
}

# ---------------------------------------------------------------------------
# require_uv
# ---------------------------------------------------------------------------
require_uv() {
    if ! command -v uv >/dev/null 2>&1; then
        echo "error: uv is not installed."                                  >&2
        echo "       Install it with:  brew install uv"                     >&2
        echo "       or see https://docs.astral.sh/uv/getting-started/"     >&2
        exit 127
    fi
}

# ---------------------------------------------------------------------------
# warn_if_locked <what-not-to-run>
#
# DuckDB permits one writer process. Rather than let the caller hit a lock
# error that explains nothing, name the process that is probably holding it.
# ---------------------------------------------------------------------------
warn_if_locked() {
    local other="$1" pattern="$2"
    if pgrep -f "$pattern" >/dev/null 2>&1; then
        echo "warning: a $other appears to be running."
        echo "         DuckDB allows one writer at a time, so both cannot hold"
        echo "         $(basename "$DB") open. Close it if this fails on a lock error."
        echo
    fi
}

# ---------------------------------------------------------------------------
# announce <what>
# ---------------------------------------------------------------------------
announce() {
    echo "$1"
    echo "  database: $DB"
    if [ "${DB_IS_DEFAULT:-1}" -eq 0 ]; then
        echo "            (from the command line, via SAILORS_DB)"
    fi
    echo
}

# ---------------------------------------------------------------------------
# open_notebook <notebook-path> [marimo args...]
#
# The whole body of the five run_notebook*.sh scripts: check the environment,
# say which database is being opened, and hand over to marimo. Every notebook
# in this project opens the database READ-ONLY, which is also why a running
# Streamlit app blocks it -- DuckDB allows many readers or one writer.
#
# Call it after resolve_db and after cd-ing to the project.
# ---------------------------------------------------------------------------
open_notebook() {
    local notebook="$1"; shift

    load_dotenv
    require_uv
    require_db
    warn_if_locked "Streamlit app" "streamlit run app/streamlit_app.py"

    announce "Opening $(basename "$notebook") (read-only)."
    echo "  Marimo will print a URL; Ctrl-C here closes it."
    echo

    # The notebook's first cell calls sailors_db.connect(read_only=True), which
    # resolves DB_PATH from SAILORS_DB.
    export SAILORS_DB="$DB"

    exec uv run marimo edit "$notebook" "$@"
}

# ---------------------------------------------------------------------------
# show_help <script>
#
# Prints the script's leading comment block (minus the shebang) as its usage
# text, stopping at the first line that is not a comment. Keeping this out of
# line-number ranges means editing a header can never truncate or over-run the
# help output.
# ---------------------------------------------------------------------------
show_help() {
    awk 'NR == 1 { next }
         /^#/    { sub(/^# ?/, ""); print; next }
                 { exit }' "$1"
}
