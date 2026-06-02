#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CSV="${ROOT_DIR}/reports/61-lynis-rocky-summary.csv"
if [[ ! -f "${CSV}" ]]; then
  echo "Missing ${CSV}" >&2
  exit 1
fi
{ head -1 "${CSV}"; tail -n +2 "${CSV}" | sort -t'|' -k8,8n; } | column -t -s '|'
