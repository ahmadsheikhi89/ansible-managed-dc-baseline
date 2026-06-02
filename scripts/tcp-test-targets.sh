#!/usr/bin/env bash
set -euo pipefail

targets_file="${1:-/dev/stdin}"

while read -r host port; do
  [[ -z "${host:-}" || -z "${port:-}" ]] && continue
  printf 'TCP_TEST target=%s port=%s ' "${host}" "${port}"
  timeout 2 bash -c "</dev/tcp/${host}/${port}" >/dev/null 2>&1 && echo "OK" || echo "FAILED"
done < "${targets_file}"
