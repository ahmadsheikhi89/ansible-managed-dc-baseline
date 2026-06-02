#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
input_dir="${repo_root}/reports/lynis"
output_file="${repo_root}/reports/61-lynis-rocky-summary.csv"

mkdir -p "$(dirname "${output_file}")"
printf 'inventory_hostname|ansible_host|service_name|real_hostname|os|version|hardening_index|tests_done|warnings|suggestions|status|notes\n' > "${output_file}"

if compgen -G "${input_dir}/*.dat" > /dev/null; then
  for file in "${input_dir}"/*.dat; do
    hostid="$(awk -F= '/^hostid=/{print $2}' "${file}" | head -1)"
    index="$(awk -F= '/^hardening_index=/{print $2}' "${file}" | head -1)"
    warnings="$(awk -F= '/^warnings=/{print $2}' "${file}" | head -1)"
    suggestions="$(awk -F= '/^suggestions=/{print $2}' "${file}" | head -1)"
    printf '%s|synthetic|unknown|%s.atlasforge.example|Rocky|9.4|%s|N/A|%s|%s|OK|Rebuilt from synthetic Lynis dat file\n' \
      "${hostid:-unknown}" "${hostid:-unknown}" "${index:-N/A}" "${warnings:-N/A}" "${suggestions:-N/A}" >> "${output_file}"
  done
else
  echo "No Lynis .dat files found under ${input_dir}" >&2
fi

echo "Rebuilt ${output_file}"
