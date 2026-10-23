#!/bin/sh
set -eu
. "$(dirname -- "$0")/_common.sh"
exec "$PAIEC_PYTHON" -B src/build_zip.py --out "$PAIEC_RUN_DIR/dist/C2_r1.zip"
