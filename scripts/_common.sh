#!/bin/sh
set -eu
PAIEC_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
: "${PAIEC_RUN_DIR:?Set an external fresh run directory}"
: "${PAIEC_PYTHON:?Set the fresh virtual environment interpreter}"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$PAIEC_RUN_DIR/bytecode"
unset PYTHONPATH PYTHONHOME
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
cd "$PAIEC_ROOT"
