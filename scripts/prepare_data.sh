#!/bin/sh
set -eu
. "$(dirname -- "$0")/_common.sh"
[ "$#" -eq 1 ] || { echo 'Usage: prepare_data.sh public-data-root' >&2; exit 2; }
exec "$PAIEC_PYTHON" -B src/prepare_data.py --source "$1" --out "$PAIEC_RUN_DIR/data"
