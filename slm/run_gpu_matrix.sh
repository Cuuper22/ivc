#!/usr/bin/env bash
# Start the run matrix on a GPU host. This is what the Modal launcher executes,
# and it is also the way to run the matrix by hand on any rented machine.
#
# Fail loudly and early: unset variables and any failing command stop the script,
# because a half-run matrix that keeps going still costs money by the hour.
set -euo pipefail

cd "$(dirname "$0")"
# Unbuffered output so progress is visible in the host log while the run is live.
export PYTHONUNBUFFERED=1
# Results go to attached storage when the caller says so; otherwise beside the
# package. Checkpoints are large and are not repository artifacts.
export IVCSLM_OUTPUT_DIR="${IVCSLM_OUTPUT_DIR:-$PWD/runs}"
# No default rate. The budget guard is only meaningful with the provider's actual
# all-in rate, so refuse to start rather than guess one.
: "${IVCSLM_HOURLY_RATE_USD:?Set IVCSLM_HOURLY_RATE_USD to the provider actual all-in hourly rate}"
# Billing starts when the machine was allocated, not when this script ran. A
# caller who knows the real start time passes it in; otherwise now is the closest
# honest estimate available here.
export IVCSLM_BILLED_START_UNIX="${IVCSLM_BILLED_START_UNIX:-$(date +%s)}"
# Editable install so the container runs the source that was shipped into it.
python -m pip install --disable-pip-version-check -e .
python -m ivcslm run-matrix \
  --config "${IVCSLM_CONFIG:-configs/ivc_research_14usd.json}" \
  --scope "${IVCSLM_RUN_SCOPE:-full}"
