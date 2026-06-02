#!/usr/bin/env bash
set -euo pipefail
TESTS=(
  "10.44.10.11 22"
  "10.44.10.61 443"
  "10.44.10.63 8081"
  "10.44.10.71 3000"
)
for item in "${TESTS[@]}"; do
  host="${item% *}"
  port="${item#* }"
  echo "TCP ${host}:${port}"
  nc -vz -w 3 "${host}" "${port}" || true
  echo
 done
