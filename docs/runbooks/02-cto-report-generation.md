# Runbook 02 - CTO Report Generation

## Inputs

- `reports/final/99-managed-dc-baseline-readonly.csv`
- `reports/61-lynis-rocky-summary.csv`
- `reports/exceptions/74-firewalld-operational-exceptions.csv`
- `reports/firewall/73-gitlab-firewalld-readonly-report.csv`
- `reports/repo-cleanup/69-external-repo-refs-report.csv`

## Generate Excel

```bash
python3 scripts/build-final-manager-excel.py
```

## Generate HTML

```bash
python3 scripts/build-final-manager-report.py
```

## Review checklist

- Dashboard KPIs match expected totals.
- Exception hosts are limited to GitLab and Runner.
- External repository references are zero.
- HTML charts render from local SVG files.
