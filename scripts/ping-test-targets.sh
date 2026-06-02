#!/usr/bin/env bash
set -euo pipefail

inventory_file="${1:-inventory/hosts.yml}"

if [[ ! -f "${inventory_file}" ]]; then
  echo "Inventory file not found: ${inventory_file}" >&2
  exit 1
fi

grep -E 'ansible_host:' "${inventory_file}" | awk '{print $2}' | while read -r ip; do
  printf 'PING_TEST target=%s ' "${ip}"
  ping -c 1 -W 1 "${ip}" >/dev/null 2>&1 && echo "OK" || echo "FAILED"
done
