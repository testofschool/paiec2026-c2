#!/bin/sh
set -eu
. "$(dirname -- "$0")/_common.sh"
exec "$PAIEC_PYTHON" -B src/train.py --data "$PAIEC_RUN_DIR/data" --out "$PAIEC_RUN_DIR/artifacts"
