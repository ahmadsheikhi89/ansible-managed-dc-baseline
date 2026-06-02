# Runbook 04 - Safe Cleanup and Archive

## Goal

Move intermediate evidence into a dated archive without committing private or temporary files.

## Commands

```bash
archive_dir="archive/$(date +%Y%m%d)-baseline-run"
mkdir -p "${archive_dir}"
cp -a reports/final reports/firewall reports/repo-cleanup reports/exceptions "${archive_dir}/"
find "${archive_dir}" -type f -name '*.tmp' -delete
```

## Safety checks

```bash
grep -RInE 'password|secret|token|PRIVATE KEY|BEGIN RSA|BEGIN OPENSSH' "${archive_dir}" || true
```
