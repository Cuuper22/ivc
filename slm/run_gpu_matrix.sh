#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1
export IVCSLM_OUTPUT_DIR="${IVCSLM_OUTPUT_DIR:-$PWD/runs}"
: "${IVCSLM_HOURLY_RATE_USD:?Set IVCSLM_HOURLY_RATE_USD to the provider actual all-in hourly rate}"
export IVCSLM_BILLED_START_UNIX="${IVCSLM_BILLED_START_UNIX:-$(date +%s)}"
python -m pip install --disable-pip-version-check -e .
python -m ivcslm run-matrix \
  --config "${IVCSLM_CONFIG:-configs/ivc_research_14usd.json}" \
  --scope "${IVCSLM_RUN_SCOPE:-full}"
