#!/usr/bin/env bash
set -euo pipefail
TARGETS=(
  10.44.10.11
  10.44.10.21
  10.44.10.41
  10.44.10.61
  10.44.10.71
)
for target in "${TARGETS[@]}"; do
  echo "PING ${target}"
  ping -c 2 -W 1 "${target}" || true
  echo
 done
