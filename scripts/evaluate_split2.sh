#!/bin/sh
set -eu
. "$(dirname -- "$0")/_common.sh"
exec "$PAIEC_PYTHON" -B src/evaluate.py --data "$PAIEC_RUN_DIR/data" --artifacts "$PAIEC_RUN_DIR/artifacts" --out "$PAIEC_RUN_DIR/eval_split2" --split split2
