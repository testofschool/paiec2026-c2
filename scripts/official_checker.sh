#!/bin/sh
set -eu
. "$(dirname -- "$0")/_common.sh"
: "${PAIEC_CHECKER_DIR:?Set the independently supplied official baseline directory}"
exec "$PAIEC_PYTHON" -B src/check_official.py --checker-dir "$PAIEC_CHECKER_DIR" --zip "$PAIEC_RUN_DIR/dist/C2_r1.zip"
